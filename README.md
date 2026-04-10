# Andie va Nhung Con So Biet Noi
### Sach phan tich du lieu — 9 Lens Bat Bien

---

## Gioi thieu

Cuon sach ke ve **Andie** — mot Junior Analyst ngay dau di lam — va hanh trinh cau hoc cach "nghe" data noi. Qua tung tinh huong thuc te (sai lam, bi sep hoi van, bao cao sai), ban se hoc duoc **9 Lens** — 9 goc nhin bat bien, apply duoc cho moi nganh, moi loai du lieu.

> *Cuon sach nay khong day Python. Khong day SQL. Khong day Excel.*
> *Cuon sach nay day cach nhin.*

---

## Cau truc thu muc

```
9lensdata/
├── README.md
├── requirements.txt
├── .gitignore
│
├── chapters/                    # Noi dung sach — moi chapter tu chua data + images
│   ├── 00-loi-mo-dau/
│   │   └── README.md
│   ├── 01-ngay-dau-tien/            Lens #1 Completeness + #2 Distribution
│   │   ├── README.md
│   │   ├── images/
│   │   │   ├── chart-01-completeness.png
│   │   │   └── chart-02-distribution.png
│   │   └── data/
│   │       └── techmart-orders-mar2024.csv       12,847 don hang thang 3/2024
│   ├── 02-thang-3-giam/             Lens #3 Outliers + #4 Timeline
│   │   ├── README.md
│   │   ├── images/
│   │   │   └── chart-03-timeline-outliers.png
│   │   └── data/
│   │       └── techmart-orders-full2024.csv      134,504 don hang T3/2023 - T9/2024
│   ├── 03-khach-hang-quan-trong/    Lens #5 Concentration + #8 Segmentation
│   │   ├── README.md
│   │   ├── images/
│   │   │   ├── chart-04-concentration.png
│   │   │   └── chart-07-segmentation.png
│   │   └── data/
│   │       └── techmart-customers.csv            28,000 khach hang + RFM + churn
│   ├── 04-correlation-volatility/   Lens #6 Correlation + #9 Volatility + Marketing
│   │   ├── README.md
│   │   ├── images/
│   │   │   ├── chart-05-correlation.png
│   │   │   ├── chart-08-volatility.png
│   │   │   └── chart-09-marketing-correlation.png
│   │   └── data/
│   │       └── techmart-marketing-campaigns.csv  488 campaigns, 6 kenh quang cao
│   ├── 05-ke-chuyen-dung-nguoi/     Lens #7 Comparison + Multi-source storytelling
│   │   ├── README.md
│   │   ├── images/
│   │   │   ├── chart-06-comparison.png
│   │   │   ├── chart-10-finance-pl.png
│   │   │   └── chart-11-operations-dashboard.png
│   │   └── data/
│   │       ├── techmart-finance-monthly.csv      P&L hang thang 2023-2024
│   │       └── techmart-operations-daily.csv     Giao hang, NPS, return rate hang ngay
│   └── 06-master-framework/
│       └── README.md                Tong hop 9 Lens + Mini Cases da nganh
│
└── scripts/                     # Code sinh data + charts (dung chung)
    ├── generate-data.py             Entry point — sinh tat ca CSV vao chapter/data/
    ├── generate-charts.py           Entry point — sinh tat ca charts vao chapter/images/
    ├── data_generators.py           Logic sinh data e-commerce + customers
    ├── data_generators_extra.py     Logic sinh data marketing + finance + ops
    ├── chart_helpers.py             Shared utilities (style, save, format, paths)
    ├── charts_lens1_2.py            Charts 01-02 → ch01
    ├── charts_lens3_4.py            Charts 03-04 → ch02, ch03
    ├── charts_lens5_6.py            Charts 05-06 → ch04, ch05
    ├── charts_lens7_8.py            Charts 07-08 → ch03, ch04
    ├── charts_marketing.py          Chart 09 → ch04
    └── charts_finance_ops.py        Charts 10-11 → ch05
```

---

## 9 Lens Bat Bien

| # | Lens | Cau hoi cot loi | Chapter | Data |
|---|------|----------------|---------|------|
| 1 | COMPLETENESS | Data co o do khong? | Ch.01 | Orders |
| 2 | DISTRIBUTION | Data trong nhu the nao? | Ch.01 | Orders |
| 3 | OUTLIERS | Co gi bat thuong khong? | Ch.02 | Orders |
| 4 | TIMELINE | Xu huong di ve dau? | Ch.02 | Orders (full year) |
| 5 | CONCENTRATION | 80% den tu 20% nao? | Ch.03 | Customers |
| 6 | CORRELATION | Thu gi lien quan thu gi? | Ch.04 | Customers + Marketing |
| 7 | COMPARISON | Tot hay xau so voi gi? | Ch.05 | Finance + Operations |
| 8 | SEGMENTATION | Average che giau gi? | Ch.03 | Customers |
| 9 | VOLATILITY | On dinh hay lung tung? | Ch.04 | Orders + Marketing |

---

## Bat dau nhanh

### 1. Cai dat

```bash
git clone https://github.com/your-username/9lensdata.git
cd 9lensdata
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 2. Sinh data

```bash
.venv/bin/python3 scripts/generate-data.py
```

Output: 6 file CSV trong `chapters/*/data/`. Data duoc sinh voi `seed=42` — chay lai luon ra ket qua giong nhau.

### 3. Sinh charts

```bash
.venv/bin/python3 scripts/generate-charts.py
```

Output: 11 file PNG trong `chapters/*/images/`.

### 4. Doc sach

**Obsidian** (khuyen nghi):
1. Open Folder as Vault → chon thu muc `9lensdata/`
2. Anh hien thi inline tu dong, mo `chapters/00-loi-mo-dau/README.md` de bat dau

**VS Code**:
1. Mo thu muc `9lensdata/`
2. Cai extension **Markdown Preview Enhanced**
3. `Ctrl+Shift+V` de preview

---

## Tu thuc hanh

Sau khi doc moi chapter, ban co the tu phan tich data:

```bash
# Mo Python interactive
.venv/bin/python3

>>> import pandas as pd
>>> orders = pd.read_csv('chapters/01-ngay-dau-tien/data/techmart-orders-mar2024.csv')
>>> orders.head()
>>> orders.describe()
```

**Bai tap goi y:**

| Chapter | Bai tap | File CSV |
|---|---|---|
| Ch.1 | Tim missing values, ve histogram doanh thu | `chapters/01-ngay-dau-tien/data/techmart-orders-mar2024.csv` |
| Ch.2 | Ve timeline doanh thu theo ngay, tim outliers | `chapters/02-thang-3-giam/data/techmart-orders-full2024.csv` |
| Ch.3 | Tu tinh RFM score, segment khach hang | `chapters/03-khach-hang-quan-trong/data/techmart-customers.csv` |
| Ch.4 | Tinh correlation matrix, tim confounding variable | `chapters/04-correlation-volatility/data/techmart-marketing-campaigns.csv` |
| Ch.5 | Merge 3 nguon data, tao 1-page summary | Tat ca 6 files trong chapters/*/data/ |

---

## Chinh sua & dong gop

- **Sua text**: mo file `.md` trong `chapters/` bang bat ky editor nao
- **Thay chart**: chay lai `generate-charts.py` sau khi sua script
- **Them data**: sua `data_generators.py` hoac `data_generators_extra.py`, chay lai `generate-data.py`
- **Them chapter**: tao file moi trong `chapters/`, dat ten theo so thu tu

---

## Ghi chu ky thuat

- Anh dung **relative path**: `./images/chart-01-completeness.png` (trong cung chapter folder)
- Charts co caption: `*Hinh X: ...*`
- Pause boxes: `> ⏸ ...`
- Lens tags: `> 🔭 ...`
- Data sinh bang `numpy.random.seed(42)` — reproducible
- Charts sinh tu CSV that, khong phai anh tinh
