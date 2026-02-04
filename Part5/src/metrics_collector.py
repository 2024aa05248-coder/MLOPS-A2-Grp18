"""
Metrics Collector for Post-Deployment Performance Tracking

Collects predictions from the deployed model and compares with true labels
to calculate post-deployment performance metrics.
"""

import json
import requests
from pathlib import Path
from typing import List, Dict, Tuple
import time
from PIL import Image


class MetricsCollector:
    """Collect predictions and true labels for performance tracking"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.predictions = []
        self.true_labels = []
        self.image_paths = []
        
    def load_test_data(self, test_data_path: str, limit: int = None) -> List[str]:
        """Load test data paths from JSON file"""
        with open(test_data_path, 'r') as f:
            data = json.load(f)
        
        paths = data.get('paths', [])
        
        if limit:
            paths = paths[:limit]
        
        return paths
    
    def extract_true_label(self, image_path: str) -> str:
        """Extract true label from image path (Cat or Dog)"""
        path = Path(image_path)
        # Path format: .../PetImages/Cat/xxx.jpg or .../PetImages/Dog/xxx.jpg
        if 'Cat' in path.parts:
            return 'Cat'
        elif 'Dog' in path.parts:
            return 'Dog'
        else:
            raise ValueError(f"Cannot determine label from path: {image_path}")
    
    def predict_image(self, image_path: str) -> Dict:
        """Send image to API and get prediction"""
        try:
            with open(image_path, 'rb') as f:
                files = {'file': (Path(image_path).name, f, 'image/jpeg')}
                response = requests.post(
                    f"{self.api_url}/predict",
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error predicting {image_path}: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception predicting {image_path}: {e}")
            return None
    
    def collect_predictions(self, image_paths: List[str], verbose: bool = True) -> Tuple[List[str], List[str]]:
        """
        Collect predictions for a batch of images
        
        Returns:
            Tuple of (predictions, true_labels)
        """
        self.predictions = []
        self.true_labels = []
        self.image_paths = []
        
        total = len(image_paths)
        
        for idx, image_path in enumerate(image_paths):
            if verbose and (idx + 1) % 10 == 0:
                print(f"Processing {idx + 1}/{total} images...")
            
            # Get true label
            try:
                true_label = self.extract_true_label(image_path)
            except ValueError as e:
                print(f"Skipping {image_path}: {e}")
                continue
            
            # Get prediction
            result = self.predict_image(image_path)
            
            if result and 'prediction' in result:
                self.predictions.append(result['prediction'])
                self.true_labels.append(true_label)
                self.image_paths.append(image_path)
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.1)
        
        if verbose:
            print(f"\nCollected {len(self.predictions)} predictions")
        
        return self.predictions, self.true_labels
    
    def save_results(self, output_path: str):
        """Save collected predictions and true labels to JSON"""
        results = {
            'predictions': self.predictions,
            'true_labels': self.true_labels,
            'image_paths': self.image_paths,
            'total_samples': len(self.predictions)
        }
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to {output_path}")
    
    def load_results(self, input_path: str):
        """Load previously collected results"""
        with open(input_path, 'r') as f:
            results = json.load(f)
        
        self.predictions = results['predictions']
        self.true_labels = results['true_labels']
        self.image_paths = results.get('image_paths', [])
        
        print(f"Loaded {len(self.predictions)} predictions from {input_path}")


def main():
    """Main function to collect predictions"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Collect predictions for performance tracking')
    parser.add_argument('--api-url', default='http://localhost:8000', help='API URL')
    parser.add_argument('--test-data', required=True, help='Path to test_data.json')
    parser.add_argument('--output', default='predictions_results.json', help='Output file path')
    parser.add_argument('--limit', type=int, default=100, help='Number of samples to test (default: 100)')
    
    args = parser.parse_args()
    
    # Initialize collector
    collector = MetricsCollector(api_url=args.api_url)
    
    # Load test data
    print(f"Loading test data from {args.test_data}")
    image_paths = collector.load_test_data(args.test_data, limit=args.limit)
    print(f"Loaded {len(image_paths)} test images")
    
    # Check API health
    try:
        response = requests.get(f"{args.api_url}/health", timeout=5)
        if response.status_code == 200:
            print(f"API is healthy: {response.json()}")
        else:
            print(f"Warning: API health check failed with status {response.status_code}")
    except Exception as e:
        print(f"Error: Cannot connect to API at {args.api_url}")
        print(f"Error details: {e}")
        return
    
    # Collect predictions
    print("\nCollecting predictions...")
    predictions, true_labels = collector.collect_predictions(image_paths)
    
    # Save results
    collector.save_results(args.output)
    
    # Print summary
    correct = sum(1 for p, t in zip(predictions, true_labels) if p == t)
    accuracy = correct / len(predictions) if predictions else 0
    print(f"\nQuick Summary:")
    print(f"  Total predictions: {len(predictions)}")
    print(f"  Correct: {correct}")
    print(f"  Accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    main()
