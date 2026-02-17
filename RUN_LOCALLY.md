# 🚀 Run Mini-RAG Locally (No Docker Needed)

## Quick Start - 5 Minutes

### Step 1: Setup Backend

Open PowerShell and run:

```powershell
cd C:\Users\shara\Downloads\mini-RAG\backend

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```powershell
# Still in backend folder
# Copy the example env file
cp .env.example .env

# Open .env in notepad
notepad .env
```

**Add your API keys to .env:**
```env
JINA_API_KEY=your_actual_jina_key_here
PINECONE_API_KEY=your_actual_pinecone_key_here
GROQ_API_KEY=your_actual_groq_key_here
```

Save and close.

### Step 3: Start Backend

```powershell
# Still in backend folder with venv activated
uvicorn app.main:app --reload --port 8001
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
```

**Leave this terminal running!**

### Step 4: Setup Frontend (New Terminal)

Open a **NEW PowerShell window**:

```powershell
cd C:\Users\shara\Downloads\mini-RAG\frontend

# Install dependencies
npm install

# Copy env file
cp .env.example .env

# Start frontend
npm run dev
```

You should see:
```
VITE ready in XXX ms
Local: http://localhost:5173
```

### Step 5: Open Your App

Go to: **http://localhost:5173**

## ✅ You're Done!

Your RAG application is now running locally. You can:
- Ingest documents
- Query them
- See citations

## 🐳 Fix Docker Later

Once your app is working, we can fix Docker by:
1. Restarting Docker Desktop completely
2. Or updating Docker Desktop to latest version
3. Or switching Docker settings

But for now, **local development works perfectly!**
