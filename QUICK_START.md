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
 
**Code Linting** - flake8, pylint, black, isort
**Unit Testing** - pytest with coverage reporting
**Model Training** - Optional, with MLflow tracking
**Docker Build** - Automated image building and push to Docker Hub
**Artifacts & Logging** - Test reports, coverage, models, logs

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

- [Quick Reference](Part3/QUICK_REFERENCE.md) - Command cheatsheet
- [Setup Guide](Part3/SETUP_GUIDE.md) - Step-by-step setup
- [Full Documentation](Part3/CI_CD_DOCUMENTATION.md) - Detailed info

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

## Part 5: Monitoring, Logs & Performance Tracking

### Quick Start (5 minutes)

```bash
cd Part5

# 1. Install monitoring dependencies
pip install prometheus-client requests scikit-learn matplotlib seaborn

# 2. Start monitoring stack (API + Prometheus + Grafana)
docker-compose -f docker-compose-monitoring.yml up -d

# 3. Verify services are running
docker-compose -f docker-compose-monitoring.yml ps

# 4. Check API health
curl http://localhost:8001/health

# 5. Test prediction
curl -X POST "http://localhost:8001/predict" \
  -F "file=@../PetImages/Cat/0.jpg"

# 6. View metrics
curl http://localhost:8001/metrics
```

### Access Monitoring Services

- **API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (login: `admin` / `admin`)

### View Grafana Dashboard

```bash
 1. Open Grafana at http://localhost:3000
 2. Login: admin / admin
 3. Navigate to: Dashboards → "Cats vs Dogs API Monitoring"
 4. View 8 panels showing:
    - Request rate and total requests
    - P95 latency
    - Request rate by status code
    - Latency percentiles (P50, P95, P99)
    - Prediction distribution (Cat vs Dog)
    - Model inference latency
```

### Collect Performance Metrics

```bash
# Collect 100 predictions from test dataset
python src/metrics_collector.py \
  --api-url http://localhost:8000 \
  --test-data ../Part1/data/processed/test_data.json \
  --output predictions_results.json \
  --limit 100

# Calculate performance metrics
python src/performance_tracker.py \
  --predictions predictions_results.json \
  --output performance_metrics.json \
  --plot \
  --plot-output confusion_matrix.png

# Compare with training metrics (optional)
python src/performance_tracker.py \
  --predictions predictions_results.json \
  --compare ../Part1/models/training_metrics.json
```

### View Logs

```bash
# View API logs (structured JSON)
docker logs cats-dogs-api-monitoring

# Follow logs in real-time
docker logs -f cats-dogs-api-monitoring

# View last 50 lines
docker logs --tail 50 cats-dogs-api-monitoring
```

### Stop Monitoring Stack

```bash
# Stop all services
docker-compose -f docker-compose-monitoring.yml down

# Stop and remove volumes (clean slate)
docker-compose -f docker-compose-monitoring.yml down -v
```

### What Gets Generated

After running Part 5:
- **Real-time monitoring**: Grafana dashboard with 8 visualization panels
- **Metrics**: Prometheus metrics at `/metrics` endpoint
- **Performance analysis**: 
  - `predictions_results.json` - Collected predictions and true labels
  - `performance_metrics.json` - Accuracy, precision, recall, F1-score
  - `confusion_matrix.png` - Visual confusion matrix
- **Logs**: Structured JSON logs in Docker container


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
