from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def load_json(path: Path):
    return json.loads(resolve_path(path).read_text(encoding="utf-8"))


def validate_output_dir(output_dir: str) -> dict:
    base = resolve_path(output_dir)
    required = [
        "student_agents.json",
        "student_schedules.json",
        "generated_routes.json",
        "node_traffic.json",
        "edge_traffic.json",
        "heatmap_data.json",
        "simulation_summary.json",
        "simulation_warnings.json",
        "simulation_validation_report.json",
    ]
    errors = []
    for filename in required:
        if not (base / filename).exists():
            errors.append({"type": "MISSING_OUTPUT_FILE", "message": filename})

    if errors:
        return {"output_dir": output_dir, "errors": errors, "warnings": []}

    agents = load_json(base / "student_agents.json")
    routes = load_json(base / "generated_routes.json")
    node_traffic = load_json(base / "node_traffic.json")
    edge_traffic = load_json(base / "edge_traffic.json")
    report = load_json(base / "simulation_validation_report.json")

    warnings = []
    if len(agents) == 0:
        errors.append({"type": "NO_AGENTS", "message": "No student agents generated."})
    if len(routes) == 0:
        warnings.append({"type": "NO_ROUTES", "message": "No routes generated."})
    for item in node_traffic + edge_traffic:
        if item.get("total_count", 0) < 0:
            errors.append({"type": "NEGATIVE_TRAFFIC", "message": item.get("id") or item.get("edge_id")})
    errors.extend(report.get("errors", []))
    warnings.extend(report.get("warnings", []))
    return {
        "output_dir": output_dir,
        "total_agents": len(agents),
        "total_routes": len(routes),
        "total_node_traffic_items": len(node_traffic),
        "total_edge_traffic_items": len(edge_traffic),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="outputs/node_1_2")
    args = parser.parse_args()
    result = validate_output_dir(args.output_dir)
    output_path = resolve_path(args.output_dir) / "simulation_output_validation_report.json"
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {output_path}")
    print(f"Errors: {len(result['errors'])}")


if __name__ == "__main__":
    main()
