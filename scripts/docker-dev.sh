#!/bin/bash
# ================================
# Mini RAG - Development Environment
# ================================
# This script starts the development environment with hot reload

echo "🚀 Starting Mini RAG Development Environment..."
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env from .env.docker template..."
    cp .env.docker .env
    echo "✅ Created .env file. Please edit it with your API keys before continuing."
    echo ""
    read -p "Press Enter after you've added your API keys to .env..."
fi

# Start services
echo "🐳 Starting Docker containers..."
docker-compose up --build

# Note: Use Ctrl+C to stop
