# Part 1: Model Development & Experiment Tracking (M1)

## Objective
Build a baseline model, track experiments, and version all artifacts for binary image classification (Cats vs Dogs).

## Tasks

### 1. Data & Code Versioning
- **Git**: Source code versioning (project structure, scripts, and notebooks)
- **DVC**: Dataset versioning and tracking pre-processed data
  - Track raw dataset (PetImages)
  - Track pre-processed data (224x224 RGB images)
  - Track train/validation/test splits

### 2. Model Building
- Implement at least one baseline model:
  - Simple CNN (recommended)
  - Or logistic regression on flattened pixels
- Save trained model in standard format (.pkl, .pt, .h5)

### 3. Experiment Tracking
- Use MLflow to log:
  - Runs and parameters
  - Metrics (accuracy, loss, etc.)
  - Artifacts (confusion matrix, loss curves, model files)

## Project Structure

```
Part1/
├── README.md                    # This file
├── src/
│   ├── data_preprocessing.py    # Data loading, preprocessing, augmentation
│   ├── train_model.py          # Model training with MLflow tracking
│   └── utils.py                # Utility functions
├── data/
│   ├── raw/                     # Original PetImages (symlinked via DVC)
│   ├── interim/                 # Preprocessed images (224x224 RGB)
│   └── processed/               # Train/val/test splits
├── models/                      # Saved model files
├── reports/
│   └── figures/                 # Visualizations (confusion matrix, loss curves)
└── mlruns/                      # MLflow tracking data
```

## Dataset

- **Source**: PetImages folder (already downloaded)
- **Structure**: 
  - `PetImages/Cat/` - Cat images
  - `PetImages/Dog/` - Dog images
- **Preprocessing**:
  - Resize to 224x224 RGB images
  - Normalize pixel values
  - Data augmentation (rotation, flip, etc.)

## Data Split

- **Train**: 80%
- **Validation**: 10%
- **Test**: 10%

## Prerequisites

```bash
pip install torch torchvision mlflow dvc pandas numpy pillow scikit-learn matplotlib seaborn
```

## Setup DVC

```bash
# Initialize DVC
dvc init

# Add dataset to DVC tracking
dvc add PetImages

# Commit DVC files
git add .dvc .gitignore
git commit -m "Add dataset to DVC"
```

## How to Run

### 1. Preprocess Data
```bash
python src/data_preprocessing.py
```

This will:
- Load images from PetImages
- Resize to 224x224 RGB
- Split into train/val/test (80/10/10)
- Apply data augmentation
- Save processed data

### 2. Train Model with MLflow Tracking
```bash
python src/train_model.py
```

This will:
- Load preprocessed data
- Train baseline CNN model
- Log metrics and artifacts to MLflow
- Save trained model

### 3. View MLflow UI
```bash
mlflow ui --backend-store-uri file://$(pwd)/mlruns
```

Then open http://localhost:5000 in your browser.

## Expected Outputs

- Preprocessed datasets in `data/processed/`
- Trained model in `models/`
- MLflow runs in `mlruns/`
- Visualizations in `reports/figures/`
