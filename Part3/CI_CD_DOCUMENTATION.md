# CI/CD Pipeline Documentation

## Overview

This document describes the comprehensive CI/CD pipeline implemented using GitHub Actions for the Cats vs Dogs classification MLOps project.

## Pipeline Architecture

The CI/CD pipeline consists of 5 main jobs that run in parallel or sequentially based on dependencies:

```
┌─────────────┐     ┌──────────────┐
│   Linting   │     │   Testing    │
└──────┬──────┘     └──────┬───────┘
       │                   │
       └─────────┬─────────┘
                 │
         ┌───────▼────────┐
         │  Docker Build  │
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │    Summary     │
         └────────────────┘
                 │
         ┌───────▼────────┐
         │  Model Train   │ (Optional)
         └────────────────┘
```

## Jobs Description

### 1. Code Linting (`lint`)

**Purpose**: Ensures code quality and adherence to Python coding standards.

**Tools**:
- **flake8**: Checks for PEP 8 compliance and code errors
- **pylint**: Advanced code analysis and quality metrics
- **black**: Code formatting verification
- **isort**: Import statement organization

**Artifacts**:
- `linting-reports/`: Contains detailed reports from all linting tools
  - `flake8-report.txt`
  - `pylint-report.txt`
  - `black-report.txt`
  - `isort-report.txt`

**Configuration Files**:
- `.flake8`: Flake8 settings
- `.pylintrc`: Pylint configuration
- `pyproject.toml`: Black and isort settings

### 2. Unit Testing (`test`)

**Purpose**: Runs unit tests and generates coverage reports.

**Features**:
- Runs all tests in `Part3/tests/`
- Generates code coverage for `Part1/src` and `Part2/src`
- Creates HTML, XML, and terminal coverage reports
- Generates test result summary in GitHub Actions UI
- Uploads coverage to Codecov

**Artifacts**:
- `test-results/`: Test reports and coverage
  - `test-report.html`: Visual HTML test report
  - `test-report.json`: Machine-readable test results
  - `htmlcov/`: HTML coverage report

**Coverage Metrics**:
- Line coverage
- Branch coverage
- Function coverage

### 3. Model Training (`train`)

**Purpose**: Trains the machine learning model (optional job).

**Trigger Conditions**:
- Manual workflow dispatch with `train_model` input
- Automatic on push to `main` branch
- Requires successful linting and testing

**Steps**:
1. Downloads training data (DVC integration ready)
2. Runs data preprocessing
3. Trains the model
4. Logs training metrics

**Artifacts**:
- `training-artifacts/`: Complete training outputs
  - `models/`: Trained model files
  - `mlruns/`: MLflow experiment tracking
  - `*.log`: Training and preprocessing logs
  - `data/processed/`: Processed datasets
- `trained-model/`: Final model file (90-day retention)
  - `model.pt`

### 4. Docker Build & Push (`build`)

**Purpose**: Builds and pushes Docker images to Docker Hub.

**Trigger Conditions**:
- Push to `main` or `develop` branch
- Requires successful linting and testing

**Features**:
- Multi-tag support:
  - `latest`: Latest build from main branch
  - `<branch-name>`: Branch-specific tags
  - `<branch>-<sha>`: Commit-specific tags
- Build caching for faster builds
- Metadata labeling (build date, VCS ref)

**Requirements**:
- Docker Hub credentials stored in GitHub Secrets:
  - `DOCKER_USERNAME`
  - `DOCKER_PASSWORD`

**Artifacts**:
- `docker-build-logs/`: Build process logs (7-day retention)

### 5. Workflow Summary (`summary`)

**Purpose**: Provides a comprehensive summary of all jobs.

**Features**:
- Aggregates status of all pipeline jobs
- Displays in GitHub Actions summary page
- Always runs (even if previous jobs fail)

## Trigger Events

### Push Events
```yaml
branches: [ main, develop ]
```
- Triggers full pipeline
- Docker build only on main/develop

### Pull Request Events
```yaml
branches: [ main ]
```
- Runs linting and testing
- No Docker build or deployment
- Posts coverage comment on PR

### Manual Dispatch
```yaml
workflow_dispatch
```
- Can manually trigger the pipeline
- Option to enable model training

## Environment Variables

```yaml
PYTHON_VERSION: '3.9'
CACHE_KEY: pip-${{ hashFiles('**/requirements.txt') }}
```

## Artifacts & Retention

| Artifact Name | Contents | Retention | Size Estimate |
|---------------|----------|-----------|---------------|
| `linting-reports` | Code quality reports | 30 days | ~100 KB |
| `test-results` | Test and coverage reports | 30 days | ~5 MB |
| `training-artifacts` | Models, logs, MLflow data | 30 days | ~500 MB |
| `trained-model` | Final model file | 90 days | ~100 MB |
| `docker-build-logs` | Docker build logs | 7 days | ~1 MB |

## GitHub Actions Summary

Each workflow run generates a detailed summary accessible from the Actions tab:

### Test Results Summary
```
- Total Tests: X
- Passed: Y ✅
- Failed: Z ❌
- Duration: Xs
```

### Model Training Summary
```
- Branch: main
- Commit: abc123
- Trigger: push
```

### Docker Build Summary
```
- Image Tags: username/cats-dogs-api:latest
- Build Date: 2024-01-28T10:30:00Z
- Commit SHA: abc123
```

## Setup Instructions

### 1. Configure GitHub Secrets

Navigate to: `Repository Settings > Secrets and variables > Actions`

Add the following secrets:
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password or access token

### 2. Configure DVC (Optional)

If using DVC for data versioning:
```bash
dvc remote add -d storage <your-remote-storage>
dvc push
```

Add DVC credentials to GitHub Secrets if needed.

### 3. Enable Codecov (Optional)

1. Sign up at [codecov.io](https://codecov.io)
2. Add your repository
3. No additional secrets needed (uses `github.token`)

### 4. Copy Configuration Files

Ensure these files are in your repository root:
- `Part3/.github/workflows/ci.yml`
- `Part3/.flake8`
- `Part3/.pylintrc`
- `Part3/pyproject.toml`

## Running Locally

### Run Linting
```bash
# Flake8
flake8 Part1/src Part2/src

# Pylint
pylint Part1/src Part2/src

# Black
black --check Part1/src Part2/src

# Isort
isort --check-only Part1/src Part2/src
```

### Run Tests
```bash
# Basic tests
pytest Part3/tests/ -v

# With coverage
pytest Part3/tests/ \
  --cov=Part1/src \
  --cov=Part2/src \
  --cov-report=html \
  --html=test-report.html
```

### Build Docker Image
```bash
# From project root
docker build -t cats-dogs-api:latest -f Part2/Dockerfile .

# Test the image
docker run -p 8000:8000 cats-dogs-api:latest
```

## Monitoring Pipeline Performance

### View Pipeline Status

1. Navigate to `Actions` tab in GitHub repository
2. Select `CI/CD Pipeline - MLOps Assignment`
3. View individual workflow runs

### Download Artifacts

1. Click on a workflow run
2. Scroll to "Artifacts" section
3. Download desired artifacts (zip files)

### View Logs

1. Click on a workflow run
2. Click on specific job (e.g., "Code Linting")
3. Expand steps to view detailed logs

## Best Practices

### Code Quality
- Fix all critical flake8 errors before merging
- Maintain code coverage above 80%
- Run linting locally before pushing

### Testing
- Write unit tests for all new functions
- Include edge cases in tests
- Mock external dependencies

### Docker Images
- Keep images small (use multi-stage builds if needed)
- Tag images appropriately
- Test images locally before pushing

### Model Training
- Track experiments with MLflow
- Version models appropriately
- Document training parameters

## Troubleshooting

### Common Issues

#### 1. Docker Login Fails
**Solution**: Verify Docker Hub credentials in GitHub Secrets

#### 2. Tests Fail Locally But Pass in CI
**Solution**: Check Python version and dependency versions match

#### 3. Coverage Not Uploading
**Solution**: Ensure `coverage.xml` is generated and Codecov token is set

#### 4. Model Training Timeout
**Solution**: Use smaller dataset or increase timeout in workflow

#### 5. Linting Errors
**Solution**: Run linters locally and fix issues:
```bash
# Auto-fix formatting
black Part1/src Part2/src
isort Part1/src Part2/src
```

## Performance Optimization

### Caching
- Pip packages cached using `actions/cache`
- Docker layers cached using BuildKit
- Cache key based on `requirements.txt` hash

### Parallelization
- Linting and testing run in parallel
- Independent jobs don't wait for each other

### Job Dependencies
```
lint ─┐
      ├─> build ─> summary
test ─┘

train (optional, runs independently)
```

## Security Considerations

1. **Secrets Management**
   - Never commit secrets to repository
   - Use GitHub Secrets for credentials
   - Rotate secrets periodically

2. **Dependency Scanning**
   - Consider adding Dependabot
   - Review dependency updates regularly

3. **Code Scanning**
   - Consider adding CodeQL analysis
   - Review security alerts

## Future Enhancements

Potential improvements to consider:

1. **Integration Testing**
   - Add API integration tests
   - Test model inference end-to-end

2. **Performance Testing**
   - Load testing for API
   - Model inference benchmarks

3. **Security Scanning**
   - Container image vulnerability scanning
   - Dependency vulnerability checks

4. **Deployment Automation**
   - Auto-deploy to staging
   - Smoke tests in deployment environment

5. **Notification System**
   - Slack/Email notifications on failures
   - Daily summary reports

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Pytest Documentation](https://docs.pytest.org/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Black Documentation](https://black.readthedocs.io/)

## Maintenance

### Regular Tasks
- Review and update dependencies monthly
- Clean up old artifacts (automated via retention policies)
- Monitor workflow execution times
- Update documentation as pipeline evolves

### Version Updates
When updating Python version or major dependencies:
1. Update `PYTHON_VERSION` in workflow
2. Test locally with new versions
3. Update `requirements.txt`
4. Run full pipeline to verify

## Contact & Support

For issues or questions about the CI/CD pipeline:
1. Check this documentation
2. Review workflow logs in GitHub Actions
3. Open an issue in the repository
4. Contact the MLOps team

---

**Last Updated**: 2024-01-28
**Pipeline Version**: 1.0.0
**Maintained By**: MLOps Team
