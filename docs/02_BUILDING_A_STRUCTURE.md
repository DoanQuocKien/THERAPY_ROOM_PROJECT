# 02_BUILDING_A_STRUCTURE.md

# Cấu trúc Graph cho Tòa A UIT

## 1. Quy ước chung

Tòa A được mô hình hóa bằng graph.

Mỗi node có tọa độ trong hệ chuẩn hóa:

```txt
x từ 0 đến 1000
y từ 0 đến 1000
```

Quy ước:

```txt
Góc trên bên trái ảnh:  (0, 0)
Góc dưới bên phải ảnh: (1000, 1000)
```

Không cần tọa độ chính xác tuyệt đối ở phiên bản đầu.
Chỉ cần đủ gần để nhìn thấy graph đúng hình dạng tổng quát.

---

## 2. Loại node

Chỉ dùng các loại node đơn giản sau:

```txt
room
corridor
junction
stair
entrance
library
storage
```

Ý nghĩa:

| Type       | Ý nghĩa                                    |
| ---------- | ------------------------------------------ |
| `room`     | Phòng làm việc, phòng chức năng, phòng học |
| `corridor` | Một điểm nằm trên hành lang                |
| `junction` | Giao điểm hoặc điểm rẽ của hành lang       |
| `stair`    | Cầu thang                                  |
| `entrance` | Lối vào/lối ra                             |
| `library`  | Khu vực Thư viện UIT                       |
| `storage`  | Kho hoặc khu không ưu tiên đi qua          |

---

## 3. Loại edge

Chỉ dùng các loại edge sau:

```txt
corridor
door
stair
connector
```

Ý nghĩa:

| Type        | Ý nghĩa                                          |
| ----------- | ------------------------------------------------ |
| `corridor`  | Lối đi bình thường trong hành lang               |
| `door`      | Cửa nối phòng với hành lang                      |
| `stair`     | Kết nối giữa hai tầng                            |
| `connector` | Lối nối đặc biệt, ví dụ thư viện sang khối chính |

---

## 4. Nguyên tắc nối graph

Không nối phòng trực tiếp với phòng.

Dùng cấu trúc:

```txt
phòng → cửa/phòng gần hành lang → hành lang → giao điểm → hành lang khác → phòng đích
```

Ví dụ:

```txt
A-F1-ROOM-WEST-01
        ↓
A-F1-DOOR-WEST-01
        ↓
A-F1-WEST-JUNCTION
        ↓
A-F1-CENTER-01
```

Nếu chưa muốn tạo door node riêng, có thể cho phòng nối trực tiếp với junction gần nhất trong phiên bản đơn giản. Tuy nhiên nên giữ tư duy rằng kết nối đó là một cạnh loại `door`.

---

# 5. Tòa A — Tầng 1

## 5.1. Đặc điểm tầng 1

Tầng 1 có các vùng lớn:

```txt
A-F1-LIBRARY
A-F1-LIBRARY-CONNECTOR
A-F1-WEST-WING
A-F1-NORTH-WING
A-F1-CENTER
A-F1-EAST-WING
A-F1-SOUTH-WING
```

Tầng 1 đặc biệt vì có khu **Thư viện UIT** nối với khối chính của Tòa A.

---

## 5.2. Zone: Library

ID zone:

```txt
A-F1-LIBRARY
```

Mô tả:

* Nằm bên trái/dưới sơ đồ tầng 1.
* Là một không gian lớn.
* Có nhãn “Thư viện UIT”.
* Nên được xem là một vùng riêng, không chỉ là một phòng nhỏ.

Node nên có:

```txt
A-F1-LIBRARY-CENTER
A-F1-LIBRARY-ENTRANCE
```

Ý nghĩa:

| Node                    | Ý nghĩa                                     |
| ----------------------- | ------------------------------------------- |
| `A-F1-LIBRARY-CENTER`   | Điểm trung tâm đại diện cho khu thư viện    |
| `A-F1-LIBRARY-ENTRANCE` | Điểm ra/vào thư viện để nối sang khối chính |

Edge nên có:

```txt
A-F1-LIBRARY-CENTER <-> A-F1-LIBRARY-ENTRANCE
```

---

## 5.3. Zone: Library Connector

ID zone:

```txt
A-F1-LIBRARY-CONNECTOR
```

Mô tả:

* Lối nối từ Thư viện UIT sang khối chính Tòa A.
* Đây là điểm quan trọng vì nhiều đường đi từ thư viện sang tòa chính sẽ đi qua đây.

Node nên có:

```txt
A-F1-LIBRARY-CONNECTOR-01
A-F1-LIBRARY-CONNECTOR-02
A-F1-WEST-JUNCTION
```

Edge nên có:

```txt
A-F1-LIBRARY-ENTRANCE <-> A-F1-LIBRARY-CONNECTOR-01
A-F1-LIBRARY-CONNECTOR-01 <-> A-F1-LIBRARY-CONNECTOR-02
A-F1-LIBRARY-CONNECTOR-02 <-> A-F1-WEST-JUNCTION
```

---

## 5.4. Zone: West Wing

ID zone:

```txt
A-F1-WEST-WING
```

Mô tả:

* Cánh phía trái của khối chính.
* Nhận luồng đi từ thư viện sang.
* Có thể có cầu thang/thang máy/phòng nhỏ.

Node chính:

```txt
A-F1-WEST-JUNCTION
A-F1-WEST-STAIR
A-F1-WEST-ROOM-01
A-F1-WEST-ROOM-02
```

Edge chính:

```txt
A-F1-WEST-JUNCTION <-> A-F1-CENTER-01
A-F1-WEST-JUNCTION <-> A-F1-WEST-STAIR
A-F1-WEST-JUNCTION <-> A-F1-WEST-ROOM-01
A-F1-WEST-JUNCTION <-> A-F1-WEST-ROOM-02
```

---

## 5.5. Zone: Center

ID zone:

```txt
A-F1-CENTER
```

Mô tả:

* Lõi giao thông chính của tầng 1.
* Nối các cánh Tây, Bắc, Đông, Nam.
* Đây là vùng cần nhiều junction nhất.

Node chính:

```txt
A-F1-CENTER-01
A-F1-CENTER-02
A-F1-CENTER-03
A-F1-CENTER-04
```

Có thể xem 4 node này là 4 điểm quan trọng của lõi trung tâm.

Topology đề xuất:

```txt
A-F1-CENTER-01 <-> A-F1-CENTER-02
A-F1-CENTER-02 <-> A-F1-CENTER-03
A-F1-CENTER-03 <-> A-F1-CENTER-04
A-F1-CENTER-04 <-> A-F1-CENTER-01
```

Kết nối với các cánh:

```txt
A-F1-CENTER-01 <-> A-F1-WEST-JUNCTION
A-F1-CENTER-02 <-> A-F1-NORTH-JUNCTION
A-F1-CENTER-03 <-> A-F1-EAST-JUNCTION
A-F1-CENTER-04 <-> A-F1-SOUTH-JUNCTION
```

---

## 5.6. Zone: North Wing

ID zone:

```txt
A-F1-NORTH-WING
```

Mô tả:

* Cụm phòng phía trên của khối chính.
* Có hành lang ngang phía trên.
* Có cầu thang phía trên hoặc gần phía trên.

Node chính:

```txt
A-F1-NORTH-JUNCTION
A-F1-NORTH-STAIR
A-F1-NORTH-ROOM-01
A-F1-NORTH-ROOM-02
A-F1-NORTH-ROOM-03
```

Edge chính:

```txt
A-F1-NORTH-JUNCTION <-> A-F1-CENTER-02
A-F1-NORTH-JUNCTION <-> A-F1-NORTH-STAIR
A-F1-NORTH-JUNCTION <-> A-F1-NORTH-ROOM-01
A-F1-NORTH-JUNCTION <-> A-F1-NORTH-ROOM-02
A-F1-NORTH-JUNCTION <-> A-F1-NORTH-ROOM-03
```

---

## 5.7. Zone: East Wing

ID zone:

```txt
A-F1-EAST-WING
```

Mô tả:

* Cụm phòng phía phải của khối chính.
* Có cầu thang/thang máy phía phải.
* Là một vùng có nhiều phòng làm việc.

Node chính:

```txt
A-F1-EAST-JUNCTION
A-F1-EAST-STAIR
A-F1-EAST-ROOM-01
A-F1-EAST-ROOM-02
A-F1-EAST-ROOM-03
A-F1-EAST-ROOM-04
```

Edge chính:

```txt
A-F1-EAST-JUNCTION <-> A-F1-CENTER-03
A-F1-EAST-JUNCTION <-> A-F1-EAST-STAIR
A-F1-EAST-JUNCTION <-> A-F1-EAST-ROOM-01
A-F1-EAST-JUNCTION <-> A-F1-EAST-ROOM-02
A-F1-EAST-JUNCTION <-> A-F1-EAST-ROOM-03
A-F1-EAST-JUNCTION <-> A-F1-EAST-ROOM-04
```

---

## 5.8. Zone: South Wing

ID zone:

```txt
A-F1-SOUTH-WING
```

Mô tả:

* Cụm phòng phía dưới của khối chính.
* Gần vị trí “Bạn đang ở đây” trên sơ đồ.
* Có cầu thang phía dưới.
* Đây có thể là lối vào/điểm định hướng quan trọng.

Node chính:

```txt
A-F1-SOUTH-JUNCTION
A-F1-SOUTH-STAIR
A-F1-YOU-ARE-HERE
A-F1-SOUTH-ROOM-01
A-F1-SOUTH-ROOM-02
A-F1-SOUTH-ROOM-03
```

Edge chính:

```txt
A-F1-SOUTH-JUNCTION <-> A-F1-CENTER-04
A-F1-SOUTH-JUNCTION <-> A-F1-SOUTH-STAIR
A-F1-SOUTH-JUNCTION <-> A-F1-YOU-ARE-HERE
A-F1-SOUTH-JUNCTION <-> A-F1-SOUTH-ROOM-01
A-F1-SOUTH-JUNCTION <-> A-F1-SOUTH-ROOM-02
A-F1-SOUTH-JUNCTION <-> A-F1-SOUTH-ROOM-03
```

---

## 5.9. Topology tổng quát tầng 1

Có thể hình dung tầng 1 như sau:

```txt
                         NORTH
                          |
                    A-F1-NORTH-JUNCTION
                          |
                    A-F1-CENTER-02
                          |
WEST/LIBRARY -- A-F1-CENTER-01 -- A-F1-CENTER-03 -- EAST
                          |
                    A-F1-CENTER-04
                          |
                    A-F1-SOUTH-JUNCTION
                          |
                         SOUTH
```

Thêm đường thư viện:

```txt
A-F1-LIBRARY-CENTER
        |
A-F1-LIBRARY-ENTRANCE
        |
A-F1-LIBRARY-CONNECTOR-01
        |
A-F1-LIBRARY-CONNECTOR-02
        |
A-F1-WEST-JUNCTION
        |
A-F1-CENTER-01
```

---

# 6. Tòa A — Tầng 2

## 6.1. Đặc điểm tầng 2

Tầng 2 khác tầng 1:

* Không có khu thư viện lớn như tầng 1.
* Có vùng trung tâm dạng vòng/cung.
* Có một số khu vực ghi “Kho”.
* Nhiều phòng nằm quanh biên ngoài.
* Các cầu thang tương ứng nối xuống tầng 1.

Các zone chính:

```txt
A-F2-CENTER-RING
A-F2-WEST-WING
A-F2-NORTH-WING
A-F2-EAST-WING
A-F2-SOUTH-WING
A-F2-STORAGE
```

---

## 6.2. Zone: Center Ring

ID zone:

```txt
A-F2-CENTER-RING
```

Mô tả:

* Đây là lõi giao thông chính của tầng 2.
* Nên mô hình hóa thành một vòng graph.

Node chính:

```txt
A-F2-RING-NORTH
A-F2-RING-EAST
A-F2-RING-SOUTH
A-F2-RING-WEST
```

Edge chính:

```txt
A-F2-RING-NORTH <-> A-F2-RING-EAST
A-F2-RING-EAST <-> A-F2-RING-SOUTH
A-F2-RING-SOUTH <-> A-F2-RING-WEST
A-F2-RING-WEST <-> A-F2-RING-NORTH
```

Nếu muốn chi tiết hơn, có thể thêm:

```txt
A-F2-RING-NORTH-EAST
A-F2-RING-SOUTH-EAST
A-F2-RING-SOUTH-WEST
A-F2-RING-NORTH-WEST
```

Nhưng phiên bản đơn giản chỉ cần 4 node là đủ.

---

## 6.3. Zone: West Wing

Node chính:

```txt
A-F2-WEST-JUNCTION
A-F2-WEST-STAIR
A-F2-WEST-ROOM-01
A-F2-WEST-ROOM-02
```

Edge chính:

```txt
A-F2-WEST-JUNCTION <-> A-F2-RING-WEST
A-F2-WEST-JUNCTION <-> A-F2-WEST-STAIR
A-F2-WEST-JUNCTION <-> A-F2-WEST-ROOM-01
A-F2-WEST-JUNCTION <-> A-F2-WEST-ROOM-02
```

---

## 6.4. Zone: North Wing

Node chính:

```txt
A-F2-NORTH-JUNCTION
A-F2-NORTH-STAIR
A-F2-NORTH-ROOM-01
A-F2-NORTH-ROOM-02
A-F2-NORTH-ROOM-03
```

Edge chính:

```txt
A-F2-NORTH-JUNCTION <-> A-F2-RING-NORTH
A-F2-NORTH-JUNCTION <-> A-F2-NORTH-STAIR
A-F2-NORTH-JUNCTION <-> A-F2-NORTH-ROOM-01
A-F2-NORTH-JUNCTION <-> A-F2-NORTH-ROOM-02
A-F2-NORTH-JUNCTION <-> A-F2-NORTH-ROOM-03
```

---

## 6.5. Zone: East Wing

Node chính:

```txt
A-F2-EAST-JUNCTION
A-F2-EAST-STAIR
A-F2-EAST-ROOM-01
A-F2-EAST-ROOM-02
A-F2-EAST-ROOM-03
```

Edge chính:

```txt
A-F2-EAST-JUNCTION <-> A-F2-RING-EAST
A-F2-EAST-JUNCTION <-> A-F2-EAST-STAIR
A-F2-EAST-JUNCTION <-> A-F2-EAST-ROOM-01
A-F2-EAST-JUNCTION <-> A-F2-EAST-ROOM-02
A-F2-EAST-JUNCTION <-> A-F2-EAST-ROOM-03
```

---

## 6.6. Zone: South Wing

Node chính:

```txt
A-F2-SOUTH-JUNCTION
A-F2-SOUTH-STAIR
A-F2-SOUTH-ROOM-01
A-F2-SOUTH-ROOM-02
A-F2-SOUTH-ROOM-03
```

Edge chính:

```txt
A-F2-SOUTH-JUNCTION <-> A-F2-RING-SOUTH
A-F2-SOUTH-JUNCTION <-> A-F2-SOUTH-STAIR
A-F2-SOUTH-JUNCTION <-> A-F2-SOUTH-ROOM-01
A-F2-SOUTH-JUNCTION <-> A-F2-SOUTH-ROOM-02
A-F2-SOUTH-JUNCTION <-> A-F2-SOUTH-ROOM-03
```

---

## 6.7. Zone: Storage

Trên tầng 2 có khu vực “Kho”.

Node chính:

```txt
A-F2-STORAGE-01
A-F2-STORAGE-02
```

Ghi chú:

* Đây là khu vực không ưu tiên làm phòng tư vấn.
* Không nên cho routing đi xuyên qua kho nếu không phải hành lang công cộng.
* Có thể giữ node để hiển thị, nhưng không cần dùng trong shortest path.

Metadata gợi ý:

```txt
type = storage
accessible = false
candidate = false
```

---

## 6.8. Topology tổng quát tầng 2

```txt
                    A-F2-NORTH-JUNCTION
                             |
                       A-F2-RING-NORTH
                             |
A-F2-WEST-JUNCTION -- A-F2-RING-WEST -- A-F2-RING-EAST -- A-F2-EAST-JUNCTION
                             |
                       A-F2-RING-SOUTH
                             |
                    A-F2-SOUTH-JUNCTION
```

Vòng trung tâm:

```txt
A-F2-RING-NORTH
        |
A-F2-RING-EAST
        |
A-F2-RING-SOUTH
        |
A-F2-RING-WEST
        |
A-F2-RING-NORTH
```

---

# 7. Kết nối giữa tầng 1 và tầng 2

Dùng cầu thang để nối hai tầng.

Edge liên tầng:

```txt
A-F1-WEST-STAIR  <-> A-F2-WEST-STAIR
A-F1-EAST-STAIR  <-> A-F2-EAST-STAIR
A-F1-SOUTH-STAIR <-> A-F2-SOUTH-STAIR
A-F1-NORTH-STAIR <-> A-F2-NORTH-STAIR
```

Nếu chưa chắc cầu thang nào thật sự thẳng nhau, vẫn có thể thêm tạm và ghi chú:

```txt
needs_verification = true
```

---

# 8. Danh sách node tối thiểu

## 8.1. Tầng 1

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

---

## 8.2. Tầng 2

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

# 9. Ghi chú kiểm chứng sau này

Sau khi Codex sinh file JSON và ảnh graph, cần kiểm chứng các câu hỏi sau:

1. Từ thư viện có đi được sang khối chính không?
2. Từ cánh Tây có đi được sang cánh Đông không?
3. Từ cánh Bắc có đi được xuống cánh Nam không?
4. Từ tầng 1 có đi được lên tầng 2 không?
5. Các kho có bị dùng làm đường đi chính không?
6. Có node nào bị cô lập không?
7. Các cầu thang đã nối đúng giữa hai tầng chưa?
8. Các phòng có nối ra hành lang gần nhất chưa?
9. Hình dạng graph có nhìn giống sơ đồ thật ở mức tổng quát không?
10. Có cần thêm junction ở khu nào để đường đi tự nhiên hơn không?
