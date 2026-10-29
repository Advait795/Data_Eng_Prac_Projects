from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT/"data"/"raw"/"OnlineRetail.csv"

def load_raw_data() -> pd.DataFrame:
    df = pd.read_csv(
        RAW_DATA_PATH,
        encoding="ISO-8859-1"
    )
    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["InvoiceDate"] = pd.to_datetime(
            df["InvoiceDate"],
            format="%m/%d/%Y %H:%M",
            errors = "raise"
        )
    
    df["LineRevenue"] = df["Quantity"] * df["UnitPrice"]

    df["customer_id_missing"] = df["CustomerID"].isna()
    df["description_missing"] = df["Description"].isna()         
    
    return  df

def validate_data(
        df: pd.DataFrame,
        expected_row_count: int | None = None
) -> None :
        if expected_row_count is not None:
            assert len(df) == 541909, "Row count has changed"
        
        assert df["InvoiceDate"].notna().all(), "Missing dates found"
        
        assert(
            df["LineRevenue"] == df["Quantity"] * df["UnitPrice"]
        ).all(), "Revenue calculation mismatch"


def main():
    df = load_raw_data()
    df = transform_data(df)

    validate_data(df, expected_row_count=541909)

    OUTPUT_DIR = PROJECT_ROOT/"data"/"processed"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    OUTPUT_PATH = OUTPUT_DIR/"online_retail_transformed.csv"
    df.to_csv(OUTPUT_PATH, index=False)

    saved_df = pd.read_csv(
        OUTPUT_PATH,
        encoding="utf-8",
        parse_dates=["InvoiceDate"]
    )

    assert len(saved_df) == len(df), "Saved row count mismatch."
    assert saved_df.columns.tolist() == df.columns.tolist(), "Column mismatch"


    print(f"Rows loaded: {len(df):,}" )
    print(f"Columns: {list(df.columns)}")
    print(f"InvoiceDate type: {df['InvoiceDate'].dtype}")
    print(df[["Quantity", "UnitPrice", "LineRevenue"]].head())
    print("All validation checks passed.")

    print("\nMissing CustomerID:", df["customer_id_missing"].sum())
    print("Missing Description:", df["description_missing"].sum())
    print("Total rows:", len(df))

    print(f"\nTransformed data saved to: {OUTPUT_PATH}")

    print("\nOutput validation passed.")
    print(f"Saved rows: {len(saved_df):,}")

if __name__ == "__main__":
    main()