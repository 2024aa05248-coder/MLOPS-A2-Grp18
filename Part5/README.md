# Part 5: Monitoring, Logs & Final Submission (M5)

## Objective
Monitor the deployed model and submit a consolidated package of all artifacts.

## Tasks

### 1. Basic Monitoring & Logging
- Enable request/response logging in inference service
  - Exclude sensitive data
  - Log request count, latency, status codes
- Track basic metrics:
  - Request count
  - Latency (p50, p95, p99)
  - Error rate
- Options:
  - **Prometheus** + Grafana (recommended)
  - Simple in-app counters
  - Log-based metrics

### 2. Model Performance Tracking (Post-Deployment)
- Collect batch of real or simulated requests
- Track predictions vs true labels
- Calculate post-deployment metrics:
  - Accuracy
  - Precision, Recall, F1
  - Confusion matrix

## Project Structure

```
Part5/
├── README.md                    # This file
├── src/
│   ├── app_with_monitoring.py  # Enhanced API with monitoring
│   ├── metrics_collector.py    # Metrics collection utilities
│   └── performance_tracker.py  # Post-deployment performance tracking
├── config/
│   ├── prometheus.yml          # Prometheus configuration
│   └── grafana-datasource.yml  # Grafana datasource config
├── dashboards/
│   └── api-dashboard.json      # Grafana dashboard
└── docker-compose-monitoring.yml  # Monitoring stack
```

## Monitoring Setup

### Option 1: Prometheus + Grafana

#### Prerequisites
```bash
pip install prometheus-client
```

#### Components
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Application**: Exposes `/metrics` endpoint

#### Run Monitoring Stack
```bash
docker-compose -f docker-compose-monitoring.yml up -d
```

Access:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

### Option 2: Simple Logging

- Log to files or stdout
- Track metrics in-memory
- Export via `/metrics` endpoint

## Metrics to Track

### Application Metrics
- `http_requests_total` - Total request count
- `http_request_duration_seconds` - Request latency
- `http_requests_errors_total` - Error count
- `model_predictions_total` - Total predictions
- `model_prediction_duration_seconds` - Prediction latency

### Business Metrics
- Prediction distribution (Cat vs Dog)
- Confidence score distribution
- Request rate (requests/second)

## Logging

### Log Format
```json
{
  "timestamp": "2026-01-25T12:00:00Z",
  "level": "INFO",
  "endpoint": "/predict",
  "method": "POST",
  "status_code": 200,
  "latency_ms": 45,
  "prediction": "Cat",
  "confidence": 0.85
}
```

### What to Log
- Request metadata (endpoint, method, status)
- Performance metrics (latency)
- Prediction results (class, confidence)
- Errors and exceptions

### What NOT to Log
- Image data (too large)
- Sensitive user information
- Full request payloads

## Post-Deployment Performance Tracking

### Collect Test Data
- Use test set from Part1
- Or simulate requests with known labels
- Track predictions and true labels

### Calculate Metrics
- Accuracy
- Precision, Recall, F1-score
- Confusion matrix
- ROC-AUC (if applicable)

### Report
- Compare with training metrics
- Identify drift or degradation
- Document findings

## Expected Outputs

- Monitoring dashboard (Grafana or custom)
- Metrics endpoint (`/metrics`)
- Logs with proper formatting
- Post-deployment performance report
- Comparison with training metrics

## Final Submission Checklist

- [ ] All code committed to repository
- [ ] All parts (1-5) completed
- [ ] Documentation complete
- [ ] Monitoring setup and working
- [ ] Performance tracking completed
- [ ] Final report/documentation ready
