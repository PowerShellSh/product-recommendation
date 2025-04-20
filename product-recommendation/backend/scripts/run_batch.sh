#!/bin/bash

echo "[Batch Script] Waiting for database and 'purchases' table..."

# docker-compose.yml 等で定義された環境変数を使用
# DB_HOST は 'db' (docker-compose のサービス名) を想定
until PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -c '\q' &> /dev/null && \
      PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -c '\d purchases' &> /dev/null
do
  echo "[Batch Script] Database connection or 'purchases' table not ready yet - sleeping 5s"
  sleep 5 # 5秒待機して再試行
done

echo "[Batch Script] Database and 'purchases' table are ready!"
echo "[Batch Script] Starting daily training loop..."

# 毎日午前3時に実行 (実際の時刻はコンテナ起動タイミングと sleep に依存)
while true; do
    echo "[Batch Script - $(date)] Running training script: python -m app.batch.train_recommender"
    poetry run python -m app.batch.train_recommender
    echo "[Batch Script - $(date)] Training script finished. Sleeping for 24 hours (86400s)..."
    sleep 86400  # 24時間待機
done