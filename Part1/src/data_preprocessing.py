"""
Data Preprocessing for Cats vs Dogs Classification

This script:
1. Loads images from PetImages folder
2. Resizes to 224x224 RGB
3. Splits into train/val/test (80/10/10)
4. Applies data augmentation
5. Saves processed data
"""

import os
import shutil
from pathlib import Path
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
import torch
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import json


class CatDogDataset(Dataset):
    """Custom Dataset for Cats and Dogs"""
    
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        label = self.labels[idx]
        
        # Load image
        try:
            image = Image.open(image_path).convert('RGB')
        except Exception as e:
            print(f"Error loading {image_path}: {e}")
            # Return a black image as fallback
            image = Image.new('RGB', (224, 224), color='black')
        
        # Apply transforms
        if self.transform:
            image = self.transform(image)
        
        return image, label


def load_images_from_folder(base_path, class_name, class_label):
    """Load image paths and labels from a folder"""
    folder_path = Path(base_path) / class_name
    image_paths = []
    labels = []
    
    if not folder_path.exists():
        print(f"Warning: {folder_path} does not exist")
        return image_paths, labels
    
    # Supported image formats
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    
    for img_file in folder_path.iterdir():
        if img_file.suffix.lower() in image_extensions:
            image_paths.append(str(img_file))
            labels.append(class_label)
    
    return image_paths, labels


def create_data_splits(image_paths, labels, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1, random_state=42):
    """Split data into train, validation, and test sets"""
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "Ratios must sum to 1.0"
    
    # First split: train vs (val + test)
    X_train, X_temp, y_train, y_temp = train_test_split(
        image_paths, labels, 
        test_size=(val_ratio + test_ratio), 
        random_state=random_state,
        stratify=labels
    )
    
    # Second split: val vs test
    val_size = val_ratio / (val_ratio + test_ratio)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp,
        test_size=(1 - val_size),
        random_state=random_state,
        stratify=y_temp
    )
    
    return {
        'train': (X_train, y_train),
        'val': (X_val, y_val),
        'test': (X_test, y_test)
    }


def get_transforms(mode='train'):
    """Get data transforms for training or validation/test"""
    if mode == 'train':
        return transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])  # ImageNet stats
        ])
    else:  # validation/test
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])


def save_split_info(splits, output_dir):
    """Save split information to JSON"""
    split_info = {}
    for split_name, (paths, labels) in splits.items():
        split_info[split_name] = {
            'num_samples': len(paths),
            'num_cats': sum(1 for l in labels if l == 0),
            'num_dogs': sum(1 for l in labels if l == 1)
        }
    
    output_path = Path(output_dir) / 'split_info.json'
    with open(output_path, 'w') as f:
        json.dump(split_info, f, indent=2)
    
    print(f"Split info saved to {output_path}")
    return split_info


def main():
    """Main preprocessing pipeline"""
    # Paths
    base_dir = Path(__file__).parent.parent.parent
    petimages_dir = base_dir / 'PetImages'
    output_dir = base_dir / 'Part1' / 'data' / 'processed'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 50)
    print("Data Preprocessing Pipeline")
    print("=" * 50)
    
    # Load images
    print("\n1. Loading images...")
    cat_paths, cat_labels = load_images_from_folder(petimages_dir, 'Cat', class_label=0)
    dog_paths, dog_labels = load_images_from_folder(petimages_dir, 'Dog', class_label=1)
    
    print(f"   Found {len(cat_paths)} cat images")
    print(f"   Found {len(dog_paths)} dog images")
    
    # Combine
    all_paths = cat_paths + dog_paths
    all_labels = cat_labels + dog_labels
    
    print(f"\n   Total images: {len(all_paths)}")
    
    # Create splits
    print("\n2. Creating data splits (80/10/10)...")
    splits = create_data_splits(all_paths, all_labels)
    
    # Save split info
    split_info = save_split_info(splits, output_dir)
    
    # Print summary
    print("\n3. Split Summary:")
    for split_name, info in split_info.items():
        print(f"   {split_name.upper()}:")
        print(f"     Total: {info['num_samples']}")
        print(f"     Cats: {info['num_cats']}")
        print(f"     Dogs: {info['num_dogs']}")
    
    # Save split paths and labels
    print("\n4. Saving split data...")
    for split_name, (paths, labels) in splits.items():
        split_data = {
            'paths': paths,
            'labels': labels
        }
        output_file = output_dir / f'{split_name}_data.json'
        with open(output_file, 'w') as f:
            json.dump(split_data, f, indent=2)
        print(f"   Saved {split_name} data to {output_file}")
    
    print("\n" + "=" * 50)
    print("Preprocessing complete!")
    print("=" * 50)


if __name__ == '__main__':
    main()
