from __future__ import annotations

import argparse
import html
import json
import math
from pathlib import Path

from graph_utils import load_all_graphs


ROOT = Path(__file__).resolve().parents[1]
BUILDING_ORDER = ["A", "B", "C", "D", "E"]
TYPE_COLORS = {
    "gate": "#2563eb",
    "garage": "#7c2d12",
    "building_access": "#0891b2",
    "walkway": "#64748b",
    "intersection": "#f59e0b",
    "canteen": "#9333ea",
    "room": "#475569",
    "access": "#0f766e",
    "corridor": "#64748b",
    "junction": "#f97316",
    "stair": "#16a34a",
    "elevator": "#22c55e",
    "wc": "#a16207",
    "entrance": "#dc2626",
    "library": "#be185d",
    "storage": "#78716c",
}


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def load_json(path: str | Path):
    return json.loads(resolve_path(path).read_text(encoding="utf-8"))


def panel_for_node(node_id: str, attrs: dict) -> str:
    if node_id.startswith("UIT-"):
        return "Campus"
    building = attrs.get("building") or (node_id[0] if node_id else "?")
    floor = attrs.get("floor")
    if floor is None:
        return f"Building {building}"
    return f"{building} Floor {floor}"


def panel_layout(graph) -> dict[str, dict]:
    panels = {
        "Campus": {"x": 80, "y": 80, "scale": 1.0, "w": 1000, "h": 1000, "title": "Campus"},
    }
    cell_w = 620
    cell_h = 620
    start_x = 1180
    start_y = 80
    columns = 4
    floor_panels = []
    for building in BUILDING_ORDER:
        floors = sorted({
            int(attrs.get("floor"))
            for _, attrs in graph.nodes(data=True)
            if attrs.get("building") == building and attrs.get("floor") is not None
        })
        for floor in floors:
            floor_panels.append((building, floor))
    for index, (building, floor) in enumerate(floor_panels):
        col = index % columns
        row = index // columns
        key = f"{building} Floor {floor}"
        panels[key] = {
            "x": start_x + col * cell_w,
            "y": start_y + row * cell_h,
            "scale": 0.55,
            "w": 550,
            "h": 550,
            "title": key,
        }
    return panels


def node_positions(graph, panels: dict[str, dict]) -> dict[str, tuple[float, float]]:
    positions = {}
    for node_id, attrs in graph.nodes(data=True):
        panel_name = panel_for_node(node_id, attrs)
        panel = panels.get(panel_name, panels["Campus"])
        x = float(attrs.get("x", 0))
        y = float(attrs.get("y", 0))
        positions[node_id] = (panel["x"] + x * panel["scale"], panel["y"] + y * panel["scale"])
    return positions


def normalize_edge_id_local(source: str, target: str) -> str:
    return "__".join(sorted([source, target]))


def traffic_maps(node_traffic_path: str | Path, edge_traffic_path: str | Path) -> tuple[dict, dict]:
    node_items = load_json(node_traffic_path)
    edge_items = load_json(edge_traffic_path)
    node_map = {item.get("node_id") or item.get("id"): item for item in node_items}
    edge_map = {item.get("edge_id") or item.get("id"): item for item in edge_items}
    return node_map, edge_map


def metric_value(item: dict | None, metric: str) -> float:
    if not item:
        return 0.0
    if metric == "stress":
        return float(item.get("stress_traffic", 0))
    return float(item.get("total_count", item.get("weekly_count", 0)))


def heat_color(value: float, max_value: float) -> str:
    if max_value <= 0 or value <= 0:
        return "#e5e7eb"
    ratio = min(1.0, value / max_value)
    stops = [
        (0.00, (229, 231, 235)),
        (0.10, (254, 240, 138)),
        (0.35, (251, 146, 60)),
        (0.65, (239, 68, 68)),
        (1.00, (126, 34, 206)),
    ]
    for index in range(len(stops) - 1):
        left_pos, left = stops[index]
        right_pos, right = stops[index + 1]
        if ratio <= right_pos:
            local = (ratio - left_pos) / max(0.0001, right_pos - left_pos)
            rgb = tuple(round(left[channel] + (right[channel] - left[channel]) * local) for channel in range(3))
            return f"rgb({rgb[0]},{rgb[1]},{rgb[2]})"
    return "rgb(126,34,206)"


def node_radius(value: float, max_value: float) -> float:
    if max_value <= 0:
        return 4.0
    return 4.0 + 18.0 * math.sqrt(value / max_value)


def edge_width(value: float, max_value: float) -> float:
    if max_value <= 0:
        return 1.2
    return 1.0 + 12.0 * math.sqrt(value / max_value)


def svg_title(lines: list[str]) -> str:
    return "<title>" + html.escape("\n".join(lines)) + "</title>"


def render_panels(panels: dict[str, dict]) -> str:
    items = []
    for panel in panels.values():
        items.append(
            f'<rect x="{panel["x"]}" y="{panel["y"]}" width="{panel["w"]}" height="{panel["h"]}" '
            'rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />'
        )
        items.append(
            f'<text x="{panel["x"] + 12}" y="{panel["y"] + 24}" class="panel-title">'
            f'{html.escape(panel["title"])}</text>'
        )
    return "\n".join(items)


def render_edges(graph, positions: dict, edge_map: dict, metric: str, max_edge: float) -> str:
    items = []
    for source, target, attrs in graph.edges(data=True):
        if source not in positions or target not in positions:
            continue
        edge_id = normalize_edge_id_local(source, target)
        traffic = edge_map.get(edge_id)
        value = metric_value(traffic, metric)
        x1, y1 = positions[source]
        x2, y2 = positions[target]
        color = heat_color(value, max_edge)
        width = edge_width(value, max_edge)
        opacity = 0.28 if value <= 0 else 0.78
        tooltip = [
            f"EDGE {edge_id}",
            f"{source} -> {target}",
            f"weekly traffic: {int(metric_value(traffic, 'traffic'))}",
            f"stress traffic: {int(metric_value(traffic, 'stress'))}",
            f"type: {attrs.get('type', '')}",
            f"distance: {attrs.get('distance', '')}",
        ]
        items.append(
            f'<line class="edge" data-id="{html.escape(edge_id)}" data-value="{value}" '
            f'x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width:.2f}" stroke-opacity="{opacity}">'
            f'{svg_title(tooltip)}</line>'
        )
    return "\n".join(items)


def render_nodes(graph, positions: dict, node_map: dict, metric: str, max_node: float) -> str:
    items = []
    for node_id, attrs in graph.nodes(data=True):
        if node_id not in positions:
            continue
        traffic = node_map.get(node_id)
        value = metric_value(traffic, metric)
        x, y = positions[node_id]
        color = heat_color(value, max_node)
        base_color = TYPE_COLORS.get(attrs.get("type"), "#334155")
        radius = node_radius(value, max_node)
        tooltip = [
            f"NODE {node_id}",
            f"label: {attrs.get('label', '')}",
            f"type: {attrs.get('type', '')}",
            f"building: {attrs.get('building', '')}",
            f"floor: {attrs.get('floor', '')}",
            f"weekly traffic: {int(metric_value(traffic, 'traffic'))}",
            f"stress traffic: {int(metric_value(traffic, 'stress'))}",
        ]
        items.append(
            f'<circle class="node" data-id="{html.escape(node_id)}" data-value="{value}" '
            f'cx="{x:.1f}" cy="{y:.1f}" r="{radius:.2f}" fill="{color}" '
            f'stroke="{base_color}" stroke-width="2" fill-opacity="{0.35 if value <= 0 else 0.92}">'
            f'{svg_title(tooltip)}</circle>'
        )
        if value > 0 and radius >= 12:
            items.append(
                f'<text class="node-label" x="{x + radius + 3:.1f}" y="{y + 4:.1f}">'
                f'{html.escape(node_id)}</text>'
            )
    return "\n".join(items)


def render_top_lists(node_map: dict, edge_map: dict, limit: int = 12) -> str:
    top_nodes = sorted(node_map.values(), key=lambda item: item.get("total_count", 0), reverse=True)[:limit]
    top_edges = sorted(edge_map.values(), key=lambda item: item.get("total_count", 0), reverse=True)[:limit]
    node_rows = "".join(
        f"<tr><td>{html.escape(item.get('node_id') or item.get('id'))}</td><td>{item.get('total_count', 0)}</td><td>{item.get('stress_traffic', 0)}</td></tr>"
        for item in top_nodes
    )
    edge_rows = "".join(
        f"<tr><td>{html.escape(item.get('edge_id') or item.get('id'))}</td><td>{item.get('total_count', 0)}</td><td>{item.get('stress_traffic', 0)}</td></tr>"
        for item in top_edges
    )
    return f"""
    <section class="tables">
      <div>
        <h2>Top weekly nodes</h2>
        <table><thead><tr><th>Node</th><th>Traffic</th><th>Stress</th></tr></thead><tbody>{node_rows}</tbody></table>
      </div>
      <div>
        <h2>Top weekly edges</h2>
        <table><thead><tr><th>Edge</th><th>Traffic</th><th>Stress</th></tr></thead><tbody>{edge_rows}</tbody></table>
      </div>
    </section>
    """


def render_html(graph, node_map: dict, edge_map: dict, metric: str) -> str:
    panels = panel_layout(graph)
    positions = node_positions(graph, panels)
    width = max(panel["x"] + panel["w"] for panel in panels.values()) + 120
    height = max(panel["y"] + panel["h"] for panel in panels.values()) + 120
    max_node = max([metric_value(item, metric) for item in node_map.values()] + [0])
    max_edge = max([metric_value(item, metric) for item in edge_map.values()] + [0])
    graph_node_count = graph.number_of_nodes()
    graph_edge_count = graph.number_of_edges()
    observed_node_count = len(node_map)
    observed_edge_count = len(edge_map)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>UIT Weekly Graph Heatmap</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #0f172a;
      color: #e2e8f0;
    }}
    header {{
      position: sticky;
      top: 0;
      z-index: 2;
      padding: 14px 18px;
      background: rgba(15, 23, 42, 0.96);
      border-bottom: 1px solid #334155;
    }}
    h1 {{ margin: 0 0 8px; font-size: 20px; }}
    .meta {{ display: flex; gap: 18px; flex-wrap: wrap; color: #cbd5e1; font-size: 13px; }}
    .legend {{ display: flex; align-items: center; gap: 8px; margin-top: 10px; font-size: 12px; color: #cbd5e1; }}
    .gradient {{ width: 240px; height: 12px; border-radius: 999px; background: linear-gradient(90deg, #e5e7eb, #fef08a, #fb923c, #ef4444, #7e22ce); }}
    .scroll {{
      overflow: auto;
      height: 78vh;
      background: #e2e8f0;
      border-bottom: 1px solid #334155;
    }}
    svg {{
      display: block;
      background: #e2e8f0;
    }}
    .panel-title {{
      font-size: 16px;
      font-weight: 700;
      fill: #334155;
    }}
    .node-label {{
      font-size: 9px;
      fill: #0f172a;
      paint-order: stroke;
      stroke: #f8fafc;
      stroke-width: 3px;
      stroke-linejoin: round;
    }}
    .edge:hover {{ stroke: #111827; stroke-opacity: 1; }}
    .node:hover {{ stroke: #111827; stroke-width: 4; }}
    .tables {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap: 18px;
      padding: 18px;
    }}
    h2 {{ margin: 0 0 10px; font-size: 16px; }}
    table {{ width: 100%; border-collapse: collapse; background: #111827; font-size: 12px; }}
    th, td {{ padding: 8px; border-bottom: 1px solid #334155; text-align: left; vertical-align: top; }}
    th {{ color: #93c5fd; }}
    td:first-child {{ word-break: break-all; }}
  </style>
</head>
<body>
  <header>
    <h1>UIT weekly graph heatmap</h1>
    <div class="meta">
      <span>Metric: <strong>{html.escape(metric)}</strong></span>
      <span>Graph nodes: <strong>{graph_node_count}</strong></span>
      <span>Graph edges: <strong>{graph_edge_count}</strong></span>
      <span>Observed nodes: <strong>{observed_node_count}</strong></span>
      <span>Observed edges: <strong>{observed_edge_count}</strong></span>
      <span>Max node: <strong>{int(max_node)}</strong></span>
      <span>Max edge: <strong>{int(max_edge)}</strong></span>
    </div>
    <div class="legend"><span>low / zero</span><div class="gradient"></div><span>high</span><span>Hover nodes/edges for exact counts. Scroll horizontally and vertically to inspect all floors.</span></div>
  </header>
  <main>
    <div class="scroll">
      <svg width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="Weekly graph heatmap">
        {render_panels(panels)}
        {render_edges(graph, positions, edge_map, metric, max_edge)}
        {render_nodes(graph, positions, node_map, metric, max_node)}
      </svg>
    </div>
    {render_top_lists(node_map, edge_map)}
  </main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--node-traffic", default="outputs/node_1_2/node_traffic.json")
    parser.add_argument("--edge-traffic", default="outputs/node_1_2/edge_traffic.json")
    parser.add_argument("--metric", choices=["traffic", "stress"], default="traffic")
    parser.add_argument("--output", default="outputs/heatmaps/weekly_graph_heatmap.html")
    args = parser.parse_args()

    graph = load_all_graphs()
    node_map, edge_map = traffic_maps(args.node_traffic, args.edge_traffic)
    output = resolve_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_html(graph, node_map, edge_map, args.metric), encoding="utf-8")
    print(f"Saved {output}")
    print(f"Graph nodes: {graph.number_of_nodes()}")
    print(f"Graph edges: {graph.number_of_edges()}")
    print(f"Observed traffic nodes: {len(node_map)}")
    print(f"Observed traffic edges: {len(edge_map)}")


if __name__ == "__main__":
    main()
