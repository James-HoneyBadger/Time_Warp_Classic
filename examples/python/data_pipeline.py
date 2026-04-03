#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════
DATA ANALYSIS PIPELINE
Complete data processing suite with statistical
analysis, trend detection, and formatted reporting
═══════════════════════════════════════════════════════
"""

import math
from collections import defaultdict

# ═══════════════════════════════════════
# DATA PROCESSING CLASSES
# ═══════════════════════════════════════

class DataTable:
    """Tabular data container with analysis methods"""

    def __init__(self, headers, rows):
        self.headers = headers
        self.rows = rows

    def column(self, name):
        """Extract a column by header name"""
        idx = self.headers.index(name)
        return [row[idx] for row in self.rows]

    def filter_rows(self, col_name, predicate):
        """Filter rows by column predicate"""
        idx = self.headers.index(col_name)
        return DataTable(self.headers,
                         [row for row in self.rows if predicate(row[idx])])

    def sort_by(self, col_name, reverse=False):
        """Sort rows by column"""
        idx = self.headers.index(col_name)
        sorted_rows = sorted(self.rows, key=lambda r: r[idx], reverse=reverse)
        return DataTable(self.headers, sorted_rows)

    def group_by(self, col_name):
        """Group rows by column value"""
        idx = self.headers.index(col_name)
        groups = defaultdict(list)
        for row in self.rows:
            groups[row[idx]].append(row)
        return {k: DataTable(self.headers, v) for k, v in groups.items()}

    def add_computed_column(self, name, func):
        """Add a new column computed from existing data"""
        new_headers = self.headers + [name]
        new_rows = [row + [func(dict(zip(self.headers, row)))] for row in self.rows]
        return DataTable(new_headers, new_rows)


class Stats:
    """Statistical functions"""

    @staticmethod
    def mean(data):
        return sum(data) / len(data) if data else 0

    @staticmethod
    def median(data):
        s = sorted(data)
        n = len(s)
        if n % 2 == 0:
            return (s[n // 2 - 1] + s[n // 2]) / 2
        return s[n // 2]

    @staticmethod
    def std_dev(data):
        m = Stats.mean(data)
        variance = sum((x - m) ** 2 for x in data) / len(data)
        return math.sqrt(variance)

    @staticmethod
    def percentile(data, p):
        s = sorted(data)
        idx = (p / 100) * (len(s) - 1)
        lower = int(idx)
        upper = min(lower + 1, len(s) - 1)
        weight = idx - lower
        return s[lower] * (1 - weight) + s[upper] * weight

    @staticmethod
    def correlation(x, y):
        mx, my = Stats.mean(x), Stats.mean(y)
        n = len(x)
        cov = sum((x[i] - mx) * (y[i] - my) for i in range(n)) / n
        sx = Stats.std_dev(x)
        sy = Stats.std_dev(y)
        return cov / (sx * sy) if sx * sy != 0 else 0

    @staticmethod
    def linear_trend(data):
        """Calculate linear trend (slope per unit)"""
        n = len(data)
        x_vals = list(range(n))
        mx = Stats.mean(x_vals)
        my = Stats.mean(data)
        num = sum((x_vals[i] - mx) * (data[i] - my) for i in range(n))
        den = sum((x_vals[i] - mx) ** 2 for i in range(n))
        slope = num / den if den != 0 else 0
        intercept = my - slope * mx
        return slope, intercept

    @staticmethod
    def moving_average(data, window):
        result = []
        for i in range(len(data)):
            start = max(0, i - window + 1)
            result.append(Stats.mean(data[start:i + 1]))
        return result


# ═══════════════════════════════════════
# SAMPLE DATA
# ═══════════════════════════════════════

# Monthly sales data for a retail company
sales_data = DataTable(
    ["Month", "Region", "Product", "Units", "Revenue", "Cost"],
    [
        ["Jan", "North", "Electronics", 150, 45000, 28000],
        ["Jan", "North", "Clothing",    200, 16000, 9000],
        ["Jan", "South", "Electronics", 120, 36000, 22000],
        ["Jan", "South", "Clothing",    180, 14400, 8100],
        ["Jan", "East",  "Electronics", 130, 39000, 24000],
        ["Jan", "East",  "Clothing",    160, 12800, 7200],
        ["Feb", "North", "Electronics", 165, 49500, 30000],
        ["Feb", "North", "Clothing",    210, 16800, 9500],
        ["Feb", "South", "Electronics", 135, 40500, 25000],
        ["Feb", "South", "Clothing",    195, 15600, 8800],
        ["Feb", "East",  "Electronics", 140, 42000, 26000],
        ["Feb", "East",  "Clothing",    170, 13600, 7700],
        ["Mar", "North", "Electronics", 180, 54000, 33000],
        ["Mar", "North", "Clothing",    230, 18400, 10400],
        ["Mar", "South", "Electronics", 145, 43500, 27000],
        ["Mar", "South", "Clothing",    205, 16400, 9300],
        ["Mar", "East",  "Electronics", 155, 46500, 28500],
        ["Mar", "East",  "Clothing",    185, 14800, 8400],
        ["Apr", "North", "Electronics", 195, 58500, 36000],
        ["Apr", "North", "Clothing",    245, 19600, 11000],
        ["Apr", "South", "Electronics", 160, 48000, 29500],
        ["Apr", "South", "Clothing",    215, 17200, 9700],
        ["Apr", "East",  "Electronics", 170, 51000, 31000],
        ["Apr", "East",  "Clothing",    200, 16000, 9100],
    ]
)


# ═══════════════════════════════════════
# ANALYSIS AND REPORTING
# ═══════════════════════════════════════

def main():
    print("=" * 62)
    print("          DATA ANALYSIS PIPELINE v1.0")
    print("=" * 62)
    print()

    # Add profit column
    data = sales_data.add_computed_column(
        "Profit", lambda r: r["Revenue"] - r["Cost"])
    data = data.add_computed_column(
        "Margin", lambda r: round((r["Revenue"] - r["Cost"]) / r["Revenue"] * 100, 1))

    # ─── Overview ───
    print("-" * 62)
    print("  DATASET OVERVIEW")
    print("-" * 62)
    all_revenue = data.column("Revenue")
    all_units = data.column("Units")
    all_profit = data.column("Profit")

    print(f"  Records:        {len(data.rows)}")
    print(f"  Total Revenue:  ${sum(all_revenue):,.0f}")
    print(f"  Total Units:    {sum(all_units):,}")
    print(f"  Total Profit:   ${sum(all_profit):,.0f}")
    print(f"  Avg Margin:     {Stats.mean(data.column('Margin')):.1f}%")
    print()

    # ─── Regional Breakdown ───
    print("-" * 62)
    print("  REGIONAL PERFORMANCE")
    print("-" * 62)
    print()
    print(f"  {'Region':<10s} {'Revenue':>12s} {'Profit':>10s} {'Margin':>8s} {'Units':>8s}")
    print("  " + "-" * 50)

    regions = data.group_by("Region")
    region_stats = []
    for region_name in sorted(regions.keys()):
        rdata = regions[region_name]
        rev = sum(rdata.column("Revenue"))
        prof = sum(rdata.column("Profit"))
        margin = prof / rev * 100 if rev else 0
        units = sum(rdata.column("Units"))
        region_stats.append((region_name, rev, prof, margin, units))
        print(f"  {region_name:<10s} ${rev:>10,}  ${prof:>8,}  {margin:>6.1f}%  {units:>6,}")

    print()

    # Bar chart
    print("  Revenue by Region:")
    max_rev = max(r[1] for r in region_stats)
    for name, rev, _, _, _ in region_stats:
        bar = "#" * int(rev / max_rev * 35)
        print(f"    {name:<8s} {bar} ${rev:,}")
    print()

    # ─── Product Analysis ───
    print("-" * 62)
    print("  PRODUCT LINE ANALYSIS")
    print("-" * 62)
    print()

    products = data.group_by("Product")
    for prod_name in sorted(products.keys()):
        pdata = products[prod_name]
        rev = sum(pdata.column("Revenue"))
        cost = sum(pdata.column("Cost"))
        profit = rev - cost
        units = sum(pdata.column("Units"))
        avg_price = rev / units if units else 0
        margin = profit / rev * 100 if rev else 0

        print(f"  {prod_name}:")
        print(f"    Revenue:     ${rev:>10,}")
        print(f"    Cost:        ${cost:>10,}")
        print(f"    Profit:      ${profit:>10,}")
        print(f"    Units Sold:  {units:>10,}")
        print(f"    Avg Price:   ${avg_price:>10,.2f}")
        print(f"    Margin:      {margin:>9.1f}%")
        print()

    # ─── Monthly Trends ───
    print("-" * 62)
    print("  MONTHLY TREND ANALYSIS")
    print("-" * 62)
    print()

    months = data.group_by("Month")
    month_order = ["Jan", "Feb", "Mar", "Apr"]
    monthly_revenue = []
    monthly_profit = []

    print(f"  {'Month':<8s} {'Revenue':>12s} {'Profit':>10s} {'Units':>8s} {'Margin':>8s}")
    print("  " + "-" * 48)

    for month in month_order:
        if month in months:
            mdata = months[month]
            rev = sum(mdata.column("Revenue"))
            prof = sum(mdata.column("Profit"))
            units = sum(mdata.column("Units"))
            margin = prof / rev * 100 if rev else 0
            monthly_revenue.append(rev)
            monthly_profit.append(prof)
            print(f"  {month:<8s} ${rev:>10,}  ${prof:>8,}  {units:>6,}  {margin:>6.1f}%")

    print()

    # Trend analysis
    rev_slope, rev_intercept = Stats.linear_trend(monthly_revenue)
    prof_slope, _ = Stats.linear_trend(monthly_profit)

    print("  Trend Analysis:")
    print(f"    Revenue trend:  ${rev_slope:+,.0f} per month")
    print(f"    Profit trend:   ${prof_slope:+,.0f} per month")
    print(f"    Direction:      {'Upward' if rev_slope > 0 else 'Downward'}")
    print()

    # Forecast
    print("  5-Month Forecast (linear projection):")
    forecast_months = ["May", "Jun", "Jul", "Aug", "Sep"]
    for i, month in enumerate(forecast_months):
        idx = len(monthly_revenue) + i
        forecast = rev_intercept + rev_slope * idx
        print(f"    {month}: ${forecast:>10,.0f}")
    print()

    # ─── Statistical Summary ───
    print("-" * 62)
    print("  STATISTICAL SUMMARY")
    print("-" * 62)
    print()

    for col_name in ["Revenue", "Units", "Profit"]:
        col_data = data.column(col_name)
        prefix = "$" if col_name != "Units" else ""

        print(f"  {col_name}:")
        print(f"    Mean:      {prefix}{Stats.mean(col_data):>10,.1f}")
        print(f"    Median:    {prefix}{Stats.median(col_data):>10,.1f}")
        print(f"    Std Dev:   {prefix}{Stats.std_dev(col_data):>10,.1f}")
        print(f"    Min:       {prefix}{min(col_data):>10,}")
        print(f"    Max:       {prefix}{max(col_data):>10,}")
        print(f"    Q1 (25%):  {prefix}{Stats.percentile(col_data, 25):>10,.1f}")
        print(f"    Q3 (75%):  {prefix}{Stats.percentile(col_data, 75):>10,.1f}")
        print()

    # ─── Correlation Matrix ───
    print("-" * 62)
    print("  CORRELATION MATRIX")
    print("-" * 62)
    print()

    numeric_cols = ["Units", "Revenue", "Cost", "Profit"]
    print(f"  {'':>12s}", end="")
    for col in numeric_cols:
        print(f"  {col:>10s}", end="")
    print()
    print("  " + "-" * 54)

    for col1 in numeric_cols:
        print(f"  {col1:>10s}  ", end="")
        for col2 in numeric_cols:
            r = Stats.correlation(data.column(col1), data.column(col2))
            print(f"  {r:>10.4f}", end="")
        print()
    print()

    # ─── Top Performers ───
    print("-" * 62)
    print("  TOP PERFORMERS")
    print("-" * 62)
    print()

    sorted_data = data.sort_by("Profit", reverse=True)
    print("  Top 5 by Profit:")
    print(f"  {'Month':<6s} {'Region':<8s} {'Product':<14s} {'Revenue':>10s} {'Profit':>10s} {'Margin':>7s}")
    print("  " + "-" * 58)
    for row in sorted_data.rows[:5]:
        d = dict(zip(sorted_data.headers, row))
        print(f"  {d['Month']:<6s} {d['Region']:<8s} {d['Product']:<14s} ${d['Revenue']:>9,} ${d['Profit']:>9,} {d['Margin']:>5.1f}%")

    print()
    print("  Bottom 5 by Margin:")
    sorted_margin = data.sort_by("Margin")
    for row in sorted_margin.rows[:5]:
        d = dict(zip(sorted_margin.headers, row))
        print(f"  {d['Month']:<6s} {d['Region']:<8s} {d['Product']:<14s} ${d['Revenue']:>9,} ${d['Profit']:>9,} {d['Margin']:>5.1f}%")

    print()
    print("=" * 62)
    print("  Data Analysis Pipeline Complete")
    print(f"  Processed {len(data.rows)} records across {len(data.headers)} dimensions")
    print("=" * 62)


if __name__ == "__main__":
    main()
