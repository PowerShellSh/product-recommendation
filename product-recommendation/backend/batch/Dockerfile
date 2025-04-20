FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

# postgresql-client をインストール (psql コマンド用)
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./app ./app

# バッチ実行用のスクリプト
COPY ./scripts/run_batch.sh ./
RUN chmod +x ./run_batch.sh

CMD ["./run_batch.sh"]