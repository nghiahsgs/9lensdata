"""
ch03_khach_hang_quan_trong/charts.py — Lens 4 (concentration) and Lens 7 (segmentation) charts.
Chapter 03: Khach Hang Quan Trong
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from shared.chart_helpers import save_fig, PALETTE, CAT_COLORS, vnd_formatter, IMG_CH03


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


def chart_07_segmentation(df_mar: pd.DataFrame, df_cust: pd.DataFrame) -> None:
    """Revenue heatmap (City × Category) + RFM segment bubble map (separate rows)."""
    fig, axes = plt.subplots(2, 1, figsize=(14, 14),
                             gridspec_kw={"height_ratios": [1, 1.2]})
    fig.suptitle("Lens #7: SEGMENTATION — Phân tích theo nhóm và không gian",
                 fontsize=15, fontweight="bold")

    # 1. Revenue heatmap City × Category
    pivot = df_mar.pivot_table(
        values="revenue", index="city", columns="category", aggfunc="sum", fill_value=0
    )
    pivot_m = pivot / 1e6  # million VND
    sns.heatmap(
        pivot_m, ax=axes[0], annot=True, fmt=".0f", cmap="Blues",
        linewidths=0.5, cbar_kws={"label": "Doanh thu (triệu VND)"},
        annot_kws={"fontsize": 11},
    )
    axes[0].set_title("Doanh thu theo Thành phố × Danh mục (triệu VND) — Tháng 3/2024",
                      fontsize=12)
    axes[0].set_xlabel("Danh mục sản phẩm", fontsize=11)
    axes[0].set_ylabel("Thành phố", fontsize=11)
    axes[0].tick_params(axis="x", rotation=30, labelsize=10)
    axes[0].tick_params(axis="y", rotation=0, labelsize=10)

    # 2. RFM segment bubble map — LARGE
    seg_agg = df_cust.groupby("rfm_segment").agg(
        avg_aov=("avg_order_value", "mean"),
        avg_orders=("total_orders", "mean"),
        total_rev=("total_revenue", "sum"),
        count=("customer_id", "count"),
    ).reset_index()

    seg_colors = {
        "Champions":          CAT_COLORS[0],
        "Loyal":              CAT_COLORS[1],
        "Potential Loyalists": CAT_COLORS[2],
        "At Risk":            CAT_COLORS[3],
        "Hibernating":        CAT_COLORS[4],
        "Lost":               CAT_COLORS[5],
    }
    ax2 = axes[1]
    for _, row in seg_agg.iterrows():
        color = seg_colors.get(row["rfm_segment"], PALETTE["neutral"])
        size = row["total_rev"] / seg_agg["total_rev"].max() * 5000
        ax2.scatter(
            row["avg_aov"] / 1_000,
            row["avg_orders"],
            s=size, color=color, alpha=0.75, edgecolors="white", linewidth=2,
        )
        ax2.annotate(
            f"{row['rfm_segment']}\n{row['count']:,} khách",
            xy=(row["avg_aov"] / 1_000, row["avg_orders"]),
            xytext=(12, 6), textcoords="offset points",
            fontsize=10, fontweight="bold",
        )

    ax2.set_xlabel("Giá trị trung bình mỗi đơn (nghìn VND)", fontsize=11)
    ax2.set_ylabel("Số đơn hàng trung bình mỗi khách", fontsize=11)
    ax2.set_title("Bản đồ phân khúc RFM — Dữ liệu T1-T9/2024 (9 tháng)\n"
                  "Bong bóng càng TO = tổng doanh thu nhóm càng LỚN",
                  fontsize=12)
    ax2.tick_params(labelsize=10)

    # legend for bubble size
    for rev_m, label in [(1e9, "1 tỷ VND"), (5e9, "5 tỷ VND")]:
        size_leg = rev_m / seg_agg["total_rev"].max() * 5000
        ax2.scatter([], [], s=size_leg, color=PALETTE["neutral"], alpha=0.5, label=label)
    ax2.legend(title="Tổng doanh thu", fontsize=10, loc="lower right",
               title_fontsize=10)

    plt.tight_layout()
    save_fig(fig, "chart-07-segmentation.png", img_dir=IMG_CH03)
