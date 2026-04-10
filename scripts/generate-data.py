"""
generate-data.py — Generate TechMart e-commerce datasets for "9 Lens Data Analysis" book.

Outputs:
  data/techmart-orders-mar2024.csv   — 12,847 rows (Ch.1 main dataset)
  data/techmart-orders-full2024.csv  — Jan–Sep 2024 + T3/2023 (Ch.2 timeline)
  data/techmart-customers.csv        — 28,000 customers with RFM (Ch.3–4)

Usage:
  .venv/bin/python3 scripts/generate-data.py
"""

import sys
import os

# Ensure scripts/ dir is importable as package sibling
sys.path.insert(0, os.path.dirname(__file__))

from pathlib import Path
from data_generators import (
    generate_mar2024_orders,
    generate_full2024_orders,
    generate_customers,
)

DATA_DIR = Path(__file__).parent.parent / "data"


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating data/techmart-orders-mar2024.csv ...")
    mar = generate_mar2024_orders(12_847)
    out = DATA_DIR / "techmart-orders-mar2024.csv"
    mar.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"  -> {len(mar):,} rows written to {out}")

    # Sanity checks
    qty_zero = (mar["quantity"] == 0).sum()
    price_test = (mar["unit_price"] == 1_000).sum()
    missing_rating = mar["rating"].isna().mean()
    missing_quanhuyen = mar["quan_huyen"].isna().mean()
    cat_rev = mar.groupby("category")["revenue"].sum()
    elec_rev_share = cat_rev["Điện Tử"] / cat_rev.sum()
    qty1_share = (mar["quantity"] == 1).mean()
    print(f"     qty=0 rows: {qty_zero} (expect 3)")
    print(f"     unit_price=1000 rows: {price_test} (expect 1)")
    print(f"     rating missing: {missing_rating:.1%} (expect ~60%)")
    print(f"     quan_huyen missing: {missing_quanhuyen:.1%} (expect ~38%)")
    print(f"     Điện Tử revenue share: {elec_rev_share:.1%} (expect ~42%)")
    print(f"     qty=1 share: {qty1_share:.1%} (expect ~52%)")

    print("\nGenerating data/techmart-orders-full2024.csv ...")
    full = generate_full2024_orders()
    out2 = DATA_DIR / "techmart-orders-full2024.csv"
    full.to_csv(out2, index=False, encoding="utf-8-sig")
    monthly = full.groupby(full["order_date"].dt.to_period("M")).size()
    print(f"  -> {len(full):,} rows written to {out2}")
    print(f"     Months covered: {sorted(full['order_date'].dt.to_period('M').unique())}")

    print("\nGenerating data/techmart-customers.csv ...")
    cust = generate_customers(28_000)
    out3 = DATA_DIR / "techmart-customers.csv"
    cust.to_csv(out3, index=False, encoding="utf-8-sig")
    print(f"  -> {len(cust):,} rows written to {out3}")
    seg_counts = cust["rfm_segment"].value_counts()
    print(f"     Segment distribution:\n{seg_counts.to_string()}")

    # Simpson's Paradox retention check
    # Business retention (42%) = customers who made repeat purchase in period.
    # churn_risk is a 0-1 score; threshold 0.75 maps to ~42% "not at high risk".
    # This matches the book's narrative where overall=42%, TPHCM=38%, Other=52%.
    RETENTION_THRESHOLD = 0.75
    cust["retained"] = cust["churn_risk"] < RETENTION_THRESHOLD
    overall_ret = cust["retained"].mean()
    city_ret = cust.groupby("city")["retained"].mean()
    print(f"\n     Retention proxy (churn_risk < {RETENTION_THRESHOLD}):")
    print(f"       Overall: {overall_ret:.1%} (book target ~42%)")
    for city in ["TP.HCM", "Hà Nội", "Đà Nẵng"]:
        val = city_ret.get(city, 0)
        print(f"       {city}: {val:.1%}")

    print("\nAll datasets generated successfully.")


if __name__ == "__main__":
    main()
