# Chương 6 — 9 Lens: Tổng Hợp
## *Khi nào dùng lens nào — và tư duy của data expert*

---

## Andie viết lại — Sau 1 năm

Cuối năm. Andie lên Senior Analyst. Nhìn lại, cậu nhận ra: mọi bài toán data đều đi qua cùng một quy trình tư duy. Và 9 lens không phải 9 bước riêng lẻ — chúng xuất hiện đồng thời, chồng lên nhau, bổ sung cho nhau.

---

## 9 Lens — Thứ Tự Áp Dụng

```
═══ PHASE 1: HIỂU DATA ═══════════════════════════════════
#1 COMPLETENESS   → Luôn làm đầu tiên.
                    Data có ở đó không? Missing pattern gì?

#2 DISTRIBUTION   → Ngay sau đó.
                    Shape quyết định metric. Right-skewed → Median.

#3 OUTLIERS       → Song song với #2.
                    Phân loại 3 loại trước khi xử lý.

═══ PHASE 2: NHÌN XA ═════════════════════════════════════
#4 TIMELINE       → Nhìn chuỗi thời gian.
                    Trend / Seasonal / Residual?

#5 CONCENTRATION  → 20% nào tạo 80%?
                    Tìm ra trước khi làm gì khác.

═══ PHASE 3: HIỂU SÂU ════════════════════════════════════
#6 CORRELATION    → Thứ gì predict thứ gì?
                    Signal nào mạnh nhất?

#7 COMPARISON     → So với gì?
                    Target → YoY → Benchmark → Control.

#8 SEGMENTATION   → Average che giấu gì?
                    Segment trước, conclude sau.

═══ PHASE 4: ĐO RISK ═════════════════════════════════════
#9 VOLATILITY     → Ổn định hay lung tung?
                    CV > 50% → scenario planning.
```

---

## Khi bạn được hỏi... → Dùng Lens nào?

| Câu Hỏi Bạn Nhận Được | Dùng Lens | Câu Hỏi Cốt Lõi |
|---|---|---|
| "Data này trông như thế nào?" | #1 + #2 + #3 | Complete? Shape? Outlier gì? |
| "Tháng này tốt hay xấu?" | #4 + #7 | Timeline thế nào? So với gì? |
| "Tập trung vào đâu?" | #5 + #8 | 80% đến từ 20% nào? Segment gì? |
| "Tại sao X xảy ra?" | #6 + #3 | Có gì correlate? Anomaly gì? |
| "Tháng tới sẽ như thế nào?" | #4 + #9 | Trend + seasonal? Volatile bao nhiêu? |
| "Risk ở đâu?" | #9 + #5 + #3 | CV cao nhất ở đâu? Concentration risk? |
| "Kể cho CEO nghe?" | #7 + #8 + SCQA | So sánh đúng + Segment đúng + Cấu trúc đúng |

---

## 10 Mental Models — In Ra, Dán Lên Bàn

```
1.  Context is king: Số liệu không có context là vô nghĩa. "So với cái gì?"
2.  All models are wrong, some are useful. (George Box)
3.  Correlation ≠ Causation — mãi mãi ghi nhớ.
4.  Averages lie — luôn hỏi về distribution.
5.  Sample size matters — kết quả từ sample nhỏ có thể là may mắn.
6.  You only see survivors — Survivorship Bias luôn rình rập.
7.  Garbage in, garbage out — data quality là nền tảng.
8.  80% data cleaning, 20% analysis — đừng kỳ vọng ngược lại.
9.  Compare apples to apples — cùng definition, cùng period, cùng scope.
10. The goal is decision, not insight — analysis chỉ có giá trị khi ai đó hành động.
```

---

## Quick Reference: 9 Lens

| # | Lens | Câu Hỏi Kích Hoạt | Công Cụ | Bẫy Hay Gặp |
|---|---|---|---|---|
| 1 | COMPLETENESS | Data có ở đó không? | Missing heatmap, null count | Xóa missing mà không hỏi pattern |
| 2 | DISTRIBUTION | Data trông như thế nào? | Histogram, boxplot | Dùng mean khi data skewed |
| 3 | OUTLIERS | Có gì bất thường không? | Z-score, IQR, scatter | Xóa outlier tự động không điều tra |
| 4 | TIMELINE | Xu hướng đi về đâu? | Line chart, decomposition | So MoM thay vì YoY khi có seasonal |
| 5 | CONCENTRATION | 80% đến từ 20% nào? | Lorenz curve, Pareto chart | Treat all customers equally |
| 6 | CORRELATION | Thứ gì liên quan thứ gì? | Correlation matrix, scatter | Kết luận nhân quả từ correlation |
| 7 | COMPARISON | Tốt hay xấu so với gì? | Waterfall, YoY bar | So sánh số tuyệt đối không baseline |
| 8 | SEGMENTATION | Average che giấu gì? | Heatmap 2D, scatter | Simpson's Paradox, aggregate vội |
| 9 | VOLATILITY | Ổn định hay lung tung? | CV, rolling std, risk matrix | 1 model cho cả FMCG lẫn Bundle |

---

## Lời Kết

> 💬 **Andie nói với Linh — junior mới join:**
>
> *"Linh sẽ học rất nhiều tool: Python, SQL, Power BI, Tableau. Tất cả đều quan trọng. Nhưng tool thay đổi theo năm.*
>
> *9 Lens này — tôi dùng mỗi ngày, từ 10 năm nay và sẽ còn dùng 10 năm nữa.*
>
> *Câu hỏi quan trọng nhất không phải 'Tôi có thể tính gì từ data này?' Mà là: 'Quyết định nào sẽ thay đổi dựa trên những gì tôi tìm ra?'"*

---

*— Hết —*

---

## Từ Điển Thuật Ngữ

| Thuật Ngữ | Giải Thích Đơn Giản | Lens |
|---|---|---|
| Mean (Trung bình) | Tổng / số phần tử. Bị kéo bởi outlier. | #2, #3 |
| Median (Trung vị) | Giá trị ở giữa khi sort. Robust hơn mean. | #2 |
| CV | Std Dev / Mean × 100%. Đo biến động tương đối. | #9 |
| Correlation (r) | −1 đến +1. Mức độ 2 biến thay đổi cùng nhau. | #6 |
| Outlier | Giá trị bất thường, xa phần còn lại. | #3 |
| Seasonality | Pattern lặp lại theo chu kỳ cố định. | #4 |
| Lorenz Curve | Đường cong thể hiện mức độ tập trung. | #5 |
| Simpson's Paradox | Trend tổng hợp ngược chiều với từng subgroup. | #8 |
| YoY | Year-over-Year: so với cùng kỳ năm ngoái. | #4, #7 |
| SCQA | Situation-Complication-Question-Answer. | #7 |
| p-value | Xác suất kết quả xảy ra do may mắn (ngưỡng < 0.05). | #6 |
| Baseline | "Nếu không làm gì thì là bao nhiêu?" | #7 |
| Survivorship Bias | Chỉ thấy data từ "người sống sót". | #1, #2 |