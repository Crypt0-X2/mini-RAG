# ================================
# Mini RAG - Docker Cleanup (Windows)
# ================================
# This script stops and removes all Docker containers, networks, and volumes

Write-Host "🧹 Cleaning up Mini RAG Docker environment..." -ForegroundColor Green
Write-Host ""

# Stop and remove development containers
Write-Host "🛑 Stopping development containers..." -ForegroundColor Cyan
docker-compose down -v

# Stop and remove production containers
Write-Host "🛑 Stopping production containers..." -ForegroundColor Cyan
docker-compose -f docker-compose.prod.yml down -v

# Optional: Remove images
$response = Read-Host "Do you want to remove Docker images as well? (y/N)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "🗑️  Removing Docker images..." -ForegroundColor Yellow
    docker rmi mini-rag-backend:latest 2>$null
    docker rmi mini-rag-frontend:latest 2>$null
    $danglingImages = docker images -f "dangling=true" -q
    if ($danglingImages) {
        docker rmi $danglingImages 2>$null
    }
}

Write-Host ""
Write-Host "✅ Cleanup complete!" -ForegroundColor Green
