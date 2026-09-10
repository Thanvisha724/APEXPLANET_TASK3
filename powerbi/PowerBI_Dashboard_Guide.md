# Power BI Dashboard Build Guide

## 1. Load and model the data

1. Run `python scripts\\prepare_data.py`.
2. In Power BI Desktop, choose **Get data > Text/CSV** and select `output/sales_clean.csv`.
3. Rename the imported table to `Sales`.
4. Set data types:
   - `Order_Date`: Date
   - `Quantity`: Whole number
   - `Age`: Whole number
   - `Unit_Price`, `Total_Sales`: Decimal number
5. Create the `DateTable` from `measures.dax`.
6. Create a one-to-many relationship from `DateTable[Date]` to `Sales[Order_Date]`.
7. Mark `DateTable` as the date table using `DateTable[Date]`.
8. Sort `DateTable[Month]` by `DateTable[Month Number]`, and sort `DateTable[Year Month]` by the date column if needed.

## 2. Executive Overview page

Set the page title to **Sales Performance Overview**.

- KPI cards across the top: `Total Sales`, `Total Orders`, `Total Customers`, `Units Sold`, `Average Order Value`.
- Line chart: `DateTable[Year Month]` on the X-axis and `Total Sales` on the Y-axis.
- Clustered bar chart: `Sales[Category]` by `Total Sales`, sorted descending.
- Filled map or bar chart: `Sales[City]` by `Total Sales`.
- Donut chart: `Sales[Gender]` by `Total Sales`.
- Slicers: Date, Category, City, Product, Gender.

Use tooltips for `Total Orders`, `Units Sold`, and `Average Order Value`; keep the page focused on comparison and movement.

## 3. Product and Customer page

Set the page title to **Product and Customer Insights**.

- Horizontal bar chart: `Sales[Product]` by `Total Sales`, with data labels.
- Treemap: `Sales[Category]` and `Sales[Product]` by `Total Sales`.
- Matrix: `Sales[City]` > `Sales[Product]`, with `Total Sales`, `Units Sold`, and `Average Order Value`.
- Scatter chart: `Sales[Age]` on X, `Total Sales` on Y, `Quantity` as size, `Gender` as legend.
- Table: Customer name, city, order count, total sales, and average order value.
- Slicers: Category, Product, City, Gender, and Age.

## 4. Formatting standards

- Apply `powerbi/theme.json`.
- Use currency formatting with no decimals for sales and average order value.
- Use whole numbers for orders, customers, and units.
- Use percentage formatting for `Sales YoY %`.
- Keep visual titles short and descriptive; use consistent teal for primary measures and amber for highlights.
- Add a report-level filter to exclude blank `Order_ID` values if the source changes.

## 5. Recommended interactions

Enable cross-filtering from the category, product, city, and gender visuals into the KPI cards and monthly trend. Keep the date slicer as a Between slicer. Add a reset-filters bookmark if the report will be used by non-technical stakeholders.

## 6. Validation checklist

- Total Sales should be approximately `139,399,439.65` for the full dataset.
- Total Orders should be `992`.
- Total Customers should be `947`.
- Units Sold should equal the sum of `Quantity`.
- The monthly trend should include January 2025 through January 2026.
- Selecting a city or category should update the KPI cards and all charts.
