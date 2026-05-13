import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# =====================================================
# 🌍 PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="International Debt Dashboard",
    layout="wide"
)

# =====================================================
# 🔗 MYSQL CONNECTION
# =====================================================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Thaheer@1609",
        database="debt_project"
    )

# =====================================================
# 📥 LOAD DATA
# =====================================================
@st.cache_data
def load_data():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM debt_data",
        conn
    )

    conn.close()

    return df

df = load_data().copy()

if df.empty:
    st.error("❌ No data found. Run app.py first.")
    st.stop()

st.success("✅ Data Loaded Successfully")

# =====================================================
# 🌍 TITLE
# =====================================================
st.title("🌍 International Debt Analysis Dashboard")

# =====================================================
# 📌 SIDEBAR MENU
# =====================================================
menu = st.sidebar.radio(
    "Go To",
    ["Dashboard", "SQL Analysis", "Insights"]
)

# =====================================================
# 📊 DASHBOARD
# =====================================================
if menu == "Dashboard":

    st.sidebar.header("🔍 Filter")

    # ---------------- COUNTRY FILTER ----------------
    countries = ["All"] + sorted(
        df["country_name"].dropna().unique()
    )

    selected_country = st.sidebar.selectbox(
        "Select Country",
        countries
    )

    # ---------------- YEAR FILTER ----------------
    years = ["All"] + sorted(
        df["year"].dropna().unique().tolist()
    )

    selected_year = st.sidebar.selectbox(
        "Select Year",
        years
    )

    # ---------------- REGION FILTER ----------------
    regions = ["All"] + sorted(
        df["region"].dropna().unique()
    )

    selected_region = st.sidebar.selectbox(
        "Select Region",
        regions
    )

    # ---------------- FILTER LOGIC ----------------
    filtered_df = df.copy()

    if selected_country != "All":
        filtered_df = filtered_df[
            filtered_df["country_name"] == selected_country
        ]

    if selected_year != "All":
        filtered_df = filtered_df[
            filtered_df["year"] == selected_year
        ]

    if selected_region != "All":
        filtered_df = filtered_df[
            filtered_df["region"] == selected_region
        ]

    st.caption(
        f"Country = {selected_country} | "
        f"Year = {selected_year} | "
        f"Region = {selected_region}"
    )

    # =====================================================
    # 📊 OVERVIEW
    # =====================================================
    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Debt",
        f"${filtered_df['value'].sum():,.0f}"
    )

    col2.metric(
        "Countries",
        filtered_df["country_name"].nunique()
    )

    col3.metric(
        "Indicators",
        filtered_df["series_name"].nunique()
    )

    st.markdown("---")

    # =====================================================
    # 🏆 TOP COUNTRIES
    # =====================================================
    st.subheader("🏆 Top Countries by Debt")

    top = (
        filtered_df.groupby("country_name")["value"]
        .sum()
        .reset_index()
        .sort_values(by="value", ascending=False)
        .head(10)
    )

    st.plotly_chart(
        px.bar(
            top,
            x="country_name",
            y="value",
            text_auto=True
        ),
        use_container_width=True,
        key="dash1"
    )

    st.markdown("---")

    # =====================================================
    # 📌 INDICATOR
    # =====================================================
    st.subheader("📌 Debt by Indicator")

    ind = (
        filtered_df.groupby("series_name")["value"]
        .sum()
        .reset_index()
        .sort_values(by="value", ascending=False)
        .head(10)
    )

    st.plotly_chart(
        px.pie(
            ind,
            names="series_name",
            values="value"
        ),
        use_container_width=True,
        key="dash2"
    )

    st.markdown("---")

    # =====================================================
    # 📈 TREND
    # =====================================================
    st.subheader("📈 Year-wise Trend")

    trend = (
        filtered_df.groupby("year")["value"]
        .sum()
        .reset_index()
    )

    st.plotly_chart(
        px.line(
            trend,
            x="year",
            y="value",
            markers=True
        ),
        use_container_width=True,
        key="dash3"
    )

# =====================================================
# 🚀 SQL ANALYSIS (30 QUERIES)
# =====================================================
elif menu == "SQL Analysis":

    st.subheader("🚀 SQL Query Analysis (30 Queries)")

    query_labels = {

        "1. Retrieve all distinct country names":
        "SELECT DISTINCT country_name FROM debt_data",

        "2. Count total number of countries":
        "SELECT COUNT(DISTINCT country_name) FROM debt_data",

        "3. Total number of indicators":
        "SELECT COUNT(DISTINCT series_code) FROM debt_data",

        "4. First 10 records":
        "SELECT * FROM debt_data LIMIT 10",

        "5. Total global debt":
        "SELECT SUM(value) FROM debt_data",

        "6. Unique indicator names":
        "SELECT DISTINCT series_name FROM debt_data",

        "7. Number of records per country":
        "SELECT country_name, COUNT(*) FROM debt_data GROUP BY country_name",

        "8. Debt > 1 billion USD":
        "SELECT * FROM debt_data WHERE value > 1000000000",

        "9. Min, Max, Avg debt":
        "SELECT MIN(value), MAX(value), AVG(value) FROM debt_data",

        "10. Total records":
        "SELECT COUNT(*) FROM debt_data",

        "11. Total debt per country":
        "SELECT country_name, SUM(value) FROM debt_data GROUP BY country_name",

        "12. Top 10 countries by total debt":
        "SELECT country_name, SUM(value) total FROM debt_data GROUP BY country_name ORDER BY total DESC LIMIT 10",

        "13. Average debt per country":
        "SELECT country_name, AVG(value) FROM debt_data GROUP BY country_name",

        "14. Total debt per indicator":
        "SELECT series_name, SUM(value) FROM debt_data GROUP BY series_name",

        "15. Indicator with highest debt":
        "SELECT series_name, SUM(value) total FROM debt_data GROUP BY series_name ORDER BY total DESC LIMIT 1",

        "16. Country with lowest total debt":
        "SELECT country_name, SUM(value) total FROM debt_data GROUP BY country_name ORDER BY total ASC LIMIT 1",

        "17. Country + indicator combination debt":
        "SELECT country_name, series_name, SUM(value) FROM debt_data GROUP BY country_name, series_name",

        "18. Count indicators per country":
        "SELECT country_name, COUNT(DISTINCT series_code) FROM debt_data GROUP BY country_name",

        "19. Countries above global average debt":
        """SELECT country_name, SUM(value) total
        FROM debt_data
        GROUP BY country_name
        HAVING total >
        (
            SELECT AVG(country_total)
            FROM (
                SELECT SUM(value) country_total
                FROM debt_data
                GROUP BY country_name
            ) t
        )""",

        "20. Rank countries by total debt":
        """SELECT country_name,
        SUM(value),
        RANK() OVER (ORDER BY SUM(value) DESC)
        FROM debt_data
        GROUP BY country_name""",

        "21. Top 5 indicators contributing to global debt":
        "SELECT series_name, SUM(value) FROM debt_data GROUP BY series_name ORDER BY SUM(value) DESC LIMIT 5",

        "22. Percentage contribution of each country":
        """SELECT country_name,
        SUM(value),
        (SUM(value)/(SELECT SUM(value) FROM debt_data))*100
        FROM debt_data
        GROUP BY country_name""",

        "23. Top 3 countries per indicator":
        """SELECT * FROM (
        SELECT country_name,
        series_name,
        SUM(value),
        RANK() OVER (
        PARTITION BY series_name
        ORDER BY SUM(value) DESC
        ) rnk
        FROM debt_data
        GROUP BY country_name, series_name
        ) t WHERE rnk<=3""",

        "24. Debt range per country":
        "SELECT country_name, MAX(value)-MIN(value) FROM debt_data GROUP BY country_name",

        "25. View: Top 10 countries":
        "SELECT * FROM top_10_countries",

        "26. Debt classification":
        """SELECT country_name,
        SUM(value),
        CASE
        WHEN SUM(value)>10000000000 THEN 'High'
        WHEN SUM(value)>1000000000 THEN 'Medium'
        ELSE 'Low'
        END
        FROM debt_data
        GROUP BY country_name""",

        "27. Cumulative debt per country":
        """SELECT country_name,
        year,
        SUM(value) OVER (
        PARTITION BY country_name
        ORDER BY year
        )
        FROM debt_data""",

        "28. Indicators above overall average":
        """SELECT series_name,
        AVG(value)
        FROM debt_data
        GROUP BY series_name
        HAVING AVG(value) >
        (
            SELECT AVG(value)
            FROM debt_data
        )""",

        "29. Countries contributing >5% global debt":
        """SELECT country_name,
        SUM(value),
        (SUM(value)/(SELECT SUM(value) FROM debt_data))*100
        FROM debt_data
        GROUP BY country_name
        HAVING
        (SUM(value)/(SELECT SUM(value) FROM debt_data))*100 > 5""",

        "30. Most dominant indicator per country":
        """SELECT * FROM (
        SELECT country_name,
        series_name,
        SUM(value),
        RANK() OVER (
        PARTITION BY country_name
        ORDER BY SUM(value) DESC
        ) rnk
        FROM debt_data
        GROUP BY country_name, series_name
        ) t WHERE rnk=1"""
    }

    selected = st.selectbox(
        "Select Query",
        list(query_labels.keys())
    )

    conn = get_connection()

    result = pd.read_sql(
        query_labels[selected],
        conn
    )

    conn.close()

    st.markdown("---")

    st.dataframe(
        result,
        use_container_width=True
    )

    if result.shape[1] >= 2:

        st.plotly_chart(
            px.bar(
                result,
                x=result.columns[0],
                y=result.columns[1]
            ),
            use_container_width=True,
            key=f"sql_{selected}"
        )

# =====================================================
# 📊 INSIGHTS
# =====================================================
elif menu == "Insights":

    st.sidebar.header("🔍 Filter")

    # ---------------- COUNTRY FILTER ----------------
    countries = ["All"] + sorted(
        df["country_name"].unique()
    )

    selected_country = st.sidebar.selectbox(
        "Select Country",
        countries,
        key="insight_country"
    )

    # ---------------- YEAR FILTER ----------------
    years = ["All"] + sorted(
        df["year"].unique().tolist()
    )

    selected_year = st.sidebar.selectbox(
        "Select Year",
        years,
        key="insight_year"
    )

    # ---------------- REGION FILTER ----------------
    regions = ["All"] + sorted(
        df["region"].unique()
    )

    selected_region = st.sidebar.selectbox(
        "Select Region",
        regions,
        key="insight_region"
    )

    # ---------------- FILTER LOGIC ----------------
    filtered_df = df.copy()

    if selected_country != "All":
        filtered_df = filtered_df[
            filtered_df["country_name"] == selected_country
        ]

    if selected_year != "All":
        filtered_df = filtered_df[
            filtered_df["year"] == selected_year
        ]

    if selected_region != "All":
        filtered_df = filtered_df[
            filtered_df["region"] == selected_region
        ]

    st.caption(
        f"Country = {selected_country} | "
        f"Year = {selected_year} | "
        f"Region = {selected_region}"
    )

    st.subheader("📊 Key Insights")

    country = (
        filtered_df.groupby("country_name")["value"]
        .sum()
        .reset_index()
        .sort_values(by="value", ascending=False)
    )

    indicator = (
        filtered_df.groupby("series_name")["value"]
        .sum()
        .reset_index()
        .sort_values(by="value", ascending=False)
    )

    trend = (
        filtered_df.groupby("year")["value"]
        .sum()
        .reset_index()
    )

    # =====================================================
    # 1. TOP 10
    # =====================================================
    st.write("🔹 Country-wise Debt Distribution (Top 10)")

    st.plotly_chart(
        px.bar(
            country.head(10),
            x="country_name",
            y="value"
        ),
        use_container_width=True,
        key="i1"
    )

    st.markdown("---")

    # =====================================================
    # 2. HIGHEST
    # =====================================================
    st.write("🔹 Highest Debt Country")

    st.plotly_chart(
        px.bar(
            country.head(1),
            x="country_name",
            y="value"
        ),
        use_container_width=True,
        key="i2"
    )

    st.markdown("---")

    # =====================================================
    # 3. LOWEST
    # =====================================================
    st.write("🔹 Lowest Debt Country")

    st.plotly_chart(
        px.bar(
            country.tail(1),
            x="country_name",
            y="value"
        ),
        use_container_width=True,
        key="i3"
    )

    st.markdown("---")

    # =====================================================
    # 4. INDICATOR
    # =====================================================
    st.write("🔹 Debt by Indicator (Top 10)")

    st.plotly_chart(
        px.pie(
            indicator.head(10),
            names="series_name",
            values="value"
        ),
        use_container_width=True,
        key="i4"
    )

    # =====================================================
    # 🔥 ADDITIONAL INSIGHTS
    # =====================================================
    st.markdown("## 🔥 Additional Insights")

    total = filtered_df["value"].sum()

    top10 = country.head(10).copy()

    # =====================================================
    # 5. CONTRIBUTION %
    # =====================================================
    st.write("✔ Top 10 Countries Contribution %")

    if total != 0:
        top10["percentage"] = (
            top10["value"] / total
        ) * 100
    else:
        top10["percentage"] = 0

    st.plotly_chart(
        px.bar(
            top10,
            x="country_name",
            y="percentage"
        ),
        use_container_width=True,
        key="i5"
    )

    st.markdown("---")

    # =====================================================
    # 6. ABOVE AVERAGE
    # =====================================================
    st.write("✔ Countries Above Average Debt")

    avg = country["value"].mean()

    above = country[
        country["value"] > avg
    ]

    st.plotly_chart(
        px.bar(
            above.head(10),
            x="country_name",
            y="value"
        ),
        use_container_width=True,
        key="i6"
    )

    st.markdown("---")

    # =====================================================
    # 7. RANGE
    # =====================================================
    st.write("✔ Debt Range per Country")

    rng = (
        filtered_df.groupby("country_name")["value"]
        .agg(["min", "max"])
        .reset_index()
    )

    rng["range"] = rng["max"] - rng["min"]

    st.plotly_chart(
        px.bar(
            rng.head(10),
            x="country_name",
            y="range"
        ),
        use_container_width=True,
        key="i7"
    )

    st.markdown("---")

    # =====================================================
    # 8. TREND
    # =====================================================
    st.write("✔ Global Debt Trend Over Time")

    st.plotly_chart(
        px.line(
            trend,
            x="year",
            y="value",
            markers=True
        ),
        use_container_width=True,
        key="i8"
    )
