"""
generate-charts.py — Generate all 11 lens charts for "9 Lens Data Analysis" book.

Reads CSVs from chapter data/ folders, outputs PNGs to chapter images/ folders.

Usage:
  .venv/bin/python3 scripts/generate-charts.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from shared.chart_helpers import (
    load_mar2024, load_full2024, load_customers,
    IMG_CH01, IMG_CH02, IMG_CH03, IMG_CH04, IMG_CH05,
)
from ch01.charts import (
    chart_01_completeness, chart_02_distribution,
    chart_02b_category_breakdown, chart_02c_city_breakdown,
    chart_02d_discount_and_status,
)
from ch02.charts import chart_03_timeline_outliers
from ch03.charts import chart_04_concentration, chart_07_segmentation
from ch04.charts import (
    load_marketing, chart_05_correlation, chart_08_volatility, chart_09_marketing_correlation,
)
from ch05.charts import (
    load_finance, load_operations,
    chart_06_comparison, chart_10_finance_pl, chart_11_operations_dashboard,
)


def main() -> None:
    print("Loading datasets...")
    df_mar = load_mar2024()
    df_full = load_full2024()
    df_cust = load_customers()
    df_mkt = load_marketing()
    df_fin = load_finance()
    df_ops = load_operations()
    print(f"  mar2024:    {len(df_mar):,} rows")
    print(f"  full2024:   {len(df_full):,} rows")
    print(f"  customers:  {len(df_cust):,} rows")
    print(f"  marketing:  {len(df_mkt):,} rows")
    print(f"  finance:    {len(df_fin):,} rows")
    print(f"  operations: {len(df_ops):,} rows")

    charts = [
        ("chart-01-completeness",          lambda: chart_01_completeness(df_mar)),
        ("chart-02-distribution",          lambda: chart_02_distribution(df_mar)),
        ("chart-02b-category-breakdown",   lambda: chart_02b_category_breakdown(df_mar)),
        ("chart-02c-city-breakdown",       lambda: chart_02c_city_breakdown(df_mar)),
        ("chart-02d-discount-status",      lambda: chart_02d_discount_and_status(df_mar)),
        ("chart-03-timeline-outliers",     lambda: chart_03_timeline_outliers(df_full)),
        ("chart-04-concentration",         lambda: chart_04_concentration(df_mar, df_cust)),
        ("chart-05-correlation",           lambda: chart_05_correlation(df_mar, df_cust)),
        ("chart-06-comparison",            lambda: chart_06_comparison(df_full, df_mar)),
        ("chart-07-segmentation",          lambda: chart_07_segmentation(df_mar, df_cust)),
        ("chart-08-volatility",            lambda: chart_08_volatility(df_full)),
        ("chart-09-marketing-correlation", lambda: chart_09_marketing_correlation(df_mkt)),
        ("chart-10-finance-pl",            lambda: chart_10_finance_pl(df_fin)),
        ("chart-11-operations-dashboard",  lambda: chart_11_operations_dashboard(df_ops)),
    ]

    print(f"\nGenerating {len(charts)} charts -> chapters/*/images/\n")
    failed = []
    for name, fn in charts:
        print(f"Rendering {name} ...")
        try:
            fn()
        except Exception as exc:
            print(f"  ERROR: {exc}")
            failed.append((name, exc))

    print("\n── Summary ──────────────────────────────────────")
    img_dirs = [IMG_CH01, IMG_CH02, IMG_CH03, IMG_CH04, IMG_CH05]
    generated = sorted(p for d in img_dirs for p in d.glob("chart-*.png"))
    for p in generated:
        size_kb = p.stat().st_size // 1024
        print(f"  {p.name:<40} {size_kb:>5} KB")

    if failed:
        print(f"\nFailed ({len(failed)}):")
        for name, exc in failed:
            print(f"  {name}: {exc}")
        sys.exit(1)
    else:
        print(f"\nAll {len(charts)} charts generated successfully.")


if __name__ == "__main__":
    main()
