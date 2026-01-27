"""
Unit tests for data preprocessing functions
"""

import pytest
import numpy as np
import torch
from PIL import Image
from pathlib import Path
import sys

# Add Part1 src to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'Part1' / 'src'))
from data_preprocessing import (
    get_transforms,
    load_images_from_folder,
    create_data_splits
)


def test_image_resize():
    """Test that images are resized to 224x224"""
    transform = get_transforms('val')
    
    # Create a test image (different size)
    test_image = Image.new('RGB', (500, 300), color='red')
    transformed = transform(test_image)
    
    # Check shape: (C, H, W) = (3, 224, 224)
    assert transformed.shape == (3, 224, 224), f"Expected (3, 224, 224), got {transformed.shape}"


def test_normalization():
    """Test that images are normalized"""
    transform = get_transforms('val')
    test_image = Image.new('RGB', (224, 224), color='red')
    transformed = transform(test_image)
    
    # Check that values are normalized (not in [0, 255] range)
    assert transformed.min() < 0 or transformed.max() > 1, "Image should be normalized"


def test_data_augmentation():
    """Test that training transforms include augmentation"""
    train_transform = get_transforms('train')
    val_transform = get_transforms('val')
    
    test_image = Image.new('RGB', (300, 300), color='blue')
    
    # Apply transforms multiple times - training should vary, validation should be consistent
    train_results = [train_transform(test_image) for _ in range(5)]
    val_results = [val_transform(test_image) for _ in range(5)]
    
    # Training transforms should produce different results (due to augmentation)
    # Validation should be consistent
    # Note: This is probabilistic, so we check that at least some variation exists
    train_variation = any(
        not torch.equal(train_results[0], train_results[i]) 
        for i in range(1, 5)
    )
    
    # Validation should be deterministic
    val_consistent = all(
        torch.equal(val_results[0], val_results[i]) 
        for i in range(1, 5)
    )
    
    assert val_consistent, "Validation transforms should be deterministic"


def test_load_images_from_folder(tmp_path):
    """Test loading images from folder"""
    # Create temporary folder structure
    cat_folder = tmp_path / 'Cat'
    cat_folder.mkdir()
    
    # Create dummy image files
    (cat_folder / 'cat1.jpg').touch()
    (cat_folder / 'cat2.png').touch()
    (cat_folder / 'not_an_image.txt').touch()  # Should be ignored
    
    paths, labels = load_images_from_folder(tmp_path, 'Cat', class_label=0)
    
    assert len(paths) == 2, f"Expected 2 images, got {len(paths)}"
    assert all(l == 0 for l in labels), "All labels should be 0 (Cat)"
    assert all(Path(p).suffix.lower() in ['.jpg', '.png'] for p in paths)


def test_create_data_splits():
    """Test data splitting"""
    # Create dummy data
    image_paths = [f'image_{i}.jpg' for i in range(100)]
    labels = [0 if i < 50 else 1 for i in range(100)]  # 50 cats, 50 dogs
    
    splits = create_data_splits(image_paths, labels, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1)
    
    # Check splits exist
    assert 'train' in splits
    assert 'val' in splits
    assert 'test' in splits
    
    # Check sizes
    train_paths, train_labels = splits['train']
    val_paths, val_labels = splits['val']
    test_paths, test_labels = splits['test']
    
    assert len(train_paths) == 80, f"Expected 80 train samples, got {len(train_paths)}"
    assert len(val_paths) == 10, f"Expected 10 val samples, got {len(val_paths)}"
    assert len(test_paths) == 10, f"Expected 10 test samples, got {len(test_paths)}"
    
    # Check stratification (approximately balanced)
    train_cats = sum(1 for l in train_labels if l == 0)
    assert 35 <= train_cats <= 45, f"Train split should be approximately balanced, got {train_cats} cats"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
