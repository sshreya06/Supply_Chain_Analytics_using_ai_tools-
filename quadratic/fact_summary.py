#code for creating table "fact_summary" in quadratic

import pandas as pd
fact_orders_raw = q.cells("fact_order_line!A:Z")
dim_products_raw = q.cells("dim_products!A:Z")
dim_customers_raw = q.cells("dim_customers!A:Z")
exchange_rates_raw = q.cells("exchange_rate!A:Z")
def use_second_row_as_header(df):
    new_header = df.iloc[1]
    df = df[2:].reset_index(drop=True)
    df.columns = new_header
    return df
fact_orders = use_second_row_as_header(fact_orders_raw)
dim_products = use_second_row_as_header(dim_products_raw)
dim_customers = use_second_row_as_header(dim_customers_raw)
exchange_rates = use_second_row_as_header(exchange_rates_raw)

# ---------- 2. Clean data ----------

def clean_id(series):
    s = series.astype(str).str.strip()
    s = s.replace("", pd.NA)
    s = pd.to_numeric(s, errors="coerce")
    return s

# Clean and validate IDs
fact_orders["product_id"] = clean_id(fact_orders["product_id"])
dim_products["product_id"] = clean_id(dim_products["product_id"])

fact_orders["customer_id"] = clean_id(fact_orders["customer_id"])
dim_customers["customer_id"] = clean_id(dim_customers["customer_id"])

# Remove rows with NULL IDs
fact_orders = fact_orders.dropna(subset=["product_id", "customer_id"])
dim_products = dim_products.dropna(subset=["product_id"])
dim_customers = dim_customers.dropna(subset=["customer_id"])

# Convert to integers
fact_orders["product_id"] = fact_orders["product_id"].astype("int64")
fact_orders["customer_id"] = fact_orders["customer_id"].astype("int64")
dim_products["product_id"] = dim_products["product_id"].astype("int64")
dim_customers["customer_id"] = dim_customers["customer_id"].astype("int64")

# Convert dates
fact_orders["order_placement_date"] = pd.to_datetime(
    fact_orders["order_placement_date"], errors="coerce"
)
exchange_rates["date"] = pd.to_datetime(exchange_rates["date"], errors="coerce")

fact_orders = fact_orders.dropna(subset=["order_placement_date"])
exchange_rates = exchange_rates.dropna(subset=["date"])

# ---------- 3. Merge tables (safe, collision‑free) ----------

# 3.1 Prepare dimension tables to avoid duplicate columns
# Keep only the columns you actually need from each dim table

# From dim_products, keep product info
dim_products_keep = [
    "product_id",
    "product_name",
    "category",
    "price_INR",
    "price_USD"
]
dim_products_slim = dim_products[dim_products_keep]

# From dim_customers, keep customer info
dim_customers_keep = [
    "customer_id"
]
dim_customers_slim = dim_customers[dim_customers_keep]

# From exchange_rates, keep only date + rate
exchange_rates_keep = [
    "date",           
    "USD_INR_rate"
]
exchange_rates_slim = exchange_rates[exchange_rates_keep]

# 3.2 Merge orders with products
orders_products = fact_orders.merge(
    dim_products_slim,
    on="product_id",
    how="left",
    suffixes=("", "_prod")   # if any overlap, product columns get _prod
)

# 3.3 Merge result with customers
orders_customers = orders_products.merge(
    dim_customers_slim,
    on="customer_id",
    how="left",
    suffixes=("", "_cust")   # overlapping columns from customers get _cust
)

# 3.4 Merge with exchange rates on order_placement_date
full_df = orders_customers.merge(
    exchange_rates_slim,
    left_on="order_placement_date",
    right_on="date",        
    how="left",
    suffixes=("", "_er")     # overlapping columns from FX table get _er
)

# Drop the redundant right‑side key column if not needed
full_df = full_df.drop(columns=["date"], errors="ignore")

# ---------- 4. Calculate total_amount (INR) ----------

full_df["total_amount"] = 0.0
full_df["total_amount"] = full_df["total_amount"].astype("float64")

# Convert prices and rates to numeric
full_df["price_USD"] = pd.to_numeric(full_df["price_USD"], errors="coerce")
full_df["price_INR"] = pd.to_numeric(full_df["price_INR"], errors="coerce")
full_df["USD_INR_rate"] = pd.to_numeric(full_df["USD_INR_rate"], errors="coerce")
full_df["order_qty"] = pd.to_numeric(full_df["order_qty"], errors="coerce")

# USD rows: where price_USD exists
usd_mask = full_df["price_USD"].notna()
full_df.loc[usd_mask, "total_amount"] = (
    full_df.loc[usd_mask, "price_USD"]
    * full_df.loc[usd_mask, "USD_INR_rate"] 
    * full_df.loc[usd_mask, "order_qty"]
)

# INR rows: where price_USD is null but price_INR exists
inr_mask = full_df["price_USD"].isna() & full_df["price_INR"].notna()
full_df.loc[inr_mask, "total_amount"] = (
    full_df.loc[inr_mask, "price_INR"]
    * full_df.loc[inr_mask, "order_qty"]
)

# ---------- 5. Final cleanup + select requested columns ----------

columns_to_drop = ["price_USD", "price_INR", "USD_INR_rate", "date", "date"]
final_df = full_df.drop(
    columns=[c for c in columns_to_drop if c in full_df.columns],
    errors="ignore"
)

desired_cols = [
    "order_id",
    "order_placement_date",
    "customer_id",
    "product_id",
    "product_name",
    "category",
    "order_qty",
    "agreed_delivery_date",
    "actual_delivery_date",
    "delivery_qty",
    "In Full",
    "On Time",
    "On Time In Full",
    "total_amount"
]
desired_cols = [c for c in desired_cols if c in final_df.columns]
final_df = final_df[desired_cols]

final_df
