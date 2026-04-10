"""
shared/chart_helpers.py — Shared utilities for generate-charts.py.
Handles data loading, styling setup, and reusable plot primitives.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# ── paths ────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.parent.parent
CHAPTERS = ROOT / "chapters"

# Per-chapter data directories
DATA_DIR = CHAPTERS / "01-ngay-dau-tien" / "data"  # default (orders-mar2024)

# Per-chapter data paths (used by loaders)
DATA_CH01 = CHAPTERS / "01-ngay-dau-tien" / "data"
DATA_CH02 = CHAPTERS / "02-thang-3-giam" / "data"
DATA_CH03 = CHAPTERS / "03-khach-hang-quan-trong" / "data"
DATA_CH04 = CHAPTERS / "04-correlation-volatility" / "data"
DATA_CH05 = CHAPTERS / "05-ke-chuyen-dung-nguoi" / "data"

# Per-chapter image directories
IMG_CH01 = CHAPTERS / "01-ngay-dau-tien" / "images"
IMG_CH02 = CHAPTERS / "02-thang-3-giam" / "images"
IMG_CH03 = CHAPTERS / "03-khach-hang-quan-trong" / "images"
IMG_CH04 = CHAPTERS / "04-correlation-volatility" / "images"
IMG_CH05 = CHAPTERS / "05-ke-chuyen-dung-nguoi" / "images"

# IMG_DIR kept for backward-compat in generate-charts.py summary scan
IMG_DIR = CHAPTERS  # not used for saving; each chart uses its own chapter IMG dir

# ── style ────────────────────────────────────────────────────────────────────

PALETTE = {
    "primary":   "#2E86AB",
    "secondary": "#A23B72",
    "accent":    "#F18F01",
    "positive":  "#44BBA4",
    "negative":  "#E94F37",
    "neutral":   "#6C757D",
}
CAT_COLORS = [
    "#2E86AB", "#A23B72", "#F18F01", "#44BBA4", "#E94F37", "#6C757D"
]

sns.set_theme(style="whitegrid", font_scale=1.0)
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "white",
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   13,
    "axes.labelsize":   11,
})


def save_fig(fig: plt.Figure, filename: str, dpi: int = 150, img_dir: Path = None) -> None:
    """Save figure to the given img_dir (or IMG_CH01 as fallback)."""
    if img_dir is None:
        img_dir = IMG_CH01
    img_dir.mkdir(parents=True, exist_ok=True)
    path = img_dir / filename
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  -> saved {path}")


def vnd_formatter(x, pos=None) -> str:
    """Format large VND numbers as 'XM' or 'XB'."""
    if x >= 1e9:
        return f"{x/1e9:.1f}B"
    if x >= 1e6:
        return f"{x/1e6:.0f}M"
    return f"{x/1e3:.0f}K"


# ── data loaders ─────────────────────────────────────────────────────────────

def load_mar2024() -> pd.DataFrame:
    df = pd.read_csv(DATA_CH01 / "techmart-orders-mar2024.csv", encoding="utf-8-sig")
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


def load_full2024() -> pd.DataFrame:
    df = pd.read_csv(DATA_CH02 / "techmart-orders-full2024.csv", encoding="utf-8-sig")
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


def load_customers() -> pd.DataFrame:
    return pd.read_csv(DATA_CH03 / "techmart-customers.csv", encoding="utf-8-sig")
