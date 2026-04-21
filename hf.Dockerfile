# Hugging Face Space Dockerfile
# Auto-updated by GitHub Actions
ARG TAG_VERSION=latest
FROM hoopstreet/tiktok-prompt-generator:${TAG_VERSION}
LABEL name="TikTok Prompt Generator"
LABEL version="${TAG_VERSION}"
EXPOSE 7860
CMD ["python", "app.py"]
