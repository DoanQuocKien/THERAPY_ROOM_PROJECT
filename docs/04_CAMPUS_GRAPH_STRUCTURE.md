# 04_CAMPUS_GRAPH_STRUCTURE.md

# CS117 Node 1.1 — Campus Graph cho toàn UIT

## 1. Mục tiêu

Sau khi đã dựng graph chi tiết cho Tòa A, bước tiếp theo là mở rộng mô hình sang toàn bộ khuôn viên UIT.

Từ bây giờ, graph không chỉ gồm các phòng bên trong từng tòa, mà cần thêm một lớp graph ngoài trời để kết nối các tòa với nhau.

Ta chia hệ thống thành 2 lớp:

```txt
Layer 1: Campus Graph
Layer 2: Building Graph
```

Trong đó:

* `Campus Graph` mô hình hóa đường đi ngoài trời, cổng trường, lối vào các tòa, node access giữa các tòa.
* `Building Graph` mô hình hóa phòng, hành lang, cầu thang, thang máy bên trong từng tòa.

Mục tiêu cuối cùng là có thể tìm đường từ một phòng bất kỳ ở tòa này sang một phòng bất kỳ ở tòa khác.

Ví dụ:

```txt
A-F1-TOP-ROOM-01
    ↓
A-F1-ENTRANCE
    ↓
CAMPUS-WALKWAY-A-C
    ↓
C-F2-ENTRANCE
    ↓
C-F2-CORRIDOR
    ↓
C205
```

---

## 2. Tư duy graph toàn trường

Toàn bộ UIT sẽ được xem như một graph lớn:

```txt
G_UIT = (V_campus ∪ V_buildings, E_campus ∪ E_buildings ∪ E_access)
```

Trong đó:

* `V_campus`: node ngoài trời.
* `V_buildings`: node trong các tòa.
* `E_campus`: đường đi ngoài trời.
* `E_buildings`: đường đi trong tòa.
* `E_access`: cạnh nối từ ngoài trời vào cửa tòa.

---

## 3. Các tòa cần mô hình hóa

Các tòa chính:

```txt
A
B
C
D
E
```

Ngoài ra cần có:

```txt
GATE_A
GATE_B
CANTEEN
OUTDOOR_WALKWAY
```

Nếu chưa muốn dựng canteen thành building riêng, có thể giữ canteen như một node ngoài trời.

---

## 4. Campus node types

Dùng các loại node sau cho campus graph:

```txt
gate
outdoor
walkway
building_access
building_anchor
canteen
intersection
```

Ý nghĩa:

| Type              | Ý nghĩa                                                |
| ----------------- | ------------------------------------------------------ |
| `gate`            | Cổng trường                                            |
| `outdoor`         | Điểm ngoài trời chung                                  |
| `walkway`         | Điểm trên đường đi bộ                                  |
| `building_access` | Điểm trước cửa/lối vào tòa                             |
| `building_anchor` | Node đại diện vị trí tổng quát của một tòa trên bản đồ |
| `canteen`         | Căn tin hoặc khu dịch vụ                               |
| `intersection`    | Giao điểm đường đi ngoài trời                          |

---

## 5. Campus edge types

```txt
outdoor_walk
building_entry
gate_entry
campus_connector
```

Ý nghĩa:

| Type               | Ý nghĩa                                    |
| ------------------ | ------------------------------------------ |
| `outdoor_walk`     | Đi bộ ngoài trời                           |
| `building_entry`   | Cạnh nối từ ngoài trời vào tòa             |
| `gate_entry`       | Cạnh nối từ cổng vào đường đi trong trường |
| `campus_connector` | Cạnh kết nối hai khu vực ngoài trời lớn    |

---

## 6. Quy ước tọa độ campus

Dùng hệ tọa độ chuẩn hóa:

```txt
x ∈ [0, 1000]
y ∈ [0, 1000]
```

Tọa độ dựa trên ảnh bản đồ toàn UIT.

Quy ước tương đối:

```txt
Tòa A: phía trên-trái
Tòa B: phía trên-phải / giữa-phải
Tòa C: phía giữa-dưới
Tòa D: phía dưới
Tòa E: phía trái
Cổng A: phía trái-trên
Cổng B: phía phải-dưới
```

Tọa độ không cần tuyệt đối chính xác. Quan trọng là quan hệ không gian và kết nối giữa các tòa hợp lý.

---

## 7. Campus nodes đề xuất

```txt
UIT-GATE-A
UIT-GATE-B

UIT-OUTDOOR-A-FRONT
UIT-OUTDOOR-B-FRONT
UIT-OUTDOOR-C-FRONT
UIT-OUTDOOR-D-FRONT
UIT-OUTDOOR-E-FRONT

UIT-WALKWAY-A-E
UIT-WALKWAY-A-B
UIT-WALKWAY-A-C
UIT-WALKWAY-B-C
UIT-WALKWAY-C-D
UIT-WALKWAY-D-GATE-B
UIT-WALKWAY-E-C

UIT-INTERSECTION-CENTER
UIT-INTERSECTION-CANTEEN
UIT-CANTEEN
```

---

## 8. Building access nodes

Mỗi tòa cần ít nhất một node access ngoài trời và một node entrance trong tòa.

Ví dụ với tòa A:

```txt
Campus side:
UIT-OUTDOOR-A-FRONT

Building side:
A-F1-BUILDING-ENTRANCE
```

Cạnh nối:

```txt
UIT-OUTDOOR-A-FRONT <-> A-F1-BUILDING-ENTRANCE
```

Tương tự:

```txt
UIT-OUTDOOR-B-FRONT <-> B-F1-BUILDING-ENTRANCE
UIT-OUTDOOR-C-FRONT <-> C-F1-BUILDING-ENTRANCE
UIT-OUTDOOR-D-FRONT <-> D-F1-BUILDING-ENTRANCE
UIT-OUTDOOR-E-FRONT <-> E-F1-BUILDING-ENTRANCE
```

---

## 9. Campus topology đề xuất

Dựa theo bản đồ tổng thể, có thể mô hình hóa skeleton ngoài trời như sau:

```txt
                    UIT-GATE-A
                        |
                 UIT-OUTDOOR-A-FRONT
                   /        |        \
                  /         |         \
      UIT-OUTDOOR-E-FRONT   |   UIT-OUTDOOR-B-FRONT
                  \         |         /
                   \        |        /
                 UIT-INTERSECTION-CENTER
                        |
                UIT-OUTDOOR-C-FRONT
                        |
              UIT-INTERSECTION-CANTEEN
                    /          \
                   /            \
        UIT-OUTDOOR-D-FRONT   UIT-GATE-B
```

Cấu trúc này không cần mô phỏng từng mét đường, chỉ cần đủ để pathfinding đi được giữa các tòa.

---

## 10. Campus edges đề xuất

```txt
UIT-GATE-A <-> UIT-OUTDOOR-A-FRONT

UIT-OUTDOOR-A-FRONT <-> UIT-WALKWAY-A-E
UIT-WALKWAY-A-E <-> UIT-OUTDOOR-E-FRONT

UIT-OUTDOOR-A-FRONT <-> UIT-WALKWAY-A-B
UIT-WALKWAY-A-B <-> UIT-OUTDOOR-B-FRONT

UIT-OUTDOOR-A-FRONT <-> UIT-WALKWAY-A-C
UIT-WALKWAY-A-C <-> UIT-INTERSECTION-CENTER

UIT-OUTDOOR-B-FRONT <-> UIT-WALKWAY-B-C
UIT-WALKWAY-B-C <-> UIT-INTERSECTION-CENTER

UIT-OUTDOOR-E-FRONT <-> UIT-WALKWAY-E-C
UIT-WALKWAY-E-C <-> UIT-INTERSECTION-CENTER

UIT-INTERSECTION-CENTER <-> UIT-OUTDOOR-C-FRONT
UIT-OUTDOOR-C-FRONT <-> UIT-INTERSECTION-CANTEEN

UIT-INTERSECTION-CANTEEN <-> UIT-CANTEEN
UIT-INTERSECTION-CANTEEN <-> UIT-OUTDOOR-D-FRONT
UIT-INTERSECTION-CANTEEN <-> UIT-GATE-B
```

---

## 11. Building entry edges

```txt
UIT-OUTDOOR-A-FRONT <-> A-F1-BUILDING-ENTRANCE
UIT-OUTDOOR-B-FRONT <-> B-F1-BUILDING-ENTRANCE
UIT-OUTDOOR-C-FRONT <-> C-F1-BUILDING-ENTRANCE
UIT-OUTDOOR-D-FRONT <-> D-F1-BUILDING-ENTRANCE
UIT-OUTDOOR-E-FRONT <-> E-F1-BUILDING-ENTRANCE
```

Các cạnh này có type:

```txt
building_entry
```

---

## 12. Gợi ý distance

Khoảng cách trong campus graph chỉ cần tương đối.

Ví dụ:

```txt
Gate A → A Front: 20
A Front → E Front: 35
A Front → B Front: 45
A Front → Center Intersection: 50
B Front → Center Intersection: 35
E Front → Center Intersection: 40
Center Intersection → C Front: 25
C Front → Canteen Intersection: 25
Canteen Intersection → D Front: 35
Canteen Intersection → Gate B: 30
```

Distance ban đầu không cần chính xác theo mét. Sau này có thể calibrate.

---

## 13. JSON structure đề xuất

Campus graph nên được lưu trong file riêng:

```txt
campus_graph.json
```

Cấu trúc:

```json
{
  "campus": "UIT",
  "coordinate_system": {
    "type": "normalized",
    "width": 1000,
    "height": 1000
  },
  "nodes": [],
  "edges": [],
  "building_entry_edges": []
}
```

---

## 14. Node schema

```json
{
  "id": "UIT-OUTDOOR-A-FRONT",
  "label": "Outdoor A Front",
  "type": "building_access",
  "x": 330,
  "y": 220,
  "accessible": true,
  "notes": "Outdoor access point near Building A"
}
```

---

## 15. Edge schema

```json
{
  "source": "UIT-OUTDOOR-A-FRONT",
  "target": "UIT-INTERSECTION-CENTER",
  "distance": 50,
  "type": "outdoor_walk",
  "bidirectional": true,
  "accessible": true
}
```

---

## 16. Acceptance checklist

Campus graph đúng nếu:

1. Có node cổng A.
2. Có node cổng B.
3. Có node access cho A, B, C, D, E.
4. Có đường ngoài trời nối giữa các tòa.
5. Có thể tìm path từ Gate A đến Building D.
6. Có thể tìm path từ Building E đến Building B.
7. Có thể nối campus graph với graph nội bộ từng tòa.
8. Sau này sinh viên có thể đi từ phòng trong tòa này sang phòng trong tòa khác.
