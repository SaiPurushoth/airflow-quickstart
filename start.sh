#!/bin/bash

# Airflow Docker Setup Script
# This script initializes and starts Apache Airflow with Docker

set -e

echo "================================================"
echo "  Apache Airflow Docker Setup"
echo "================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed."
    echo "Please install Docker from https://www.docker.com/get-started"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker is not running."
    echo "Please start Docker and try again."
    exit 1
fi

echo "✓ Docker is installed and running"
echo ""

# Create necessary directories
echo "Creating required directories..."
mkdir -p ./dags ./logs ./plugins ./config
echo "✓ Directories created"
echo ""

# Set proper permissions for Airflow
echo "Setting up permissions..."
echo -e "AIRFLOW_UID=$(id -u)" > .env
echo "_AIRFLOW_WWW_USER_USERNAME=airflow" >> .env
echo "_AIRFLOW_WWW_USER_PASSWORD=airflow" >> .env
echo "✓ Permissions configured"
echo ""

# Initialize Airflow database
echo "Initializing Airflow (this may take a few minutes)..."
docker compose up airflow-init
echo "✓ Airflow initialized"
echo ""

# Start Airflow services
echo "Starting Airflow services..."
docker compose up -d
echo "✓ Airflow services started"
echo ""

# Wait for services to be healthy
echo "Waiting for Airflow to be ready..."
sleep 10

if docker compose ps airflow-webserver --filter "status=running" | grep -q airflow-webserver; then
    echo ""
    echo "================================================"
    echo "  ✓ Airflow is now running!"
    echo "================================================"
    echo ""
    echo "Access the Airflow UI at: http://localhost:8080"
    echo ""
    echo "Login credentials:"
    echo "  Username: airflow"
    echo "  Password: airflow"
    echo ""
    echo "Available DAGs:"
    echo "  - example_hello_world: Simple Hello World DAG"
    echo "  - example_data_pipeline: ETL Pipeline example"
    echo ""
    echo "Useful commands:"
    echo "  - View logs: docker compose logs -f"
    echo "  - Stop Airflow: docker compose down"
    echo "  - Restart Airflow: docker compose restart"
    echo "  - Stop and remove all data: docker compose down -v"
    echo ""
    echo "================================================"
else
    echo "❌ Error: Airflow services failed to start"
    echo "Check logs with: docker compose logs"
    exit 1
fi