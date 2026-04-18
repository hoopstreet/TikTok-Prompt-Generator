FROM hoopstreet/tiktok-prompt-generator:v1.2.3

WORKDIR /app

COPY . .

ENV PYTHONPATH="/app"
ENV HF_HUB_OFFLINE=1
ENV TRANSFORMERS_OFFLINE=1

EXPOSE 7860

CMD ["python", "app.py"]
