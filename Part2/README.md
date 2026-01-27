# Part 2: Model Packaging & Containerization (M2)

## Objective
Package the trained model into a reproducible, containerized service.

## Tasks

### 1. Inference Service
- Wrap trained model with REST API using **FastAPI** (recommended) or Flask
- Implement endpoints:
  - **Health Check**: `/health` - Returns service status
  - **Prediction**: `/predict` - Accepts image, returns class probabilities/label

### 2. Environment Specification
- Create `requirements.txt` with:
  - All dependencies
  - Version pinning for key ML libraries (PyTorch, NumPy, etc.)
  - FastAPI/Flask and related dependencies

### 3. Containerization
- Create `Dockerfile` to containerize the inference service
- Build and run image locally
- Verify predictions via curl/Postman

## Project Structure

```
Part2/
├── README.md                    # This file
├── src/
│   ├── app.py                   # FastAPI application
│   ├── model_loader.py          # Model loading utilities
│   └── preprocess.py            # Image preprocessing for inference
├── models/                      # Trained model (from Part1)
├── Dockerfile                   # Container definition
├── .dockerignore               # Files to exclude from Docker build
├── requirements.txt            # Python dependencies
└── test_api.py                 # Script to test API endpoints
```

## API Endpoints

### Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### Prediction
```bash
POST /predict
Content-Type: multipart/form-data

file: <image_file>
```

**Response:**
```json
{
  "prediction": "Cat",
  "probabilities": {
    "Cat": 0.85,
    "Dog": 0.15
  },
  "confidence": 0.85
}
```

## Prerequisites

```bash
pip install fastapi uvicorn python-multipart pillow torch torchvision
```

## How to Run

### 1. Local Development (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

### 2. Build Docker Image

```bash
# Build image
docker build -t cats-dogs-api:latest -f Dockerfile .

# Run container
docker run -d -p 8000:8000 --name cats-dogs-api cats-dogs-api:latest
```

### 3. Test API

```bash
# Health check
curl http://localhost:8000/health

# Prediction (using test script)
python test_api.py

# Or with curl
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/test_image.jpg"
```

## Dockerfile Structure

- Base image: Python 3.9+
- Copy requirements.txt and install dependencies
- Copy source code and model files
- Expose port 8000
- Run uvicorn server

## Expected Outputs

- Working FastAPI application
- Docker image that runs successfully
- API responds to health check and prediction requests
