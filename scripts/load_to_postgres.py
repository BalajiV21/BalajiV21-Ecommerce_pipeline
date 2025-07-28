import os
import pandas as pd
import psycopg2 # type: ignore
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
STAGING_PATH = os.getenv("STAGING_PATH", "./data_lake/staging/")

# PostgreSQL connection config
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB = os.getenv("PG_DB", "ecommerce")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "airflow")

# Connect to Postgres
conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    dbname=PG_DB,
    user=PG_USER,
    password=PG_PASSWORD
)
cur = conn.cursor()

# Loop through cleaned files
files = sorted([f for f in os.listdir(STAGING_PATH) if f.endswith(".csv")])
for file in files:
    path = os.path.join(STAGING_PATH, file)
    print(f"📥 Loading: {path}")

    df = pd.read_csv(path)
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO fact_sales (invoice, stock_code, description, quantity, invoice_date, price, total_price, customer_id, country)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row["Invoice"],
            row["StockCode"],
            row["Description"],
            int(row["Quantity"]),
            row["InvoiceDate"],
            float(row["Price"]),
            float(row["TotalPrice"]),
            int(row["Customer ID"]),
            row["Country"]
        ))

    conn.commit()
    print(f"✅ Done: {file}")

cur.close()
conn.close()
