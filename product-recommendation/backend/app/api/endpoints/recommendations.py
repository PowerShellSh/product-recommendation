from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.api import deps
from app.ml.recommender import RecommendationResult
from app.schemas.product import ProductInDB
from app.core.recommender import get_recommendation_engine
from app.crud import crud_product as crud

router = APIRouter()

@router.get("/{user_id}", response_model=List[ProductInDB])
async def get_recommendations(
    user_id: int,
    db: Session = Depends(deps.get_db),
    n_recommendations: int = 5
) -> List[ProductInDB]:
    try:
        engine = get_recommendation_engine()
        recommendations: List[RecommendationResult] = engine.get_recommendations(
            user_id=user_id,
            n_recommendations=n_recommendations
        )
        
        # 推薦された商品の詳細情報を取得
        products = []
        for rec in recommendations:
            product = crud.get(db, id=rec.product_id)
            if product:
                products.append(product)
        
        return products
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get recommendations: {str(e)}"
        ) 