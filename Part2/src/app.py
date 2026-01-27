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
sys.path.append(str(Path(__file__).parent.parent.parent / 'Part1' / 'src'))
from train_model import SimpleCNN

app = FastAPI(title="Cats vs Dogs Classification API", version="1.0.0")

# Global variables
model = None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
class_names = ['Cat', 'Dog']


def load_model():
    """Load the trained model"""
    global model
    
    # Path to saved model
    model_path = Path(__file__).parent.parent.parent / 'Part1' / 'models' / 'model.pt'
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")
    
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
        print(f"Error loading model: {e}")
        raise


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
        raise HTTPException(status_code=503, detail="Model not loaded")
    
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
