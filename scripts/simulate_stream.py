import pandas as pd
import os
import time
from dotenv import load_dotenv

# Load .env for RAW_PATH config
load_dotenv()
RAW_PATH = os.getenv("RAW_PATH", "./data_lake/raw/")

# Ensure raw directory exists
os.makedirs(RAW_PATH, exist_ok=True)

# Load dataset
df = pd.read_csv("./dataset/online_retail_II.csv", encoding='ISO-8859-1')

# Filter rows with valid invoices and customers
df = df.dropna(subset=["Invoice", "Customer ID"])

# Group by invoice number
invoice_groups = df.groupby("Invoice")
invoice_list = list(invoice_groups)

# Set batch size and sleep time
BATCH_SIZE = 150
SLEEP_TIME = 0.5 # seconds

print(f"Total invoice groups: {len(invoice_list)}")
print(f"Streaming in batches of {BATCH_SIZE} every {SLEEP_TIME} seconds...")

for i in range(0, len(invoice_list), BATCH_SIZE):
    batch = invoice_list[i:i + BATCH_SIZE]
    batch_df = pd.concat([group for _, group in batch])

    batch_file = f"batch_{i // BATCH_SIZE + 1}.csv"
    output_path = os.path.join(RAW_PATH, batch_file)
    batch_df.to_csv(output_path, index=False)

    print(f"[Batch {i // BATCH_SIZE + 1}] Streamed → {output_path}")
    time.sleep(SLEEP_TIME)
