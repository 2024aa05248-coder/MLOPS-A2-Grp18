"""
FastAPI Application for Cats vs Dogs Classification

Endpoints:
- GET /health - Health check
- POST /predict - Image classification
"""

import torch
import torch.nn as nn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
from pathlib import Path
import sys

# Add parent directory to path to import model
# Try Docker path first (/app/Part1/src), then local path
current_file = Path(__file__)
docker_path = current_file.parent.parent / 'Part1' / 'src'
local_path = current_file.parent.parent.parent / 'Part1' / 'src'

if docker_path.exists():
    sys.path.append(str(docker_path))
elif local_path.exists():
    sys.path.append(str(local_path))
else:
    raise ImportError("Cannot find Part1/src directory")

from train_model import SimpleCNN

app = FastAPI(title="Cats vs Dogs Classification API", version="1.0.0")

# Global variables
model = None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
class_names = ['Cat', 'Dog']


def load_model():
    """Load the trained model"""
    global model

    # Path to saved model - works in both Docker and local environments
    current_file = Path(__file__)
    # Try Docker path first (/app/models/model.pt)
    docker_model_path = current_file.parent.parent / 'models' / 'model.pt'
    # Then try local path
    local_model_path = current_file.parent.parent.parent / 'Part1' / 'models' / 'model.pt'

    if docker_model_path.exists():
        model_path = docker_model_path
    elif local_model_path.exists():
        model_path = local_model_path
    else:
        raise FileNotFoundError(f"Model not found at {docker_model_path} or {local_model_path}")
    
    # Initialize model
    model = SimpleCNN(num_classes=2)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    
    print(f"Model loaded from {model_path}")


def preprocess_image(image: Image.Image) -> torch.Tensor:
    """Preprocess image for inference"""
    from torchvision import transforms
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    image_tensor = transform(image).unsqueeze(0)
    return image_tensor.to(device)


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        load_model()
        print("Model loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load model: {e}")
        print("Service will start without model. Predictions will not be available.")
        # Don't raise - allow service to start without model for CI/testing


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": str(device)
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Predict image class"""
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. This may be a CI/test environment without the trained model."
        )
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Preprocess
        image_tensor = preprocess_image(image)
        
        # Predict
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        # Format response
        pred_class = class_names[predicted.item()]
        confidence_score = confidence.item()
        
        probs = probabilities[0].cpu().numpy()
        prob_dict = {
            class_names[i]: float(probs[i]) 
            for i in range(len(class_names))
        }
        
        return {
            "prediction": pred_class,
            "probabilities": prob_dict,
            "confidence": confidence_score
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
