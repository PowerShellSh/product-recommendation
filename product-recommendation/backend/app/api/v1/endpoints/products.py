# backend/app/api/v1/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# SQLAlchemyモデル (DB操作用)
from app.models.product import Product as models_product
# Pydanticスキーマ (レスポンス定義用) - エイリアス 'schemas_product' を使用
from app.schemas.product import Product as schemas_product # このファイル/クラスが存在する必要あり
# DBセッション取得用の依存関係 (仮に recommendations.py と同じ場所からインポート)
# from app.api import deps # 本来は deps.py などに get_db を定義推奨
# --- 仮の get_db 定義 ---
from app.db.session import SessionLocal
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# --- 仮定義ここまで ---


router = APIRouter()

# ★★★ 修正: response_model を List[schemas_product] に変更 ★★★
@router.get("/", response_model=List[schemas_product], tags=["Products"])
async def read_products(
    skip: int = 0,   # ページネーション用: スキップする件数
    limit: int = 100, # ページネーション用: 取得する最大件数
    db: Session = Depends(get_db)
):
    """
    商品リストを取得する (ページネーション対応)
    """
    print(f"API Endpoint /products called (skip={skip}, limit={limit})") # ログ出力
    products = db.query(models_product).offset(skip).limit(limit).all()
    return products

# ★★★ 修正: response_model を schemas_product に変更 ★★★
@router.get("/{id}", response_model=schemas_product, tags=["Products"])
async def read_product(
    id: int, # パスパラメータ
    db: Session = Depends(get_db)
):
    """
    指定されたIDの商品詳細を取得する
    """
    print(f"API Endpoint /products/{id} called") # ログ出力
    db_product = db.query(models_product).filter(models_product.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product