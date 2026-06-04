from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "data" / "graphs" / "building_a_graph.json"
TYPE_STYLES = {
    "room": {"color": "#4C78A8", "shape": "o", "size": 160},
    "access": {"color": "#72B7B2", "shape": "o", "size": 80},
    "corridor": {"color": "#8C8C8C", "shape": "o", "size": 90},
    "junction": {"color": "#F58518", "shape": "o", "size": 260},
    "stair": {"color": "#54A24B", "shape": "s", "size": 260},
    "elevator": {"color": "#59A14F", "shape": "D", "size": 240},
    "wc": {"color": "#9D755D", "shape": "p", "size": 200},
    "entrance": {"color": "#E45756", "shape": "^", "size": 280},
    "library": {"color": "#B279A2", "shape": "*", "size": 520},
    "storage": {"color": "#B8B8B8", "shape": "X", "size": 260},
}


def load_graph_data(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def _all_nodes(data: dict) -> list[dict]:
    nodes = []
    for floor_data in data["floors"].values():
        nodes.extend(floor_data.get("nodes", []))
    return nodes


def _floor_edges(data: dict, floor: int) -> list[dict]:
    return data["floors"][str(floor)].get("edges", [])


def build_graph(data: dict, floor: int | None = None, include_inaccessible: bool = False) -> nx.Graph:
    graph = nx.Graph()

    if floor is None:
        floor_keys = sorted(data["floors"].keys(), key=int)
    else:
        floor_keys = [str(floor)]

    for floor_key in floor_keys:
        for node in data["floors"][floor_key].get("nodes", []):
            if include_inaccessible or node.get("accessible", True):
                graph.add_node(node["id"], **node)

    edges = []
    for floor_key in floor_keys:
        edges.extend(data["floors"][floor_key].get("edges", []))
    if floor is None:
        edges.extend(data.get("inter_floor_edges", []))

    for edge in edges:
        if not (include_inaccessible or edge.get("accessible", True)):
            continue
        if edge["source"] not in graph or edge["target"] not in graph:
            continue
        graph.add_edge(
            edge["source"],
            edge["target"],
            distance=float(edge["distance"]),
            type=edge["type"],
            accessible=edge.get("accessible", True),
            notes=edge.get("notes", ""),
        )

    return graph


def validate_graph(data: dict) -> list[str]:
    warnings = []
    node_ids = []

    for node in _all_nodes(data):
        node_ids.append(node["id"])
        for field in ["id", "label", "type", "floor", "x", "y", "zone", "accessible"]:
            if field not in node:
                warnings.append(f"Node {node.get('id', '<missing id>')} is missing field: {field}")

    duplicates = sorted({node_id for node_id in node_ids if node_ids.count(node_id) > 1})
    for node_id in duplicates:
        warnings.append(f"Duplicate node id: {node_id}")

    node_id_set = set(node_ids)
    all_edges = []
    for floor in data["floors"]:
        all_edges.extend(data["floors"][floor].get("edges", []))
    all_edges.extend(data.get("inter_floor_edges", []))

    for edge in all_edges:
        source = edge.get("source")
        target = edge.get("target")
        if source not in node_id_set:
            warnings.append(f"Edge source does not exist: {source}")
        if target not in node_id_set:
            warnings.append(f"Edge target does not exist: {target}")
        if float(edge.get("distance", 0)) <= 0:
            warnings.append(f"Edge has invalid distance: {source} -> {target}")

    route_graph = build_graph(data, include_inaccessible=False)
    isolated = sorted(nx.isolates(route_graph))
    for node_id in isolated:
        warnings.append(f"Accessible node is isolated: {node_id}")

    if route_graph.number_of_nodes() > 0 and not nx.is_connected(route_graph):
        warnings.append("Accessible graph is not connected")

    for node in _all_nodes(data):
        if node.get("type") != "room":
            continue
        access_id = f"{node['id']}-ACCESS"
        neighbors = set(route_graph.neighbors(node["id"])) if node["id"] in route_graph else set()
        if access_id not in node_id_set:
            warnings.append(f"Room is missing matching access node: {node['id']}")
        elif access_id not in neighbors:
            warnings.append(f"Room is not connected to its access node: {node['id']}")

    for node_id, attrs in route_graph.nodes(data=True):
        if attrs.get("type") != "access":
            continue
        neighbors = list(route_graph.neighbors(node_id))
        room_neighbors = [neighbor for neighbor in neighbors if route_graph.nodes[neighbor].get("type") == "room"]
        road_neighbors = [neighbor for neighbor in neighbors if route_graph.nodes[neighbor].get("type") != "room"]
        if len(room_neighbors) != 1:
            warnings.append(f"Access node should connect to exactly one room: {node_id}")
        if len(road_neighbors) < 2:
            warnings.append(f"Access node is not embedded in the road path: {node_id}")

    for source, target in route_graph.edges():
        source_type = route_graph.nodes[source].get("type")
        target_type = route_graph.nodes[target].get("type")
        if source_type == "room" and target_type == "room":
            warnings.append(f"Room-to-room edge should not exist: {source} -> {target}")

    return warnings


def draw_floor_graph(data: dict, floor: int, output_path: str) -> None:
    graph = build_graph(data, floor=floor, include_inaccessible=True)
    positions = {node_id: (attrs["x"], attrs["y"]) for node_id, attrs in graph.nodes(data=True)}

    fig, ax = plt.subplots(figsize=(11, 11))
    background_path = ROOT / "assets" / f"building_a_floor_{floor}.jpg"
    if background_path.exists():
        image = plt.imread(background_path)
        ax.imshow(image, extent=[0, 1000, 1000, 0], alpha=0.35)

    accessible_edges = [
        (source, target)
        for source, target, attrs in graph.edges(data=True)
        if attrs.get("accessible", True)
    ]
    blocked_edges = [
        (source, target)
        for source, target, attrs in graph.edges(data=True)
        if not attrs.get("accessible", True)
    ]
    nx.draw_networkx_edges(graph, positions, edgelist=accessible_edges, ax=ax, width=1.8, edge_color="#555555")
    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=blocked_edges,
        ax=ax,
        width=1.2,
        style="dashed",
        edge_color="#B0B0B0",
    )

    for node_type, style in TYPE_STYLES.items():
        nodes = [node for node, attrs in graph.nodes(data=True) if attrs.get("type") == node_type]
        if not nodes:
            continue
        nx.draw_networkx_nodes(
            graph,
            positions,
            nodelist=nodes,
            node_color=style["color"],
            node_shape=style["shape"],
            node_size=style["size"],
            edgecolors="#222222",
            linewidths=0.7,
            ax=ax,
        )

    labels = {node_id: attrs["label"] for node_id, attrs in graph.nodes(data=True)}
    nx.draw_networkx_labels(graph, positions, labels=labels, font_size=6, font_family="sans-serif", ax=ax)

    ax.set_title(f"Building A - Floor {floor} Graph")
    ax.set_xlim(0, 1000)
    ax.set_ylim(1000, 0)
    ax.set_aspect("equal")
    ax.grid(True, color="#E6E6E6", linewidth=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def main() -> None:
    data = load_graph_data(GRAPH_PATH)
    warnings = validate_graph(data)
    for warning in warnings:
        print(f"Warning: {warning}")

    output_dir = ROOT / "outputs" / "buildings" / "a"
    output_dir.mkdir(parents=True, exist_ok=True)
    floor_1_path = output_dir / "building_a_floor_1_graph.png"
    floor_2_path = output_dir / "building_a_floor_2_graph.png"
    draw_floor_graph(data, 1, str(floor_1_path))
    draw_floor_graph(data, 2, str(floor_2_path))
    print(f"Saved {floor_1_path}")
    print(f"Saved {floor_2_path}")


if __name__ == "__main__":
    main()
