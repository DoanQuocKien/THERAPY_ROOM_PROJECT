import json
import argparse
import sys
from pathlib import Path
import networkx as nx
from graph_utils import load_all_graphs, shortest_path

ROOT = Path(__file__).resolve().parents[1]

# Default candidate rooms to evaluate
DEFAULT_CANDIDATES = [
    "A-F1-TOP-ROOM-01",
    "B1.02",
    "C103",
    "E2.01",
    "A-F2-RIGHT-ROOM-01"
]

def load_json(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)

def get_node_traffic(traffic_path: Path) -> dict[str, float]:
    data = load_json(traffic_path)
    # Map node id to its total count
    return {item["id"]: float(item["total_count"]) for item in data}

def evaluate_accessibility(graph: nx.Graph, candidates: list[str], traffic_map: dict[str, float]) -> dict[str, float]:
    """
    Accessibility indicator computation (P3).
    WTC(r) = sum_{v_c in V_core} Traffic(v_c) * d(v_c, r) / sum Traffic(v_c)
    """
    # Core activity nodes are room nodes with positive traffic
    core_nodes = [
        node_id for node_id, attrs in graph.nodes(data=True)
        if attrs.get("type") == "room" and traffic_map.get(node_id, 0) > 0
    ]
    
    if not core_nodes:
        # Fallback to all room nodes if no traffic is generated
        core_nodes = [node_id for node_id, attrs in graph.nodes(data=True) if attrs.get("type") == "room"]
        
    wtc_scores = {}
    for r in candidates:
        total_weighted_dist = 0.0
        total_traffic = 0.0
        for v_c in core_nodes:
            traffic = traffic_map.get(v_c, 1.0) # default to 1 if no traffic data
            try:
                # Calculate shortest path distance
                _, dist = shortest_path(graph, v_c, r)
                total_weighted_dist += traffic * dist
                total_traffic += traffic
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue
        wtc_scores[r] = total_weighted_dist / total_traffic if total_traffic > 0 else 9999.0

    # Normalize accessibility: min-max normalization where lower WTC is better
    wtc_vals = list(wtc_scores.values())
    wtc_min = min(wtc_vals)
    wtc_max = max(wtc_vals)
    
    acc_indicators = {}
    for r, wtc in wtc_scores.items():
        if wtc_max == wtc_min:
            acc_indicators[r] = 1.0
        else:
            acc_indicators[r] = (wtc_max - wtc) / (wtc_max - wtc_min)
            
    return acc_indicators, wtc_scores

def get_node_building(node_id: str, attrs: dict) -> str | None:
    if attrs.get("building"):
        return attrs["building"]
    if node_id.startswith("UIT-"):
        return "UIT"
    # Fallback to ID prefix
    for prefix in ["A-", "B", "C", "D", "E"]:
        if node_id.startswith(prefix):
            return prefix.replace("-", "")
    return None

def get_zone_nodes(graph: nx.Graph, access_node: str, max_dist: float) -> dict[str, float]:
    """
    BFS helper to find nodes on the same building floor within max_dist.
    """
    if access_node not in graph:
        return {}
        
    start_attrs = graph.nodes[access_node]
    start_building = get_node_building(access_node, start_attrs)
    start_floor = start_attrs.get("floor")
    
    # Run a simple dijkstra to find all reachable nodes on same floor within distance limit
    lengths = nx.single_source_dijkstra_path_length(graph, access_node, cutoff=max_dist, weight="distance")
    
    # Filter nodes to keep them on the same floor/building to prevent visual bleeding
    filtered_lengths = {}
    for n, dist in lengths.items():
        n_attrs = graph.nodes[n]
        n_building = get_node_building(n, n_attrs)
        
        # Safely compare building and floor attributes
        same_building = (n_building == start_building)
        same_floor = (str(n_attrs.get("floor")) == str(start_floor))
        
        if same_building and same_floor:
            filtered_lengths[n] = dist
            
    return filtered_lengths

def evaluate_visibility(graph: nx.Graph, candidates: list[str], traffic_map: dict[str, float]) -> dict[str, float]:
    """
    Visibility indicator computation (P4).
    Exposure zone is within 10m of access node.
    RawVisibility(r) = sum_{v in EZ(r)} Traffic(v) * lambda(v, r)
    lambda = 1 / (1 + 0.1 * d)
    """
    raw_vis = {}
    for r in candidates:
        access_node = f"{r}-ACCESS"
        if access_node not in graph:
            access_node = r # Fallback to node itself if access node not configured
            
        ez = get_zone_nodes(graph, access_node, max_dist=10.0)
        score = 0.0
        for v, d in ez.items():
            traffic = traffic_map.get(v, 0.0)
            lam = 1.0 / (1.0 + 0.1 * d)
            score += traffic * lam
        raw_vis[r] = score

    # Normalize visibility: min-max normalization where higher RawVisibility is better
    vis_vals = list(raw_vis.values())
    vis_min = min(vis_vals)
    vis_max = max(vis_vals)
    
    vis_indicators = {}
    for r, val in raw_vis.items():
        if vis_max == vis_min:
            vis_indicators[r] = 1.0
        else:
            vis_indicators[r] = (val - vis_min) / (vis_max - vis_min)
            
    return vis_indicators, raw_vis

def evaluate_privacy(graph: nx.Graph, candidates: list[str], traffic_map: dict[str, float]) -> dict[str, float]:
    """
    Privacy indicator computation (P5).
    Sensitive zone is within 3m of access node.
    RawExposureRisk(r) = sum_{v in SZ(r)} Traffic(v)
    """
    raw_risk = {}
    for r in candidates:
        access_node = f"{r}-ACCESS"
        if access_node not in graph:
            access_node = r
            
        sz = get_zone_nodes(graph, access_node, max_dist=3.0)
        score = sum(traffic_map.get(v, 0.0) for v in sz)
        raw_risk[r] = score

    # Normalize privacy: inverse min-max normalization where lower risk is better
    risk_vals = list(raw_risk.values())
    risk_min = min(risk_vals)
    risk_max = max(risk_vals)
    
    priv_indicators = {}
    for r, val in raw_risk.items():
        if risk_max == risk_min:
            priv_indicators[r] = 1.0
        else:
            priv_indicators[r] = (risk_max - val) / (risk_max - risk_min)
            
    return priv_indicators, raw_risk

def generate_trade_off_report(room: str, acc: float, vis: float, priv: float, wtc: float, raw_vis: float, risk: float) -> str:
    explanations = []
    
    # Privacy warning rules
    if priv < 0.3:
        explanations.append(
            f"Mật độ giao thông trước phòng {room} rất lớn (Exposure Risk thô: {risk:.1f} lượt). "
            "Yêu cầu lắp đặt thêm vách cách âm, rèm cửa che tầm nhìn và biển báo hạn chế tụ tập trước cửa nếu lựa chọn vị trí này."
        )
    # Accessibility warning rules
    if acc < 0.3:
        explanations.append(
            f"Vị trí phòng {room} cách xa giảng đường chính (nỗ lực đi bộ trung bình có trọng số WTC: {wtc:.1f}m). "
            "Cần thiết lập sơ đồ hướng dẫn tại sảnh chính các tòa nhà để sinh viên dễ dàng định vị lối đi."
        )
    # Balanced option rules
    if 0.5 <= acc <= 0.8 and 0.5 <= vis <= 0.8 and 0.5 <= priv <= 0.8:
        explanations.append(
            f"Đây là vị trí cân bằng rất tốt, đáp ứng hài hòa cả 3 tiêu chí tiếp cận (Acc: {acc:.2f}), "
            f"riêng tư (Priv: {priv:.2f}) và nhận diện tự nhiên (Vis: {vis:.2f})."
        )
        
    if not explanations:
        explanations.append(
            f"Phòng {room} có điểm tiếp cận {acc:.2f}, độ hiển thị {vis:.2f}, độ riêng tư {priv:.2f}. "
            f"WTC đi bộ: {wtc:.1f}m, Visibility thô: {raw_vis:.1f}, Risk thô: {risk:.1f}."
        )
        
    return " ".join(explanations)

def main() -> None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    parser = argparse.ArgumentParser(description="CS117 Psychological Counseling Room Candidate Ranking Engine")
    parser.add_argument("--traffic-dir", default="outputs/node_1_2", help="Directory containing node_traffic.json")
    parser.add_argument("--candidates-file", help="Path to JSON file containing candidate list (D3)")
    parser.add_argument("--output", default="outputs/node_1_2/ranked_candidates.json", help="Path to save ranked JSON output")
    parser.add_argument("--w-acc", type=float, default=0.35, help="Accessibility weight")
    parser.add_argument("--w-vis", type=float, default=0.15, help="Visibility weight")
    parser.add_argument("--w-priv", type=float, default=0.50, help="Privacy weight")
    
    args = parser.parse_args()
    
    # Load candidates (D3)
    if args.candidates_file:
        candidates = load_json(args.candidates_file)
    else:
        candidates = DEFAULT_CANDIDATES
        
    print(f"Loaded {len(candidates)} candidates: {candidates}")
    
    # Validate weights
    weight_sum = args.w_acc + args.w_vis + args.w_priv
    if not (0.99 <= weight_sum <= 1.01):
        print(f"Warning: Weights do not sum to 1.0 (Sum={weight_sum:.4f}). Normalizing...")
        w_acc = args.w_acc / weight_sum
        w_vis = args.w_vis / weight_sum
        w_priv = args.w_priv / weight_sum
    else:
        w_acc = args.w_acc
        w_vis = args.w_vis
        w_priv = args.w_priv
        
    print(f"Using weights: w_acc={w_acc:.2f}, w_vis={w_vis:.2f}, w_priv={w_priv:.2f}")

    # Load graphs and traffic
    graph = load_all_graphs()
    traffic_path = ROOT / args.traffic_dir / "node_traffic.json"
    if not traffic_path.exists():
        print(f"Error: Traffic file {traffic_path} not found. Please run the student simulation first.")
        return
        
    traffic_map = get_node_traffic(traffic_path)
    
    # Verify candidate rooms existence in graph
    valid_candidates = []
    for r in candidates:
        if r in graph:
            valid_candidates.append(r)
        else:
            print(f"Warning: Candidate {r} not found in graph nodes. Skipping.")
            
    if not valid_candidates:
        print("Error: No valid candidate rooms found in the graph.")
        return

    # Compute indicators (P3, P4, P5)
    acc_indicators, wtc_scores = evaluate_accessibility(graph, valid_candidates, traffic_map)
    vis_indicators, raw_vis_scores = evaluate_visibility(graph, valid_candidates, traffic_map)
    priv_indicators, risk_scores = evaluate_privacy(graph, valid_candidates, traffic_map)

    # Rank and calculate final score (P6)
    ranked_list = []
    for r in valid_candidates:
        acc = acc_indicators[r]
        vis = vis_indicators[r]
        priv = priv_indicators[r]
        final_score = w_acc * acc + w_vis * vis + w_priv * priv
        
        trade_off_desc = generate_trade_off_report(
            r, acc, vis, priv, 
            wtc_scores[r], raw_vis_scores[r], risk_scores[r]
        )
        
        ranked_list.append({
            "candidate_room": r,
            "accessibility_indicator": round(acc, 4),
            "visibility_indicator": round(vis, 4),
            "privacy_indicator": round(priv, 4),
            "final_score": round(final_score, 4),
            "explanation": trade_off_desc
        })
        
    # Sort candidates by final score descending
    ranked_list.sort(key=lambda x: x["final_score"], reverse=True)
    
    # Assign ranks
    for rank_idx, item in enumerate(ranked_list):
        item["final_rank"] = rank_idx + 1

    # Format output JSON
    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(ranked_list, f, indent=2, ensure_ascii=False)
        
    print(f"\nSuccessfully evaluated and ranked candidates. Saved report to: {args.output}\n")
    
    # Print ranked output table
    print("=" * 110)
    print(f"{'RANK':<6}{'ROOM':<20}{'ACCESSIBILITY':<18}{'VISIBILITY':<15}{'PRIVACY':<15}{'FINAL SCORE':<15}")
    print("=" * 110)
    for item in ranked_list:
        print(f"{item['final_rank']:<6}{item['candidate_room']:<20}{item['accessibility_indicator']:<18.4f}{item['visibility_indicator']:<15.4f}{item['privacy_indicator']:<15.4f}{item['final_score']:<15.4f}")
    print("=" * 110)
    print("\nChi tiết thuyết minh Đánh đổi (Trade-off Explanations):")
    for item in ranked_list:
        print(f"- [Hạng {item['final_rank']}] {item['candidate_room']}: {item['explanation']}")
    print("=" * 110)

if __name__ == "__main__":
    main()
