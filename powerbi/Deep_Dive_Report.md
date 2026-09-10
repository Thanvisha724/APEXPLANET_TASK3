# ApexPlanet Sales Deep-Dive Report

## Executive summary

The dataset contains 1,000 transaction rows, 992 distinct orders, 947 customers, and total sales of **139,399,439.65**. Electronics is the dominant category, producing **36.4%** of sales. Laptop and Mobile are the two largest products, while sales are geographically well distributed across the named cities. Male customers contribute a modest majority of sales at **52.0%**.

The most important interpretation caution is time completeness: the data runs from 2025-01-01 through 2026-01-01, but January 2026 contains only five orders. January 2026 should therefore be treated as a partial period, not compared directly with full months.

## 1. Business performance

| Metric | Result |
| --- | ---: |
| Transaction rows | 1,000 |
| Distinct orders | 992 |
| Distinct customers | 947 |
| Total sales | 139,399,439.65 |
| Average order value | 140,523.63 |
| Units sold | 5,435 |
| Sales per unit | 25,648.47 |
| Date coverage | 2025-01-01 to 2026-01-01 |

The difference between transaction rows and distinct orders means `Order_ID` should be counted with `DISTINCTCOUNT` in Power BI. Summing rows as orders would overstate order volume by eight records.

## 2. Time analysis

The strongest complete months are:

- **March 2025:** 13,059,899.94 in sales across 89 orders.
- **June 2025:** 12,912,332.64 across 83 orders.
- **November 2025:** 12,627,620.22 across 76 orders.

The weakest complete months are September 2025 at 9,179,896.29 and August 2025 at 9,448,471.22. January 2026 recorded 809,389.99 from only five orders and should be excluded from full-month ranking until the period is complete.

**Dashboard implication:** use a monthly line chart with a clear partial-period indicator. Add a date slicer and avoid presenting January 2026 as a normal month in executive comparisons.

## 3. Category performance

| Category | Sales | Share | Orders | Units |
| --- | ---: | ---: | ---: | ---: |
| Electronics | 50,778,581.70 | 36.4% | 353 | 1,978 |
| Education | 25,031,689.40 | 18.0% | 177 | 977 |
| Grocery | 22,231,711.28 | 15.9% | 151 | 826 |
| Furniture | 21,521,561.48 | 15.4% | 158 | 855 |
| Fashion | 19,835,895.79 | 14.2% | 156 | 799 |

Electronics generates more than twice the sales of any other category and accounts for approximately 1.8 times its nearest category, Education. It is the clearest commercial growth and risk focus: strong performance can lift the entire business, but concentration creates exposure if electronics demand weakens.

**Recommended action:** monitor electronics by product and city, and test whether high electronics sales are driven by price, volume, or a small number of large orders.

## 4. Product performance

| Product | Category | Sales | Share | Orders |
| --- | --- | ---: | ---: | ---: |
| Laptop | Electronics | 25,443,008.51 | 18.3% | 170 |
| Mobile | Electronics | 25,335,573.19 | 18.2% | 184 |
| Book | Education | 25,031,689.40 | 18.0% | 177 |
| Rice | Grocery | 22,231,711.28 | 15.9% | 151 |
| Chair | Furniture | 21,521,561.48 | 15.4% | 158 |
| Shoes | Fashion | 19,835,895.79 | 14.2% | 156 |

The top three products contribute 54.5% of total sales. Laptop and Mobile together account for 36.4%, exactly matching the electronics category share because they are the category's two products in this dataset. Book is the strongest non-electronics product.

**Recommended action:** use product-level drill-through in Power BI and compare units, unit price, and order value together. Sales rank alone cannot show whether a product is winning through volume or price.

## 5. Geographic performance

| City | Sales | Share | Orders |
| --- | ---: | ---: | ---: |
| Patna | 19,285,966.89 | 13.8% | 135 |
| Kolkata | 18,884,349.57 | 13.6% | 132 |
| Bengaluru | 18,773,574.32 | 13.5% | 120 |
| Mumbai | 18,757,050.17 | 13.5% | 131 |
| Hyderabad | 17,166,766.87 | 12.3% | 125 |
| Delhi | 16,097,079.00 | 11.6% | 125 |
| Pune | 14,513,175.90 | 10.4% | 98 |
| Gaya | 14,380,859.39 | 10.3% | 117 |
| Unknown | 1,540,617.54 | 1.1% | 13 |

Named-city performance is relatively balanced: the top city, Patna, contributes only 13.8%, while the lowest named city, Gaya, contributes 10.3%. This suggests there is no single-city dependency. `Unknown` is small but should remain visible in the data-quality view rather than being silently discarded.

**Recommended action:** use city as a filter and compare city-category combinations. A city that is average overall may still be especially strong or weak for Electronics, Fashion, or Furniture.

## 6. Customer and demographic analysis

Male customers contribute 72,463,550.63, or 52.0% of sales. Female customers contribute 66,935,889.02, or 48.0%. The difference is meaningful but not large enough to justify gender-only targeting.

Sales by age band:

| Age band | Sales | Customers |
| --- | ---: | ---: |
| 18-25 | 22,284,096.94 | 158 |
| 26-35 | 29,632,336.96 | 217 |
| 36-45 | 31,533,245.71 | 222 |
| 46-55 | 28,216,508.63 | 202 |
| 56-65 | 27,733,251.41 | 196 |

The 36-45 segment is the largest by sales, followed by 26-35. However, all age bands contribute substantial value, so the data supports differentiated messaging rather than excluding older or younger customers.

Customer concentration is low: the top 10 customers contribute only 4.2% of sales. Only 52 customers have more than one order, representing 5.5% of the customer base. This indicates a broad, mostly one-order customer population and creates an opportunity for retention, repeat purchase, and cross-sell programs.

## 7. Data-quality findings

- There are 8 duplicate `Order_ID` occurrences across the 1,000 rows. The dashboard therefore uses distinct orders rather than row count.
- There are 20 missing ages. The preparation script imputes them with the median age for reporting continuity.
- There are 13 missing cities. The preparation script labels them `Unknown` so sales are preserved and visible.
- `Total_Sales` reconciles to `Quantity * Unit_Price` for every row after rounding to two decimals.
- January 2026 is a partial month with five orders and should not be used as a full-period benchmark.

## 8. Decision questions for the dashboard

1. Is electronics growth coming from more units or higher prices?
2. Which cities have the strongest electronics and mobile/laptop performance?
3. Can repeat purchase activity be increased from the current 5.5% customer share?
4. Which categories perform best in the 26-45 age bands?
5. Are the March, June, and November peaks seasonal, campaign-driven, or driven by a few large orders?

## 9. Recommended Power BI additions

Add these visuals or report features to the main dashboard:

- A card showing data coverage and a warning for incomplete periods.
- A decomposition tree for Total Sales by Category, Product, City, and Gender.
- A scatter plot of average unit price versus units sold by product.
- A repeat-customer KPI using `DISTINCTCOUNT(Customer_ID)` filtered to customers with more than one order.
- A tooltip page showing sales, orders, units, average order value, and sales share for the selected segment.

## Method

All figures were calculated from `output/sales_clean.csv`, generated by `scripts/prepare_data.py`. Sales are summed from `Total_Sales`; orders and customers are distinct counts; missing city and age values use the preparation rules documented in the project README.
