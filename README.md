# ApexPlanet Sales Power BI Dashboard

This project prepares the supplied sales workbook for a Power BI sales-performance dashboard.

## Dashboard outcome

The recommended report contains:

- Executive overview: Total Sales, Total Orders, Total Customers, Units Sold, Average Order Value, and Sales YoY %.
- Trend analysis: monthly sales trend with category and city breakdowns.
- Product and customer analysis: product ranking, category contribution, customer segment, gender, and city filters.
- Deep-dive analysis: see [powerbi/Deep_Dive_Report.md](powerbi/Deep_Dive_Report.md) for findings, risks, opportunities, and decision questions.

The source data covers January 2025 through January 2026 and contains 1,000 rows. The preparation step fills missing cities with `Unknown`, fills missing ages with the dataset median, and verifies that `Total_Sales = Quantity * Unit_Price`.

## Quick start

1. Install Python dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Prepare the Power BI import file:

   ```powershell
   python scripts\prepare_data.py
   ```

3. Generate the current dashboard image:

   ```powershell
   python scripts\\create_dashboard_image.py
   ```

   The image is written to `output/sales_dashboard.png`.

4. Open Power BI Desktop and import `output/sales_clean.csv`.
5. Follow [powerbi/PowerBI_Dashboard_Guide.md](powerbi/PowerBI_Dashboard_Guide.md) to create the model and report pages.
6. Import [powerbi/theme.json](powerbi/theme.json) from **View > Themes > Browse for themes**.
7. Copy the measures from [powerbi/measures.dax](powerbi/measures.dax) into the model.

## Refresh workflow

Replace the workbook at `data/ApexPlanet_DataAnalytics_Dataset (1).xlsx`, run the preparation script again, and refresh the CSV source in Power BI. The validation step stops the export when required columns are missing or sales totals do not reconcile.

## Data dictionary

| Field | Meaning |
| --- | --- |
| `Order_ID` | Transaction identifier |
| `Order_Date` | Transaction date |
| `Customer_ID` / `Customer_Name` | Customer identifiers |
| `Age` / `Gender` | Customer demographics |
| `City` | Customer city |
| `Product` / `Category` | Product and merchandise grouping |
| `Quantity` | Units in the transaction |
| `Unit_Price` | Price per unit |
| `Total_Sales` | Transaction value |

## Requirements

- Power BI Desktop with permission to import CSV files and add DAX measures.
- Python 3.10 or newer for the optional preparation script.
- Packages listed in `requirements.txt`.
