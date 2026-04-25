import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# ---------------- DB CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Thaheer@1609",
        database="debt_project"
    )

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM debt_data", conn)
    conn.close()
    return df

df = load_data().copy()

# CHECK
if df.empty:
    st.error("❌ No data found in database. Please run debt_analysis.py first.")
    st.stop()

st.success("✅ Data Loaded Successfully")
st.caption(f"Dataset Shape: {df.shape}")

# ---------------- TITLE ----------------
st.title("🌍 International Debt Analysis Dashboard")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Dashboard", "SQL Analysis", "Insights"])

# =====================================================
# 📊 DASHBOARD
# =====================================================
if menu == "Dashboard":

    st.subheader("📊 Overview")

    total_debt = df["value"].sum()
    total_countries = df["country_name"].nunique()
    total_indicators = df["series_name"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Debt", f"${total_debt:,.0f}")
    col2.metric("Countries", total_countries)
    col3.metric("Indicators", total_indicators)

    # Top Countries
    st.subheader("🏆 Top 10 Countries by Debt")
    top_countries = df.groupby("country_name")["value"].sum().reset_index()
    top_countries = top_countries.sort_values(by="value", ascending=False).head(10)

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(top_countries)
    with col2:
        st.plotly_chart(px.bar(top_countries, x="country_name", y="value", text_auto=True))

    # Indicator
    st.subheader("📌 Debt by Indicator")
    indicator = df.groupby("series_name")["value"].sum().reset_index()
    indicator = indicator.sort_values(by="value", ascending=False).head(10)

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(indicator)
    with col2:
        st.plotly_chart(px.pie(indicator, names="series_name", values="value"))

    # Trend
    st.subheader("📈 Year-wise Debt Trend")
    trend = df.groupby("year")["value"].sum().reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(trend)
    with col2:
        st.plotly_chart(px.line(trend, x="year", y="value", markers=True))

# =====================================================
# 🚀 SQL ANALYSIS (ONLY CHANGE HERE)
# =====================================================
elif menu == "SQL Analysis":

    st.subheader("🚀 SQL Query Analysis (30 Queries)")

    query_labels = {
        "1. Retrieve all distinct country names": "SELECT DISTINCT country_name FROM debt_data",
        "2. Count total number of countries": "SELECT COUNT(DISTINCT country_name) AS total_countries FROM debt_data",
        "3. Total number of indicators": "SELECT COUNT(DISTINCT series_code) AS total_indicators FROM debt_data",
        "4. First 10 records": "SELECT * FROM debt_data LIMIT 10",
        "5. Total global debt": "SELECT SUM(value) AS total_global_debt FROM debt_data",
        "6. Unique indicator names": "SELECT DISTINCT series_name FROM debt_data",
        "7. Number of records per country": "SELECT country_name, COUNT(*) FROM debt_data GROUP BY country_name",
        "8. Debt > 1 billion USD": "SELECT * FROM debt_data WHERE value > 1000000000",
        "9. Min, Max, Avg debt": "SELECT MIN(value), MAX(value), AVG(value) FROM debt_data",
        "10. Total records": "SELECT COUNT(*) FROM debt_data",

        "11. Total debt per country": "SELECT country_name, SUM(value) FROM debt_data GROUP BY country_name",
        "12. Top 10 countries by total debt": "SELECT country_name, SUM(value) total FROM debt_data GROUP BY country_name ORDER BY total DESC LIMIT 10",
        "13. Average debt per country": "SELECT country_name, AVG(value) FROM debt_data GROUP BY country_name",
        "14. Total debt per indicator": "SELECT series_name, SUM(value) FROM debt_data GROUP BY series_name",
        "15. Indicator with highest debt": "SELECT series_name, SUM(value) total FROM debt_data GROUP BY series_name ORDER BY total DESC LIMIT 1",
        "16. Country with lowest total debt": "SELECT country_name, SUM(value) total FROM debt_data GROUP BY country_name ORDER BY total ASC LIMIT 1",
        "17. Country + indicator combination debt": "SELECT country_name, series_name, SUM(value) FROM debt_data GROUP BY country_name, series_name",
        "18. Count indicators per country": "SELECT country_name, COUNT(DISTINCT series_code) FROM debt_data GROUP BY country_name",
        "19. Countries above global average debt": """SELECT country_name, SUM(value) total FROM debt_data GROUP BY country_name
        HAVING total > (SELECT AVG(country_total) FROM (SELECT SUM(value) country_total FROM debt_data GROUP BY country_name) t)""",
        "20. Rank countries by total debt": """SELECT country_name, SUM(value),
        RANK() OVER (ORDER BY SUM(value) DESC) FROM debt_data GROUP BY country_name""",

        "21. Top 5 indicators contributing to global debt": "SELECT series_name, SUM(value) FROM debt_data GROUP BY series_name ORDER BY SUM(value) DESC LIMIT 5",
        "22. Percentage contribution of each country": "SELECT country_name, SUM(value), (SUM(value)/(SELECT SUM(value) FROM debt_data))*100 FROM debt_data GROUP BY country_name",
        "23. Top 3 countries per indicator": """SELECT * FROM (
        SELECT country_name, series_name, SUM(value),
        RANK() OVER (PARTITION BY series_name ORDER BY SUM(value) DESC) rnk
        FROM debt_data GROUP BY country_name, series_name) t WHERE rnk<=3""",
        "24. Debt range per country": "SELECT country_name, MAX(value)-MIN(value) FROM debt_data GROUP BY country_name",
        "25. View: Top 10 countries": "SELECT * FROM top_10_countries",
        "26. Debt classification": """SELECT country_name, SUM(value),
        CASE WHEN SUM(value)>10000000000 THEN 'High'
        WHEN SUM(value)>1000000000 THEN 'Medium'
        ELSE 'Low' END FROM debt_data GROUP BY country_name""",
        "27. Cumulative debt per country": """SELECT country_name, year,
        SUM(value) OVER (PARTITION BY country_name ORDER BY year)
        FROM debt_data""",
        "28. Indicators above overall average": "SELECT series_name, AVG(value) FROM debt_data GROUP BY series_name HAVING AVG(value) > (SELECT AVG(value) FROM debt_data)",
        "29. Countries contributing >5% global debt": """SELECT country_name, SUM(value) AS total,
        (SUM(value)/(SELECT SUM(value) FROM debt_data))*100 AS percentage
        FROM debt_data GROUP BY country_name HAVING percentage > 5""",
        "30. Most dominant indicator per country": """SELECT * FROM (
        SELECT country_name, series_name, SUM(value),
        RANK() OVER (PARTITION BY country_name ORDER BY SUM(value) DESC) rnk
        FROM debt_data GROUP BY country_name, series_name
        ) t WHERE rnk=1"""
    }

    selected_label = st.selectbox("Select Query", list(query_labels.keys()))

    conn = get_connection()
    result = pd.read_sql(query_labels[selected_label], conn)
    conn.close()

    st.caption(f"Running: {selected_label}")

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(result)

    with col2:
        try:
            if result.shape[1] >= 2:
                st.plotly_chart(px.bar(result, x=result.columns[0], y=result.columns[1]))
        except:
            pass


# =====================================================
# 📊 INSIGHTS
# =====================================================
elif menu == "Insights":

    st.subheader("📊 Key Insights")

    country_dist = df.groupby("country_name")["value"].sum().reset_index()
    country_dist = country_dist.sort_values(by="value", ascending=False)

    indicator = df.groupby("series_name")["value"].sum().reset_index()
    indicator = indicator.sort_values(by="value", ascending=False)

    trend = df.groupby("year")["value"].sum().reset_index()

    # ---------------- 1. Top 10 Countries ----------------
    st.write("🔹 Country-wise Debt Distribution (Top 10)")
    top10 = country_dist.head(10)

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(top10)
    with col2:
        st.plotly_chart(px.bar(top10, x="country_name", y="value", text_auto=True))

    # ---------------- 2. Highest Debt ----------------
    st.write("🔹 Highest Debt Country")
    highest = country_dist.head(1)

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(highest)
    with col2:
        st.plotly_chart(px.bar(highest, x="country_name", y="value"))

    # ---------------- 3. Lowest Debt ----------------
    st.write("🔹 Lowest Debt Country")
    lowest = country_dist.tail(1)

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(lowest)
    with col2:
        st.plotly_chart(px.bar(lowest, x="country_name", y="value"))

    # ---------------- 4. Indicator-wise ----------------
    st.write("🔹 Debt by Indicator (Top 10)")
    top_indicator = indicator.head(10)

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(top_indicator)
    with col2:
        st.plotly_chart(px.pie(top_indicator, names="series_name", values="value"))

    # =====================================================
    # 🔥 ADDITIONAL INSIGHTS (4)
    # =====================================================
    st.subheader("🔥 Additional Insights")

    total = df["value"].sum()

    # ---------------- 5. Contribution % ----------------
    st.write("✔ Top 10 Countries Contribution %")
    top10["percentage"] = (top10["value"] / total) * 100

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(top10)
    with col2:
        st.plotly_chart(px.bar(top10, x="country_name", y="percentage"))

    # ---------------- 6. Above Average ----------------
    st.write("✔ Countries Above Average Debt")
    avg = country_dist["value"].mean()
    above_avg = country_dist[country_dist["value"] > avg]

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(above_avg.head(10))
    with col2:
        st.plotly_chart(px.bar(above_avg.head(10), x="country_name", y="value"))

    # ---------------- 7. Debt Range ----------------
    st.write("✔ Debt Range per Country")
    debt_range = df.groupby("country_name")["value"].agg(["min", "max"]).reset_index()
    debt_range["range"] = debt_range["max"] - debt_range["min"]

    top_range = debt_range.sort_values(by="range", ascending=False).head(10)

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(top_range)
    with col2:
        st.plotly_chart(px.bar(top_range, x="country_name", y="range"))

    # ---------------- 8. Year Trend ----------------
    st.write("✔ Global Debt Trend Over Time")

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(trend)
    with col2:
        st.plotly_chart(px.line(trend, x="year", y="value", markers=True))