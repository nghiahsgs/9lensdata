"""
ch05_ke_chuyen_dung_nguoi/charts.py — Lens 6 (comparison), Lens 10 (finance P&L),
and Lens 11 (operations dashboard) charts.
Chapter 05: Ke Chuyen Dung Nguoi
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import seaborn as sns
from shared.chart_helpers import save_fig, PALETTE, CAT_COLORS, vnd_formatter, DATA_CH05, IMG_CH05


def load_finance() -> pd.DataFrame:
    df = pd.read_csv(DATA_CH05 / "techmart-finance-monthly.csv", encoding="utf-8-sig")
    df["period"] = pd.to_datetime(
        df[["year", "month"]].assign(day=1)
    )
    return df


def load_operations() -> pd.DataFrame:
    df = pd.read_csv(DATA_CH05 / "techmart-operations-daily.csv", encoding="utf-8-sig")
    df["date"] = pd.to_datetime(df["date"])
    return df


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


def chart_10_finance_pl(df: pd.DataFrame) -> None:
    """
    3 subplots (14×6):
    Left:   Stacked bar monthly P&L (revenue, COGS, costs breakdown) — 2024 only
    Middle: Line chart margins over time (gross & operating margin)
    Right:  Waterfall actual Q1-Q3 vs Q4 target (30 tỷ, 15% margin)
    """
    df2024 = df[df["year"] == 2024].copy().sort_values("month")
    month_labels = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]

    fig, axes = plt.subplots(1, 3, figsize=(14, 6))
    fig.suptitle(
        "Lens #10: TÀI CHÍNH — Phân tích P&L & Biên lợi nhuận 2024",
        fontsize=13, fontweight="bold"
    )

    # Left: Stacked bar breakdown
    ax = axes[0]
    x = np.arange(len(df2024))
    net_rev = df2024["net_revenue"].values / 1e9
    cogs_v = df2024["cogs"].values / 1e9
    mkt_v = df2024["marketing_spend"].values / 1e9
    ops_v = df2024["operations_cost"].values / 1e9
    sal_v = df2024["salaries"].values / 1e9
    other_v = df2024["other_costs"].values / 1e9

    bar_w = 0.6
    b1 = ax.bar(x, cogs_v, bar_w, label="Giá vốn (COGS)", color=PALETTE["negative"], alpha=0.85)
    b2 = ax.bar(x, mkt_v, bar_w, bottom=cogs_v, label="Marketing", color=PALETTE["accent"], alpha=0.85)
    b3 = ax.bar(x, ops_v, bar_w, bottom=cogs_v + mkt_v, label="Vận hành", color=PALETTE["secondary"], alpha=0.85)
    b4 = ax.bar(x, sal_v, bar_w, bottom=cogs_v + mkt_v + ops_v, label="Lương", color=PALETTE["neutral"], alpha=0.85)
    b5 = ax.bar(x, other_v, bar_w, bottom=cogs_v + mkt_v + ops_v + sal_v,
                label="Chi phí khác", color="#cccccc", alpha=0.85)

    # Net revenue line overlay
    ax.plot(x, net_rev, "o-", color=PALETTE["primary"], linewidth=2,
            markersize=5, label="Doanh thu thuần", zorder=5)

    ax.set_xticks(x)
    ax.set_xticklabels(month_labels, fontsize=8)
    ax.set_ylabel("Tỷ VND")
    ax.set_title("Cơ cấu chi phí & Doanh thu\ntheo tháng 2024")
    ax.legend(fontsize=7, loc="upper left")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}B"))

    # Middle: Margin trend lines
    ax = axes[1]
    df2023 = df[df["year"] == 2023].sort_values("month")

    x24 = np.arange(len(df2024))
    x23 = np.arange(len(df2023))

    ax.plot(x24, df2024["gross_margin_pct"].values, "o-",
            color=PALETTE["primary"], linewidth=2, markersize=5, label="Biên gộp 2024")
    ax.plot(x24, df2024["operating_margin_pct"].values, "s-",
            color=PALETTE["secondary"], linewidth=2, markersize=5, label="Biên EBIT 2024")
    ax.plot(x23, df2023["gross_margin_pct"].values, "o--",
            color=PALETTE["primary"], linewidth=1.2, markersize=4, alpha=0.5, label="Biên gộp 2023")
    ax.plot(x23, df2023["operating_margin_pct"].values, "s--",
            color=PALETTE["secondary"], linewidth=1.2, markersize=4, alpha=0.5, label="Biên EBIT 2023")

    ax.axhline(15.0, color=PALETTE["positive"], linestyle=":", linewidth=1.5,
               label="Mục tiêu Q4: 15%")
    ax.set_xticks(x24)
    ax.set_xticklabels(month_labels, fontsize=8)
    ax.set_ylabel("Biên lợi nhuận (%)")
    ax.set_title("Xu hướng biên lợi nhuận\n(COGS tăng nhanh hơn doanh thu)")
    ax.legend(fontsize=7)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))

    # Annotate declining trend
    gm_start = df2024["gross_margin_pct"].iloc[0]
    gm_end = df2024["gross_margin_pct"].iloc[-1]
    ax.annotate(
        f"Giảm {gm_start:.0f}% → {gm_end:.0f}%",
        xy=(len(df2024) - 1, gm_end),
        xytext=(len(df2024) - 3, gm_end + 3),
        arrowprops=dict(arrowstyle="->", color=PALETTE["negative"]),
        fontsize=8, color=PALETTE["negative"], fontweight="bold",
    )

    # Right: Waterfall actual Q1-Q3 vs Q4 target
    ax = axes[2]
    q1_rev = df2024[df2024["month"].isin([1, 2, 3])]["net_revenue"].sum() / 1e9
    q2_rev = df2024[df2024["month"].isin([4, 5, 6])]["net_revenue"].sum() / 1e9
    q3_rev = df2024[df2024["month"].isin([7, 8, 9])]["net_revenue"].sum() / 1e9
    q4_target = 30.0  # tỷ

    labels = ["Q1/2024\nThực tế", "Q2/2024\nThực tế", "Q3/2024\nThực tế",
              "Q4/2024\nMục tiêu"]
    values = [q1_rev, q2_rev, q3_rev, q4_target]
    colors = [PALETTE["primary"], PALETTE["positive"], PALETTE["accent"], PALETTE["secondary"]]

    bars = ax.bar(labels, values, color=colors, alpha=0.85, edgecolor="white", linewidth=0.5)

    # Hatching on Q4 target (it's a forecast)
    bars[3].set_hatch("//")
    bars[3].set_edgecolor(PALETTE["secondary"])
    bars[3].set_linewidth(1.5)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f"{val:.1f}B", ha="center", va="bottom", fontsize=9, fontweight="bold")

    q4_profit_needed = q4_target * 0.15
    ax.text(
        0.97, 0.97,
        f"Mục tiêu Q4:\n30 tỷ doanh thu\n15% biên lợi nhuận\n→ Lợi nhuận: {q4_profit_needed:.1f}B",
        transform=ax.transAxes, ha="right", va="top", fontsize=8,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#e8f5e9", edgecolor=PALETTE["positive"],
                  alpha=0.9),
    )

    ax.set_ylabel("Doanh thu thuần (tỷ VND)")
    ax.set_title("Thực tế Q1-Q3 vs Mục tiêu Q4\n(cột có gạch = dự báo)")
    ax.set_ylim(0, max(values) * 1.25)

    plt.tight_layout()
    save_fig(fig, "chart-10-finance-pl.png", img_dir=IMG_CH05)


def chart_11_operations_dashboard(df: pd.DataFrame) -> None:
    """
    3 subplots (14×6):
    Left:   Dual-axis line (delivery time + fulfillment rate)
    Middle: NPS trend with regression trendline annotation
    Right:  Return rate by month with Jul spike highlighted
    """
    # Aggregate to monthly
    df["month"] = df["date"].dt.to_period("M")
    monthly = df.groupby("month").agg(
        delivery_time_avg_days=("delivery_time_avg_days", "mean"),
        warehouse_fulfillment_rate_pct=("warehouse_fulfillment_rate_pct", "mean"),
        nps_score=("nps_score", "mean"),
        return_rate_pct=("return_rate_pct", "mean"),
        customer_complaints=("customer_complaints", "sum"),
    ).reset_index()

    month_labels = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]
    x = np.arange(len(monthly))

    fig, axes = plt.subplots(1, 3, figsize=(14, 6))
    fig.suptitle(
        "Lens #11: VẬN HÀNH — Giao hàng, NPS & Tỷ lệ hoàn trả 2024",
        fontsize=13, fontweight="bold"
    )

    # Left: Dual-axis delivery time + fulfillment rate
    ax1 = axes[0]
    color_dt = PALETTE["primary"]
    color_fr = PALETTE["positive"]

    line1 = ax1.plot(x, monthly["delivery_time_avg_days"], "o-",
                     color=color_dt, linewidth=2, markersize=6,
                     label="Thời gian giao (ngày)")
    ax1.set_ylabel("Thời gian giao hàng TB (ngày)", color=color_dt)
    ax1.tick_params(axis="y", labelcolor=color_dt)
    ax1.set_ylim(0, monthly["delivery_time_avg_days"].max() * 1.4)

    ax1b = ax1.twinx()
    line2 = ax1b.plot(x, monthly["warehouse_fulfillment_rate_pct"], "s--",
                      color=color_fr, linewidth=2, markersize=6,
                      label="Tỷ lệ hoàn thành kho (%)")
    ax1b.set_ylabel("Tỷ lệ hoàn thành kho (%)", color=color_fr)
    ax1b.tick_params(axis="y", labelcolor=color_fr)
    ax1b.set_ylim(50, 105)

    # Annotate flash sale drop
    apr_idx = 3  # T4
    ax1b.annotate(
        "Flash sale:\ncông suất quá tải",
        xy=(apr_idx, monthly["warehouse_fulfillment_rate_pct"].iloc[apr_idx]),
        xytext=(apr_idx - 1.2, monthly["warehouse_fulfillment_rate_pct"].iloc[apr_idx] - 8),
        arrowprops=dict(arrowstyle="->", color=PALETTE["accent"]),
        fontsize=7.5, color=PALETTE["accent"],
    )

    ax1.set_xticks(x)
    ax1.set_xticklabels(month_labels, fontsize=8)
    ax1.set_title("Thời gian giao hàng & Tỷ lệ\nhoàn thành kho theo tháng")

    lines = line1 + line2
    labs = [l.get_label() for l in lines]
    ax1.legend(lines, labs, fontsize=7, loc="lower left")

    # Middle: NPS trend with trendline
    ax = axes[1]
    ax.plot(x, monthly["nps_score"], "o-", color=PALETTE["primary"],
            linewidth=2, markersize=7, label="NPS hàng tháng", zorder=3)
    ax.fill_between(x, monthly["nps_score"], alpha=0.12, color=PALETTE["primary"])

    # Linear trendline
    coeffs = np.polyfit(x, monthly["nps_score"], 1)
    trend_line = np.poly1d(coeffs)(x)
    ax.plot(x, trend_line, "--", color=PALETTE["negative"], linewidth=1.8,
            label=f"Xu hướng ({coeffs[0]:+.2f}/tháng)")

    # Reference lines
    ax.axhline(50, color=PALETTE["positive"], linestyle=":", linewidth=1, alpha=0.7,
               label="NPS tốt (≥50)")
    ax.axhline(0, color=PALETTE["neutral"], linestyle=":", linewidth=0.8, alpha=0.5)

    # Annotate start and end NPS
    nps_start = monthly["nps_score"].iloc[0]
    nps_end = monthly["nps_score"].iloc[-1]
    ax.annotate(f"Đầu kỳ: {nps_start:.0f}", xy=(0, nps_start),
                xytext=(0.5, nps_start + 2), fontsize=8,
                arrowprops=dict(arrowstyle="->", color=PALETTE["neutral"]))
    ax.annotate(f"Cuối kỳ: {nps_end:.0f}", xy=(len(x) - 1, nps_end),
                xytext=(len(x) - 2.5, nps_end - 3.5), fontsize=8,
                color=PALETTE["negative"],
                arrowprops=dict(arrowstyle="->", color=PALETTE["negative"]))

    ax.set_xticks(x)
    ax.set_xticklabels(month_labels, fontsize=8)
    ax.set_ylabel("NPS Score")
    ax.set_title("Xu hướng NPS đang giảm\n(Cần hành động cải thiện trải nghiệm)")
    ax.legend(fontsize=7)
    ax.set_ylim(monthly["nps_score"].min() - 5, monthly["nps_score"].max() + 8)

    # Right: Return rate by month + Jul spike
    ax = axes[2]
    bar_colors = [
        PALETTE["negative"] if monthly["return_rate_pct"].iloc[i] ==
        monthly["return_rate_pct"].max() else PALETTE["primary"]
        for i in range(len(monthly))
    ]
    bars = ax.bar(x, monthly["return_rate_pct"], color=bar_colors, alpha=0.85,
                  edgecolor="white", linewidth=0.5)

    # Annotate Jul spike
    jul_idx = 6  # T7
    jul_val = monthly["return_rate_pct"].iloc[jul_idx]
    ax.annotate(
        f"T7: {jul_val:.1f}%\nSự cố hệ thống!",
        xy=(jul_idx, jul_val),
        xytext=(jul_idx + 0.8, jul_val - 1.5),
        arrowprops=dict(arrowstyle="->", color=PALETTE["negative"]),
        fontsize=8, color=PALETTE["negative"], fontweight="bold",
    )

    # Average line
    avg_return = monthly["return_rate_pct"].mean()
    ax.axhline(avg_return, color=PALETTE["accent"], linestyle="--", linewidth=1.5,
               label=f"TB: {avg_return:.1f}%")

    # Value labels on bars
    for bar, val in zip(bars, monthly["return_rate_pct"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=7.5)

    ax.set_xticks(x)
    ax.set_xticklabels(month_labels, fontsize=8)
    ax.set_ylabel("Tỷ lệ hoàn trả (%)")
    ax.set_title("Tỷ lệ hoàn trả theo tháng\n(T7: đột biến do sự cố hệ thống)")
    ax.legend(fontsize=8)
    ax.set_ylim(0, monthly["return_rate_pct"].max() * 1.3)

    plt.tight_layout()
    save_fig(fig, "chart-11-operations-dashboard.png", img_dir=IMG_CH05)
