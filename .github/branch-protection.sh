#!/bin/bash

# Script to set up branch protection rules via GitHub API

BRANCHES="main stable-v3"

for BRANCH in $BRANCHES; do
  echo "Setting up protection for $BRANCH branch..."
  
  curl -X PUT \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/repos/hoopstreet/TikTok-Prompt-Generator/branches/$BRANCH/protection \
    -d '{
      "required_status_checks": {
        "strict": true,
        "contexts": ["CI/CD Pipeline"]
      },
      "enforce_admins": true,
      "required_pull_request_reviews": {
        "required_approving_review_count": 1,
        "dismiss_stale_reviews": true
      },
      "restrictions": null
    }'
done

echo "✅ Branch protection rules applied"
