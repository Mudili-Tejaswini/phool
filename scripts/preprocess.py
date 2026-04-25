"""
scripts/preprocess.py
Cleans and standardizes the raw scraped Myntra data.

Usage:
    python scripts/preprocess.py \
        --input  data/raw/myntra_raw.csv \
        --output data/processed/phool_processed.csv
"""

import argparse
import logging
import os

import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ── Valid category values (after standardization) ──
VALID_SHAPES  = {"Straight", "A-Line", "Anarkali"}
VALID_SLEEVES = {"Sleeveless", "Short Sleeves", "Three-Quarter Sleeves", "Long Sleeves"}
VALID_HEMS    = {"Straight", "Curved", "Flared", "High-Low", "Asymmetric"}
VALID_NECKS   = {"Round Neck", "V-Neck", "Mandarin Collar", "Band Collar", "Square Neck"}
VALID_LENGTHS = {"Above Knee", "Knee Length", "Calf Length", "Ankle Length"}
VALID_FABRICS = {"Cotton", "Silk", "Georgette"}


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    log.info(f"Loaded {len(df)} rows from {path}")
    return df


def clean_prices(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    before = len(df)
    df = df.dropna(subset=["price"])
    df = df[(df["price"] >= 200) & (df["price"] <= 5000)]
    log.info(f"Price filter: {before} → {len(df)} rows")
    return df


def standardize_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["dress_shape"]    = df["dress_shape"].str.strip().where(df["dress_shape"].isin(VALID_SHAPES), "Straight")
    df["sleeve_length"]  = df["sleeve_length"].str.strip().where(df["sleeve_length"].isin(VALID_SLEEVES), "Three-Quarter Sleeves")
    df["hemline"]        = df["hemline"].str.strip().where(df["hemline"].isin(VALID_HEMS), "Straight")
    df["neck_style"]     = df["neck_style"].str.strip().where(df["neck_style"].isin(VALID_NECKS), "Round Neck")
    df["dress_length"]   = df["dress_length"].str.strip().where(df["dress_length"].isin(VALID_LENGTHS), "Knee Length")
    df["fabric"]         = df["fabric"].str.strip().where(df["fabric"].isin(VALID_FABRICS), "Unknown")
    df["slit_detail"]    = df["slit_detail"].fillna("Unknown")
    df["pattern"]        = df["pattern"].fillna("Floral Print")

    return df


def extract_sizes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["sizes_available"] = df["sizes_available"].fillna("")
    df["num_sizes"] = df["sizes_available"].apply(
        lambda x: len(str(x).split(",")) if x else 4
    )
    df["num_sizes"] = df["num_sizes"].clip(1, 20)
    return df


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=["url"], keep="first")
    log.info(f"Dedup: {before} → {len(df)} rows")
    return df


def preprocess(input_path: str, output_path: str):
    df = load(input_path)
    df = deduplicate(df)
    df = clean_prices(df)
    df = standardize_categoricals(df)
    df = extract_sizes(df)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    log.info(f"Processed dataset saved → {output_path} ({len(df)} rows)")

    # Quick summary
    print("\n── Price Summary ──")
    print(df["price"].describe().round(0).to_string())
    print(f"\n── Dress Shape Distribution ──")
    print(df["dress_shape"].value_counts().to_string())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default="data/raw/myntra_raw.csv")
    parser.add_argument("--output", default="data/processed/phool_processed.csv")
    args = parser.parse_args()
    preprocess(args.input, args.output)
