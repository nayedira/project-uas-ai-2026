FROM python:3.11-slim

WORKDIR /app

# Copy backend requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/
COPY .env .

# Set environment
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=backend/Model/edusist_model_new
ENV USE_LOCAL_MODEL=true

EXPOSE 8000

CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]