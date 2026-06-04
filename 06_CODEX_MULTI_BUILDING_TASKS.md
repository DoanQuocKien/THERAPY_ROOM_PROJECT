# 06_CODEX_MULTI_BUILDING_TASKS.md

# Codex Tasks — Multi-building UIT Graph

## 1. Mục tiêu

Mở rộng project graph hiện tại từ chỉ Tòa A sang toàn bộ UIT.

Project vẫn phải đơn giản:

```txt
Python local
JSON graph data
NetworkX
Matplotlib
Không backend
Không database
Không web app
```

Mục tiêu:

1. Load được campus graph.
2. Load được graph của từng tòa.
3. Merge tất cả thành một graph toàn trường.
4. Visualize campus graph.
5. Visualize từng building graph.
6. Chạy shortest path giữa hai phòng bất kỳ trong toàn UIT.

---

## 2. File cần tạo

```txt
campus_graph.json

building_a_graph.json
building_b_graph.json
building_c_graph.json
building_d_graph.json
building_e_graph.json

visualize_campus.py
visualize_building.py
shortest_path_global.py
validate_all_graphs.py

README.md
```

Có thể giữ `building_a_graph.json` hiện tại và chỉ thêm các file mới.

---

## 3. JSON schema thống nhất

Mỗi building graph nên có dạng:

```json
{
  "building": "B",
  "coordinate_system": {
    "type": "normalized",
    "width": 1000,
    "height": 1000
  },
  "floors": {
    "1": {
      "nodes": [],
      "edges": []
    }
  },
  "inter_floor_edges": []
}
```

Campus graph nên có dạng:

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

## 4. Node schema

```json
{
  "id": "B1.22",
  "label": "B1.22",
  "type": "room",
  "building": "B",
  "floor": 1,
  "x": 100,
  "y": 200,
  "zone": "B-F1-ROOMS",
  "accessible": true,
  "notes": ""
}
```

Node ngoài trời:

```json
{
  "id": "UIT-OUTDOOR-B-FRONT",
  "label": "Outdoor B Front",
  "type": "building_access",
  "building": null,
  "floor": null,
  "x": 620,
  "y": 350,
  "zone": "UIT-CAMPUS",
  "accessible": true,
  "notes": ""
}
```

---

## 5. Edge schema

```json
{
  "source": "B-F1-CORRIDOR-01",
  "target": "B1.22-ACCESS",
  "distance": 8,
  "type": "corridor",
  "bidirectional": true,
  "accessible": true,
  "notes": ""
}
```

---

## 6. Coding task 1 — Create campus graph

Create:

```txt
campus_graph.json
```

Include nodes:

```txt
UIT-GATE-A
UIT-GATE-B

UIT-OUTDOOR-A-FRONT
UIT-OUTDOOR-B-FRONT
UIT-OUTDOOR-C-FRONT
UIT-OUTDOOR-D-FRONT
UIT-OUTDOOR-E-FRONT

UIT-INTERSECTION-CENTER
UIT-INTERSECTION-CANTEEN
UIT-CANTEEN
```

Include walkway nodes if useful:

```txt
UIT-WALKWAY-A-E
UIT-WALKWAY-A-B
UIT-WALKWAY-A-C
UIT-WALKWAY-B-C
UIT-WALKWAY-E-C
UIT-WALKWAY-C-D
```

Include building entry edges:

```txt
UIT-OUTDOOR-A-FRONT <-> A-F1-BUILDING-ENTRANCE
UIT-OUTDOOR-B-FRONT <-> B-F1-BUILDING-ENTRANCE
UIT-OUTDOOR-C-FRONT <-> C-F1-BUILDING-ENTRANCE
UIT-OUTDOOR-D-FRONT <-> D-F1-BUILDING-ENTRANCE
UIT-OUTDOOR-E-FRONT <-> E-F1-BUILDING-ENTRANCE
```

---

## 7. Coding task 2 — Create Building B graph

Create:

```txt
building_b_graph.json
```

Use staircase-shaped floors.

Room lists:

```txt
Floor 1:
B1.22 B1.20 B1.18 B1.16 B1.14 B1.12 B1.10 B1.08 B1.06 B1.04 B1.02 B1.01

Floor 2:
B2.22 B2.20 B2.18 B2.16 B2.14 B2.12 B2.10 B2.08 B2.06 B2.04 B2.02 B2.01

Floor 3:
B3.22 B3.20 B3.18 B3.16 B3.14 B3.12 B3.10 B3.08 B3.06 B3.04 B3.02 B3.01

Floor 4:
B4.22 B4.20 B4.18 B4.16 B4.14 B4.12 B4.10 B4.08 B4.06 B4.04 B4.02 B4.01

Floor 5:
B5.14 B5.12 B5.10 B5.08 B5.06 B5.04 B5.02 B5.01

Floor 6:
B6.12 B6.10 B6.08 B6.06 B6.04 B6.02 B6.01

Floor 7:
B7.08 B7.06 B7.04 B7.02 B7.01

Floor 8:
B8.08 B8.06 B8.04 B8.02

Floor 9:
B9.04 B9.02
```

For every room:

```txt
Create ROOM node
Create ACCESS node
Connect corridor -> access -> room
```

Generate corridor length based on number of main rooms on that floor.

Important visualization rule:

```txt
Higher floors must look shorter.
The right side should shrink as floor number increases.
This creates the staircase-like shape of Building B.
```

---

## 8. Coding task 3 — Create Building C graph

Create:

```txt
building_c_graph.json
```

Floor 1 rooms:

```txt
C113 C111 C109 C107 C105 C103 C101
C110 C108 C106 C104 C102
```

Floor 2 rooms:

```txt
C213 C211 C209 C207 C205 C203 C201
C218 C216 C214 C212 C210 C208 C206 C204 C202
```

Floor 3 rooms:

```txt
C315 C313 C311 C309 C307 C305 C303 C301
C318 C316 C314 C312 C310 C308 C306 C304 C302
```

For each floor:

```txt
Create one horizontal corridor.
Create left, mid, right stair nodes.
Attach rooms to nearest corridor node.
Connect stairs vertically.
```

---

## 9. Coding task 4 — Create Building D graph

Create:

```txt
building_d_graph.json
```

Use simple 4-room model:

```txt
D-F1-BUILDING-ENTRANCE
D-F1-CENTER
D-F1-ROOM-01
D-F1-ROOM-02
D-F1-ROOM-03
D-F1-ROOM-04
```

Each room has access node.

Edges:

```txt
D-F1-BUILDING-ENTRANCE <-> D-F1-CENTER
D-F1-CENTER <-> D-F1-ROOM-01-ACCESS <-> D-F1-ROOM-01
D-F1-CENTER <-> D-F1-ROOM-02-ACCESS <-> D-F1-ROOM-02
D-F1-CENTER <-> D-F1-ROOM-03-ACCESS <-> D-F1-ROOM-03
D-F1-CENTER <-> D-F1-ROOM-04-ACCESS <-> D-F1-ROOM-04
```

---

## 10. Coding task 5 — Create Building E graph

Create:

```txt
building_e_graph.json
```

Use repeated vertical building pattern.

Create floor nodes:

```txt
E-FG-CORRIDOR
E-F1-CORRIDOR
E-F2-CORRIDOR
...
E-F12-CORRIDOR
```

Create elevator/stair nodes:

```txt
E-FG-ELEVATOR
E-F1-ELEVATOR
...
E-F12-ELEVATOR

E-FG-STAIR
E-F1-STAIR
...
E-F12-STAIR
```

Create vertical edges:

```txt
E-FG-ELEVATOR <-> E-F1-ELEVATOR <-> ... <-> E-F12-ELEVATOR
E-FG-STAIR <-> E-F1-STAIR <-> ... <-> E-F12-STAIR
```

Rooms to include:

```txt
Floor 1:
E1.1 E1.2 E1.3 E1.4 E1.5 E1.7

Floor 2:
E2.1 E2.2 E2.3 E2.4 E2.5

Floor 3:
E3.1 E3.2 E3.3 E3.4 E3.5

Floor 4:
E4.1 E4.2 E4.3 E4.4 E4.5

Floor 5:
E5.1

Floor 6:
E6.1

Floor 7:
E7.1

Floor 8:
E8.1

Floor 9:
E9.1

Floor 10:
E10.1

Floor 11:
E11.1 E11.2 E11.3 E11.4 E11.6 E11.8

Floor 12:
E12.1 E12.2
```

Every room must have access node.

---

## 11. Coding task 6 — Merge all graphs

Create function:

```python
def load_all_graphs() -> nx.Graph:
    pass
```

It should load:

```txt
campus_graph.json
building_a_graph.json
building_b_graph.json
building_c_graph.json
building_d_graph.json
building_e_graph.json
```

Then merge:

```txt
campus nodes
campus edges
building nodes
building edges
inter-floor edges
building-entry edges
```

---

## 12. Coding task 7 — Global shortest path

Create:

```txt
shortest_path_global.py
```

Example test cases:

```python
start = "A-F1-TOP-ROOM-01"
end = "C205"
```

```python
start = "B1.22"
end = "E12.2"
```

```python
start = "UIT-GATE-A"
end = "D-F1-ROOM-04"
```

Output:

```txt
Shortest path:
...
Total distance:
Number of nodes:
Buildings passed:
Floors passed:
```

---

## 13. Coding task 8 — Visualization

Create:

```txt
visualize_campus.py
visualize_building.py
```

`visualize_campus.py`:

* Draw campus graph only.
* Show gates.
* Show building outdoor access nodes.
* Show outdoor paths.
* Save `campus_graph.png`.

`visualize_building.py`:

* Input building ID.
* Draw each floor separately.
* Save PNG per floor.

Example:

```bash
python visualize_building.py B
python visualize_building.py C
python visualize_building.py E
```

---

## 14. Coding task 9 — Validation

Create:

```txt
validate_all_graphs.py
```

Check:

1. Duplicate node IDs.
2. Edge source/target exists.
3. Isolated nodes.
4. Each room has access node.
5. Each access node connects to corridor and room.
6. Each building has entrance node.
7. Each building entrance connects to campus graph.
8. Stairs/elevators connect vertically.
9. Global graph is connected.
10. Dijkstra works between sample pairs.

---

## 15. Acceptance criteria

The multi-building graph is successful if:

1. Building A graph still works.
2. Building B graph has staircase-like shrinking floors.
3. Building C graph has 3 corridor floors.
4. Building D graph has 4 rooms.
5. Building E graph has vertical floors 1–12.
6. Campus graph connects A, B, C, D, E, Gate A, Gate B.
7. Global shortest path works between any two major rooms.
8. Visualizations are clear enough to inspect manually.
9. Code remains simple Python, not a full app.
10. The graph can later be used for student movement simulation.
