# Integration Summary

This document summarizes how the components of Phool Intelligence connect end-to-end.

---

## Data Pipeline

```
Myntra website
     │
     ▼
scripts/scrape.py          → data/raw/myntra_raw.csv
     │
     ▼
scripts/preprocess.py      → data/processed/phool_processed.csv
     │
     ▼
src/features.py            → feature matrix (14 columns)
     │
     ▼
src/model.py               → models/random_forest.pkl
     │
     ▼
src/predictor.py           → price dict { price, low, high, std, premium }
     │
     ▼
app.py  POST /api/predict  → JSON response to frontend
     │
     ▼
phool-intelligence.html    → rendered price recommendation
```

---

## Component Responsibilities

| Component | Responsibility |
|---|---|
| `scripts/scrape.py` | Fetches raw listing HTML from Myntra, extracts price + design attributes |
| `scripts/preprocess.py` | Cleans prices, standardizes categoricals, deduplicates |
| `src/features.py` | Label-encodes categoricals; produces model-ready DataFrame |
| `src/model.py` | Trains 4 models, evaluates, saves best as `.pkl` |
| `src/predictor.py` | Loads saved model; wraps prediction into API-friendly dict |
| `app.py` | Flask server; exposes `POST /api/predict` and `GET /api/health` |
| `phool-intelligence.html` | Self-contained dashboard; calls `/api/predict` on form submit |

---

## API Contract

### `POST /api/predict`

**Request body:**
```json
{
  "shape":  "Anarkali",
  "sleeve": "Long Sleeves",
  "hem":    "Curved",
  "neck":   "Round Neck",
  "length": "Ankle Length",
  "fabric": "Georgette",
  "slit":   "Side Slits",
  "sizes":  8
}
```

**Response:**
```json
{
  "price":   880,
  "low":     790,
  "high":    970,
  "std":     1010,
  "premium": 1140
}
```

### `GET /api/health`
```json
{ "status": "ok", "model": "random_forest" }
```

---

## Model Retraining

To retrain the model with fresh scraped data:

```bash
python scripts/scrape.py --pages 20 --output data/raw/myntra_raw.csv
python scripts/preprocess.py
python -m src.model
```

The new `models/random_forest.pkl` will be picked up automatically on the next app restart.

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `PORT` | `5000` | Flask server port |
| `FLASK_DEBUG` | `false` | Enable debug mode |
