#!/bin/bash
# ================================
# Mini RAG - Production Build & Deploy
# ================================
# This script builds and starts the production environment

echo "🏭 Building Mini RAG Production Environment..."
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env from .env.docker template and add your API keys."
    exit 1
fi

# Build and start production services
echo "🐳 Building production images..."
docker-compose -f docker-compose.prod.yml build

echo ""
echo "🚀 Starting production containers..."
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "✅ Production environment is running!"
echo ""
echo "📊 Service URLs:"
echo "   Frontend: http://localhost"
echo "   Backend:  http://localhost:8001"
echo ""
echo "📝 View logs:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose -f docker-compose.prod.yml down"
