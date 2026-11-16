
import pandas as pd

from src.cleaning import clean_sales_data


def test_duplicate_orders_are_removed():

    df = pd.DataFrame([
        {
            "order_id": "ORD-001",
            "order_date": "2024-01-01",
            "product": "Laptop",
            "category": "Electronics",
            "region": "North",
            "quantity": 2,
            "unit_price": 1000,
            "unit_cost": 700,
            "discount": 0.10,
            "payment_method": "Cash"
        },
        {
            "order_id": "ORD-001",
            "order_date": "2024-01-01",
            "product": "Laptop",
            "category": "Electronics",
            "region": "North",
            "quantity": 2,
            "unit_price": 1000,
            "unit_cost": 700,
            "discount": 0.10,
            "payment_method": "Cash"
        }
    ])

    result = clean_sales_data(df)

    assert len(result) == 1


def test_revenue_calculation():

    df = pd.DataFrame([
        {
            "order_id": "ORD-002",
            "order_date": "2024-01-01",
            "product": "Laptop",
            "category": "Electronics",
            "region": "North",
            "quantity": 2,
            "unit_price": 1000,
            "unit_cost": 700,
            "discount": 0.10,
            "payment_method": "Cash"
        }
    ])

    result = clean_sales_data(df)

    assert result.iloc[0]["revenue"] == 1800

    assert result.iloc[0]["profit"] == 400


def test_missing_region_is_replaced():

    df = pd.DataFrame([
        {
            "order_id": "ORD-003",
            "order_date": "2024-01-01",
            "product": "Laptop",
            "category": "Electronics",
            "region": None,
            "quantity": 2,
            "unit_price": 1000,
            "unit_cost": 700,
            "discount": 0.10,
            "payment_method": "Cash"
        }
    ])

    result = clean_sales_data(df)

    assert result.iloc[0]["region"] == "Unknown"
