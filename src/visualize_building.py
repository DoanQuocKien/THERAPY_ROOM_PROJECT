from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

from graph_utils import BUILDING_FILES, load_json
from visualize_building_a import TYPE_STYLES


ROOT = Path(__file__).resolve().parents[1]


def draw_floor(data: dict, building: str, floor_key: str) -> None:
    floor_data = data["floors"][floor_key]
    graph = nx.Graph()
    for node in floor_data["nodes"]:
        graph.add_node(node["id"], **node)
    for edge in floor_data["edges"]:
        if edge["source"] in graph and edge["target"] in graph:
            graph.add_edge(edge["source"], edge["target"], **edge)

    positions = {node_id: (attrs["x"], attrs["y"]) for node_id, attrs in graph.nodes(data=True)}
    fig, ax = plt.subplots(figsize=(12, 8))
    nx.draw_networkx_edges(graph, positions, edge_color="#666666", width=1.4, ax=ax)
    for node_type, style in TYPE_STYLES.items():
        nodes = [node_id for node_id, attrs in graph.nodes(data=True) if attrs.get("type") == node_type]
        if nodes:
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
    nx.draw_networkx_labels(graph, positions, labels=labels, font_size=6, ax=ax)
    ax.set_title(f"Building {building} - Floor {floor_key}")
    ax.set_xlim(0, 1000)
    ax.set_ylim(1000, 0)
    ax.set_aspect("equal")
    ax.grid(True, color="#E6E6E6", linewidth=0.5)
    fig.tight_layout()
    output_dir = ROOT / "outputs" / "buildings" / building.lower()
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"building_{building.lower()}_floor_{floor_key}_graph.png"
    fig.savefig(output, dpi=180)
    plt.close(fig)
    print(f"Saved {output}")


def main() -> None:
    building = sys.argv[1].upper() if len(sys.argv) > 1 else "B"
    if building not in BUILDING_FILES:
        raise SystemExit(f"Unknown building: {building}")
    data = load_json(BUILDING_FILES[building])
    for floor_key in sorted(data["floors"].keys(), key=lambda value: int(value) if value.isdigit() else -1):
        draw_floor(data, building, floor_key)


if __name__ == "__main__":
    main()
