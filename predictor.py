"""
src/predictor.py
Inference wrapper — loads a saved model and returns price predictions.
"""

import os
import joblib
import numpy as np
from typing import Dict, Any

from src.features import encode_input


class PricePredictor:
    """
    Loads a saved sklearn model and exposes a predict() method
    that accepts raw API input and returns a priced result dict.
    """

    def __init__(self, model_path: str = "models/random_forest.pkl"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found at '{model_path}'. "
                "Run `python -m src.model` to train and save a model first."
            )
        self.model = joblib.load(model_path)
        self.model_name = os.path.splitext(os.path.basename(model_path))[0]

    def predict(self, raw: Dict[str, Any]) -> Dict[str, int]:
        """
        Predict the Myntra benchmark price for a dress.

        Parameters
        ----------
        raw : dict — raw input from API (see app.py for schema)

        Returns
        -------
        dict with keys: price, low, high, std, premium
        """
        X = encode_input(raw)
        raw_price = float(self.model.predict(X)[0])

        price   = self._round10(raw_price)
        low     = self._round10(price * 0.90)
        high    = self._round10(price * 1.10)
        std     = self._round10(price * 1.15)
        premium = self._round10(price * 1.30)

        return {
            "price":   price,
            "low":     low,
            "high":    high,
            "std":     std,
            "premium": premium,
        }

    @staticmethod
    def _round10(value: float) -> int:
        """Round to the nearest ₹10."""
        return int(round(value / 10) * 10)
