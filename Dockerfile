FROM python:3.14.6-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

COPY . .

CMD ["gunicorn", "server:app", "--config", "gunicorn_config.py", "-k", "uvicorn.workers.UvicornWorker"]
