#!/bin/bash

echo "🚀 Quick Start - TikTok Prompt Generator"

# Check if gradio is installed
if ! python3 -c "import gradio" 2>/dev/null; then
    echo "📦 Installing gradio..."
    pip3 install gradio
fi

# Run the app
echo "🎬 Starting TikTok Prompt Generator..."
echo "   Open http://localhost:7860 in your browser"
echo "   Press Ctrl+C to stop"
echo ""
python3 app.py
