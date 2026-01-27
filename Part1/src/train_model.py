"""
Model Training with MLflow Tracking

This script:
1. Loads preprocessed data
2. Trains a baseline CNN model
3. Logs metrics and artifacts to MLflow
4. Saves trained model
"""

import json
import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from pathlib import Path
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from data_preprocessing import CatDogDataset, get_transforms


class SimpleCNN(nn.Module):
    """Simple CNN for binary image classification"""
    
    def __init__(self, num_classes=2):
        super(SimpleCNN, self).__init__()
        
        # Convolutional layers
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        
        # Pooling
        self.pool = nn.MaxPool2d(2, 2)
        
        # Fully connected layers
        self.fc1 = nn.Linear(128 * 28 * 28, 512)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(512, num_classes)
        
        # Activation
        self.relu = nn.ReLU()
    
    def forward(self, x):
        # Conv block 1
        x = self.pool(self.relu(self.bn1(self.conv1(x))))
        
        # Conv block 2
        x = self.pool(self.relu(self.bn2(self.conv2(x))))
        
        # Conv block 3
        x = self.pool(self.relu(self.bn3(self.conv3(x))))
        
        # Flatten
        x = x.view(-1, 128 * 28 * 28)
        
        # FC layers
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x


def train_epoch(model, dataloader, criterion, optimizer, device):
    """Train for one epoch"""
    model.train()
    running_loss = 0.0
    all_preds = []
    all_labels = []
    
    for images, labels in dataloader:
        images, labels = images.to(device), labels.to(device)
        
        # Forward pass
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # Metrics
        running_loss += loss.item()
        _, preds = torch.max(outputs, 1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
    
    epoch_loss = running_loss / len(dataloader)
    epoch_acc = accuracy_score(all_labels, all_preds)
    
    return epoch_loss, epoch_acc


def validate(model, dataloader, criterion, device):
    """Validate model"""
    model.eval()
    running_loss = 0.0
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    epoch_loss = running_loss / len(dataloader)
    epoch_acc = accuracy_score(all_labels, all_preds)
    precision = precision_score(all_labels, all_preds, average='weighted')
    recall = recall_score(all_labels, all_preds, average='weighted')
    f1 = f1_score(all_labels, all_preds, average='weighted')
    
    return epoch_loss, epoch_acc, precision, recall, f1, all_preds, all_labels


def plot_confusion_matrix(y_true, y_pred, save_path):
    """Plot and save confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Cat', 'Dog'], 
                yticklabels=['Cat', 'Dog'])
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_loss_curves(train_losses, val_losses, save_path):
    """Plot training and validation loss curves"""
    plt.figure(figsize=(10, 6))
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def main():
    """Main training pipeline"""
    # Paths
    base_dir = Path(__file__).parent.parent.parent
    data_dir = base_dir / 'Part1' / 'data' / 'processed'
    models_dir = base_dir / 'Part1' / 'models'
    reports_dir = base_dir / 'Part1' / 'reports' / 'figures'
    mlruns_dir = base_dir / 'Part1' / 'mlruns'
    
    models_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # MLflow setup
    mlflow.set_tracking_uri(f"file://{mlruns_dir.absolute()}")
    mlflow.set_experiment("cats_vs_dogs_classification")
    
    # Hyperparameters
    config = {
        'batch_size': 32,
        'learning_rate': 0.001,
        'num_epochs': 10,
        'random_state': 42
    }
    
    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Load data splits
    print("Loading data splits...")
    with open(data_dir / 'train_data.json', 'r') as f:
        train_data = json.load(f)
    with open(data_dir / 'val_data.json', 'r') as f:
        val_data = json.load(f)
    
    # Create datasets
    train_dataset = CatDogDataset(
        train_data['paths'], 
        train_data['labels'],
        transform=get_transforms('train')
    )
    val_dataset = CatDogDataset(
        val_data['paths'],
        val_data['labels'],
        transform=get_transforms('val')
    )
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=config['batch_size'], shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=config['batch_size'], shuffle=False)
    
    # Initialize model
    model = SimpleCNN(num_classes=2).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config['learning_rate'])
    
    # Training loop
    print("\nStarting training...")
    train_losses = []
    val_losses = []
    
    with mlflow.start_run():
        # Log parameters
        mlflow.log_params(config)
        mlflow.log_param("model", "SimpleCNN")
        
        for epoch in range(config['num_epochs']):
            print(f"\nEpoch {epoch+1}/{config['num_epochs']}")
            
            # Train
            train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
            train_losses.append(train_loss)
            
            # Validate
            val_loss, val_acc, val_precision, val_recall, val_f1, val_preds, val_labels = validate(
                model, val_loader, criterion, device
            )
            val_losses.append(val_loss)
            
            # Log metrics
            mlflow.log_metrics({
                'train_loss': train_loss,
                'train_accuracy': train_acc,
                'val_loss': val_loss,
                'val_accuracy': val_acc,
                'val_precision': val_precision,
                'val_recall': val_recall,
                'val_f1': val_f1
            }, step=epoch)
            
            print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
            print(f"  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
        
        # Final validation metrics
        final_val_loss, final_val_acc, final_val_precision, final_val_recall, final_val_f1, final_preds, final_labels = validate(
            model, val_loader, criterion, device
        )
        
        # Plot confusion matrix
        cm_path = reports_dir / 'confusion_matrix.png'
        plot_confusion_matrix(final_labels, final_preds, cm_path)
        mlflow.log_artifact(str(cm_path))
        
        # Plot loss curves
        loss_curve_path = reports_dir / 'loss_curves.png'
        plot_loss_curves(train_losses, val_losses, loss_curve_path)
        mlflow.log_artifact(str(loss_curve_path))
        
        # Save model
        model_path = models_dir / 'model.pt'
        torch.save(model.state_dict(), model_path)
        mlflow.pytorch.log_model(model, "model")
        
        print(f"\nModel saved to {model_path}")
        print(f"Final Validation Accuracy: {final_val_acc:.4f}")
        print(f"Final Validation F1: {final_val_f1:.4f}")
    
    print("\nTraining complete!")


if __name__ == '__main__':
    main()
