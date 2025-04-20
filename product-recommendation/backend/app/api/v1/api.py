# backend/app/api/v1/api.py
from fastapi import APIRouter

from app.api.v1.endpoints import recommendations
from app.api.v1.endpoints import products

api_router = APIRouter()

# 各エンドポイントルーターを組み込む
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])

# 他のエンドポイントもあれば同様に追加