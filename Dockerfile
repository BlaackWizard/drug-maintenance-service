FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update -y && \
    apt install -y --no-install-recommends \
    python3-dev \
    gcc \
    musl-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

COPY . /app/
