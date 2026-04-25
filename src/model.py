"""
src/model.py
Model training, evaluation, and persistence for Phool price prediction.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Tuple

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.features import engineer_dataframe, FEATURE_COLUMNS


MODELS = {
    "linear_regression": LinearRegression(),
    "ridge":             Ridge(alpha=10),
    "random_forest":     RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1),
    "gradient_boosting": GradientBoostingRegressor(n_estimators=200, random_state=42),
}

MODEL_DIR = "models"


def load_data(path: str = "data/processed/phool_processed.csv") -> pd.DataFrame:
    """Load the processed dataset."""
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows from {path}")
    return df


def split_data(
    df: pd.DataFrame,
    target: str = "price",
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple:
    X = df[FEATURE_COLUMNS]
    y = df[target]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
    """Return MAE, RMSE, and R² for a fitted model."""
    preds = model.predict(X_test)
    mae   = mean_absolute_error(y_test, preds)
    rmse  = np.sqrt(mean_squared_error(y_test, preds))
    r2    = r2_score(y_test, preds)
    return {"MAE": round(mae, 1), "RMSE": round(rmse, 1), "R2": round(r2, 3)}


def train_all(data_path: str = "data/processed/phool_processed.csv") -> Dict:
    """
    Train all candidate models, print a comparison table,
    save the best model to disk, and return all metrics.
    """
    df = load_data(data_path)
    df = engineer_dataframe(df)

    X_train, X_test, y_train, y_test = split_data(df)
    print(f"Train: {len(X_train)} | Test: {len(X_test)}\n")

    results = {}
    best_model = None
    best_mae = float("inf")

    for name, model in MODELS.items():
        model.fit(X_train, y_train)
        metrics = evaluate_model(model, X_test, y_test)
        results[name] = {"model": model, **metrics}
        print(f"{name:25s}  MAE={metrics['MAE']:6.1f}  RMSE={metrics['RMSE']:6.1f}  R²={metrics['R2']:.3f}")

        if metrics["MAE"] < best_mae:
            best_mae = metrics["MAE"]
            best_model = (name, model)

    # Save best model
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, f"{best_model[0]}.pkl")
    joblib.dump(best_model[1], model_path)
    print(f"\n✅ Best model: {best_model[0]} (MAE=₹{best_mae:.0f}) → saved to {model_path}")

    # Feature importance (Random Forest)
    rf = results["random_forest"]["model"]
    importances = pd.Series(rf.feature_importances_, index=FEATURE_COLUMNS).sort_values(ascending=False)
    print("\nFeature Importances:")
    for feat, imp in importances.items():
        bar = "█" * int(imp * 40)
        print(f"  {feat:20s} {imp:.3f}  {bar}")

    return results


if __name__ == "__main__":
    train_all()
