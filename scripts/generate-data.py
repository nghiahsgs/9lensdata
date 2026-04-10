"""
generate-data.py — Generate TechMart e-commerce datasets for "9 Lens Data Analysis" book.

Outputs (chapter-based paths):
  chapters/01-ngay-dau-tien/data/techmart-orders-mar2024.csv        — 12,847 rows (Ch.1)
  chapters/02-thang-3-giam/data/techmart-orders-full2024.csv        — Jan–Sep 2024 + T3/2023
  chapters/03-khach-hang-quan-trong/data/techmart-customers.csv     — 28,000 customers + RFM
  chapters/04-correlation-volatility/data/techmart-marketing-campaigns.csv — ~500 campaigns
  chapters/05-ke-chuyen-dung-nguoi/data/techmart-finance-monthly.csv — 18 monthly P&L rows
  chapters/05-ke-chuyen-dung-nguoi/data/techmart-operations-daily.csv — ~273 daily ops rows

Usage:
  .venv/bin/python3 scripts/generate-data.py
"""

import sys
import os

# Ensure scripts/ dir is importable as package sibling
sys.path.insert(0, os.path.dirname(__file__))

from pathlib import Path
from shared.data_generators import (
    generate_mar2024_orders,
    generate_full2024_orders,
    generate_customers,
)
from shared.data_generators_extra import (
    generate_marketing_campaigns,
    generate_finance_monthly,
    generate_operations_daily,
)

ROOT = Path(__file__).parent.parent
CHAPTERS = ROOT / "chapters"
DATA_CH01 = CHAPTERS / "01-ngay-dau-tien" / "data"
DATA_CH02 = CHAPTERS / "02-thang-3-giam" / "data"
DATA_CH03 = CHAPTERS / "03-khach-hang-quan-trong" / "data"
DATA_CH04 = CHAPTERS / "04-correlation-volatility" / "data"
DATA_CH05 = CHAPTERS / "05-ke-chuyen-dung-nguoi" / "data"


def main() -> None:
    for d in [DATA_CH01, DATA_CH02, DATA_CH03, DATA_CH04, DATA_CH05]:
        d.mkdir(parents=True, exist_ok=True)

    print("Generating chapters/01-ngay-dau-tien/data/techmart-orders-mar2024.csv ...")
    mar = generate_mar2024_orders(12_847)
    out = DATA_CH01 / "techmart-orders-mar2024.csv"
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

    print("\nGenerating chapters/02-thang-3-giam/data/techmart-orders-full2024.csv ...")
    full = generate_full2024_orders()
    out2 = DATA_CH02 / "techmart-orders-full2024.csv"
    full.to_csv(out2, index=False, encoding="utf-8-sig")
    monthly = full.groupby(full["order_date"].dt.to_period("M")).size()
    print(f"  -> {len(full):,} rows written to {out2}")
    print(f"     Months covered: {sorted(full['order_date'].dt.to_period('M').unique())}")

    print("\nGenerating chapters/03-khach-hang-quan-trong/data/techmart-customers.csv ...")
    cust = generate_customers(28_000)
    out3 = DATA_CH03 / "techmart-customers.csv"
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

    print("\nGenerating chapters/04-correlation-volatility/data/techmart-marketing-campaigns.csv ...")
    mkt = generate_marketing_campaigns(500)
    out4 = DATA_CH04 / "techmart-marketing-campaigns.csv"
    mkt.to_csv(out4, index=False, encoding="utf-8-sig")
    print(f"  -> {len(mkt):,} rows written to {out4}")
    channel_roas = mkt.groupby("channel")["roas"].mean().round(2)
    print(f"     Avg ROAS by channel:\n{channel_roas.to_string()}")
    failed_campaigns = (mkt["roas"] < 1.0).sum()
    print(f"     Failed campaigns (ROAS < 1.0): {failed_campaigns}")

    print("\nGenerating chapters/05-ke-chuyen-dung-nguoi/data/techmart-finance-monthly.csv ...")
    fin = generate_finance_monthly()
    out5 = DATA_CH05 / "techmart-finance-monthly.csv"
    fin.to_csv(out5, index=False, encoding="utf-8-sig")
    print(f"  -> {len(fin):,} rows written to {out5}")
    fin2024 = fin[fin["year"] == 2024]
    avg_gm = fin2024["gross_margin_pct"].mean()
    avg_om = fin2024["operating_margin_pct"].mean()
    print(f"     2024 avg gross margin: {avg_gm:.1f}%")
    print(f"     2024 avg operating margin: {avg_om:.1f}%")

    print("\nGenerating chapters/05-ke-chuyen-dung-nguoi/data/techmart-operations-daily.csv ...")
    ops = generate_operations_daily()
    out6 = DATA_CH05 / "techmart-operations-daily.csv"
    ops.to_csv(out6, index=False, encoding="utf-8-sig")
    print(f"  -> {len(ops):,} rows written to {out6}")
    print(f"     Date range: {ops['date'].min()} to {ops['date'].max()}")
    jul_return = ops[ops["date"].str.startswith("2024-07")]["return_rate_pct"].mean()
    print(f"     Jul avg return rate: {jul_return:.1f}% (expect spike)")
    nps_first = ops["nps_score"].iloc[:30].mean()
    nps_last = ops["nps_score"].iloc[-30:].mean()
    print(f"     NPS first 30d avg: {nps_first:.1f}, last 30d avg: {nps_last:.1f} (expect decline)")

    print("\nAll datasets generated successfully.")

    # File summary
    print("\n── File Summary ─────────────────────────────────────────────")
    for data_dir in [DATA_CH01, DATA_CH02, DATA_CH03, DATA_CH04, DATA_CH05]:
        for csv_path in sorted(data_dir.glob("techmart-*.csv")):
            size_kb = csv_path.stat().st_size // 1024
            rel = csv_path.relative_to(ROOT)
            print(f"  {str(rel):<65} {size_kb:>5} KB")


if __name__ == "__main__":
    main()
