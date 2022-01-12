FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

ARG USERNAME=vscode
ARG UID=1000
ARG GID=1000

# ユーザー作成
RUN addgroup --gid $GID $USERNAME \
    && adduser --uid $UID --gid $GID --disabled-password $USERNAME

# ディレクトリのオーナーが$UID:$GIDになるよう先に作成しておく
RUN mkdir /var/lib/tfs && chown $UID:$GID /var/lib/tfs

# gitのインストール
RUN apt update && apt install -y \
    git \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry \
    && poetry config virtualenvs.create false

WORKDIR /app

COPY app/pyproject.toml* app/poetry.lock* ./
RUN poetry install --no-root
