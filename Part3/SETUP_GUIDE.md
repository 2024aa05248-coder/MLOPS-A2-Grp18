# CI/CD Pipeline - Quick Setup Guide

This guide will help you set up and run the CI/CD pipeline in 5 minutes.

## Prerequisites Checklist

- [ ] GitHub account
- [ ] Docker Hub account
- [ ] Git repository initialized
- [ ] Code pushed to GitHub

## Step 1: Copy Workflow Files (2 minutes)

Ensure these files exist in your repository:

```bash
# Check if files exist
ls Part3/.github/workflows/ci.yml
ls Part3/.flake8
ls Part3/.pylintrc
ls Part3/pyproject.toml
ls Part3/tests/test_*.py
```

If using a different repository structure, copy files:

```bash
# Copy workflow
mkdir -p .github/workflows
cp Part3/.github/workflows/ci.yml .github/workflows/

# Copy configuration files to project root
cp Part3/.flake8 .
cp Part3/.pylintrc .
cp Part3/pyproject.toml .
```

## Step 2: Configure GitHub Secrets (1 minute)

1. Go to your GitHub repository
2. Click: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add two secrets:

   **Secret 1:**
   - Name: `DOCKER_USERNAME`
   - Value: Your Docker Hub username

   **Secret 2:**
   - Name: `DOCKER_PASSWORD`
   - Value: Your Docker Hub password or access token

### Creating Docker Hub Access Token (Recommended)

Instead of using your password, create an access token:

1. Go to [Docker Hub](https://hub.docker.com/)
2. Click your profile → **Account Settings**
3. Click **Security** → **New Access Token**
4. Name it: `github-actions`
5. Click **Generate**
6. Copy the token (you won't see it again!)
7. Use this token as `DOCKER_PASSWORD`

## Step 3: Enable GitHub Actions (30 seconds)

1. Go to your repository
2. Click the **Actions** tab
3. If prompted, click **I understand my workflows, go ahead and enable them**

## Step 4: Test Locally (1 minute)

Before pushing, test locally:

```bash
# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov flake8 pylint black isort

# Run linting
flake8 Part1/src Part2/src

# Run tests
pytest Part3/tests/ -v

# Format code (auto-fix)
black Part1/src Part2/src
isort Part1/src Part2/src
```

## Step 5: Push and Verify (30 seconds)

```bash
# Add all files
git add .

# Commit
git commit -m "Add CI/CD pipeline"

# Push to trigger pipeline
git push origin main
```

## Verify Pipeline is Running

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You should see "CI/CD Pipeline - MLOps Assignment" running
4. Click on the workflow run to see live logs

## Expected Timeline

- Linting: ~1-2 minutes
- Testing: ~2-3 minutes
- Docker Build: ~3-5 minutes
- **Total**: ~5-8 minutes for first run

Subsequent runs are faster due to caching (~2-4 minutes).

## What to Expect

### First Run

✅ **Linting Job**
- Checks code quality
- May show warnings (not failures)

✅ **Testing Job**
- Runs unit tests
- Generates coverage reports

⏭️ **Docker Build** (may skip if not on main/develop)
- Builds Docker image
- Pushes to Docker Hub

✅ **Summary**
- Shows overall status

### Artifacts Available

After the run completes, scroll down to see artifacts:
- `linting-reports`
- `test-results`
- `training-artifacts` (if training ran)
- `trained-model` (if training ran)

## Troubleshooting

### ❌ Workflow doesn't appear

**Solution**: Check that `.github/workflows/ci.yml` exists in the correct location:
```bash
ls .github/workflows/ci.yml
```

### ❌ Docker login fails

**Solution**: Verify secrets are set correctly:
1. Go to Settings → Secrets → Actions
2. Check `DOCKER_USERNAME` and `DOCKER_PASSWORD` exist
3. If using access token, make sure you copied it correctly

### ❌ Linting fails with many errors

**Solution**: Auto-fix locally:
```bash
black Part1/src Part2/src
isort Part1/src Part2/src
git add .
git commit -m "Fix code formatting"
git push
```

### ❌ Tests fail in CI but pass locally

**Solution**: Check Python version matches:
```bash
python --version  # Should be 3.9.x
```

If different:
```bash
# Use pyenv or conda to switch to Python 3.9
pyenv install 3.9.18
pyenv local 3.9.18
```

### ❌ Build job skipped

**Reason**: Docker build only runs on `main` or `develop` branches.

**Solution**: Either:
- Push to `main` branch
- Change workflow to build on other branches:
  ```yaml
  # In .github/workflows/ci.yml
  if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop' || github.ref == 'refs/heads/YOUR_BRANCH')
  ```

## Next Steps

### 1. Add Status Badge

Add this to your main README.md:

```markdown
[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci.yml)
```

Replace:
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO` with your repository name

### 2. Configure Branch Protection

Protect your main branch:

1. Go to: **Settings** → **Branches**
2. Add rule for `main`
3. Enable:
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - Select: `Code Linting` and `Unit Tests & Coverage`
4. Save changes

Now PRs must pass CI before merging!

### 3. Enable Codecov (Optional)

For coverage tracking:

1. Go to [codecov.io](https://codecov.io)
2. Sign in with GitHub
3. Add your repository
4. No additional setup needed (uses `github.token`)

### 4. Run Manual Training

To trigger model training:

1. Go to **Actions** tab
2. Select **CI/CD Pipeline - MLOps Assignment**
3. Click **Run workflow**
4. Select branch: `main`
5. Check ✅ **Run model training**
6. Click **Run workflow**

## Customization

### Change Python Version

In `.github/workflows/ci.yml`:
```yaml
env:
  PYTHON_VERSION: '3.10'  # Change to desired version
```

### Modify Linting Rules

Edit configuration files:
- `.flake8` - Flake8 rules
- `.pylintrc` - Pylint rules
- `pyproject.toml` - Black/isort rules

### Add More Tests

Create new test files in `Part3/tests/`:
```python
# Part3/tests/test_new_feature.py
def test_my_feature():
    assert my_function() == expected_output
```

### Change Docker Registry

To use GitHub Container Registry instead:

In `.github/workflows/ci.yml`:
```yaml
- name: Log in to GitHub Container Registry
  uses: docker/login-action@v2
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

## Verification Checklist

After setup, verify:

- [ ] Pipeline runs on push to main
- [ ] Linting job completes (green or yellow)
- [ ] Testing job passes (green)
- [ ] Coverage reports generated
- [ ] Docker image built (on main/develop)
- [ ] Docker image pushed to Docker Hub
- [ ] Artifacts available for download
- [ ] Status badge shows "passing"

## Common Workflows

### Daily Development

```bash
# 1. Make changes to code
vim Part1/src/train_model.py

# 2. Test locally
pytest Part3/tests/ -v

# 3. Fix any issues
black Part1/src Part2/src

# 4. Push
git add .
git commit -m "Update training logic"
git push

# 5. Check Actions tab for CI results
```

### Creating Pull Request

```bash
# 1. Create feature branch
git checkout -b feature/new-model

# 2. Make changes and test
pytest Part3/tests/ -v

# 3. Push branch
git push origin feature/new-model

# 4. Create PR on GitHub
# CI will run automatically

# 5. Review CI results in PR
# Fix any issues before merging
```

### Release Process

```bash
# 1. Merge to main
git checkout main
git pull

# 2. CI runs automatically
# Builds and pushes Docker image

# 3. Verify Docker image
docker pull YOUR_USERNAME/cats-dogs-api:latest

# 4. Tag release
git tag v1.0.0
git push origin v1.0.0
```

## Getting Help

1. **Check logs**: Click on failed job → Expand failed step
2. **Download artifacts**: Scroll to bottom of workflow run
3. **Read docs**: See [CI_CD_DOCUMENTATION.md](CI_CD_DOCUMENTATION.md)
4. **Test locally**: Reproduce issue on your machine

## Success Criteria

Your setup is complete when:

✅ Push to main triggers pipeline
✅ All jobs complete successfully
✅ Docker image available on Docker Hub
✅ Coverage report shows >70%
✅ Status badge shows "passing"

## Quick Commands Reference

```bash
# Test everything locally
pytest Part3/tests/ -v --cov=Part1/src --cov=Part2/src

# Fix formatting
black Part1/src Part2/src && isort Part1/src Part2/src

# Check linting
flake8 Part1/src Part2/src

# Build Docker
docker build -t test -f Part2/Dockerfile .

# View coverage
open htmlcov/index.html

# Clean up
rm -rf .pytest_cache htmlcov .coverage
```

---

**Estimated Setup Time**: 5 minutes
**First Pipeline Run**: ~8 minutes
**Subsequent Runs**: ~2-4 minutes

For detailed information, see [CI_CD_DOCUMENTATION.md](CI_CD_DOCUMENTATION.md)
