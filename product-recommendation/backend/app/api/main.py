# app/api/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from typing import List

# --- 設定 ---
# from app.core.config import settings # 必要に応じて実際のconfigをインポート
class Settings: # 仮の設定クラス (現状維持)
    PROJECT_NAME: str = "商品推薦システム API"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

settings = Settings() # 仮の設定インスタンス

# --- APIルーター ---
# ★★★ 修正: app.api.v1.api から中央ルーターをインポート ★★★
from app.api.v1.api import api_router  # このファイルが存在し、中でAPIRouterが定義されている必要あり

# --- データベースセッション ---
# from app.api import deps # 本来は deps.py などに get_db を定義推奨
from app.db.session import SessionLocal
def get_db(): # 仮の get_db (現状維持)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- FastAPIアプリケーションインスタンス作成 ---
# ★★★ 修正: app定義を include_router より前に移動 ★★★
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" # OpenAPIスキーマのURL
)

# --- CORSミドルウェア設定 ---
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# --- APIルーターの組み込み ---
# ★★★ 修正: インポートした中央の api_router を使用 ★★★
# /api/v1 プレフィックスをつけて中央APIルーターをアプリケーションに含める
app.include_router(api_router, prefix=settings.API_V1_STR)

# --- ルートエンドポイント ---
@app.get("/", tags=["Root"])
async def read_root():
    """
    ルートエンドポイント。アプリケーションの基本的な情報を返す。
    """
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

# --- ヘルスチェックエンドポイント (DB接続確認含む) ---
@app.get("/health", tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """
    基本的なヘルスチェックを実行する。データベース接続も確認する。
    """
    try:
        # 簡単なクエリを実行してDB接続を確認
        # SQLAlchemy 2.0 スタイル: db.execute(text("SELECT 1"))
        # 古いスタイル: db.execute("SELECT 1")
        from sqlalchemy import text # text をインポート
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        print(f"Database connection error: {e}") # エラーログ
        db_status = "error"
    return {"status": "ok", "database": db_status}

# 備考: データベースの初期化 (init_db) は、通常このファイル内ではなく、
#       uvicorn/gunicorn を起動する前の pre_start.py や起動スクリプト (start.sh)
#       から呼び出す方が、特に初期データ投入の場合は安全です。
#       FastAPIの startup イベントで実行することも可能ですが、
#       複数ワーカー起動時や冪等性の問題に注意が必要です。