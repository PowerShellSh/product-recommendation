from app.ml.recommender import RecommendationEngine
from app.db.session import SessionLocal
from app.models.purchase import Purchase
from app.ml.recommender import UserPreference
import pickle
import os

def train_and_save_model():
    engine = RecommendationEngine()
    
    # DBから購入履歴を取得して学習
    db = SessionLocal()
    try:
        purchases = db.query(Purchase).all()
        preferences = [
            UserPreference(
                user_id=p.user_id,
                product_id=p.product_id,
                rating=p.rating
            )
            for p in purchases
        ]
        engine.train(preferences)
        
        # モデルを保存
        model_path = os.getenv('MODEL_PATH', '/app/models/recommender.pkl')
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        with open(model_path, 'wb') as f:
            pickle.dump(engine, f)
            
    finally:
        db.close()

if __name__ == "__main__":
    train_and_save_model()

_engine = None

def get_recommendation_engine() -> RecommendationEngine:
    global _engine
    if _engine is None:
        model_path = os.getenv('MODEL_PATH', '/app/models/recommender.pkl')
        try:
            with open(model_path, 'rb') as f:
                _engine = pickle.load(f)
        except FileNotFoundError:
            # モデルが存在しない場合は空のエンジンを返す
            _engine = RecommendationEngine()
    return _engine 