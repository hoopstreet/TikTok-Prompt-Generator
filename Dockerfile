FROM python:3.11-slim

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# copy project
COPY . .

# install deps
RUN pip install --no-cache-dir -r requirements.txt

# HF SAFE ENV
ENV HF_HUB_OFFLINE=1
ENV TRANSFORMERS_OFFLINE=1
ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["python", "app.py"]
