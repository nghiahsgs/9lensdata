"""
generate-charts.py — Generate all 8 lens charts for "9 Lens Data Analysis" book.

Reads from data/ CSVs, outputs PNG to images/.

Usage:
  .venv/bin/python3 scripts/generate-charts.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from chart_helpers import load_mar2024, load_full2024, load_customers, IMG_DIR
from charts_lens1_2 import chart_01_completeness, chart_02_distribution
from charts_lens3_4 import chart_03_timeline_outliers, chart_04_concentration
from charts_lens5_6 import chart_05_correlation, chart_06_comparison
from charts_lens7_8 import chart_07_segmentation, chart_08_volatility


def main() -> None:
    print("Loading datasets...")
    df_mar = load_mar2024()
    df_full = load_full2024()
    df_cust = load_customers()
    print(f"  mar2024:   {len(df_mar):,} rows")
    print(f"  full2024:  {len(df_full):,} rows")
    print(f"  customers: {len(df_cust):,} rows")

    charts = [
        ("chart-01-completeness",    lambda: chart_01_completeness(df_mar)),
        ("chart-02-distribution",    lambda: chart_02_distribution(df_mar)),
        ("chart-03-timeline-outliers", lambda: chart_03_timeline_outliers(df_full)),
        ("chart-04-concentration",   lambda: chart_04_concentration(df_mar, df_cust)),
        ("chart-05-correlation",     lambda: chart_05_correlation(df_mar, df_cust)),
        ("chart-06-comparison",      lambda: chart_06_comparison(df_full, df_mar)),
        ("chart-07-segmentation",    lambda: chart_07_segmentation(df_mar, df_cust)),
        ("chart-08-volatility",      lambda: chart_08_volatility(df_full)),
    ]

    print(f"\nGenerating {len(charts)} charts -> {IMG_DIR}/\n")
    failed = []
    for name, fn in charts:
        print(f"Rendering {name} ...")
        try:
            fn()
        except Exception as exc:
            print(f"  ERROR: {exc}")
            failed.append((name, exc))

    print("\n── Summary ──────────────────────────────────────")
    generated = sorted(IMG_DIR.glob("chart-*.png"))
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
