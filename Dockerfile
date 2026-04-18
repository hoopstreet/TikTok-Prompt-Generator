FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel

WORKDIR /app

# Crucial: Ensure the container uses the high-version torch
ENV PYTHONPATH="/app:${PYTHONPATH}"
ENV TORCH_CUDA_ARCH_LIST="7.5 8.0 8.6 8.9 9.0"

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY . .

# Force upgrade dependencies to match Moondream 3
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    gradio \
    transformers>=4.44.2 \
    pillow>=10.0.0 \
    einops \
    accelerate \
    sentencepiece

EXPOSE 7860

CMD ["python", "hf_moondream.py"]
