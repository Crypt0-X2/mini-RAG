#!/bin/bash
# ================================
# Mini RAG - Docker Cleanup
# ================================
# This script stops and removes all Docker containers, networks, and volumes

echo "🧹 Cleaning up Mini RAG Docker environment..."
echo ""

# Stop and remove development containers
echo "🛑 Stopping development containers..."
docker-compose down -v

# Stop and remove production containers
echo "🛑 Stopping production containers..."
docker-compose -f docker-compose.prod.yml down -v

# Optional: Remove images
read -p "Do you want to remove Docker images as well? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing Docker images..."
    docker rmi mini-rag-backend:latest 2>/dev/null || true
    docker rmi mini-rag-frontend:latest 2>/dev/null || true
    docker rmi $(docker images -f "dangling=true" -q) 2>/dev/null || true
fi

echo ""
echo "✅ Cleanup complete!"
