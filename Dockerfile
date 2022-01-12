FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

RUN pip install poetry \
    && poetry config virtualenvs.create false

WORKDIR /app

COPY app ./
RUN poetry install --no-root --no-dev
