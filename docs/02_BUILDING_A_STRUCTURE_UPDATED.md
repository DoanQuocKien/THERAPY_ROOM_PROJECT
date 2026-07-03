# 02_BUILDING_A_STRUCTURE_UPDATED.md

# Cấu trúc Graph cập nhật cho Tòa A UIT

## 1. Tư duy mô hình hóa mới

Không nối trực tiếp `junction -> room` một cách quá đơn giản.

Thay vào đó, mỗi phòng nên có một node trung gian gọi là **access node** hoặc **door node**.

Cấu trúc đúng hơn:

```txt
main walking path
      ↓
room access node
      ↓
room node
```

Ví dụ:

```txt
A-F1-TOP-PATH-02
      ↓
A-F1-TOP-ROOM-03-ACCESS
      ↓
A-F1-TOP-ROOM-03
```

Ý nghĩa:

* `PATH/JUNCTION`: nơi sinh viên thật sự đi bộ qua.
* `ACCESS`: điểm trước cửa phòng, nằm trên hoặc sát hành lang.
* `ROOM`: không gian bên trong phòng.

Cách này giúp sau này mô phỏng được:

1. Sinh viên đi ngang qua phòng.
2. Sinh viên rẽ vào phòng.
3. Traffic trên hành lang.
4. Traffic trước cửa phòng.
5. Heatmap theo trục di chuyển chính.

---

## 2. Node types

Dùng các type sau:

```txt
room
access
corridor
junction
stair
library
storage
entrance
```

Trong đó:

| Type       | Ý nghĩa                       |
| ---------- | ----------------------------- |
| `room`     | Phòng thật sự                 |
| `access`   | Điểm tiếp cận/cửa trước phòng |
| `corridor` | Điểm trên hành lang           |
| `junction` | Ngã rẽ/ngã tư                 |
| `stair`    | Cầu thang                     |
| `library`  | Khu thư viện                  |
| `storage`  | Kho                           |
| `entrance` | Lối vào/ra                    |

---

## 3. Cấu trúc tổng quát tầng 1

Tầng 1 nên được mô hình hóa theo 2 lớp:

```txt
Lớp 1: Trục đi bộ chính
Lớp 2: Các access node dẫn vào phòng
```

Trục đi bộ chính của tầng 1 gồm:

1. Một vòng/hình vuông chính bao quanh khu trung tâm.
2. Một ngã tư ở giữa.
3. Một nhánh nối sang thư viện.
4. Các cầu thang ở những vị trí chính.

Sơ đồ logic:

```txt
                  TOP-LEFT -------- TOP-MID -------- TOP-RIGHT
                     |                                  |
                     |                                  |
                 LEFT-MID -------- CENTER -------- RIGHT-MID
                     |                                  |
                     |                                  |
               BOTTOM-LEFT ---- BOTTOM-MID ---- BOTTOM-RIGHT
```

Trong đó `CENTER` là ngã tư ở giữa.

---

# 4. Tầng 1 — Main walking path

## 4.1. Outer square/ring nodes

Các node trục chính hình vuông:

```txt
A-F1-RING-TOP-LEFT
A-F1-RING-TOP-MID
A-F1-RING-TOP-RIGHT

A-F1-RING-LEFT-MID
A-F1-RING-CENTER
A-F1-RING-RIGHT-MID

A-F1-RING-BOTTOM-LEFT
A-F1-RING-BOTTOM-MID
A-F1-RING-BOTTOM-RIGHT
```

Các edge chính:

```txt
A-F1-RING-TOP-LEFT <-> A-F1-RING-TOP-MID
A-F1-RING-TOP-MID <-> A-F1-RING-TOP-RIGHT

A-F1-RING-TOP-LEFT <-> A-F1-RING-LEFT-MID
A-F1-RING-TOP-RIGHT <-> A-F1-RING-RIGHT-MID

A-F1-RING-LEFT-MID <-> A-F1-RING-BOTTOM-LEFT
A-F1-RING-RIGHT-MID <-> A-F1-RING-BOTTOM-RIGHT

A-F1-RING-BOTTOM-LEFT <-> A-F1-RING-BOTTOM-MID
A-F1-RING-BOTTOM-MID <-> A-F1-RING-BOTTOM-RIGHT
```

---

## 4.2. Center cross / ngã tư giữa

Ở giữa tầng 1 có một ngã tư có thể di chuyển được.

Node trung tâm:

```txt
A-F1-CENTER-CROSS
```

Kết nối từ ngã tư ra 4 hướng:

```txt
A-F1-CENTER-CROSS <-> A-F1-RING-TOP-MID
A-F1-CENTER-CROSS <-> A-F1-RING-BOTTOM-MID
A-F1-CENTER-CROSS <-> A-F1-RING-LEFT-MID
A-F1-CENTER-CROSS <-> A-F1-RING-RIGHT-MID
```

---

# 5. Tầng 1 — Phòng quanh vòng ngoài

## 5.1. Phía trên có 5 phòng

Các phòng phía trên:

```txt
A-F1-TOP-ROOM-01
A-F1-TOP-ROOM-02
A-F1-TOP-ROOM-03
A-F1-TOP-ROOM-04
A-F1-TOP-ROOM-05
```

Access node tương ứng:

```txt
A-F1-TOP-ROOM-01-ACCESS
A-F1-TOP-ROOM-02-ACCESS
A-F1-TOP-ROOM-03-ACCESS
A-F1-TOP-ROOM-04-ACCESS
A-F1-TOP-ROOM-05-ACCESS
```

Kết nối:

```txt
A-F1-RING-TOP-LEFT <-> A-F1-TOP-ROOM-01-ACCESS <-> A-F1-TOP-ROOM-01
A-F1-RING-TOP-MID <-> A-F1-TOP-ROOM-02-ACCESS <-> A-F1-TOP-ROOM-02
A-F1-RING-TOP-MID <-> A-F1-TOP-ROOM-03-ACCESS <-> A-F1-TOP-ROOM-03
A-F1-RING-TOP-RIGHT <-> A-F1-TOP-ROOM-04-ACCESS <-> A-F1-TOP-ROOM-04
A-F1-RING-TOP-RIGHT <-> A-F1-TOP-ROOM-05-ACCESS <-> A-F1-TOP-ROOM-05
```

---

## 5.2. Phía dưới có 5 phòng

```txt
A-F1-BOTTOM-ROOM-01
A-F1-BOTTOM-ROOM-02
A-F1-BOTTOM-ROOM-03
A-F1-BOTTOM-ROOM-04
A-F1-BOTTOM-ROOM-05
```

Access node:

```txt
A-F1-BOTTOM-ROOM-01-ACCESS
A-F1-BOTTOM-ROOM-02-ACCESS
A-F1-BOTTOM-ROOM-03-ACCESS
A-F1-BOTTOM-ROOM-04-ACCESS
A-F1-BOTTOM-ROOM-05-ACCESS
```

Kết nối:

```txt
A-F1-RING-BOTTOM-LEFT <-> A-F1-BOTTOM-ROOM-01-ACCESS <-> A-F1-BOTTOM-ROOM-01
A-F1-RING-BOTTOM-MID <-> A-F1-BOTTOM-ROOM-02-ACCESS <-> A-F1-BOTTOM-ROOM-02
A-F1-RING-BOTTOM-MID <-> A-F1-BOTTOM-ROOM-03-ACCESS <-> A-F1-BOTTOM-ROOM-03
A-F1-RING-BOTTOM-RIGHT <-> A-F1-BOTTOM-ROOM-04-ACCESS <-> A-F1-BOTTOM-ROOM-04
A-F1-RING-BOTTOM-RIGHT <-> A-F1-BOTTOM-ROOM-05-ACCESS <-> A-F1-BOTTOM-ROOM-05
```

---

## 5.3. Bên trái có 2 phòng

```txt
A-F1-LEFT-ROOM-01
A-F1-LEFT-ROOM-02
```

Access node:

```txt
A-F1-LEFT-ROOM-01-ACCESS
A-F1-LEFT-ROOM-02-ACCESS
```

Kết nối:

```txt
A-F1-RING-LEFT-MID <-> A-F1-LEFT-ROOM-01-ACCESS <-> A-F1-LEFT-ROOM-01
A-F1-RING-LEFT-MID <-> A-F1-LEFT-ROOM-02-ACCESS <-> A-F1-LEFT-ROOM-02
```

---

## 5.4. Bên phải có 2 phòng

```txt
A-F1-RIGHT-ROOM-01
A-F1-RIGHT-ROOM-02
```

Access node:

```txt
A-F1-RIGHT-ROOM-01-ACCESS
A-F1-RIGHT-ROOM-02-ACCESS
```

Kết nối:

```txt
A-F1-RING-RIGHT-MID <-> A-F1-RIGHT-ROOM-01-ACCESS <-> A-F1-RIGHT-ROOM-01
A-F1-RING-RIGHT-MID <-> A-F1-RIGHT-ROOM-02-ACCESS <-> A-F1-RIGHT-ROOM-02
```

---

# 6. Tầng 1 — Phòng do khối bên trong tạo ra

Do có các khối phòng bên trong, các góc có thêm phòng.

## 6.1. Góc trên phải có 3 phòng

```txt
A-F1-INNER-TOP-RIGHT-ROOM-01
A-F1-INNER-TOP-RIGHT-ROOM-02
A-F1-INNER-TOP-RIGHT-ROOM-03
```

Access:

```txt
A-F1-INNER-TOP-RIGHT-ROOM-01-ACCESS
A-F1-INNER-TOP-RIGHT-ROOM-02-ACCESS
A-F1-INNER-TOP-RIGHT-ROOM-03-ACCESS
```

Các access này nên nối vào đoạn:

```txt
A-F1-CENTER-CROSS
A-F1-RING-TOP-MID
A-F1-RING-RIGHT-MID
```

---

## 6.2. Góc dưới phải có 3 phòng

```txt
A-F1-INNER-BOTTOM-RIGHT-ROOM-01
A-F1-INNER-BOTTOM-RIGHT-ROOM-02
A-F1-INNER-BOTTOM-RIGHT-ROOM-03
```

Các access này nên nối vào đoạn:

```txt
A-F1-CENTER-CROSS
A-F1-RING-BOTTOM-MID
A-F1-RING-RIGHT-MID
```

---

## 6.3. Góc trên trái có 2 phòng

```txt
A-F1-INNER-TOP-LEFT-ROOM-01
A-F1-INNER-TOP-LEFT-ROOM-02
```

Các access này nên nối vào đoạn:

```txt
A-F1-CENTER-CROSS
A-F1-RING-TOP-MID
A-F1-RING-LEFT-MID
```

---

## 6.4. Góc dưới trái có 2 phòng

```txt
A-F1-INNER-BOTTOM-LEFT-ROOM-01
A-F1-INNER-BOTTOM-LEFT-ROOM-02
```

Các access này nên nối vào đoạn:

```txt
A-F1-CENTER-CROSS
A-F1-RING-BOTTOM-MID
A-F1-RING-LEFT-MID
```

---

# 7. Tầng 1 — Phòng dọc đường ngang/dọc ở giữa

## 7.1. Đường ngang khúc trái có 2 phòng mỗi bên

Đoạn này là nhánh từ:

```txt
A-F1-RING-LEFT-MID <-> A-F1-CENTER-CROSS
```

Phòng phía trên đoạn ngang trái:

```txt
A-F1-MID-LEFT-UPPER-ROOM-01
A-F1-MID-LEFT-UPPER-ROOM-02
```

Phòng phía dưới đoạn ngang trái:

```txt
A-F1-MID-LEFT-LOWER-ROOM-01
A-F1-MID-LEFT-LOWER-ROOM-02
```

Mỗi phòng cần có access node tương ứng.

---

## 7.2. Đường dọc phía trên có 2 phòng bên phải

Đoạn này là nhánh từ:

```txt
A-F1-CENTER-CROSS <-> A-F1-RING-TOP-MID
```

Phòng:

```txt
A-F1-MID-TOP-RIGHT-ROOM-01
A-F1-MID-TOP-RIGHT-ROOM-02
```

Mỗi phòng cần có access node.

---

## 7.3. Đường dọc phía dưới có 2 phòng bên phải

Đoạn này là nhánh từ:

```txt
A-F1-CENTER-CROSS <-> A-F1-RING-BOTTOM-MID
```

Phòng:

```txt
A-F1-MID-BOTTOM-RIGHT-ROOM-01
A-F1-MID-BOTTOM-RIGHT-ROOM-02
```

Mỗi phòng cần có access node.

---

# 8. Thư viện tầng 1

Thư viện nằm bên trái/dưới và nối vào tòa A.

Node:

```txt
A-F1-LIBRARY-CENTER
A-F1-LIBRARY-ENTRANCE
A-F1-LIBRARY-CONNECTOR
```

Kết nối:

```txt
A-F1-LIBRARY-CENTER <-> A-F1-LIBRARY-ENTRANCE
A-F1-LIBRARY-ENTRANCE <-> A-F1-LIBRARY-CONNECTOR
A-F1-LIBRARY-CONNECTOR <-> A-F1-RING-LEFT-MID
```

---

# 9. Cầu thang tầng 1

Các cầu thang chính:

```txt
A-F1-STAIR-LEFT
A-F1-STAIR-RIGHT
A-F1-STAIR-BOTTOM
A-F1-STAIR-TOP
```

Kết nối gợi ý:

```txt
A-F1-STAIR-LEFT <-> A-F1-RING-LEFT-MID
A-F1-STAIR-RIGHT <-> A-F1-RING-RIGHT-MID
A-F1-STAIR-BOTTOM <-> A-F1-RING-BOTTOM-MID
A-F1-STAIR-TOP <-> A-F1-RING-TOP-MID
```

---

# 10. Tầng 2 — Cấu trúc cập nhật

Tầng 2 đơn giản hơn tầng 1.

Mỗi hướng có 2 phòng:

```txt
TOP:    2 phòng
BOTTOM: 2 phòng
LEFT:   2 phòng
RIGHT:  2 phòng
```

Tầng 2 cũng nối với thư viện ở vị trí tương tự tầng 1 vì thư viện có 2 tầng.

---

## 10.1. Trục đi bộ tầng 2

Dùng một ring đơn giản:

```txt
A-F2-RING-TOP
A-F2-RING-RIGHT
A-F2-RING-BOTTOM
A-F2-RING-LEFT
A-F2-CENTER-CROSS
```

Edge:

```txt
A-F2-RING-TOP <-> A-F2-RING-RIGHT
A-F2-RING-RIGHT <-> A-F2-RING-BOTTOM
A-F2-RING-BOTTOM <-> A-F2-RING-LEFT
A-F2-RING-LEFT <-> A-F2-RING-TOP

A-F2-CENTER-CROSS <-> A-F2-RING-TOP
A-F2-CENTER-CROSS <-> A-F2-RING-RIGHT
A-F2-CENTER-CROSS <-> A-F2-RING-BOTTOM
A-F2-CENTER-CROSS <-> A-F2-RING-LEFT
```

---

## 10.2. Phòng tầng 2

Phía trên:

```txt
A-F2-TOP-ROOM-01
A-F2-TOP-ROOM-02
```

Phía dưới:

```txt
A-F2-BOTTOM-ROOM-01
A-F2-BOTTOM-ROOM-02
```

Bên trái:

```txt
A-F2-LEFT-ROOM-01
A-F2-LEFT-ROOM-02
```

Bên phải:

```txt
A-F2-RIGHT-ROOM-01
A-F2-RIGHT-ROOM-02
```

Mỗi phòng có access node:

```txt
A-F2-TOP-ROOM-01-ACCESS
...
```

Kết nối:

```txt
A-F2-RING-TOP <-> A-F2-TOP-ROOM-01-ACCESS <-> A-F2-TOP-ROOM-01
A-F2-RING-TOP <-> A-F2-TOP-ROOM-02-ACCESS <-> A-F2-TOP-ROOM-02

A-F2-RING-BOTTOM <-> A-F2-BOTTOM-ROOM-01-ACCESS <-> A-F2-BOTTOM-ROOM-01
A-F2-RING-BOTTOM <-> A-F2-BOTTOM-ROOM-02-ACCESS <-> A-F2-BOTTOM-ROOM-02

A-F2-RING-LEFT <-> A-F2-LEFT-ROOM-01-ACCESS <-> A-F2-LEFT-ROOM-01
A-F2-RING-LEFT <-> A-F2-LEFT-ROOM-02-ACCESS <-> A-F2-LEFT-ROOM-02

A-F2-RING-RIGHT <-> A-F2-RIGHT-ROOM-01-ACCESS <-> A-F2-RIGHT-ROOM-01
A-F2-RING-RIGHT <-> A-F2-RIGHT-ROOM-02-ACCESS <-> A-F2-RIGHT-ROOM-02
```

---

## 10.3. Thư viện tầng 2

Vì thư viện có 2 tầng, cần thêm thư viện tầng 2:

```txt
A-F2-LIBRARY-CENTER
A-F2-LIBRARY-ENTRANCE
A-F2-LIBRARY-CONNECTOR
```

Kết nối:

```txt
A-F2-LIBRARY-CENTER <-> A-F2-LIBRARY-ENTRANCE
A-F2-LIBRARY-ENTRANCE <-> A-F2-LIBRARY-CONNECTOR
A-F2-LIBRARY-CONNECTOR <-> A-F2-RING-LEFT
```

---

# 11. Kết nối giữa tầng 1 và tầng 2

Cầu thang:

```txt
A-F1-STAIR-LEFT <-> A-F2-STAIR-LEFT
A-F1-STAIR-RIGHT <-> A-F2-STAIR-RIGHT
A-F1-STAIR-BOTTOM <-> A-F2-STAIR-BOTTOM
A-F1-STAIR-TOP <-> A-F2-STAIR-TOP
```

Thư viện 2 tầng:

```txt
A-F1-LIBRARY-CENTER <-> A-F2-LIBRARY-CENTER
```

Nếu muốn chi tiết hơn:

```txt
A-F1-LIBRARY-STAIR <-> A-F2-LIBRARY-STAIR
```

---

# 12. Ghi chú kiểm chứng

Sau khi vẽ graph, cần kiểm tra:

1. Đường đi chính tầng 1 có tạo thành hình vuông/ring không?
2. Có ngã tư giữa không?
3. Mỗi phòng có access node riêng chưa?
4. Phía trên tầng 1 có 5 phòng chưa?
5. Phía dưới tầng 1 có 5 phòng chưa?
6. Bên trái tầng 1 có 2 phòng chưa?
7. Bên phải tầng 1 có 2 phòng chưa?
8. Góc trên phải và dưới phải có 3 phòng chưa?
9. Góc trên trái và dưới trái có 2 phòng chưa?
10. Đường ngang trái ở giữa có 2 phòng mỗi bên chưa?
11. Đường dọc trên/dưới có 2 phòng bên phải chưa?
12. Tầng 2 mỗi hướng có 2 phòng chưa?
13. Tầng 2 có nối thư viện chưa?
14. Đường đi của sinh viên có đi qua access node trước khi vào phòng không?
