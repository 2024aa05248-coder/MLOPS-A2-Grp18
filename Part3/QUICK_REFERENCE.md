# CI/CD Pipeline - Quick Reference

## Commands Cheatsheet

### Testing
```bash
# Run all tests
pytest Part3/tests/ -v

# Run with coverage
pytest Part3/tests/ --cov=Part1/src --cov=Part2/src --cov-report=html

# Run specific test
pytest Part3/tests/test_preprocessing.py::test_image_resize -v

# View coverage
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
```

### Linting
```bash
# Check all
flake8 Part1/src Part2/src
pylint Part1/src Part2/src
black --check Part1/src Part2/src
isort --check-only Part1/src Part2/src

# Auto-fix
black Part1/src Part2/src
isort Part1/src Part2/src
```

### Docker
```bash
# Build
docker build -t cats-dogs-api:latest -f Part2/Dockerfile .

# Run
docker run -p 8000:8000 cats-dogs-api:latest

# Test
curl http://localhost:8000/health

# Pull from registry
docker pull YOUR_USERNAME/cats-dogs-api:latest
```

### Git Workflow
```bash
# Before pushing
black Part1/src Part2/src
isort Part1/src Part2/src
pytest Part3/tests/ -v
git add .
git commit -m "Your message"
git push

# Feature branch
git checkout -b feature/name
# ... make changes ...
git push origin feature/name
# Create PR on GitHub
```

## Pipeline Jobs

| Job | Runs When | Duration | Output |
|-----|-----------|----------|--------|
| **Linting** | Always | ~1-2 min | Code quality reports |
| **Testing** | Always | ~2-3 min | Test results, coverage |
| **Training** | Manual/Main | ~10-20 min | Model artifacts |
| **Docker** | Main/Develop | ~3-5 min | Docker image |
| **Summary** | Always | ~10 sec | Status overview |

## Trigger Events

| Event | Branches | What Runs |
|-------|----------|-----------|
| **Push** | main, develop | All jobs + Docker build |
| **Pull Request** | → main | Lint + Test only |
| **Manual** | Any | All jobs (optional training) |

## Artifacts

| Name | Contents | Retention | Size |
|------|----------|-----------|------|
| `linting-reports` | flake8, pylint, black, isort | 30 days | ~100 KB |
| `test-results` | HTML reports, coverage | 30 days | ~5 MB |
| `training-artifacts` | Models, logs, MLflow | 30 days | ~500 MB |
| `trained-model` | model.pt | 90 days | ~100 MB |
| `docker-build-logs` | Build logs | 7 days | ~1 MB |

## Configuration Files

| File | Purpose | Key Settings |
|------|---------|--------------|
| `.flake8` | Linting rules | max-line-length: 127 |
| `.pylintrc` | Code quality | max-args: 10, max-line-length: 127 |
| `pyproject.toml` | Black/isort/pytest | line_length: 127, profile: black |
| `.github/workflows/ci.yml` | Pipeline definition | Jobs, triggers, steps |

## GitHub Secrets Required

| Secret | Value | Where to Get |
|--------|-------|--------------|
| `DOCKER_USERNAME` | Docker Hub username | hub.docker.com |
| `DOCKER_PASSWORD` | Access token | Settings → Security → New Token |

## Docker Tags

| Tag | When Created | Example |
|-----|--------------|---------|
| `latest` | Push to main | `username/cats-dogs-api:latest` |
| `<branch>` | Push to branch | `username/cats-dogs-api:develop` |
| `<branch>-<sha>` | Every push | `username/cats-dogs-api:main-abc1234` |

## Common Issues

| Problem | Solution |
|---------|----------|
| Linting fails | `black Part1/src Part2/src && isort Part1/src Part2/src` |
| Tests fail | Check Python version (should be 3.9) |
| Docker login fails | Verify secrets in Settings → Secrets → Actions |
| Build skipped | Only runs on main/develop branches |
| Coverage low | Add more tests, check coverage with `pytest --cov` |

## Status Badge

```markdown
[![CI/CD Pipeline](https://github.com/USERNAME/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/USERNAME/REPO/actions/workflows/ci.yml)
```

## Quick Fix Workflow

```bash
# 1. Pipeline failed? Check logs
# GitHub → Actions → Click failed run → Click failed job

# 2. Reproduce locally
pytest Part3/tests/ -v
flake8 Part1/src Part2/src

# 3. Fix issues
black Part1/src Part2/src
isort Part1/src Part2/src

# 4. Verify
pytest Part3/tests/ -v

# 5. Push fix
git add .
git commit -m "Fix CI issues"
git push
```

## Manual Trigger

1. Actions tab
2. Select "CI/CD Pipeline - MLOps Assignment"
3. Click "Run workflow"
4. Select branch
5. Check "Run model training" if needed
6. Click "Run workflow"

## Local Development Workflow

```bash
# Setup (once)
pip install -r requirements.txt
pip install pytest pytest-cov flake8 pylint black isort

# Before each commit
black Part1/src Part2/src
isort Part1/src Part2/src
pytest Part3/tests/ -v
flake8 Part1/src Part2/src

# Commit and push
git add .
git commit -m "Your message"
git push
```

## Coverage Targets

| Metric | Target | Current |
|--------|--------|---------|
| Line Coverage | >80% | Check in CI |
| Branch Coverage | >70% | Check in CI |
| Function Coverage | >90% | Check in CI |

## Performance

| Metric | First Run | Cached Run |
|--------|-----------|------------|
| Linting | ~2 min | ~1 min |
| Testing | ~3 min | ~2 min |
| Docker Build | ~5 min | ~2 min |
| **Total** | ~8 min | ~4 min |

## Key URLs

- **Actions**: `https://github.com/USERNAME/REPO/actions`
- **Secrets**: `https://github.com/USERNAME/REPO/settings/secrets/actions`
- **Docker Hub**: `https://hub.docker.com/r/USERNAME/cats-dogs-api`
- **Codecov**: `https://codecov.io/gh/USERNAME/REPO`

## Documentation

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and quick start |
| [CI_CD_DOCUMENTATION.md](CI_CD_DOCUMENTATION.md) | Detailed documentation |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Step-by-step setup |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | This file |

## Support

- Read docs above
- Check GitHub Actions logs
- Test locally first
- Open issue if needed

---

**Quick Links**:
[Setup](SETUP_GUIDE.md) | [Docs](CI_CD_DOCUMENTATION.md) | [README](README.md)
