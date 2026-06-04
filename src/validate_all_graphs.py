from __future__ import annotations

import networkx as nx

from graph_utils import BUILDING_FILES, CAMPUS_FILE, load_all_graphs, load_json, shortest_path


SAMPLES = [
    ("A-F1-TOP-ROOM-01", "C205"),
    ("B1.22", "B9.02"),
    ("C102", "C315"),
    ("E1.1", "E12.2"),
    ("UIT-GATE-A", "D-F1-ROOM-04"),
]


def validate() -> list[str]:
    warnings = []
    all_ids = []
    all_edges = []
    room_ids = []
    access_ids = set()

    campus = load_json(CAMPUS_FILE)
    all_ids.extend(node["id"] for node in campus["nodes"])
    all_edges.extend(campus["edges"])
    all_edges.extend(campus["building_entry_edges"])

    for building, path in BUILDING_FILES.items():
        data = load_json(path)
        entrance = f"{building}-F1-BUILDING-ENTRANCE"
        building_node_ids = []
        for floor_data in data["floors"].values():
            for node in floor_data["nodes"]:
                all_ids.append(node["id"])
                building_node_ids.append(node["id"])
                if node.get("type") == "room":
                    room_ids.append(node["id"])
                if node.get("type") == "access":
                    access_ids.add(node["id"])
            all_edges.extend(floor_data["edges"])
        all_edges.extend(data.get("inter_floor_edges", []))
        if entrance not in building_node_ids:
            warnings.append(f"Missing building entrance: {entrance}")

    duplicates = sorted({node_id for node_id in all_ids if all_ids.count(node_id) > 1})
    for node_id in duplicates:
        warnings.append(f"Duplicate node id: {node_id}")

    id_set = set(all_ids)
    for edge in all_edges:
        if edge["source"] not in id_set:
            warnings.append(f"Missing edge source: {edge['source']}")
        if edge["target"] not in id_set:
            warnings.append(f"Missing edge target: {edge['target']}")
        if float(edge.get("distance", 0)) <= 0:
            warnings.append(f"Invalid edge distance: {edge['source']} -> {edge['target']}")

    for room_id in room_ids:
        access_id = f"{room_id}-ACCESS"
        if access_id not in access_ids:
            warnings.append(f"Room missing access node: {room_id}")

    graph = load_all_graphs()
    if graph.number_of_nodes() > 0 and not nx.is_connected(graph):
        warnings.append("Global graph is not connected")

    for start, end in SAMPLES:
        try:
            shortest_path(graph, start, end)
        except (nx.NetworkXNoPath, nx.NodeNotFound) as exc:
            warnings.append(f"Shortest path failed for {start} -> {end}: {exc}")

    return warnings


def main() -> None:
    warnings = validate()
    if not warnings:
        print("All graph validations passed.")
        return
    for warning in warnings:
        print(f"Warning: {warning}")


if __name__ == "__main__":
    main()
