#!/bin/bash

echo "========================================="
echo "🚀 Deploying to Hugging Face Space"
echo "========================================="

# Check if we're in git repo
if [ ! -d .git ]; then
    echo "❌ Not in git repository!"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Check if HF remote exists
if ! git remote | grep -q "space"; then
    echo "📡 Adding Hugging Face Space remote..."
    git remote add space https://huggingface.co/spaces/hoopstreet/TikTok-Prompt-Generator
else
    echo "✅ HF Space remote already exists"
fi

# Verify we have the latest code
echo "📦 Current branch: $(git branch --show-current)"
echo "📦 Latest commit: $(git log -1 --oneline)"

# Check if we have the HF Space token
if [ -n "$HF_TOKEN" ]; then
    echo "✅ HF_TOKEN found"
    # Use token for authentication
    git remote set-url space https://hoopstreet:$HF_TOKEN@huggingface.co/spaces/hoopstreet/TikTok-Prompt-Generator
else
    echo "⚠️  HF_TOKEN not set"
    echo "You will need to enter credentials manually"
fi

echo ""
echo "========================================="
echo "To push to HF Space, run:"
echo "  git push space main"
echo ""
echo "Or if you need to force push:"
echo "  git push space main --force"
echo "========================================="
