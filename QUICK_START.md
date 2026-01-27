# Quick Start Guide - Assignment 2

This guide provides quick commands to get started with each part of Assignment 2.

## Prerequisites

```bash
# Initialize Git repository (required for DVC)
git init
git add .
git commit -m "Initial commit"

# Install Python dependencies
pip install -r requirements.txt

# Install DVC (for Part1)
pip install dvc

# Initialize DVC (must be run from root directory)
dvc init
git add .dvc .dvcignore
git commit -m "Initialize DVC"
```

## Part 1: Model Development & Experiment Tracking

```bash
cd Part1

# Add dataset to DVC
dvc add ../PetImages

# Preprocess data
python src/data_preprocessing.py

# Train model with MLflow
python src/train_model.py

# View MLflow UI
mlflow ui --backend-store-uri file://$(pwd)/mlruns
```

## Part 2: Model Packaging & Containerization

```bash
cd Part2

# Run locally (without Docker)
uvicorn src.app:app --host 0.0.0.0 --port 8000

# Test API
python test_api.py

# Build Docker image
docker build -t cats-dogs-api:latest -f Dockerfile ..

# Run Docker container
docker run -d -p 8000:8000 --name cats-dogs-api cats-dogs-api:latest

# Test Docker container
curl http://localhost:8000/health
```

## Part 3: CI Pipeline

```bash
cd Part3

# Run tests locally
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=../Part1/src --cov=../Part2/src --cov-report=html

# CI runs automatically on push to GitHub
```

## Part 4: CD Pipeline & Deployment

### Option 1: Kubernetes (kind)

```bash
# Create cluster
kind create cluster --name cats-dogs-cluster

# Load image
kind load docker-image cats-dogs-api:latest --name cats-dogs-cluster

# Deploy
cd Part4
kubectl apply -f k8s/

# Port forward
kubectl port-forward svc/cats-dogs-api-service 8000:8000

# Run smoke tests
python src/smoke_test.py
```

### Option 2: Docker Compose

```bash
cd Part4

# Update docker-compose.yml with your Docker Hub username
# Then deploy
docker-compose -f docker-compose/docker-compose.yml up -d

# Run smoke tests
python src/smoke_test.py
```

## Part 5: Monitoring

```bash
cd Part5

# Start monitoring stack
docker-compose -f docker-compose-monitoring.yml up -d

# Access:
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
# - API: http://localhost:8000
```

## Common Issues

### Model not found
- Ensure Part1 training completed successfully
- Check that `Part1/models/model.pt` exists

### Docker build fails
- Ensure all dependencies are in requirements.txt
- Check Dockerfile paths are correct

### Tests fail
- Ensure Part1 preprocessing completed
- Check that test data exists

## Next Steps

1. Complete Part 1 (data preprocessing and training)
2. Move to Part 2 (API and Docker)
3. Set up CI/CD in Part 3
4. Deploy in Part 4
5. Add monitoring in Part 5

For detailed instructions, see each part's README.md file.
