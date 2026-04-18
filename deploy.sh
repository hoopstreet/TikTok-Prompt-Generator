#!/bin/sh
# Usage: ./deploy.sh v1.0.2
VERSION=$1
if [ -z "$VERSION" ]; then
  echo "Usage: ./deploy.sh v1.x.x"
  exit 1
fi

echo "nameserver 8.8.8.8" > /etc/resolv.conf
sed -i "s|hoopstreet/tiktok-prompt-generator:v.*|hoopstreet/tiktok-prompt-generator:$VERSION|g" Dockerfile.hf

git add .
git commit -m "release: $VERSION"
git push origin main
git tag $VERSION
git push origin $VERSION

echo "Successfully deployed $VERSION to GitHub & Docker Hub!"
