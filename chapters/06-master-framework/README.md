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

## 9 Lens Ngoài E-commerce — Mini Cases

TechMart là nơi Andie học. Nhưng 9 Lens không thuộc về e-commerce.

> **🏥 Mini Case — Lens #1 COMPLETENESS trong Y tế**
> Bệnh viện X phát hiện 30% hồ sơ bệnh nhân thiếu cột huyết áp. Không phải ngẫu nhiên — y tá ca đêm không đo vì thiếu nhân lực. Kết quả: bác sĩ kê đơn cao huyết áp dựa trên data thiếu → under-diagnosis hàng loạt. Cùng pattern "missing không ngẫu nhiên" như rating KH của TechMart — bỏ qua pattern này là bỏ qua sự thật.

> **🏘️ Mini Case — Lens #2 DISTRIBUTION trong Bất động sản**
> Giá nhà ở một quận right-skewed nặng: median 3 tỷ, mean 8 tỷ. Một vài biệt thự kéo mean lên cao. Agent dùng mean để quảng cáo "giá trung bình 8 tỷ" — khách hàng phổ thông đến xem rồi thất vọng. Dùng sai metric, mất cả traffic lẫn trust.

> **🏦 Mini Case — Lens #3 OUTLIERS trong Ngân hàng**
> Hệ thống flagged một giao dịch 500 triệu lúc 3h sáng từ tài khoản thường chỉ giao dịch dưới 5 triệu. Analyst đầu tiên tưởng lỗi hệ thống, định bỏ qua. Analyst thứ hai điều tra — đây là money laundering signal thật. Outlier không phải lỗi. Outlier là câu hỏi.

> **🎓 Mini Case — Lens #4 TIMELINE trong Giáo dục**
> Điểm thi toán toàn quốc giảm 3 năm liên tiếp — headline báo: "Chất lượng giáo dục đi xuống." Nhưng khi tách timeline theo loại trường: trường thành thị giữ nguyên, trường nông thôn giảm đều. Trend tổng hợp che giấu trend thật. Fix đúng vấn đề phải nhìn đúng segment theo thời gian.

> **💻 Mini Case — Lens #5 CONCENTRATION trong Startup SaaS**
> Startup có 120 khách hàng, MRR 2 tỷ. Nghe ổn. Nhưng 3 enterprise clients = 72% MRR. Tháng 7, 1 client lớn nhất báo churn — công ty mất 38% doanh thu trong 1 email. Concentration risk không hiện ra trong dashboard average. Chỉ hiện ra khi bạn hỏi "80% đến từ 20% nào?"

> **👥 Mini Case — Lens #6 CORRELATION trong HR**
> HR phát hiện: nhân viên đi muộn correlate với tỷ lệ resign trong 3 tháng tiếp theo (r = 0.52). Đề xuất ban đầu: "Phạt tiền đi muộn để giảm resign." Nhưng thật ra cả đi muộn lẫn resign đều do burnout — workload quá cao. Phạt đi muộn không fix burnout. Lại là confounding variable.

> **₿ Mini Case — Lens #7 COMPARISON trong Crypto/Finance**
> Investor khoe: "Tháng này Bitcoin của tôi tăng 40%!" Nghe ấn tượng. Nhưng cùng tháng đó ETH tăng 65%, altcoin index tăng 80%. So với benchmark phù hợp — nhà đầu tư này thật ra underperform thị trường. "Tốt" hay "xấu" phụ thuộc vào so với cái gì.

> **🍜 Mini Case — Lens #8 SEGMENTATION trong F&B**
> Nhà hàng có average bill 250K. Menu được thiết kế quanh mức này. Nhưng khi segment theo giờ: buổi trưa bill TB 120K (nhân viên văn phòng ăn nhanh), buổi tối 480K (gia đình ăn cuối tuần). Menu 250K không phù hợp với cả hai nhóm. Average che giấu 2 nhóm khách hàng hoàn toàn khác nhau với nhu cầu hoàn toàn khác nhau.

> **🚚 Mini Case — Lens #9 VOLATILITY trong Logistics**
> Công ty logistics áp 1 SLA chung: "Giao hàng trong 3 ngày." Nhưng CV thời gian giao nội thành = 15% (ổn định), CV liên tỉnh = 65% (cực kỳ volatile). SLA 3 ngày ổn cho nội thành — nhưng liên tỉnh cần buffer thêm 2 ngày để đạt cùng mức confidence. Cùng 1 con số, 2 thực tế hoàn toàn khác nhau.

---

9 Lens không phải framework chỉ cho e-commerce. Bất kỳ ngành nào có data — y tế, tài chính, giáo dục, logistics, HR — đều cần cùng những câu hỏi này. Tool thay đổi, ngành thay đổi, nhưng cách đặt câu hỏi thì không.

---

## Lời Kết

Tháng 12. Cuối năm. Linh — junior mới vào TechMart, 23 tuổi, vừa tốt nghiệp — ngồi ở cái bàn mà Andie từng ngồi năm ngoái. Cô mở file Excel đầu tiên, ngón tay hover trên bàn phím, không biết bắt đầu từ đâu.

Andie đi qua, ngồi xuống cạnh.

> 💬 **Linh** *(hơi lo lắng)*:
> *"Anh Andie, anh chỉ cho em bắt đầu thế nào với? Em không biết nên tính gì trước..."*

Andie cười. Cậu nhớ lại chính mình một năm trước — cũng ngón tay hover, cũng sợ bấm sai.

> 💬 **Andie:**
> *"Linh sẽ học rất nhiều tool: Python, SQL, Power BI, Tableau. Tất cả đều quan trọng. Nhưng tool thay đổi theo năm.*
>
> *9 Lens này — anh dùng mỗi ngày, và anh nghĩ sẽ còn dùng 10 năm nữa. Bởi vì chúng không phải là công cụ. Chúng là câu hỏi.*
>
> *Câu hỏi quan trọng nhất không phải 'Tôi có thể tính gì từ data này?' Mà là: 'Quyết định nào sẽ thay đổi dựa trên những gì tôi tìm ra?'"*

Linh ghi vào notebook. Andie nhìn cô gõ và nhớ lại: chính cậu, một năm trước, cũng đã ghi vào một tờ giấy A4 sau khi báo sai 14.6% trước sếp.

> 💬 **Andie:**
> *"Một điều nữa, Linh. Em sẽ sai. Nhiều lần. Anh đã sai mỗi tháng trong năm đầu tiên — và có những lần sai rất đau. Nhưng mỗi lần sai, em sẽ học được một lens mới. Đừng sợ sai. Sợ là không hiểu tại sao mình sai."*

Linh gật đầu, mở file, bắt đầu quét cột đầu tiên. Không vội bấm SUM. Đầu tiên, cô hỏi: *"Dữ liệu này về ai, cái gì, khi nào, từ đâu, để làm gì?"*

Andie mỉm cười, đứng dậy về bàn. Một lens đã truyền đi.

---

*— Hết —*

---

## Liên Hệ Tác Giả

Cuốn sách này **miễn phí**. Bạn được đọc, chia sẻ, tải xuống, và dùng dataset để thực hành mà không cần xin phép — forever.

Có gì muốn góp ý, hỏi thêm, hoặc chia sẻ câu chuyện của bạn — liên hệ tác giả:

📧 **nghiahsgs@gmail.com**

*Hoặc chỉ đơn giản: share cuốn sách này cho một người bạn cũng đang loay hoay với data.*

**Cảm ơn bạn đã đọc đến trang cuối.**

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
| FMCG | Fast-Moving Consumer Goods — hàng tiêu dùng nhanh (sữa, dầu gội, mì gói). | #2, #9 |
| RFM | Recency-Frequency-Monetary — phân khúc KH theo 3 chiều. | #8 |
| ROAS | Return on Ad Spend — doanh thu / chi phí quảng cáo. | #6 |
| CAC | Customer Acquisition Cost — chi phí để có 1 khách hàng mới. | #6 |
| MoM | Month-over-Month — so với tháng trước. | #4, #7 |
| NPS | Net Promoter Score — đo mức độ KH sẵn sàng giới thiệu. | #7 |