# ================================
# Mini RAG - Production Build & Deploy (Windows)
# ================================
# This script builds and starts the production environment

Write-Host "🏭 Building Mini RAG Production Environment..." -ForegroundColor Green
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ Error: .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env from .env.docker template and add your API keys."
    exit 1
}

# Build and start production services
Write-Host "🐳 Building production images..." -ForegroundColor Cyan
docker-compose -f docker-compose.prod.yml build

Write-Host ""
Write-Host "🚀 Starting production containers..." -ForegroundColor Cyan
docker-compose -f docker-compose.prod.yml up -d

Write-Host ""
Write-Host "✅ Production environment is running!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Service URLs:" -ForegroundColor Yellow
Write-Host "   Frontend: http://localhost"
Write-Host "   Backend:  http://localhost:8001"
Write-Host ""
Write-Host "📝 View logs:" -ForegroundColor Yellow
Write-Host "   docker-compose -f docker-compose.prod.yml logs -f"
Write-Host ""
Write-Host "🛑 Stop services:" -ForegroundColor Yellow
Write-Host "   docker-compose -f docker-compose.prod.yml down"
