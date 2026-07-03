# 03_CODEX_IMPLEMENTATION_TASKS.md

# Codex Implementation Tasks — Simple Local Graph Viewer

## 1. Mục tiêu triển khai

Hãy tạo một project Python đơn giản để mô hình hóa và visualize graph của Tòa A UIT.

Đây không phải là web app.
Không dùng backend.
Không dùng database.
Không cần UI phức tạp.

Chỉ cần code chạy local bằng Python.

---

## 2. File cần tạo

Tạo các file sau:

```txt
building_a_graph.json
visualize_building_a.py
shortest_path_demo.py
README.md
```

Có thể tạo thêm thư mục:

```txt
assets/
```

Nếu có ảnh nền, đặt ảnh vào:

```txt
assets/building_a_floor_1.jpg
assets/building_a_floor_2.jpg
```

---

## 3. Thư viện Python cần dùng

Dùng các thư viện đơn giản:

```txt
networkx
matplotlib
json
math
```

Không dùng framework nặng.

Có thể cài bằng:

```bash
pip install networkx matplotlib
```

---

# 4. File `building_a_graph.json`

## 4.1. Cấu trúc tổng quát

File JSON cần có cấu trúc:

```json
{
  "building": "A",
  "coordinate_system": {
    "type": "normalized",
    "width": 1000,
    "height": 1000
  },
  "floors": {
    "1": {
      "nodes": [],
      "edges": []
    },
    "2": {
      "nodes": [],
      "edges": []
    }
  },
  "inter_floor_edges": []
}
```

---

## 4.2. Node schema

Mỗi node có dạng:

```json
{
  "id": "A-F1-CENTER-01",
  "label": "Center 01",
  "type": "junction",
  "floor": 1,
  "x": 500,
  "y": 500,
  "zone": "A-F1-CENTER",
  "accessible": true,
  "candidate": false,
  "notes": ""
}
```

Các field bắt buộc:

```txt
id
label
type
floor
x
y
zone
accessible
```

Các field tùy chọn:

```txt
candidate
notes
```

---

## 4.3. Edge schema

Mỗi edge có dạng:

```json
{
  "source": "A-F1-CENTER-01",
  "target": "A-F1-CENTER-02",
  "distance": 20,
  "type": "corridor",
  "bidirectional": true,
  "accessible": true,
  "notes": ""
}
```

Các field bắt buộc:

```txt
source
target
distance
type
bidirectional
accessible
```

---

## 4.4. Inter-floor edge schema

Kết nối giữa hai tầng đặt trong `inter_floor_edges`.

Ví dụ:

```json
{
  "source": "A-F1-WEST-STAIR",
  "target": "A-F2-WEST-STAIR",
  "distance": 10,
  "type": "stair",
  "bidirectional": true,
  "accessible": true,
  "notes": "Temporary vertical connector, needs verification"
}
```

---

# 5. Dữ liệu graph ban đầu

Hãy tạo dữ liệu graph nháp cho Tòa A theo các node dưới đây.

## 5.1. Tầng 1 — nodes

Tạo các node sau với tọa độ x, y gần đúng trong hệ 0–1000:

```txt
A-F1-LIBRARY-CENTER
A-F1-LIBRARY-ENTRANCE
A-F1-LIBRARY-CONNECTOR-01
A-F1-LIBRARY-CONNECTOR-02

A-F1-WEST-JUNCTION
A-F1-WEST-STAIR
A-F1-WEST-ROOM-01
A-F1-WEST-ROOM-02

A-F1-CENTER-01
A-F1-CENTER-02
A-F1-CENTER-03
A-F1-CENTER-04

A-F1-NORTH-JUNCTION
A-F1-NORTH-STAIR
A-F1-NORTH-ROOM-01
A-F1-NORTH-ROOM-02
A-F1-NORTH-ROOM-03

A-F1-EAST-JUNCTION
A-F1-EAST-STAIR
A-F1-EAST-ROOM-01
A-F1-EAST-ROOM-02
A-F1-EAST-ROOM-03
A-F1-EAST-ROOM-04

A-F1-SOUTH-JUNCTION
A-F1-SOUTH-STAIR
A-F1-YOU-ARE-HERE
A-F1-SOUTH-ROOM-01
A-F1-SOUTH-ROOM-02
A-F1-SOUTH-ROOM-03
```

Gợi ý tọa độ tương đối:

```txt
Library ở bên trái/dưới
West wing ở bên trái khối chính
Center ở giữa khối chính
North wing ở phía trên
East wing ở phía phải
South wing ở phía dưới
```

---

## 5.2. Tầng 1 — edges

Tạo các edge chính:

```txt
A-F1-LIBRARY-CENTER <-> A-F1-LIBRARY-ENTRANCE
A-F1-LIBRARY-ENTRANCE <-> A-F1-LIBRARY-CONNECTOR-01
A-F1-LIBRARY-CONNECTOR-01 <-> A-F1-LIBRARY-CONNECTOR-02
A-F1-LIBRARY-CONNECTOR-02 <-> A-F1-WEST-JUNCTION

A-F1-WEST-JUNCTION <-> A-F1-CENTER-01
A-F1-CENTER-01 <-> A-F1-CENTER-02
A-F1-CENTER-02 <-> A-F1-CENTER-03
A-F1-CENTER-03 <-> A-F1-CENTER-04
A-F1-CENTER-04 <-> A-F1-CENTER-01

A-F1-CENTER-02 <-> A-F1-NORTH-JUNCTION
A-F1-CENTER-03 <-> A-F1-EAST-JUNCTION
A-F1-CENTER-04 <-> A-F1-SOUTH-JUNCTION

A-F1-WEST-JUNCTION <-> A-F1-WEST-STAIR
A-F1-NORTH-JUNCTION <-> A-F1-NORTH-STAIR
A-F1-EAST-JUNCTION <-> A-F1-EAST-STAIR
A-F1-SOUTH-JUNCTION <-> A-F1-SOUTH-STAIR
A-F1-SOUTH-JUNCTION <-> A-F1-YOU-ARE-HERE
```

Nối các phòng vào junction gần nhất:

```txt
A-F1-WEST-JUNCTION <-> A-F1-WEST-ROOM-01
A-F1-WEST-JUNCTION <-> A-F1-WEST-ROOM-02

A-F1-NORTH-JUNCTION <-> A-F1-NORTH-ROOM-01
A-F1-NORTH-JUNCTION <-> A-F1-NORTH-ROOM-02
A-F1-NORTH-JUNCTION <-> A-F1-NORTH-ROOM-03

A-F1-EAST-JUNCTION <-> A-F1-EAST-ROOM-01
A-F1-EAST-JUNCTION <-> A-F1-EAST-ROOM-02
A-F1-EAST-JUNCTION <-> A-F1-EAST-ROOM-03
A-F1-EAST-JUNCTION <-> A-F1-EAST-ROOM-04

A-F1-SOUTH-JUNCTION <-> A-F1-SOUTH-ROOM-01
A-F1-SOUTH-JUNCTION <-> A-F1-SOUTH-ROOM-02
A-F1-SOUTH-JUNCTION <-> A-F1-SOUTH-ROOM-03
```

---

## 5.3. Tầng 2 — nodes

Tạo các node sau:

```txt
A-F2-RING-NORTH
A-F2-RING-EAST
A-F2-RING-SOUTH
A-F2-RING-WEST

A-F2-WEST-JUNCTION
A-F2-WEST-STAIR
A-F2-WEST-ROOM-01
A-F2-WEST-ROOM-02

A-F2-NORTH-JUNCTION
A-F2-NORTH-STAIR
A-F2-NORTH-ROOM-01
A-F2-NORTH-ROOM-02
A-F2-NORTH-ROOM-03

A-F2-EAST-JUNCTION
A-F2-EAST-STAIR
A-F2-EAST-ROOM-01
A-F2-EAST-ROOM-02
A-F2-EAST-ROOM-03

A-F2-SOUTH-JUNCTION
A-F2-SOUTH-STAIR
A-F2-SOUTH-ROOM-01
A-F2-SOUTH-ROOM-02
A-F2-SOUTH-ROOM-03

A-F2-STORAGE-01
A-F2-STORAGE-02
```

---

## 5.4. Tầng 2 — edges

Vòng trung tâm:

```txt
A-F2-RING-NORTH <-> A-F2-RING-EAST
A-F2-RING-EAST <-> A-F2-RING-SOUTH
A-F2-RING-SOUTH <-> A-F2-RING-WEST
A-F2-RING-WEST <-> A-F2-RING-NORTH
```

Kết nối các cánh:

```txt
A-F2-RING-WEST <-> A-F2-WEST-JUNCTION
A-F2-RING-NORTH <-> A-F2-NORTH-JUNCTION
A-F2-RING-EAST <-> A-F2-EAST-JUNCTION
A-F2-RING-SOUTH <-> A-F2-SOUTH-JUNCTION
```

Cầu thang:

```txt
A-F2-WEST-JUNCTION <-> A-F2-WEST-STAIR
A-F2-NORTH-JUNCTION <-> A-F2-NORTH-STAIR
A-F2-EAST-JUNCTION <-> A-F2-EAST-STAIR
A-F2-SOUTH-JUNCTION <-> A-F2-SOUTH-STAIR
```

Phòng:

```txt
A-F2-WEST-JUNCTION <-> A-F2-WEST-ROOM-01
A-F2-WEST-JUNCTION <-> A-F2-WEST-ROOM-02

A-F2-NORTH-JUNCTION <-> A-F2-NORTH-ROOM-01
A-F2-NORTH-JUNCTION <-> A-F2-NORTH-ROOM-02
A-F2-NORTH-JUNCTION <-> A-F2-NORTH-ROOM-03

A-F2-EAST-JUNCTION <-> A-F2-EAST-ROOM-01
A-F2-EAST-JUNCTION <-> A-F2-EAST-ROOM-02
A-F2-EAST-JUNCTION <-> A-F2-EAST-ROOM-03

A-F2-SOUTH-JUNCTION <-> A-F2-SOUTH-ROOM-01
A-F2-SOUTH-JUNCTION <-> A-F2-SOUTH-ROOM-02
A-F2-SOUTH-JUNCTION <-> A-F2-SOUTH-ROOM-03
```

Storage:

```txt
A-F2-STORAGE-01
A-F2-STORAGE-02
```

Storage nodes can be isolated or connected with `accessible = false`.

---

## 5.5. Inter-floor edges

Tạo các edge nối tầng:

```txt
A-F1-WEST-STAIR <-> A-F2-WEST-STAIR
A-F1-NORTH-STAIR <-> A-F2-NORTH-STAIR
A-F1-EAST-STAIR <-> A-F2-EAST-STAIR
A-F1-SOUTH-STAIR <-> A-F2-SOUTH-STAIR
```

---

# 6. File `visualize_building_a.py`

## 6.1. Chức năng

Script này cần:

1. Load `building_a_graph.json`.
2. Tạo NetworkX graph.
3. Vẽ riêng tầng 1.
4. Vẽ riêng tầng 2.
5. Mỗi node type có marker hoặc màu khác nhau.
6. Hiển thị label node.
7. Hiển thị edge.
8. Lưu ảnh PNG.

Output:

```txt
building_a_floor_1_graph.png
building_a_floor_2_graph.png
```

---

## 6.2. Yêu cầu vẽ

Node nên được phân biệt theo type:

```txt
room: hình tròn nhỏ
junction: hình tròn lớn hơn
corridor: chấm nhỏ
stair: hình vuông
library: hình sao hoặc node lớn
storage: node xám hoặc node có dấu X
entrance: hình tam giác
```

Nếu không muốn phức tạp, chỉ cần dùng màu khác nhau cho từng type.

Edge nên được vẽ bằng đường mảnh.

Label nên hiển thị nhỏ để không quá rối.

---

## 6.3. Optional background image

Nếu có ảnh nền:

```txt
assets/building_a_floor_1.jpg
assets/building_a_floor_2.jpg
```

thì script có thể hiển thị ảnh nền dưới graph bằng `imshow`.

Nếu không có ảnh nền, vẫn phải vẽ graph bình thường.

---

# 7. File `shortest_path_demo.py`

## 7.1. Chức năng

Script này cần:

1. Load `building_a_graph.json`.
2. Tạo graph gồm cả tầng 1, tầng 2 và inter-floor edges.
3. Chọn start node và end node trong code.
4. Chạy Dijkstra bằng trọng số `distance`.
5. In ra đường đi.
6. In tổng khoảng cách.
7. Vẽ graph với path được highlight.

Ví dụ:

```python
start = "A-F1-LIBRARY-CENTER"
end = "A-F2-EAST-JUNCTION"
```

Output dạng text:

```txt
Shortest path:
A-F1-LIBRARY-CENTER
→ A-F1-LIBRARY-ENTRANCE
→ A-F1-LIBRARY-CONNECTOR-01
→ ...
→ A-F2-EAST-JUNCTION

Total distance: 120.5
```

---

# 8. Hàm cần viết

## 8.1. `load_graph_data`

```python
def load_graph_data(path: str) -> dict:
    pass
```

Đọc JSON.

---

## 8.2. `build_graph`

```python
def build_graph(data: dict, floor: int | None = None) -> nx.Graph:
    pass
```

Nếu `floor` là 1 hoặc 2 thì chỉ build graph của tầng đó.
Nếu `floor` là `None` thì build graph toàn bộ tòa, gồm cả inter-floor edges.

---

## 8.3. `draw_floor_graph`

```python
def draw_floor_graph(data: dict, floor: int, output_path: str) -> None:
    pass
```

Vẽ một tầng.

---

## 8.4. `find_shortest_path`

```python
def find_shortest_path(G: nx.Graph, start: str, end: str) -> tuple[list[str], float]:
    pass
```

Trả về:

```txt
path node list
total distance
```

---

## 8.5. `validate_graph`

Có thể viết đơn giản:

```python
def validate_graph(data: dict) -> list[str]:
    pass
```

Kiểm tra:

1. Có node trùng ID không.
2. Edge source/target có tồn tại không.
3. Có node cô lập không.
4. Graph có liên thông không.
5. Edge có distance hợp lệ không.

---

# 9. README.md

README cần ghi:

```txt
# Building A Graph Visualization

This is a simple local Python project for CS117 Node 1.1.

The goal is to convert Building A into a weighted graph, where rooms, corridors, stairs, and junctions are nodes, and walking paths are edges.

## How to run

pip install networkx matplotlib

python visualize_building_a.py

python shortest_path_demo.py

## Files

building_a_graph.json: graph data
visualize_building_a.py: visualize floor graphs
shortest_path_demo.py: run Dijkstra shortest path demo

## Future work

This graph will later be used to simulate student movement and generate traffic heatmaps.
```

---

# 10. Nguyên tắc code

Codex cần giữ code đơn giản:

1. Không tạo web app.
2. Không tạo database.
3. Không dùng class phức tạp nếu chưa cần.
4. Không hard-code quá nhiều trong hàm vẽ.
5. Dữ liệu graph phải nằm trong JSON.
6. Code phải dễ chỉnh sửa tọa độ node.
7. Nếu ảnh nền không tồn tại, chương trình vẫn chạy.
8. Nếu node/edge lỗi, in warning rõ ràng.
9. Không cần tối ưu quá mức.
10. Ưu tiên dễ hiểu để đưa vào báo cáo CS117.

---

# 11. Acceptance criteria

Hoàn thành khi:

1. Chạy được `python visualize_building_a.py`.
2. Sinh ra ảnh graph tầng 1.
3. Sinh ra ảnh graph tầng 2.
4. Chạy được `python shortest_path_demo.py`.
5. In được đường đi ngắn nhất.
6. Có thể đi từ thư viện tầng 1 lên một node tầng 2.
7. File JSON dễ đọc và dễ sửa.
8. Graph nhìn tương đối giống cấu trúc Tòa A.
9. Không có app phức tạp ngoài phạm vi bài toán.
10. Có thể dùng ảnh graph trong báo cáo hoặc poster.
