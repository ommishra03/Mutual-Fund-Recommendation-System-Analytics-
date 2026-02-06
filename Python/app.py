import pandas as pd
import numpy as np
import streamlit as st
from scipy.stats import zscore
import plotly.express as px

# =========================================================
# Page Configuration
# =========================================================
st.set_page_config(
    page_title="Mutual Fund Recommendation System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# Header
# =========================================================
st.markdown(
    """
    <h1 style='text-align:center;'>Mutual Fund Recommendation System</h1>
    <p style='text-align:center; color:grey;'>
    Risk-aligned mutual fund recommendations using quantitative analysis
    </p>
    """,
    unsafe_allow_html=True
)

# =========================================================
# Load Data
# =========================================================
@st.cache_data
def load_data():
    return pd.read_excel("../Excel/mutual_funds_.xlsx")

df = load_data()

# =========================================================
# Sidebar – User Inputs
# =========================================================
st.sidebar.header("Investment Preferences")

risk_level = st.sidebar.selectbox(
    "Risk Preference",
    ["No Preference", "Low", "Moderate", "High"]
)

investment_type = st.sidebar.radio(
    "Investment Type",
    ["SIP", "Lumpsum"]
)

compare_mode = st.sidebar.toggle("Compare SIP vs Lumpsum")

amount = st.sidebar.number_input(
    "Investment Amount (₹)",
    min_value=1000,
    step=1000,
    value=5000
)

years = st.sidebar.slider(
    "Investment Duration (Years)",
    min_value=1,
    max_value=30,
    value=10
)

run = st.sidebar.button("Generate Recommendations")

# =========================
# NUMERIC SANITIZATION (CRITICAL)
# =========================
numeric_cols = ["returns_5yr", "sharpe", "standard_deviation"]

df[numeric_cols] = (
    df[numeric_cols]
    .replace(["-", "—", ""], np.nan)
    .apply(pd.to_numeric, errors="coerce")
    .astype(float)
)

df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# =========================================================
# Feature Engineering
# =========================================================
df = df.copy()

df["z_returns_5yr"] = zscore(df["returns_5yr"].to_numpy())
df["z_sharpe"] = zscore(df["sharpe"].to_numpy())
df["z_std_dev"] = -zscore(df["standard_deviation"].to_numpy())  # lower volatility is better

df["raw_score"] = (
    0.5 * df["z_returns_5yr"] +
    0.3 * df["z_sharpe"] +
    0.2 * df["z_std_dev"]
)

df["ranking_score"] = zscore(df["raw_score"])

# =========================================================
# Risk Mapping
# =========================================================
RISK_MAP = {
    "Low": ["Low Risk", "Moderately Low"],
    "Moderate": ["Moderate"],
    "High": ["High Risk"]
}

# =========================================================
# Utility Functions
# =========================================================
def future_value_sip(monthly, annual_return, years):
    r = annual_return / 100 / 12
    n = years * 12
    return monthly * ((1 + r) ** n - 1) / r * (1 + r)

def future_value_lumpsum(amount, annual_return, years):
    return amount * ((1 + annual_return / 100) ** years)

def format_lakhs(value):
    return f"₹{value / 1e5:,.2f} Lakhs"

def confidence_score(row):
    score = (
        0.45 * row["z_returns_5yr"] +
        0.35 * row["z_sharpe"] +
        0.20 * row["z_std_dev"]
    )
    return round(min(100, max(0, 50 + score * 15)), 2)

def explain_fund(row):
    reasons = []

    if row["z_returns_5yr"] > 0.75:
        reasons.append("Strong long-term returns")
    elif row["z_returns_5yr"] > 0:
        reasons.append("Above-average returns")
    else:
        reasons.append("Moderate returns")

    if row["z_sharpe"] > 0.5:
        reasons.append("Good risk-adjusted performance")
    elif row["z_sharpe"] > 0:
        reasons.append("Acceptable risk-adjusted performance")

    if row["z_std_dev"] < 0:
        reasons.append("Higher volatility expected")
    else:
        reasons.append("Relatively stable volatility")

    return ", ".join(reasons)

# =========================================================
# Main Logic
# =========================================================
if run:

    # ---------- Risk Filtering ----------
    if risk_level == "No Preference":
        low = df[df["risk_bucket"].isin(["Low Risk", "Moderately Low"])].nlargest(2, "ranking_score")
        moderate = df[df["risk_bucket"] == "Moderate"].nlargest(2, "ranking_score")
        high = df[df["risk_bucket"] == "High Risk"].nlargest(2, "ranking_score")
        filtered = pd.concat([low, moderate, high])
        st.caption("Balanced selection across all risk categories")
    else:
        filtered = df[df["risk_bucket"].isin(RISK_MAP[risk_level])]
        st.caption(f"Funds aligned with {risk_level} risk preference")

    # ---------- Top Funds ----------
    top_funds = (
        filtered
        .sort_values("ranking_score", ascending=False)
        .head(5)
        .copy()
    )

    # ---------- Ranking ----------
    top_funds["Rank"] = range(1, len(top_funds) + 1)

    # ---------- Projections ----------
    top_funds["SIP Corpus"] = top_funds["returns_5yr"].apply(
        lambda r: future_value_sip(amount, r, years)
    )

    top_funds["Lumpsum Corpus"] = top_funds["returns_5yr"].apply(
        lambda r: future_value_lumpsum(amount * 12 * years, r, years)
    )

    top_funds["Confidence (%)"] = top_funds.apply(confidence_score, axis=1)
    top_funds["Recommendation Rationale"] = top_funds.apply(explain_fund, axis=1)

    # =========================================================
    # KPI Cards
    # =========================================================
    best = top_funds.iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Top Ranked Fund", best["scheme_name"])
    c2.metric("Projected SIP Value", format_lakhs(best["SIP Corpus"]))
    c3.metric("Confidence Score", f"{best['Confidence (%)']}%")

    st.divider()

    # =========================================================
    # Return vs Risk Visualization
    # =========================================================
    st.subheader("Return vs Risk Analysis")

    fig = px.scatter(
        top_funds,
        x="standard_deviation",
        y="returns_5yr",
        size="Confidence (%)",
        color="scheme_name",
        labels={
            "standard_deviation": "Volatility (Risk)",
            "returns_5yr": "5-Year Annual Return (%)"
        },
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # SIP vs Lumpsum Comparison
    # =========================================================
    if compare_mode:
        st.subheader("SIP vs Lumpsum Comparison")

        compare_df = pd.DataFrame({
            "Fund": top_funds["scheme_name"],
            "SIP (₹ Lakhs)": (top_funds["SIP Corpus"] / 1e5).round(2),
            "Lumpsum (₹ Lakhs)": (top_funds["Lumpsum Corpus"] / 1e5).round(2)
        })

        fig2 = px.bar(
            compare_df.melt(id_vars="Fund"),
            x="Fund",
            y="value",
            color="variable",
            barmode="group",
            labels={"value": "Corpus (₹ Lakhs)", "variable": "Investment Type"},
            height=420
        )

        st.plotly_chart(fig2, use_container_width=True)
    


    # =========================================================
    # Final Table
    # =========================================================
    final_view = top_funds[[
        "Rank",
        "scheme_name",
        "risk_bucket",
        "ranking_score",
        "Confidence (%)",
        "returns_5yr",
        "SIP Corpus",
        "Recommendation Rationale"
    ]].copy()

    final_view["SIP Corpus"] = final_view["SIP Corpus"].apply(format_lakhs)

    final_view.columns = [
        "Rank",
        "Fund Name",
        "Risk Level",
        "Model Ranking Score",
        "Confidence Level (%)",
        "5-Year Annual Return (%)",
        "Expected SIP Value",
        "Recommendation Rationale"
    ]

    st.subheader("Top Recommended Mutual Funds")
    st.dataframe(final_view, use_container_width=True)

    # =========================================================
    # Export
    # =========================================================
    st.subheader("Export Recommendation Report")

    csv = final_view.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        data=csv,
        file_name="mutual_fund_recommendations.csv",
        mime="text/csv"
    )

    # =========================================================
    # Methodology
    # =========================================================
    with st.expander("How recommendations are generated"):
        st.markdown("""
        - **Return Strength**: Long-term historical returns  
        - **Risk-Adjusted Strength**: Sharpe ratio  
        - **Volatility Control**: Standard deviation  
        - Scores are normalized and combined using weighted quantitative logic
        """)

else:
    st.info("Select preferences from the sidebar and click **Generate Recommendations**")