#!/bin/sh

echo "nameserver 8.8.8.8" > /etc/resolv.conf
cd ~/TikTok-Prompt-Generator

# Check version argument
if [ -z "$1" ]; then
  echo "Usage: ./deploy.sh v1.x.x"
  exit 1
fi

VERSION=$1
DATE=$(date "+%Y-%m-%d %H:%M")

# Append to DNA.md (no overwrite)
cat <<EOT >> DNA.md

## $VERSION: [AUTO] Mobile Release
- Timestamp: $DATE
- Source: iSH Mobile Deploy
- Notes:
  - Auto-commit from mobile
  - Synced with GitHub Actions
  - Triggered Docker + HF pipeline

EOT

# Git flow
git add .
git commit -m "release: $VERSION (auto DNA update)"
git push origin main

# Tag + push
git tag $VERSION
git push origin $VERSION

echo "✅ Deployed $VERSION successfully"
