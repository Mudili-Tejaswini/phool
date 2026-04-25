# 🌸 Phool Intelligence — Floral Ethnic Dress Price Analytics

> Machine-learning price intelligence for the Indian ethnic fashion market, powered by Myntra data.

---

## Overview

Phool Intelligence is a data-driven pricing tool that helps boutique owners set competitive, profitable prices for floral ethnic dress collections. It scrapes listings from Myntra, extracts design attributes, trains regression models, and serves predictions through an interactive web dashboard.

**Key results:**
- ✅ 314 Myntra listings analyzed across 20 brands
- ✅ Random Forest model with MAE ±₹79
- ✅ Interactive price advisor with boutique markup tiers
- ✅ Real-time price prediction API
- ✅ End-to-end MLOps pipeline implemented

---

## Project Structure

```
phool/
├── .kiro/specs/               # Spec configs
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
├── app.py                     # Flask web app entry point
├── phool-intelligence.html    # Interactive dashboard
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
git clone https://github.com/Mudili-Tejaswini/phool.git
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

| Rank | Feature | Importance |
|---|---|---|
| 1 | Hemline style | 31.7% |
| 2 | Sleeve length | 18.5% |
| 3 | Is printed | 13.6% |
| 4 | Dress shape | 7.8% |
| 5 | Slit detail | 6.5% |

---

## 🧠 Key Learnings

- End-to-end ML pipeline development
- Web scraping with BeautifulSoup and Requests
- Model training & evaluation techniques
- Feature engineering for fashion retail data
- API development using Flask
- Building interactive dashboards with HTML & Chart.js
- Handling real-world dataset issues (missing values, outliers)
- Competitive pricing strategy using data insights

---

## ⭐ Future Improvements

- [ ] Deploy on cloud (AWS / Render)
- [ ] Improve model accuracy with XGBoost
- [ ] Expand dataset to 1,000+ listings with periodic re-scraping
- [ ] Add brand tier as an encoded feature
- [ ] Add image-based feature extraction using CNN
- [ ] Add authentication for API
- [ ] Add frontend UI with Streamlit
- [ ] Include discount percentage and MRP as additional signals

---

## 👩‍💻 Authors

**M. Tejaswini** — B.Tech CSE (AIML) &nbsp;|&nbsp; **I. Gayathri** — B.Tech CSE (AIML) &nbsp;|&nbsp; **A. Lahari** — B.Tech CSE (AIML) &nbsp;|&nbsp; **V. Rishitha** — B.Tech CSE (AIML)

---

## 🙏 Acknowledgments

- Data sourced from Myntra India
- Built with open-source tools and libraries
- Inspired by real-world pricing challenges in Indian ethnic fashion e-commerce

---

**Made with ❤️ for data-driven pricing decisions**

*If you found this helpful, give it a ⭐ on GitHub!*
