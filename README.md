# 📊 Customer Segmentation & Retention Analysis

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_URL)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.1-green)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0-red)

> A complete end-to-end data science project analysing 1M+ retail
> transactions to segment customers, predict churn, and recommend
> retention strategies — with an interactive Streamlit dashboard.

🔗 **[Live Dashboard →](# 📊 Customer Segmentation & Retention Analysis

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_URL)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.1-green)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0-red)

> A complete end-to-end data science project analysing 1M+ retail
> transactions to segment customers, predict churn, and recommend
> retention strategies — with an interactive Streamlit dashboard.

🔗 **[Live Dashboard →](# 📊 Customer Segmentation & Retention Analysis

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_URL)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.1-green)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0-red)

> A complete end-to-end data science project analysing 1M+ retail
> transactions to segment customers, predict churn, and recommend
> retention strategies — with an interactive Streamlit dashboard.

🔗 **[Live Dashboard →](https://customer-segmentation-ayywdyzc4cffdp9yzs4gym.streamlit.app/)**

---

## 📌 Project Overview

This project analyses the **Online Retail II dataset (UCI)**
containing 1,067,371 transactions from a UK-based online retailer
(2009–2011). Using ML and business analytics, it:

- Segments 3,921 customers into 7 groups using **RFM analysis + K-Means clustering**
- Predicts customer churn with **XGBoost (ROC-AUC: 0.87)**
- Identifies top churn drivers via **feature importance analysis**
- Recommends **data-driven retention strategies** per segment
- Visualises all findings in an **interactive Streamlit dashboard**

---

## 📈 Key Results

| Metric | Value |
|--------|-------|
| Dataset size | 1,067,371 transactions |
| Customers analysed | 3,921 UK customers |
| Date range | December 2009 — December 2011 |
| Total revenue analysed | £14.4M |
| Customer segments | 7 (RFM-based) |
| K-Means clusters | 6 (Silhouette score: 0.6031) |
| Churn model ROC-AUC | 0.8403 (XGBoost) |
| Top churn driver | Customer tenure |
| At-risk revenue | £1.4M |

---

## 🧪 Methodology

### Week 1 — Data Preparation
- Loaded 1,067,371 raw transactions across 2 years
- Cleaned: removed cancellations, returns, nulls → 779,425 clean rows
- Feature engineering: TotalPrice, time features, UK subset
- EDA: revenue trends, Pareto analysis, customer behavior

### Week 2 — Segmentation & ML
- **RFM Analysis**: scored 3,921 customers on Recency, Frequency, Monetary (1–5)
- **K-Means Clustering**: elbow method + silhouette score → K=6 optimal
- **Hierarchical Clustering**: confirmed K=6; K-Means selected (silhouette: 0.60 vs 0.61)
- **Churn Prediction**: 3 models compared → XGBoost wins (ROC-AUC: 0.84)

### Week 3 — Insights & Dashboard
- Retention strategies mapped per segment with priority and ROI
- Interactive Streamlit dashboard with 4 pages deployed to cloud

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.10 |
| Data | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Dashboard | Streamlit |
| Version Control | Git, GitHub |
| Environment | Jupyter Notebook, VS Code |

---

## 📁 Project Structure)**


