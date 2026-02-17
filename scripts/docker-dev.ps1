# ================================
# Mini RAG - Development Environment (Windows)
# ================================
# This script starts the development environment with hot reload

Write-Host "🚀 Starting Mini RAG Development Environment..." -ForegroundColor Green
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from .env.docker template..."
    Copy-Item ".env.docker" ".env"
    Write-Host "✅ Created .env file. Please edit it with your API keys before continuing." -ForegroundColor Green
    Write-Host ""
    Read-Host "Press Enter after you've added your API keys to .env"
}

# Start services
Write-Host "🐳 Starting Docker containers..." -ForegroundColor Cyan
docker-compose up --build

# Note: Use Ctrl+C to stop
