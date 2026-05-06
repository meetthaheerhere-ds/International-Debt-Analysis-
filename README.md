🌍 International Debt Analysis System

📌 Project Overview

This project focuses on analyzing global debt data sourced from the World Bank. The raw dataset is transformed into a structured format using Python, stored in a MySQL database, and visualized through an interactive Streamlit dashboard.

The system enables users to explore country-wise debt, indicator-based insights, and global financial trends using SQL and data visualization techniques.

🚀 Tech Stack
Python (Pandas) – Data cleaning & preprocessing
MySQL – Data storage & querying
Streamlit – Dashboard development
Plotly – Interactive visualizations

📊 Key Features
✔ Data Cleaning & Preprocessing (handling nulls, duplicates)
✔ CSV to Structured Data Transformation
✔ MySQL Database Integration
✔ 30 SQL Analytical Queries (Basic → Advanced)
✔ Interactive Dashboard using Streamlit
✔ Country-wise & Indicator-wise Analysis
✔ Additional Insights & Trend Analysis

📁 Project Structure
📦 International-Debt-Analysis
 ┣ 📂 data/
 ┃ ┣ IDS_ALLCountries_Data.csv
 ┃ ┣ Country-Series - Metadata.csv
 ┃ ┣ IDS_CountryMetaData.csv
 ┃ ┣ IDS_SeriesMetaData.csv
 ┃ ┗ IDS_FootNoteMetaData.csv
 ┣ 📄 app.py                → Data preprocessing & MySQL insertion
 ┣ 📄 db.py                 → Streamlit dashboard
 ┣ 📄 mini project 2.sql    → Database schema & queries
 ┣ 📄 README.md
 ┣ 📄 Presentation.pptx
 ┗ 📄 Documentation.pdf

⚙️ How to Run the Project

1️⃣ Install Dependencies
pip install pandas mysql-connector-python streamlit plotly

2️⃣ Run Data Pipeline
python app.py

3️⃣ Launch Dashboard
streamlit run db.py

🗄️ Database Design
Single main table: debt_data
Indexed columns for performance:
country_name
series_code
year

📊 SQL Analysis

The project includes 30 SQL queries, covering:

🔹 Basic
Total countries, indicators
Global debt calculation
Filtering high debt values

🔹 Intermediate
Country-wise aggregation
Top & lowest debt countries
Ranking using RANK()

🔹 Advanced
Window functions
Percentage contribution
Cumulative debt
Debt classification (High / Medium / Low)

📈 Key Insights
🌍 A small number of countries contribute a large share of global debt
📊 External debt dominates across financial indicators
📉 Significant inequality exists between high-debt and low-debt countries
📈 Debt trends show fluctuations across years
🔍 Few countries consistently rank at the top across indicators

🎯 Project Outcome
✔ Cleaned and transformed dataset
✔ Structured relational database
✔ SQL-based analytical insights
✔ Interactive visualization dashboard
✔ End-to-end data analytics pipeline

👨‍💻 Author

Thaheer
