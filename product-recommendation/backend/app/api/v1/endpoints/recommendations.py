# backend/app/api/v1/endpoints/recommendations.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import traceback

# 必要なモジュールや関数をインポート (実際のパスに合わせる)
from app import models
from app import schemas # schemas.Token が定義されている想定
# from app import deps # deps.get_db が定義されている想定
# from app.core.security import verify_password, create_access_token
from app.core.config import Settings

# DBモデルとPydanticスキーマ
from app.models.product import Product as models_product
# schemas.product が app/schemas/product.py に定義されている想定
from app.schemas.product import Product as schemas_product

# DBセッション取得 (main.py から移すか、共通の deps モジュールを推奨)
from app.db.session import SessionLocal
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ★★★ 推薦エンジンとローダー関数をインポート ★★★
# 本来 get_recommendation_engine は train_recommender.py ではなく、
# app.ml.engine や app.core など別の場所に定義するのが構造的に望ましいです。
try:
    from app.batch.train_recommender import get_recommendation_engine
    from app.ml.recommender import RecommendationEngine, RecommendationResult
except ImportError:
    # もしインポートエラーが出る場合、PYTHONPATHやモジュール構造を確認
    print("Error importing recommendation engine components.")
    # 代替としてダミー関数を定義するか、エラーを発生させる
    RecommendationEngine = None # type: ignore
    RecommendationResult = None # type: ignore
    def get_recommendation_engine(): raise ImportError("Cannot import recommendation engine")


router = APIRouter()

@router.get("/", response_model=List[schemas_product], tags=["Recommendations"])
async def read_recommendations(
    user_id: int = Query(..., description="推薦を取得したいユーザーのID (例: 1 から 8)"),
    # 取得する推薦数もパラメータ化 (デフォルト5件)
    n_recommendations: int = Query(5, ge=1, le=20, description="取得する推薦数"),
    db: Session = Depends(get_db) # DBセッション
):
    """
    指定されたユーザーへの商品推薦リストを取得する。
    学習済みモデルから推薦IDを取得し、DBから商品詳細を検索して返す。
    """
    print(f"API Endpoint /recommendations called for user_id={user_id}, n={n_recommendations}")

    if RecommendationEngine is None:
         raise HTTPException(status_code=500, detail="Recommendation engine module not loaded correctly")

    try:
        # 学習済み推薦エンジンを取得 (ファイルからロード)
        engine: RecommendationEngine = get_recommendation_engine()

        # モデルがロードされたが、訓練データがない場合 (初期状態など)
        if engine.user_item_matrix is None:
             print("Recommendation engine is not trained or loaded properly.")
             # エラーを返すか、空リストを返す (ここでは空リスト)
             return []

        # 指定された user_id がモデルの学習データに存在するかチェック
        if user_id not in engine.user_idx:
             print(f"User ID {user_id} not found in recommendation model's training data.")
             # ユーザーが見つからない場合の処理 (例: 人気商品を返す、空リストを返す、404エラー)
             # ここでは空リストを返す例
             return []
             # または raise HTTPException(status_code=404, detail=f"Recommendations not available for user ID {user_id}")

        # 推薦を取得 (product_id と score のリスト)
        recommended_results: List[RecommendationResult] = engine.get_recommendations(
            user_id=user_id, n_recommendations=n_recommendations
        )

        if not recommended_results:
            print(f"No recommendations generated for user ID {user_id}")
            return [] # 推薦がない場合は空リストを返す

        # 推薦結果から product_id のリストを抽出
        recommended_ids = [result.product_id for result in recommended_results]
        print(f"Recommended product IDs: {recommended_ids}")

        # DBから推薦された商品の詳細を取得
        # filter(models_product.Product.id.in_(recommended_ids)) を使用
        recommendations = db.query(models_product).filter(
            models_product.id.in_(recommended_ids)
        ).all()

        # 注意: DBからの取得順序は recommended_ids の順序（スコア順）とは限りません。
        # もし推薦スコア順に厳密に並べたい場合は、ここで再度ソートする必要があります。
        # 例: recommendation_map = {prod.id: prod for prod in recommendations}
        #     sorted_recommendations = [recommendation_map[pid] for pid in recommended_ids if pid in recommendation_map]
        #     return sorted_recommendations
        # 今回はDBから取得した順序で返します。

        print(f"Returning {len(recommendations)} product details.")
        # Pydantic スキーマ (schemas_product) のリストに自動変換されて返却される
        return recommendations

    except FileNotFoundError:
        print("Recommendation model file (`recommender.pkl`) not found.")
        # モデルファイルがない = バッチ処理がまだ実行されていないか失敗している
        # 空リストを返すか、人気商品を返す、あるいはエラーにするかを選択
        # ここでは空リストを返す例
        return []
        # または raise HTTPException(status_code=503, detail="Recommendation model not found. Please run the batch process.")
    except ValueError as e:
        # engine.get_recommendations 内で発生しうるエラー (例: 不正な user_id)
        print(f"Value error getting recommendations: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # その他の予期せぬエラー
        print(f"An unexpected error occurred in recommendations endpoint: {e}")
        # 詳細なエラーログは別に出力推奨
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error generating recommendations")
    
# @router.post("/api/v1/login/token", response_model=schemas.Token)
# def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
#     user = db.query(models.User).filter(models.User.username == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}