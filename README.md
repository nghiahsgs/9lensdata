# Andie và Những Con Số Biết Nói
### *Sách phân tích dữ liệu — 9 Lens Bất Biến*

> *Cuốn sách này không dạy Python. Không dạy SQL. Không dạy Excel.*
> *Cuốn sách này dạy **cách nhìn**.*

---

## Cuốn sách này dành cho ai?

- **Junior analyst / fresher** vừa đi làm, mở file Excel mà không biết bắt đầu từ đâu
- **Marketer / founder / PM** phải ra quyết định dựa trên data nhưng chưa tự tin với con số
- **Sinh viên kinh tế / kỹ thuật** muốn hiểu data analytics ngoài lý thuyết khô khan
- **Bất kỳ ai** từng báo sai số trước sếp — và muốn tránh lần thứ hai

---

## Cuốn sách kể về gì?

Cuốn sách kể về **Andie** — một Junior Analyst 24 tuổi, không background kỹ thuật, ngày đầu đi làm tại TechMart (công ty e-commerce).

Qua 6 chương, bạn sẽ theo Andie từ **ngày đầu tiên** (báo sai doanh thu 14.6% trước sếp) đến **cuộc họp CEO 15 phút** (51 slide bị cắt thành 6 slide), và cuối cùng trở thành Senior Analyst truyền lại bài học cho junior mới.

Mỗi chương = **1 tình huống công việc thật** + **1-2 Lens mới** + **dataset thật để bạn tự thực hành**.

---

## 9 Lens Bất Biến

9 góc nhìn giúp bạn "nghe" data nói — apply được cho mọi ngành, mọi loại dữ liệu:

| # | Lens | Câu hỏi cốt lõi |
|---|------|-----------------|
| 1 | **COMPLETENESS** | Data có ở đó không? Thiếu ở đâu, theo pattern gì? |
| 2 | **DISTRIBUTION** | Data trông như thế nào? Shape quyết định metric. |
| 3 | **OUTLIERS** | Có gì bất thường không? Tại sao? |
| 4 | **TIMELINE** | Xu hướng đi về đâu? Trend, seasonal, hay đột biến? |
| 5 | **CONCENTRATION** | 80% kết quả đến từ 20% nào? |
| 6 | **CORRELATION** | Thứ gì liên quan thứ gì? Signal nào predict outcome? |
| 7 | **COMPARISON** | Tốt hay xấu so với gì? |
| 8 | **SEGMENTATION** | Average đang che giấu điều gì? |
| 9 | **VOLATILITY** | Ổn định hay lung tung? |

---

## Đọc sách ở đâu?

### 📖 Cách 1: Đọc online trên GitHub (dễ nhất)

Mở từng chương theo thứ tự:

1. [Lời Mở Đầu](./chapters/00-loi-mo-dau/) — Đọc trước khi bắt đầu
2. [Chương 1 — Ngày Đầu Tiên](./chapters/01-ngay-dau-tien/) · *Lens #1 Completeness + #2 Distribution*
3. [Chương 2 — Tháng 3 Doanh Số Giảm?](./chapters/02-thang-3-giam/) · *Lens #3 Outliers + #4 Timeline*
4. [Chương 3 — Khách Hàng Nào Quan Trọng Nhất?](./chapters/03-khach-hang-quan-trong/) · *Lens #5 Concentration + #8 Segmentation*
5. [Chương 4 — Cái Gì Đang Predict Cái Gì?](./chapters/04-correlation-volatility/) · *Lens #6 Correlation + #9 Volatility*
6. [Chương 5 — Kể Chuyện Đúng Với Đúng Người](./chapters/05-ke-chuyen-dung-nguoi/) · *Lens #7 Comparison + Storytelling*
7. [Chương 6 — 9 Lens Tổng Hợp](./chapters/06-master-framework/) · *Master framework + Mini cases*

### 📄 Cách 2: Tải PDF

Tải file `andie-va-nhung-con-so-biet-noi.pdf` trong [Releases](../../releases) hoặc ở thư mục gốc repo.

### 📓 Cách 3: Đọc bằng Obsidian (khuyến nghị)

1. Tải [Obsidian](https://obsidian.md) (miễn phí)
2. `Open Folder as Vault` → chọn thư mục `9lensdata/`
3. Ảnh và link hoạt động inline tự động

---

## Tự thực hành với dataset thật

Mỗi chương đi kèm **dataset CSV thật** để bạn tự phân tích:

| Chapter | Dataset | Số dòng | Bài tập gợi ý |
|---|---|---|---|
| Ch.1 | `techmart-orders-mar2024.csv` | 12,847 đơn | Tìm missing values, vẽ histogram doanh thu |
| Ch.2 | `techmart-orders-full2024.csv` | 134,504 đơn | Vẽ timeline, tìm outliers |
| Ch.3 | `techmart-customers.csv` | 28,000 KH | Tự tính RFM, segment khách hàng |
| Ch.4 | `techmart-marketing-campaigns.csv` | 488 campaigns | Tính correlation matrix, tìm confounding variable |
| Ch.5 | `techmart-finance-monthly.csv` + `techmart-operations-daily.csv` | Full year | Merge 3 nguồn, tạo 1-page summary |

Tất cả dataset đã có sẵn trong `chapters/*/data/`. Clone repo về là có thể chạy luôn.

```bash
git clone https://github.com/your-username/9lensdata.git
cd 9lensdata
# Mở bằng bất kỳ công cụ nào: Excel, Google Sheets, Python, R...
```

---

## Liên Hệ Tác Giả

Cuốn sách này **miễn phí**. Bạn được đọc, chia sẻ, tải xuống, và dùng dataset để thực hành mà không cần xin phép — forever.

Có gì muốn góp ý, hỏi thêm, hoặc chia sẻ câu chuyện của bạn với cuốn sách — liên hệ tác giả:

📧 **nghiahsgs@gmail.com**

*Hoặc chỉ cần share cuốn sách này cho một người bạn cũng đang loay hoay với data.*

---

## Cho developers — Tự sinh lại data & charts

Nếu bạn muốn sinh lại data/charts từ đầu hoặc modify:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Sinh lại 6 file CSV (seed=42, deterministic)
.venv/bin/python3 scripts/generate-data.py

# Sinh lại 11 file PNG charts
.venv/bin/python3 scripts/generate-charts.py
```

**Cấu trúc repo:**

```
9lensdata/
├── chapters/              # Nội dung sách — mỗi chapter tự chứa data + images
│   ├── 00-loi-mo-dau/
│   ├── 01-ngay-dau-tien/
│   ├── 02-thang-3-giam/
│   ├── 03-khach-hang-quan-trong/
│   ├── 04-correlation-volatility/
│   ├── 05-ke-chuyen-dung-nguoi/
│   └── 06-master-framework/
├── scripts/               # Code sinh data + charts (reproducible, seed=42)
├── requirements.txt
└── README.md
```

---

## License

**Creative Commons BY-NC-SA 4.0** — Bạn được đọc, chia sẻ, remix cho mục đích phi thương mại, miễn là ghi nguồn và giữ cùng license.

---

*Cảm ơn bạn đã đọc đến dòng cuối.* 🙏
