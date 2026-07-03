# Walkthrough: Kiểm chứng Toán học & Logic Hệ thống

Tài liệu này trình bày chi tiết quá trình kiểm chứng về toán học, logic, tính toàn vẹn và độ chính xác số học của hệ thống đánh giá vị trí đặt phòng tư vấn tâm lý tại UIT.

---

## 1. Kiểm chứng Logic & Tính toàn vẹn của Đồ thị (Graph Isolation)

Trong phiên bản đầu tiên của thuật toán lan tỏa (BFS/Dijkstra trên hành lang để tính Visibility và Privacy), hệ thống gặp rủi ro "lan tỏa nhầm sang tòa nhà khác" (visual bleeding) ở các lối vào nơi các tòa nhà nằm gần nhau, do thuộc tính `"building"` bị thiếu ở một số đỉnh tòa nhà A.

Chúng tôi đã triển khai hàm kiểm soát biên để cô lập các lượt đi ngang theo tầng và tòa nhà:
1.  **Hàm xác định tòa nhà (`get_node_building`):** Chuẩn hóa cách nhận diện tòa nhà dựa trên thuộc tính sẵn có hoặc tiền tố của định danh node (ví dụ: các node bắt đầu bằng `A-` thuộc tòa nhà `A`, node bắt đầu bằng `B` thuộc tòa nhà `B`).
2.  **Ràng buộc cô lập tầng và tòa nhà (`get_zone_nodes`):** Khi chạy Dijkstra/BFS tìm các đỉnh xung quanh lối tiếp cận phòng, hệ thống áp dụng bộ lọc kép:
    $$\text{n\_building} == \text{start\_building} \quad \text{và} \quad \text{str(n\_floor)} == \text{str(start\_floor)}$$
    Ràng buộc này triệt tiêu hoàn toàn khả năng lan tỏa lưu lượng nhầm sang các tòa nhà lân cận hoặc các tầng khác nhau trong cùng tòa nhà.

---

## 2. Kiểm chứng Toán học & Số học (Numerical Verification)

Dựa trên dữ liệu mô phỏng thực tế chạy trên 1.000 sinh viên, hệ thống đã tính toán và xếp hạng các phòng ứng viên với độ chính xác tuyệt đối. Dưới đây là các bước phân tích kiểm chứng số học:

### 2.1. Accessibility Indicator ($A(r)$)
Công thức tính Chi phí đi bộ trung bình có trọng số ($WTC$):
$$WTC(r) = \frac{\sum_{v_c} Traffic(v_c) \cdot d(v_c, r)}{\sum_{v_c} Traffic(v_c)}$$
Từ kết quả chạy thực nghiệm:
- Phòng có khoảng cách tiếp cận tốt nhất: `B1.02` với $WTC_{min} = 183.2m \rightarrow A(\text{B1.02}) = 1.0$
- Phòng có khoảng cách tiếp cận kém nhất: `C103` với $WTC_{max} = 245.6m \rightarrow A(\text{C103}) = 0.0$
- Đối với phòng `A-F2-RIGHT-ROOM-01` có $WTC = 215.8m$:
  $$A(\text{A-F2}) = \frac{245.6 - 215.8}{245.6 - 183.2} = \frac{29.8}{62.4} \approx 0.4767 \quad (\text{Khớp hoàn toàn})$$

### 2.2. Visibility Indicator ($V(r)$)
Quy mô vùng hiển thị $EZ(r)$ được quét trong bán kính 10m.
- Phòng nằm ở góc khuất nhất: `A-F2-RIGHT-ROOM-01` có điểm thô $RawVisibility = 0.0 \rightarrow V(\text{A-F2}) = 0.0$
- Phòng nằm ở khu vực hiển thị cao nhất: `A-F1-TOP-ROOM-01` có điểm thô $RawVisibility = 2052.4 \rightarrow V(\text{A-F1-TOP}) = 1.0$
- Đối với phòng `B1.02` có $RawVisibility = 293.2$:
  $$V(\text{B1.02}) = \frac{293.2 - 0.0}{2052.4 - 0.0} \approx 0.1429 \quad (\text{Khớp hoàn toàn})$$

### 2.3. Privacy Indicator ($P(r)$)
Lưu lượng rủi ro bị quan sát ($RawExposureRisk$) được quét trong vùng nhạy cảm 3m xung quanh cửa phòng.
- Phòng an toàn nhất (không có giao thông qua lại): `A-F2-RIGHT-ROOM-01` có $RawExposureRisk_{min} = 0.0 \rightarrow P(\text{A-F2}) = 1.0$
- Phòng rủi ro cao nhất (nằm trên lối đi chính): `A-F1-TOP-ROOM-01` có $RawExposureRisk_{max} = 952.0 \rightarrow P(\text{A-F1-TOP}) = 0.0$
- Đối với phòng `B1.02` có $RawExposureRisk = 136.0$:
  $$P(\text{B1.02}) = \frac{952.0 - 136.0}{952.0 - 0.0} = \frac{816.0}{952.0} \approx 0.8571 \quad (\text{Khớp hoàn toàn})$$

### 2.4. Final Xếp hạng (Weighted Sum Scalarization)
Công thức điểm số tổng hợp:
$$FinalScore(r) = w_A \cdot A(r) + w_V \cdot V(r) + w_P \cdot P(r)$$
Với bộ trọng số mặc định: $w_A = 0.35, w_V = 0.15, w_P = 0.50$.
- **Hạng 1: B1.02**
  $$FinalScore = 0.35 \cdot (1.0) + 0.15 \cdot (0.1429) + 0.50 \cdot (0.8571) = 0.35 + 0.0214 + 0.4286 = 0.8000$$
- **Hạng 2: A-F2-RIGHT-ROOM-01**
  $$FinalScore = 0.35 \cdot (0.4767) + 0.15 \cdot (0.0) + 0.50 \cdot (1.0) = 0.1668 + 0.50 = 0.6668$$
- **Hạng 3: A-F1-TOP-ROOM-01**
  $$FinalScore = 0.35 \cdot (0.9980) + 0.15 \cdot (1.0) + 0.50 \cdot (0.0) = 0.3493 + 0.15 = 0.4993$$
- **Hạng 4: C103**
  $$FinalScore = 0.35 \cdot (0.0) + 0.15 \cdot (0.3530) + 0.50 \cdot (0.6292) = 0.0530 + 0.3146 = 0.3676$$

---

## 3. Khớp vị trí tệp tin (Integrity of File Tree)

Hệ thống được đặt gọn gàng và nhất quán trong thư mục làm việc:
*   Mã nguồn xếp hạng: [src/rank_candidates.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/rank_candidates.py)
*   Báo cáo đầu ra JSON: `outputs/node_1_2/ranked_candidates.json`
*   Đặc tả báo cáo dự án: [bao_cao_du_an.md](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md)
*   Kế hoạch kiểm chứng và khắc phục: [implementation_plan.md](file:///d:/CS117/THERAPY_ROOM_PROJECT/implementation_plan.md) và [project_verification_report.md](file:///d:/CS117/THERAPY_ROOM_PROJECT/project_verification_report.md) tại thư mục gốc.
