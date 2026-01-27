"""
FastAPI Application with Monitoring and Logging

Enhanced version of app.py with:
- Request/response logging
- Prometheus metrics
- Performance tracking
"""

import time
import logging
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import sys
from pathlib import Path

# Import original app components
sys.path.append(str(Path(__file__).parent.parent.parent / 'Part2' / 'src'))
from app import load_model, preprocess_image, model, device, class_names

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
    datefmt='%Y-%m-%dT%H:%M:%SZ'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

model_predictions_total = Counter(
    'model_predictions_total',
    'Total model predictions',
    ['prediction_class']
)

model_prediction_duration_seconds = Histogram(
    'model_prediction_duration_seconds',
    'Model prediction duration in seconds'
)

app = FastAPI(title="Cats vs Dogs Classification API with Monitoring", version="1.1.0")


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        load_model()
        logger.info("Model loaded successfully", extra={"device": str(device)})
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log requests and track metrics"""
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Log request (excluding sensitive data)
    log_data = {
        "method": request.method,
        "endpoint": str(request.url.path),
        "status_code": response.status_code,
        "latency_ms": round(duration * 1000, 2)
    }
    
    logger.info("Request processed", extra=log_data)
    
    # Update metrics
    http_requests_total.labels(
        method=request.method,
        endpoint=str(request.url.path),
        status=response.status_code
    ).inc()
    
    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=str(request.url.path)
    ).observe(duration)
    
    return response


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": str(device)
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Predict image class with logging"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    start_time = time.time()
    
    try:
        # Read and preprocess image
        import io
        from PIL import Image
        import torch
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Preprocess
        image_tensor = preprocess_image(image)
        
        # Predict
        with torch.no_grad():
            pred_start = time.time()
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            pred_duration = time.time() - pred_start
        
        # Format response
        pred_class = class_names[predicted.item()]
        confidence_score = confidence.item()
        
        probs = probabilities[0].cpu().numpy()
        prob_dict = {
            class_names[i]: float(probs[i]) 
            for i in range(len(class_names))
        }
        
        # Log prediction (excluding image data)
        log_data = {
            "endpoint": "/predict",
            "prediction": pred_class,
            "confidence": round(confidence_score, 4),
            "prediction_latency_ms": round(pred_duration * 1000, 2)
        }
        logger.info("Prediction made", extra=log_data)
        
        # Update metrics
        model_predictions_total.labels(prediction_class=pred_class).inc()
        model_prediction_duration_seconds.observe(pred_duration)
        
        return {
            "prediction": pred_class,
            "probabilities": prob_dict,
            "confidence": confidence_score
        }
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
