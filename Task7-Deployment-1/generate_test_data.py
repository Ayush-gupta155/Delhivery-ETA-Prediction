#!/usr/bin/env python3
"""
Test script to generate API calls and populate metrics for Grafana visualization
"""

import requests
import time
import random
import json
from concurrent.futures import ThreadPoolExecutor
import threading

# API base URL
API_BASE = "http://localhost:8000"

def generate_delivery_data():
    """Generate realistic delivery data for testing"""
    return {
        "osrm_distance": random.uniform(1000, 50000),  # 1-50 km
        "osrm_time": random.uniform(60, 3600),  # 1-60 minutes
        "actual_distance_to_destination": random.uniform(1000, 50000),
        "cutoff_factor": random.uniform(0.8, 1.2),
        "factor": random.uniform(0.9, 1.1),
        "time_difference": random.uniform(-300, 300),
        "distance_per_min": random.uniform(500, 2000),
        "planned_duration": random.uniform(1800, 7200),
        "actual_vs_osrm_time": random.uniform(-600, 600),
        "is_cutoff": random.choice([True, False]),
        "is_heavy_delay": random.choice([True, False]),
        "start_scan_to_end_scan": random.uniform(0, 3600),
        "start_to_cutoff_mins": random.uniform(0, 120),
        "center_pair_count": random.uniform(0, 10),
        "cutoff_hour": random.uniform(0, 23),
        "od_start_time_hour": random.uniform(0, 23),
        "cutoff_timestamp_weekday": random.uniform(0, 6),
        "destination_center": random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]),
        "destination_name": random.choice(["Office", "Home", "Warehouse", "Store", "Factory"])
    }

def make_prediction_request():
    """Make a single prediction request"""
    try:
        data = generate_delivery_data()
        response = requests.post(f"{API_BASE}/predict", json=data, timeout=10)
        return response.status_code
    except Exception as e:
        print(f"Request failed: {e}")
        return 500

def make_batch_request():
    """Make a batch prediction request"""
    try:
        batch_data = {
            "deliveries": [generate_delivery_data() for _ in range(random.randint(1, 5))]
        }
        response = requests.post(f"{API_BASE}/predict/batch", json=batch_data, timeout=15)
        return response.status_code
    except Exception as e:
        print(f"Batch request failed: {e}")
        return 500

def make_health_check():
    """Make a health check request"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        return response.status_code
    except Exception as e:
        print(f"Health check failed: {e}")
        return 500

def make_model_info_request():
    """Make a model info request"""
    try:
        response = requests.get(f"{API_BASE}/model/info", timeout=5)
        return response.status_code
    except Exception as e:
        print(f"Model info request failed: {e}")
        return 500

def worker(worker_id, duration=60):
    """Worker function to generate continuous load"""
    print(f"Worker {worker_id} started")
    end_time = time.time() + duration
    
    while time.time() < end_time:
        # Randomly choose request type
        request_type = random.choices(
            ['predict', 'batch', 'health', 'model_info'],
            weights=[0.6, 0.2, 0.1, 0.1]
        )[0]
        
        if request_type == 'predict':
            status = make_prediction_request()
        elif request_type == 'batch':
            status = make_batch_request()
        elif request_type == 'health':
            status = make_health_check()
        else:
            status = make_model_info_request()
        
        # Add some random delay between requests
        time.sleep(random.uniform(0.1, 2.0))
        
        if status != 200:
            print(f"Worker {worker_id}: {request_type} returned {status}")
    
    print(f"Worker {worker_id} finished")

def generate_error_scenarios():
    """Generate some error scenarios to test error rate visualization"""
    print("Generating error scenarios...")
    
    # Invalid data
    invalid_data = {"invalid_field": "invalid_value"}
    try:
        response = requests.post(f"{API_BASE}/predict", json=invalid_data, timeout=5)
        print(f"Invalid data request: {response.status_code}")
    except Exception as e:
        print(f"Invalid data request failed: {e}")
    
    # Missing required fields
    incomplete_data = {"osrm_distance": 1000}  # Missing other required fields
    try:
        response = requests.post(f"{API_BASE}/predict", json=incomplete_data, timeout=5)
        print(f"Incomplete data request: {response.status_code}")
    except Exception as e:
        print(f"Incomplete data request failed: {e}")
    
    # Non-existent endpoint
    try:
        response = requests.get(f"{API_BASE}/nonexistent", timeout=5)
        print(f"Non-existent endpoint: {response.status_code}")
    except Exception as e:
        print(f"Non-existent endpoint failed: {e}")

def main():
    """Main function to orchestrate the test data generation"""
    print("🚚 Delhivery API Test Data Generator")
    print("=" * 50)
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and healthy")
        else:
            print(f"⚠️  API returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("Please ensure the API is running with: docker-compose up -d")
        return
    
    # Generate some error scenarios first
    generate_error_scenarios()
    
    # Start multiple workers to generate load
    num_workers = 3
    duration = 120  # 2 minutes
    
    print(f"\nStarting {num_workers} workers for {duration} seconds...")
    print("This will generate various API calls to populate metrics.")
    print("You can monitor the results in Grafana at http://localhost:3000")
    print("Press Ctrl+C to stop early\n")
    
    try:
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [
                executor.submit(worker, i, duration) 
                for i in range(num_workers)
            ]
            
            # Wait for all workers to complete
            for future in futures:
                future.result()
                
    except KeyboardInterrupt:
        print("\n🛑 Test stopped by user")
    
    print("\n✅ Test data generation completed!")
    print("\n📊 Next steps:")
    print("1. Open Grafana: http://localhost:3000 (admin/admin)")
    print("2. View the 'Delhivery ETA Prediction API Dashboard'")
    print("3. Check Prometheus: http://localhost:9090 for raw metrics")
    print("4. Explore different time ranges and refresh intervals")

if __name__ == "__main__":
    main() 