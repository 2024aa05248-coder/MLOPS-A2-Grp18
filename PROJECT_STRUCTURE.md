# Assignment 2 - Complete Project Structure

## Overview

This document provides a complete overview of the Assignment 2 project structure for the Cats vs Dogs image classification MLOps pipeline.

## Directory Structure

```
Assignment2/
├── README.md                          # Main project README
├── SETUP.md                           # Initial setup instructions
├── QUICK_START.md                     # Quick command reference
├── PROJECT_STRUCTURE.md               # This file
├── requirements.txt                   # Root Python dependencies
├── .gitignore                         # Git ignore patterns
├── .dvcignore                         # DVC ignore patterns
│
├── PetImages/                         # Dataset (already downloaded)
│   ├── Cat/                           # Cat images
│   └── Dog/                           # Dog images
│
├── Part1/                             # M1: Model Development & Experiment Tracking
│   ├── README.md                      # Part 1 documentation
│   ├── src/
│   │   ├── __init__.py
│   │   ├── data_preprocessing.py      # Data loading, preprocessing, augmentation
│   │   └── train_model.py             # Model training with MLflow
│   ├── data/
│   │   ├── raw/                       # Original images (via DVC)
│   │   ├── interim/                   # Preprocessed images
│   │   └── processed/                 # Train/val/test splits
│   ├── models/                        # Saved model files (.pt)
│   ├── reports/
│   │   └── figures/                   # Visualizations
│   └── mlruns/                        # MLflow tracking data
│
├── Part2/                             # M2: Model Packaging & Containerization
│   ├── README.md                      # Part 2 documentation
│   ├── src/
│   │   ├── __init__.py
│   │   └── app.py                     # FastAPI application
│   ├── models/                        # Model files (symlink or copy from Part1)
│   ├── Dockerfile                     # Container definition
│   ├── .dockerignore                  # Docker ignore patterns
│   ├── requirements.txt               # API dependencies
│   └── test_api.py                    # API testing script
│
├── Part3/                             # M3: CI Pipeline
│   ├── README.md                      # Part 3 documentation
│   ├── src/                           # Shared source code
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_preprocessing.py     # Data preprocessing tests
│   │   └── test_inference.py          # Model inference tests
│   ├── pytest.ini                     # Pytest configuration
│   └── .github/
│       └── workflows/
│           └── ci.yml                 # GitHub Actions CI pipeline
│
├── Part4/                             # M4: CD Pipeline & Deployment
│   ├── README.md                      # Part 4 documentation
│   ├── k8s/
│   │   ├── deployment.yaml            # Kubernetes Deployment
│   │   └── service.yaml               # Kubernetes Service
│   ├── docker-compose/
│   │   └── docker-compose.yml         # Docker Compose configuration
│   └── src/
│       ├── __init__.py
│       └── smoke_test.py              # Post-deployment smoke tests
│
└── Part5/                             # M5: Monitoring & Logs
    ├── README.md                      # Part 5 documentation
    ├── src/
    │   ├── __init__.py
    │   └── app_with_monitoring.py     # Enhanced API with monitoring
    ├── config/
    │   ├── prometheus.yml             # Prometheus configuration
    │   └── grafana-datasource.yml     # Grafana datasource config
    ├── dashboards/                    # Grafana dashboards (optional)
    └── docker-compose-monitoring.yml  # Monitoring stack
```

## Key Files Description

### Part 1 (Model Development)
- **data_preprocessing.py**: Handles image loading, resizing (224x224), data splitting (80/10/10), and augmentation
- **train_model.py**: Trains SimpleCNN model, logs to MLflow, saves model and visualizations

### Part 2 (Packaging & Containerization)
- **app.py**: FastAPI application with `/health` and `/predict` endpoints
- **Dockerfile**: Containerizes the API service
- **test_api.py**: Tests API endpoints locally

### Part 3 (CI Pipeline)
- **test_preprocessing.py**: Unit tests for data preprocessing functions
- **test_inference.py**: Unit tests for model inference functions
- **ci.yml**: GitHub Actions workflow for automated testing and Docker image building

### Part 4 (CD Pipeline)
- **deployment.yaml**: Kubernetes deployment manifest
- **service.yaml**: Kubernetes service manifest
- **docker-compose.yml**: Docker Compose configuration
- **smoke_test.py**: Post-deployment health and prediction tests

### Part 5 (Monitoring)
- **app_with_monitoring.py**: Enhanced API with Prometheus metrics and logging
- **prometheus.yml**: Prometheus scrape configuration
- **docker-compose-monitoring.yml**: Complete monitoring stack (API + Prometheus + Grafana)

## Data Flow

```
PetImages (raw)
    ↓
Part1: Preprocessing → Train/Val/Test splits → Model Training → MLflow Tracking
    ↓
Part2: Model → FastAPI → Docker Image
    ↓
Part3: Tests → CI Pipeline → Docker Registry
    ↓
Part4: CD Pipeline → Kubernetes/Docker Compose → Deployment
    ↓
Part5: Monitoring → Prometheus → Grafana → Performance Tracking
```

## Technology Stack

- **ML Framework**: PyTorch
- **Experiment Tracking**: MLflow
- **API Framework**: FastAPI
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Orchestration**: Kubernetes / Docker Compose
- **Monitoring**: Prometheus + Grafana
- **Testing**: pytest
- **Data Versioning**: DVC

## Workflow Order

1. **Part 1**: Preprocess data → Train model → Track with MLflow
2. **Part 2**: Create API → Containerize → Test locally
3. **Part 3**: Write tests → Set up CI → Build and push images
4. **Part 4**: Deploy → Run smoke tests → Verify deployment
5. **Part 5**: Add monitoring → Track metrics → Analyze performance

## Notes

- Each part builds on the previous one
- Model from Part 1 is used in Part 2
- Docker image from Part 2 is deployed in Part 4
- Monitoring in Part 5 enhances the API from Part 2
- All parts should be completed sequentially
