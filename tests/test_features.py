"""
tests/test_features.py
Unit tests for src/features.py
"""

import pytest
import pandas as pd
from src.features import encode_input, FEATURE_COLUMNS


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


def test_encode_input_returns_dataframe():
    result = encode_input(SAMPLE_INPUT)
    assert isinstance(result, pd.DataFrame)


def test_encode_input_has_correct_columns():
    result = encode_input(SAMPLE_INPUT)
    assert list(result.columns) == FEATURE_COLUMNS


def test_encode_input_single_row():
    result = encode_input(SAMPLE_INPUT)
    assert len(result) == 1


def test_encode_input_anarkali_shape():
    result = encode_input(SAMPLE_INPUT)
    # Anarkali → 2 in SHAPE_MAP
    assert result["shape_enc"].iloc[0] == 2


def test_encode_input_long_sleeve():
    result = encode_input(SAMPLE_INPUT)
    # Long Sleeves → 3 in SLEEVE_MAP
    assert result["sleeve_enc"].iloc[0] == 3


def test_encode_input_curved_hem():
    result = encode_input(SAMPLE_INPUT)
    # Curved → 4 in HEM_MAP
    assert result["hem_enc"].iloc[0] == 4


def test_encode_input_num_sizes():
    result = encode_input(SAMPLE_INPUT)
    assert result["num_sizes"].iloc[0] == 8


def test_encode_input_unknown_shape_defaults():
    inp = {**SAMPLE_INPUT, "shape": "NonExistent"}
    result = encode_input(inp)
    # Should fallback to default without raising
    assert result["shape_enc"].iloc[0] is not None


def test_encode_input_is_floral_always_1():
    result = encode_input(SAMPLE_INPUT)
    assert result["is_floral"].iloc[0] == 1


def test_encode_input_missing_optional_keys():
    minimal = {"shape": "Straight", "sizes": 4}
    result = encode_input(minimal)
    assert list(result.columns) == FEATURE_COLUMNS
