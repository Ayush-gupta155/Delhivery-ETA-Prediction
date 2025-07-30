# Grafana Dashboard Setup for Delhivery ETA Prediction API

This guide explains how to set up and use Grafana to visualize metrics from the Delhivery ETA Prediction API.

## Overview

The monitoring stack consists of:
- **FastAPI Application**: Exposes Prometheus metrics at `/metrics` endpoint
- **Prometheus**: Collects and stores metrics from the API
- **Grafana**: Visualizes the collected metrics through dashboards

## Quick Start

1. **Start the monitoring stack:**
   ```bash
   docker-compose up -d
   ```

2. **Access the services:**
   - **API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Prometheus**: http://localhost:9090
   - **Grafana**: http://localhost:3000

3. **Grafana Login:**
   - Username: `admin`
   - Password: `admin`

## Dashboard Features

The Delhivery API Dashboard includes the following visualizations:

### 1. Request Rate (Requests per Second)
- Shows the rate of incoming requests per second
- Color-coded thresholds: Green (normal), Red (high load)

### 2. Response Time (95th Percentile)
- Displays 95th percentile response times
- Thresholds: Green (<1s), Yellow (1-5s), Red (>5s)

### 3. Error Rate
- Percentage of requests resulting in 4xx or 5xx errors
- Thresholds: Green (<1%), Yellow (1-5%), Red (>5%)

### 4. Total Requests by Status Code
- Pie chart showing distribution of HTTP status codes
- Helps identify success vs error patterns

### 5. Request Rate Over Time
- Time series graph showing request patterns
- Useful for identifying traffic spikes and trends

### 6. Response Time Distribution
- Multiple percentile lines (50th, 90th, 95th, 99th)
- Helps understand latency distribution

### 7. Requests by Endpoint
- Table showing total request counts per endpoint
- Instant view of endpoint usage

### 8. Error Rate by Endpoint
- Table showing error rates per endpoint
- Helps identify problematic endpoints

## Available Metrics

The API exposes the following Prometheus metrics:

### Counters
- `req_count_total`: Total number of HTTP requests
  - Labels: `method`, `path`, `status`

### Histograms
- `req_latency_sec`: Request latency in seconds
  - Labels: `method`, `path`
  - Provides quantiles and buckets for latency analysis

## Customizing the Dashboard

### Adding New Panels

1. In Grafana, click the "+" icon in the top right
2. Select "Add panel"
3. Choose your visualization type
4. Use PromQL queries to fetch data

### Useful PromQL Queries

```promql
# Request rate for specific endpoint
rate(req_count_total{path="/predict"}[5m])

# Error rate for specific endpoint
rate(req_count_total{path="/predict", status=~"4..|5.."}[5m]) / rate(req_count_total{path="/predict"}[5m]) * 100

# 95th percentile latency for specific endpoint
histogram_quantile(0.95, rate(req_latency_sec_bucket{path="/predict"}[5m]))

# Success rate
rate(req_count_total{status=~"2.."}[5m]) / rate(req_count_total[5m]) * 100
```

### Setting Up Alerts

1. In Grafana, go to Alerting → Alert Rules
2. Create new alert rules based on metrics
3. Example alert conditions:
   - Error rate > 5%
   - Response time 95th percentile > 5 seconds
   - Request rate > 100 req/s

## Troubleshooting

### No Data in Grafana
1. Check if Prometheus is collecting data:
   - Visit http://localhost:9090
   - Go to Status → Targets
   - Ensure the API target is "UP"

2. Check if the API is exposing metrics:
   - Visit http://localhost:8000/metrics
   - Should see Prometheus-formatted metrics

3. Verify datasource connection:
   - In Grafana, go to Configuration → Data Sources
   - Ensure Prometheus is connected to http://prometheus:9090

### Dashboard Not Loading
1. Check file permissions for dashboard JSON
2. Verify the dashboard provider configuration
3. Restart Grafana container if needed

## Performance Optimization

### For High-Traffic APIs
1. Increase Prometheus scrape interval in `prometheus.yml`
2. Add metric relabeling to reduce cardinality
3. Use recording rules for complex queries
4. Consider using Prometheus remote storage

### For Production Deployment
1. Change default Grafana credentials
2. Set up proper authentication
3. Configure persistent storage
4. Set up backup and retention policies
5. Use HTTPS for all endpoints

## File Structure

```
Task7-Deployment-1/
├── docker-compose.yml              # Main orchestration file
├── prometheus.yml                  # Prometheus configuration
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── prometheus.yml     # Prometheus datasource config
│   │   └── dashboards/
│   │       └── dashboard.yml      # Dashboard provider config
│   └── dashboards/
│       └── delhivery-api-dashboard.json  # Main dashboard
└── GRAFANA_SETUP.md               # This file
```

## Support

For issues or questions:
1. Check the logs: `docker-compose logs grafana`
2. Verify network connectivity between services
3. Ensure all required ports are available
4. Check Prometheus target status

## Next Steps

Consider implementing:
- Custom business metrics (prediction accuracy, model performance)
- Alerting rules for SLA violations
- Integration with external monitoring systems
- Custom dashboards for specific use cases 