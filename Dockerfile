FROM hoopstreet/tiktok-prompt-generator:$NEW_TAG

# Hugging Face requirement
EXPOSE 7860
RUN mkdir -p /app/.cache && chmod -R 777 /app
