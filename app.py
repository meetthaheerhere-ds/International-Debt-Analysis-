import pandas as pd
import mysql.connector

print("🚀 Starting project...")

try:
    # ---------------- LOAD MAIN DATA ----------------
    main_df = pd.read_csv(
        "data/IDS_ALLCountries_Data.csv",
        encoding="latin1"
    )

    # ---------------- LOAD COUNTRY METADATA ----------------
    meta_df = pd.read_csv(
        "data/IDS_CountryMetaData.csv",
        encoding="latin1"
    )

    print(f"✅ Loaded Main Data: {main_df.shape}")
    print(f"✅ Loaded Metadata: {meta_df.shape}")

    # ---------------- SELECT REQUIRED COLUMNS ----------------
    main_df = main_df[
        ["Country Name", "Country Code", "Series Name", "Series Code"]
        + [col for col in main_df.columns if col.isdigit()]
    ]

    # ---------------- MELT YEARS ----------------
    main_df = main_df.melt(
        id_vars=[
            "Country Name",
            "Country Code",
            "Series Name",
            "Series Code"
        ],
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
    main_df = main_df[
        main_df["Series Code"] == "DT.DOD.DECT.CD"
    ]

    print(f"📊 After filter: {len(main_df)} rows")

    # ---------------- MERGE REGION DATA ----------------
    meta_df = meta_df[["Code", "Region"]]

    # CLEAN SPACES
    meta_df["Code"] = meta_df["Code"].astype(str).str.strip()
    main_df["Country Code"] = (
        main_df["Country Code"]
        .astype(str)
        .str.strip()
    )

    # MERGE
    main_df = pd.merge(
        main_df,
        meta_df,
        left_on="Country Code",
        right_on="Code",
        how="left"
    )

    print("✅ Region merged successfully")

    # DROP EXTRA COLUMN
    main_df.drop(columns=["Code"], inplace=True)

    # HANDLE EMPTY REGION
    main_df["Region"] = main_df["Region"].fillna("Unknown")

    # ---------------- TYPE CONVERSION ----------------
    main_df["Year"] = main_df["Year"].astype(int)
    main_df["Value"] = main_df["Value"].astype(float)

    # ---------------- RENAME COLUMNS ----------------
    main_df.columns = [
        "country_name",
        "country_code",
        "series_name",
        "series_code",
        "year",
        "value",
        "region"
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
    (
        country_name,
        country_code,
        series_name,
        series_code,
        year,
        value,
        region
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
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
