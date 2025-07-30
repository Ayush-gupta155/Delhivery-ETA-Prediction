#!/bin/bash

echo "🚚 Delhivery ETA Prediction API - Monitoring Stack"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Start the monitoring stack
echo "🚀 Starting monitoring stack..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "📊 Checking service status..."

# Check API
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ API is running at http://localhost:8000"
else
    echo "❌ API is not responding"
fi

# Check Prometheus
if curl -s http://localhost:9090/-/healthy > /dev/null; then
    echo "✅ Prometheus is running at http://localhost:9090"
else
    echo "❌ Prometheus is not responding"
fi

# Check Grafana
if curl -s http://localhost:3000/api/health > /dev/null; then
    echo "✅ Grafana is running at http://localhost:3000"
else
    echo "❌ Grafana is not responding"
fi

echo ""
echo "🎉 Monitoring stack is ready!"
echo ""
echo "📱 Access Points:"
echo "   • API: http://localhost:8000"
echo "   • API Docs: http://localhost:8000/docs"
echo "   • Prometheus: http://localhost:9090"
echo "   • Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "📈 To generate test data and see metrics:"
echo "   python3 generate_test_data.py"
echo ""
echo "🛑 To stop the stack:"
echo "   docker-compose down"
echo ""
echo "📋 To view logs:"
echo "   docker-compose logs -f" 