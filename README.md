# Assignment 2: An End-to-End MLOps Pipeline for Image Classification

## Project Overview

A complete MLOps pipeline for binary image classification (Cats vs Dogs) for a pet adoption platform. This project demonstrates end-to-end machine learning workflow from model development to production deployment with CI/CD, containerization, and monitoring.

### Use Case
Binary image classification (Cats vs Dogs) for a pet adoption platform.

### Dataset
Cats and Dogs classification dataset (PetImages folder)
- **Download**: [Kaggle Dogs vs Cats](https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset)
- **Important**: After downloading, extract and place the `Cat` and `Dog` folders inside a `PetImages` folder in the root directory of this project
- Pre-processed to 224x224 RGB images for standard CNNs
- Split into train/validation/test sets (80%/10%/10%)
- Data augmentation for better generalization

---

## Project Structure

```
Image Classification/
├── README.md                    # This file
├── PetImages/                   # Dataset (Cats and Dogs images)
│   ├── Cat/                     # Cat images
│   └── Dog/                     # Dog images
├── Part1/                       # M1: Model Development & Experiment Tracking
│   ├── src/                     # Source code
│   ├── data/                    # Data directories (raw, interim, processed)
│   ├── models/                  # Trained models
│   ├── reports/                 # Visualizations and reports
│   └── mlruns/                  # MLflow tracking data
├── Part2/                       # M2: Model Packaging & Containerization
│   ├── src/                     # FastAPI application
│   ├── models/                  # Model files
│   ├── Dockerfile              # Container definition
│   └── requirements.txt        # Dependencies
├── Part3/                       # M3: CI Pipeline
│   ├── src/                     # Source code
│   ├── tests/                   # Unit tests
│   └── .github/workflows/       # GitHub Actions CI
├── Part4/                       # M4: CD Pipeline & Deployment
│   ├── k8s/                     # Kubernetes manifests
│   ├── docker-compose/          # Docker Compose config
│   └── src/                     # Deployment scripts
└── Part5/                       # M5: Monitoring & Logs
    ├── src/                     # Monitoring code
    ├── config/                  # Monitoring configuration
    └── dashboards/              # Grafana dashboards
```

---

## Breakdown

### Part 1: Model Development & Experiment Tracking (M1)

**Objective**: Build a baseline model, track experiments, and version all artifacts.

**Tasks**:
1. **Data & Code Versioning**
   - Git for source code versioning
   - DVC for dataset versioning

2. **Model Building**
   - Implement baseline model (CNN)
   - Save model in standard format (.pt)

3. **Experiment Tracking**
   - MLflow for logging runs, parameters, metrics, artifacts

**See**: [Part1/README.md](Part1/README.md)

---

### Part 2: Model Packaging & Containerization (M2) 

**Objective**: Package the trained model into a reproducible, containerized service.

**Tasks**:
1. **Inference Service**
   - REST API with FastAPI/Flask
   - Endpoints: `/health` and `/predict`

2. **Environment Specification**
   - requirements.txt with version pinning

3. **Containerization**
   - Dockerfile for containerization
   - Build and test locally

**See**: [Part2/README.md](Part2/README.md)

---

### Part 3: CI Pipeline (M3) 

**Objective**: Implement Continuous Integration for automated testing and image building.

**Tasks**:
1. **Automated Testing**
   - Unit tests for data preprocessing
   - Unit tests for model inference
   - pytest for test execution

2. **CI Setup**
   - GitHub Actions workflow for CI
   - Pipeline: checkout → install → test → build image

3. **Artifact Publishing**
   - Push Docker image to registry (Docker Hub)

**See**: [Part3/README.md](Part3/README.md)

---

### Part 4: CD Pipeline & Deployment (M4) - 

**Objective**: Implement Continuous Deployment to target environment.

**Tasks**:
1. **Deployment Target**
   - Kubernetes (minikube) and Docker Compose
   - Infrastructure manifests (Deployment + Service YAML)

2. **CD / GitOps Flow**
   - Auto-deploy on main branch changes
   - Pull image from registry and deploy

3. **Smoke Tests**
   - Post-deploy health check
   - Prediction test
   - Fail pipeline if tests fail

**See**: [Part4/README.md](Part4/README.md)

---

### Part 5: Monitoring & Logs (M5) - 

**Objective**: Monitor deployed model and track performance.

**Tasks**:
1. **Basic Monitoring & Logging**
   - Request/response logging (exclude sensitive data)
   - Track metrics: request count, latency
   - Prometheus for metrics collection
   - Grafana for visualization

2. **Model Performance Tracking**
   - Collect batch of requests with true labels
   - Calculate post-deployment metrics

**See**: [Part5/README.md](Part5/README.md)

---

## Quick Start

### Prerequisites

- Python 3.9+
- Docker
- Git
- DVC (for Part1)
- kubectl + minikube (for Part4, if using Kubernetes)

### Setup

1. **Clone Repository** (when created)
   ```bash
   git clone <https://github.com/2024aa05248-coder/MLOPS-A2-Grp18.git>
   ```

2. **Set up Python Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Initialize DVC** (Part1)
   ```bash
   cd Part1
   dvc init
   dvc add ../PetImages
   ```

4. **Follow Part-by-Part Instructions**
   - Start with [Part1/README.md](Part1/README.md)
   - Complete each part sequentially

---

## Workflow Overview

```
Part1: Data → Preprocessing → Training → MLflow Tracking
   ↓
Part2: Model → FastAPI → Docker → Containerized Service
   ↓
Part3: Tests → CI Pipeline → Build Image → Push to Registry
   ↓
Part4: CD Pipeline → Deploy → Kubernetes/Docker Compose → Smoke Tests
   ↓
Part5: Monitoring → Logging → Performance Tracking → Final Report
```

---

## Key Technologies

- **ML Framework**: PyTorch / TensorFlow
- **Experiment Tracking**: MLflow
- **API Framework**: FastAPI
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Orchestration**: Kubernetes / Docker Compose
- **Monitoring**: Prometheus + Grafana
- **Testing**: pytest

---

## All Links
- **Demo**: [Video Demo Link](https://drive.google.com/file/d/1Cv8IVx-Ro7E1Azqq_Oa1oj28SzH5dxW3/view?usp=drive_link)
- **Model Artifacts**: [Google Drive Link](https://drive.google.com/drive/folders/1aryPsaw1uYxcW0Xsl2hFWSshdMkPpaiW?usp=drive_link)

## The Team

| Name                | Roll No.    | Contribution |
|---------------------|-------------|--------------|
| Ashmita De          | 2024AA05248 | 100%         |
| Ayush Goyal         | 2024AA05463 | 100%         |
| Srinivasan V        | 2024AA05292 | 100%         |
| Saurabh Vikas Kolhe | 2024AA05350 | 100%         |
---

## License

This project is for educational purposes as part of MLOps coursework.

---

**Built by Group18**
