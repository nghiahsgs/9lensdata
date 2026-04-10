"""
charts_lens3_4.py — Lens 3 (timeline + outliers) and Lens 4 (concentration) charts.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from chart_helpers import save_fig, PALETTE, CAT_COLORS, vnd_formatter, IMG_CH02, IMG_CH03


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


def chart_04_concentration(df_mar: pd.DataFrame, df_cust: pd.DataFrame) -> None:
    """Lorenz curve + Pareto SKU chart + Pie chart revenue by customer group."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle("Lens #4: CONCENTRATION — Quy luật tập trung 80/20",
                 fontsize=14, fontweight="bold")

    # 1. Lorenz curve (customer revenue distribution)
    cust_rev = df_cust["total_revenue"].sort_values().values
    n = len(cust_rev)
    cum_pop = np.linspace(0, 1, n)
    cum_rev = np.cumsum(cust_rev) / cust_rev.sum()
    ax = axes[0]
    ax.plot(cum_pop * 100, cum_rev * 100, color=PALETTE["primary"], linewidth=2,
            label="Đường Lorenz")
    ax.plot([0, 100], [0, 100], color=PALETTE["neutral"], linestyle="--",
            linewidth=1, label="Phân phối đều")
    # annotate top 20% = 78% revenue
    ax.axvline(80, color=PALETTE["accent"], linestyle=":", alpha=0.7)
    ax.axhline(22, color=PALETTE["accent"], linestyle=":", alpha=0.7)
    ax.text(55, 18, "Top 20% KH\n= 78% DT", fontsize=9,
            color=PALETTE["accent"], ha="center")
    ax.fill_between(cum_pop * 100, cum_pop * 100, cum_rev * 100,
                    alpha=0.12, color=PALETTE["primary"])
    ax.set_xlabel("% khách hàng (tích luỹ)")
    ax.set_ylabel("% doanh thu (tích luỹ)")
    ax.set_title("Đường Lorenz — Bất bình đẳng doanh thu")
    ax.legend(fontsize=9)

    # 2. Pareto SKU chart
    sku_rev = (
        df_mar.groupby("product_name")["revenue"].sum()
        .sort_values(ascending=False)
        .head(15)
    )
    cum_sku = sku_rev.cumsum() / sku_rev.sum() * 100
    ax2 = axes[1]
    bars = ax2.bar(range(len(sku_rev)), sku_rev.values / 1e6,
                   color=PALETTE["primary"], alpha=0.8)
    ax2_r = ax2.twinx()
    ax2_r.plot(range(len(sku_rev)), cum_sku.values, color=PALETTE["negative"],
               marker="o", markersize=4, linewidth=1.5, label="% tích luỹ")
    ax2_r.axhline(80, color=PALETTE["accent"], linestyle="--", alpha=0.7)
    ax2_r.set_ylabel("% doanh thu tích luỹ")
    ax2_r.set_ylim(0, 110)
    ax2.set_xticks(range(len(sku_rev)))
    ax2.set_xticklabels([s[:12] for s in sku_rev.index], rotation=45, ha="right", fontsize=7)
    ax2.set_ylabel("Doanh thu (triệu VND)")
    ax2.set_title("Phân tích Pareto — Top 15 SKU")

    # 3. Pie: revenue by customer segment
    seg_rev = df_cust.groupby("rfm_segment")["total_revenue"].sum()
    seg_rev = seg_rev.sort_values(ascending=False)
    colors_pie = CAT_COLORS[:len(seg_rev)]
    wedges, texts, autotexts = axes[2].pie(
        seg_rev.values, labels=seg_rev.index, autopct="%1.1f%%",
        colors=colors_pie, startangle=140,
        textprops={"fontsize": 8},
    )
    for at in autotexts:
        at.set_fontsize(7)
    axes[2].set_title("Doanh thu theo phân khúc khách hàng")

    plt.tight_layout()
    save_fig(fig, "chart-04-concentration.png", img_dir=IMG_CH03)
