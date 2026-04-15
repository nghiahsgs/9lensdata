#!/usr/bin/env bash
# Build PDF from all chapter markdown files
# Usage: ./scripts/build-pdf.sh

set -e
cd "$(dirname "$0")/.."

BUILD_DIR="build"
COMBINED="$BUILD_DIR/combined.md"
HTML_FILE="$BUILD_DIR/book.html"
COVER_FILE="$BUILD_DIR/cover.html"
CSS_FILE="scripts/book-style.css"
OUTPUT="andie-va-nhung-con-so-biet-noi.pdf"

mkdir -p "$BUILD_DIR"

# Cover HTML — injected before TOC via --include-before-body
cat > "$COVER_FILE" <<'EOF'
<section class="cover">
  <div class="cover-eyebrow">9 Lens Bất Biến</div>
  <div class="cover-title">Andie<br/>và Những Con Số<br/>Biết Nói</div>
  <div class="cover-divider"></div>
  <div class="cover-subtitle">Sách phân tích dữ liệu<br/>qua câu chuyện của một Junior Analyst</div>
  <div class="cover-author">9LENSDATA</div>
  <div class="cover-tagline"><em>"Cuốn sách này không dạy Python. Không dạy SQL. Không dạy Excel.<br/>Cuốn sách này dạy cách nhìn."</em></div>
</section>
EOF

# Chapter order
CHAPTERS=(
  "chapters/00-loi-mo-dau/README.md"
  "chapters/01-ngay-dau-tien/README.md"
  "chapters/02-thang-3-giam/README.md"
  "chapters/03-khach-hang-quan-trong/README.md"
  "chapters/04-correlation-volatility/README.md"
  "chapters/05-ke-chuyen-dung-nguoi/README.md"
  "chapters/06-master-framework/README.md"
)

# Combined markdown — body content only (cover is injected via include-before-body)
cat > "$COMBINED" <<'EOF'
---
lang: vi
---

EOF

# Append each chapter, rewriting relative image paths to absolute
REPO_ROOT="$(pwd)"
for ch in "${CHAPTERS[@]}"; do
  chapter_dir=$(dirname "$ch")
  # Rewrite ./images/ → absolute repo path
  sed "s|](\./images/|](${REPO_ROOT}/${chapter_dir}/images/|g" "$ch" >> "$COMBINED"
  echo -e "\n\n" >> "$COMBINED"
done

echo "Combined markdown: $COMBINED"
echo "Generating PDF via pandoc → HTML → weasyprint..."

# Step 1: pandoc → standalone HTML with TOC
pandoc "$COMBINED" \
  -f markdown-implicit_figures \
  -o "$HTML_FILE" \
  --standalone \
  --toc \
  --toc-depth=2 \
  --include-before-body="$COVER_FILE" \
  --metadata lang=vi

# Post-process: strip emoji from TOC nav only (keeps body emoji intact)
python3 <<'PYEOF'
import re
path = "build/book.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# Unicode ranges: emoji + pictographs + dingbats + symbols
emoji_re = re.compile(
    "[\U0001F300-\U0001FAFF"   # misc symbols, pictographs, emoticons
    "\U00002600-\U000027BF"    # misc symbols, dingbats
    "\U0001F000-\U0001F2FF"    # playing cards, enclosed chars
    "\uFE00-\uFE0F"            # variation selectors
    "\u200D"                    # zero-width joiner
    "]+",
    flags=re.UNICODE,
)

def clean(match):
    block = match.group(0)
    return emoji_re.sub("", block)

html = re.sub(r'<nav id="TOC".*?</nav>', clean, html, flags=re.DOTALL)
with open(path, "w", encoding="utf-8") as f:
    f.write(html)
PYEOF

# Step 2: weasyprint with custom CSS
weasyprint "$HTML_FILE" "$OUTPUT" -s "$CSS_FILE" 2>&1 | grep -v "^WARNING" | grep -v "extra bytes" | grep -v "timestamp" || true

echo "Done: $OUTPUT"
ls -lh "$OUTPUT"
