# Implementation Plan: Sửa chữa và Hoàn thiện `bao_cao_du_an.md`

## 1. Tổng quan Phân tích

Báo cáo [bao_cao_du_an.md](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md) có nền tảng khoa học và toán học **tốt** ở các phần đã viết (Sections 1–6, 9–12), nhưng mắc **3 lỗi nghiêm trọng cấp cấu trúc** và nhiều vấn đề logic/khoa học cần khắc phục trước khi nộp.

---

## 2. Đánh giá Cấu trúc vs Yêu cầu Đề bài

### Cấu trúc đề bài yêu cầu vs Cấu trúc hiện tại

| # | Cấu trúc yêu cầu | Tồn tại trong báo cáo? | Trạng thái |
|---|---|---|---|
| 1 | **Problem Definition/Clarification** | ✅ Section 1 (L28–L60) | Tốt, chi tiết |
| 2 | **Vận dụng CAT trong giải quyết vấn đề** | ❌ **HOÀN TOÀN THIẾU** | 🔴 CRITICAL |
| 3 | **Decomposition Hierarchy/Breakdown Tree** | ❌ **HOÀN TOÀN THIẾU** | 🔴 CRITICAL |
| 4 | **Solution** (algorithm + giải pháp cho leaf nodes) | ⚠️ Section 9 tồn tại nhưng header bị lỗi | 🟡 CORRUPT |
| 5 | **Evaluation** | ✅ Section 5 + 11 | Tốt |
| 6 | **Ethic & Social Impacts** | ✅ Section 12 (L625–L651) | Tốt |
| 7 | **Others (demo etc.)** | ✅ Section 13 (L655–L662) | Cần cập nhật link |

---

## 3. Các Lỗi Nghiêm Trọng (CRITICAL)

### 🔴 CRITICAL-1: Section 7 — "Vận dụng CAT" hoàn toàn thiếu

> [!CAUTION]
> Đây là phần **cốt lõi nhất** của đề bài CS117 — yêu cầu trình bày **tuần tự từng bước** vận dụng các kỹ thuật Computational/AI Thinking (Abstraction, Pattern Recognition, Decomposition) để đi từ bài toán gốc đến lời giải cuối cùng. **Báo cáo hiện không chứa nội dung này.**

TOC liệt kê Section 7 tại [L18](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L18), nhưng giữa Section 6 (kết thúc ở L261) và Section 9 (bắt đầu cũng ở L261 do lỗi merge), **không có bất kỳ dòng nào** chứa từ khóa `Abstraction`, `Pattern Recognition`, `Decomposition`, `Step`, hay `CAT`.

**Yêu cầu cần bổ sung:** Một chuỗi các bước tuần tự dạng:

```
Step 1: Abstraction — Bài toán "Tìm vị trí tối ưu cho phòng tư vấn tâm lý" 
        → Trừu tượng hóa thành "Multi-objective facility location ranking on weighted graph"
Step 2: Decomposition — Phân rã thành 3 sub-problem: Accessibility, Visibility, Privacy  
Step 3: Decomposition — Sub-problem Accessibility phân rã thành:
        3a. Trích xuất O-D pairs từ TKB
        3b. Tìm đường đi trên đồ thị
        3c. Tính weighted travel cost
Step 4: Pattern Recognition - Matching — Sub-problem "Tìm đường đi trên đồ thị có trọng số" 
        → Khớp với bài toán Shortest Path → Sử dụng Dijkstra
...
```

### 🔴 CRITICAL-2: Section 8 — "Cây Phân rã Bài toán" hoàn toàn thiếu

TOC liệt kê Section 8 tại [L19](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L19), nhưng **không tồn tại trong file**. Phần này cần một Decomposition Tree trực quan (dạng mermaid diagram hoặc text tree) thể hiện:

```
Root: Đánh giá & Xếp hạng vị trí phòng tư vấn
├── P1: Trích xuất nhu cầu di chuyển
│   ├── P1.1: Sắp xếp events
│   └── P1.3: Trích xuất O-D pairs
├── P2: Ước lượng tuyến đường & lưu lượng
│   ├── P2.1: Dijkstra shortest paths
│   ├── P2.2: Node traffic
│   ├── P2.3: Edge traffic
│   └── P2.4: Access node pass count
├── P3: Đánh giá Accessibility
│   ├── P3.1: Distance matrix
│   ├── P3.2: Weighted travel cost
│   └── P3.3: Chuẩn hóa [0,1]
├── P4: Đánh giá Visibility
│   ├── P4.1: Exposure zone
│   ├── P4.2: Pass-by count
│   └── P4.3: Chuẩn hóa [0,1]
├── P5: Đánh giá Privacy
│   ├── P5.1: Sensitive zone
│   ├── P5.2: Exposure risk
│   └── P5.3: Chuẩn hóa [0,1]
└── P6: Xếp hạng & Báo cáo
    ├── P6.1: Score validation
    ├── P6.2: Weighted scalarization
    └── P6.3: Trade-off report
```

### 🔴 CRITICAL-3: Đoạn văn bị cắt/merge — Section 6.6 & Section 9 header bị hỏng

Tại [L261](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L261), nội dung Section 6.6 bị **cắt giữa câu** và merge trực tiếp vào header Section 9:

```
...thuật toán tính điểm vô hướng hóa đa mục tiêu (Mul## 9. Chi tiết Kiến trúc Giải pháp...
```

Hậu quả:
- Section 6.6 mất kết luận về giải pháp Pareto
- Section 9 không có header `##` riêng → markdown renderer không tạo heading đúng
- Anchor link trong TOC `#9-chi-tiết-...` sẽ bị hỏng

Tương tự, tại [L559](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L559), cuối Rule 3 có ký tự rác và text thừa:

```
...nhận diện tự nhiên."*�a Ứng viên (Evaluate Accessibility)
```

### 🔴 CRITICAL-4: Section 13 — "Kết luận và Khuyến nghị Phát triển" hoàn toàn thiếu

TOC liệt kê tại [L24](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L24): `13. Kết luận và Khuyến nghị Phát triển`, nhưng Section 13 thực tế chỉ chứa "Khác (Others - Demo & Links)" — **không có phần Kết luận**.

---

## 4. Các Vấn đề Logic & Khoa học

### 🟡 ISSUE-L1: Thiếu P1.2 trong Module P1 (Section 9)

[CS117_Detailed_Problem_Breakdown.md](file:///d:/CS117/THERAPY_ROOM_PROJECT/docs/CS117_Detailed_Problem_Breakdown.md) định nghĩa P1 gồm P1.1, **P1.2** (Loại bỏ tiết bù), P1.3. Nhưng trong báo cáo Section 9.1, sub-module nhảy thẳng từ P1.1 → P1.3. P1.2 bị thiếu hoàn toàn.

### 🟡 ISSUE-L2: Phân loại Metrics lẫn lộn giữa "model-internal" và "real-world"

- Section 5 (Metrics) liệt kê CUR, UPR, PSR, SIS, Runtime — đây là các **real-world post-deployment metrics**.
- Section 6 (NFRs) sử dụng lại CUR, UPR, PSR làm **verification formulas** (VD: `CUR_after >= 1.2 * CUR_before`).
- Nhưng các chỉ số **model-internal** thực sự (Accessibility/Visibility/Privacy indicators ∈ [0,1]) mà hệ thống thực sự tính toán lại được trình bày muộn hơn trong Section 9 (P3–P5).

**Vấn đề logic:** Báo cáo trình bày metrics thực tế (cần khảo sát sau triển khai) TRƯỚC KHI trình bày mô hình tính toán. Người đọc sẽ thắc mắc "hệ thống tính CUR bằng cách nào?" trong khi CUR hoàn toàn không phải output trực tiếp của mô hình.

**Khuyến nghị:** Thêm đoạn giải thích rõ ràng ở đầu Section 5 rằng đây là **post-deployment evaluation metrics**, tách biệt với **model-internal scoring indicators** (A, V, P).

### 🟡 ISSUE-L3: Trọng số mặc định thiếu cơ sở khoa học

Tại [L541–L544](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L541-L544), bộ trọng số `w_P=0.50, w_A=0.35, w_V=0.15` được gán cứng mà không có:
- Trích dẫn nghiên cứu/literature review nào hỗ trợ tỷ lệ này
- Phương pháp AHP (Analytic Hierarchy Process) hoặc khảo sát stakeholder
- Phân tích độ nhạy (sensitivity analysis) nếu trọng số thay đổi

**Khuyến nghị:** Thêm giải thích nguồn gốc (VD: "Dựa trên các nghiên cứu về tâm lý sinh viên, tính riêng tư được ưu tiên hàng đầu...") hoặc đề cập đến sensitivity analysis.

### 🟡 ISSUE-L4: Hệ số suy giảm visibility (λ) thiếu justification

Tại [L442](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L442), hệ số `λ(v,r) = 1/(1 + 0.1·d(v,a_r))` xuất hiện mà không giải thích tại sao chọn hàm nghịch đảo tuyến tính với hệ số `0.1`, thay vì hàm Gaussian hoặc exponential decay thường dùng trong mô hình visibility.

### 🟡 ISSUE-L5: Giả định elevator cost cố định 3m thiếu thực tế

Tại [L128](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L128), chi phí thang máy = **3m cố định** bất kể số tầng. Điều này có nghĩa đi thang máy từ tầng 1→2 tốn 3m, nhưng đi tầng 1→5 cũng tốn 3m — phi thực tế vì thời gian chạy thang máy tỷ lệ với số tầng. Nên dùng `3m + 1m/tầng` hoặc tương tự.

### 🟡 ISSUE-L6: Min-Max normalization không robust khi k=1

Khi chỉ có 1 phòng ứng viên (k=1), `WTC_max = WTC_min`, các công thức chuẩn hóa ([L402](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L402), [L452](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L452), [L498](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L498)) đều trả về 1.0 — mất ý nghĩa so sánh. Báo cáo chưa thảo luận edge case này.

### 🟡 ISSUE-L7: Runtime requirement mâu thuẫn nội bộ

- Tại [L249](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L249): Runtime ≤ **120 giây (2 phút)**
- [CS117_Detailed_Problem_Breakdown.md](file:///d:/CS117/THERAPY_ROOM_PROJECT/docs/CS117_Detailed_Problem_Breakdown.md#L172) ghi: Runtime ≤ **10 giây**

Hai tài liệu trong cùng dự án mâu thuẫn nhau gấp 12 lần.

### 🟢 ISSUE-L8: Demo links là placeholder

Tại [L659–L662](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md#L659-L662), các URL GitHub và YouTube đều là placeholder giả (`https://github.com/uit-cs117-counseling-ranking`, `https://youtube.com/uit-counseling-room-location-evaluation`). Cần thay bằng link thật.

---

## 5. Đánh giá Tổng thể về Logic & Khoa học

### ✅ Các điểm mạnh

| Khía cạnh | Đánh giá |
|---|---|
| **Problem Definition** | Xuất sắc — phát biểu bài toán rõ ràng, In-scope/Out-of-scope rành mạch |
| **Mô hình hóa toán học** | Tốt — công thức WTC, chuẩn hóa Min-Max, FinalScore nhất quán |
| **Input specification** | Chi tiết — D1, D2, D3 được mô tả kỹ lưỡng với ký hiệu toán rõ ràng |
| **Assumptions** | Hợp lý — bounded rationality 15%, uniform entry distribution |
| **Ethics** | Rất tốt — 6 nguyên tắc đạo đức toàn diện, phù hợp bối cảnh sức khỏe tinh thần |
| **Data flow** | Tốt — 22 data elements được liệt kê đầy đủ với I/O tracing |
| **Evaluation data collection** | Tốt — chiến lược before-after study, confounding variable control |

### ❌ Các điểm cần sửa

| Mức độ | Số lượng | Tóm tắt |
|---|---|---|
| 🔴 CRITICAL | 4 | Section 7 (CAT), Section 8 (Tree), Section 6.6/9 corrupt, Section 13 thiếu Kết luận |
| 🟡 MAJOR | 7 | P1.2 thiếu, metrics lẫn lộn, trọng số thiếu cơ sở, λ thiếu justification, elevator cost, Min-Max k=1, Runtime mâu thuẫn |
| 🟢 MINOR | 1 | Demo links placeholder |

---

## 6. Kế hoạch Sửa chữa (Implementation Plan)

### Phase 1: Sửa các lỗi cấu trúc CRITICAL

> [!IMPORTANT]
> Tất cả các thay đổi dưới đây thực hiện trên file [bao_cao_du_an.md](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md)

#### [MODIFY] [bao_cao_du_an.md](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md)

**Fix 1 — Sửa Section 6.6 bị cắt (L261):**
- Hoàn chỉnh câu về Pareto-optimal solutions và scalarization
- Tách Section 9 header ra dòng riêng với proper `## 9.` markdown heading

**Fix 2 — Thêm Section 7: "Vận dụng CAT trong Giải quyết Vấn đề" (chèn giữa Section 6 và Section 9):**
- Viết ~10–15 bước CAT tuần tự, bao gồm:
  - **Abstraction:** Trừu tượng hóa bài toán thực tế → Multi-objective facility location ranking
  - **Decomposition (Level 1):** Phân rã thành P1→P6
  - **Decomposition (Level 2):** Phân rã từng P thành sub-problems
  - **Pattern Recognition — Matching:** Nhận dạng bài toán con khớp với các bài toán kinh điển (Shortest Path → Dijkstra, Multi-objective optimization → Weighted Scalarization, Normalization → Min-Max)
  - **Abstraction/Generalization:** Trừu tượng hóa hành vi di chuyển sinh viên → luồng trên đồ thị có trọng số

**Fix 3 — Thêm Section 8: "Cây Phân rã Bài toán" (chèn sau Section 7):**
- Mermaid diagram hoặc text-based tree thể hiện cấu trúc phân rã P1–P6 và các sub-modules

**Fix 4 — Sửa ký tự rác tại L559:**
- Xóa `�a Ứng viên (Evaluate Accessibility)` cuối dòng

**Fix 5 — Cập nhật Section 13:**
- Đổi heading thành "Kết luận, Khuyến nghị Phát triển & Demo"
- Thêm phần Kết luận tóm tắt kết quả dự án và hướng phát triển

### Phase 2: Sửa các vấn đề logic/khoa học

**Fix 6 — Bổ sung P1.2** trong Section 9.1 (hoặc ghi chú rõ ràng tại sao P1.2 bị loại bỏ)

**Fix 7 — Thêm clarification ở đầu Section 5** phân biệt post-deployment metrics vs model-internal indicators

**Fix 8 — Thêm justification cho trọng số** `w_P=0.50, w_A=0.35, w_V=0.15` (tối thiểu 2–3 câu giải thích)

**Fix 9 — Thêm giải thích cho hệ số λ** decay function

**Fix 10 — Sửa elevator cost** hoặc thêm giải thích tại sao chi phí cố định là hợp lý

**Fix 11 — Thêm thảo luận edge case k=1** trong phần chuẩn hóa

**Fix 12 — Thống nhất Runtime requirement** với tài liệu kỹ thuật (chọn 10s hoặc 120s)

### Phase 3: Minor fixes

**Fix 13 — Cập nhật demo links** placeholder thành URLs thực

**Fix 14 — Cập nhật TOC** cho khớp với cấu trúc file sau khi sửa

---

## 7. Verification Plan

### Manual Verification
- Đọc lại toàn bộ báo cáo sau sửa, kiểm tra:
  - Tất cả 13 sections trong TOC đều tồn tại và có heading đúng
  - Section 7 có đúng format step-by-step CAT
  - Section 8 có Decomposition Tree diagram
  - Không còn ký tự rác hoặc text bị cắt
  - Các anchor links trong TOC hoạt động đúng

## Open Questions

> [!IMPORTANT]
> Các câu hỏi cần được trả lời trước khi bắt đầu sửa:

1. **Runtime target nào là đúng?** Báo cáo ghi 120s, tài liệu kỹ thuật ghi 10s. Chọn giá trị nào?
2. **Demo links:** Bạn có GitHub repo URL và video demo URL thực không? Hay để placeholder?
3. **Elevator cost:** Giữ nguyên 3m cố định (và thêm justification) hay đổi thành cost tỷ lệ với số tầng?
4. **Trọng số w_P, w_A, w_V:** Có cơ sở nào (literature, khảo sát) hay cần viết justification mới?
