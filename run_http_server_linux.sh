#!/bin/bash

# Get the current directory where the script is located
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

echo "Building Docker image..."
docker build -t test-http-server "$SCRIPT_DIR"
if [ $? -ne 0 ]; then
    echo "Docker image build failed. Exiting."
    exit 1
fi

echo "Running Docker container..."
docker run -d --name test-http-server -p 80:5000 -v "$SCRIPT_DIR":/app/uploads test-http-server
if [ $? -ne 0 ]; then
    echo "Docker container run failed. Exiting."
    exit 1
fi

echo "Docker container is running. You can access it at http://127.0.0.1."
