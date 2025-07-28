CREATE TABLE IF NOT EXISTS fact_sales (
    invoice TEXT,
    stock_code TEXT,
    description TEXT,
    quantity INTEGER,
    invoice_date TIMESTAMP,
    price FLOAT,
    total_price FLOAT,
    customer_id INTEGER,
    country TEXT
);
