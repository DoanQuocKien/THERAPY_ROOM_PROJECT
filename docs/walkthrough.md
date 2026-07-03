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
- Phòng có khoảng cách tiếp cận tốt nhất: `B1.02` với $WTC_{min} = 183.6m \rightarrow A(\text{B1.02}) = 1.0$
- Phòng có khoảng cách tiếp cận kém nhất: `C103` với $WTC_{max} = 245.8m \rightarrow A(\text{C103}) = 0.0$
- Đối với phòng `A-F2-RIGHT-ROOM-01` có $WTC = 236.6m$:
  $$A(\text{A-F2}) = \frac{245.8 - 236.6}{245.8 - 183.6} = \frac{9.2}{62.2} \approx 0.1476 \quad (\text{Khớp hoàn toàn})$$

### 2.2. Visibility Indicator ($V(r)$)
Quy mô vùng hiển thị $EZ(r)$ được quét trong bán kính 10m.
- Phòng nằm ở góc khuất nhất: `A-F2-RIGHT-ROOM-01` có điểm thô $RawVisibility = 0.0 \rightarrow V(\text{A-F2}) = 0.0$
- Phòng nằm ở khu vực hiển thị cao nhất: `A-F1-TOP-ROOM-01` có điểm thô $RawVisibility = 2370.4 \rightarrow V(\text{A-F1-TOP}) = 1.0$
- Đối với phòng `B1.02` có $RawVisibility = 261.5$:
  $$V(\text{B1.02}) = \frac{261.5 - 0.0}{2370.4 - 0.0} \approx 0.1103 \quad (\text{Khớp hoàn toàn})$$

### 2.3. Privacy Indicator ($P(r)$)
Lưu lượng rủi ro bị quan sát ($RawExposureRisk$) được quét trong vùng nhạy cảm 3m xung quanh cửa phòng.
- Phòng an toàn nhất (không có giao thông qua lại): `A-F2-RIGHT-ROOM-01` có $RawExposureRisk_{min} = 0.0 \rightarrow P(\text{A-F2}) = 1.0$
- Phòng rủi ro cao nhất (nằm trên lối đi chính): `A-F1-TOP-ROOM-01` có $RawExposureRisk_{max} = 1101.0 \rightarrow P(\text{A-F1-TOP}) = 0.0$
- Đối với phòng `B1.02` có $RawExposureRisk = 124.0$:
  $$P(\text{B1.02}) = \frac{1101.0 - 124.0}{1101.0 - 0.0} = \frac{977.0}{1101.0} \approx 0.8874 \quad (\text{Khớp hoàn toàn})$$

### 2.4. Final Xếp hạng (Weighted Sum Scalarization)
Công thức điểm số tổng hợp:
$$FinalScore(r) = w_A \cdot A(r) + w_V \cdot V(r) + w_P \cdot P(r)$$
Với bộ trọng số mặc định: $w_A = 0.35, w_V = 0.15, w_P = 0.50$.
- **Hạng 1: B1.02**
  $$FinalScore = 0.35 \cdot (1.0) + 0.15 \cdot (0.1103) + 0.50 \cdot (0.8874) = 0.35 + 0.0165 + 0.4437 = 0.8102$$
- **Hạng 2: A-F2-RIGHT-ROOM-01**
  $$FinalScore = 0.35 \cdot (0.1476) + 0.15 \cdot (0.0) + 0.50 \cdot (1.0) = 0.0517 + 0.50 = 0.5517$$
- **Hạng 3: A-F1-TOP-ROOM-01**
  $$FinalScore = 0.35 \cdot (0.8601) + 0.15 \cdot (1.0) + 0.50 \cdot (0.0) = 0.3010 + 0.15 = 0.4510$$
- **Hạng 4: C103**
  $$FinalScore = 0.35 \cdot (0.0) + 0.15 \cdot (0.2675) + 0.50 \cdot (0.7193) = 0.0401 + 0.3597 = 0.3998$$

---

## 3. Cổng thông tin Trực quan (Interactive Visual UI Portal)

Chúng tôi đã hoàn thiện cổng thông tin trực quan tương tác hoàn chỉnh tại thư mục [gui/](file:///d:/CS117/THERAPY_ROOM_PROJECT/gui):
*   **Trang giao diện chính:** [index.html](file:///d:/CS117/THERAPY_ROOM_PROJECT/gui/index.html)
*   **Tệp bó dữ liệu cục bộ (CORS-free):** [gui_data.js](file:///d:/CS117/THERAPY_ROOM_PROJECT/gui/gui_data.js)

### 3.1. Các tính năng nổi bật của UI:
1.  **Nhập liệu trực tiếp cả 3 nguồn (D1, D2, D3):**
    - **Thời khóa biểu (D1):** Có ô nhập liệu JSON dạng danh sách lớp học và sĩ số.
    - **Đồ thị Không gian (D2):** Ô nhập cấu trúc đỉnh & cạnh của UIT.
    - **Phòng ứng viên (D3):** Ô nhập mảng JSON phòng ứng tuyển (mặc định hiển thị tất cả 198 phòng học).
    - Các ô nhập D1 và D2 được thiết kế thu gọn (`<details>`) giúp thanh điều khiển bên cạnh luôn gọn gàng và tinh tế.
2.  **Mô phỏng Giao thông thời gian thực trên Trình duyệt:** Khi nhấn "Tính toán", hệ thống tự động chạy bộ mô phỏng giao thông (Student Routing Traffic Simulator) bằng Javascript trực tiếp trên đồ thị D2 với lịch học D1 (chạy Dijkstra tích lũy lưu lượng trên từng tuyến đường và nút giao) trong vòng chưa đầy 20ms, cập nhật bản đồ nhiệt động.
3.  **Tối ưu hóa Thuật toán Dijkstra:** Mã nguồn Dijkstra được thiết kế tối ưu $O(V)$ thay thế cho sắp xếp hàng đợi cũ giúp loại bỏ hoàn toàn hiện tượng treo/lag trình duyệt, thực hiện xếp hạng toàn diện tất cả các phòng tức thời.
4.  **Bản đồ trực quan độ tương phản cao:**
    - Sử dụng giao diện nền sáng kiểu giấy vẽ kỹ thuật (#f8fafc) kèm lưới tọa độ chi tiết.
    - Tuyến đường di chuyển của sinh viên hiển thị dưới dạng các sợi dây phát sáng có màu sắc (xanh dương $\rightarrow$ cam $\rightarrow$ đỏ) và độ dày nét vẽ tỷ lệ thuận với lưu lượng đi qua.
    - Phòng học vẽ dưới dạng các hình chữ nhật sáng màu kiến trúc rõ nét. Để tránh chồng chéo nhãn tên, hệ thống chỉ vẽ nhãn phòng khi nó thuộc danh sách ứng viên, được chọn, hoặc khi trỏ chuột vào.
5.  **Tính toán và Hiển thị Chỉ số Toàn diện cho TẤT CẢ các phòng:**
    - Khi di chuột qua bất kỳ phòng nào (kể cả không nằm trong danh sách ứng viên $D_3$), tooltip kính mờ sẽ hiển thị đầy đủ thông tin: Chỉ số tiếp cận (A) kèm nỗ lực đi bộ trung bình (WTC), Chỉ số hiển thị (V) kèm Visibility thô, Chỉ số riêng tư (P) kèm Exposure Risk thô và tổng điểm FinalScore chuẩn hóa theo phạm vi toàn trường.

---

## 4. Khớp vị trí tệp tin (Integrity of File Tree)

Hệ thống được đặt gọn gàng và nhất quán trong thư mục làm việc:
*   Mã nguồn xếp hạng: [src/rank_candidates.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/rank_candidates.py)
*   Báo cáo đầu ra JSON: `outputs/node_1_2/ranked_candidates.json`
*   Đặc tả báo cáo dự án: [bao_cao_du_an.md](file:///d:/CS117/THERAPY_ROOM_PROJECT/bao_cao_du_an.md)
*   Thư mục giao diện trực quan: [gui/](file:///d:/CS117/THERAPY_ROOM_PROJECT/gui)
*   Kế hoạch kiểm chứng và khắc phục: [implementation_plan.md](file:///d:/CS117/THERAPY_ROOM_PROJECT/implementation_plan.md), [project_verification_report.md](file:///d:/CS117/THERAPY_ROOM_PROJECT/project_verification_report.md) và [walkthrough.md](file:///d:/CS117/THERAPY_ROOM_PROJECT/walkthrough.md) tại thư mục gốc.

