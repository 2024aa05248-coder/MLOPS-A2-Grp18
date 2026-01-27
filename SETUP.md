# Setup Instructions for Assignment 2

## Initial Setup

### 1. Create New GitHub Repository

Since this is a new repository (separate from Assignment 1):

1. Go to https://github.com
2. Click "New repository"
3. Name it: `MLOP-Assign2` or `cats-dogs-mlops`
4. Make it **Public** (for GitHub Actions free tier)
5. Don't initialize with README (we already have one)
6. Click "Create repository"

### 2. Initialize Git Repository

```bash
cd Assignment2
git init
git add .
git commit -m "Initial commit: Assignment 2 - Cats vs Dogs MLOps Pipeline"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

### 3. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Initialize DVC (Part 1)

```bash
cd Part1
dvc init
dvc add ../PetImages
git add .dvc .gitignore
git commit -m "Add dataset to DVC"
```

### 5. Configure Docker Hub (for CI/CD)

1. Create account at https://hub.docker.com
2. Create repository: `cats-dogs-api`
3. Get your Docker Hub username

Update these files with your Docker Hub username:
- `Part4/k8s/deployment.yaml` - Replace `YOUR_DOCKER_USERNAME`
- `Part4/docker-compose/docker-compose.yml` - Replace `YOUR_DOCKER_USERNAME`
- `Part5/docker-compose-monitoring.yml` - Replace `YOUR_DOCKER_USERNAME`

### 6. Configure GitHub Secrets (for CI/CD)

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password/token

## Verification Checklist

- [ ] Git repository initialized and pushed
- [ ] Python virtual environment created and activated
- [ ] Dependencies installed
- [ ] DVC initialized and dataset added
- [ ] Docker Hub account created
- [ ] GitHub secrets configured
- [ ] All configuration files updated with your Docker Hub username

## Next Steps

Follow the part-by-part instructions:
1. Start with [Part1/README.md](Part1/README.md)
2. Complete each part sequentially
3. Refer to [QUICK_START.md](QUICK_START.md) for quick commands

## Troubleshooting

### DVC Issues
- Ensure DVC is installed: `pip install dvc`
- Check that PetImages folder exists

### Docker Issues
- Ensure Docker is installed and running
- Test with: `docker run hello-world`

### GitHub Actions Issues
- Ensure repository is public (for free tier)
- Check that secrets are configured correctly
- Verify workflow file syntax
