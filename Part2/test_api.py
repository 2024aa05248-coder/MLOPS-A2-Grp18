"""
Test script for API endpoints
"""

import requests
from pathlib import Path
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health check endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✓ Health check passed\n")


def test_predict():
    """Test prediction endpoint"""
    print("Testing /predict endpoint...")
    
    # Find a test image (use first available image from dataset)
    base_dir = Path(__file__).parent.parent
    petimages_dir = base_dir / 'PetImages'
    
    # Try to find a cat or dog image
    test_image_path = None
    for folder in ['Cat', 'Dog']:
        folder_path = petimages_dir / folder
        if folder_path.exists():
            for img_file in folder_path.iterdir():
                if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    test_image_path = img_file
                    break
            if test_image_path:
                break
    
    if not test_image_path:
        print("⚠ No test image found. Skipping prediction test.")
        return
    
    print(f"Using test image: {test_image_path}")
    
    with open(test_image_path, 'rb') as f:
        files = {'file': (test_image_path.name, f, 'image/jpeg')}
        response = requests.post(f"{BASE_URL}/predict", files=files)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    result = response.json()
    assert "prediction" in result
    assert "probabilities" in result
    assert "confidence" in result
    print("✓ Prediction test passed\n")


if __name__ == "__main__":
    print("=" * 50)
    print("API Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_health()
        test_predict()
        print("=" * 50)
        print("All tests passed!")
        print("=" * 50)
    except Exception as e:
        print(f"✗ Test failed: {e}")
        exit(1)
