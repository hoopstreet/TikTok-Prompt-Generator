FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for GPU and Git
RUN apt-get update && apt-get install -y \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# FORCE INSTALL: PyTorch 2.5.1 (Extra stable for Flex Attention)
RUN pip install --no-cache-dir torch==2.5.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Install AI/Gradio stack
RUN pip install --no-cache-dir \
    gradio \
    transformers>=4.46.0 \
    pillow \
    einops \
    accelerate

COPY . .

# Set Path to ensure local imports work
ENV PYTHONPATH="/app"

EXPOSE 7860

CMD ["python", "hf_moondream.py"]
