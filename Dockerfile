FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copier le code
COPY ./src /app/src
COPY ./templates /app/templates
COPY ./static /app/static
COPY main.py /app/main.py

# Port exposé
EXPOSE 8000

# Lancement en prod avec uvicorn
CMD ["uvicorn", "main:asgi_app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
