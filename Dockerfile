# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod 644 /app/src/google_credentials.json
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
ENV PYTHONUNBUFFERED=1
CMD ["python", "src/main.py"]