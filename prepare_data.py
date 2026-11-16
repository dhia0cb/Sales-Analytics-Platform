
import pandas as pd
from pathlib import Path

from src.cleaning import clean_sales_data
from src.database import save_sales_data


BASE_DIR = Path(__file__).resolve().parent

RAW_PATH = (
    BASE_DIR / "data" / "raw" / "sales_raw.csv"
)

PROCESSED_PATH = (
    BASE_DIR / "data" / "processed" / "sales_clean.csv"
)


def main():

    print("Loading raw dataset...")

    raw_df = pd.read_csv(RAW_PATH)

    print(f"Raw rows: {len(raw_df)}")

    print("\nCleaning dataset...")

    clean_df = clean_sales_data(raw_df)

    print(f"Clean rows: {len(clean_df)}")

    print("\nSaving processed CSV...")

    PROCESSED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    clean_df.to_csv(
        PROCESSED_PATH,
        index=False
    )

    print("\nSaving database...")

    save_sales_data(clean_df)

    print("\nData preparation completed!")

    print("\nFinal dataset preview:")
    print(clean_df.head())

    print("\nFinal dataset information:")
    print(clean_df.info())


if __name__ == "__main__":
    main()
