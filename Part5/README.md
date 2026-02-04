# Part 5: Monitoring, Logs & Final Submission (M5)

## Objective
Monitor the deployed model and submit a consolidated package of all artifacts.

## Tasks Completed

### 1. Basic Monitoring & Logging ✅
- ✅ Request/response logging in inference service (excludes sensitive data)
- ✅ Track metrics: request count, latency (p50, p95, p99), error rate
- ✅ Prometheus + Grafana monitoring stack
- ✅ Structured JSON logging with timestamps

### 2. Model Performance Tracking (Post-Deployment) ✅
- ✅ Metrics collector to gather predictions vs true labels
- ✅ Performance tracker for calculating accuracy, precision, recall, F1
- ✅ Confusion matrix generation
- ✅ Comparison with training metrics

## Project Structure

```
Part5/
├── README.md                           # This file
├── src/
│   ├── __init__.py
│   ├── app_with_monitoring.py         # Enhanced API with monitoring
│   ├── metrics_collector.py           # Collect predictions from API
│   └── performance_tracker.py         # Calculate performance metrics
├── config/
│   ├── prometheus.yml                 # Prometheus scrape config
│   ├── grafana-datasource.yml         # Grafana datasource config
│   └── grafana-dashboard-provider.yml # Dashboard provisioning
├── dashboards/
│   └── api-dashboard.json             # Pre-configured Grafana dashboard
└── docker-compose-monitoring.yml      # Full monitoring stack
```

## Quick Start

### Prerequisites
```bash
# Install required Python packages
pip install prometheus-client requests scikit-learn matplotlib seaborn

# Ensure Docker is running
docker --version
```

### Step 1: Start Monitoring Stack

```bash
# Navigate to Part5 directory
cd Part5

# Start the monitoring stack (API + Prometheus + Grafana)
docker-compose -f docker-compose-monitoring.yml up -d

# Check services are running
docker-compose -f docker-compose-monitoring.yml ps
```

**Access Points:**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (login: admin/admin)

### Step 2: Verify Monitoring

```bash
# Check health endpoint
curl http://localhost:8000/health

# Check metrics endpoint
curl http://localhost:8000/metrics

# Test prediction (replace with actual image path)
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -F "file=@path/to/test/image.jpg"
```

### Step 3: View Grafana Dashboard

1. Open Grafana at http://localhost:3000
2. Login with `admin` / `admin`
3. Navigate to Dashboards → "Cats vs Dogs API Monitoring"
4. View real-time metrics:
   - Request rate and total requests
   - Latency percentiles (P50, P95, P99)
   - Prediction distribution (Cat vs Dog)
   - Model inference latency

### Step 4: Collect Performance Metrics

```bash
# Collect predictions from test dataset
python src/metrics_collector.py \
  --api-url http://localhost:8000 \
  --test-data ../Part1/data/processed/test_data.json \
  --output predictions_results.json \
  --limit 100

# Calculate performance metrics
python src/performance_tracker.py \
  --predictions predictions_results.json \
  --output performance_metrics.json \
  --plot \
  --plot-output confusion_matrix.png

# Compare with training metrics (if available)
python src/performance_tracker.py \
  --predictions predictions_results.json \
  --output performance_metrics.json \
  --compare ../Part1/models/training_metrics.json
```

### Step 5: Stop Monitoring Stack

```bash
# Stop all services
docker-compose -f docker-compose-monitoring.yml down

# Stop and remove volumes (clean slate)
docker-compose -f docker-compose-monitoring.yml down -v
```

## Metrics Tracked

### Application Metrics (Prometheus)
- `http_requests_total` - Total HTTP requests by method, endpoint, and status
- `http_request_duration_seconds` - Request latency histogram
- `model_predictions_total` - Total predictions by class (Cat/Dog)
- `model_prediction_duration_seconds` - Model inference latency histogram

### Performance Metrics (Post-Deployment)
- **Accuracy** - Overall classification accuracy
- **Precision** - Per-class and macro/weighted averages
- **Recall** - Per-class and macro/weighted averages
- **F1-Score** - Per-class and macro/weighted averages
- **Confusion Matrix** - True vs predicted labels
- **Support** - Number of samples per class

## Logging Implementation

### Log Format (Structured JSON)
```json
{
  "timestamp": "2026-02-04T12:00:00Z",
  "level": "INFO",
  "message": "Prediction made",
  "endpoint": "/predict",
  "prediction": "Cat",
  "confidence": 0.8542,
  "prediction_latency_ms": 45.23
}
```

### What We Log ✅
- Request metadata (method, endpoint, status code)
- Response times (latency in milliseconds)
- Prediction results (class, confidence)
- Errors and exceptions with stack traces

### What We DON'T Log ❌
- Image data (too large, not useful)
- Sensitive user information
- Full request payloads
- Binary data

## Post-Deployment Performance Tracking

### How It Works

1. **Metrics Collector** (`metrics_collector.py`)
   - Loads test images from Part1 test dataset
   - Sends images to deployed API for prediction
   - Extracts true labels from file paths
   - Saves predictions and true labels to JSON

2. **Performance Tracker** (`performance_tracker.py`)
   - Loads collected predictions
   - Calculates comprehensive metrics using scikit-learn
   - Generates confusion matrix visualization
   - Compares with training metrics to detect drift

### Metrics Calculated
- **Accuracy**: Overall classification accuracy
- **Per-Class Metrics**: Precision, Recall, F1-score for Cat and Dog
- **Macro Average**: Unweighted mean of per-class metrics
- **Weighted Average**: Weighted by class support
- **Confusion Matrix**: Visual representation of predictions vs true labels

### Drift Detection
- Compares post-deployment accuracy with training accuracy
- Alerts if difference exceeds 5% threshold
- Helps identify model degradation in production

## Key Features Implemented

### 1. Enhanced API with Monitoring
- Prometheus metrics integration
- Structured JSON logging
- Request/response middleware
- Health and metrics endpoints

### 2. Monitoring Stack
- **Prometheus**: Scrapes metrics every 15 seconds
- **Grafana**: Pre-configured dashboard with 8 panels
  - Request rate and total requests
  - P95 latency
  - Request rate by status code
  - Latency percentiles (P50, P95, P99)
  - Prediction distribution (pie chart)
  - Model inference latency

### 3. Performance Tracking Tools
- **metrics_collector.py**: Automated prediction collection
- **performance_tracker.py**: Comprehensive metric calculation
- Confusion matrix visualization
- Training vs deployment comparison

## Outputs Generated

1. **Real-time Monitoring**
   - Grafana dashboard at http://localhost:3000
   - Prometheus metrics at http://localhost:9090
   - API metrics endpoint at http://localhost:8000/metrics

2. **Performance Analysis Files**
   - `predictions_results.json` - Collected predictions and true labels
   - `performance_metrics.json` - Calculated metrics (accuracy, precision, recall, F1)
   - `confusion_matrix.png` - Visual confusion matrix

3. **Logs**
   - Structured JSON logs in Docker container
   - View with: `docker logs cats-dogs-api-monitoring`

## Troubleshooting

### API Not Starting
```bash
# Check if model exists
ls ../Part1/models/model.pt

# Check Docker logs
docker logs cats-dogs-api-monitoring
```

### Prometheus Not Scraping
```bash
# Check Prometheus targets
# Open http://localhost:9090/targets
# Ensure 'cats-dogs-api' target is UP
```

### Grafana Dashboard Not Loading
```bash
# Check dashboard provisioning
docker exec grafana ls /var/lib/grafana/dashboards

# Restart Grafana
docker-compose -f docker-compose-monitoring.yml restart grafana
```

### Metrics Collection Fails
```bash
# Ensure API is running
curl http://localhost:8000/health

# Check test data path
ls ../Part1/data/processed/test_data.json

# Run with verbose output
python src/metrics_collector.py --api-url http://localhost:8000 \
  --test-data ../Part1/data/processed/test_data.json \
  --limit 10
```

## Assignment Requirements Met ✅

### M5 Task 1: Basic Monitoring & Logging ✅
- ✅ Request/response logging enabled (excludes sensitive data)
- ✅ Tracks request count via Prometheus counter
- ✅ Tracks latency via Prometheus histogram
- ✅ Prometheus + Grafana monitoring stack
- ✅ Pre-configured dashboard with 8 visualization panels

### M5 Task 2: Model Performance Tracking ✅
- ✅ Collects batch of requests with true labels
- ✅ Calculates accuracy, precision, recall, F1-score
- ✅ Generates confusion matrix
- ✅ Compares with training metrics
- ✅ Detects performance drift (5% threshold)
