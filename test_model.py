"""
tests/test_model.py
Unit tests for src/model.py — evaluation logic.
"""

import pytest
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from src.model import evaluate_model, split_data, FEATURE_COLUMNS


@pytest.fixture
def dummy_df():
    np.random.seed(42)
    n = 100
    data = {col: np.random.randint(0, 4, n) for col in FEATURE_COLUMNS}
    data["price"] = np.random.randint(500, 1200, n).astype(float)
    return pd.DataFrame(data)


def test_split_data_sizes(dummy_df):
    X_train, X_test, y_train, y_test = split_data(dummy_df)
    assert len(X_train) == 80
    assert len(X_test) == 20


def test_evaluate_model_returns_dict(dummy_df):
    X_train, X_test, y_train, y_test = split_data(dummy_df)
    model = RandomForestRegressor(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    assert set(metrics.keys()) == {"MAE", "RMSE", "R2"}


def test_evaluate_model_mae_positive(dummy_df):
    X_train, X_test, y_train, y_test = split_data(dummy_df)
    model = RandomForestRegressor(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    assert metrics["MAE"] > 0


def test_evaluate_model_r2_range(dummy_df):
    X_train, X_test, y_train, y_test = split_data(dummy_df)
    model = RandomForestRegressor(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    assert -1 <= metrics["R2"] <= 1
