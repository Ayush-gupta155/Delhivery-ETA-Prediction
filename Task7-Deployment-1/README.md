
# 🚚 XGBoost Delivery Time Prediction API - Task 7 Deployment

**Team Member:** Laavanjan  
**Task:** Unified Inference Pipeline + API Development  
**Project:** Delhivery Logistics - Task 7 Deployment

---


## 📝 README

### Overview
This project delivers a production-ready REST API for predicting delivery times using a trained XGBoost model. The solution includes a unified inference pipeline, robust input validation, batch and single prediction endpoints, and automated tests.

### Folder Structure
```
Task7-Deployment/
├── inference_pipeline.py    # Unified inference pipeline
├── api_app.py              # FastAPI application
├── test_api.py             # API testing suite
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

### Key Features
- **Unified Inference Pipeline:**
  - Loads XGBoost model and preprocessing objects
  - Validates and preprocesses input data (ensures correct feature order/count)
  - Handles missing values and type conversions
  - Supports both single and batch predictions
- **FastAPI REST API:**
  - `/predict`: Single prediction endpoint
  - `/predict/batch`: Batch prediction endpoint
  - `/health`: Health check endpoint
  - `/model/info`: Model metadata endpoint
  - `/docs`: Interactive API documentation (Swagger UI)
- **Automated Testing:**
  - `test_api.py` covers all endpoints and error handling
- **Comprehensive Logging & Error Handling**

### How It Works
1. **Start the API Server**
   ```bash
   python api_app.py
   ```
   The API will be available at `http://localhost:8000`.

2. **Test the API**
   ```bash
   python test_api.py
   ```
   This runs all endpoint tests and prints results.

3. **Manual Testing**
   - Open `http://localhost:8000/docs` in your browser for interactive API testing.

### Input/Output Example
**Single Prediction Request:**
```json
{
  "osrm_distance": 5200,
  "osrm_time": 950,
  "actual_distance_to_destination": 5100,
  "cutoff_factor": 1.1,
  "factor": 0.95,
  "time_difference": 120,
  "distance_per_min": 5.5,
  "planned_duration": 1000,
  "actual_vs_osrm_time": 30,
  "is_cutoff": false,
  "is_heavy_delay": false,
  "start_scan_to_end_scan": 980,
  "start_to_cutoff_mins": 15,
  "center_pair_count": 2,
  "cutoff_hour": 17,
  "od_start_time_hour": 9,
  "cutoff_timestamp_weekday": 2,
  "destination_center": "Delhi_Hub",
  "destination_name": "Customer_Location_1"
}
```
**Response:**
```json
{
  "success": true,
  "prediction": {
    "predicted_time_seconds": 1462.455078125,
    "predicted_time_minutes": 24.374250411987305,
    "predicted_time_formatted": "0h 24m"
  },
  "model_info": {
    "model_type": "XGBoost",
    "version": "1.0",
    "features_used": 50
  },
  "request_id": "req_1753358479965",
  "timestamp": "2025-07-24T17:31:19.990460",
  "processing_time_ms": 24.924278259277344
}
```

### How to Extend or Integrate
- Add new features or endpoints in `api_app.py` as needed
- Update `inference_pipeline.py` if the model or feature engineering changes
- Use `test_api.py` to validate any changes before deployment

---

**Ready for integration and handoff to other team members (containerization, monitoring, deployment, etc.)**
