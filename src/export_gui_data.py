import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH_DIR = ROOT / "data" / "graphs"
OUTPUT_DIR = ROOT / "outputs" / "node_1_2"
GUI_DIR = ROOT / "gui"

def main():
    GUI_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Load graphs
    campus = json.loads((GRAPH_DIR / "campus_graph.json").read_text(encoding="utf-8"))
    
    building_graphs = {}
    buildings = ["A", "B", "C", "D", "E"]
    for b in buildings:
        b_data = json.loads((GRAPH_DIR / f"building_{b.lower()}_graph.json").read_text(encoding="utf-8"))
        building_graphs[b] = b_data
        
    # 2. Build unified graph representation for input choice
    nodes = []
    edges = []
    
    # Add campus nodes
    for node in campus["nodes"]:
        node["building"] = "UIT"
        nodes.append(node)
        
    # Add campus edges
    edges.extend(campus["edges"])
    edges.extend(campus["building_entry_edges"])
    
    # Add building nodes
    for b, bg in building_graphs.items():
        for floor_key, floor_data in bg["floors"].items():
            for node in floor_data.get("nodes", []):
                node["building"] = b
                nodes.append(node)
            edges.extend(floor_data.get("edges", []))
        edges.extend(bg.get("inter_floor_edges", []))

    unified_graph = {
        "nodes": nodes,
        "edges": edges
    }
    
    # 3. Load FULL timetable to ensure 100% data integrity matching Python simulator
    timetable_full = json.loads((ROOT / "data" / "normalized" / "normalized_timetable.json").read_text(encoding="utf-8"))
    
    # 4. Load traffic counts
    node_traffic = json.loads((OUTPUT_DIR / "node_traffic.json").read_text(encoding="utf-8"))
    edge_traffic = json.loads((OUTPUT_DIR / "edge_traffic.json").read_text(encoding="utf-8"))
    
    # 5. Load ranked candidates
    ranked_candidates_path = OUTPUT_DIR / "ranked_candidates.json"
    if ranked_candidates_path.exists():
        ranked_candidates = json.loads(ranked_candidates_path.read_text(encoding="utf-8"))
    else:
        ranked_candidates = []

    # Write Javascript bundle file containing all required definitions
    js_content = f"""// Auto-generated data bundle for GUI visualization
const CAMPUS_GRAPH = {json.dumps(campus, indent=2, ensure_ascii=False)};
const BUILDING_GRAPHS = {json.dumps(building_graphs, indent=2, ensure_ascii=False)};
const DEFAULT_UNIFIED_GRAPH = {json.dumps(unified_graph, indent=2, ensure_ascii=False)};
const DEFAULT_TIMETABLE_SUBSET = {json.dumps(timetable_full, indent=2, ensure_ascii=False)};
const DEFAULT_NODE_TRAFFIC = {json.dumps(node_traffic, indent=2, ensure_ascii=False)};
const DEFAULT_EDGE_TRAFFIC = {json.dumps(edge_traffic, indent=2, ensure_ascii=False)};
const DEFAULT_RANKED_CANDIDATES = {json.dumps(ranked_candidates, indent=2, ensure_ascii=False)};
"""
    (GUI_DIR / "gui_data.js").write_text(js_content, encoding="utf-8")
    print(f"Successfully generated GUI data bundle: {GUI_DIR / 'gui_data.js'}")

if __name__ == "__main__":
    main()
