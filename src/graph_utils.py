from __future__ import annotations

import json
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]
GRAPH_DIR = ROOT / "data" / "graphs"


def graph_path(filename: str) -> str:
    staged = GRAPH_DIR / filename
    return str(staged) if staged.exists() else str(ROOT / filename)


BUILDING_FILES = {
    "A": graph_path("building_a_graph.json"),
    "B": graph_path("building_b_graph.json"),
    "C": graph_path("building_c_graph.json"),
    "D": graph_path("building_d_graph.json"),
    "E": graph_path("building_e_graph.json"),
}
CAMPUS_FILE = graph_path("campus_graph.json")


def load_json(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def add_edge(graph: nx.Graph, edge: dict) -> None:
    if not edge.get("accessible", True):
        return
    if edge["source"] not in graph or edge["target"] not in graph:
        return
    graph.add_edge(
        edge["source"],
        edge["target"],
        distance=float(edge["distance"]),
        type=edge.get("type", ""),
        accessible=edge.get("accessible", True),
        notes=edge.get("notes", ""),
    )


def add_building_graph(graph: nx.Graph, data: dict) -> None:
    for floor_key, floor_data in data["floors"].items():
        for node in floor_data.get("nodes", []):
            if node.get("accessible", True):
                graph.add_node(node["id"], **node)
    for floor_data in data["floors"].values():
        for edge in floor_data.get("edges", []):
            add_edge(graph, edge)
    for edge in data.get("inter_floor_edges", []):
        add_edge(graph, edge)


def load_all_graphs() -> nx.Graph:
    graph = nx.Graph()
    campus = load_json(CAMPUS_FILE)

    for node in campus.get("nodes", []):
        if node.get("accessible", True):
            graph.add_node(node["id"], **node)
    for edge in campus.get("edges", []):
        add_edge(graph, edge)

    for building_file in BUILDING_FILES.values():
        if Path(building_file).exists():
            add_building_graph(graph, load_json(building_file))

    for edge in campus.get("building_entry_edges", []):
        add_edge(graph, edge)

    return graph


def shortest_path(graph: nx.Graph, start: str, end: str) -> tuple[list[str], float]:
    path = nx.shortest_path(graph, start, end, weight="distance")
    distance = nx.shortest_path_length(graph, start, end, weight="distance")
    return path, float(distance)
