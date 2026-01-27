"""
Post-deployment smoke tests

Tests:
1. Health check endpoint
2. Prediction endpoint with test image
"""

import requests
import sys
from pathlib import Path
import json

# Default API URL (can be overridden via environment variable)
API_URL = "http://localhost:8000"


def test_health_check():
    """Test health check endpoint"""
    print("=" * 50)
    print("Smoke Test: Health Check")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json()["status"] == "healthy", "Service should be healthy"
        assert response.json()["model_loaded"] == True, "Model should be loaded"
        
        print("✓ Health check passed\n")
        return True
    
    except Exception as e:
        print(f"✗ Health check failed: {e}\n")
        return False


def test_prediction():
    """Test prediction endpoint"""
    print("=" * 50)
    print("Smoke Test: Prediction")
    print("=" * 50)
    
    # Find a test image
    base_dir = Path(__file__).parent.parent.parent
    petimages_dir = base_dir / 'PetImages'
    
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
        return True
    
    try:
        print(f"Using test image: {test_image_path}")
        
        with open(test_image_path, 'rb') as f:
            files = {'file': (test_image_path.name, f, 'image/jpeg')}
            response = requests.post(f"{API_URL}/predict", files=files, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert "prediction" in result, "Response should contain 'prediction'"
        assert "probabilities" in result, "Response should contain 'probabilities'"
        assert "confidence" in result, "Response should contain 'confidence'"
        assert result["prediction"] in ["Cat", "Dog"], "Prediction should be Cat or Dog"
        assert 0 <= result["confidence"] <= 1, "Confidence should be between 0 and 1"
        
        print("✓ Prediction test passed\n")
        return True
    
    except Exception as e:
        print(f"✗ Prediction test failed: {e}\n")
        return False


def main():
    """Run all smoke tests"""
    import os
    
    # Allow API URL override via environment variable
    global API_URL
    API_URL = os.getenv("API_URL", API_URL)
    
    print(f"Testing API at: {API_URL}\n")
    
    results = []
    results.append(test_health_check())
    results.append(test_prediction())
    
    print("=" * 50)
    if all(results):
        print("✓ All smoke tests passed!")
        print("=" * 50)
        sys.exit(0)
    else:
        print("✗ Some smoke tests failed!")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
