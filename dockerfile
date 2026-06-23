FROM python:3.11-slim

WORKDIR /app

# Copy requirements dari backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file backend
COPY backend/ ./backend/

# Set environment variables (tanpa .env file)
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=backend/Model/edusist_model_new
ENV USE_LOCAL_MODEL=true

EXPOSE 8000

CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]