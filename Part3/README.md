# Part 3: CI/CD Pipeline - Build, Test & Image Creation

## Objective
Implement a comprehensive Continuous Integration pipeline to automatically lint, test, train models, and build container images.

## Features Implemented

### 1. Automated Testing ✅
- **Unit tests** using pytest:
  - Data preprocessing function tests ([test_preprocessing.py](tests/test_preprocessing.py))
  - Model inference function tests ([test_inference.py](tests/test_inference.py))
- **Coverage reporting** with HTML, XML, and terminal output
- **Test artifacts** uploaded to GitHub Actions

### 2. Code Quality - Linting ✅
- **flake8**: PEP 8 compliance checking
- **pylint**: Advanced code quality metrics
- **black**: Code formatting verification
- **isort**: Import statement organization
- **Configuration files**: `.flake8`, `.pylintrc`, `pyproject.toml`

### 3. CI/CD Pipeline ✅
**Platform**: GitHub Actions

**Jobs**:
1. **Linting** (parallel) - Code quality checks
2. **Testing** (parallel) - Unit tests with coverage
3. **Model Training** (optional) - Data preprocessing & model training
4. **Docker Build** - Build and push Docker images
5. **Summary** - Aggregate all job results

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main`
- Manual workflow dispatch

### 4. Artifact Management ✅
- **Linting reports** (30-day retention)
- **Test results & coverage** (30-day retention)
- **Training artifacts** (30-day retention)
- **Trained models** (90-day retention)
- **Docker build logs** (7-day retention)

### 5. Docker Image Publishing ✅
- **Registry**: Docker Hub
- **Tags**:
  - `latest` (main branch)
  - `<branch>` (branch-specific)
  - `<branch>-<sha>` (commit-specific)
- **Build caching** for faster builds
- **Metadata labeling** (build date, VCS ref)

## Project Structure

```
Part3/
├── README.md                     # This file
├── CI_CD_DOCUMENTATION.md        # Detailed pipeline documentation
├── .github/
│   └── workflows/
│       └── ci.yml                # Complete CI/CD pipeline
├── tests/
│   ├── test_preprocessing.py     # Data preprocessing tests
│   └── test_inference.py         # Model inference tests
├── .flake8                       # Flake8 linting configuration
├── .pylintrc                     # Pylint configuration
└── pyproject.toml                # Black/isort/pytest configuration
```

## Quick Start

### Prerequisites

```bash
# Install project dependencies
pip install -r ../requirements.txt

# Install testing and linting tools
pip install pytest pytest-cov pytest-html pytest-json-report
pip install flake8 pylint black isort
```

### Setup GitHub Secrets

For Docker image publishing, add these secrets to your GitHub repository:
1. Go to: `Settings > Secrets and variables > Actions`
2. Add:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password/token

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

## Running Locally

### Run Tests

```bash
# Basic test run
pytest Part3/tests/ -v

# With coverage for Part1 and Part2 source code
pytest Part3/tests/ \
  --cov=Part1/src \
  --cov=Part2/src \
  --cov-report=html \
  --cov-report=term

# With HTML report
pytest Part3/tests/ \
  -v \
  --cov=Part1/src \
  --cov=Part2/src \
  --cov-report=html \
  --html=test-report.html \
  --self-contained-html

# View coverage report (opens in browser)
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
xdg-open htmlcov/index.html # Linux

# Run specific test file
pytest Part3/tests/test_preprocessing.py -v

# Run specific test function
pytest Part3/tests/test_preprocessing.py::test_image_resize -v
```

### Run Linting

```bash
# Flake8 - Check for PEP 8 compliance
flake8 Part1/src Part2/src

# Pylint - Advanced code analysis
pylint Part1/src Part2/src

# Black - Check code formatting
black --check Part1/src Part2/src

# Isort - Check import sorting
isort --check-only Part1/src Part2/src
```

### Auto-fix Code Issues

```bash
# Format code with black
black Part1/src Part2/src

# Sort imports with isort
isort Part1/src Part2/src

# Verify fixes
flake8 Part1/src Part2/src
```

### Build Docker Image

```bash
# From project root
cd ..
docker build -t cats-dogs-api:latest -f Part2/Dockerfile .

# Run container
docker run -p 8000:8000 cats-dogs-api:latest

# Test API
curl http://localhost:8000/health
```

## CI/CD Pipeline Details

### Pipeline Architecture

```
┌─────────────┐     ┌──────────────┐
│   Linting   │     │   Testing    │  (Run in parallel)
└──────┬──────┘     └──────┬───────┘
       │                   │
       └─────────┬─────────┘
                 │
         ┌───────▼────────┐
         │  Docker Build  │  (Only on main/develop)
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │    Summary     │  (Always runs)
         └────────────────┘

         ┌────────────────┐
         │  Model Train   │  (Optional/Manual)
         └────────────────┘
```

### Triggers

- **Push**: Runs on `main` and `develop` branches
- **Pull Request**: Runs on PRs to `main`
- **Manual**: Can be triggered manually with options

### Jobs Breakdown

#### 1. Linting Job
- Runs flake8, pylint, black, isort
- Uploads linting reports as artifacts
- Continues even if warnings found

#### 2. Testing Job
- Runs pytest with coverage
- Generates HTML and XML coverage reports
- Uploads to Codecov
- Creates test summary in GitHub UI
- Posts coverage comment on PRs

#### 3. Model Training Job (Optional)
- Only runs on manual trigger or main branch push
- Runs data preprocessing
- Trains model with MLflow tracking
- Uploads model and training logs

#### 4. Docker Build Job
- Requires linting and testing to pass
- Only on main/develop branches
- Uses Docker BuildKit caching
- Pushes multiple tags to Docker Hub
- Includes build metadata

#### 5. Summary Job
- Always runs (even on failure)
- Aggregates status of all jobs
- Creates comprehensive summary

### Artifacts Generated

| Artifact | Description | Retention |
|----------|-------------|-----------|
| `linting-reports` | Flake8, pylint, black, isort reports | 30 days |
| `test-results` | Test reports, coverage HTML | 30 days |
| `training-artifacts` | Models, MLflow runs, logs | 30 days |
| `trained-model` | Final trained model file | 90 days |
| `docker-build-logs` | Docker build process logs | 7 days |

### Viewing Pipeline Results

1. **GitHub Actions Tab**
   - Go to repository > Actions
   - Select "CI/CD Pipeline - MLOps Assignment"
   - View workflow runs

2. **Download Artifacts**
   - Click on a workflow run
   - Scroll to "Artifacts" section
   - Download desired reports

3. **View Logs**
   - Click on specific job
   - Expand steps to see detailed logs

### Manual Workflow Trigger

To run with custom options:
1. Go to Actions tab
2. Select workflow
3. Click "Run workflow"
4. Choose branch
5. Enable "Run model training" if needed
6. Click "Run workflow"

## Expected Outputs

✅ **Code Quality**
- All linting checks pass with configurable rules
- Detailed reports for each linter

✅ **Tests**
- All unit tests pass
- >80% code coverage recommended
- HTML coverage report generated

✅ **Training** (when enabled)
- Model trained successfully
- Metrics logged to MLflow
- Model artifact saved

✅ **Docker**
- Image built successfully
- Pushed to Docker Hub with multiple tags
- Cache optimized for faster builds

✅ **Artifacts**
- All reports and logs preserved
- Easy download from GitHub Actions

## Configuration Files

### [.flake8](.flake8)
```ini
max-line-length = 127
max-complexity = 10
# Excludes venv, mlruns, etc.
```

### [.pylintrc](.pylintrc)
```ini
max-line-length = 127
# Disabled warnings for common ML patterns
```

### [pyproject.toml](pyproject.toml)
Configures:
- Black (code formatting)
- Isort (import sorting)
- Pytest (test discovery and reporting)

## Troubleshooting

### Pipeline Fails on Linting
```bash
# Auto-fix most issues locally
black Part1/src Part2/src
isort Part1/src Part2/src
```

### Tests Pass Locally But Fail in CI
- Check Python version matches (3.9)
- Verify all dependencies in requirements.txt
- Check file paths are relative to project root

### Docker Build Fails
- Verify Dockerfile paths
- Test build locally first
- Check secrets are configured correctly

### Coverage Not Uploading
- Ensure coverage.xml is generated
- Check Codecov integration is enabled

## Best Practices

### Before Pushing
1. Run linting locally: `flake8 Part1/src Part2/src`
2. Run tests: `pytest Part3/tests/ -v`
3. Fix any issues before pushing

### Writing Tests
- One test per function behavior
- Use descriptive test names
- Include edge cases
- Mock external dependencies

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for public functions
- Keep functions small and focused

## Additional Resources

- 📖 [Detailed CI/CD Documentation](CI_CD_DOCUMENTATION.md)
- 🔧 [GitHub Actions Docs](https://docs.github.com/en/actions)
- 🧪 [Pytest Documentation](https://docs.pytest.org/)
- 🐳 [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## Support

For detailed information, see [CI_CD_DOCUMENTATION.md](CI_CD_DOCUMENTATION.md)

---

[![CI/CD Pipeline](../.github/workflows/ci.yml/badge.svg)](../.github/workflows/ci.yml)

**Status**: ✅ Fully Implemented
**Last Updated**: 2024-01-28
