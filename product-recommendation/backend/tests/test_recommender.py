import pytest
from typing import List
import numpy as np
from numpy.testing import assert_array_almost_equal

from app.ml.recommender import RecommendationEngine, UserPreference, RecommendationResult

@pytest.fixture
def sample_preferences() -> List[UserPreference]:
    return [
        UserPreference(user_id=1, product_id=1, rating=5.0),
        UserPreference(user_id=1, product_id=2, rating=3.0),
        UserPreference(user_id=2, product_id=1, rating=4.0),
    ]

def test_recommendation_engine_training(sample_preferences: List[UserPreference]) -> None:
    engine = RecommendationEngine()
    engine.train(sample_preferences)
    
    assert engine.user_item_matrix is not None
    assert engine.item_similarity_matrix is not None
    assert engine.product_ids is not None
    
    expected_shape = (2, 2)  # 2 users x 2 products
    assert engine.user_item_matrix.shape == expected_shape

def test_get_recommendations(sample_preferences: List[UserPreference]) -> None:
    engine = RecommendationEngine()
    engine.train(sample_preferences)
    
    recommendations = engine.get_recommendations(user_id=1, n_recommendations=2)
    
    assert len(recommendations) <= 2
    assert all(isinstance(rec, RecommendationResult) for rec in recommendations) 