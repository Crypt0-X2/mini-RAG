# 🐳 Docker Guide for Mini RAG

Complete guide to running Mini RAG with Docker.

---

## 📋 Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Docker Compose** v2.0+
- **API Keys**: Jina AI, Pinecone, Groq

---

## 🚀 Quick Start

### 1. Setup Environment Variables

```bash
# Copy the template
cp .env.docker .env

# Edit .env and add your API keys
# Required: JINA_API_KEY, PINECONE_API_KEY, GROQ_API_KEY
```

### 2. Start Development Environment

**Windows (PowerShell):**
```powershell
.\scripts\docker-dev.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/docker-dev.sh
./scripts/docker-dev.sh
```

**Or manually:**
```bash
docker-compose up --build
```

### 3. Access the Application

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

---

## 🏭 Production Deployment

### Build and Run Production

**Windows:**
```powershell
.\scripts\docker-prod.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/docker-prod.sh
./scripts/docker-prod.sh
```

**Or manually:**
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

### Access Production

- **Frontend**: http://localhost
- **Backend**: http://localhost:8001

---

## 📁 Docker Files Overview

| File | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage backend build (Python 3.11) |
| `frontend/Dockerfile` | Production frontend (Node + Nginx) |
| `frontend/Dockerfile.dev` | Development frontend (hot reload) |
| `docker-compose.yml` | Development environment |
| `docker-compose.prod.yml` | Production environment |
| `.env.docker` | Environment variable template |
| `.dockerignore` | Files excluded from builds |

---

## 🛠️ Common Commands

### Development

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild images
docker-compose up --build
```

### Production

```bash
# Start production
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop production
docker-compose -f docker-compose.prod.yml down

# Restart a service
docker-compose -f docker-compose.prod.yml restart backend
```

### Cleanup

**Windows:**
```powershell
.\scripts\docker-clean.ps1
```

**Linux/Mac:**
```bash
./scripts/docker-clean.sh
```

**Or manually:**
```bash
# Stop and remove containers, networks, volumes
docker-compose down -v
docker-compose -f docker-compose.prod.yml down -v

# Remove images
docker rmi mini-rag-backend:latest
docker rmi mini-rag-frontend:latest

# Remove dangling images
docker image prune -f
```

---

## 🔍 Debugging

### View Container Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Execute Commands in Container

```bash
# Backend shell
docker-compose exec backend bash

# Frontend shell
docker-compose exec frontend sh

# Run Python in backend
docker-compose exec backend python -c "print('Hello')"
```

### Check Container Health

```bash
# List running containers
docker-compose ps

# Inspect container
docker inspect mini-rag-backend-dev

# Check health status
docker inspect --format='{{.State.Health.Status}}' mini-rag-backend-dev
```

---

## 🏗️ Architecture

### Development Setup

```
┌─────────────────────────────────────────┐
│         Docker Network (Bridge)         │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Backend    │    │   Frontend   │  │
│  │              │    │              │  │
│  │ FastAPI      │◄───┤ Vite Dev     │  │
│  │ Port: 8001   │    │ Port: 5173   │  │
│  │              │    │              │  │
│  │ Hot Reload ✓ │    │ Hot Reload ✓ │  │
│  └──────────────┘    └──────────────┘  │
│         ▲                    ▲          │
│         │                    │          │
└─────────┼────────────────────┼──────────┘
          │                    │
    Volume Mount          Volume Mount
    (./backend)          (./frontend)
```

### Production Setup

```
┌─────────────────────────────────────────┐
│         Docker Network (Bridge)         │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Backend    │    │   Frontend   │  │
│  │              │    │              │  │
│  │ Uvicorn      │◄───┤ Nginx        │  │
│  │ Port: 8001   │    │ Port: 80     │  │
│  │              │    │              │  │
│  │ Multi-stage  │    │ Multi-stage  │  │
│  │ Non-root     │    │ Optimized    │  │
│  │ Health check │    │ Gzip enabled │  │
│  └──────────────┘    └──────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## ⚙️ Configuration

### Environment Variables

All environment variables are loaded from `.env` file:

```env
# Required API Keys
JINA_API_KEY=your_key
PINECONE_API_KEY=your_key
GROQ_API_KEY=your_key

# Optional Settings (with defaults)
CHUNK_SIZE=1000
CHUNK_OVERLAP=120
RETRIEVAL_TOP_K=20
RERANK_TOP_K=5
```

### Resource Limits (Production)

**Backend:**
- CPU: 0.5-1.0 cores
- Memory: 256MB-512MB

**Frontend:**
- CPU: 0.25-0.5 cores
- Memory: 64MB-128MB

---

## 🔒 Security Features

### Backend
- ✅ Non-root user (UID 1000)
- ✅ Minimal base image (python:3.11-slim)
- ✅ No secrets in image
- ✅ Health checks enabled

### Frontend
- ✅ Nginx security headers
- ✅ Gzip compression
- ✅ Static asset caching
- ✅ Alpine base image

---

## 📊 Image Sizes

| Image | Size | Optimization |
|-------|------|--------------|
| Backend | ~200MB | Multi-stage build, slim base |
| Frontend | ~25MB | Nginx Alpine, static files only |

**Comparison:**
- Without optimization: ~700MB total
- With optimization: ~225MB total
- **Savings: 68%** 🎉

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to Docker daemon"

**Solution:**
```bash
# Windows: Start Docker Desktop
# Linux: Start Docker service
sudo systemctl start docker
```

### Issue: "Port already in use"

**Solution:**
```bash
# Find process using port
# Windows:
netstat -ano | findstr :8001

# Linux/Mac:
lsof -i :8001

# Kill the process or change port in docker-compose.yml
```

### Issue: "Build failed - no space left on device"

**Solution:**
```bash
# Clean up Docker
docker system prune -a --volumes

# Remove unused images
docker image prune -a
```

### Issue: "Backend health check failing"

**Solution:**
```bash
# Check backend logs
docker-compose logs backend

# Verify environment variables
docker-compose exec backend env | grep API_KEY

# Test health endpoint manually
docker-compose exec backend curl http://localhost:8001/health
```

### Issue: "Frontend shows 'Offline' status"

**Solution:**
```bash
# Check if backend is running
docker-compose ps

# Verify network connectivity
docker-compose exec frontend ping backend

# Check VITE_API_BASE_URL
docker-compose exec frontend env | grep VITE
```

---

## 🚀 CI/CD Integration

### GitHub Actions Example

```yaml
name: Docker Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Backend
        run: docker build -t mini-rag-backend .
      
      - name: Build Frontend
        run: docker build -t mini-rag-frontend ./frontend
      
      - name: Test
        run: |
          docker-compose up -d
          sleep 10
          curl http://localhost:8001/health
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

## 💡 Tips

1. **Use `.env` for secrets** - Never commit API keys
2. **Volume mounts for development** - Enables hot reload
3. **Multi-stage builds** - Reduces image size significantly
4. **Health checks** - Ensures services are ready
5. **Resource limits** - Prevents resource exhaustion
6. **Logging** - Rotate logs to prevent disk fill

---

## 🎯 Next Steps

After mastering Docker:
1. Deploy to cloud (AWS ECS, Google Cloud Run)
2. Set up Kubernetes for orchestration
3. Implement CI/CD pipeline
4. Add monitoring (Prometheus + Grafana)
5. Set up log aggregation (ELK stack)
