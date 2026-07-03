# Báo cáo Kiểm chứng Dự án (Project Verification Report)

**Dự án:** Hệ thống Đánh giá và Xếp hạng vị trí Phòng Tư vấn Tâm lý tại UIT  
**Môn học:** Tư duy Tính toán / Tư duy AI (CS117)

---

## 1. Bản đồ Ánh xạ (Mapping) từ Báo cáo tới Mã nguồn thực tế

Dưới đây là bảng đối chiếu chi tiết giữa các module chức năng được đặc tả trong Báo cáo dự án và Cây phân rã bài toán (Decomposition Tree) với mã nguồn Python hiện tại trong thư mục [src/](file:///d:/CS117/THERAPY_ROOM_PROJECT/src):

| Phân hệ (Breakdown Node) | Chức năng Đặc tả | Mã nguồn Chịu trách nhiệm | Trạng thái Chức năng |
|---|---|---|---|
| **P1.1: Sort Events** | Sắp xếp thời khóa biểu theo trình tự thời gian | [simulate_students.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/simulate_students.py) | ✅ Đã triển khai và hoạt động tốt |
| **P1.3: Extract O-D Pairs** | Trích xuất cặp di chuyển (phòng học kế tiếp) | [simulate_students.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/simulate_students.py) | ✅ Đã triển khai (hàm `match_courses_to_timetable` & `generate_routes_for_schedule`) |
| **P2.1: Route Finder** | Tìm đường đi ngắn nhất giữa hai phòng (Dijkstra) | [graph_utils.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/graph_utils.py) & [simulate_students.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/simulate_students.py) | ✅ Đã triển khai thuật toán Dijkstra bằng thư viện NetworkX |
| **P2.2: Node Traffic** | Đếm và tích lũy lưu lượng đi qua từng đỉnh trên đồ thị | [simulate_students.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/simulate_students.py) (hàm `accumulate_traffic`) | ✅ Đã triển khai, xuất ra `outputs/node_1_2/node_traffic.json` |
| **P2.3: Edge Traffic** | Đếm và tích lũy lưu lượng đi qua từng cạnh trên đồ thị | [simulate_students.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/simulate_students.py) (hàm `accumulate_traffic`) | ✅ Đã triển khai, xuất ra `outputs/node_1_2/edge_traffic.json` |
| **P2.4: Access Node Pass Count**| Lấy lưu lượng đi ngang cửa các phòng ứng viên | [simulate_students.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/simulate_students.py) | ✅ Đã tích lũy đầy đủ trên toàn đồ thị |
| **P3: Accessibility Evaluation** | Tính WTC và chuẩn hóa Min-Max điểm Accessibility | [rank_candidates.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/rank_candidates.py) (hàm `evaluate_accessibility`) | ✅ Đã triển khai bổ sung |
| **P4: Visibility Evaluation** | BFS tìm Exposure zone, tính visibility với decay λ | [rank_candidates.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/rank_candidates.py) (hàm `evaluate_visibility`) | ✅ Đã triển khai bổ sung |
| **P5: Privacy Evaluation** | BFS tìm Sensitive zone, tính risk và chuẩn hóa Privacy | [rank_candidates.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/rank_candidates.py) (hàm `evaluate_privacy`) | ✅ Đã triển khai bổ sung |
| **P6: Rank & Report** | Tổ hợp tuyến tính (Weighted Scalarization) & Trade-off | [rank_candidates.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/rank_candidates.py) (hàm `main` & `generate_trade_off_report`) | ✅ Đã triển khai bổ sung, xuất bảng so sánh và giải thích |

---

## 2. Kết quả Chạy Kiểm chứng Hệ thống (Verification Results)

### 2.1. Kiểm chứng dữ liệu đồ thị không gian (D2)
Chạy script kiểm chứng đồ thị [validate_all_graphs.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/validate_all_graphs.py):
*   **Lệnh thực thi:** `python src/validate_all_graphs.py`
*   **Kết quả:** `All graph validations passed.` (Không phát hiện lỗi đỉnh trùng lặp, mất kết nối, hoặc thiếu Access Node cho các phòng học).

### 2.2. Kiểm chứng kết quả mô phỏng (Simulation Output Validation)
Chạy script kiểm chứng kết quả mô phỏng di chuyển sinh viên [validate_simulation.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/validate_simulation.py):
*   **Lệnh thực thi:** `python src/validate_simulation.py`
*   **Kết quả:** Đã xuất ra báo cáo `simulation_output_validation_report.json` với **0 lỗi (Errors: 0)**. Các tệp dữ liệu lưu lượng di chuyển `node_traffic.json` và `edge_traffic.json` đã được tạo đầy đủ và đúng cấu trúc.

### 2.3. Chạy thực nghiệm bộ công cụ Xếp hạng Phòng ứng viên (Ranking Engine)
Chúng tôi đã bổ sung và chạy thử nghiệm thành công công cụ xếp hạng phòng ứng viên [rank_candidates.py](file:///d:/CS117/THERAPY_ROOM_PROJECT/src/rank_candidates.py) trên 4 phòng ứng viên chính (`B1.02`, `A-F2-RIGHT-ROOM-01`, `A-F1-TOP-ROOM-01`, `C103`):
*   **Lệnh thực thi:** `python src/rank_candidates.py`
*   **Bảng xếp hạng kết quả đầu ra:**

```txt
==============================================================================================================
RANK  ROOM                ACCESSIBILITY     VISIBILITY     PRIVACY        FINAL SCORE    
==============================================================================================================
1     B1.02               1.0000            0.1103         0.8874         0.8102         
2     A-F2-RIGHT-ROOM-01  0.1476            0.0000         1.0000         0.5517         
3     A-F1-TOP-ROOM-01    0.8601            1.0000         0.0000         0.4510         
4     C103                0.0000            0.2675         0.7193         0.3998         
==============================================================================================================
```

*   **Nhận xét phân tích Đánh đổi (Rule-based Trade-off):**
    *   **B1.02 (Hạng 1 - Final Score: 0.8102):** Đạt điểm tiếp cận tuyệt đối (1.00), độ riêng tư cao (0.89), độ hiển thị thấp (0.11). Đây là căn phòng tối ưu nhất theo cấu hình trọng số ưu tiên riêng tư $50\%$.
    *   **A-F1-TOP-ROOM-01 (Hạng 3 - Final Score: 0.4510):** Độ hiển thị tối đa (1.00) và tiếp cận tốt (0.86), nhưng điểm riêng tư bằng $0.0$ do nằm sát tuyến hành lang chính đông đúc. Hệ thống tự động cảnh báo: *"Mật độ giao thông rất lớn (1101 lượt). Yêu cầu lắp đặt vách cách âm, rèm che và biển báo hạn chế tụ tập."*
    *   **C103 (Hạng 4 - Final Score: 0.3998):** Khoảng cách đi lại trung bình lớn (WTC = 245.8m). Hệ thống tự động cảnh báo: *"Vị trí xa giảng đường chính, cần thiết lập sơ đồ hướng dẫn tại sảnh chính."*

---

## 3. Các Phần còn thiếu và Kế hoạch Tiếp theo (What to do next)

### 3.1. Các phần còn thiếu trong dự án
1.  **Thay thế các liên kết Demo (GitHub, YouTube) bằng link thật:** Báo cáo hiện vẫn đang để cảnh báo link placeholder trong Section 13.4.
2.  **Kịch bản Sensitivity Analysis tự động:** Chưa có script tự động quét qua các dải trọng số khác nhau ($w_P, w_A, w_V$) để vẽ biểu đồ sự thay đổi thứ hạng của các candidate.

### 3.2. Kế hoạch tiếp theo (Next Steps)
1.  **Cập nhật Link thực tế:** Thu âm video demo và đăng tải mã nguồn lên GitHub, sau đó thay thế các URL placeholder trong Section 13.4 của `bao_cao_du_an.md`.
2.  **sensitivity_analysis.py:** Phát triển một script nhỏ chạy quét bộ ba trọng số từ $0.0$ đến $1.0$ (bước nhảy $0.05$) để kiểm chứng độ nhạy của thuật toán xếp hạng, từ đó giúp stakeholder dễ đưa ra quyết định khi muốn thay đổi độ ưu tiên.
3.  **Đóng gói Báo cáo:** Xuất bản tài liệu `bao_cao_du_an.md` thành file PDF để chuẩn bị nộp bài.
