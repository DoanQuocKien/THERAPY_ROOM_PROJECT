from __future__ import annotations

import matplotlib
from pathlib import Path

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

from visualize_building_a import GRAPH_PATH, TYPE_STYLES, build_graph, load_graph_data, validate_graph


ROOT = Path(__file__).resolve().parents[1]
START_NODE = "A-F1-LIBRARY-CENTER"
END_NODE = "A-F2-RIGHT-ROOM-01"


def find_shortest_path(graph: nx.Graph, start: str, end: str) -> tuple[list[str], float]:
    path = nx.shortest_path(graph, start, end, weight="distance")
    total_distance = nx.shortest_path_length(graph, start, end, weight="distance")
    return path, float(total_distance)


def _combined_positions(graph: nx.Graph) -> dict[str, tuple[float, float]]:
    positions = {}
    for node_id, attrs in graph.nodes(data=True):
        floor_offset = (attrs["floor"] - 1) * 1100
        positions[node_id] = (attrs["x"] + floor_offset, attrs["y"])
    return positions


def draw_shortest_path(graph: nx.Graph, path: list[str], output_path: str) -> None:
    positions = _combined_positions(graph)
    path_edges = set(zip(path, path[1:]))
    path_edges.update({(target, source) for source, target in path_edges})
    normal_edges = [(source, target) for source, target in graph.edges() if (source, target) not in path_edges]
    highlighted_edges = [(source, target) for source, target in graph.edges() if (source, target) in path_edges]

    fig, ax = plt.subplots(figsize=(18, 8))
    nx.draw_networkx_edges(graph, positions, edgelist=normal_edges, edge_color="#C7C7C7", width=1.2, ax=ax)
    nx.draw_networkx_edges(graph, positions, edgelist=highlighted_edges, edge_color="#D62728", width=3.2, ax=ax)

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

    nx.draw_networkx_nodes(
        graph,
        positions,
        nodelist=path,
        node_color="#D62728",
        node_size=320,
        edgecolors="#111111",
        linewidths=1.0,
        ax=ax,
    )
    labels = {node_id: attrs["label"] for node_id, attrs in graph.nodes(data=True)}
    nx.draw_networkx_labels(graph, positions, labels=labels, font_size=6, ax=ax)

    ax.text(500, 30, "Floor 1", fontsize=14, fontweight="bold", ha="center")
    ax.text(1600, 30, "Floor 2", fontsize=14, fontweight="bold", ha="center")
    ax.axvline(1050, color="#DDDDDD", linewidth=1.0)
    ax.set_title(f"Shortest Path: {path[0]} to {path[-1]}")
    ax.set_xlim(-50, 2150)
    ax.set_ylim(1000, 0)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def main() -> None:
    data = load_graph_data(GRAPH_PATH)
    warnings = validate_graph(data)
    for warning in warnings:
        print(f"Warning: {warning}")

    graph = build_graph(data, floor=None, include_inaccessible=False)
    path, total_distance = find_shortest_path(graph, START_NODE, END_NODE)

    print("Shortest path:")
    for index, node_id in enumerate(path):
        prefix = "   " if index == 0 else "-> "
        print(f"{prefix}{node_id}")
    print(f"\nTotal distance: {total_distance:.1f}")

    output_dir = ROOT / "outputs" / "paths"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "shortest_path_highlight.png"
    draw_shortest_path(graph, path, str(output_path))
    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
