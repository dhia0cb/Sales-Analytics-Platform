
import sqlite3
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
    BASE_DIR / "database" / "sales.db"
)


def save_sales_data(df: pd.DataFrame):
    """
    Save cleaned sales data into SQLite.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with sqlite3.connect(DATABASE_PATH) as connection:

        df.to_sql(
            "sales",
            connection,
            if_exists="replace",
            index=False
        )

    print("Sales data saved to SQLite successfully!")


def load_sales_data() -> pd.DataFrame:
    """
    Retrieve sales data from SQLite.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        df = pd.read_sql_query(
            "SELECT * FROM sales",
            connection,
            parse_dates=["order_date"]
        )

    return df
