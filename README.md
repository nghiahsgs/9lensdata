# Andie và Những Con Số Biết Nói
### Sách phân tích dữ liệu — Bản Markdown (dễ chỉnh sửa)

---

## Cấu trúc thư mục

```
book/
├── README.md                    ← File này
├── chapters/
│   ├── 00-loi-mo-dau.md
│   ├── 01-ngay-dau-tien.md      ← Lens #1 Completeness + #2 Distribution
│   ├── 02-thang-3-giam.md       ← Lens #3 Outliers + #4 Timeline
│   ├── 03-khach-hang-quan-trong.md  ← Lens #5 Concentration + #8 Segmentation
│   ├── 04-correlation-volatility.md ← Lens #6 Correlation + #9 Volatility
│   ├── 05-ke-chuyen-dung-nguoi.md   ← Lens #7 Comparison + Storytelling
│   └── 06-master-framework.md   ← Tổng hợp 9 Lens
└── images/
    ├── chart-01-completeness.png
    ├── chart-02-distribution.png
    ├── chart-03-timeline-outliers.png
    ├── chart-04-concentration.png
    ├── chart-05-correlation.png
    ├── chart-06-comparison.png
    ├── chart-07-segmentation.png
    └── chart-08-volatility.png
```

---

## 9 Lens Bất Biến

| # | Lens | Câu hỏi cốt lõi | Chapter |
|---|------|-----------------|---------|
| 1 | COMPLETENESS | Data có ở đó không? | Ch.01 |
| 2 | DISTRIBUTION | Data trông như thế nào? | Ch.01 |
| 3 | OUTLIERS | Có gì bất thường không? | Ch.02 |
| 4 | TIMELINE | Xu hướng đi về đâu? | Ch.02 |
| 5 | CONCENTRATION | 80% đến từ 20% nào? | Ch.03 |
| 6 | CORRELATION | Thứ gì liên quan thứ gì? | Ch.04 |
| 7 | COMPARISON | Tốt hay xấu so với gì? | Ch.05 |
| 8 | SEGMENTATION | Average che giấu gì? | Ch.03 |
| 9 | VOLATILITY | Ổn định hay lung tung? | Ch.04 |

---

## Cách đọc & chỉnh sửa

**Đọc bằng Obsidian** (khuyến nghị):
1. Mở Obsidian → Open Folder as Vault → chọn thư mục `book/`
2. Ảnh hiển thị inline tự động

**Đọc bằng VS Code**:
1. Mở thư mục `book/`
2. Cài extension **Markdown Preview Enhanced**
3. Ctrl+Shift+V để preview

**Chỉnh sửa**:
- Sửa text: mở file `.md` tương ứng bằng bất kỳ text editor nào
- Thay chart: swap file PNG trong `images/` (giữ nguyên tên file)
- Thêm chapter: tạo file mới trong `chapters/`, đặt tên theo số thứ tự

---

## Ghi chú kỹ thuật

- Ảnh dùng **relative path**: `../images/chart-01.png`
- Mọi chart đều có caption bên dưới dạng `*Hình X: ...*`
- Pause boxes dùng blockquote `> ⏸ ...`
- Lens tags dùng blockquote styled `> 🔭 ...`
- Framework boxes dùng code block hoặc blockquote
