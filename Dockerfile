FROM python:3.10-slim

# Install system dependencies for VIPS and typical build tools
RUN apt-get update && apt-get install -y \
    libvips-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip first for better dependency resolution
RUN pip install --no-cache-dir --upgrade pip

# Moondream 3 needs these specific libraries to handle the MoE architecture
RUN pip install --no-cache-dir \
    torch \
    transformers \
    accelerate \
    huggingface_hub \
    einops \
    tokenizers \
    pillow \
    numpy \
    pyvips

# Copy your local repository files into the container
COPY . .

# Set the entry point
CMD ["python", "hf_moondream.py"]
