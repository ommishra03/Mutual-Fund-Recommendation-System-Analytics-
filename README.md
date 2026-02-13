# 📊 Mutual Fund Recommendation System & Analytics

> An end-to-end **Mutual Fund Analytics, Machine Learning & Business Intelligence** project that simulates how real fintech and asset-management analytics pipelines are built — from raw data to ML-based fund recommendations and executive dashboards.

🌐 **Live Application:**  
👉 https://mutual-fund-analysis-om.streamlit.app/

---

# 🚀 Project Overview

This repository demonstrates how investment recommendation systems evolve from **basic analytics → statistical modeling → machine learning ranking**.

The project integrates:

- 🐍 Python (Data Analytics + ML)
- 📑 Excel (Data Cleaning & Validation Layer)
- 📊 Power BI (Business Dashboards)
- 🌐 Streamlit (Interactive Web App)

The goal is to recommend mutual funds using **risk-adjusted performance metrics** and intelligent scoring models — similar to workflows used in fintech analytics teams.

---

# 🎯 Project Objective

Build a data-driven system to evaluate and recommend mutual funds based on:

- Risk profile
- Return expectations
- Historical performance
- Volatility & risk-adjusted metrics
- Composite statistical scoring
- Machine learning ranking

---

# 🧠 Recommendation System Approaches

## 1️⃣ Baseline Recommendation (Rule-Based)
- Uses filtering logic based on returns and volatility
- Acts as a benchmark model
- Highly interpretable

📄 `Python/mutual_fund_baseline.ipynb`

---

## 2️⃣ Z-Score Statistical Model
- Standardizes financial metrics
- Enables fair comparison across funds
- Produces composite scores

📄 `Python/mutual_fund_zscore.ipynb`

---

## 3️⃣ Machine Learning Ranking (XGBoost)
- Gradient boosting model for ranking funds
- Captures nonlinear relationships between features
- Mimics production fintech recommendation engines

📄 `Python/mutual_fund-XGboost.ipynb`  
📦 Model File: `Python/xgboost_fund_ranker.pkl`

---

# 🌐 Live Streamlit Application

The deployed app demonstrates the full recommendation workflow in an interactive format.

🔗 https://mutual-fund-analysis-om.streamlit.app/

### Features
- Interactive fund analysis
- Risk vs Return visualization
- ML-based scoring demonstration
- Business-friendly analytics interface

---

# 📁 Repository Structure

```
MUTUAL_FUND_ANALYSIS/
│
├── Excel/
│ ├── mutual_funds_original.xlsx
│ ├── mutual_funds.xlsx
│ └── mutual_funds_cleaned.xlsx
│
├── PowerBI/
│ └── mutual_fund_dashboard.pbix
│
├── Python/
│ ├── app.py
│ ├── Mutual Fund Analysis.ipynb
│ ├── mutual_fund_baseline.ipynb
│ ├── mutual_fund_final.ipynb
│ ├── mutual_fund_zscore.ipynb
│ ├── mutual_fund-XGboost.ipynb
│ └── xgboost_fund_ranker.pkl
│
├── Category & AMC Benchmarking.png
├── Fund Performance Overview.png
├── Risk vs Return.png
├── requirements.txt
├── License
├── .gitignore
└── README.md
```

---

# 🛠 Tools & Technologies

## Analytics & Machine Learning
- Python
- Pandas, NumPy
- Scikit-learn
- XGBoost
- Statistical Normalization (Z-Score)

## Business Intelligence
- Power BI
- KPI Design
- Investment Analytics Visualization

## Data Layer
- Microsoft Excel
- Data Validation & Cleaning

## Deployment
- Streamlit
- GitHub Version Control

---

# 📊 Key Metrics Used

- Absolute Returns
- CAGR
- Volatility / Standard Deviation
- Risk-Adjusted Scores
- Composite Z-Score Ranking
- Machine Learning Fund Score

---

# 📈 Dashboards & Business Insights

The Power BI dashboard converts model outputs into business insights:

- Category-wise fund comparison
- Risk vs Return positioning
- AMC benchmarking
- Performance trend analysis
- Executive-level KPI storytelling

📊 `PowerBI/mutual_fund_dashboard.pbix`

---

# 🔄 End-to-End Analytics Pipeline

```
Excel (Data Layer)
↓
Python Analytics & Feature Engineering
↓
Z-Score Statistical Model
↓
XGBoost Machine Learning Ranking
↓
Streamlit Web App + Power BI Dashboard
```

---

# 💼 Business Value

This project reflects real analytics work done in:

- Fintech investment platforms
- Asset management firms
- Wealth advisory analytics teams
- Data-driven investment research

It demonstrates:

✅ Explainable recommendation systems  
✅ ML integration into business analytics  
✅ Risk-return financial modeling  
✅ Storytelling through dashboards  

---

# ▶️ How to Run Locally

## 1. Clone Repository
```bash
git clone <https://github.com/ommishra03/Mutual-Fund-Recommendation-System-Analytics->
cd MUTUAL_FUND_ANALYSIS
```
## 2️. Install Requirements
``` bash
pip install -r requirements.txt
```
## 3️. Run Streamlit App
```bash
streamlit run Python/app.py
```
---

# 👤 Author

Om Mishra

Data Analytics | Machine Learning | Fintech Analytics

🔗 LinkedIn: https://www.linkedin.com/in/om-mishra-a62991289

---

# 📜 License

This project is licensed under the MIT License.
---

# ⭐ Final Note

This is a portfolio-grade analytics + ML project designed to mirror how senior BI analysts and fintech data teams structure recommendation engines — combining:

```
> Statistical modeling
> Machine learning ranking
> Financial analytics
> Business storytelling
```

Ideal for roles in:

Data Analytics • Business Analytics • Fintech ML • BI Engineering
