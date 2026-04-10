"""
Helper module: data generation logic for TechMart datasets.
Imported by generate-data.py — not run directly.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

RNG = np.random.default_rng(42)

# ── constants ────────────────────────────────────────────────────────────────

CATEGORIES = ["Điện Tử", "Thời Trang", "FMCG", "Gia Dụng", "Thể Thao", "Phụ Kiện"]
CITIES = ["TP.HCM", "Hà Nội", "Đà Nẵng", "Cần Thơ", "Hải Phòng"]
CITY_WEIGHTS = [0.58, 0.27, 0.07, 0.04, 0.04]
STATUSES = ["Hoàn thành", "Đã hủy", "Hoàn trả"]
STATUS_WEIGHTS = [0.853, 0.079, 0.068]

# category weights for orders (Điện Tử = 18% orders but 42% revenue)
CAT_ORDER_WEIGHTS = [0.18, 0.22, 0.20, 0.17, 0.12, 0.11]

PRODUCTS = {
    "Điện Tử": [
        "iPhone 15 Pro", "Samsung Galaxy S24", "Laptop Dell XPS 13",
        "MacBook Air M2", "iPad Pro 11", "Tai nghe Sony WH-1000XM5",
        "Smart TV Samsung 55\"", "Máy ảnh Sony A7 IV", "Apple Watch Series 9",
    ],
    "Thời Trang": [
        "Áo thun Uniqlo", "Quần jeans Levi's 501", "Đầm maxi hoa nhí",
        "Giày Nike Air Max", "Túi xách Coach", "Áo khoác bomber",
        "Váy công sở", "Sandal Birkenstock",
    ],
    "FMCG": [
        "Dầu gội Dove 650ml", "Sữa tắm Nivea", "Kem đánh răng Colgate",
        "Nước giặt OMO 3.7kg", "Sữa Vinamilk 1L", "Mì Hảo Hảo thùng 30 gói",
        "Nước mắm Phú Quốc 1L", "Dầu ăn Simply 5L",
    ],
    "Gia Dụng": [
        "Nồi cơm điện Cuckoo", "Máy lọc không khí Xiaomi", "Robot hút bụi Roomba",
        "Lò vi sóng Panasonic", "Bàn ủi hơi nước Philips", "Quạt điều hòa Casper",
        "Máy xay sinh tố Vitamix",
    ],
    "Thể Thao": [
        "Dây kéo tập gym", "Thảm yoga Decathlon", "Xe đạp Giant ATX",
        "Vợt cầu lông Yonex", "Giày chạy bộ Adidas Ultraboost",
        "Bóng đá Mikasa", "Găng tay boxing",
    ],
    "Phụ Kiện": [
        "Ốp lưng iPhone 15", "Cáp sạc nhanh USB-C", "Balo laptop 15\"",
        "Chuột không dây Logitech", "Bàn phím cơ Keychron K2",
        "Hub USB-C 7 in 1", "Giá đỡ laptop",
    ],
}

# Price config: (lo_clip, hi_clip, median_target) — log-normal mu = log(median_target)
# Calibrated so Điện Tử = 18% of orders → ~42% of revenue.
# Math: 0.18×P / (0.18×P + sum_others) = 0.42 → P ≈ 1,050,000 VND
PRICE_CONFIG = {
    "Điện Tử":    (200_000,   8_000_000, 1_050_000),
    "Thời Trang":  (80_000,   2_500_000,   350_000),
    "FMCG":        (15_000,     300_000,    65_000),
    "Gia Dụng":   (200_000,   4_000_000,   750_000),
    "Thể Thao":   (80_000,    3_000_000,   380_000),
    "Phụ Kiện":    (20_000,     800_000,   130_000),
}

QUAN_HUYEN = {
    "TP.HCM": ["Q.1", "Q.3", "Q.7", "Q.Bình Thạnh", "Q.Tân Bình", "Q.Gò Vấp", "Q.12"],
    "Hà Nội": ["Hoàn Kiếm", "Đống Đa", "Ba Đình", "Cầu Giấy", "Hoàng Mai", "Long Biên"],
    "Đà Nẵng": ["Hải Châu", "Thanh Khê", "Ngũ Hành Sơn"],
    "Cần Thơ": ["Ninh Kiều", "Bình Thuỷ"],
    "Hải Phòng": ["Hồng Bàng", "Lê Chân", "Ngô Quyền"],
}


def _sample_price(category: str, n: int) -> np.ndarray:
    lo, hi, median_target = PRICE_CONFIG[category]
    # mu = log(median) gives correct median for log-normal
    mu = np.log(median_target)
    sigma = 0.6
    prices = RNG.lognormal(mu, sigma, n)
    return np.clip(prices, lo, hi).round(-3)  # round to nearest 1000 VND


def _make_quanhuyen(cities: pd.Series) -> pd.Series:
    """Assign quận/huyện with ~38% missing."""
    result = []
    for city in cities:
        if RNG.random() < 0.38:
            result.append(np.nan)
        else:
            options = QUAN_HUYEN.get(city, ["N/A"])
            result.append(RNG.choice(options))
    return pd.Series(result, dtype="object")


# ── Mar 2024 orders ──────────────────────────────────────────────────────────

def generate_mar2024_orders(n: int = 12_847) -> pd.DataFrame:
    """Main dataset: 12,847 rows for March 2024."""
    cats = RNG.choice(CATEGORIES, size=n, p=CAT_ORDER_WEIGHTS)
    products = [RNG.choice(PRODUCTS[c]) for c in cats]

    # quantities: 52% = 1, rest 2-10
    qty = np.ones(n, dtype=int)
    mask_multi = RNG.random(n) > 0.52
    qty[mask_multi] = RNG.integers(2, 11, size=mask_multi.sum())

    # inject 3 zero-qty test orders
    qty[:3] = 0

    prices = np.array([_sample_price(c, 1)[0] for c in cats], dtype=float)
    # inject 1 test entry with price=1000
    prices[3] = 1_000.0

    discounts = RNG.beta(1.5, 8, n).round(2)  # skewed low, mostly <20%

    revenue = qty * prices * (1 - discounts)

    # dates: uniform over 28 days of March 2024
    base = datetime(2024, 3, 1)
    days_offset = RNG.integers(0, 28, n)
    seconds_offset = RNG.integers(0, 86400, n)
    dates = [base + timedelta(days=int(d), seconds=int(s))
             for d, s in zip(days_offset, seconds_offset)]

    cities = RNG.choice(CITIES, size=n, p=CITY_WEIGHTS)
    statuses = RNG.choice(STATUSES, size=n, p=STATUS_WEIGHTS)

    # ratings: ~60% missing; unhappy customers rate more → left-skew for raters
    ratings = []
    for status in statuses:
        if RNG.random() < 0.60:
            ratings.append(np.nan)
        elif status == "Hoàn trả":
            ratings.append(float(RNG.choice([1, 2, 3], p=[0.5, 0.35, 0.15])))
        elif status == "Đã hủy":
            ratings.append(float(RNG.choice([1, 2, 3, 4], p=[0.35, 0.3, 0.25, 0.1])))
        else:
            ratings.append(float(RNG.choice([3, 4, 5], p=[0.15, 0.45, 0.40])))

    df = pd.DataFrame({
        "order_id": [f"ORD{str(i+1).zfill(6)}" for i in range(n)],
        "customer_id": [f"CUS{str(RNG.integers(1, 28001)).zfill(6)}" for _ in range(n)],
        "order_date": dates,
        "product_name": products,
        "category": cats,
        "quantity": qty,
        "unit_price": prices.astype(int),
        "discount_pct": discounts,
        "revenue": revenue.round(0).astype(int),
        "city": cities,
        "quan_huyen": _make_quanhuyen(pd.Series(cities)),
        "status": statuses,
        "rating": ratings,
    })
    return df


# ── Full 2024 + T3/2023 orders ───────────────────────────────────────────────

def _monthly_multiplier() -> dict:
    """Return revenue multipliers relative to baseline for each month."""
    return {
        (2023, 3): 0.72,   # T3/2023 for YoY
        (2024, 1): 0.88,
        (2024, 2): 1.25,   # Valentine spike
        (2024, 3): 1.00,   # baseline
        (2024, 4): 1.65,   # Apr 30 flash sale +180% on last 2 days → monthly ~+65%
        (2024, 5): 1.05,
        (2024, 6): 0.98,
        (2024, 7): 0.45,   # system downtime -55%
        (2024, 8): 0.82,
        (2024, 9): 1.67,   # Sep uptrend +67%
    }


def generate_full2024_orders() -> pd.DataFrame:
    """Monthly aggregated data for timeline analysis (Ch.2)."""
    mults = _monthly_multiplier()
    base_orders_per_month = 12_847
    rows = []
    for (year, month), mult in mults.items():
        import calendar
        days_in_month = calendar.monthrange(year, month)[1]
        n = max(1, int(base_orders_per_month * mult))
        base = datetime(year, month, 1)
        cats = RNG.choice(CATEGORIES, size=n, p=CAT_ORDER_WEIGHTS)
        products = [RNG.choice(PRODUCTS[c]) for c in cats]
        qty = np.ones(n, dtype=int)
        mask = RNG.random(n) > 0.52
        qty[mask] = RNG.integers(2, 11, size=mask.sum())
        prices = np.array([_sample_price(c, 1)[0] for c in cats], dtype=float)
        discounts = RNG.beta(1.5, 8, n).round(2)
        revenue = qty * prices * (1 - discounts)
        days_off = RNG.integers(0, days_in_month, n)
        secs_off = RNG.integers(0, 86400, n)
        dates = [base + timedelta(days=int(d), seconds=int(s))
                 for d, s in zip(days_off, secs_off)]
        cities = RNG.choice(CITIES, size=n, p=CITY_WEIGHTS)
        statuses = RNG.choice(STATUSES, size=n, p=STATUS_WEIGHTS)
        for i in range(n):
            rows.append({
                "order_id": f"ORD-{year}{str(month).zfill(2)}-{str(i+1).zfill(5)}",
                "customer_id": f"CUS{str(RNG.integers(1, 28001)).zfill(6)}",
                "order_date": dates[i],
                "product_name": products[i],
                "category": cats[i],
                "quantity": int(qty[i]),
                "unit_price": int(prices[i]),
                "discount_pct": float(discounts[i]),
                "revenue": int(round(revenue[i])),
                "city": cities[i],
                "status": statuses[i],
            })
    return pd.DataFrame(rows)


# ── Customers ─────────────────────────────────────────────────────────────────

RFM_SEGMENTS = {
    "Champions":          1_240,
    "Loyal":              2_890,
    "Potential Loyalists": 3_210,
    "At Risk":            1_670,
    "Hibernating":        4_990,
    "Lost":              14_000,   # bumped 13k→14k so total = 28,000
}

# revenue share per segment (Champions+Loyal dominate)
SEG_REV_SHARE = {
    "Champions":          0.30,
    "Loyal":              0.25,
    "Potential Loyalists": 0.15,
    "At Risk":            0.10,
    "Hibernating":        0.12,
    "Lost":               0.08,
}


def _city_for_customer(n: int) -> np.ndarray:
    """City distribution with Simpson's Paradox built-in."""
    return RNG.choice(CITIES, size=n, p=CITY_WEIGHTS)


def generate_customers(n: int = 28_000) -> pd.DataFrame:
    """Customer-level data for RFM analysis."""
    total_revenue_pool = 887_000 * 12_847  # approx total revenue

    rows = []
    cid = 1
    for seg, count in RFM_SEGMENTS.items():
        seg_revenue = total_revenue_pool * SEG_REV_SHARE[seg]
        avg_rev = seg_revenue / count

        # recency: champions = recent, lost = old
        # churn_risk calibration targets (churn_risk < 0.5 = retained):
        # Champions(1240)~100% retained, Loyal(2890)~95%, PotLoy(3210)~80%
        # AtRisk(1670)~40%, Hibernating(4990)~20%, Lost(14000)~10%
        # Weighted: (1240+2745+2568+668+998+1400)/28000 ≈ 9619/28000 ≈ 34%
        # +Simpson adj raises TP.HCM slightly lower, Other higher → overall ~36-40%
        if seg == "Champions":
            last_days_ago = RNG.integers(1, 15, count)
            first_days_ago = RNG.integers(180, 730, count)
            orders_mu, orders_sigma = 18, 6
            churn_mu, churn_sigma = 0.10, 0.06   # ~100% below 0.5
        elif seg == "Loyal":
            last_days_ago = RNG.integers(7, 45, count)
            first_days_ago = RNG.integers(365, 1095, count)
            orders_mu, orders_sigma = 12, 4
            churn_mu, churn_sigma = 0.20, 0.08   # ~98% below 0.5
        elif seg == "Potential Loyalists":
            last_days_ago = RNG.integers(14, 60, count)
            first_days_ago = RNG.integers(60, 365, count)
            orders_mu, orders_sigma = 4, 2
            churn_mu, churn_sigma = 0.35, 0.10   # ~85% below 0.5
        elif seg == "At Risk":
            last_days_ago = RNG.integers(60, 120, count)
            first_days_ago = RNG.integers(180, 730, count)
            orders_mu, orders_sigma = 6, 3
            churn_mu, churn_sigma = 0.55, 0.12   # ~40% below 0.5
        elif seg == "Hibernating":
            last_days_ago = RNG.integers(120, 365, count)
            first_days_ago = RNG.integers(365, 1095, count)
            orders_mu, orders_sigma = 3, 2
            churn_mu, churn_sigma = 0.65, 0.12   # ~20% below 0.5
        else:  # Lost
            last_days_ago = RNG.integers(365, 730, count)
            first_days_ago = RNG.integers(730, 1825, count)
            orders_mu, orders_sigma = 2, 1
            churn_mu, churn_sigma = 0.80, 0.10   # ~10% below 0.5

        ref_date = datetime(2024, 3, 28)
        last_purchase = [ref_date - timedelta(days=int(d)) for d in last_days_ago]
        first_purchase = [ref_date - timedelta(days=int(d)) for d in first_days_ago]

        total_orders = np.maximum(1, RNG.normal(orders_mu, orders_sigma, count).astype(int))
        # revenue: log-normal around avg_rev
        total_rev = RNG.lognormal(np.log(max(avg_rev, 1)), 0.6, count).round(0).astype(int)
        avg_order_val = (total_rev / total_orders).round(0).astype(int)

        cities = _city_for_customer(count)
        # Simpson's Paradox: TP.HCM retention 38% (higher churn), HN 41%, Other 52%
        # Positive churn_adj = more churn = lower retention
        churn_adj = np.where(cities == "TP.HCM",  0.05,   # higher churn
                    np.where(cities == "Hà Nội",   0.02,   # slightly higher churn
                                                  -0.08))  # Other: lower churn
        churn_score = np.clip(
            RNG.normal(churn_mu, churn_sigma, count) + churn_adj, 0.01, 0.99
        ).round(3)

        for i in range(count):
            rows.append({
                "customer_id": f"CUS{str(cid).zfill(6)}",
                "first_purchase": first_purchase[i].strftime("%Y-%m-%d"),
                "last_purchase": last_purchase[i].strftime("%Y-%m-%d"),
                "total_orders": int(total_orders[i]),
                "total_revenue": int(total_rev[i]),
                "avg_order_value": int(avg_order_val[i]),
                "city": cities[i],
                "rfm_segment": seg,
                "churn_risk": float(churn_score[i]),
            })
            cid += 1

    df = pd.DataFrame(rows)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df
