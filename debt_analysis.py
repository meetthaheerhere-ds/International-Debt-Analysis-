import pandas as pd
import mysql.connector

print("Starting project...")

# Load dataset
main_df = pd.read_csv(
    "IDS_ALLCountries_Data.csv",
    nrows=10000,
    encoding="latin1"
)

# Keep only required columns + year columns
main_df = main_df[
    ["Country Name", "Country Code", "Series Name", "Series Code"]
    + [col for col in main_df.columns if col.isdigit()]
]

# Convert wide → long format
main_df = main_df.melt(
    id_vars=["Country Name", "Country Code", "Series Name", "Series Code"],
    var_name="Year",
    value_name="Value"
)

# Data cleaning
main_df.dropna(inplace=True)
main_df.drop_duplicates(inplace=True)

# Filter only external debt
main_df = main_df[main_df["Series Code"] == "DT.DOD.DECT.CD"]

# Convert datatypes 
main_df["Year"] = main_df["Year"].astype(int)
main_df["Value"] = main_df["Value"].astype(float)

print("Data ready for insertion")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Thaheer@1609",
    database="debt_project"
)

cursor = conn.cursor()
cursor.execute("TRUNCATE TABLE debt_data")

# Insert data
for _, row in main_df.iterrows():
    cursor.execute("""
        INSERT INTO debt_data 
        (country_name, country_code, series_name, series_code, year, value)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()

print("Data inserted successfully")

cursor.close()
conn.close()