#!/bin/bash

# Navigate to backend and start FastAPI (on port 8000)

cd "backend"
echo "Starting FastAPI backend..."

# ✅ Activate virtual environment (Windows-compatible)
source venv/Scripts/activate

uvicorn app:app --reload &
BACKEND_PID=$!
cd ..


# Navigate to frontend and start Vite dev server (on port 5173)
echo "Starting frontend (Vite)..."
cd "frontend"
npm install
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Both backend (http://localhost:8000) and frontend (http://localhost:5173) are running."

echo ""
echo "To stop everything, run:"
echo "kill $BACKEND_PID $FRONTEND_PID"

# Optionally, you can start the local app (uncomment if desired)
cd "local-app"
echo "Starting local app..."
source venv/Scripts/activate
python main.py &
LOCALAPP_PID=$!
cd ..
echo "Local app PID: $LOCALAPP_PID"

# Wait for background jobs (optional, or just exit)
wait