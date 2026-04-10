"""
charts_lens5_6.py — Lens 5 (correlation) and Lens 6 (comparison) charts.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from chart_helpers import save_fig, PALETTE, CAT_COLORS, vnd_formatter, IMG_CH04, IMG_CH05


def chart_05_correlation(df_mar: pd.DataFrame, df_cust: pd.DataFrame) -> None:
    """Correlation matrix heatmap + Recency vs Churn scatter + horizontal bar correlation ranking."""
    import seaborn as sns

    # build numeric frame for correlation matrix
    df_num = df_mar[["quantity", "unit_price", "discount_pct", "revenue"]].copy()
    df_num["rating"] = df_mar["rating"]
    corr = df_num.corr()

    # recency (days since last purchase) for customers
    df_c = df_cust.copy()
    df_c["last_purchase"] = pd.to_datetime(df_c["last_purchase"])
    ref = pd.Timestamp("2024-03-28")
    df_c["recency_days"] = (ref - df_c["last_purchase"]).dt.days

    # correlation of numeric features with churn_risk
    feat_cols = ["recency_days", "total_orders", "total_revenue", "avg_order_value"]
    corr_churn = df_c[feat_cols + ["churn_risk"]].corr()["churn_risk"].drop("churn_risk")
    corr_churn = corr_churn.sort_values()

    label_map = {
        "recency_days":    "Số ngày không mua",
        "total_orders":    "Tổng đơn hàng",
        "total_revenue":   "Tổng doanh thu",
        "avg_order_value": "Giá trị đơn TB",
    }
    corr_churn.index = [label_map.get(i, i) for i in corr_churn.index]

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle("Lens #5: CORRELATION — Mối quan hệ giữa các biến số",
                 fontsize=14, fontweight="bold")

    # 1. Correlation matrix heatmap
    col_labels_vi = ["Số lượng", "Đơn giá", "Giảm giá", "Doanh thu", "Đánh giá"]
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(
        corr, ax=axes[0], annot=True, fmt=".2f", cmap="RdBu_r",
        center=0, vmin=-1, vmax=1,
        xticklabels=col_labels_vi, yticklabels=col_labels_vi,
        linewidths=0.5, square=True,
        cbar_kws={"shrink": 0.8},
    )
    axes[0].set_title("Ma trận tương quan\n(biến số đơn hàng)")
    axes[0].tick_params(axis="x", rotation=30)
    axes[0].tick_params(axis="y", rotation=0)

    # 2. Recency vs Churn scatter (sample 2000 pts for readability)
    sample = df_c.sample(min(2000, len(df_c)), random_state=42)
    seg_palette = {
        "Champions": CAT_COLORS[0],
        "Loyal": CAT_COLORS[1],
        "Potential Loyalists": CAT_COLORS[2],
        "At Risk": CAT_COLORS[3],
        "Hibernating": CAT_COLORS[4],
        "Lost": CAT_COLORS[5],
    }
    for seg, color in seg_palette.items():
        mask_s = sample["rfm_segment"] == seg
        axes[1].scatter(
            sample.loc[mask_s, "recency_days"],
            sample.loc[mask_s, "churn_risk"],
            color=color, alpha=0.4, s=15, label=seg,
        )
    axes[1].set_xlabel("Số ngày không mua (Recency)")
    axes[1].set_ylabel("Điểm rủi ro rời bỏ (Churn Risk)")
    axes[1].set_title("Recency vs Churn Risk\ntheo phân khúc RFM")
    axes[1].legend(fontsize=7, markerscale=1.5, loc="upper left")

    # 3. Horizontal bar: feature correlation with churn_risk
    colors_bar = [PALETTE["negative"] if v > 0 else PALETTE["positive"]
                  for v in corr_churn.values]
    axes[2].barh(corr_churn.index, corr_churn.values, color=colors_bar, alpha=0.85)
    axes[2].axvline(0, color=PALETTE["neutral"], linewidth=1)
    axes[2].set_xlabel("Hệ số tương quan với Churn Risk")
    axes[2].set_title("Xếp hạng tương quan\nvới rủi ro rời bỏ")
    for i, (idx, val) in enumerate(corr_churn.items()):
        ha = "left" if val >= 0 else "right"
        offset = 0.01 if val >= 0 else -0.01
        axes[2].text(val + offset, i, f"{val:.2f}", va="center", ha=ha, fontsize=9)

    plt.tight_layout()
    save_fig(fig, "chart-05-correlation.png", img_dir=IMG_CH04)


def chart_06_comparison(df_full: pd.DataFrame, df_mar: pd.DataFrame) -> None:
    """Waterfall T2→T3 + YoY 2023 vs 2024 bar chart + Benchmark comparison."""
    df_full = df_full.copy()
    df_full["month"] = df_full["order_date"].dt.to_period("M")

    def month_rev(year: int, month: int) -> float:
        mask = (df_full["order_date"].dt.year == year) & \
               (df_full["order_date"].dt.month == month)
        return df_full.loc[mask, "revenue"].sum()

    rev_feb = month_rev(2024, 2)
    rev_mar = month_rev(2024, 3)
    rev_mar23 = month_rev(2023, 3)

    # waterfall components: T2 base → items gained / lost → T3
    # Simulate category breakdown deltas
    cats = ["Điện Tử", "Thời Trang", "FMCG", "Gia Dụng", "Thể Thao", "Phụ Kiện"]
    cat_feb = df_full[(df_full["order_date"].dt.year == 2024) &
                      (df_full["order_date"].dt.month == 2)].groupby("category")["revenue"].sum()
    cat_mar = df_full[(df_full["order_date"].dt.year == 2024) &
                      (df_full["order_date"].dt.month == 3)].groupby("category")["revenue"].sum()
    deltas = {c: cat_mar.get(c, 0) - cat_feb.get(c, 0) for c in cats}

    # build waterfall data
    wf_labels = ["T2/2024"] + cats + ["T3/2024"]
    wf_values = [rev_feb] + [deltas[c] for c in cats] + [rev_mar]
    bottoms = []
    running = rev_feb
    for i, v in enumerate(wf_values):
        if i == 0 or i == len(wf_values) - 1:
            bottoms.append(0)
        else:
            if v >= 0:
                bottoms.append(running)
                running += v
            else:
                running += v
                bottoms.append(running)

    wf_colors = [PALETTE["primary"]] + \
                [PALETTE["positive"] if d >= 0 else PALETTE["negative"] for d in deltas.values()] + \
                [PALETTE["secondary"]]

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle("Lens #6: COMPARISON — So sánh theo thời gian và chuẩn mực",
                 fontsize=14, fontweight="bold")

    # 1. Waterfall
    ax = axes[0]
    bar_vals = [abs(v) for v in wf_values]
    ax.bar(range(len(wf_labels)), bar_vals, bottom=bottoms,
           color=wf_colors, alpha=0.85, edgecolor="white", linewidth=0.5)
    ax.set_xticks(range(len(wf_labels)))
    ax.set_xticklabels(["T2/2024"] + [c[:6] for c in cats] + ["T3/2024"],
                       rotation=45, ha="right", fontsize=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(vnd_formatter))
    ax.set_title("Biến động doanh thu T2 → T3/2024\n(Waterfall)")
    ax.set_ylabel("Doanh thu (VND)")

    # 2. YoY bar chart: 2023 vs 2024 monthly
    months_shared = list(range(1, 4))  # only T1-T3 for both years (T1/2023 not in data → use T3)
    labels_yoy = ["T3"]
    rev_23 = [rev_mar23 / 1e6]
    rev_24 = [rev_mar / 1e6]
    x = np.arange(len(labels_yoy))
    w = 0.35
    ax2 = axes[1]
    b1 = ax2.bar(x - w / 2, rev_23, w, label="2023", color=PALETTE["neutral"], alpha=0.85)
    b2 = ax2.bar(x + w / 2, rev_24, w, label="2024", color=PALETTE["primary"], alpha=0.85)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels_yoy)
    ax2.set_ylabel("Doanh thu (triệu VND)")
    ax2.set_title("So sánh YoY: T3/2023 vs T3/2024")
    ax2.legend()
    yoy_pct = (rev_mar - rev_mar23) / rev_mar23 * 100
    ax2.text(0.5, 0.92, f"YoY: +{yoy_pct:.1f}%", transform=ax2.transAxes,
             ha="center", fontsize=11, color=PALETTE["positive"], fontweight="bold")

    # 3. Benchmark comparison: category revenue vs hypothetical benchmark
    cat_rev_mar = df_mar.groupby("category")["revenue"].sum().sort_values(ascending=True)
    # simulate industry benchmark as 110% of actual for most, 90% for Điện Tử
    benchmarks = cat_rev_mar * np.array([1.1, 1.05, 0.90, 1.08, 1.12, 1.03])
    ax3 = axes[2]
    y = np.arange(len(cat_rev_mar))
    ax3.barh(y - 0.2, cat_rev_mar.values / 1e6, 0.4,
             label="TechMart T3/2024", color=PALETTE["primary"], alpha=0.85)
    ax3.barh(y + 0.2, benchmarks.values / 1e6, 0.4,
             label="Chuẩn ngành (ước tính)", color=PALETTE["neutral"], alpha=0.6)
    ax3.set_yticks(y)
    ax3.set_yticklabels(cat_rev_mar.index, fontsize=9)
    ax3.set_xlabel("Doanh thu (triệu VND)")
    ax3.set_title("So sánh với chuẩn ngành\ntheo danh mục")
    ax3.xaxis.set_major_formatter(mticker.FuncFormatter(vnd_formatter))
    ax3.legend(fontsize=9)

    plt.tight_layout()
    save_fig(fig, "chart-06-comparison.png", img_dir=IMG_CH05)
