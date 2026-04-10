"""
ch02_thang_3_giam/charts.py — Lens 3 (timeline + outliers) chart.
Chapter 02: Thang 3 Giam
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from shared.chart_helpers import save_fig, PALETTE, CAT_COLORS, vnd_formatter, IMG_CH02


def chart_03_timeline_outliers(df_full: pd.DataFrame) -> None:
    """Top: daily revenue with 21-day rolling mean + anomaly bands.
       Bottom: seasonal index by month."""
    daily = (
        df_full.groupby(df_full["order_date"].dt.date)["revenue"]
        .sum()
        .reset_index()
    )
    daily.columns = ["date", "revenue"]
    daily["date"] = pd.to_datetime(daily["date"])
    daily = daily.sort_values("date")
    daily["rolling21"] = daily["revenue"].rolling(21, center=True, min_periods=5).mean()
    daily["roll_std"] = daily["revenue"].rolling(21, center=True, min_periods=5).std()
    daily["upper"] = daily["rolling21"] + 2 * daily["roll_std"]
    daily["lower"] = daily["rolling21"] - 2 * daily["roll_std"]
    anomalies = daily[(daily["revenue"] > daily["upper"]) | (daily["revenue"] < daily["lower"])]

    # seasonal index: monthly avg revenue / overall avg
    df_full = df_full.copy()
    df_full["month"] = df_full["order_date"].dt.to_period("M")
    monthly_rev = df_full.groupby("month")["revenue"].sum()
    # only 2024 months for seasonal index
    monthly_2024 = monthly_rev[[m for m in monthly_rev.index if m.year == 2024]]
    seasonal_idx = monthly_2024 / monthly_2024.mean()

    month_labels_vi = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]

    fig, axes = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={"height_ratios": [2, 1]})
    fig.suptitle("Lens #3: TIMELINE & OUTLIERS — Xu hướng và điểm bất thường",
                 fontsize=14, fontweight="bold")

    # top: daily revenue
    ax = axes[0]
    ax.plot(daily["date"], daily["revenue"] / 1e6, color=PALETTE["primary"],
            alpha=0.5, linewidth=1, label="Doanh thu ngày")
    ax.plot(daily["date"], daily["rolling21"] / 1e6, color=PALETTE["secondary"],
            linewidth=2, label="Trung bình 21 ngày")
    ax.fill_between(daily["date"],
                    daily["lower"].fillna(0) / 1e6,
                    daily["upper"].fillna(0) / 1e6,
                    alpha=0.15, color=PALETTE["secondary"], label="Dải ±2σ")
    ax.scatter(anomalies["date"], anomalies["revenue"] / 1e6,
               color=PALETTE["negative"], zorder=5, s=60, label="Điểm bất thường")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}M"))
    ax.set_ylabel("Doanh thu (triệu VND)")
    ax.set_title("Doanh thu theo ngày với dải phát hiện bất thường")
    ax.legend(fontsize=9)
    ax.tick_params(axis="x", rotation=30)

    # bottom: seasonal index
    ax2 = axes[1]
    colors_s = [PALETTE["positive"] if v >= 1 else PALETTE["negative"]
                for v in seasonal_idx.values]
    bars = ax2.bar(range(len(seasonal_idx)), seasonal_idx.values, color=colors_s, alpha=0.85)
    ax2.axhline(1.0, color=PALETTE["neutral"], linestyle="--", linewidth=1)
    ax2.set_xticks(range(len(seasonal_idx)))
    ax2.set_xticklabels(month_labels_vi[:len(seasonal_idx)])
    ax2.set_ylabel("Chỉ số mùa vụ")
    ax2.set_title("Chỉ số mùa vụ theo tháng (2024)")
    for i, (bar, val) in enumerate(zip(bars, seasonal_idx.values)):
        ax2.text(bar.get_x() + bar.get_width() / 2, val + 0.02,
                 f"{val:.2f}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    save_fig(fig, "chart-03-timeline-outliers.png", img_dir=IMG_CH02)
