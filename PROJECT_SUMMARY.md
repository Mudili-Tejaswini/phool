# Project Summary — Phool Intelligence

## Objective

Build a machine-learning price intelligence tool that helps boutique owners price floral ethnic dresses competitively against Myntra's catalog.

---

## Dataset

| Attribute | Value |
|---|---|
| Source | Myntra ethnic dress category |
| Total listings | 314 |
| Brands | 20 |
| Features used | 14 |
| Price range | ₹455 – ₹1,215 |
| Mean price | ₹759 |
| Median price | ₹750 |
| Floral pattern share | 94% |

**Design attributes collected:** dress shape, sleeve length, hemline style, neck style, dress length, fabric type, slit detail, pattern type, sizes available, rating, rating count.

---

## Methodology

1. **Scraping** — Requests + BeautifulSoup against Myntra search results and individual product pages.
2. **Preprocessing** — Price outlier removal, categorical standardization, deduplication.
3. **Feature engineering** — Label encoding of 7 categorical attributes + 3 binary flags.
4. **Modelling** — 80/20 train-test split across 4 algorithms.
5. **Evaluation** — MAE, RMSE, R² on hold-out test set.
6. **Deployment** — Flask API + standalone HTML dashboard.

---

## Model Results

| Model | MAE (₹) | RMSE (₹) | R² |
|---|---|---|---|
| Linear Regression | 104 | 129 | 0.322 |
| Ridge (α=10) | 102 | 126 | 0.353 |
| **Random Forest** | **79** | **123** | **0.383** |
| Gradient Boosting | 79 | 131 | 0.298 |

Random Forest was selected as the production model for its lowest MAE and highest R².

---

## Feature Importance (Random Forest)

| Rank | Feature | Importance |
|---|---|---|
| 1 | Hemline style | 31.7% |
| 2 | Sleeve length | 18.5% |
| 3 | Is printed | 13.6% |
| 4 | Dress shape | 7.8% |
| 5 | Slit detail | 6.5% |
| 6 | Neck style | 5.6% |
| 7 | Dress length | 5.4% |
| 8 | Is floral | 4.9% |
| 9 | Num sizes | 2.6% |
| 10 | Fabric | 1.9% |

---

## Key Business Insights

- **Anarkali** silhouette commands a 30% premium over A-Line (₹881 vs ₹679 avg).
- **Hemline** is the top price driver — Curved/Flared hemlines average ₹900+ vs ₹738 for Straight.
- **Long sleeves** carry a ₹245 premium over Sleeveless.
- **Georgette** is the highest-value fabric in the dataset (₹858 avg), outperforming Silk (₹644).
- Floral print is table-stakes (94% share) — silhouette is the true differentiator.
- Boutiques should price at benchmark +15% (standard) to +30% (bespoke/custom fit).

---

## Limitations

- Dataset size (314 listings) limits model complexity — R² of 0.38 leaves room for improvement.
- Prices reflect a single point-in-time scrape; Myntra applies dynamic discounts.
- Brand as a feature was excluded due to cardinality but is likely a strong signal.
- Model does not account for embroidery, embellishments, or print quality.

---

## Future Work

- Expand dataset to 1,000+ listings with periodic re-scraping.
- Add brand tier as an encoded feature.
- Incorporate discount percentage and MRP as additional signals.
- Deploy as a hosted web app (Render / Railway / Vercel + Python backend).
- Add image-based feature extraction using a CNN for print complexity scoring.
