# 01_GOAL_AND_SCOPE.md

# CS117 Node 1.1 — Mô hình hóa Tòa A thành Đồ thị Không gian

## 1. Mục tiêu

Mục tiêu của Node 1.1 là chuyển sơ đồ vật lý của **Tòa A UIT** thành một **đồ thị có trọng số** để phục vụ các bước tính toán sau này.

Đây không phải là một app lớn.
Không cần backend.
Không cần database.
Không cần frontend phức tạp.
Không cần deploy.

Chỉ cần một project Python nhỏ chạy trên máy cá nhân, giúp người làm đồ án có thể:

1. Nhìn thấy graph của Tòa A.
2. Kiểm tra các phòng/hành lang/cầu thang nằm ở đâu.
3. Kiểm tra các node và edge có hợp lý không.
4. Chạy thử thuật toán tìm đường ngắn nhất.
5. Chuẩn bị nền tảng cho bước sau: giả lập sinh viên di chuyển.

---

## 2. Ý tưởng toán học

Không gian vật lý của tòa nhà được mô hình hóa thành graph:

```txt
G = (V, E)
```

Trong đó:

* `V` là tập các đỉnh.
* `E` là tập các cạnh.

Mỗi đỉnh đại diện cho một điểm quan trọng trong không gian:

```txt
phòng
hành lang
giao điểm hành lang
cầu thang
lối vào
thư viện
kho
```

Mỗi cạnh đại diện cho một lối đi hợp lệ giữa hai điểm:

```txt
hành lang nối hành lang
cửa phòng nối ra hành lang
cầu thang nối giữa hai tầng
lối nối thư viện với khối chính
```

Mỗi cạnh có trọng số là khoảng cách đi bộ tương đối hoặc khoảng cách ước lượng theo mét.

---

## 3. Vì sao dùng graph?

Tòa A có hình dạng không đều, nhiều nhánh, nhiều cụm phòng và có khu Thư viện UIT nối với khối chính. Vì vậy không nên mô hình hóa bằng lưới đơn giản.

Graph phù hợp hơn vì:

1. Dễ biểu diễn hành lang, giao điểm, cầu thang.
2. Dễ thêm phòng mới.
3. Dễ chạy thuật toán tìm đường.
4. Dễ cộng lưu lượng sinh viên lên node/edge sau này.
5. Dễ mở rộng sang heatmap và tối ưu vị trí phòng tư vấn.

---

## 4. Phạm vi hiện tại

Chỉ làm cho **Tòa A**.

Có 2 tầng từ ảnh sơ đồ hiện tại:

```txt
Tầng 1
Tầng 2
```

Mỗi tầng cần có graph riêng, nhưng có thể lưu chung trong một file JSON.

---

## 5. Sản phẩm cần có

Project tối thiểu gồm:

```txt
building_a_graph.json
visualize_building_a.py
shortest_path_demo.py
README.md
```

Có thể thêm ảnh nền nếu muốn hiển thị graph chồng lên sơ đồ gốc:

```txt
assets/
  building_a_floor_1.jpg
  building_a_floor_2.jpg
```

---

## 6. Chức năng cần có

### 6.1. Visualize graph

File:

```txt
visualize_building_a.py
```

Chức năng:

1. Đọc dữ liệu từ `building_a_graph.json`.
2. Dựng graph bằng `networkx`.
3. Vẽ graph bằng `matplotlib`.
4. Tách hiển thị tầng 1 và tầng 2.
5. Hiển thị node, edge, label.
6. Lưu ảnh kết quả ra file PNG.

Output mong muốn:

```txt
building_a_floor_1_graph.png
building_a_floor_2_graph.png
```

---

### 6.2. Shortest path demo

File:

```txt
shortest_path_demo.py
```

Chức năng:

1. Đọc dữ liệu graph.
2. Chọn một node bắt đầu và một node kết thúc.
3. Chạy Dijkstra.
4. In đường đi ngắn nhất.
5. In tổng khoảng cách.
6. Vẽ graph với đường đi được highlight.

Ví dụ:

```txt
Start: A-F1-LIBRARY-CENTER
End:   A-F2-EAST-JUNCTION
```

---

## 7. Những gì chưa làm ở Node 1.1

Chưa cần làm:

```txt
database
web app
backend
API
user login
deploy
simulation sinh viên
heatmap thật
machine learning
tối ưu vị trí phòng tư vấn
```

Các phần đó để sau.

Node 1.1 chỉ cần chứng minh rằng ta đã biến được không gian vật lý thành graph có thể tính toán được.

---

## 8. Pipeline hiện tại

Pipeline đơn giản:

```txt
Ảnh sơ đồ Tòa A
        ↓
Xác định node quan trọng
        ↓
Xác định edge nối giữa các node
        ↓
Lưu thành JSON
        ↓
Vẽ graph bằng Python
        ↓
Chạy Dijkstra thử nghiệm
```

---

## 9. Pipeline tương lai

Sau này, khi có graph ổn định:

```txt
Graph Tòa A
        ↓
Gắn thời khóa biểu vào phòng
        ↓
Sinh sinh viên ảo theo năm/ngành
        ↓
Tìm đường đi giữa các phòng học
        ↓
Cộng lưu lượng lên node/edge
        ↓
Tạo heatmap
        ↓
Tính điểm visibility, privacy, stress
        ↓
Đề xuất vị trí phòng tư vấn
```

---

## 10. Tiêu chí hoàn thành Node 1.1

Node 1.1 được xem là hoàn thành khi:

1. Có file JSON mô tả graph Tòa A.
2. Có thể vẽ graph tầng 1.
3. Có thể vẽ graph tầng 2.
4. Có thể nối tầng 1 và tầng 2 bằng cầu thang.
5. Có thể chạy Dijkstra giữa hai node bất kỳ.
6. Có thể kiểm tra thủ công rằng cấu trúc phòng/hành lang/cầu thang hợp lý với sơ đồ.
7. Code đơn giản, dễ chỉnh sửa, không bị nặng về kỹ thuật phần mềm.

---

## 11. Ghi chú quan trọng

Ưu tiên của project này là:

```txt
đúng mô hình toán học > giao diện đẹp
graph hợp lý > tọa độ tuyệt đối chính xác
dễ kiểm chứng > code phức tạp
```

Tọa độ ban đầu có thể gần đúng. Sau này người làm đồ án có thể chỉnh dần tọa độ trong file JSON.
