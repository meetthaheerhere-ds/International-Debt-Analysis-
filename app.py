import pandas as pd
import mysql.connector

print("🚀 Starting project...")

try:
    # ---------------- LOAD DATA ----------------
    main_df = pd.read_csv("IDS_ALLCountries_Data.csv", encoding="latin1")
    print(f"✅ Loaded: {main_df.shape}")

    # ---------------- SELECT COLUMNS ----------------
    main_df = main_df[
        ["Country Name", "Country Code", "Series Name", "Series Code"]
        + [col for col in main_df.columns if col.isdigit()]
    ]

    # ---------------- MELT ----------------
    main_df = main_df.melt(
        id_vars=["Country Name", "Country Code", "Series Name", "Series Code"],
        var_name="Year",
        value_name="Value"
    )

    print(f"📊 After melt: {main_df.shape}")

    # ---------------- CLEANING ----------------
    main_df = main_df[main_df["Value"].notna()]
    main_df.drop_duplicates(inplace=True)

    # ---------------- REMOVE AGGREGATED DATA ----------------
    main_df = main_df[
        ~main_df["Country Name"].str.contains(
            "income|region|IBRD|IDA|World|OECD|Euro",
            case=False,
            na=False
        )
    ]

    print(f"📊 After cleaning: {main_df.shape}")

    # ---------------- FILTER SERIES ----------------
    main_df = main_df[main_df["Series Code"] == "DT.DOD.DECT.CD"]

    print(f"📊 After filter: {len(main_df)} rows")

    if main_df.empty:
        raise ValueError("❌ No data after filtering")

    # ---------------- TYPE CONVERSION ----------------
    main_df["Year"] = main_df["Year"].astype(int)
    main_df["Value"] = main_df["Value"].astype(float)

    # ---------------- RENAME ----------------
    main_df.columns = [
        "country_name", "country_code",
        "series_name", "series_code",
        "year", "value"
    ]

    # ---------------- MYSQL CONNECTION ----------------
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Thaheer@1609",
        database="debt_project"
    )
    cursor = conn.cursor()

    # ---------------- CLEAR TABLE ----------------
    cursor.execute("TRUNCATE TABLE debt_data")

    # ---------------- INSERT ----------------
    data = list(main_df.itertuples(index=False, name=None))

    query = """
    INSERT INTO debt_data 
    (country_name, country_code, series_name, series_code, year, value)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    batch_size = 10000
    for i in range(0, len(data), batch_size):
        cursor.executemany(query, data[i:i+batch_size])
        conn.commit()

    print(f"🎉 Inserted {len(data)} rows")

except Exception as e:
    print("❌ Error:", e)

finally:
    try:
        cursor.close()
        conn.close()
        print("🔒 Closed DB")
    except:
        pass