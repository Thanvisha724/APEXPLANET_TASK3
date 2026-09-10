from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "output" / "sales_clean.csv"
OUTPUT = ROOT / "output" / "sales_dashboard.png"

BG = "#F5F7FA"
INK = "#102A43"
MUTED = "#627D98"
TEAL = "#0F766E"
BLUE = "#2563EB"
AMBER = "#F59E0B"
RED = "#DC2626"
GRID = "#D9E2EC"


def money(value: float) -> str:
    return f"{value / 1_000_000:.1f}M"


def compact_value(value: float) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    return f"{value / 1_000:.1f}K"


def main() -> None:
    data = pd.read_csv(SOURCE, parse_dates=["Order_Date"])
    data["Month"] = data["Order_Date"].dt.to_period("M").astype(str)

    total_sales = data["Total_Sales"].sum()
    orders = data["Order_ID"].nunique()
    customers = data["Customer_ID"].nunique()
    units = data["Quantity"].sum()
    average_order = total_sales / orders

    monthly = data.groupby("Month", sort=True)["Total_Sales"].sum()
    category = data.groupby("Category")["Total_Sales"].sum().sort_values()
    product = data.groupby("Product")["Total_Sales"].sum().sort_values()
    city = data.groupby("City")["Total_Sales"].sum().sort_values()
    gender = data.groupby("Gender")["Total_Sales"].sum()

    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titleweight": "bold"})
    figure = plt.figure(figsize=(16, 9), facecolor=BG)
    grid = figure.add_gridspec(12, 24, left=0.04, right=0.97, top=0.92, bottom=0.07, hspace=1.35, wspace=1.5)

    figure.text(0.04, 0.955, "APEXPLANET SALES PULSE", fontsize=23, fontweight="bold", color=INK)
    figure.text(0.04, 0.928, "Executive dashboard | Data through 01 Jan 2026", fontsize=10, color=MUTED)
    figure.text(0.97, 0.95, "LIVE DATA REFRESH", fontsize=9, fontweight="bold", color=TEAL, ha="right")

    cards = [
        ("TOTAL SALES", money(total_sales), TEAL),
        ("DISTINCT ORDERS", f"{orders:,}", BLUE),
        ("CUSTOMERS", f"{customers:,}", AMBER),
        ("UNITS SOLD", f"{units:,}", RED),
        ("AVG ORDER VALUE", compact_value(average_order), TEAL),
    ]
    for index, (label, value, color) in enumerate(cards):
        left = 0.04 + index * 0.19
        axis = figure.add_axes([left, 0.835, 0.17, 0.07])
        axis.set_facecolor("white")
        axis.set_xticks([])
        axis.set_yticks([])
        for spine in axis.spines.values():
            spine.set_visible(False)
        axis.add_patch(plt.Rectangle((0, 0), 0.018, 1, transform=axis.transAxes, color=color, clip_on=False))
        axis.text(0.08, 0.68, label, fontsize=8, fontweight="bold", color=MUTED, transform=axis.transAxes)
        axis.text(0.08, 0.24, value, fontsize=17, fontweight="bold", color=INK, transform=axis.transAxes)

    def style_axis(axis, title):
        axis.set_facecolor("white")
        axis.set_title(title, loc="left", fontsize=12, color=INK, pad=12)
        axis.grid(axis="y", color=GRID, linewidth=0.8)
        axis.set_axisbelow(True)
        axis.tick_params(colors=MUTED, labelsize=8)
        for spine in axis.spines.values():
            spine.set_visible(False)

    trend_axis = figure.add_subplot(grid[3:8, :13])
    style_axis(trend_axis, "Monthly sales trend")
    trend_axis.plot(monthly.index, monthly.values / 1_000_000, color=TEAL, linewidth=2.8, marker="o", markersize=4)
    trend_axis.fill_between(range(len(monthly)), monthly.values / 1_000_000, color=TEAL, alpha=0.10)
    trend_axis.set_ylabel("Sales ($M)", color=MUTED, fontsize=8)
    trend_axis.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}"))
    trend_axis.set_xticks(range(len(monthly)))
    trend_axis.set_xticklabels(monthly.index, rotation=45, ha="right", fontsize=7)
    trend_axis.axvline(len(monthly) - 1, color=AMBER, linestyle="--", linewidth=1.2)
    trend_axis.text(len(monthly) - 1, monthly.iloc[-1] / 1_000_000, " partial month", color=AMBER, fontsize=8, va="bottom")

    category_axis = figure.add_subplot(grid[3:8, 14:])
    style_axis(category_axis, "Sales by category")
    category_axis.barh(category.index, category.values / 1_000_000, color=[TEAL, BLUE, AMBER, RED, "#7C3AED"])
    category_axis.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:.0f}M"))
    category_axis.tick_params(axis="y", labelsize=8)
    category_axis.set_xlabel("Sales", color=MUTED, fontsize=8)

    product_axis = figure.add_subplot(grid[8:12, :8])
    style_axis(product_axis, "Product ranking")
    product_axis.barh(product.index, product.values / 1_000_000, color=BLUE)
    product_axis.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:.0f}M"))
    product_axis.tick_params(axis="y", labelsize=8)

    city_axis = figure.add_subplot(grid[8:12, 9:17])
    style_axis(city_axis, "Sales by city")
    city_axis.barh(city.index, city.values / 1_000_000, color=TEAL)
    city_axis.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:.0f}M"))
    city_axis.tick_params(axis="y", labelsize=7)

    gender_axis = figure.add_subplot(grid[8:12, 18:])
    gender_axis.set_facecolor("white")
    gender_axis.set_title("Sales by gender", loc="left", fontsize=12, color=INK, pad=12)
    gender_axis.pie(gender.values, labels=gender.index, autopct="%1.0f%%", startangle=90, colors=[BLUE, AMBER], textprops={"color": INK, "fontsize": 8}, wedgeprops={"width": 0.42, "edgecolor": "white"})
    gender_axis.text(0, 0, money(total_sales), ha="center", va="center", fontsize=12, fontweight="bold", color=INK)

    figure.text(0.04, 0.025, "Source: ApexPlanet_DataAnalytics_Dataset (1).xlsx | Distinct orders used for order KPI | January 2026 is incomplete", fontsize=8, color=MUTED)
    OUTPUT.parent.mkdir(exist_ok=True)
    figure.savefig(OUTPUT, dpi=180, facecolor=BG)
    plt.close(figure)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
