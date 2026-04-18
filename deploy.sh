#!/bin/sh

echo "nameserver 8.8.8.8" > /etc/resolv.conf
cd ~/TikTok-Prompt-Generator

# Require version
if [ -z "$1" ]; then
  echo "Usage: ./deploy.sh v1.x.x"
  exit 1
fi

VERSION=$1
DATE=$(date "+%Y-%m-%d %H:%M")

# Get last 5 commits (auto-read GitHub history)
COMMITS=$(git log -5 --pretty=format:"- %s")

# Generate "AI-style" summary (structured)
SUMMARY="Auto-generated summary:\n$COMMITS"

# Append to DNA.md
cat <<EOT >> DNA.md

---

### $VERSION [AUTO+AI]
- Timestamp: $DATE
- Source: iSH Mobile Deploy
- Location: iPhone (iSH) → GitHub → Docker → HF
- Execution: Manual Trigger → Automated CI/CD

#### 🧠 AI Summary
$SUMMARY

EOT

# Git flow
git add .
git commit -m "release: $VERSION (AI DNA log)"
git push origin main

# Tag
git tag $VERSION
git push origin $VERSION

echo "✅ AI Deploy Complete: $VERSION"
