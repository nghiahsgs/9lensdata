"""
ch04_correlation_volatility/charts.py — Lens 5 (correlation), Lens 8 (volatility),
and Lens 9 (marketing correlation) charts.
Chapter 04: Correlation & Volatility
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
from shared.chart_helpers import save_fig, PALETTE, CAT_COLORS, vnd_formatter, DATA_CH04, IMG_CH04


def load_marketing() -> pd.DataFrame:
    df = pd.read_csv(DATA_CH04 / "techmart-marketing-campaigns.csv", encoding="utf-8-sig")
    df["start_date"] = pd.to_datetime(df["start_date"])
    return df


def chart_05_correlation(df_mar: pd.DataFrame, df_cust: pd.DataFrame) -> None:
    """Correlation matrix heatmap + Recency vs Churn scatter + horizontal bar correlation ranking."""
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
    save_fig(fig, "chart-08-volatility.png", img_dir=IMG_CH04)


def chart_09_marketing_correlation(df: pd.DataFrame) -> None:
    """
    3 subplots (14×6):
    Left:   Scatter ROAS by channel (color-coded), Email dominates
    Middle: Heatmap correlation matrix (spend, impressions, clicks, conversions, revenue, ROAS)
    Right:  Bar chart CAC by channel, holiday campaigns annotated
    """
    CHANNEL_COLORS = {
        "Facebook":  CAT_COLORS[0],
        "Google":    CAT_COLORS[1],
        "TikTok":    CAT_COLORS[2],
        "Email":     CAT_COLORS[3],
        "SMS":       CAT_COLORS[4],
        "Affiliate": CAT_COLORS[5],
    }

    fig, axes = plt.subplots(1, 3, figsize=(14, 6))
    fig.suptitle(
        "Lens #9: MARKETING — Tương quan kênh quảng cáo & Biến nhiễu (Confounding)",
        fontsize=13, fontweight="bold"
    )

    # Left: ROAS scatter by channel
    ax = axes[0]
    channels = df["channel"].unique()
    x_pos = {ch: i for i, ch in enumerate(sorted(channels))}

    for ch, color in CHANNEL_COLORS.items():
        subset = df[df["channel"] == ch]
        jitter = np.random.default_rng(42).uniform(-0.25, 0.25, len(subset))
        ax.scatter(
            [x_pos[ch]] * len(subset) + jitter,
            subset["roas"],
            color=color, alpha=0.45, s=25, label=ch,
        )
        # mean marker
        ax.plot(x_pos[ch], subset["roas"].mean(),
                "D", color=color, markersize=9, markeredgecolor="white",
                markeredgewidth=1.2, zorder=5)

    # Annotate Email as highest ROAS
    email_mean = df[df["channel"] == "Email"]["roas"].mean()
    email_x = x_pos["Email"]
    ax.annotate(
        f"Email ROAS TB\n{email_mean:.1f}x",
        xy=(email_x, email_mean),
        xytext=(email_x + 0.7, email_mean + 1.2),
        arrowprops=dict(arrowstyle="->", color=PALETTE["positive"]),
        fontsize=8, color=PALETTE["positive"], fontweight="bold",
    )

    ax.axhline(1.0, color=PALETTE["negative"], linestyle="--", linewidth=1, alpha=0.7,
               label="ROAS = 1 (hòa vốn)")
    ax.set_xticks(list(x_pos.values()))
    ax.set_xticklabels(sorted(channels), rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("ROAS (Return on Ad Spend)")
    ax.set_title("ROAS theo kênh\n(◆ = trung bình, Email dẫn đầu)")
    ax.legend(fontsize=7, loc="upper right", markerscale=1.2)

    # Middle: Correlation heatmap
    ax = axes[1]
    corr_cols = ["spend_vnd", "impressions", "clicks", "conversions",
                 "revenue_generated", "roas"]
    corr_labels_vi = ["Chi phí", "Lượt hiển thị", "Lượt click",
                      "Chuyển đổi", "Doanh thu", "ROAS"]
    corr_matrix = df[corr_cols].corr()

    sns.heatmap(
        corr_matrix,
        ax=ax,
        annot=True, fmt=".2f",
        cmap="RdBu_r", center=0, vmin=-1, vmax=1,
        xticklabels=corr_labels_vi,
        yticklabels=corr_labels_vi,
        linewidths=0.5, square=True,
        cbar_kws={"shrink": 0.8, "label": "r"},
    )
    ax.set_title("Ma trận tương quan\n(Email: chi phí thấp → ROAS cao)")
    ax.tick_params(axis="x", rotation=35, labelsize=8)
    ax.tick_params(axis="y", rotation=0, labelsize=8)

    # Right: CAC by channel + holiday annotation
    ax = axes[2]
    cac_by_channel = df.groupby("channel")["cac"].median().sort_values()

    bar_colors = [CHANNEL_COLORS.get(ch, PALETTE["neutral"]) for ch in cac_by_channel.index]
    bars = ax.barh(cac_by_channel.index, cac_by_channel.values / 1000,
                   color=bar_colors, alpha=0.85, edgecolor="white")

    ax.set_xlabel("CAC trung bình (nghìn VND)")
    ax.set_title("Chi phí thu hút khách hàng (CAC)\n& Biến nhiễu: Campaign mùa lễ hội")

    # Add value labels
    for bar, val in zip(bars, cac_by_channel.values):
        ax.text(val / 1000 + 1, bar.get_y() + bar.get_height() / 2,
                f"{val/1000:.0f}K", va="center", fontsize=8)

    # Holiday annotation box (spurious correlation note)
    holiday_conv_avg = df[df["is_holiday_period"]]["roas"].mean()
    non_holiday_conv_avg = df[~df["is_holiday_period"]]["roas"].mean()
    ax.text(
        0.97, 0.12,
        f"Mùa lễ hội:\nROAS = {holiday_conv_avg:.1f}x\nvs bình thường = {non_holiday_conv_avg:.1f}x\n"
        f"→ Biến nhiễu (confounding)!\nKhông phải chi phí → kết quả",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5,
        color=PALETTE["negative"],
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff3cd", edgecolor=PALETTE["accent"],
                  alpha=0.9),
    )

    plt.tight_layout()
    save_fig(fig, "chart-09-marketing-correlation.png", img_dir=IMG_CH04)
