FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY space.yaml . 2>/dev/null || true

# Expose port
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
