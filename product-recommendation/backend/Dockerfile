FROM python:3.12-slim

WORKDIR /app

# Poetryのインストール
RUN pip install poetry

# 依存関係のファイルをコピー
COPY pyproject.toml poetry.lock ./

# 先に依存関係をインストール（--no-rootオプションを追加）
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# アプリケーションコードをコピー
COPY ./app ./app

# 初期化スクリプトを追加
COPY ./scripts/start.sh ./
RUN chmod +x ./start.sh

# ポートの公開
EXPOSE 8000

ENV PYTHONPATH=/app

# 起動スクリプトを実行
CMD ["./start.sh"] 