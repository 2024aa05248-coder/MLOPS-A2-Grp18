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
import random

# Default API URL (can be overridden via environment variable)
API_URL = "http://localhost:8000"


def test_health_check(require_model=True):
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

        # In CI environments without the model, allow model_loaded to be False
        if require_model:
            assert response.json()["model_loaded"] == True, "Model should be loaded"
        else:
            print(f"Model loaded: {response.json()['model_loaded']} (model check skipped in CI)")

        print("Health check passed\n")
        return True

    except Exception as e:
        print(f"Health check failed: {e}\n")
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
    image_files = []

    # Collect all valid image files
    for folder in ['Dog', 'Cat']:
        folder_path = petimages_dir / folder
        if folder_path.exists():
            for img_file in folder_path.iterdir():
                if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    image_files.append(img_file)

    # Pick a random one
    if image_files:
        test_image_path = random.choice(image_files)
    
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
        
        print("Prediction test passed\n")
        return True
    
    except Exception as e:
        print(f"Prediction test failed: {e}\n")
        return False


def main():
    """Run all smoke tests"""
    import os

    # Allow API URL override via environment variable
    global API_URL
    API_URL = os.getenv("API_URL", API_URL)

    # Check if we're running in CI environment (where model might not be available)
    ci_mode = os.getenv("CI_MODE", "false").lower() == "true"
    require_model = not ci_mode

    print(f"Testing API at: {API_URL}")
    if ci_mode:
        print("Running in CI mode (model checks relaxed)\n")
    else:
        print("")

    results = []
    results.append(test_health_check(require_model=require_model))

    # Skip prediction test in CI if model is not available
    if ci_mode:
        print("Skipping prediction test in CI mode\n")
    else:
        results.append(test_prediction())

    print("=" * 50)
    if all(results):
        print("All smoke tests passed!")
        print("=" * 50)
        sys.exit(0)
    else:
        print("Some smoke tests failed!")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
