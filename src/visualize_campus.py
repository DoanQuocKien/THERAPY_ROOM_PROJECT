from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path

from graph_utils import CAMPUS_FILE, load_json


ROOT = Path(__file__).resolve().parents[1]


TYPE_COLORS = {
    "gate": "#E45756",
    "garage": "#7F4E2F",
    "building_access": "#4C78A8",
    "walkway": "#72B7B2",
    "intersection": "#F58518",
    "canteen": "#B279A2",
    "outdoor": "#8C8C8C",
}


def main() -> None:
    data = load_json(CAMPUS_FILE)
    graph = nx.Graph()
    for node in data["nodes"]:
        graph.add_node(node["id"], **node)
    for edge in data["edges"]:
        graph.add_edge(edge["source"], edge["target"], distance=edge["distance"], type=edge["type"])

    positions = {node_id: (attrs["x"], attrs["y"]) for node_id, attrs in graph.nodes(data=True)}
    fig, ax = plt.subplots(figsize=(10, 10))
    nx.draw_networkx_edges(graph, positions, ax=ax, edge_color="#666666", width=1.8)

    for node_type, color in TYPE_COLORS.items():
        nodes = [node_id for node_id, attrs in graph.nodes(data=True) if attrs.get("type") == node_type]
        if nodes:
            nx.draw_networkx_nodes(graph, positions, nodelist=nodes, node_color=color, node_size=280, edgecolors="#222222", ax=ax)

    labels = {node_id: attrs["label"] for node_id, attrs in graph.nodes(data=True)}
    nx.draw_networkx_labels(graph, positions, labels=labels, font_size=7, ax=ax)
    ax.set_title("UIT Campus Graph")
    ax.set_xlim(0, 1000)
    ax.set_ylim(1000, 0)
    ax.set_aspect("equal")
    ax.grid(True, color="#E6E6E6", linewidth=0.5)
    fig.tight_layout()
    output_dir = ROOT / "outputs" / "campus"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "campus_graph.png"
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
