"""
chart_helpers.py — Shared utilities for generate-charts.py.
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

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
IMG_DIR = ROOT / "images"

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


def save_fig(fig: plt.Figure, filename: str, dpi: int = 150) -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    path = IMG_DIR / filename
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
    df = pd.read_csv(DATA_DIR / "techmart-orders-mar2024.csv", encoding="utf-8-sig")
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


def load_full2024() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "techmart-orders-full2024.csv", encoding="utf-8-sig")
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


def load_customers() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "techmart-customers.csv", encoding="utf-8-sig")
