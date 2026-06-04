# 05_BUILDING_B_C_D_E_STRUCTURE.md

# Cấu trúc Graph cho Tòa B, C, D, E UIT

## 1. Mục tiêu

File này mô tả cách dựng graph cho các tòa còn lại sau khi đã dựng Tòa A.

Các tòa B, C, D, E đơn giản hơn Tòa A. Không cần dựng quá chi tiết như Tòa A, chỉ cần đủ để:

1. Biểu diễn phòng học.
2. Biểu diễn hành lang chính.
3. Biểu diễn cầu thang/thang máy.
4. Cho phép tìm đường trong tòa.
5. Cho phép nối với campus graph.
6. Cho phép mô phỏng sinh viên đi từ phòng này sang phòng khác.

---

# 2. Quy ước chung cho Building Graph

## 2.1. Node types

```txt
room
access
corridor
junction
stair
elevator
wc
storage
entrance
building_anchor
```

Ý nghĩa:

| Type              | Ý nghĩa                           |
| ----------------- | --------------------------------- |
| `room`            | Phòng học/phòng làm việc          |
| `access`          | Điểm trước cửa phòng              |
| `corridor`        | Điểm trên hành lang               |
| `junction`        | Điểm rẽ hoặc node nối nhiều hướng |
| `stair`           | Cầu thang                         |
| `elevator`        | Thang máy                         |
| `wc`              | Nhà vệ sinh                       |
| `storage`         | Kho                               |
| `entrance`        | Lối vào tòa                       |
| `building_anchor` | Node đại diện tổng quát của tòa   |

---

## 2.2. Edge types

```txt
corridor
door
stair
elevator
building_entry
```

---

## 2.3. Nguyên tắc nối phòng

Không nối phòng trực tiếp vào hành lang chính nếu muốn visualize rõ.

Dùng:

```txt
corridor node → access node → room node
```

Ví dụ:

```txt
B-F1-CORRIDOR-04
    ↓
B1.14-ACCESS
    ↓
B1.14
```

---

## 2.4. Vertical connectors

Các tầng được nối bằng:

```txt
STAIR-LEFT
STAIR-MID
STAIR-RIGHT
ELEVATOR
```

Ví dụ:

```txt
B-F1-STAIR-LEFT <-> B-F2-STAIR-LEFT
B-F2-STAIR-LEFT <-> B-F3-STAIR-LEFT
...
```

---

# 3. Tòa B — Staircase-shaped room distribution

## 3.1. Đặc điểm chính

Tòa B có cấu trúc hành lang dài, nhưng số lượng phòng giảm dần khi lên cao.

Đây không phải là lỗi dữ liệu.
Tòa B có hình dạng kiểu “cầu thang”: càng lên cao, phần mặt bằng khả dụng càng ngắn lại, làm số phòng giảm từ phải sang trái.

Vì vậy khi visualize, không nên ép mọi tầng có cùng chiều dài.
Mỗi tầng nên có `corridor length` khác nhau.

---

## 3.2. Tư duy mô hình hóa Tòa B

Mỗi tầng B là một hành lang ngang:

```txt
B-Fx-STAIR-LEFT/ELEVATOR
        |
B-Fx-CORRIDOR-01 -- B-Fx-CORRIDOR-02 -- ... -- B-Fx-CORRIDOR-N
        |
B-Fx-STAIR-RIGHT / STAIR-MID / WC / ROOM ACCESS
```

Phòng được treo vào các corridor node:

```txt
B-Fx-CORRIDOR-i <-> Bx.yy-ACCESS <-> Bx.yy
```

---

## 3.3. Tầng 1 và tầng 2

Tầng 1 và tầng 2 có số phòng nhiều nhất.

Phòng tầng 1:

```txt
B1.22
B1.20
B1.18
B1.16
B1.14
B1.12
B1.10
B1.08
B1.06
B1.04
B1.02
B1.01
```

Phòng tầng 2:

```txt
B2.22
B2.20
B2.18
B2.16
B2.14
B2.12
B2.10
B2.08
B2.06
B2.04
B2.02
B2.01
```

Graph pattern:

```txt
B-F1-CORRIDOR-01 -- B-F1-CORRIDOR-02 -- ... -- B-F1-CORRIDOR-11
B-F2-CORRIDOR-01 -- B-F2-CORRIDOR-02 -- ... -- B-F2-CORRIDOR-11
```

Mỗi phòng tạo access node tương ứng.

---

## 3.4. Tầng 3 và tầng 4

Tầng 3:

```txt
B3.22
B3.20
B3.18
B3.16
B3.14
B3.12
B3.10
B3.08
B3.06
B3.04
B3.02
B3.01
```

Tầng 4:

```txt
B4.22
B4.20
B4.18
B4.16
B4.14
B4.12
B4.10
B4.08
B4.06
B4.04
B4.02
B4.01
```

Tầng 3 và 4 vẫn có hành lang dài tương tự tầng 1–2.

---

## 3.5. Tầng 5

Tầng 5 ngắn hơn:

```txt
B5.14
B5.12
B5.10
B5.08
B5.06
B5.04
B5.02
B5.01
```

Graph pattern:

```txt
B-F5-CORRIDOR-01 -- ... -- B-F5-CORRIDOR-07
```

---

## 3.6. Tầng 6

Tầng 6:

```txt
B6.12
B6.10
B6.08
B6.06
B6.04
B6.02
B6.01
```

Graph pattern:

```txt
B-F6-CORRIDOR-01 -- ... -- B-F6-CORRIDOR-06
```

---

## 3.7. Tầng 7

Tầng 7:

```txt
B7.08
B7.06
B7.04
B7.02
B7.01
```

Graph pattern:

```txt
B-F7-CORRIDOR-01 -- ... -- B-F7-CORRIDOR-04
```

---

## 3.8. Tầng 8

Tầng 8:

```txt
B8.08
B8.06
B8.04
B8.02
```

Graph pattern:

```txt
B-F8-CORRIDOR-01 -- ... -- B-F8-CORRIDOR-04
```

---

## 3.9. Tầng 9

Tầng 9 nhỏ nhất:

```txt
B9.04
B9.02
```

Graph pattern:

```txt
B-F9-CORRIDOR-01 -- B-F9-CORRIDOR-02
```

---

## 3.10. Stairs/elevators của Tòa B

Vì sơ đồ có nhiều cụm `Thang máy/bộ`, ta nên dùng 3 trục vertical chính:

```txt
B-CORE-LEFT
B-CORE-MID
B-CORE-RIGHT
```

Với mỗi tầng:

```txt
B-Fx-CORE-LEFT
B-Fx-CORE-MID
B-Fx-CORE-RIGHT
```

Nếu tầng cao không còn core phải do mặt bằng ngắn lại, có thể không tạo node đó hoặc tạo nhưng `accessible = false`.

Vertical edges:

```txt
B-F1-CORE-LEFT <-> B-F2-CORE-LEFT
B-F2-CORE-LEFT <-> B-F3-CORE-LEFT
...
B-F8-CORE-LEFT <-> B-F9-CORE-LEFT
```

Tương tự cho mid/right nếu tồn tại.

---

## 3.11. B building entrance

Node entrance:

```txt
B-F1-BUILDING-ENTRANCE
```

Kết nối vào hành lang tầng 1:

```txt
B-F1-BUILDING-ENTRANCE <-> B-F1-CORRIDOR-01
```

Campus edge:

```txt
UIT-OUTDOOR-B-FRONT <-> B-F1-BUILDING-ENTRANCE
```

---

# 4. Tòa C — Straight corridor building

## 4.1. Đặc điểm chính

Tòa C có 3 tầng.
Mỗi tầng là một hành lang dài, phòng nằm hai bên.
Có nhiều cầu thang ở trái, giữa và phải.

---

## 4.2. Tầng 1

Phòng tầng 1:

```txt
C113
C111
C109
C107
C105
C103
C101

C110
C108
C106
C104
C102
```

Các node phụ:

```txt
C-F1-STAIR-LEFT
C-F1-STAIR-MID
C-F1-STAIR-RIGHT
C-F1-WC-LEFT
C-F1-WC-RIGHT
C-F1-STORAGE
C-F1-WATER-TANK
```

Graph pattern:

```txt
C-F1-CORRIDOR-01 -- C-F1-CORRIDOR-02 -- ... -- C-F1-CORRIDOR-08
```

Phòng nối theo pattern:

```txt
C-F1-CORRIDOR-i <-> Cxxx-ACCESS <-> Cxxx
```

---

## 4.3. Tầng 2

Phòng tầng 2:

```txt
C213
C211
C209
C207
C205
C203
C201

C218
C216
C214
C212
C210
C208
C206
C204
C202
```

Các node phụ:

```txt
C-F2-STAIR-LEFT
C-F2-STAIR-MID
C-F2-STAIR-RIGHT
C-F2-WC-LEFT
C-F2-WC-RIGHT
C-F2-STORAGE
```

---

## 4.4. Tầng 3

Phòng tầng 3:

```txt
C315
C313
C311
C309
C307
C305
C303
C301

C318
C316
C314
C312
C310
C308
C306
C304
C302
```

Các node phụ:

```txt
C-F3-STAIR-LEFT
C-F3-STAIR-MID
C-F3-STAIR-RIGHT
C-F3-WC-LEFT
C-F3-WC-RIGHT
C-F3-STORAGE
```

---

## 4.5. Vertical connectors Tòa C

```txt
C-F1-STAIR-LEFT <-> C-F2-STAIR-LEFT
C-F2-STAIR-LEFT <-> C-F3-STAIR-LEFT

C-F1-STAIR-MID <-> C-F2-STAIR-MID
C-F2-STAIR-MID <-> C-F3-STAIR-MID

C-F1-STAIR-RIGHT <-> C-F2-STAIR-RIGHT
C-F2-STAIR-RIGHT <-> C-F3-STAIR-RIGHT
```

---

## 4.6. C building entrance

```txt
C-F1-BUILDING-ENTRANCE
C-F1-BUILDING-ENTRANCE <-> C-F1-CORRIDOR-01
UIT-OUTDOOR-C-FRONT <-> C-F1-BUILDING-ENTRANCE
```

---

# 5. Tòa D — Small four-room building

## 5.1. Đặc điểm chính

Tòa D nhỏ và không có sơ đồ phòng chi tiết trong file PDF.

Theo mô tả, Tòa D có 4 phòng chia thành 4 phần gần bằng nhau.

Vì vậy chỉ cần mô hình hóa đơn giản.

---

## 5.2. Node structure

```txt
D-F1-BUILDING-ENTRANCE
D-F1-CENTER
D-F1-ROOM-01-ACCESS
D-F1-ROOM-01
D-F1-ROOM-02-ACCESS
D-F1-ROOM-02
D-F1-ROOM-03-ACCESS
D-F1-ROOM-03
D-F1-ROOM-04-ACCESS
D-F1-ROOM-04
```

---

## 5.3. Topology

```txt
               D-F1-ROOM-01
                    |
            D-F1-ROOM-01-ACCESS
                    |
D-F1-ROOM-02 -- D-F1-CENTER -- D-F1-ROOM-03
                    |
            D-F1-ROOM-04-ACCESS
                    |
               D-F1-ROOM-04
```

Thực tế nên lưu edge như:

```txt
D-F1-BUILDING-ENTRANCE <-> D-F1-CENTER

D-F1-CENTER <-> D-F1-ROOM-01-ACCESS <-> D-F1-ROOM-01
D-F1-CENTER <-> D-F1-ROOM-02-ACCESS <-> D-F1-ROOM-02
D-F1-CENTER <-> D-F1-ROOM-03-ACCESS <-> D-F1-ROOM-03
D-F1-CENTER <-> D-F1-ROOM-04-ACCESS <-> D-F1-ROOM-04
```

Campus edge:

```txt
UIT-OUTDOOR-D-FRONT <-> D-F1-BUILDING-ENTRANCE
```

---

# 6. Tòa E — Repeated vertical building

## 6.1. Đặc điểm chính

Tòa E là tòa nhiều tầng.
Mặt bằng mỗi tầng khá đơn giản, gồm:

```txt
main corridor
WC
elevator
stair
storage
rooms
```

Các tầng 2, 3, 4 trong sơ đồ có layout lặp tương đối giống nhau.

---

## 6.2. Tầng G

Tầng G:

```txt
Bàn bảo vệ
Bãi để xe ô tô
```

Node đề xuất:

```txt
E-FG-BUILDING-ENTRANCE
E-FG-SECURITY-DESK
E-FG-PARKING
E-FG-ELEVATOR
E-FG-STAIR
E-FG-CORRIDOR
```

---

## 6.3. Tầng 1

Danh sách chức năng tầng 1:

```txt
Bàn bảo vệ
Sảnh tiếp đón
E1.1
E1.2
E1.3
E1.4
E1.5
E1.7
```

Diễn giải:

```txt
E1.1: Phòng họp
E1.2: Phòng Không gian Tiếng Anh
E1.3: Phòng điện tòa nhà
E1.4: Trung tâm Ngoại ngữ
E1.5: Phòng hệ thống máy lạnh
E1.7: Phòng nghỉ Trung tâm Ngoại ngữ
```

Node:

```txt
E-F1-BUILDING-ENTRANCE
E-F1-LOBBY
E-F1-SECURITY-DESK
E-F1-ELEVATOR
E-F1-STAIR
E-F1-CORRIDOR
E1.1
E1.2
E1.3
E1.4
E1.5
E1.7
```

---

## 6.4. Tầng 2

```txt
E2.1: Văn phòng Các chương trình Đặc biệt
E2.2: Phòng tự học
E2.3: Phòng học
E2.4: Phòng học
E2.5: Ban Quản lý Cơ sở
```

---

## 6.5. Tầng 3

```txt
E3.1: Phòng Thực hành Khoa MMT&TT
E3.2: Phòng học
E3.3: Phòng học
E3.4: Phòng học
E3.5: Phòng Giảng viên Tiếng Nhật
```

---

## 6.6. Tầng 4

```txt
E4.1
E4.2
E4.3
E4.4
E4.5
```

Trong đó:

```txt
E4.1-E4.4: Phòng học
E4.5: Phòng Giảng viên Tiếng Nhật
```

---

## 6.7. Tầng 5 đến tầng 10

Các tầng này có thể mô hình hóa đơn giản bằng một node chức năng chính trên mỗi tầng:

```txt
E5.1: Phòng Thí nghiệm Truyền thông Đa phương tiện
E6.1: Phòng Thí nghiệm Vi mạch Tích hợp Chuyên dụng
E7.1: Phòng Ăn - Phòng nghỉ Giảng viên - Viên chức & Người lao động
E8.1: Phòng Thí nghiệm An toàn Thông tin / Trung tâm An ninh mạng
E9.1: Phòng Thí nghiệm Hệ thống Thông tin
E10.1: Phòng học
```

Ngoài ra có thể thêm department nodes:

```txt
E-F5-KHOA-KHMT
E-F6-KHOA-KTMT
E-F7-KHOA-CNPM
E-F8-KHOA-MMTT
E-F9-KHOA-HTTT
E-F10-KHOA-KHKT-TT
```

Nếu chỉ cần routing, các department nodes có thể bỏ qua.

---

## 6.8. Tầng 11 và tầng 12

Tầng 11:

```txt
E11.1: Công ty Rosen
E11.2
E11.3: Trung tâm An ninh mạng
E11.4
E11.6
E11.8
```

Tầng 12:

```txt
E12.1: Phòng Sinh hoạt chung
E12.2: Hội trường E
```

---

## 6.9. Generic floor pattern cho Tòa E

Với mỗi tầng `f`, tạo:

```txt
E-F{f}-CORRIDOR
E-F{f}-ELEVATOR
E-F{f}-STAIR
E-F{f}-WC
```

Và các phòng:

```txt
E{f}.1
E{f}.2
...
```

Pattern:

```txt
E-F{f}-ELEVATOR <-> E-F{f}-CORRIDOR
E-F{f}-STAIR <-> E-F{f}-CORRIDOR
E-F{f}-WC <-> E-F{f}-CORRIDOR
E-F{f}-CORRIDOR <-> E{f}.x-ACCESS <-> E{f}.x
```

Vertical connectors:

```txt
E-F1-ELEVATOR <-> E-F2-ELEVATOR <-> ... <-> E-F12-ELEVATOR
E-F1-STAIR <-> E-F2-STAIR <-> ... <-> E-F12-STAIR
```

---

## 6.10. E building entrance

```txt
E-F1-BUILDING-ENTRANCE
E-F1-BUILDING-ENTRANCE <-> E-F1-LOBBY
E-F1-LOBBY <-> E-F1-CORRIDOR
UIT-OUTDOOR-E-FRONT <-> E-F1-BUILDING-ENTRANCE
```

---

# 7. Validation checklist

## 7.1. Tòa B

Graph Tòa B đúng nếu:

1. Tầng 1–4 dài nhất.
2. Tầng 5 ngắn hơn.
3. Tầng 6 ngắn hơn tầng 5.
4. Tầng 7–8 ngắn hơn nữa.
5. Tầng 9 chỉ có 2 phòng.
6. Hình visualize tạo cảm giác “cầu thang” giảm dần từ phải sang trái.
7. Các core cầu thang/thang máy nối được giữa tầng.
8. Có thể đi từ B1.22 đến B9.02.

---

## 7.2. Tòa C

Graph Tòa C đúng nếu:

1. Có 3 tầng.
2. Mỗi tầng có hành lang ngang.
3. Phòng nằm hai bên hành lang.
4. Có cầu thang trái, giữa, phải.
5. Có thể đi từ C102 đến C315.

---

## 7.3. Tòa D

Graph Tòa D đúng nếu:

1. Có 4 phòng.
2. Có một center node.
3. Mỗi phòng nối qua access node.
4. Có entrance nối ra campus graph.

---

## 7.4. Tòa E

Graph Tòa E đúng nếu:

1. Có tầng G hoặc tầng 1 làm entrance.
2. Có các tầng 1–12.
3. Có elevator/stair vertical connectors.
4. Mỗi tầng có corridor node.
5. Các phòng E1.x, E2.x, E3.x, E4.x, E11.x, E12.x được tạo rõ.
6. Có thể đi từ E1.1 đến E12.2.
