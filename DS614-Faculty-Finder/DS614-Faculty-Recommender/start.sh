#!/bin/bash

# Stop any running containers using these ports
echo "🧹 Cleaning up old containers..."
docker-compose down 2>/dev/null || true
docker stop $(docker ps -q --filter ancestor=faculty-recommender) 2>/dev/null || true

# Build and start
echo "🚀 Starting Faculty Recommender..."
docker-compose up --build
