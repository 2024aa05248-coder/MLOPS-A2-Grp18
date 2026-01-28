# Quick Start Guide - Assignment 2

This guide provides quick commands to get started with each part of Assignment 2.

## Prerequisites

```bash
# Initialize Git repository (required for DVC)
git init

# Install Python dependencies
pip install -r requirements.txt

# Install DVC (for Part1)
pip install dvc

# Initialize DVC (must be run from root directory)
dvc init

# Add files to Git (excluding large data that will be tracked by DVC)
git add .
git commit -m "Initial commit"

# Remove PetImages from Git tracking and add to DVC instead
git rm -r --cached PetImages
git commit -m "Stop tracking PetImages with Git"
dvc add PetImages
git add PetImages.dvc .gitignore
git commit -m "Add PetImages to DVC"
```

## Part 1: Model Development & Experiment Tracking

```bash
cd Part1

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

## Part 3: CI/CD Pipeline

### Quick Setup (5 minutes)

```bash
# 1. Configure GitHub Secrets (one-time setup)
# Go to GitHub: Settings → Secrets and variables → Actions
# Add two secrets:
#   - DOCKER_USERNAME: Your Docker Hub username
#   - DOCKER_PASSWORD: Your Docker Hub password/token

# 2. Install testing and linting tools
pip install pytest pytest-cov pytest-html flake8 pylint black isort

# 3. Run linting locally
flake8 Part1/src Part2/src
pylint Part1/src Part2/src

# 4. Auto-fix code formatting
black Part1/src Part2/src
isort Part1/src Part2/src

# 5. Run tests locally
cd Part3
pytest tests/ -v --cov=../Part1/src --cov=../Part2/src --cov-report=html

# 6. View coverage report
# Windows: start htmlcov/index.html
# macOS: open htmlcov/index.html
# Linux: xdg-open htmlcov/index.html

# 7. Push to trigger CI/CD pipeline
git add .
git commit -m "Add CI/CD pipeline"
git push origin main

# 8. View pipeline results
# Go to GitHub → Actions tab → Click on workflow run
```

### Pipeline Features

✅ **Code Linting** - flake8, pylint, black, isort
✅ **Unit Testing** - pytest with coverage reporting
✅ **Model Training** - Optional, with MLflow tracking
✅ **Docker Build** - Automated image building and push to Docker Hub
✅ **Artifacts & Logging** - Test reports, coverage, models, logs

### Pipeline Triggers

- **Push** to `main` or `develop` branches
- **Pull requests** to `main`
- **Manual trigger** with optional model training

### Quick Commands

```bash
# Before every push (recommended)
black Part1/src Part2/src && isort Part1/src Part2/src
pytest Part3/tests/ -v
```

### Documentation

- 📋 [Quick Reference](Part3/QUICK_REFERENCE.md) - Command cheatsheet
- 🚀 [Setup Guide](Part3/SETUP_GUIDE.md) - Step-by-step setup
- 📚 [Full Documentation](Part3/CI_CD_DOCUMENTATION.md) - Detailed info

### What Gets Generated

After each pipeline run:
- Linting reports (flake8, pylint, black, isort)
- Test results with coverage (HTML + XML)
- Training artifacts (if enabled)
- Trained model files (if training runs)
- Docker images pushed to Docker Hub

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
