"""
data_generators_extra.py — Extra TechMart datasets for Ch.4 (Marketing) and Ch.5 (Finance/Ops).
Imported by generate-data.py — not run directly.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date

RNG = np.random.default_rng(99)

# ── constants ─────────────────────────────────────────────────────────────────

CHANNELS = ["Facebook", "Google", "TikTok", "Email", "SMS", "Affiliate"]
TARGET_SEGMENTS = ["New", "Returning", "VIP", "Win-back"]

# Holiday periods (confounding variable)
HOLIDAYS_2024 = [
    (date(2024, 1, 27), date(2024, 2, 10)),   # Tết Nguyên Đán
    (date(2024, 3, 8), date(2024, 3, 10)),     # 8/3
    (date(2024, 4, 28), date(2024, 5, 5)),     # 30/4 - 1/5
    (date(2024, 9, 1), date(2024, 9, 5)),      # Back to school
]

# Channel characteristics (budget share, ROAS profile, variance)
CHANNEL_CONFIG = {
    "Facebook":  {"budget_share": 0.32, "roas_mu": 1.8,  "roas_sigma": 0.5,  "cac_base": 180_000},
    "Google":    {"budget_share": 0.28, "roas_mu": 2.5,  "roas_sigma": 0.4,  "cac_base": 150_000},
    "TikTok":    {"budget_share": 0.18, "roas_mu": 2.1,  "roas_sigma": 1.2,  "cac_base": 130_000},
    "Email":     {"budget_share": 0.08, "roas_mu": 4.2,  "roas_sigma": 0.6,  "cac_base": 45_000},
    "SMS":       {"budget_share": 0.06, "roas_mu": 2.8,  "roas_sigma": 0.5,  "cac_base": 60_000},
    "Affiliate": {"budget_share": 0.08, "roas_mu": 3.1,  "roas_sigma": 0.7,  "cac_base": 90_000},
}

TOTAL_BUDGET_VND = 2_400_000_000  # 2.4 tỷ across 9 months


def _is_holiday(d: date) -> bool:
    for start, end in HOLIDAYS_2024:
        if start <= d <= end:
            return True
    return False


def _campaign_name(channel: str, idx: int, month: int) -> str:
    prefix_map = {
        "Facebook": "FB",
        "Google":   "GG",
        "TikTok":   "TT",
        "Email":    "EM",
        "SMS":      "SM",
        "Affiliate": "AF",
    }
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{prefix_map[channel]}-{month_names[month-1]}-{idx:03d}"


# ── Dataset A: Marketing campaigns ───────────────────────────────────────────

def generate_marketing_campaigns(n: int = 500) -> pd.DataFrame:
    """
    ~500 campaign-level rows for Jan-Sep 2024.
    Key insights:
    - Facebook high spend, low ROAS (r~0.7 email conversion correlation)
    - Email low spend, highest ROAS
    - TikTok high variance
    - Holiday confounding: both high spend AND high conversion during holidays
    """
    rows = []
    campaign_idx = {ch: 1 for ch in CHANNELS}

    months = list(range(1, 10))  # Jan-Sep 2024
    # distribute ~500 campaigns across 9 months and 6 channels
    campaigns_per_cell = n // (len(months) * len(CHANNELS))
    extra = n - campaigns_per_cell * len(months) * len(CHANNELS)

    campaign_id = 1
    for month in months:
        days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30][month - 1]  # 2024 leap year
        for ch_idx, channel in enumerate(CHANNELS):
            cfg = CHANNEL_CONFIG[channel]
            count = campaigns_per_cell + (1 if campaign_id <= extra else 0)

            for _ in range(count):
                # campaign duration: 7-30 days
                duration = int(RNG.integers(7, 31))
                start_day = int(RNG.integers(1, max(2, days_in_month - duration + 1)))
                start_dt = date(2024, month, start_day)
                end_dt = date(2024, month, min(start_day + duration - 1, days_in_month))

                # check if campaign overlaps holiday
                is_hol = any(_is_holiday(start_dt + timedelta(days=d))
                             for d in range((end_dt - start_dt).days + 1))

                # budget allocation per campaign
                channel_monthly_budget = TOTAL_BUDGET_VND * cfg["budget_share"] / 9
                budget_variance = RNG.uniform(0.6, 1.4)
                budget_vnd = int(channel_monthly_budget / max(1, campaigns_per_cell) * budget_variance)
                budget_vnd = max(5_000_000, budget_vnd)

                # spend: 70-105% of budget
                spend_pct = RNG.uniform(0.70, 1.05)
                spend_vnd = int(budget_vnd * spend_pct)

                # impressions based on channel scale and spend
                cpm_map = {"Facebook": 45, "Google": 38, "TikTok": 28, "Email": 12, "SMS": 8, "Affiliate": 35}
                cpm = cpm_map[channel]
                impressions = int(spend_vnd / 1000 * (1000 / cpm) * RNG.uniform(0.85, 1.15))

                # CTR by channel (Email/SMS much higher, TikTok variable)
                ctr_base = {"Facebook": 1.8, "Google": 3.5, "TikTok": 2.8, "Email": 18.0, "SMS": 12.0, "Affiliate": 2.2}
                ctr_pct = float(np.clip(
                    ctr_base[channel] + RNG.normal(0, ctr_base[channel] * 0.3),
                    0.5, 40.0
                ))
                clicks = int(impressions * ctr_pct / 100)

                # ROAS: holiday boosts ROAS by confounding (not caused by campaign)
                holiday_boost = 1.4 if is_hol else 1.0
                roas_raw = RNG.normal(cfg["roas_mu"], cfg["roas_sigma"])
                # TikTok: high variance (more extremes)
                if channel == "TikTok":
                    roas_raw = roas_raw * RNG.choice([0.5, 1.0, 1.5, 2.0],
                                                     p=[0.2, 0.4, 0.25, 0.15])
                roas = float(np.clip(roas_raw * holiday_boost, 0.3, 12.0))

                revenue_generated = int(spend_vnd * roas)

                # conversion rate 1-8% of clicks
                conv_rate_base = {"Facebook": 0.025, "Google": 0.04, "TikTok": 0.03,
                                  "Email": 0.08, "SMS": 0.06, "Affiliate": 0.035}
                conv_rate = float(np.clip(
                    conv_rate_base[channel] * holiday_boost * RNG.uniform(0.7, 1.3),
                    0.005, 0.15
                ))
                conversions = max(0, int(clicks * conv_rate))

                # CAC: revenue / conversions if conversions > 0
                if conversions > 0:
                    cac = int(spend_vnd / conversions)
                else:
                    cac = int(cfg["cac_base"] * RNG.uniform(1.5, 3.0))

                target_seg = RNG.choice(TARGET_SEGMENTS, p=[0.35, 0.30, 0.15, 0.20])

                rows.append({
                    "campaign_id":        f"CMP{campaign_id:05d}",
                    "campaign_name":      _campaign_name(channel, campaign_idx[channel], month),
                    "channel":            channel,
                    "start_date":         start_dt.strftime("%Y-%m-%d"),
                    "end_date":           end_dt.strftime("%Y-%m-%d"),
                    "budget_vnd":         budget_vnd,
                    "spend_vnd":          spend_vnd,
                    "impressions":        impressions,
                    "clicks":             clicks,
                    "ctr_pct":            round(ctr_pct, 2),
                    "conversions":        conversions,
                    "revenue_generated":  revenue_generated,
                    "cac":                cac,
                    "roas":               round(roas, 3),
                    "target_segment":     target_seg,
                    "is_holiday_period":  is_hol,
                })
                campaign_idx[channel] += 1
                campaign_id += 1

    df = pd.DataFrame(rows)
    # shuffle rows
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


# ── Dataset B: Finance P&L monthly ───────────────────────────────────────────

def generate_finance_monthly() -> pd.DataFrame:
    """
    18 rows: Jan-Sep 2023 (YoY baseline) + Jan-Sep 2024.
    Key patterns:
    - Revenue growing YoY but margins shrinking (COGS increasing faster)
    - Marketing spend % of revenue rising 8% → 12%
    - Q2 2024 best (flash sales), Q3 dipping
    - Operations cost stable
    """
    rows = []

    # Monthly revenue multiplier relative to Mar 2024 baseline (~8.5 tỷ)
    BASE_REVENUE = 8_500_000_000  # 8.5 tỷ

    revenue_mult = {
        (2023, 1): 0.65,
        (2023, 2): 0.78,
        (2023, 3): 0.72,
        (2023, 4): 0.80,
        (2023, 5): 0.75,
        (2023, 6): 0.70,
        (2023, 7): 0.68,
        (2023, 8): 0.74,
        (2023, 9): 0.82,
        (2024, 1): 0.88,
        (2024, 2): 1.25,   # Valentine spike
        (2024, 3): 1.00,   # baseline
        (2024, 4): 1.65,   # Apr 30 flash sale
        (2024, 5): 1.05,
        (2024, 6): 0.98,
        (2024, 7): 0.45,   # system downtime
        (2024, 8): 0.82,
        (2024, 9): 1.67,   # Sep uptrend
    }

    for (year, month), mult in revenue_mult.items():
        gross_rev = int(BASE_REVENUE * mult * RNG.uniform(0.97, 1.03))

        # Returns: 3-6% of gross
        return_rate = RNG.uniform(0.03, 0.06)
        returns = int(gross_rev * return_rate)
        net_revenue = gross_rev - returns

        # COGS: 2023 ~55%, 2024 trending up to 62% (margin squeeze)
        if year == 2023:
            cogs_pct = RNG.uniform(0.53, 0.57)
        else:
            # progressive increase Jan(58%) → Sep(62%)
            cogs_pct = 0.58 + (month - 1) * 0.004 + RNG.uniform(-0.01, 0.01)
            cogs_pct = min(cogs_pct, 0.63)

        cogs = int(net_revenue * cogs_pct)
        gross_profit = net_revenue - cogs
        gross_margin_pct = round(gross_profit / net_revenue * 100, 2)

        # Marketing spend: 2023 ~8%, 2024 rising 8%→12%
        if year == 2023:
            mkt_pct = RNG.uniform(0.078, 0.085)
        else:
            mkt_pct = 0.08 + (month - 1) * 0.004 + RNG.uniform(-0.005, 0.005)
            mkt_pct = min(mkt_pct, 0.125)

        marketing_spend = int(net_revenue * mkt_pct)

        # Operations: stable ~4.5% of net_revenue
        operations_cost = int(net_revenue * RNG.uniform(0.043, 0.048))

        # Salaries: roughly fixed cost ~450M/month, slight growth YoY
        salary_base = 450_000_000 if year == 2023 else 510_000_000
        salaries = int(salary_base * RNG.uniform(0.95, 1.05))

        # Other costs: 1-2%
        other_costs = int(net_revenue * RNG.uniform(0.01, 0.02))

        total_opex = marketing_spend + operations_cost + salaries + other_costs
        operating_profit = gross_profit - total_opex
        operating_margin_pct = round(operating_profit / net_revenue * 100, 2)

        # Order and customer metrics
        # Use revenue to back-calculate approximate orders
        avg_order = int(RNG.uniform(650_000, 900_000))
        order_count = int(net_revenue / avg_order)
        avg_order_value = int(net_revenue / max(1, order_count))
        customers_active = int(order_count * RNG.uniform(0.75, 0.90))

        rows.append({
            "month":                month,
            "year":                 year,
            "gross_revenue":        gross_rev,
            "returns":              returns,
            "net_revenue":          net_revenue,
            "cogs":                 cogs,
            "gross_profit":         gross_profit,
            "gross_margin_pct":     gross_margin_pct,
            "marketing_spend":      marketing_spend,
            "operations_cost":      operations_cost,
            "salaries":             salaries,
            "other_costs":          other_costs,
            "operating_profit":     operating_profit,
            "operating_margin_pct": operating_margin_pct,
            "order_count":          order_count,
            "avg_order_value":      avg_order_value,
            "customers_active":     customers_active,
        })

    return pd.DataFrame(rows)


# ── Dataset C: Operations daily ───────────────────────────────────────────────

def generate_operations_daily() -> pd.DataFrame:
    """
    ~273 rows (daily Jan-Sep 2024).
    Key patterns:
    - Delivery time bimodal: HCM/HN ~1.5d, others ~4d (shown as weighted avg)
    - Fulfillment drops during flash sales (Apr/May)
    - NPS declining 45 → 38
    - Return rate spike in Jul (system issues)
    """
    rows = []

    start = date(2024, 1, 1)
    end = date(2024, 9, 30)
    current = start

    # NPS starts at 45, declines to 38
    total_days = (end - start).days + 1
    nps_start = 45.0
    nps_end = 38.0

    day_idx = 0
    while current <= end:
        month = current.month
        day_of_year = current.timetuple().tm_yday

        # Base orders shipped — follows revenue pattern
        base_orders = {1: 380, 2: 550, 3: 430, 4: 710, 5: 450,
                       6: 420, 7: 195, 8: 355, 9: 720}.get(month, 400)
        orders_shipped = max(50, int(base_orders + RNG.normal(0, base_orders * 0.12)))

        # Delivery time: mix HCM/HN (40%+25%=65% at ~1.5d) + other (35% at ~4d)
        hcm_hn_pct = 0.65
        dt_hcm = RNG.normal(1.5, 0.3)
        dt_other = RNG.normal(4.0, 0.8)
        delivery_time_avg = round(hcm_hn_pct * dt_hcm + (1 - hcm_hn_pct) * dt_other, 2)
        delivery_time_avg = max(0.5, delivery_time_avg)

        # Fulfillment rate: drops during flash sales (Apr peak, Jul system down)
        if month == 4 and current.day >= 25:
            # Apr 30 flash sale: capacity strained
            fulfillment_base = RNG.uniform(0.78, 0.86)
        elif month == 5 and current.day <= 5:
            # Post-sale strain
            fulfillment_base = RNG.uniform(0.82, 0.90)
        elif month == 7:
            # System issues
            fulfillment_base = RNG.uniform(0.65, 0.80)
        else:
            fulfillment_base = RNG.uniform(0.92, 0.99)

        warehouse_fulfillment_rate_pct = round(float(fulfillment_base * 100), 1)

        # Delivered = shipped × fulfillment
        orders_delivered = int(orders_shipped * fulfillment_base * RNG.uniform(0.95, 1.0))

        # Return rate: normally 3-6%, spike in Jul
        if month == 7:
            return_rate = RNG.uniform(0.09, 0.15)  # spike
        elif month in [4, 5]:
            return_rate = RNG.uniform(0.05, 0.08)  # slightly higher post-sale
        else:
            return_rate = RNG.uniform(0.03, 0.06)

        return_rate_pct = round(float(return_rate * 100), 2)

        # Customer complaints proportional to orders, higher when fulfillment drops
        complaint_rate = (1 - fulfillment_base) * 0.3 + return_rate * 0.2
        customer_complaints = max(0, int(orders_shipped * complaint_rate + RNG.normal(0, 2)))

        # NPS: linear decline from 45 to 38 with noise
        nps_trend = nps_start + (nps_end - nps_start) * (day_idx / total_days)
        nps_score = round(float(np.clip(nps_trend + RNG.normal(0, 1.5), 25, 60)), 1)

        rows.append({
            "date":                           current.strftime("%Y-%m-%d"),
            "orders_shipped":                 orders_shipped,
            "orders_delivered":               orders_delivered,
            "delivery_time_avg_days":         delivery_time_avg,
            "warehouse_fulfillment_rate_pct": warehouse_fulfillment_rate_pct,
            "return_rate_pct":                return_rate_pct,
            "customer_complaints":            customer_complaints,
            "nps_score":                      nps_score,
        })

        current += timedelta(days=1)
        day_idx += 1

    return pd.DataFrame(rows)
