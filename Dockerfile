FROM python:3.10
WORKDIR /app
COPY backend/ backend/
RUN pip install fastapi uvicorn
CMD ["uvicorn","backend.main:app","--host","0.0.0.0","--port","8000"]
