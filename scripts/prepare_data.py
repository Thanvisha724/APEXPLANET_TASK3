from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "ApexPlanet_DataAnalytics_Dataset (1).xlsx"
OUTPUT_DIR = ROOT / "output"
OUTPUT = OUTPUT_DIR / "sales_clean.csv"


def main() -> None:
    frame = pd.read_excel(SOURCE, sheet_name="Sales_Dataset")
    frame.columns = [column.strip() for column in frame.columns]
    frame["Order_Date"] = pd.to_datetime(frame["Order_Date"], errors="coerce")
    frame["City"] = frame["City"].fillna("Unknown")
    frame["Age"] = frame["Age"].fillna(frame["Age"].median()).round().astype("Int64")

    required = {
        "Order_ID", "Order_Date", "Customer_ID", "Customer_Name", "Age",
        "Gender", "City", "Product", "Category", "Quantity", "Unit_Price",
        "Total_Sales",
    }
    missing_columns = required.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {sorted(missing_columns)}")

    calculated_sales = (frame["Quantity"] * frame["Unit_Price"]).round(2)
    if not calculated_sales.equals(frame["Total_Sales"].round(2)):
        raise ValueError("Total_Sales does not match Quantity * Unit_Price")

    frame = frame.sort_values("Order_Date").reset_index(drop=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    frame.to_csv(OUTPUT, index=False, date_format="%Y-%m-%d")
    print(f"Wrote {len(frame):,} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
