"""
Performance Tracker for Post-Deployment Model Evaluation

Calculates comprehensive metrics from collected predictions:
- Accuracy, Precision, Recall, F1-score
- Confusion Matrix
- Per-class metrics
"""

import json
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)
from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class PerformanceTracker:
    """Track and analyze post-deployment model performance"""
    
    def __init__(self, predictions: List[str] = None, true_labels: List[str] = None):
        self.predictions = predictions or []
        self.true_labels = true_labels or []
        self.class_names = ['Cat', 'Dog']
        self.metrics = {}
    
    def load_from_file(self, predictions_file: str):
        """Load predictions from JSON file"""
        with open(predictions_file, 'r') as f:
            data = json.load(f)
        
        self.predictions = data['predictions']
        self.true_labels = data['true_labels']
        
        print(f"Loaded {len(self.predictions)} predictions from {predictions_file}")
    
    def calculate_metrics(self) -> Dict:
        """Calculate all performance metrics"""
        if not self.predictions or not self.true_labels:
            raise ValueError("No predictions or true labels available")
        
        # Overall accuracy
        accuracy = accuracy_score(self.true_labels, self.predictions)
        
        # Per-class metrics
        precision, recall, f1, support = precision_recall_fscore_support(
            self.true_labels,
            self.predictions,
            labels=self.class_names,
            average=None
        )
        
        # Macro and weighted averages
        precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
            self.true_labels,
            self.predictions,
            average='macro'
        )
        
        precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(
            self.true_labels,
            self.predictions,
            average='weighted'
        )
        
        # Confusion matrix
        cm = confusion_matrix(self.true_labels, self.predictions, labels=self.class_names)
        
        # Store metrics
        self.metrics = {
            'accuracy': float(accuracy),
            'per_class': {
                self.class_names[i]: {
                    'precision': float(precision[i]),
                    'recall': float(recall[i]),
                    'f1_score': float(f1[i]),
                    'support': int(support[i])
                }
                for i in range(len(self.class_names))
            },
            'macro_avg': {
                'precision': float(precision_macro),
                'recall': float(recall_macro),
                'f1_score': float(f1_macro)
            },
            'weighted_avg': {
                'precision': float(precision_weighted),
                'recall': float(recall_weighted),
                'f1_score': float(f1_weighted)
            },
            'confusion_matrix': cm.tolist(),
            'total_samples': len(self.predictions)
        }
        
        return self.metrics
    
    def print_metrics(self):
        """Print metrics in a readable format"""
        if not self.metrics:
            self.calculate_metrics()
        
        print("\n" + "="*60)
        print("POST-DEPLOYMENT PERFORMANCE METRICS")
        print("="*60)
        
        print(f"\nTotal Samples: {self.metrics['total_samples']}")
        print(f"Overall Accuracy: {self.metrics['accuracy']:.4f}")
        
        print("\n" + "-"*60)
        print("PER-CLASS METRICS")
        print("-"*60)
        print(f"{'Class':<10} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
        print("-"*60)
        
        for class_name in self.class_names:
            metrics = self.metrics['per_class'][class_name]
            print(f"{class_name:<10} {metrics['precision']:<12.4f} {metrics['recall']:<12.4f} "
                  f"{metrics['f1_score']:<12.4f} {metrics['support']:<10}")
        
        print("\n" + "-"*60)
        print("MACRO AVERAGE")
        print("-"*60)
        macro = self.metrics['macro_avg']
        print(f"Precision: {macro['precision']:.4f}")
        print(f"Recall:    {macro['recall']:.4f}")
        print(f"F1-Score:  {macro['f1_score']:.4f}")
        
        print("\n" + "-"*60)
        print("WEIGHTED AVERAGE")
        print("-"*60)
        weighted = self.metrics['weighted_avg']
        print(f"Precision: {weighted['precision']:.4f}")
        print(f"Recall:    {weighted['recall']:.4f}")
        print(f"F1-Score:  {weighted['f1_score']:.4f}")
        
        print("\n" + "-"*60)
        print("CONFUSION MATRIX")
        print("-"*60)
        cm = np.array(self.metrics['confusion_matrix'])
        print(f"{'':>10} {'Predicted Cat':>15} {'Predicted Dog':>15}")
        print(f"{'Actual Cat':<10} {cm[0][0]:>15} {cm[0][1]:>15}")
        print(f"{'Actual Dog':<10} {cm[1][0]:>15} {cm[1][1]:>15}")
        print("="*60 + "\n")
    
    def save_metrics(self, output_file: str):
        """Save metrics to JSON file"""
        if not self.metrics:
            self.calculate_metrics()
        
        with open(output_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        print(f"Metrics saved to {output_file}")
    
    def plot_confusion_matrix(self, output_file: str = None):
        """Plot and optionally save confusion matrix"""
        if not self.metrics:
            self.calculate_metrics()
        
        cm = np.array(self.metrics['confusion_matrix'])
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=self.class_names, 
                    yticklabels=self.class_names)
        plt.title('Confusion Matrix - Post-Deployment')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Confusion matrix plot saved to {output_file}")
        else:
            plt.show()
        
        plt.close()
    
    def compare_with_training(self, training_metrics_file: str):
        """Compare post-deployment metrics with training metrics"""
        if not self.metrics:
            self.calculate_metrics()
        
        try:
            with open(training_metrics_file, 'r') as f:
                training_metrics = json.load(f)
            
            print("\n" + "="*60)
            print("COMPARISON: TRAINING vs POST-DEPLOYMENT")
            print("="*60)
            
            # Compare accuracy
            train_acc = training_metrics.get('test_accuracy', training_metrics.get('accuracy', 0))
            deploy_acc = self.metrics['accuracy']
            
            print(f"\nAccuracy:")
            print(f"  Training:        {train_acc:.4f}")
            print(f"  Post-Deployment: {deploy_acc:.4f}")
            print(f"  Difference:      {deploy_acc - train_acc:+.4f}")
            
            # Compare per-class metrics if available
            if 'per_class' in training_metrics:
                print("\nPer-Class F1-Score Comparison:")
                for class_name in self.class_names:
                    if class_name in training_metrics['per_class']:
                        train_f1 = training_metrics['per_class'][class_name].get('f1_score', 0)
                        deploy_f1 = self.metrics['per_class'][class_name]['f1_score']
                        print(f"  {class_name}:")
                        print(f"    Training:        {train_f1:.4f}")
                        print(f"    Post-Deployment: {deploy_f1:.4f}")
                        print(f"    Difference:      {deploy_f1 - train_f1:+.4f}")
            
            # Drift detection
            drift_threshold = 0.05  # 5% threshold
            if abs(deploy_acc - train_acc) > drift_threshold:
                print(f"\n⚠️  WARNING: Significant performance drift detected!")
                print(f"   Accuracy difference exceeds {drift_threshold:.1%} threshold")
            else:
                print(f"\n✓ Performance is stable (within {drift_threshold:.1%} threshold)")
            
            print("="*60 + "\n")
            
        except FileNotFoundError:
            print(f"Warning: Training metrics file not found: {training_metrics_file}")
        except Exception as e:
            print(f"Error comparing with training metrics: {e}")


def main():
    """Main function to calculate and display performance metrics"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Calculate post-deployment performance metrics')
    parser.add_argument('--predictions', required=True, help='Path to predictions JSON file')
    parser.add_argument('--output', default='performance_metrics.json', help='Output metrics file')
    parser.add_argument('--plot', action='store_true', help='Generate confusion matrix plot')
    parser.add_argument('--plot-output', default='confusion_matrix.png', help='Plot output file')
    parser.add_argument('--compare', help='Path to training metrics JSON for comparison')
    
    args = parser.parse_args()
    
    # Initialize tracker
    tracker = PerformanceTracker()
    
    # Load predictions
    tracker.load_from_file(args.predictions)
    
    # Calculate metrics
    tracker.calculate_metrics()
    
    # Print metrics
    tracker.print_metrics()
    
    # Save metrics
    tracker.save_metrics(args.output)
    
    # Plot confusion matrix
    if args.plot:
        tracker.plot_confusion_matrix(args.plot_output)
    
    # Compare with training metrics
    if args.compare:
        tracker.compare_with_training(args.compare)


if __name__ == "__main__":
    main()
