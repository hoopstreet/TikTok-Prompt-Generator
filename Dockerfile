FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y     libgl1-mesa-glx     libglib2.0-0     git     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HF_HOME=/tmp/hf_cache
ENV TRANSFORMERS_CACHE=/tmp/hf_cache

EXPOSE 7860

CMD ["python", "app.py"]
