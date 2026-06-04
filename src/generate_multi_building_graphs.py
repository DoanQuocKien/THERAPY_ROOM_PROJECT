import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_DIR = ROOT / "data" / "graphs"


def node(node_id, label, node_type, building, floor, x, y, zone, accessible=True, notes=""):
    return {
        "id": node_id,
        "label": label,
        "type": node_type,
        "building": building,
        "floor": floor,
        "x": x,
        "y": y,
        "zone": zone,
        "accessible": accessible,
        "notes": notes,
    }


def edge(source, target, distance=10, edge_type="corridor", notes=""):
    return {
        "source": source,
        "target": target,
        "distance": distance,
        "type": edge_type,
        "bidirectional": True,
        "accessible": True,
        "notes": notes,
    }


def write_json(path, data):
    output = Path(path)
    if not output.is_absolute():
        output = GRAPH_DIR / output.name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def building_shell(building):
    return {
        "building": building,
        "coordinate_system": {"type": "normalized", "width": 1000, "height": 1000},
        "floors": {},
        "inter_floor_edges": [],
    }


def chain_edges(ids, distance=10, edge_type="corridor"):
    return [edge(source, target, distance, edge_type) for source, target in zip(ids, ids[1:])]


def add_access_room(nodes, edges, room_id, building, floor, access_x, access_y, room_x, room_y, zone):
    access_id = f"{room_id}-ACCESS"
    nodes.append(node(access_id, f"{room_id} Access", "access", building, floor, access_x, access_y, zone))
    nodes.append(node(room_id, room_id, "room", building, floor, room_x, room_y, zone))
    edges.append(edge(access_id, room_id, 8, "door"))
    return access_id


def make_campus():
    nodes = [
        node("UIT-GATE-A", "Gate A", "gate", None, None, 230, 90, "UIT-CAMPUS"),
        node("UIT-GATE-B", "Gate B", "gate", None, None, 760, 900, "UIT-CAMPUS"),
        node("UIT-GARAGE", "Garage", "garage", None, None, 120, 150, "UIT-CAMPUS", notes="Personal transportation parking area linked to Gate A and rough back routes."),
        node("UIT-OUTDOOR-A-FRONT", "Outdoor A Front", "building_access", None, None, 310, 210, "UIT-CAMPUS"),
        node("UIT-OUTDOOR-B-FRONT", "Outdoor B Front", "building_access", None, None, 720, 280, "UIT-CAMPUS"),
        node("UIT-OUTDOOR-C-FRONT", "Outdoor C Front", "building_access", None, None, 520, 620, "UIT-CAMPUS"),
        node("UIT-OUTDOOR-D-FRONT", "Outdoor D Front", "building_access", None, None, 520, 850, "UIT-CAMPUS"),
        node("UIT-OUTDOOR-E-FRONT", "Outdoor E Front", "building_access", None, None, 170, 430, "UIT-CAMPUS"),
        node("UIT-WALKWAY-A-E", "Walkway A E", "walkway", None, None, 230, 330, "UIT-CAMPUS"),
        node("UIT-WALKWAY-A-B", "Walkway A B", "walkway", None, None, 540, 230, "UIT-CAMPUS"),
        node("UIT-WALKWAY-A-C", "Walkway A C", "walkway", None, None, 410, 390, "UIT-CAMPUS"),
        node("UIT-WALKWAY-B-C", "Walkway B C", "walkway", None, None, 650, 460, "UIT-CAMPUS"),
        node("UIT-WALKWAY-E-C", "Walkway E C", "walkway", None, None, 300, 520, "UIT-CAMPUS"),
        node("UIT-INTERSECTION-CENTER", "Center Intersection", "intersection", None, None, 500, 500, "UIT-CAMPUS"),
        node("UIT-INTERSECTION-CANTEEN", "Canteen Intersection", "intersection", None, None, 560, 740, "UIT-CAMPUS"),
        node("UIT-CANTEEN", "Canteen", "canteen", None, None, 690, 720, "UIT-CAMPUS"),
    ]
    edges = [
        edge("UIT-GATE-A", "UIT-OUTDOOR-A-FRONT", 20, "gate_entry"),
        edge("UIT-GATE-A", "UIT-GARAGE", 12, "garage_entry", "Gate A connection to bike/motorbike garage."),
        edge("UIT-OUTDOOR-A-FRONT", "UIT-WALKWAY-A-E", 18, "outdoor_walk"),
        edge("UIT-WALKWAY-A-E", "UIT-OUTDOOR-E-FRONT", 25, "outdoor_walk"),
        edge("UIT-OUTDOOR-A-FRONT", "UIT-WALKWAY-A-B", 22, "outdoor_walk"),
        edge("UIT-WALKWAY-A-B", "UIT-OUTDOOR-B-FRONT", 25, "outdoor_walk"),
        edge("UIT-OUTDOOR-A-FRONT", "UIT-WALKWAY-A-C", 26, "outdoor_walk"),
        edge("UIT-WALKWAY-A-C", "UIT-INTERSECTION-CENTER", 24, "outdoor_walk"),
        edge("UIT-OUTDOOR-B-FRONT", "UIT-WALKWAY-B-C", 20, "outdoor_walk"),
        edge("UIT-WALKWAY-B-C", "UIT-INTERSECTION-CENTER", 20, "outdoor_walk"),
        edge("UIT-OUTDOOR-E-FRONT", "UIT-WALKWAY-E-C", 22, "outdoor_walk"),
        edge("UIT-WALKWAY-E-C", "UIT-INTERSECTION-CENTER", 22, "outdoor_walk"),
        edge("UIT-INTERSECTION-CENTER", "UIT-OUTDOOR-C-FRONT", 25, "outdoor_walk"),
        edge("UIT-OUTDOOR-C-FRONT", "UIT-INTERSECTION-CANTEEN", 25, "outdoor_walk"),
        edge("UIT-INTERSECTION-CANTEEN", "UIT-CANTEEN", 12, "campus_connector"),
        edge("UIT-INTERSECTION-CANTEEN", "UIT-OUTDOOR-D-FRONT", 35, "outdoor_walk"),
        edge("UIT-INTERSECTION-CANTEEN", "UIT-GATE-B", 30, "gate_entry"),
    ]
    entry_edges = [
        edge("UIT-OUTDOOR-A-FRONT", "A-F1-BUILDING-ENTRANCE", 8, "building_entry"),
        edge("UIT-GATE-A", "A-F1-RING-BOTTOM-RIGHT", 24, "gate_to_building_a_ring", "Rough public-transport path from Gate A into Building A ring bottom right."),
        edge("UIT-GARAGE", "A-F1-RING-LEFT-MID", 18, "garage_to_building_a_ring", "Garage route to Building A ring left middle."),
        edge("UIT-GARAGE", "A-F1-RING-TOP-LEFT", 20, "garage_to_building_a_ring", "Garage route to Building A ring top left."),
        edge("UIT-GARAGE", "B-F1-BUILDING-ENTRANCE", 65, "garage_back_road", "Long direct back road between Building B and the garage."),
        edge("UIT-GARAGE", "E-F1-LOBBY", 52, "garage_e_route", "Garage route through Building E / across Building A."),
        edge("A-F1-RING-RIGHT-MID", "E-F1-LOBBY", 22, "building_a_to_e_crossing", "Preferred Building A exit toward E/C crossing."),
        edge("A-F1-RING-TOP-MID", "B-F1-BUILDING-ENTRANCE", 24, "building_a_to_b_crossing", "Preferred Building A top route toward B/C."),
        edge("A-F1-RING-TOP-RIGHT", "B-F1-BUILDING-ENTRANCE", 22, "building_a_to_b_crossing", "Preferred Building A top-right route toward B/C."),
        edge("UIT-OUTDOOR-B-FRONT", "B-F1-BUILDING-ENTRANCE", 8, "building_entry"),
        edge("UIT-OUTDOOR-C-FRONT", "C-F1-BUILDING-ENTRANCE", 8, "building_entry"),
        edge("UIT-OUTDOOR-D-FRONT", "D-F1-BUILDING-ENTRANCE", 8, "building_entry"),
        edge("UIT-OUTDOOR-E-FRONT", "E-F1-BUILDING-ENTRANCE", 8, "building_entry"),
    ]
    write_json("campus_graph.json", {
        "campus": "UIT",
        "coordinate_system": {"type": "normalized", "width": 1000, "height": 1000},
        "nodes": nodes,
        "edges": edges,
        "building_entry_edges": entry_edges,
    })


def make_b():
    rooms = {
        1: "B1.22 B1.20 B1.18 B1.16 B1.14 B1.12 B1.10 B1.08 B1.06 B1.04 B1.02 B1.01".split(),
        2: "B2.22 B2.20 B2.18 B2.16 B2.14 B2.12 B2.10 B2.08 B2.06 B2.04 B2.02 B2.01".split(),
        3: "B3.22 B3.20 B3.18 B3.16 B3.14 B3.12 B3.10 B3.08 B3.06 B3.04 B3.02 B3.01".split(),
        4: "B4.22 B4.20 B4.18 B4.16 B4.14 B4.12 B4.10 B4.08 B4.06 B4.04 B4.02 B4.01".split(),
        5: "B5.14 B5.12 B5.10 B5.08 B5.06 B5.04 B5.02 B5.01".split(),
        6: "B6.12 B6.10 B6.08 B6.06 B6.04 B6.02 B6.01".split(),
        7: "B7.08 B7.06 B7.04 B7.02 B7.01".split(),
        8: "B8.08 B8.06 B8.04 B8.02".split(),
        9: "B9.04 B9.02".split(),
    }
    graph = building_shell("B")
    max_stairs = 0
    for floor, floor_rooms in rooms.items():
        nodes, edges, road = [], [], []
        start_x, step, y = 100, 62, 500
        start_id = f"B-F{floor}-CORE-LEFT"
        nodes.append(node(start_id, "Core Left", "stair", "B", floor, start_x - 45, y, f"B-F{floor}-CORE"))
        road.append(start_id)
        if floor == 1:
            nodes.append(node("B-F1-BUILDING-ENTRANCE", "Building B Entrance", "entrance", "B", 1, 55, 610, "B-F1-ENTRY"))
            edges.append(edge("B-F1-BUILDING-ENTRANCE", start_id, 10, "building_entry"))

        stair_count = 0
        for idx, room_id in enumerate(floor_rooms):
            x = start_x + idx * step
            top = idx % 2 == 0
            access_id = add_access_room(
                nodes,
                edges,
                room_id,
                "B",
                floor,
                x,
                y,
                x,
                330 if top else 700,
                f"B-F{floor}-ROOMS",
            )
            road.append(access_id)
            if idx % 2 == 1:
                stair_count += 1
                stair_id = f"B-F{floor}-STAIR-{stair_count:02d}"
                nodes.append(node(stair_id, f"Stair {stair_count:02d}", "stair", "B", floor, x + step / 2, 620, f"B-F{floor}-STAIRS"))
                road.append(stair_id)
        max_stairs = max(max_stairs, stair_count)

        mid_id = f"B-F{floor}-CORE-MID"
        right_id = f"B-F{floor}-CORE-RIGHT"
        nodes.extend([
            node(mid_id, "Core Mid", "elevator", "B", floor, start_x + max(1, len(floor_rooms) // 2) * step, 620, f"B-F{floor}-CORE"),
            node(right_id, "Core Right", "stair", "B", floor, start_x + len(floor_rooms) * step + 35, y, f"B-F{floor}-CORE"),
        ])
        road.append(right_id)
        edges.extend(chain_edges(road, 10, "corridor"))
        edges.append(edge(mid_id, road[min(len(road) - 2, max(1, len(road) // 2))], 8, "elevator"))
        graph["floors"][str(floor)] = {"nodes": nodes, "edges": edges}

    for floor in range(1, 9):
        graph["inter_floor_edges"].extend([
            edge(f"B-F{floor}-CORE-LEFT", f"B-F{floor+1}-CORE-LEFT", 12, "stair"),
            edge(f"B-F{floor}-CORE-MID", f"B-F{floor+1}-CORE-MID", 10, "elevator"),
            edge(f"B-F{floor}-CORE-RIGHT", f"B-F{floor+1}-CORE-RIGHT", 12, "stair"),
        ])
        current_nodes = {n["id"] for n in graph["floors"][str(floor)]["nodes"]}
        next_nodes = {n["id"] for n in graph["floors"][str(floor + 1)]["nodes"]}
        for stair_idx in range(1, max_stairs + 1):
            a = f"B-F{floor}-STAIR-{stair_idx:02d}"
            b = f"B-F{floor+1}-STAIR-{stair_idx:02d}"
            if a in current_nodes and b in next_nodes:
                graph["inter_floor_edges"].append(edge(a, b, 12, "stair"))
    write_json("building_b_graph.json", graph)


def make_c():
    rooms = {
        1: "C113 C111 C109 C107 C105 C103 C101 C110 C108 C106 C104 C102".split(),
        2: "C213 C211 C209 C207 C205 C203 C201 C218 C216 C214 C212 C210 C208 C206 C204 C202".split(),
        3: "C315 C313 C311 C309 C307 C305 C303 C301 C318 C316 C314 C312 C310 C308 C306 C304 C302".split(),
    }
    graph = building_shell("C")
    for floor, floor_rooms in rooms.items():
        nodes, edges, road = [], [], []
        left = f"C-F{floor}-STAIR-LEFT"
        mid = f"C-F{floor}-STAIR-MID"
        right = f"C-F{floor}-STAIR-RIGHT"
        nodes.extend([
            node(left, "Stair Left", "stair", "C", floor, 90, 500, f"C-F{floor}-CORE"),
            node(mid, "Stair Mid", "stair", "C", floor, 500, 610, f"C-F{floor}-CORE"),
            node(right, "Stair Right", "stair", "C", floor, 900, 500, f"C-F{floor}-CORE"),
        ])
        road.append(left)
        for idx, room_id in enumerate(floor_rooms):
            x = 150 + idx * (760 / max(1, len(floor_rooms) - 1))
            top = idx % 2 == 0
            access_id = add_access_room(nodes, edges, room_id, "C", floor, x, 500, x, 320 if top else 700, f"C-F{floor}-ROOMS")
            road.append(access_id)
            if idx == len(floor_rooms) // 2:
                road.append(mid)
        road.append(right)
        edges.extend(chain_edges(road, 9, "corridor"))
        if floor == 1:
            nodes.append(node("C-F1-BUILDING-ENTRANCE", "Building C Entrance", "entrance", "C", 1, 60, 600, "C-F1-ENTRY"))
            edges.append(edge("C-F1-BUILDING-ENTRANCE", left, 10, "building_entry"))
        graph["floors"][str(floor)] = {"nodes": nodes, "edges": edges}
    for floor in [1, 2]:
        for name in ["LEFT", "MID", "RIGHT"]:
            graph["inter_floor_edges"].append(edge(f"C-F{floor}-STAIR-{name}", f"C-F{floor+1}-STAIR-{name}", 12, "stair"))
    write_json("building_c_graph.json", graph)


def make_d():
    graph = building_shell("D")
    nodes = [
        node("D-F1-BUILDING-ENTRANCE", "Building D Entrance", "entrance", "D", 1, 500, 850, "D-F1-ENTRY"),
        node("D-F1-CENTER", "Center", "junction", "D", 1, 500, 500, "D-F1-CENTER"),
    ]
    edges = [edge("D-F1-BUILDING-ENTRANCE", "D-F1-CENTER", 12, "building_entry")]
    specs = [("01", 500, 360, 500, 220), ("02", 360, 500, 220, 500), ("03", 640, 500, 780, 500), ("04", 500, 640, 500, 780)]
    for suffix, ax, ay, rx, ry in specs:
        add_access_room(nodes, edges, f"D-F1-ROOM-{suffix}", "D", 1, ax, ay, rx, ry, "D-F1-ROOMS")
        edges.append(edge("D-F1-CENTER", f"D-F1-ROOM-{suffix}-ACCESS", 8, "corridor"))
    graph["floors"]["1"] = {"nodes": nodes, "edges": edges}
    write_json("building_d_graph.json", graph)


def make_e():
    room_map = {
        1: "E1.1 E1.2 E1.3 E1.4 E1.5 E1.7".split(),
        2: "E2.1 E2.2 E2.3 E2.4 E2.5".split(),
        3: "E3.1 E3.2 E3.3 E3.4 E3.5".split(),
        4: "E4.1 E4.2 E4.3 E4.4 E4.5".split(),
        5: ["E5.1"], 6: ["E6.1"], 7: ["E7.1"], 8: ["E8.1"], 9: ["E9.1"], 10: ["E10.1"],
        11: "E11.1 E11.2 E11.3 E11.4 E11.6 E11.8".split(),
        12: "E12.1 E12.2".split(),
    }
    graph = building_shell("E")
    for floor in range(1, 13):
        nodes, edges, road = [], [], []
        elevator = f"E-F{floor}-ELEVATOR"
        stair = f"E-F{floor}-STAIR"
        wc = f"E-F{floor}-WC"
        nodes.extend([
            node(elevator, "Elevator", "elevator", "E", floor, 260, 500, f"E-F{floor}-CORE"),
            node(stair, "Stair", "stair", "E", floor, 820, 500, f"E-F{floor}-CORE"),
            node(wc, "WC", "wc", "E", floor, 520, 620, f"E-F{floor}-SERVICE"),
        ])
        road.append(elevator)
        for idx, room_id in enumerate(room_map[floor]):
            x = 330 + idx * (430 / max(1, len(room_map[floor]) - 1))
            top = idx % 2 == 0
            road.append(add_access_room(nodes, edges, room_id, "E", floor, x, 500, x, 315 if top else 700, f"E-F{floor}-ROOMS"))
        road.append(stair)
        corridor = f"E-F{floor}-CORRIDOR"
        nodes.append(node(corridor, "Corridor Mid", "corridor", "E", floor, 520, 500, f"E-F{floor}-CORRIDOR"))
        road.insert(max(1, len(road) // 2), corridor)
        edges.extend(chain_edges(road, 9, "corridor"))
        edges.append(edge(wc, corridor, 6, "corridor"))
        if floor == 1:
            nodes.extend([
                node("E-F1-BUILDING-ENTRANCE", "Building E Entrance", "entrance", "E", 1, 500, 850, "E-F1-ENTRY"),
                node("E-F1-LOBBY", "Lobby", "junction", "E", 1, 500, 720, "E-F1-ENTRY"),
            ])
            edges.extend([edge("E-F1-BUILDING-ENTRANCE", "E-F1-LOBBY", 8, "building_entry"), edge("E-F1-LOBBY", corridor, 10)])
        graph["floors"][str(floor)] = {"nodes": nodes, "edges": edges}
    for floor in range(1, 12):
        graph["inter_floor_edges"].append(edge(f"E-F{floor}-ELEVATOR", f"E-F{floor+1}-ELEVATOR", 10, "elevator"))
        graph["inter_floor_edges"].append(edge(f"E-F{floor}-STAIR", f"E-F{floor+1}-STAIR", 12, "stair"))
    write_json("building_e_graph.json", graph)


if __name__ == "__main__":
    make_campus()
    make_b()
    make_c()
    make_d()
    make_e()
