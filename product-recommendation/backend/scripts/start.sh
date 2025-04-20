#!/bin/bash

# DBの初期化を実行
poetry run python -c "from app.db.init_db import init_db; from app.db.session import SessionLocal; init_db(SessionLocal())"

# アプリケーションを起動
poetry run uvicorn app.api.main:app --host 0.0.0.0 --port 8000 