#!/bin/bash

echo "========================================="
echo "FETCHING ALL GITHUB REPOSITORY DETAILS"
echo "========================================="

cd ~/TikTok-Prompt-Generator

# 1. Git log
echo ""
echo "--- GIT LOG (last 20 commits) ---"
git log --oneline -20

# 2. Branches
echo ""
echo "--- BRANCHES ---"
git branch -a

# 3. Tags
echo ""
echo "--- TAGS ---"
git tag -l

# 4. File sizes
echo ""
echo "--- FILE SIZES ---"
du -sh * .[^.]* 2>/dev/null | sort -hr | head -20

# 5. Python files line count
echo ""
echo "--- PYTHON FILES LINE COUNT ---"
wc -l *.py backend/*.py 2>/dev/null

# 6. TypeScript/JSX files
echo ""
echo "--- REACT FILES ---"
find frontend -name "*.tsx" -o -name "*.ts" -o -name "*.jsx" 2>/dev/null | xargs wc -l 2>/dev/null

# 7. Check what's in backend
echo ""
echo "--- BACKEND FILES ---"
ls -la backend/ 2>/dev/null

# 8. Check what's in frontend
echo ""
echo "--- FRONTEND FILES ---"
ls -la frontend/ 2>/dev/null
ls -la frontend/src/ 2>/dev/null

# 9. Environment variables needed
echo ""
echo "--- ENV VARS NEEDED ---"
grep -r "SUPABASE_URL\|SUPABASE_KEY\|HF_TOKEN" --include="*.py" --include="*.yml" --include="*.yaml" . 2>/dev/null | head -10

# 10. Latest commit details
echo ""
echo "--- LATEST COMMIT ---"
git log -1 --stat

echo ""
echo "========================================="
echo "✅ FETCH COMPLETE"
echo "========================================="
