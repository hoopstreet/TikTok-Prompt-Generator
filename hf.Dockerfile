# Hugging Face Space Dockerfile
# This file is automatically updated by GitHub Actions
# It pulls the pre-built image from Docker Hub

FROM hoopstreet/tiktok-prompt-generator:latest

# Hugging Face Space metadata
LABEL name="TikTok Prompt Generator"
LABEL version="latest"
LABEL description="AI-Powered TikTok Affiliate Content Generator"

# Expose the port
EXPOSE 7860

# The app.py is already inside the Docker Hub image
# No additional files needed - everything comes from the base image

CMD ["python", "app.py"]
