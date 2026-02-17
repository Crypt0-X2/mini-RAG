# Docker Troubleshooting - INTERNAL_ERROR Fix

## Issue
Getting `INTERNAL_ERROR` when running `docker-compose up --build`

## Root Cause
This is a known issue with Docker Desktop on Windows, often caused by:
1. Docker BuildKit issues
2. WSL2 backend problems  
3. Docker daemon instability

## Solutions (Try in Order)

### Solution 1: Disable BuildKit (Quickest Fix)

**Windows PowerShell:**
```powershell
# Set environment variable to disable BuildKit
$env:DOCKER_BUILDKIT=0
$env:COMPOSE_DOCKER_CLI_BUILD=0

# Now try again
docker-compose up --build
```

**Or create a `.env` file in project root:**
```env
DOCKER_BUILDKIT=0
COMPOSE_DOCKER_CLI_BUILD=0
```

### Solution 2: Restart Docker Desktop

1. Right-click Docker Desktop icon in system tray
2. Select "Restart Docker Desktop"
3. Wait for Docker to fully restart (30-60 seconds)
4. Try again: `docker-compose up --build`

### Solution 3: Build Images Separately

Instead of using `docker-compose up --build`, build each image individually:

```powershell
# Build backend
docker build -t mini-rag-backend:latest -f Dockerfile .

# Build frontend  
docker build -t mini-rag-frontend-dev:latest -f frontend/Dockerfile.dev frontend/

# Start services (without --build)
docker-compose up
```

### Solution 4: Use Pre-built Images (Skip Build)

Modify `docker-compose.yml` to skip building:

```yaml
services:
  backend:
    image: python:3.11-slim
    # Remove build section, use direct image
    working_dir: /app
    volumes:
      - ./backend:/app
    command: sh -c "pip install -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"
    # ... rest of config
```

### Solution 5: Reset Docker Desktop

**Complete Reset (Last Resort):**
1. Docker Desktop → Settings → Troubleshoot
2. Click "Clean / Purge data"
3. Restart Docker Desktop
4. Try again

### Solution 6: Switch to WSL2 Backend

1. Docker Desktop → Settings → General
2. Ensure "Use WSL 2 based engine" is checked
3. Apply & Restart
4. Try again

## Quick Test Command

After trying any solution, test with:

```powershell
# Simple test
docker run --rm hello-world

# If that works, try building backend only
docker build -t test-backend -f Dockerfile .
```

## Alternative: Run Without Docker (Temporary)

If Docker continues to fail, you can run locally:

**Backend:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

**Frontend (new terminal):**
```powershell
cd frontend
npm install
npm run dev
```

## Recommended Immediate Action

**Try Solution 1 first** (disable BuildKit):

```powershell
# In PowerShell
$env:DOCKER_BUILDKIT=0
$env:COMPOSE_DOCKER_CLI_BUILD=0
docker-compose up --build
```

This solves 80% of INTERNAL_ERROR cases on Windows.
