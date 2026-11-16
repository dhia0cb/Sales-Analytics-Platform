
import pandas as pd


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw sales data and calculate business metrics """

    df = df.copy()

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Remove duplicate orders
    df = df.drop_duplicates(
        subset=["order_id"],
        keep="first"
    )

    # Convert dates
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    # Convert numerical columns
    numeric_columns = [
        "quantity",
        "unit_price",
        "unit_cost",
        "discount"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove records with missing critical information
    df = df.dropna(
        subset=[
            "order_id",
            "order_date",
            "product",
            "quantity",
            "unit_price",
            "unit_cost",
            "discount"
        ]
    )

    # Remove invalid values
    df = df[
        (df["quantity"] > 0)
        & (df["unit_price"] >= 0)
        & (df["unit_cost"] >= 0)
        & (df["discount"] >= 0)
        & (df["discount"] <= 1)
    ]

    # Fill missing categorical values
    categorical_columns = [
        "category",
        "region",
        "payment_method"
    ]

    for column in categorical_columns:
        df[column] = df[column].fillna("Unknown")

    # Calculate business metrics
    df["gross_sales"] = (
        df["quantity"] * df["unit_price"]
    )

    df["discount_amount"] = (
        df["gross_sales"] * df["discount"]
    )

    df["revenue"] = (
        df["gross_sales"] - df["discount_amount"]
    )

    df["total_cost"] = (
        df["quantity"] * df["unit_cost"]
    )

    df["profit"] = (
        df["revenue"] - df["total_cost"]
    )

    # Calculate profit margin safely
    df["profit_margin_pct"] = (
        df["profit"]
        .div(df["revenue"].replace(0, float("nan")))
        .mul(100)
    )

    # Add monthly grouping column
    df["order_month"] = (
        df["order_date"].dt.to_period("M").astype(str)
    )

    return df.reset_index(drop=True)
