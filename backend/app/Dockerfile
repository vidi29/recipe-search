FROM python:3.11-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r app/requirements.txt
COPY app /app
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
