# Lời Mở Đầu — Đọc Trước Khi Bắt Đầu

> *Cuốn sách này không dạy Python. Không dạy SQL. Không dạy Excel.*
> *Cuốn sách này dạy cách nhìn.*

---

Mỗi ngày thế giới tạo ra hàng tỷ gigabyte dữ liệu. Nhưng phần lớn chúng nằm im trong spreadsheet, database, dashboard màu mè — và không ai thực sự hiểu chúng đang nói gì.

Vấn đề không phải là thiếu data. Vấn đề là thiếu người biết đặt câu hỏi đúng.

Tôi viết cuốn sách này vì tôi từng là Andie. Ngày đầu đi làm, tôi cũng mở file Excel rồi bấm SUM mà chưa hiểu mình đang tính cái gì. Tôi cũng từng present con số sai trước cả phòng, cũng từng bị sếp hỏi "em đang so sánh kiểu gì?" mà không trả lời được. Những bài học trong cuốn sách này — tất cả đều đến từ những lần sai thật. Tôi chỉ thay đổi tên, công ty, và con số để bảo vệ những người liên quan.

Cuốn sách kể về **Andie** — một người hoàn toàn bình thường, không có background toán hay kỹ thuật — và hành trình cậu học cách "nghe" data nói. Qua từng tình huống công việc thực tế, bạn sẽ học được **9 Lens** — 9 góc nhìn bất biến, apply được cho mọi ngành, mọi loại dữ liệu.

---

## 9 Lens Bất Biến

Mỗi lens không được dạy như lý thuyết riêng lẻ. Chúng xuất hiện **đúng lúc Andie cần đến** — trong câu chuyện thực tế, với dataset thực tế, với câu hỏi thực tế.

```
🔭 Lens #1  COMPLETENESS   — Data có ở đó không? Thiếu ở đâu, theo pattern gì?
🔭 Lens #2  DISTRIBUTION   — Data trông như thế nào? Shape quyết định metric bạn dùng.
🔭 Lens #3  OUTLIERS       — Có gì bất thường không? Tại sao nó bất thường?
🔭 Lens #4  TIMELINE       — Xu hướng đi về đâu? Trend, seasonal, hay đột biến?
🔭 Lens #5  CONCENTRATION  — 80% kết quả đến từ 20% nào? Tìm ra nó trước tiên.
🔭 Lens #6  CORRELATION    — Thứ gì liên quan thứ gì? Signal nào predict outcome?
🔭 Lens #7  COMPARISON     — Tốt hay xấu so với gì? Context mới tạo ra meaning.
🔭 Lens #8  SEGMENTATION   — Average đang che giấu điều gì? Segment trước, conclude sau.
🔭 Lens #9  VOLATILITY     — Ổn định hay lung tung? CV cao = risk cao = cần buffer cao.
```

---

## Về nguồn gốc 9 Lens

9 Lens không phải lý thuyết mới. Đây là cách tác giả tổng hợp 9 kỹ thuật phân tích dữ liệu kinh điển — từ Exploratory Data Analysis của John Tukey (1977), nguyên lý Pareto của Vilfredo Pareto (1896), hệ số tương quan của Karl Pearson, phân tích chuỗi thời gian của Box-Jenkins, đến RFM segmentation từ ngành direct marketing những năm 1930 — thành **1 quy trình tư duy** có thể nhớ và apply ngay.

Bạn sẽ tìm thấy từng lens trong bất kỳ sách thống kê nào. Điều khác biệt là **thứ tự và cách kết hợp chúng**: Hiểu Data (#1-3) → Nhìn Xa (#4-5) → Hiểu Sâu (#6-8) → Đo Risk (#9). Thứ tự này phản ánh cách một analyst thực sự làm việc — không phải cách sách giáo khoa sắp xếp.

| Lens | Nền tảng học thuật |
|---|---|
| Completeness | Data Quality Dimensions — ISO 25012, DAMA-DMBOK |
| Distribution | Descriptive Statistics — histogram, skewness, kurtosis |
| Outliers | Outlier Detection — Tukey's IQR (1977), Z-score |
| Timeline | Time Series Decomposition — trend, seasonal, residual |
| Concentration | Pareto Principle — Vilfredo Pareto (1896), Lorenz Curve (1905) |
| Correlation | Correlation Analysis — Pearson (1896), Spearman |
| Comparison | Benchmarking & Hypothesis Testing — Fisher, Neyman-Pearson |
| Segmentation | Market Segmentation, RFM Analysis, Simpson's Paradox |
| Volatility | Coefficient of Variation — Karl Pearson, risk management |

---

## Cách đọc sách này

- Mỗi chapter = 1 tình huống thực tế. Đừng đọc lướt.
- Khi thấy hộp `⏸ DỪNG LẠI` — hãy thực sự dừng và suy nghĩ trước.
- Khi thấy `🔭 Lens #` — nhận ra bạn đang học gì ở thời điểm đó.
- Dataset trong sách có thể tự tạo lại bằng Excel để thực hành.

---

*Đọc xong, bạn sẽ không nhớ "mình đã học lens #3." Bạn sẽ tự nhiên hỏi "có gì bất thường không?" mỗi khi nhìn vào data mới. Đó mới là thứ bạn đang học.*

---

## Về Tác Giả

Tôi không phải giáo sư. Không phải data scientist với PhD. Tôi là một người đi làm, gặp data mỗi ngày, và học cách nhìn nó qua những lần sai.

Nếu cuốn sách này giúp bạn tránh được dù chỉ một lần báo sai số trước sếp — thì nó đã hoàn thành nhiệm vụ.

---

## Liên Hệ Tác Giả

Cuốn sách này **miễn phí**. Bạn được đọc, chia sẻ, và sử dụng dataset để thực hành mà không cần xin phép.

Có gì muốn góp ý, hỏi thêm, hoặc chia sẻ câu chuyện của bạn với cuốn sách — liên hệ tác giả:

📧 **nghiahsgs@gmail.com**
