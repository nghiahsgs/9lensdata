"""
charts_marketing.py — Ch.4 marketing correlation chart (chart-09).
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
from chart_helpers import save_fig, PALETTE, CAT_COLORS, vnd_formatter, DATA_CH04, IMG_CH04


def load_marketing() -> pd.DataFrame:
    df = pd.read_csv(DATA_CH04 / "techmart-marketing-campaigns.csv", encoding="utf-8-sig")
    df["start_date"] = pd.to_datetime(df["start_date"])
    return df


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

    # ── Left: ROAS scatter by channel ────────────────────────────────────────
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

    # ── Middle: Correlation heatmap ──────────────────────────────────────────
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

    # ── Right: CAC by channel + holiday annotation ───────────────────────────
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
