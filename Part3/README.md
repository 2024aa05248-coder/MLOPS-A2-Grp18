# Part 3: CI Pipeline for Build, Test & Image Creation (M3)

## Objective
Implement Continuous Integration to automatically test, package, and build container images.

## Tasks

### 1. Automated Testing
- Write unit tests using **pytest**:
  - At least one data pre-processing function test
  - At least one model utility/inference function test
- Ensure tests run via pytest

### 2. CI Setup
Choose one CI platform:
- **GitHub Actions** (recommended)
- GitLab CI
- Jenkins
- Tekton

Pipeline should:
- Checkout repository
- Install dependencies
- Run unit tests
- Build Docker image

### 3. Artifact Publishing
- Push Docker image to container registry:
  - Docker Hub
  - GitHub Container Registry (ghcr.io)
  - Local registry

## Project Structure

```
Part3/
├── README.md                    # This file
├── src/                         # Source code (shared with Part2)
├── tests/
│   ├── __init__.py
│   ├── test_preprocessing.py   # Test data preprocessing functions
│   └── test_inference.py       # Test model inference functions
├── pytest.ini                  # Pytest configuration
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
└── requirements-test.txt       # Test dependencies
```

## Prerequisites

```bash
pip install pytest pytest-cov pytest-mock
```

## Test Structure

### Test Data Preprocessing
- Test image loading
- Test image resizing (224x224)
- Test normalization
- Test data augmentation

### Test Inference Functions
- Test model loading
- Test prediction function
- Test preprocessing pipeline
- Test output format

## How to Run Tests Locally

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_preprocessing.py -v

# Run specific test
pytest tests/test_preprocessing.py::test_image_resize -v
```

## CI Pipeline (GitHub Actions)

The pipeline should:

1. **Trigger**: On push/PR to main branch
2. **Steps**:
   - Checkout code
   - Set up Python
   - Install dependencies
   - Run tests
   - Build Docker image
   - Push to registry (on main branch)

## Expected Outputs

- All tests pass
- CI pipeline runs successfully
- Docker image built and pushed to registry
- Test coverage report

## GitHub Actions Secrets

For Docker Hub:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

For GitHub Container Registry:
- Uses `GITHUB_TOKEN` automatically
