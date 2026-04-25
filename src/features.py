"""
src/features.py
Feature engineering for the Phool price prediction model.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


# ── Categorical encodings (label-encoded based on training data) ──
SHAPE_MAP = {"A-Line": 0, "Straight": 1, "Anarkali": 2}
SLEEVE_MAP = {"Sleeveless": 0, "Three-Quarter Sleeves": 1, "Short Sleeves": 2, "Long Sleeves": 3}
HEM_MAP = {"High-Low": 0, "Straight": 1, "Flared": 2, "Asymmetric": 3, "Curved": 4}
NECK_MAP = {
    "Band Collar": 0, "Round Neck": 1, "Mandarin Collar": 2,
    "V-Neck": 3, "Square Neck": 4,
}
LENGTH_MAP = {"Above Knee": 0, "Knee Length": 1, "Calf Length": 2, "Ankle Length": 3}
FABRIC_MAP = {"Silk": 0, "Unknown": 1, "Cotton": 2, "Georgette": 3}
SLIT_MAP = {"Side Slits": 0, "Unknown": 1, "Multiple Slits": 2, "Front Slit": 3}

FEATURE_COLUMNS = [
    "shape_enc",
    "sleeve_enc",
    "hem_enc",
    "neck_enc",
    "length_enc",
    "fabric_enc",
    "slit_enc",
    "num_sizes",
    "is_floral",
    "is_printed",
]


def encode_input(raw: Dict[str, Any]) -> pd.DataFrame:
    """
    Convert a raw input dict from the API into a feature DataFrame
    ready for model inference.

    Parameters
    ----------
    raw : dict
        Keys: shape, sleeve, hem, neck, length, fabric, slit, sizes

    Returns
    -------
    pd.DataFrame with one row and columns matching FEATURE_COLUMNS
    """
    row = {
        "shape_enc":  SHAPE_MAP.get(raw.get("shape", "Straight"), 1),
        "sleeve_enc": SLEEVE_MAP.get(raw.get("sleeve", "Three-Quarter Sleeves"), 1),
        "hem_enc":    HEM_MAP.get(raw.get("hem", "Straight"), 1),
        "neck_enc":   NECK_MAP.get(raw.get("neck", "Round Neck"), 1),
        "length_enc": LENGTH_MAP.get(raw.get("length", "Knee Length"), 1),
        "fabric_enc": FABRIC_MAP.get(raw.get("fabric", "Cotton"), 2),
        "slit_enc":   SLIT_MAP.get(raw.get("slit", "Unknown"), 1),
        "num_sizes":  int(raw.get("sizes", 6)),
        "is_floral":  1,   # dataset is 94% floral; assumed 1 for this tool
        "is_printed": 1,
    }
    return pd.DataFrame([row], columns=FEATURE_COLUMNS)


def engineer_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full feature engineering pipeline for training data.
    Applies all encodings and creates derived columns.

    Parameters
    ----------
    df : pd.DataFrame — raw scraped + cleaned dataset

    Returns
    -------
    pd.DataFrame with model-ready features
    """
    out = df.copy()

    out["shape_enc"]  = out["dress_shape"].map(SHAPE_MAP).fillna(1).astype(int)
    out["sleeve_enc"] = out["sleeve_length"].map(SLEEVE_MAP).fillna(1).astype(int)
    out["hem_enc"]    = out["hemline"].map(HEM_MAP).fillna(1).astype(int)
    out["neck_enc"]   = out["neck_style"].map(NECK_MAP).fillna(1).astype(int)
    out["length_enc"] = out["dress_length"].map(LENGTH_MAP).fillna(1).astype(int)
    out["fabric_enc"] = out["fabric"].map(FABRIC_MAP).fillna(1).astype(int)
    out["slit_enc"]   = out["slit_detail"].map(SLIT_MAP).fillna(1).astype(int)

    out["num_sizes"]  = out["sizes_available"].apply(lambda x: len(x) if isinstance(x, list) else int(x))
    out["is_floral"]  = out["pattern"].str.lower().str.contains("floral").astype(int)
    out["is_printed"] = out["pattern"].str.lower().str.contains("print").astype(int)

    return out[FEATURE_COLUMNS + ["price"]]
