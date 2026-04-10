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
    """Revenue heatmap (City × Category) + RFM segment bubble map."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Lens #7: SEGMENTATION — Phân tích theo nhóm và không gian",
                 fontsize=14, fontweight="bold")

    # 1. Revenue heatmap City × Category
    pivot = df_mar.pivot_table(
        values="revenue", index="city", columns="category", aggfunc="sum", fill_value=0
    )
    pivot_m = pivot / 1e6  # million VND
    sns.heatmap(
        pivot_m, ax=axes[0], annot=True, fmt=".0f", cmap="Blues",
        linewidths=0.5, cbar_kws={"label": "Doanh thu (triệu VND)"},
    )
    axes[0].set_title("Doanh thu theo Thành phố × Danh mục\n(triệu VND)")
    axes[0].set_xlabel("Danh mục sản phẩm")
    axes[0].set_ylabel("Thành phố")
    axes[0].tick_params(axis="x", rotation=30)
    axes[0].tick_params(axis="y", rotation=0)

    # 2. RFM segment bubble map
    # axes: x=avg_order_value, y=total_orders, size=total_revenue, color=segment
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
        size = row["total_rev"] / seg_agg["total_rev"].max() * 3000
        ax2.scatter(
            row["avg_aov"] / 1_000,
            row["avg_orders"],
            s=size, color=color, alpha=0.75, edgecolors="white", linewidth=1.5,
        )
        ax2.annotate(
            f"{row['rfm_segment']}\n(n={row['count']:,})",
            xy=(row["avg_aov"] / 1_000, row["avg_orders"]),
            xytext=(8, 4), textcoords="offset points",
            fontsize=8,
        )

    ax2.set_xlabel("Giá trị đơn hàng TB (nghìn VND)")
    ax2.set_ylabel("Số đơn hàng TB")
    ax2.set_title("Bản đồ phân khúc RFM\n(kích thước = tổng doanh thu)")

    # legend for bubble size
    for rev_m, label in [(1e9, "1B VND"), (5e9, "5B VND")]:
        size_leg = rev_m / seg_agg["total_rev"].max() * 3000
        ax2.scatter([], [], s=size_leg, color=PALETTE["neutral"], alpha=0.5, label=label)
    ax2.legend(title="Tổng DT", fontsize=8, loc="lower right")

    plt.tight_layout()
    save_fig(fig, "chart-07-segmentation.png", img_dir=IMG_CH03)
