# This Dockerfile is used by Hugging Face Space
# It pulls the pre-built image from Docker Hub
FROM hoopstreet/tiktok-prompt-generator:latest

# Hugging Face Space will automatically run the CMD from the base image
# No additional configuration needed
