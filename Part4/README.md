# Part 4: CD Pipeline & Deployment (M4)

## Objective
Implement Continuous Deployment of the containerized model to a target environment.

## Tasks

### 1. Deployment Target
Choose one:
- **Local Kubernetes** (kind/minikube/microk8s) - Recommended
- Docker Compose
- Simple VM server

Define infrastructure manifests:
- **Kubernetes**: Deployment + Service YAML
- **Docker Compose**: docker-compose.yml

### 2. CD / GitOps Flow
Extend CI or use CD tool:
- **Argo CD** (GitOps)
- **Jenkins** (CD pipeline)
- **GitHub Actions** (environment deployment)

Flow:
- Pull new image from registry
- Deploy/update running service automatically on main branch changes

### 3. Smoke Tests / Health Check
- Implement post-deploy smoke test script
- Calls health endpoint
- Makes one prediction call
- Fail pipeline if smoke tests fail

## Project Structure

```
Part4/
├── README.md                    # This file
├── k8s/
│   ├── deployment.yaml          # Kubernetes Deployment
│   ├── service.yaml             # Kubernetes Service
│   └── namespace.yaml           # Optional: Namespace
├── docker-compose/
│   └── docker-compose.yml       # Docker Compose configuration
├── src/
│   └── smoke_test.py            # Post-deployment smoke tests
└── scripts/
    └── deploy.sh                # Deployment script
```

## Deployment Options

### Option 1: Kubernetes

#### Prerequisites
```bash
# Install kubectl
# Install kind/minikube/microk8s
```

#### Setup Local Kubernetes (kind)
```bash
# Create cluster
kind create cluster --name cats-dogs-cluster

# Load Docker image
kind load docker-image cats-dogs-api:latest --name cats-dogs-cluster

# Deploy
kubectl apply -f k8s/
```

#### Verify Deployment
```bash
# Check pods
kubectl get pods

# Check service
kubectl get svc

# Port forward
kubectl port-forward svc/cats-dogs-api 8000:8000

# Run smoke tests
python src/smoke_test.py
```

### Option 2: Docker Compose

```bash
# Deploy
docker-compose -f docker-compose/docker-compose.yml up -d

# Check status
docker-compose ps

# Run smoke tests
python src/smoke_test.py

# View logs
docker-compose logs -f
```

## Smoke Tests

The smoke test script should:
1. Check health endpoint (`/health`)
2. Make a prediction request with a test image
3. Verify response format
4. Exit with error code if tests fail

```bash
python src/smoke_test.py
```

## CD Pipeline Integration

### GitHub Actions CD
- Extends Part3 CI pipeline
- On successful build and test:
  - Deploy to Kubernetes/Docker Compose
  - Run smoke tests
  - Rollback if smoke tests fail

### Argo CD (GitOps)
- Monitor Git repository
- Auto-sync on changes
- Deploy Kubernetes manifests

## Expected Outputs

- Service deployed and running
- Health endpoint accessible
- Prediction endpoint working
- Smoke tests passing
- CD pipeline automatically deploying on main branch changes
