#!/bin/bash

echo "🚀 Starting TikTok Prompt Generator v4.0"
echo "========================================="

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check for Supabase env vars
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_SERVICE_ROLE_KEY" ]; then
    echo "⚠️  Warning: Supabase environment variables not set"
    echo "   Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env"
    echo "   for database features"
fi
# Kill existing processes on ports 8000 and 3000
echo "📡 Cleaning ports..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Start backend
echo "📡 Starting FastAPI backend on port 8000..."
cd ~/TikTok-Prompt-Generator/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 5
# Check if backend is running
if ! curl -s http://localhost:8000/docs > /dev/null; then
    echo "❌ Backend failed to start"
    exit 1
fi
echo "✅ Backend running on http://localhost:8000"

# Start frontend
echo "🎨 Starting React frontend on port 3000..."
cd ~/TikTok-Prompt-Generator/frontend

# Install dependencies if node_modules missing
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================="
echo "✅ TikTok Prompt Generator v4.0 Running!"
echo "========================================="
echo ""
echo "   Frontend:    http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs:    http://localhost:8000/docs"
echo ""
echo "   Features:"
echo "   - Real checkbox table"
echo "   - Select All / Delete selected"
echo "   - Export to CSV"
echo "   - Taglish localization"
echo "   - 11 niche categories"
echo "   - 4-card output protocol"
echo ""
echo "   Press Ctrl+C to stop both servers"
echo "========================================="

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
