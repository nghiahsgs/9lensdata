"""
generate-pdf.py — Combine all chapters into a single PDF book.

Uses pandoc (markdown → HTML) + weasyprint (HTML → PDF).
Handles Vietnamese text, embedded images, and professional styling.

Usage:
  .venv/bin/python3 scripts/generate-pdf.py
  # Output: output/9lensdata-book.pdf
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUTPUT_DIR = ROOT / "output"
OUTPUT_PDF = OUTPUT_DIR / "9lensdata-book.pdf"
CHAPTERS_DIR = ROOT / "chapters"

# Chapter order
CHAPTERS = [
    "00-loi-mo-dau",
    "01-ngay-dau-tien",
    "02-thang-3-giam",
    "03-khach-hang-quan-trong",
    "04-correlation-volatility",
    "05-ke-chuyen-dung-nguoi",
    "06-master-framework",
]

# CSS for professional book styling with Vietnamese font support
BOOK_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,700;1,400&display=swap');

@page {
    size: A4;
    margin: 2.5cm 2cm;
    @bottom-center { content: counter(page); font-size: 10pt; color: #666; }
}

body {
    font-family: 'Noto Sans', 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #1a1a1a;
    max-width: 100%;
}

h1 {
    font-size: 24pt;
    color: #2E86AB;
    border-bottom: 3px solid #2E86AB;
    padding-bottom: 8px;
    page-break-before: always;
    margin-top: 0;
}

h1:first-of-type { page-break-before: avoid; }

h2 {
    font-size: 16pt;
    color: #333;
    margin-top: 1.5em;
}

h3 { font-size: 13pt; color: #555; }

img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 9.5pt;
}

th, td {
    border: 1px solid #ddd;
    padding: 6px 10px;
    text-align: left;
}

th { background-color: #2E86AB; color: white; font-weight: 700; }
tr:nth-child(even) { background-color: #f8f9fa; }

blockquote {
    border-left: 4px solid #F18F01;
    margin: 1.2em 0;
    padding: 0.8em 1.2em;
    background-color: #fff8f0;
    border-radius: 0 4px 4px 0;
    font-style: italic;
}

code {
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 9.5pt;
}

pre {
    background-color: #1e1e1e;
    color: #d4d4d4;
    padding: 1em;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.5;
}

pre code { background: none; color: inherit; padding: 0; }

hr {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 2em 0;
}

em { color: #555; }
strong { color: #1a1a1a; }
"""


def build_combined_markdown() -> str:
    """Read all chapter README.md files and combine, fixing image paths."""
    parts = []
    for ch_name in CHAPTERS:
        ch_dir = CHAPTERS_DIR / ch_name
        md_file = ch_dir / "README.md"
        if not md_file.exists():
            print(f"  WARN: {md_file} not found, skipping")
            continue

        content = md_file.read_text(encoding="utf-8")

        # Fix image paths: ./images/xxx.png → absolute path for weasyprint
        img_dir = ch_dir / "images"
        content = content.replace("./images/", f"{img_dir}/")

        # Fix cross-chapter links (not clickable in PDF, just clean up)
        for other_ch in CHAPTERS:
            content = content.replace(f"../{other_ch}/", "#")

        parts.append(content)

    return "\n\n---\n\n".join(parts)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Write CSS
    css_file = OUTPUT_DIR / "book.css"
    css_file.write_text(BOOK_CSS, encoding="utf-8")
    print(f"  CSS → {css_file}")

    # Combine markdown
    print("Combining chapters...")
    combined_md = build_combined_markdown()
    combined_file = OUTPUT_DIR / "combined.md"
    combined_file.write_text(combined_md, encoding="utf-8")
    print(f"  Markdown → {combined_file} ({len(combined_md):,} chars)")

    # Pandoc: markdown → HTML
    print("Converting markdown → HTML (pandoc)...")
    html_file = OUTPUT_DIR / "book.html"
    subprocess.run([
        "pandoc", str(combined_file),
        "-f", "markdown",
        "-t", "html5",
        "--standalone",
        "--css", str(css_file),
        "--metadata", "title=Andie va Nhung Con So Biet Noi",
        "-o", str(html_file),
    ], check=True)
    print(f"  HTML → {html_file}")

    # WeasyPrint: HTML → PDF
    print("Converting HTML → PDF (weasyprint)...")
    subprocess.run([
        "weasyprint", str(html_file), str(OUTPUT_PDF),
    ], check=True)

    size_mb = OUTPUT_PDF.stat().st_size / (1024 * 1024)
    print(f"\n  PDF → {OUTPUT_PDF} ({size_mb:.1f} MB)")
    print("Done!")


if __name__ == "__main__":
    main()
