FROM python:3.9-slim

WORKDIR /app

# Install dependencies if you have a requirements.txt
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Adjust this to your actual starting script
CMD ["python", "hf_moondream.py"]
