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
    axes[0, 0].set_xlabel("Giá trị đơn hàng (nghìn VND)")
    axes[0, 0].set_ylabel("Số đơn hàng")
    axes[0, 0].set_title("Số đơn theo giá trị đơn hàng (lệch phải)")
    axes[0, 0].axvline(rev.median() / 1_000, color=PALETTE["accent"],
                       linestyle="--", label=f"Median: {rev.median()/1000:.0f}K")
    axes[0, 0].axvline(rev.mean() / 1_000, color=PALETTE["negative"],
                       linestyle="--", label=f"Mean: {rev.mean()/1000:.0f}K")
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].set_xlim(0, rev.quantile(0.99) / 1_000)

    # 2. Delivery time — from CSV column delivery_days
    delivery = df["delivery_days"].dropna()
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


def chart_02b_category_breakdown(df: pd.DataFrame) -> None:
    """Pie + bar charts: order count and revenue by category."""
    # Only completed orders
    completed = df[df["status"] == "Hoàn thành"].copy()

    cat_stats = completed.groupby("category").agg(
        order_count=("order_id", "count"),
        total_revenue=("revenue", "sum"),
    ).sort_values("total_revenue", ascending=False)

    fig, axes = plt.subplots(1, 3, figsize=(18, 7),
                             gridspec_kw={"width_ratios": [1, 1, 1.3]})
    fig.suptitle("Lens #2b: Phân bổ theo danh mục sản phẩm",
                 fontsize=14, fontweight="bold")

    colors = CAT_COLORS[:len(cat_stats)]

    # 1. Pie: số đơn theo danh mục
    axes[0].pie(
        cat_stats["order_count"], labels=cat_stats.index,
        colors=colors, autopct="%1.1f%%", startangle=90,
        textprops={"fontsize": 9},
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    axes[0].set_title("Số đơn hàng theo danh mục", fontsize=11)

    # 2. Pie: doanh thu theo danh mục
    axes[1].pie(
        cat_stats["total_revenue"], labels=cat_stats.index,
        colors=colors, autopct="%1.1f%%", startangle=90,
        textprops={"fontsize": 9},
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    axes[1].set_title("Doanh thu theo danh mục", fontsize=11)

    # 3. Bar: so sánh % đơn vs % doanh thu cạnh nhau
    cat_stats["order_pct"] = cat_stats["order_count"] / cat_stats["order_count"].sum() * 100
    cat_stats["revenue_pct"] = cat_stats["total_revenue"] / cat_stats["total_revenue"].sum() * 100

    x = range(len(cat_stats))
    width = 0.35
    bars1 = axes[2].bar([i - width / 2 for i in x], cat_stats["order_pct"],
                        width, label="% Số đơn", color=PALETTE["primary"], alpha=0.85)
    bars2 = axes[2].bar([i + width / 2 for i in x], cat_stats["revenue_pct"],
                        width, label="% Doanh thu", color=PALETTE["negative"], alpha=0.85)
    axes[2].set_xticks(list(x))
    axes[2].set_xticklabels(cat_stats.index, rotation=25, ha="right", fontsize=9)
    axes[2].set_ylabel("Phần trăm (%)")
    axes[2].set_title("So sánh: % đơn vs % doanh thu", fontsize=11)
    axes[2].legend(fontsize=9)

    # Annotate the gap for Điện Tử
    if "Điện Tử" in cat_stats.index:
        idx = list(cat_stats.index).index("Điện Tử")
        order_p = cat_stats.loc["Điện Tử", "order_pct"]
        rev_p = cat_stats.loc["Điện Tử", "revenue_pct"]
        axes[2].annotate(
            f"Chỉ {order_p:.0f}% đơn\nnhưng {rev_p:.0f}% doanh thu!",
            xy=(idx + width / 2, rev_p), xytext=(idx + 1.2, rev_p + 5),
            fontsize=8, color=PALETTE["negative"], fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=PALETTE["negative"], lw=1.2),
        )

    plt.tight_layout()
    save_fig(fig, "chart-02b-category-breakdown.png", img_dir=IMG_CH01)


def chart_02c_city_breakdown(df: pd.DataFrame) -> None:
    """Bar charts: order count, revenue, and avg order value by city."""
    completed = df[df["status"] == "Hoàn thành"].copy()

    city_stats = completed.groupby("city").agg(
        order_count=("order_id", "count"),
        total_revenue=("revenue", "sum"),
        avg_order_value=("revenue", "median"),
    ).sort_values("total_revenue", ascending=False)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Phân bổ theo thành phố", fontsize=14, fontweight="bold")

    colors = [PALETTE["primary"] if c in ["TP.HCM", "Hà Nội"]
              else PALETTE["neutral"] for c in city_stats.index]

    # 1. Số đơn hàng
    bars1 = axes[0].bar(city_stats.index, city_stats["order_count"], color=colors, alpha=0.85)
    axes[0].set_title("Số đơn hàng theo thành phố", fontsize=11)
    axes[0].set_ylabel("Số đơn")
    axes[0].tick_params(axis="x", rotation=25)
    for bar, val in zip(bars1, city_stats["order_count"]):
        pct = val / city_stats["order_count"].sum() * 100
        axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                     f"{pct:.0f}%", ha="center", fontsize=9, fontweight="bold")

    # 2. Doanh thu
    bars2 = axes[1].bar(city_stats.index, city_stats["total_revenue"] / 1e9,
                        color=colors, alpha=0.85)
    axes[1].set_title("Doanh thu theo thành phố (tỷ VNĐ)", fontsize=11)
    axes[1].set_ylabel("Tỷ VNĐ")
    axes[1].tick_params(axis="x", rotation=25)
    for bar, val in zip(bars2, city_stats["total_revenue"]):
        pct = val / city_stats["total_revenue"].sum() * 100
        axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                     f"{pct:.0f}%", ha="center", fontsize=9, fontweight="bold")

    # 3. Giá trị đơn hàng trung vị
    bars3 = axes[2].bar(city_stats.index, city_stats["avg_order_value"] / 1_000,
                        color=colors, alpha=0.85)
    axes[2].set_title("Giá trị đơn trung vị (nghìn VNĐ)", fontsize=11)
    axes[2].set_ylabel("Nghìn VNĐ")
    axes[2].tick_params(axis="x", rotation=25)
    for bar, val in zip(bars3, city_stats["avg_order_value"]):
        axes[2].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                     f"{val/1_000:.0f}K", ha="center", fontsize=9)

    plt.tight_layout()
    save_fig(fig, "chart-02c-city-breakdown.png", img_dir=IMG_CH01)


def chart_02d_discount_and_status(df: pd.DataFrame) -> None:
    """Discount distribution + order status breakdown."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Phân phối giảm giá & trạng thái đơn hàng",
                 fontsize=14, fontweight="bold")

    # 1. Histogram: discount distribution
    disc = df["discount_pct"] * 100  # convert to %
    axes[0].hist(disc, bins=30, color=PALETTE["accent"], edgecolor="white", alpha=0.85)
    axes[0].set_xlabel("Mức giảm giá (%)")
    axes[0].set_ylabel("Số đơn hàng")
    axes[0].set_title("Phân phối mức giảm giá")
    axes[0].axvline(disc.median(), color=PALETTE["primary"],
                    linestyle="--", label=f"Median: {disc.median():.1f}%")
    axes[0].axvline(disc.mean(), color=PALETTE["negative"],
                    linestyle="--", label=f"Mean: {disc.mean():.1f}%")
    no_disc = (disc == 0).sum()
    no_disc_pct = no_disc / len(disc) * 100
    axes[0].text(0.97, 0.95, f"{no_disc_pct:.0f}% đơn\nkhông giảm giá",
                 transform=axes[0].transAxes, ha="right", va="top",
                 fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor="#f8f9fa"))
    axes[0].legend(fontsize=9)

    # 2. Status pie chart
    status_counts = df["status"].value_counts()
    status_colors = [PALETTE["positive"], PALETTE["negative"], PALETTE["accent"]]
    axes[1].pie(
        status_counts.values, labels=status_counts.index,
        colors=status_colors[:len(status_counts)],
        autopct="%1.1f%%", startangle=90,
        textprops={"fontsize": 10},
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    axes[1].set_title("Trạng thái đơn hàng")

    # 3. Cancel + return rate by category
    cat_status = df.groupby(["category", "status"]).size().unstack(fill_value=0)
    cat_total = cat_status.sum(axis=1)
    cat_cancel_pct = (cat_status.get("Đã hủy", 0) / cat_total * 100).sort_values(ascending=False)
    cat_return_pct = (cat_status.get("Hoàn trả", 0) / cat_total * 100).sort_values(ascending=False)

    x = range(len(cat_cancel_pct))
    width = 0.35
    axes[2].bar([i - width / 2 for i in x], cat_cancel_pct.values,
                width, label="% Hủy đơn", color=PALETTE["negative"], alpha=0.85)
    axes[2].bar([i + width / 2 for i in x], cat_return_pct.reindex(cat_cancel_pct.index).values,
                width, label="% Hoàn trả", color=PALETTE["accent"], alpha=0.85)
    axes[2].set_xticks(list(x))
    axes[2].set_xticklabels(cat_cancel_pct.index, rotation=25, ha="right", fontsize=9)
    axes[2].set_ylabel("Phần trăm (%)")
    axes[2].set_title("Tỉ lệ hủy & hoàn trả theo danh mục")
    axes[2].legend(fontsize=9)

    plt.tight_layout()
    save_fig(fig, "chart-02d-discount-status.png", img_dir=IMG_CH01)
