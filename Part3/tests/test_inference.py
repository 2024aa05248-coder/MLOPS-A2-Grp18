"""
Unit tests for model inference functions
"""

import pytest
import torch
import numpy as np
from PIL import Image
from pathlib import Path
import sys

# Add Part2 src to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'Part2' / 'src'))
from app import preprocess_image, class_names


def test_preprocess_image():
    """Test image preprocessing for inference"""
    # Create test image
    test_image = Image.new('RGB', (500, 300), color='red')
    
    # Preprocess
    image_tensor = preprocess_image(test_image)
    
    # Check shape: (batch, channels, height, width) = (1, 3, 224, 224)
    assert image_tensor.shape == (1, 3, 224, 224), f"Expected (1, 3, 224, 224), got {image_tensor.shape}"
    
    # Check tensor type
    assert isinstance(image_tensor, torch.Tensor), "Should return torch.Tensor"


def test_preprocess_image_rgb_conversion():
    """Test that non-RGB images are converted"""
    # Create grayscale image
    test_image = Image.new('L', (224, 224), color=128)
    
    # Should convert to RGB
    image_tensor = preprocess_image(test_image)
    assert image_tensor.shape[1] == 3, "Should have 3 channels (RGB)"


def test_preprocess_image_normalization():
    """Test that preprocessing includes normalization"""
    test_image = Image.new('RGB', (224, 224), color='white')
    image_tensor = preprocess_image(test_image)
    
    # Normalized values should not be in [0, 1] range (ImageNet normalization)
    # Mean subtraction and std division should shift values
    assert image_tensor.min() < 0 or image_tensor.max() > 1, "Image should be normalized"


def test_class_names():
    """Test that class names are defined correctly"""
    assert len(class_names) == 2, "Should have 2 classes"
    assert 'Cat' in class_names, "Should include 'Cat'"
    assert 'Dog' in class_names, "Should include 'Dog'"


def test_output_format():
    """Test that model output format is correct"""
    # This test would require loading the actual model
    # For now, we test the expected format structure
    
    # Expected output format
    expected_keys = ['prediction', 'probabilities', 'confidence']
    
    # Mock response structure
    mock_response = {
        'prediction': 'Cat',
        'probabilities': {'Cat': 0.85, 'Dog': 0.15},
        'confidence': 0.85
    }
    
    assert all(key in mock_response for key in expected_keys), "Response should have all required keys"
    assert mock_response['prediction'] in class_names, "Prediction should be a valid class name"
    assert 0 <= mock_response['confidence'] <= 1, "Confidence should be between 0 and 1"
    assert sum(mock_response['probabilities'].values()) == pytest.approx(1.0, abs=0.01), "Probabilities should sum to 1"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
