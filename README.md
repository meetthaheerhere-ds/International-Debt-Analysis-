🌍 International Debt Analysis System
📌 Project Overview

The International Debt Analysis System is an end-to-end data analytics project that explores global debt statistics sourced from the World Bank. The raw dataset is processed using Python, transformed into a structured format, and stored in a MySQL database. An interactive Streamlit dashboard is then used to visualize insights and perform SQL-based analysis.

This project demonstrates a complete data pipeline workflow — from data ingestion and cleaning to database design, analytical querying, and visualization.

🚀 Tech Stack
Python (Pandas) – Data cleaning, transformation, preprocessing
MySQL – Relational database storage & SQL analytics
Streamlit – Interactive web dashboard
Plotly – Data visualization & charts
📊 Key Features
✔ End-to-end ETL pipeline (CSV → MySQL)
✔ Data cleaning (null handling, duplicates removal, filtering aggregates)
✔ Wide-to-long transformation using Pandas melt
✔ MySQL integration with optimized batch insertion
✔ Indexed database for improved query performance
✔ 30 SQL analytical queries (basic to advanced)
✔ Interactive Streamlit dashboard with filters
✔ Country-wise, region-wise, and indicator-wise analysis
✔ Trend analysis across years
✔ Insight generation using grouped aggregations
📁 Project Structure
📦 International-Debt-Analysis
 ┣ 📂 data/
 ┃ ┣ IDS_ALLCountries_Data.csv
 ┃ ┣ IDS_CountryMetaData.csv
 ┃ ┣ IDS_SeriesMetaData.csv
 ┃ ┣ IDS_FootNoteMetaData.csv
 ┣ 📄 app.py                → ETL pipeline & MySQL data insertion
 ┣ 📄 db.py                 → Streamlit dashboard
 ┣ 📄 mini project 2.sql    → Database schema & SQL queries
 ┣ 📄 README.md
 ┣ 📄 Presentation.pptx
 ┗ 📄 Documentation.pdf
⚙️ How to Run the Project
1️⃣ Install Dependencies
pip install pandas mysql-connector-python streamlit plotly
2️⃣ Setup Database

Run the SQL script:

mysql -u root -p < mini project 2.sql
3️⃣ Run ETL Pipeline
python app.py
4️⃣ Launch Dashboard
streamlit run db.py
🗄️ Database Design

The system uses a single optimized table:

Table: debt_data

Key indexed columns:

country_name
series_code
year
region

This indexing improves query performance for analytical operations.

📊 SQL Analysis

The project includes 30 SQL queries, categorized as:

🔹 Basic Analysis
Total countries and indicators
Global debt calculation
Data filtering operations
🔹 Intermediate Analysis
Country-wise aggregation
Top & lowest debt countries
Ranking using window functions
🔹 Advanced Analysis
Percentage contribution to global debt
Cumulative debt trends
Conditional classification (High / Medium / Low debt)
Partition-based ranking
📈 Key Insights
🌍 A small group of countries contributes a major share of global debt
📊 External debt is concentrated in specific indicators
📉 Significant disparity exists between high and low debt economies
📈 Debt trends show fluctuations across years with noticeable spikes
🔍 Certain countries consistently appear in top rankings across indicators
🎯 Project Outcome
✔ Built a complete ETL data pipeline
✔ Designed and optimized relational database schema
✔ Performed advanced SQL analytics
✔ Developed an interactive dashboard using Streamlit
✔ Generated actionable insights from global debt data
✔ Demonstrated end-to-end data engineering workflow
👨‍💻 Author

Thaheer
