# 03_CODEX_IMPLEMENTATION_TASKS_UPDATED.md

# Codex Implementation Tasks — Updated Building A Graph

## 1. Mục tiêu cập nhật

Hãy sửa graph Tòa A theo hướng:

```txt
main path → access node → room node
```

Không nối trực tiếp mọi phòng vào một junction duy nhất nữa.

Mục tiêu là để sau này khi mô phỏng sinh viên, đường đi sẽ chạy dọc theo hành lang, đi ngang qua các access node trước cửa phòng, rồi mới rẽ vào phòng nếu phòng đó là đích đến.

---

## 2. Cập nhật node types

Dùng:

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

Đặc biệt thêm type:

```txt
access
```

`access` là node nằm trước phòng, đại diện cho cửa hoặc điểm tiếp cận phòng từ hành lang.

---

## 3. Cập nhật tầng 1

### 3.1. Main ring nodes

Tạo các node đường đi chính:

```txt
A-F1-RING-TOP-LEFT
A-F1-RING-TOP-MID
A-F1-RING-TOP-RIGHT

A-F1-RING-LEFT-MID
A-F1-RING-RIGHT-MID

A-F1-RING-BOTTOM-LEFT
A-F1-RING-BOTTOM-MID
A-F1-RING-BOTTOM-RIGHT

A-F1-CENTER-CROSS
```

Các node này tạo ra trục đi bộ chính.

---

### 3.2. Main ring edges

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

Center cross:

```txt
A-F1-CENTER-CROSS <-> A-F1-RING-TOP-MID
A-F1-CENTER-CROSS <-> A-F1-RING-BOTTOM-MID
A-F1-CENTER-CROSS <-> A-F1-RING-LEFT-MID
A-F1-CENTER-CROSS <-> A-F1-RING-RIGHT-MID
```

---

## 4. Tầng 1 — outer rooms

### 4.1. Top side: 5 rooms

Create:

```txt
A-F1-TOP-ROOM-01
A-F1-TOP-ROOM-02
A-F1-TOP-ROOM-03
A-F1-TOP-ROOM-04
A-F1-TOP-ROOM-05
```

Access:

```txt
A-F1-TOP-ROOM-01-ACCESS
A-F1-TOP-ROOM-02-ACCESS
A-F1-TOP-ROOM-03-ACCESS
A-F1-TOP-ROOM-04-ACCESS
A-F1-TOP-ROOM-05-ACCESS
```

Connect each room as:

```txt
ring node <-> access node <-> room node
```

---

### 4.2. Bottom side: 5 rooms

Create:

```txt
A-F1-BOTTOM-ROOM-01
A-F1-BOTTOM-ROOM-02
A-F1-BOTTOM-ROOM-03
A-F1-BOTTOM-ROOM-04
A-F1-BOTTOM-ROOM-05
```

Access:

```txt
A-F1-BOTTOM-ROOM-01-ACCESS
A-F1-BOTTOM-ROOM-02-ACCESS
A-F1-BOTTOM-ROOM-03-ACCESS
A-F1-BOTTOM-ROOM-04-ACCESS
A-F1-BOTTOM-ROOM-05-ACCESS
```

---

### 4.3. Left side: 2 rooms

```txt
A-F1-LEFT-ROOM-01
A-F1-LEFT-ROOM-02
```

Access:

```txt
A-F1-LEFT-ROOM-01-ACCESS
A-F1-LEFT-ROOM-02-ACCESS
```

---

### 4.4. Right side: 2 rooms

```txt
A-F1-RIGHT-ROOM-01
A-F1-RIGHT-ROOM-02
```

Access:

```txt
A-F1-RIGHT-ROOM-01-ACCESS
A-F1-RIGHT-ROOM-02-ACCESS
```

---

## 5. Tầng 1 — inner block rooms

### 5.1. Top-right inner block: 3 rooms

```txt
A-F1-INNER-TOP-RIGHT-ROOM-01
A-F1-INNER-TOP-RIGHT-ROOM-02
A-F1-INNER-TOP-RIGHT-ROOM-03
```

Each room needs an access node.

---

### 5.2. Bottom-right inner block: 3 rooms

```txt
A-F1-INNER-BOTTOM-RIGHT-ROOM-01
A-F1-INNER-BOTTOM-RIGHT-ROOM-02
A-F1-INNER-BOTTOM-RIGHT-ROOM-03
```

Each room needs an access node.

---

### 5.3. Top-left inner block: 2 rooms

```txt
A-F1-INNER-TOP-LEFT-ROOM-01
A-F1-INNER-TOP-LEFT-ROOM-02
```

Each room needs an access node.

---

### 5.4. Bottom-left inner block: 2 rooms

```txt
A-F1-INNER-BOTTOM-LEFT-ROOM-01
A-F1-INNER-BOTTOM-LEFT-ROOM-02
```

Each room needs an access node.

---

## 6. Tầng 1 — center corridor rooms

### 6.1. Left horizontal corridor

The left horizontal corridor is:

```txt
A-F1-RING-LEFT-MID <-> A-F1-CENTER-CROSS
```

It has 2 rooms above and 2 rooms below.

Upper rooms:

```txt
A-F1-MID-LEFT-UPPER-ROOM-01
A-F1-MID-LEFT-UPPER-ROOM-02
```

Lower rooms:

```txt
A-F1-MID-LEFT-LOWER-ROOM-01
A-F1-MID-LEFT-LOWER-ROOM-02
```

Each room needs an access node.

---

### 6.2. Upper vertical corridor

The upper vertical corridor is:

```txt
A-F1-CENTER-CROSS <-> A-F1-RING-TOP-MID
```

It has 2 rooms on the right side.

```txt
A-F1-MID-TOP-RIGHT-ROOM-01
A-F1-MID-TOP-RIGHT-ROOM-02
```

Each room needs an access node.

---

### 6.3. Lower vertical corridor

The lower vertical corridor is:

```txt
A-F1-CENTER-CROSS <-> A-F1-RING-BOTTOM-MID
```

It has 2 rooms on the right side.

```txt
A-F1-MID-BOTTOM-RIGHT-ROOM-01
A-F1-MID-BOTTOM-RIGHT-ROOM-02
```

Each room needs an access node.

---

## 7. Library

Tầng 1:

```txt
A-F1-LIBRARY-CENTER
A-F1-LIBRARY-ENTRANCE
A-F1-LIBRARY-CONNECTOR
```

Edges:

```txt
A-F1-LIBRARY-CENTER <-> A-F1-LIBRARY-ENTRANCE
A-F1-LIBRARY-ENTRANCE <-> A-F1-LIBRARY-CONNECTOR
A-F1-LIBRARY-CONNECTOR <-> A-F1-RING-LEFT-MID
```

Tầng 2 cũng có thư viện:

```txt
A-F2-LIBRARY-CENTER
A-F2-LIBRARY-ENTRANCE
A-F2-LIBRARY-CONNECTOR
```

Edges:

```txt
A-F2-LIBRARY-CENTER <-> A-F2-LIBRARY-ENTRANCE
A-F2-LIBRARY-ENTRANCE <-> A-F2-LIBRARY-CONNECTOR
A-F2-LIBRARY-CONNECTOR <-> A-F2-RING-LEFT
```

---

## 8. Tầng 2 updated structure

Tầng 2 gồm một ring đơn giản:

```txt
A-F2-RING-TOP
A-F2-RING-RIGHT
A-F2-RING-BOTTOM
A-F2-RING-LEFT
A-F2-CENTER-CROSS
```

Edges:

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

Each direction has 2 rooms:

```txt
A-F2-TOP-ROOM-01
A-F2-TOP-ROOM-02

A-F2-BOTTOM-ROOM-01
A-F2-BOTTOM-ROOM-02

A-F2-LEFT-ROOM-01
A-F2-LEFT-ROOM-02

A-F2-RIGHT-ROOM-01
A-F2-RIGHT-ROOM-02
```

Each room must have an access node.

---

## 9. Stair nodes

Create stair nodes:

```txt
A-F1-STAIR-LEFT
A-F1-STAIR-RIGHT
A-F1-STAIR-BOTTOM
A-F1-STAIR-TOP

A-F2-STAIR-LEFT
A-F2-STAIR-RIGHT
A-F2-STAIR-BOTTOM
A-F2-STAIR-TOP
```

Inter-floor edges:

```txt
A-F1-STAIR-LEFT <-> A-F2-STAIR-LEFT
A-F1-STAIR-RIGHT <-> A-F2-STAIR-RIGHT
A-F1-STAIR-BOTTOM <-> A-F2-STAIR-BOTTOM
A-F1-STAIR-TOP <-> A-F2-STAIR-TOP
```

---

## 10. Visualization requirement

When drawing:

* corridor/junction nodes should form the main path.
* access nodes should be smaller.
* room nodes should be outside or beside the main path.
* shortest path should mostly follow corridor/junction nodes.
* the path should only enter room nodes at the start or destination.

This is important for future student movement simulation.

---

## 11. Validation checklist

The updated graph is correct if:

1. Main path tầng 1 looks like a square/ring.
2. There is a center cross.
3. Every room has an access node.
4. Top side floor 1 has 5 rooms.
5. Bottom side floor 1 has 5 rooms.
6. Left side floor 1 has 2 rooms.
7. Right side floor 1 has 2 rooms.
8. Top-right and bottom-right inner blocks have 3 rooms each.
9. Top-left and bottom-left inner blocks have 2 rooms each.
10. Left middle corridor has 2 rooms above and 2 rooms below.
11. Upper vertical corridor has 2 rooms on the right.
12. Lower vertical corridor has 2 rooms on the right.
13. Floor 2 has 2 rooms in each direction.
14. Floor 2 connects to library.
15. Shortest path does not jump directly between rooms.
