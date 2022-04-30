FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

ARG USERNAME=vscode
ARG UID=1000
ARG GID=1000

# ユーザー作成
RUN addgroup --gid $GID $USERNAME \
    && adduser --uid $UID --gid $GID --disabled-password $USERNAME

# ディレクトリへ書き込めるようパーミッションを変更しておく
RUN mkdir /var/lib/tfs && chmod a+w /var/lib/tfs

# gitのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml* poetry.lock* ./
RUN poetry install --no-root
