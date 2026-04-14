#!/usr/bin/env bash
# Build PDF from all chapter markdown files
# Usage: ./scripts/build-pdf.sh

set -e
cd "$(dirname "$0")/.."

BUILD_DIR="build"
COMBINED="$BUILD_DIR/combined.md"
OUTPUT="andie-va-nhung-con-so-biet-noi.pdf"

mkdir -p "$BUILD_DIR"

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

# Build title page + combined markdown
cat > "$COMBINED" <<'EOF'
---
title: "Andie và Những Con Số Biết Nói"
subtitle: "Sách phân tích dữ liệu — 9 Lens Bất Biến"
author: "9lensdata"
lang: vi
toc: true
toc-depth: 2
documentclass: book
geometry: margin=2.2cm
mainfont: "Helvetica"
---

\newpage

EOF

# Append each chapter, rewriting relative image paths to absolute
for ch in "${CHAPTERS[@]}"; do
  chapter_dir=$(dirname "$ch")
  # Rewrite ./images/ → chapters/XX-xxx/images/
  sed "s|](\./images/|](${chapter_dir}/images/|g" "$ch" >> "$COMBINED"
  echo -e "\n\n\\\newpage\n\n" >> "$COMBINED"
done

echo "Combined markdown: $COMBINED"
echo "Generating PDF with pandoc + weasyprint..."

pandoc "$COMBINED" \
  -o "$OUTPUT" \
  --pdf-engine=weasyprint \
  --toc \
  --toc-depth=2 \
  -V mainfont="Helvetica" \
  -V geometry:margin=2.2cm \
  --metadata lang=vi

echo "Done: $OUTPUT"
ls -lh "$OUTPUT"
