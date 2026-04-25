# 🌸 Phool Intelligence — Floral Ethnic Dress Price Analytics

> Machine-learning price intelligence for the Indian ethnic fashion market, powered by Myntra data.

---

## Overview

Phool Intelligence is a data-driven pricing tool that helps boutique owners set competitive, profitable prices for floral ethnic dress collections. It scrapes listings from Myntra, extracts design attributes, trains regression models, and serves predictions through an interactive web dashboard.

**Key results:**
- 314 Myntra listings analyzed across 20 brands
- Random Forest model with MAE ±₹79
- Interactive price advisor with boutique markup tiers

---

## Project Structure

```
phool/
├── .kiro/specs/               # Bluetooth/spec configs
├── assets/                    # Static assets (images, icons)
├── data/
│   ├── raw/                   # Raw scraped data
│   └── processed/             # Cleaned, feature-engineered data
├── models/                    # Saved trained model files (.pkl)
├── notebooks/
│   ├── 01_eda.ipynb           # Exploratory data analysis
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
├── scripts/
│   ├── scrape.py              # Myntra scraper
│   └── preprocess.py          # Data cleaning pipeline
├── src/
│   ├── features.py            # Feature engineering logic
│   ├── model.py               # Model training & evaluation
│   └── predictor.py           # Inference / prediction logic
├── tests/
│   ├── test_features.py
│   ├── test_model.py
│   └── test_predictor.py
├── app.py                     # Flask/Streamlit web app entry point
├── requirements.txt           # Python dependencies
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── INTEGRATION_SUMMARY.md
└── PROJECT_SUMMARY.md
```

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/your-username/phool.git
cd phool
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the web app

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Notebooks

| Notebook | Description |
|---|---|
| `01_eda.ipynb` | Price distributions, neck/sleeve/hemline breakdowns |
| `02_feature_engineering.ipynb` | Encoding categorical variables, feature selection |
| `03_model_training.ipynb` | Training Linear, Ridge, Random Forest, Gradient Boosting |

Run notebooks with:
```bash
jupyter notebook notebooks/
```

---

## Model Performance

| Model | MAE (₹) | RMSE (₹) | R² |
|---|---|---|---|
| Linear Regression | 104 | 129 | 0.322 |
| Ridge (α=10) | 102 | 126 | 0.353 |
| **Random Forest** | **79** | **123** | **0.383** |
| Gradient Boosting | 79 | 131 | 0.298 |

**Winner: Random Forest** — lowest MAE and best generalization.

---

## Top Price Drivers (Feature Importance)

| Feature | Importance |
|---|---|
| Hemline style | 31.7% |
| Sleeve length | 18.5% |
| Is printed | 13.6% |
| Dress shape | 7.8% |
| Slit detail | 6.5% |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
