import os
import pandas as pd
from dotenv import load_dotenv

# Load env vars
load_dotenv()
RAW_PATH = os.getenv("RAW_PATH", "./data_lake/raw/")
STAGING_PATH = os.getenv("STAGING_PATH", "./data_lake/staging/")

# Create staging folder if needed
os.makedirs(STAGING_PATH, exist_ok=True)

# Required columns (update: 'Price' instead of 'UnitPrice')
required_columns = {"Invoice", "Customer ID", "Quantity", "Price", "InvoiceDate", "Description"}

# List raw files
raw_files = sorted([f for f in os.listdir(RAW_PATH) if f.endswith(".csv")])

if not raw_files:
    print("⚠️ No raw files found.")
else:
    for filename in raw_files:
        raw_path = os.path.join(RAW_PATH, filename)
        print(f"🔄 Processing: {raw_path}")
        try:
            df = pd.read_csv(raw_path, encoding="ISO-8859-1")

            # Check if all required columns exist
            if not required_columns.issubset(df.columns):
                raise KeyError(f"Missing columns: {required_columns - set(df.columns)}")

            # Drop nulls in key columns
            df.dropna(subset=required_columns, inplace=True)

            # Type conversions
            df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
            df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
            df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

            # Clean text columns
            df["Description"] = df["Description"].str.strip().str.title()
            df["Country"] = df["Country"].str.strip().str.title()

            # Drop rows with conversion errors
            df.dropna(inplace=True)

            # Add total price column
            df["TotalPrice"] = df["Quantity"] * df["Price"]

            # Save to staging
            cleaned_name = f"cleaned_{filename}"
            cleaned_path = os.path.join(STAGING_PATH, cleaned_name)
            df.to_csv(cleaned_path, index=False)
            print(f"✅ Cleaned file saved to: {cleaned_path}")

        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")
