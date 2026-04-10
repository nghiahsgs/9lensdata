"""
charts_lens7_8.py — Lens 7 (segmentation) and Lens 8 (volatility) charts.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from chart_helpers import save_fig, PALETTE, CAT_COLORS, vnd_formatter


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
    save_fig(fig, "chart-07-segmentation.png")


def chart_08_volatility(df_full: pd.DataFrame) -> None:
    """4 subplots: time series 3 categories + CV bar chart + rolling volatility + risk matrix."""
    df = df_full.copy()
    df["month"] = df["order_date"].dt.to_period("M")
    top_cats = ["Điện Tử", "Thời Trang", "FMCG"]

    monthly_cat = (
        df[df["category"].isin(top_cats)]
        .groupby(["month", "category"])["revenue"]
        .sum()
        .unstack(fill_value=0)
    )
    monthly_cat.index = monthly_cat.index.astype(str)

    # CV per category (all 6)
    monthly_all = (
        df.groupby(["month", "category"])["revenue"]
        .sum()
        .unstack(fill_value=0)
    )
    cv = (monthly_all.std() / monthly_all.mean()).sort_values(ascending=False)

    # rolling volatility (std of 3-month window) for top 3
    rolling_vol = monthly_cat.rolling(3, min_periods=2).std()

    # risk matrix: avg revenue (x) vs CV (y)
    avg_rev = monthly_all.mean()
    risk_df = pd.DataFrame({"avg_rev": avg_rev, "cv": cv})

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Lens #8: VOLATILITY — Phân tích biến động và rủi ro",
                 fontsize=14, fontweight="bold")

    # 1. Time series 3 categories
    ax = axes[0, 0]
    colors_ts = [PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"]]
    for i, cat in enumerate(top_cats):
        if cat in monthly_cat.columns:
            ax.plot(range(len(monthly_cat)), monthly_cat[cat] / 1e6,
                    marker="o", markersize=4, color=colors_ts[i],
                    linewidth=1.5, label=cat, alpha=0.85)
    ax.set_xticks(range(len(monthly_cat)))
    ax.set_xticklabels(monthly_cat.index, rotation=45, ha="right", fontsize=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(vnd_formatter))
    ax.set_ylabel("Doanh thu (triệu VND)")
    ax.set_title("Doanh thu theo tháng — Top 3 danh mục")
    ax.legend(fontsize=9)

    # 2. CV bar chart
    ax2 = axes[0, 1]
    colors_cv = [PALETTE["negative"] if v > 0.5 else PALETTE["accent"] if v > 0.3
                 else PALETTE["positive"] for v in cv.values]
    ax2.bar(range(len(cv)), cv.values, color=colors_cv, alpha=0.85)
    ax2.set_xticks(range(len(cv)))
    ax2.set_xticklabels(cv.index, rotation=30, ha="right", fontsize=9)
    ax2.set_ylabel("Hệ số biến thiên (CV)")
    ax2.set_title("Mức độ biến động theo danh mục\n(CV = Std / Mean)")
    ax2.axhline(0.3, color=PALETTE["accent"], linestyle="--", alpha=0.7, label="CV=0.3")
    ax2.axhline(0.5, color=PALETTE["negative"], linestyle="--", alpha=0.7, label="CV=0.5")
    ax2.legend(fontsize=9)
    for i, (cat, val) in enumerate(cv.items()):
        ax2.text(i, val + 0.01, f"{val:.2f}", ha="center", va="bottom", fontsize=8)

    # 3. Rolling volatility
    ax3 = axes[1, 0]
    for i, cat in enumerate(top_cats):
        if cat in rolling_vol.columns:
            ax3.plot(range(len(rolling_vol)), rolling_vol[cat] / 1e6,
                     color=colors_ts[i], linewidth=1.5, label=cat, alpha=0.85)
    ax3.set_xticks(range(len(rolling_vol)))
    ax3.set_xticklabels(rolling_vol.index, rotation=45, ha="right", fontsize=8)
    ax3.yaxis.set_major_formatter(mticker.FuncFormatter(vnd_formatter))
    ax3.set_ylabel("Độ lệch chuẩn (triệu VND)")
    ax3.set_title("Biến động cuốn 3 tháng")
    ax3.legend(fontsize=9)

    # 4. Risk matrix: avg revenue vs CV
    ax4 = axes[1, 1]
    colors_risk = CAT_COLORS[:len(risk_df)]
    for i, (cat, row) in enumerate(risk_df.iterrows()):
        ax4.scatter(row["avg_rev"] / 1e6, row["cv"],
                    s=200, color=colors_risk[i % len(colors_risk)],
                    alpha=0.85, zorder=3, edgecolors="white", linewidth=1)
        ax4.annotate(cat, xy=(row["avg_rev"] / 1e6, row["cv"]),
                     xytext=(5, 4), textcoords="offset points", fontsize=8)
    med_rev = risk_df["avg_rev"].median() / 1e6
    med_cv = risk_df["cv"].median()
    ax4.axvline(med_rev, color=PALETTE["neutral"], linestyle="--", alpha=0.5)
    ax4.axhline(med_cv, color=PALETTE["neutral"], linestyle="--", alpha=0.5)
    ax4.text(med_rev * 1.05, med_cv * 1.05, "Rủi ro cao\nDT thấp", fontsize=8,
             color=PALETTE["negative"])
    ax4.text(med_rev * 0.1, med_cv * 0.3, "An toàn\nDT cao", fontsize=8,
             color=PALETTE["positive"])
    ax4.set_xlabel("Doanh thu TB tháng (triệu VND)")
    ax4.set_ylabel("Hệ số biến thiên (CV)")
    ax4.set_title("Ma trận rủi ro — Doanh thu vs Biến động")
    ax4.xaxis.set_major_formatter(mticker.FuncFormatter(vnd_formatter))

    fig.subplots_adjust(top=0.90, hspace=0.45, wspace=0.35)
    save_fig(fig, "chart-08-volatility.png")
