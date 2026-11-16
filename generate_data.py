
import pandas as pd
import numpy as np
from pathlib import Path

# Reproducible random data
rng = np.random.default_rng(42)

# Project paths
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Products and their categories
products = {
    "Laptop": ("Electronics", 1200, 850),
    "Smartphone": ("Electronics", 800, 550),
    "Headphones": ("Electronics", 120, 55),
    "Keyboard": ("Accessories", 75, 30),
    "Mouse": ("Accessories", 40, 15),
    "Monitor": ("Electronics", 300, 190),
    "Office Chair": ("Furniture", 250, 140),
    "Desk": ("Furniture", 400, 240),
    "Notebook": ("Stationery", 8, 3),
    "Pen Set": ("Stationery", 15, 6),
}

regions = ["North", "South", "East", "West", "Central"]

payment_methods = [
    "Credit Card",
    "Cash",
    "Bank Transfer",
    "PayPal"
]

rows = []

# Generate 1000 orders
for i in range(1, 1001):

    product = rng.choice(list(products.keys()))

    category, unit_price, unit_cost = products[product]

    quantity = int(rng.integers(1, 9))

    discount = float(
        rng.choice([0, 0.05, 0.10, 0.15])
    )

    random_days = int(rng.integers(0, 730))

    order_date = (
        pd.Timestamp("2024-01-01")
        + pd.Timedelta(days=random_days)
    )

    rows.append({
        "order_id": f"ORD-{i:05d}",
        "order_date": order_date.strftime("%Y-%m-%d"),
        "customer_id": f"CUST-{int(rng.integers(1, 301)):04d}",
        "product": product,
        "category": category,
        "region": rng.choice(regions),
        "quantity": quantity,
        "unit_price": unit_price,
        "unit_cost": unit_cost,
        "discount": discount,
        "payment_method": rng.choice(payment_methods)
    })

df = pd.DataFrame(rows)

# Introduce missing values for cleaning practice
missing_indices = rng.choice(df.index, size=12, replace=False)

df.loc[missing_indices, "region"] = np.nan

# Introduce missing category values
missing_category_indices = rng.choice(
    df.index, size=8, replace=False
)

df.loc[missing_category_indices, "category"] = np.nan

# Introduce duplicate records
duplicates = df.sample(n=10, random_state=42)

df = pd.concat([df, duplicates], ignore_index=True)

# Save raw dataset
output_path = RAW_DIR / "sales_raw.csv"

df.to_csv(output_path, index=False)

print("Dataset generated successfully!")
print(f"Total rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved at: {output_path}")

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())
