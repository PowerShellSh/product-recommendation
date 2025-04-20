from typing import List, Dict, Optional
import numpy as np
from numpy.typing import NDArray
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel

class UserPreference(BaseModel):
    user_id: int
    product_id: int
    rating: float

class RecommendationResult(BaseModel):
    product_id: int
    score: float

class RecommendationEngine:
    def __init__(self) -> None:
        self.user_item_matrix: Optional[NDArray] = None
        self.item_similarity_matrix: Optional[NDArray] = None
        self.product_ids: Optional[List[int]] = None
        self.user_idx: Dict[int, int] = {}

    def train(self, preferences: List[UserPreference]) -> None:
        """購入履歴からモデルを学習"""
        if not preferences:
            raise ValueError("No training data provided")

        # ユーザー-アイテム行列の構築
        user_ids = sorted(set(pref.user_id for pref in preferences))
        product_ids = sorted(set(pref.product_id for pref in preferences))
        
        self.user_item_matrix = np.zeros((len(user_ids), len(product_ids)))
        self.product_ids = product_ids

        # 行列の作成
        user_idx = {uid: idx for idx, uid in enumerate(user_ids)}
        product_idx = {pid: idx for idx, pid in enumerate(product_ids)}
        
        for pref in preferences:
            self.user_item_matrix[user_idx[pref.user_id]][product_idx[pref.product_id]] = pref.rating

        # アイテム類似度行列の計算
        self.item_similarity_matrix = cosine_similarity(self.user_item_matrix.T)

        self.user_idx = user_idx

    def get_recommendations(
        self, user_id: int, n_recommendations: int = 5
    ) -> List[RecommendationResult]:
        """ユーザーへのおすすめ商品を取得"""
        if self.user_item_matrix is None or self.item_similarity_matrix is None:
            raise ValueError("Model not trained yet")

        # ユーザーのインデックスを取得
        user_idx = list(self.user_idx.keys()).index(user_id)
        
        # ユーザーの評価済み商品を取得
        user_ratings = self.user_item_matrix[user_idx]
        
        # 未評価商品のスコアを計算
        scores = []
        for product_idx, product_id in enumerate(self.product_ids):
            if user_ratings[product_idx] == 0:  # 未評価商品のみ
                score = np.sum(self.item_similarity_matrix[product_idx] * user_ratings)
                scores.append((product_id, score))
        
        # スコアの高い順にソート
        recommendations = sorted(scores, key=lambda x: x[1], reverse=True)[:n_recommendations]
        
        return [
            RecommendationResult(product_id=pid, score=score)
            for pid, score in recommendations
        ] 