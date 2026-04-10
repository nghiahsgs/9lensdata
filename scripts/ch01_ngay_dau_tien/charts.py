"""
ch01_ngay_dau_tien/charts.py — Lens 1 (completeness) and Lens 2 (distribution) charts.
Chapter 01: Ngay Dau Tien
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from shared.chart_helpers import save_fig, PALETTE, CAT_COLORS, vnd_formatter, IMG_CH01


def chart_01_completeness(df: pd.DataFrame) -> None:
    """Heatmap: missing values by column × week + bar chart % missing per column."""
    df = df.copy()
    df["week"] = df["order_date"].dt.isocalendar().week.astype(int)

    cols_with_missing = ["rating", "quan_huyen"]
    all_cols = ["order_id", "customer_id", "order_date", "product_name",
                "category", "quantity", "unit_price", "discount_pct",
                "revenue", "city", "quan_huyen", "status", "rating"]

    # missing % per column (overall)
    miss_pct = df[all_cols].isna().mean() * 100

    # missing by week for heatmap columns
    weeks = sorted(df["week"].unique())
    heatmap_data = pd.DataFrame(index=cols_with_missing, columns=weeks, dtype=float)
    for col in cols_with_missing:
        for w in weeks:
            subset = df[df["week"] == w]
            heatmap_data.loc[col, w] = subset[col].isna().mean() * 100

    fig, axes = plt.subplots(1, 2, figsize=(14, 5),
                             gridspec_kw={"width_ratios": [2, 1]})
    fig.suptitle("Lens #1: COMPLETENESS — Phân tích dữ liệu bị thiếu", fontsize=14, fontweight="bold")

    # left: heatmap
    import seaborn as sns
    col_labels = [f"Tuần {w}" for w in weeks]
    row_labels = ["Đánh giá (rating)", "Quận/Huyện"]
    sns.heatmap(
        heatmap_data.values.astype(float),
        ax=axes[0],
        annot=True, fmt=".1f", cmap="YlOrRd",
        xticklabels=col_labels, yticklabels=row_labels,
        cbar_kws={"label": "% thiếu"},
        linewidths=0.5,
    )
    axes[0].set_title("Tỷ lệ dữ liệu thiếu theo tuần (%)")
    axes[0].tick_params(axis="x", rotation=0)
    axes[0].tick_params(axis="y", rotation=0)

    # right: bar chart overall missing %
    visible = miss_pct[miss_pct > 0].sort_values(ascending=True)
    colors = [PALETTE["negative"] if v > 30 else PALETTE["accent"]
              for v in visible.values]
    axes[1].barh(visible.index, visible.values, color=colors)
    axes[1].set_xlabel("% dữ liệu thiếu")
    axes[1].set_title("Tỷ lệ thiếu tổng quan")
    axes[1].set_xlim(0, 100)
    for i, (col, val) in enumerate(visible.items()):
        axes[1].text(val + 1, i, f"{val:.1f}%", va="center", fontsize=9)

    plt.tight_layout()
    save_fig(fig, "chart-01-completeness.png", img_dir=IMG_CH01)


def chart_02_distribution(df: pd.DataFrame) -> None:
    """4 subplots: revenue (right-skewed), delivery time (bimodal),
       quantity (discrete), rating (left-skewed)."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Lens #2: DISTRIBUTION — Hình dạng phân phối dữ liệu",
                 fontsize=14, fontweight="bold")

    # 1. Revenue histogram — right-skewed
    rev = df["revenue"][df["revenue"] > 0]
    axes[0, 0].hist(rev / 1_000, bins=60, color=PALETTE["primary"], edgecolor="white", alpha=0.85)
    axes[0, 0].set_xlabel("Doanh thu (nghìn VND)")
    axes[0, 0].set_ylabel("Số đơn hàng")
    axes[0, 0].set_title("Phân phối doanh thu (lệch phải)")
    axes[0, 0].axvline(rev.median() / 1_000, color=PALETTE["accent"],
                       linestyle="--", label=f"Median: {rev.median()/1000:.0f}K")
    axes[0, 0].axvline(rev.mean() / 1_000, color=PALETTE["negative"],
                       linestyle="--", label=f"Mean: {rev.mean()/1000:.0f}K")
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].set_xlim(0, rev.quantile(0.99) / 1_000)

    # 2. Delivery time (simulated bimodal: standard 3-5d + express 1-2d)
    np.random.seed(42)
    n = len(df)
    delivery = np.concatenate([
        np.random.normal(4, 0.8, int(n * 0.65)),   # standard
        np.random.normal(1.5, 0.4, int(n * 0.35)),  # express
    ])
    delivery = np.clip(delivery, 0.5, 10)
    axes[0, 1].hist(delivery, bins=40, color=PALETTE["secondary"], edgecolor="white", alpha=0.85)
    axes[0, 1].set_xlabel("Ngày giao hàng")
    axes[0, 1].set_ylabel("Số đơn hàng")
    axes[0, 1].set_title("Thời gian giao hàng (phân phối 2 đỉnh)")
    axes[0, 1].axvline(1.5, color=PALETTE["positive"], linestyle=":", label="Giao nhanh ~1.5 ngày")
    axes[0, 1].axvline(4.0, color=PALETTE["accent"], linestyle=":", label="Giao thường ~4 ngày")
    axes[0, 1].legend(fontsize=9)

    # 3. Quantity — discrete bars
    qty_counts = df["quantity"].value_counts().sort_index()
    qty_counts = qty_counts[qty_counts.index <= 10]
    axes[1, 0].bar(qty_counts.index, qty_counts.values,
                   color=PALETTE["accent"], edgecolor="white", alpha=0.85)
    axes[1, 0].set_xlabel("Số lượng sản phẩm")
    axes[1, 0].set_ylabel("Số đơn hàng")
    axes[1, 0].set_title("Phân phối số lượng (rời rạc)")
    axes[1, 0].set_xticks(qty_counts.index)

    # 4. Rating — left-skewed (higher ratings dominate)
    ratings = df["rating"].dropna()
    rating_counts = ratings.value_counts().sort_index()
    colors_r = [PALETTE["negative"], PALETTE["accent"], PALETTE["neutral"],
                PALETTE["positive"], PALETTE["primary"]]
    axes[1, 1].bar(rating_counts.index, rating_counts.values,
                   color=colors_r[:len(rating_counts)], edgecolor="white", alpha=0.85)
    axes[1, 1].set_xlabel("Điểm đánh giá")
    axes[1, 1].set_ylabel("Số đánh giá")
    axes[1, 1].set_title("Phân phối đánh giá (lệch trái — survivorship bias)")
    axes[1, 1].set_xticks([1, 2, 3, 4, 5])
    miss_pct = df["rating"].isna().mean() * 100
    axes[1, 1].text(0.97, 0.95, f"{miss_pct:.0f}% không có\nđánh giá",
                    transform=axes[1, 1].transAxes, ha="right", va="top",
                    fontsize=9, color=PALETTE["neutral"],
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="#f8f9fa"))

    plt.tight_layout()
    save_fig(fig, "chart-02-distribution.png", img_dir=IMG_CH01)
