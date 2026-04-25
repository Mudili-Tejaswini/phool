"""
tests/test_predictor.py
Unit tests for src/predictor.py
"""

import pytest
from unittest.mock import MagicMock, patch
import numpy as np

from src.predictor import PricePredictor


SAMPLE_INPUT = {
    "shape":  "Anarkali",
    "sleeve": "Long Sleeves",
    "hem":    "Curved",
    "neck":   "Round Neck",
    "length": "Ankle Length",
    "fabric": "Georgette",
    "slit":   "Side Slits",
    "sizes":  8,
}


@pytest.fixture
def mock_predictor(tmp_path):
    """Create a PricePredictor with a mocked model file."""
    import joblib

    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([880.0])

    model_path = tmp_path / "random_forest.pkl"
    joblib.dump(mock_model, model_path)

    return PricePredictor(model_path=str(model_path))


def test_predict_returns_dict(mock_predictor):
    result = mock_predictor.predict(SAMPLE_INPUT)
    assert isinstance(result, dict)


def test_predict_has_required_keys(mock_predictor):
    result = mock_predictor.predict(SAMPLE_INPUT)
    assert set(result.keys()) == {"price", "low", "high", "std", "premium"}


def test_predict_price_rounded_to_10(mock_predictor):
    result = mock_predictor.predict(SAMPLE_INPUT)
    assert result["price"] % 10 == 0


def test_predict_low_is_90_pct(mock_predictor):
    result = mock_predictor.predict(SAMPLE_INPUT)
    assert result["low"] == round(result["price"] * 0.9 / 10) * 10


def test_predict_high_is_110_pct(mock_predictor):
    result = mock_predictor.predict(SAMPLE_INPUT)
    assert result["high"] == round(result["price"] * 1.1 / 10) * 10


def test_predict_premium_is_130_pct(mock_predictor):
    result = mock_predictor.predict(SAMPLE_INPUT)
    assert result["premium"] == round(result["price"] * 1.3 / 10) * 10


def test_model_not_found_raises():
    with pytest.raises(FileNotFoundError):
        PricePredictor(model_path="nonexistent/model.pkl")


def test_round10():
    assert PricePredictor._round10(875.4) == 880
    assert PricePredictor._round10(874.9) == 870
    assert PricePredictor._round10(750.0) == 750
