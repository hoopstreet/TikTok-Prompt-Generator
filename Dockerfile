FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /lib/apt/lists/*

# Copy all files (including weights) into the image
COPY . .

# Install Python requirements
RUN pip install --no-cache-dir gradio transformers pillow

# Export port for Gradio
EXPOSE 7860

CMD ["python", "hf_moondream.py"]
