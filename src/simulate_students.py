from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

import networkx as nx

from graph_utils import load_all_graphs


ROOT = Path(__file__).resolve().parents[1]
DAY_INDEX = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
DEFAULT_CAMPUS_START_TIME = "07:00"
DEFAULT_LUNCH_START_TIME = "11:30"
DEFAULT_LUNCH_END_TIME = "12:30"
DEFAULT_CAMPUS_END_TIME = "18:00"
PROFILE_WEIGHTS = {
    "efficient": {"distance": 1.3, "stair": 0.8, "building": 0.5, "turn": 0.4, "familiarity": 0.2, "temperature": 0.4},
    "familiar": {"distance": 1.0, "stair": 0.6, "building": 0.5, "turn": 0.4, "familiarity": 1.0, "temperature": 0.6},
    "new_student": {"distance": 1.0, "stair": 0.8, "building": 0.7, "turn": 1.2, "familiarity": 0.1, "temperature": 0.5},
    "crowd_avoiding": {"distance": 0.9, "stair": 0.6, "building": 0.5, "turn": 0.5, "familiarity": 0.3, "temperature": 0.7},
    "explorer": {"distance": 0.7, "stair": 0.5, "building": 0.4, "turn": 0.3, "familiarity": 0.2, "temperature": 1.2},
}


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def load_json(path: str | Path) -> Any:
    return json.loads(resolve_path(path).read_text(encoding="utf-8"))


def export_json(data: Any, path: str) -> None:
    output = resolve_path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_config(path: str) -> dict:
    return load_json(path)


def canonical_course_code(raw_code: Any) -> str:
    if raw_code is None:
        return ""
    code = "".join(str(raw_code).upper().split())
    if code.endswith(".1") or code.endswith(".2"):
        return code[:-2]
    return code


def normalize_probabilities(probabilities: dict[str, float]) -> list[tuple[str, float]]:
    total = sum(float(value) for value in probabilities.values())
    if total <= 0:
        raise ValueError("Probability total must be positive.")
    return [(key, float(value) / total) for key, value in probabilities.items()]


def weighted_choice(rng: random.Random, probabilities: dict[str, float]) -> str:
    normalized = normalize_probabilities(probabilities)
    threshold = rng.random()
    cumulative = 0.0
    for key, probability in normalized:
        cumulative += probability
        if threshold <= cumulative:
            return key
    return normalized[-1][0]


def load_timetable(path: str) -> tuple[list[dict], dict[str, list[dict]]]:
    events = load_json(path)
    by_course: dict[str, list[dict]] = defaultdict(list)
    for event in events:
        by_course[canonical_course_code(event["course_code"])].append(event)
    return events, by_course


def optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def infer_plan_year(item: dict, course: dict | None = None) -> int | None:
    explicit_year = optional_int(item.get("year"))
    if explicit_year is not None:
        return explicit_year
    semester = optional_int(item.get("semester") or item.get("recommended_semester"))
    if semester is not None:
        return (semester + 1) // 2
    if course:
        return optional_int(course.get("recommended_year"))
    return None


def infer_plan_semester(item: dict, course: dict | None = None) -> int | None:
    explicit_semester = optional_int(item.get("semester") or item.get("recommended_semester"))
    if explicit_semester is not None:
        return explicit_semester
    if course:
        return optional_int(course.get("recommended_semester"))
    return None


def load_curriculum(path: str) -> dict:
    data = load_json(path)
    by_major = {major["major_id"]: major for major in data["majors"]}
    plan_by_major_year: dict[tuple[str, int], list[dict]] = defaultdict(list)
    plan_by_major_semester: dict[tuple[str, int], list[dict]] = defaultdict(list)
    courses_by_major_year: dict[tuple[str, int], list[dict]] = defaultdict(list)
    courses_by_major_semester: dict[tuple[str, int], list[dict]] = defaultdict(list)
    courses_by_year: dict[int, list[dict]] = defaultdict(list)
    courses_by_semester: dict[int, list[dict]] = defaultdict(list)
    course_lookup: dict[tuple[str, str], dict] = {}
    for major in data["majors"]:
        major_id = major["major_id"]
        for course in major["curriculum_courses"]:
            course_code = canonical_course_code(course["course_code"])
            course["course_code"] = course_code
            course_lookup[(major_id, course_code)] = course
            recommended_year = optional_int(course.get("recommended_year"))
            if recommended_year is not None:
                courses_by_major_year[(major_id, recommended_year)].append(course)
                courses_by_year[recommended_year].append(course)
            recommended_semester = optional_int(course.get("recommended_semester"))
            if recommended_semester is not None:
                courses_by_major_semester[(major_id, recommended_semester)].append(course)
                courses_by_semester[recommended_semester].append(course)
        for item in major["sample_teaching_plan"]:
            course = course_lookup.get((major_id, item.get("course_code", "")))
            plan_year = infer_plan_year(item, course)
            if plan_year is not None:
                plan_by_major_year[(major_id, plan_year)].append(item)
            plan_semester = infer_plan_semester(item, course)
            if plan_semester is not None:
                plan_by_major_semester[(major_id, plan_semester)].append(item)
    return {
        "raw": data,
        "by_major": by_major,
        "plan_by_major_year": plan_by_major_year,
        "plan_by_major_semester": plan_by_major_semester,
        "courses_by_major_year": courses_by_major_year,
        "courses_by_major_semester": courses_by_major_semester,
        "courses_by_year": courses_by_year,
        "courses_by_semester": courses_by_semester,
        "course_lookup": course_lookup,
    }


def semesters_for_year(year: int) -> list[int]:
    return [year * 2 - 1, year * 2]


def active_semester_for_year(year: int) -> int:
    return year * 2


def behavior_for_agent(rng: random.Random, year: int, base_probabilities: dict[str, float], density: float) -> str:
    adjusted = dict(base_probabilities)
    if year == 1:
        adjusted["new_student"] = adjusted.get("new_student", 0) + 0.2
    if year >= 3:
        adjusted["familiar"] = adjusted.get("familiar", 0) + 0.15
    if density > 0.7:
        adjusted["efficient"] = adjusted.get("efficient", 0) + 0.15
    return weighted_choice(rng, adjusted)


def major_probabilities(config: dict) -> dict[str, float]:
    class_counts = config.get("major_class_counts")
    if class_counts:
        return {major: float(count) for major, count in class_counts.items()}
    return config["majors"]


def choose_gate_pair(config: dict, rng: random.Random) -> tuple[str, str]:
    entry_gate = weighted_choice(rng, config.get("entry_gates", {"UIT-GATE-A": 0.75, "UIT-GATE-B": 0.25}))
    if config.get("exit_same_as_entry", True):
        return entry_gate, entry_gate
    exit_gate = weighted_choice(rng, config.get("exit_gates", config.get("entry_gates", {"UIT-GATE-A": 0.75, "UIT-GATE-B": 0.25})))
    return entry_gate, exit_gate


def choose_transport_profile(config: dict, rng: random.Random) -> dict:
    mode = weighted_choice(rng, config.get("transport_modes", {"personal_transport": 0.7, "public_transport": 0.3}))
    if mode == "personal_transport":
        entry_gate = config.get("personal_transport_entry_gate", "UIT-GATE-A")
        exit_gate = config.get("personal_transport_exit_gate", "UIT-GATE-A")
        anchor = config.get("personal_transport_anchor", "UIT-GARAGE")
        return {
            "transport_mode": mode,
            "entry_gate": entry_gate,
            "exit_gate": exit_gate,
            "entry_node": anchor,
            "exit_node": anchor,
        }
    entry_gate = weighted_choice(rng, config.get("public_transport_entry_gates", {"UIT-GATE-B": 0.9, "UIT-GATE-A": 0.1}))
    exit_gate = weighted_choice(rng, config.get("public_transport_exit_gates", {"UIT-GATE-A": 0.99, "UIT-GATE-B": 0.01}))
    return {
        "transport_mode": mode,
        "entry_gate": entry_gate,
        "exit_gate": exit_gate,
        "entry_node": entry_gate,
        "exit_node": exit_gate,
    }


def choose_lunch_destination(config: dict, rng: random.Random) -> str:
    return weighted_choice(rng, config.get("lunch_destinations", {
        "UIT-GATE-A": 0.6,
        "UIT-GATE-B": 0.2,
        "UIT-CANTEEN": 0.2,
    }))


def generate_agents(config: dict, rng: random.Random) -> list[dict]:
    agents = []
    for index in range(1, int(config["num_students"]) + 1):
        major = weighted_choice(rng, major_probabilities(config))
        year = int(weighted_choice(rng, config["years"]))
        active_semester = active_semester_for_year(year)
        familiarity_ranges = {1: (0.30, 0.50), 2: (0.45, 0.65), 3: (0.60, 0.80), 4: (0.70, 0.90)}
        density = rng.uniform(0.35, 0.90)
        low, high = familiarity_ranges[year]
        profile = behavior_for_agent(rng, year, config["behavior_profiles"], density)
        transport = choose_transport_profile(config, rng)
        mental_instability = rng.betavariate(
            float(config.get("mental_instability_alpha", 2.0)),
            float(config.get("mental_instability_beta", 5.0)),
        )
        path_randomness = min(
            1.0,
            float(config.get("base_path_randomness", 0.05))
            + mental_instability * float(config.get("mental_instability_randomness_multiplier", 0.85)),
        )
        agents.append({
            "student_id": f"S{index:06d}",
            "major": major,
            "year": year,
            "active_semester": active_semester,
            "semester_preference": semesters_for_year(year),
            "class_group": f"{major}_YEAR{year}_GROUP{rng.randint(1, 5):02d}",
            "behavior_profile": profile,
            "transport_mode": transport["transport_mode"],
            "entry_gate": transport["entry_gate"],
            "exit_gate": transport["exit_gate"],
            "entry_node": transport["entry_node"],
            "exit_node": transport["exit_node"],
            "lunch_destination": choose_lunch_destination(config, rng),
            "mental_instability_metric": round(mental_instability, 3),
            "path_randomness": round(path_randomness, 3),
            "walking_speed_mps": round(rng.normalvariate(config["default_walking_speed_mps"], 0.12), 2),
            "familiarity": round(rng.uniform(low, high), 2),
            "schedule_density": round(density, 2),
        })
    return agents


def assign_courses_to_agent(agent: dict, curriculum: dict, rng: random.Random, warnings: list[dict]) -> list[dict]:
    major_id = agent["major"]
    year = agent["year"]
    active_semester = agent.get("active_semester", active_semester_for_year(year))
    selected = []
    seen = set()

    def add_items(items: list[dict], source_override: str | None = None) -> None:
        for item in items:
            code = canonical_course_code(item.get("course_code"))
            if not code or code in seen:
                continue
            course = curriculum["course_lookup"].get((major_id, code), item)
            if course.get("course_block") == "graduation" and year < 4:
                continue
            selected.append({
                "course_code": code,
                "course_name": course.get("course_name", item.get("course_name", code)),
                "credits": course.get("credits"),
                "stress_weight": course.get("stress_weight", 2),
                "recommended_semester": course.get("recommended_semester", item.get("semester")),
                "recommended_year": course.get("recommended_year", item.get("year")),
                "source": source_override or ("sample_teaching_plan" if "semester" in item else "curriculum_courses"),
            })
            seen.add(code)

    plan_items = curriculum["plan_by_major_semester"].get((major_id, active_semester), [])
    if not plan_items:
        plan_items = curriculum["plan_by_major_year"].get((major_id, year), [])
    if not plan_items:
        plan_items = curriculum["courses_by_major_semester"].get((major_id, active_semester), [])
    if not plan_items:
        plan_items = curriculum["courses_by_major_year"].get((major_id, year), [])
    if not plan_items:
        plan_items = curriculum["courses_by_semester"].get(active_semester, [])
        if plan_items:
            warnings.append({
                "student_id": agent["student_id"],
                "type": "USING_GLOBAL_SEMESTER_COURSE_FALLBACK",
                "message": f"No {major_id} year {year} pool; using global semester {active_semester} courses.",
            })
    if not plan_items:
        plan_items = curriculum["courses_by_year"].get(year, [])
        if plan_items:
            warnings.append({
                "student_id": agent["student_id"],
                "type": "USING_GLOBAL_YEAR_COURSE_FALLBACK",
                "message": f"No {major_id} year {year} pool; using global year {year} courses.",
            })

    add_items(plan_items)
    if not selected:
        fallback_items = curriculum["courses_by_semester"].get(active_semester, [])
        if fallback_items:
            warnings.append({
                "student_id": agent["student_id"],
                "type": "USING_GLOBAL_SEMESTER_COURSE_FALLBACK",
                "message": f"No usable {major_id} year {year} courses; using global semester {active_semester} courses.",
            })
            add_items(fallback_items, "global_semester_fallback")
    if not selected:
        fallback_items = curriculum["courses_by_year"].get(year, [])
        if fallback_items:
            warnings.append({
                "student_id": agent["student_id"],
                "type": "USING_GLOBAL_YEAR_COURSE_FALLBACK",
                "message": f"No usable {major_id} year {year} courses; using global year {year} courses.",
            })
            add_items(fallback_items, "global_year_fallback")

    if len(selected) > 5:
        selected = rng.sample(selected, 5)
    if not selected:
        warnings.append({"student_id": agent["student_id"], "type": "NO_COURSES_ASSIGNED", "message": f"No courses for {major_id} year {year}."})
    return selected


def minutes(value: str) -> int:
    hour, minute = value.split(":")
    return int(hour) * 60 + int(minute)


def overlaps(candidate: dict, events: list[dict]) -> bool:
    candidate_start = minutes(candidate["start_time"])
    candidate_end = minutes(candidate["end_time"])
    for event in events:
        if event["day"] != candidate["day"]:
            continue
        if candidate_start < minutes(event["end_time"]) and minutes(event["start_time"]) < candidate_end:
            return True
    return False


def match_courses_to_timetable(agent: dict, courses: list[dict], timetable_by_course: dict[str, list[dict]], rng: random.Random, warnings: list[dict]) -> dict:
    events = []
    for course in courses:
        course_code = canonical_course_code(course["course_code"])
        candidates = list(timetable_by_course.get(course_code, []))
        rng.shuffle(candidates)
        chosen = None
        for candidate in candidates:
            if not overlaps(candidate, events):
                chosen = candidate
                break
        if chosen is None:
            warnings.append({"student_id": agent["student_id"], "type": "COURSE_NOT_FOUND_IN_TIMETABLE", "message": f"No non-overlapping timetable event for {course_code}."})
            continue
        event = dict(chosen)
        event["stress_weight"] = course.get("stress_weight", 2)
        events.append(event)
    events.sort(key=lambda event: (DAY_INDEX.get(event["day"], 99), event["start_time"]))
    return {"student_id": agent["student_id"], "events": events}


def normalize_edge_id(source: str, target: str) -> str:
    return "__".join(sorted([source, target]))


def path_distance(graph: nx.Graph, path: list[str]) -> float:
    return sum(float(graph[path[index]][path[index + 1]].get("distance", 1)) for index in range(len(path) - 1))


def count_floor_changes(graph: nx.Graph, path: list[str]) -> int:
    changes = 0
    previous = graph.nodes[path[0]].get("floor")
    for node_id in path[1:]:
        floor = graph.nodes[node_id].get("floor")
        if floor is not None and previous is not None and floor != previous:
            changes += 1
        if floor is not None:
            previous = floor
    return changes


def count_buildings(graph: nx.Graph, path: list[str]) -> int:
    buildings = set()
    for node_id in path:
        building = graph.nodes[node_id].get("building")
        if building:
            buildings.add(building)
        elif node_id.startswith("UIT-"):
            buildings.add("UIT")
    return len(buildings)


def softmax_select(rng: random.Random, paths: list[list[str]], costs: list[float], temperature: float) -> list[str]:
    scaled = [math.exp(-cost / max(temperature, 0.01)) for cost in costs]
    total = sum(scaled)
    threshold = rng.random()
    cumulative = 0.0
    for path, value in zip(paths, scaled):
        cumulative += value / total
        if threshold <= cumulative:
            return path
    return paths[-1]


def get_candidate_paths(graph: nx.Graph, source: str, target: str, k: int, route_cache: dict) -> list[list[str]]:
    cache_key = ("candidates", source, target, k)
    if cache_key in route_cache:
        return route_cache[cache_key]
    candidates = []
    for path in nx.shortest_simple_paths(graph, source, target, weight="distance"):
        candidates.append(path)
        if len(candidates) >= k:
            break
    route_cache[cache_key] = candidates
    return candidates


def choose_path(
    graph: nx.Graph,
    source: str,
    target: str,
    profile: str,
    mode: str,
    k: int,
    rng: random.Random,
    familiarity: float,
    path_randomness: float,
    route_cache: dict,
) -> list[str]:
    if mode == "shortest_path":
        cache_key = ("shortest", source, target)
        if cache_key not in route_cache:
            route_cache[cache_key] = nx.shortest_path(graph, source, target, weight="distance")
        return route_cache[cache_key]
    candidates = get_candidate_paths(graph, source, target, k, route_cache)
    if mode == "k_shortest_paths":
        costs = [path_distance(graph, path) for path in candidates]
        return softmax_select(rng, candidates, costs, temperature=20.0 + path_randomness * 40.0)
    weights = PROFILE_WEIGHTS.get(profile, PROFILE_WEIGHTS["efficient"])
    costs = []
    noise_scale = 3.0 + path_randomness * float(12.0)
    for path in candidates:
        distance = path_distance(graph, path)
        floor_changes = count_floor_changes(graph, path)
        buildings = count_buildings(graph, path)
        turns = max(0, len(path) - 2)
        cost = (
            weights["distance"] * distance
            + weights["stair"] * floor_changes * 10
            + weights["building"] * buildings * 8
            + weights["turn"] * turns
            - weights["familiarity"] * familiarity * 10
            + rng.uniform(0, noise_scale)
        )
        costs.append(cost)
    temperature = weights["temperature"] * 20 * (1.0 + path_randomness)
    return softmax_select(rng, candidates, costs, temperature)


def route_transition_minutes(departure_time: str | None, arrival_time: str | None) -> int:
    if not departure_time or not arrival_time:
        return 0
    return max(0, minutes(arrival_time) - minutes(departure_time))


def route_stress_between(previous: dict | None, current: dict | None) -> int:
    previous_stress = int((previous or {}).get("stress_weight", 1))
    current_stress = int((current or {}).get("stress_weight", 1))
    return max(previous_stress, current_stress)


def synthetic_event(event_id: str, node_id: str, day: str, start_time: str, end_time: str, stress_weight: int = 1) -> dict:
    return {
        "event_id": event_id,
        "course_code": event_id,
        "course_name": event_id.replace("_", " ").title(),
        "room_id": node_id,
        "day": day,
        "start_time": start_time,
        "end_time": end_time,
        "stress_weight": stress_weight,
        "event_type": "movement_anchor",
    }


def node_building(node_id: str, graph: nx.Graph) -> str | None:
    if node_id in graph:
        building = graph.nodes[node_id].get("building")
        if building:
            return str(building)
    if node_id and node_id[0] in {"A", "B", "C", "D", "E"}:
        return node_id[0]
    return None


def event_building(event: dict, graph: nx.Graph) -> str | None:
    return event.get("building") or node_building(event.get("room_id", ""), graph)


def choose_building_a_top_waypoint(rng: random.Random) -> str:
    return rng.choice(["A-F1-RING-TOP-MID", "A-F1-RING-TOP-RIGHT"])


def choose_building_a_garage_waypoint(rng: random.Random) -> str:
    return rng.choice(["A-F1-RING-LEFT-MID", "A-F1-RING-TOP-LEFT"])


def entry_waypoints(agent: dict, first_event: dict, graph: nx.Graph, rng: random.Random) -> list[str]:
    if agent.get("transport_mode") == "personal_transport":
        building = event_building(first_event, graph)
        if building == "B":
            return [choose_building_a_top_waypoint(rng)]
        if building in {"C", "E"}:
            return ["A-F1-RING-RIGHT-MID", "E-F1-LOBBY"]
        return [choose_building_a_garage_waypoint(rng)]
    if agent.get("entry_gate") == "UIT-GATE-A":
        building = event_building(first_event, graph)
        if building in {"E", "C"}:
            return ["A-F1-RING-BOTTOM-RIGHT", "A-F1-RING-RIGHT-MID"]
        if building == "B":
            return ["A-F1-RING-BOTTOM-RIGHT", choose_building_a_top_waypoint(rng)]
        return ["A-F1-RING-BOTTOM-RIGHT"]
    return []


def personal_exit_waypoints(agent: dict, last_event: dict, graph: nx.Graph, config: dict, rng: random.Random) -> tuple[list[str], str]:
    building = event_building(last_event, graph)
    if agent.get("transport_mode") != "personal_transport":
        return [], "campus_exit"
    if building == "B":
        strategy = weighted_choice(rng, config.get("personal_exit_from_building_b", {"garage_back_road": 0.5, "building_a_route": 0.5}))
        if strategy == "building_a_route":
            return [choose_building_a_top_waypoint(rng), choose_building_a_garage_waypoint(rng)], "campus_exit_garage_via_a"
        return [], "campus_exit_garage_back_road"
    if building == "C":
        strategy = weighted_choice(rng, config.get("personal_exit_from_building_c", {"building_e_route": 0.9, "building_a_route": 0.1}))
        if strategy == "building_a_route":
            return ["A-F1-RING-RIGHT-MID", choose_building_a_garage_waypoint(rng)], "campus_exit_garage_via_a"
        return ["E-F1-LOBBY"], "campus_exit_garage_via_e"
    if building == "E":
        return ["E-F1-LOBBY"], "campus_exit_garage_via_e"
    if building == "A":
        return [choose_building_a_garage_waypoint(rng)], "campus_exit_garage_via_a"
    return [], "campus_exit_garage"


def crosses_lunch_break(previous: dict, current: dict, config: dict) -> bool:
    lunch_start = config.get("lunch_start_time", DEFAULT_LUNCH_START_TIME)
    lunch_end = config.get("lunch_end_time", DEFAULT_LUNCH_END_TIME)
    return minutes(previous["end_time"]) <= minutes(lunch_start) and minutes(current["start_time"]) >= minutes(lunch_end)


def create_route_leg(
    agent: dict,
    day: str,
    source: str,
    target: str,
    previous_event: dict | None,
    current_event: dict | None,
    graph: nx.Graph,
    config: dict,
    route_cache: dict,
    route_counter: list[int],
    rng: random.Random,
    warnings: list[dict],
    leg_type: str,
    departure_time: str | None,
    arrival_time: str | None,
) -> dict | None:
    if source == target:
        return None
    if source not in graph or target not in graph:
        warnings.append({"student_id": agent["student_id"], "type": "NODE_NOT_FOUND_IN_GRAPH", "message": f"{source} or {target} missing."})
        return None

    mode = config["route_choice_mode"]
    profile = agent["behavior_profile"]
    try:
        path = choose_path(
            graph,
            source,
            target,
            profile,
            mode,
            int(config["k_shortest_paths"]),
            rng,
            agent["familiarity"],
            float(agent.get("path_randomness", 0.0)),
            route_cache if config.get("enable_route_cache", True) else {},
        )
    except (nx.NetworkXNoPath, nx.NodeNotFound) as exc:
        warnings.append({"student_id": agent["student_id"], "type": "ROUTE_NOT_FOUND", "message": str(exc)})
        return None

    route_counter[0] += 1
    distance = path_distance(graph, path)
    speed = max(0.8, float(agent["walking_speed_mps"]))
    transition_minutes = route_transition_minutes(departure_time, arrival_time)
    estimated_walk_time_seconds = int(distance / speed)
    path_edges = [normalize_edge_id(path[index], path[index + 1]) for index in range(len(path) - 1)]
    return {
        "route_id": f"R{route_counter[0]:06d}",
        "student_id": agent["student_id"],
        "day": day,
        "leg_type": leg_type,
        "from_event_id": (previous_event or {}).get("event_id"),
        "to_event_id": (current_event or {}).get("event_id"),
        "from_room": source,
        "to_room": target,
        "from_node": source,
        "to_node": target,
        "planned_departure_time": departure_time,
        "planned_arrival_time": arrival_time,
        "entry_gate": agent.get("entry_gate"),
        "exit_gate": agent.get("exit_gate"),
        "lunch_destination": agent.get("lunch_destination"),
        "route_choice_mode": mode,
        "behavior_profile": profile,
        "mental_instability_metric": agent.get("mental_instability_metric", 0),
        "path_randomness": agent.get("path_randomness", 0),
        "path_nodes": path,
        "path_edges": path_edges,
        "total_distance": round(distance, 2),
        "estimated_walk_time_seconds": estimated_walk_time_seconds,
        "number_of_buildings_passed": count_buildings(graph, path),
        "number_of_floor_changes": count_floor_changes(graph, path),
        "transition_available_minutes": transition_minutes,
        "is_late_risk": estimated_walk_time_seconds > transition_minutes * 60 if transition_minutes else False,
        "time_window": time_window(departure_time or arrival_time or "00:00"),
        "route_stress": route_stress_between(previous_event, current_event),
    }


def append_route_leg(routes: list[dict], *args, **kwargs) -> None:
    route = create_route_leg(*args, **kwargs)
    if route is not None:
        routes.append(route)


def append_route_sequence(
    routes: list[dict],
    agent: dict,
    day: str,
    source: str,
    target: str,
    waypoints: list[str],
    previous_event: dict | None,
    current_event: dict | None,
    graph: nx.Graph,
    config: dict,
    route_cache: dict,
    route_counter: list[int],
    rng: random.Random,
    warnings: list[dict],
    leg_type: str,
    departure_time: str | None,
    arrival_time: str | None,
) -> None:
    nodes = [source] + [waypoint for waypoint in waypoints if waypoint and waypoint != source and waypoint != target] + [target]
    for index, (segment_source, segment_target) in enumerate(zip(nodes, nodes[1:])):
        segment_previous = previous_event if index == 0 else synthetic_event(
            f"WAYPOINT_{agent['student_id']}_{day}_{route_counter[0]}_{index}",
            segment_source,
            day,
            departure_time or "00:00",
            departure_time or "00:00",
        )
        segment_current = current_event if index == len(nodes) - 2 else synthetic_event(
            f"WAYPOINT_{agent['student_id']}_{day}_{route_counter[0]}_{index + 1}",
            segment_target,
            day,
            arrival_time or departure_time or "00:00",
            arrival_time or departure_time or "00:00",
        )
        append_route_leg(
            routes,
            agent,
            day,
            segment_source,
            segment_target,
            segment_previous,
            segment_current,
            graph,
            config,
            route_cache,
            route_counter,
            rng,
            warnings,
            leg_type,
            departure_time if index == 0 else None,
            arrival_time if index == len(nodes) - 2 else None,
        )


def add_lunch_stop(
    routes: list[dict],
    agent: dict,
    day: str,
    previous_event: dict,
    current_event: dict | None,
    graph: nx.Graph,
    config: dict,
    route_cache: dict,
    route_counter: list[int],
    rng: random.Random,
    warnings: list[dict],
) -> None:
    lunch_start = config.get("lunch_start_time", DEFAULT_LUNCH_START_TIME)
    lunch_end = config.get("lunch_end_time", DEFAULT_LUNCH_END_TIME)
    lunch_destination = agent["lunch_destination"]
    lunch_event = synthetic_event(f"LUNCH_{agent['student_id']}_{day}", lunch_destination, day, lunch_start, lunch_end)

    append_route_leg(
        routes,
        agent,
        day,
        previous_event["room_id"],
        lunch_destination,
        previous_event,
        lunch_event,
        graph,
        config,
        route_cache,
        route_counter,
        rng,
        warnings,
        "lunch_out",
        previous_event["end_time"],
        lunch_start,
    )

    if current_event is not None:
        append_route_leg(
            routes,
            agent,
            day,
            lunch_destination,
            current_event["room_id"],
            lunch_event,
            current_event,
            graph,
            config,
            route_cache,
            route_counter,
            rng,
            warnings,
            "lunch_return",
            lunch_end,
            current_event["start_time"],
        )


def build_daily_plan(agent: dict, day: str, events: list[dict]) -> dict:
    return {
        "day": day,
        "transport_mode": agent["transport_mode"],
        "entry_gate": agent["entry_gate"],
        "exit_gate": agent["exit_gate"],
        "entry_node": agent["entry_node"],
        "exit_node": agent["exit_node"],
        "lunch_destination": agent["lunch_destination"],
        "class_event_ids": [event["event_id"] for event in events],
    }


def generate_routes_for_schedule(agent: dict, schedule: dict, graph: nx.Graph, config: dict, route_cache: dict, route_counter: list[int], rng: random.Random, warnings: list[dict]) -> list[dict]:
    routes = []
    daily_plans = []
    events_by_day: dict[str, list[dict]] = defaultdict(list)
    for event in schedule["events"]:
        events_by_day[event["day"]].append(event)

    for day, events in events_by_day.items():
        events.sort(key=lambda event: event["start_time"])
        if not events:
            continue
        daily_plans.append(build_daily_plan(agent, day, events))

        first_event = events[0]
        entry_event = synthetic_event(f"ENTRY_{agent['student_id']}_{day}", agent["entry_node"], day, config.get("campus_start_time", DEFAULT_CAMPUS_START_TIME), config.get("campus_start_time", DEFAULT_CAMPUS_START_TIME))
        append_route_sequence(
            routes,
            agent,
            day,
            agent["entry_node"],
            first_event["room_id"],
            entry_waypoints(agent, first_event, graph, rng),
            entry_event,
            first_event,
            graph,
            config,
            route_cache,
            route_counter,
            rng,
            warnings,
            "campus_entry",
            config.get("campus_start_time", DEFAULT_CAMPUS_START_TIME),
            first_event["start_time"],
        )

        lunch_added = False
        for previous, current in zip(events, events[1:]):
            if crosses_lunch_break(previous, current, config):
                add_lunch_stop(routes, agent, day, previous, current, graph, config, route_cache, route_counter, rng, warnings)
                lunch_added = True
                continue
            append_route_leg(
                routes,
                agent,
                day,
                previous["room_id"],
                current["room_id"],
                previous,
                current,
                graph,
                config,
                route_cache,
                route_counter,
                rng,
                warnings,
                "class_transition",
                previous["end_time"],
                current["start_time"],
            )

        last_event = events[-1]
        if not lunch_added and minutes(last_event["end_time"]) <= minutes(config.get("lunch_start_time", DEFAULT_LUNCH_START_TIME)):
            add_lunch_stop(routes, agent, day, last_event, None, graph, config, route_cache, route_counter, rng, warnings)
            lunch_destination = agent["lunch_destination"]
            if lunch_destination == agent["exit_gate"] or graph.nodes[lunch_destination].get("type") == "gate":
                continue
            lunch_event = synthetic_event(f"LUNCH_{agent['student_id']}_{day}", lunch_destination, day, config.get("lunch_start_time", DEFAULT_LUNCH_START_TIME), config.get("lunch_end_time", DEFAULT_LUNCH_END_TIME))
            last_event = lunch_event

        exit_waypoints, exit_leg_type = personal_exit_waypoints(agent, last_event, graph, config, rng)
        exit_event = synthetic_event(f"EXIT_{agent['student_id']}_{day}", agent["exit_node"], day, config.get("campus_end_time", DEFAULT_CAMPUS_END_TIME), config.get("campus_end_time", DEFAULT_CAMPUS_END_TIME))
        append_route_sequence(
            routes,
            agent,
            day,
            last_event["room_id"],
            agent["exit_node"],
            exit_waypoints,
            last_event,
            exit_event,
            graph,
            config,
            route_cache,
            route_counter,
            rng,
            warnings,
            exit_leg_type,
            last_event["end_time"],
            config.get("campus_end_time", DEFAULT_CAMPUS_END_TIME),
        )

    schedule["daily_plans"] = daily_plans
    return routes


def time_window(start_time: str) -> str:
    value = minutes(start_time)
    if value < minutes("11:30"):
        return "morning"
    if value < minutes("13:30"):
        return "noon"
    if value < minutes("17:30"):
        return "afternoon"
    return "evening"


def blank_traffic(item_id: str, extra: dict | None = None) -> dict:
    data = {
        "id": item_id,
        "total_count": 0,
        "morning_count": 0,
        "noon_count": 0,
        "afternoon_count": 0,
        "evening_count": 0,
        "all_day_count": 0,
        "weekly_count": 0,
        "stress_traffic": 0,
    }
    if extra:
        data.update(extra)
    return data


def accumulate_traffic(routes: list[dict]) -> tuple[dict[str, dict], dict[str, dict]]:
    node_traffic: dict[str, dict] = {}
    edge_traffic: dict[str, dict] = {}
    for route in routes:
        window = route["time_window"]
        stress = route.get("route_stress", 1)
        for node_id in route["path_nodes"]:
            item = node_traffic.setdefault(node_id, blank_traffic(node_id, {"node_id": node_id}))
            item["total_count"] += 1
            item["all_day_count"] += 1
            item["weekly_count"] += 1
            item[f"{window}_count"] += 1
            item["stress_traffic"] += stress
        for index, edge_id in enumerate(route["path_edges"]):
            source = route["path_nodes"][index]
            target = route["path_nodes"][index + 1]
            item = edge_traffic.setdefault(edge_id, blank_traffic(edge_id, {"edge_id": edge_id, "source": source, "target": target}))
            item["total_count"] += 1
            item["all_day_count"] += 1
            item["weekly_count"] += 1
            item[f"{window}_count"] += 1
            item["stress_traffic"] += stress
    return node_traffic, edge_traffic


def generate_heatmap_data(node_traffic: dict[str, dict], edge_traffic: dict[str, dict]) -> dict:
    node_max = max((item["total_count"] for item in node_traffic.values()), default=0)
    edge_max = max((item["total_count"] for item in edge_traffic.values()), default=0)
    stress_max = max([item["stress_traffic"] for item in node_traffic.values()] + [item["stress_traffic"] for item in edge_traffic.values()] + [0])
    items = []
    for item in node_traffic.values():
        items.append({
            "id": item["node_id"],
            "type": "node",
            "value": item["total_count"],
            "normalized_value": item["total_count"] / node_max if node_max else 0,
            "stress_value": item["stress_traffic"],
            "normalized_stress_value": item["stress_traffic"] / stress_max if stress_max else 0,
        })
    for item in edge_traffic.values():
        items.append({
            "id": item["edge_id"],
            "type": "edge",
            "value": item["total_count"],
            "normalized_value": item["total_count"] / edge_max if edge_max else 0,
            "stress_value": item["stress_traffic"],
            "normalized_stress_value": item["stress_traffic"] / stress_max if stress_max else 0,
        })
    return {"scope": "campus", "time_window": "weekly", "items": items}


def validate_simulation_outputs(graph: nx.Graph, agents: list[dict], schedules: list[dict], routes: list[dict], node_traffic: dict[str, dict], edge_traffic: dict[str, dict]) -> dict:
    errors = []
    warnings = []
    for agent in agents:
        for field in ["student_id", "major", "year", "active_semester", "behavior_profile", "transport_mode", "entry_gate", "exit_gate", "entry_node", "exit_node", "lunch_destination", "mental_instability_metric", "path_randomness"]:
            if field not in agent or agent[field] in (None, ""):
                errors.append({"type": "AGENT_MISSING_FIELD", "message": f"{agent.get('student_id')} missing {field}."})
        if agent.get("active_semester") != active_semester_for_year(int(agent.get("year", 0))):
            errors.append({"type": "INVALID_ACTIVE_SEMESTER", "message": f"{agent.get('student_id')} has invalid active semester."})
        for node_field in ["entry_gate", "exit_gate", "entry_node", "exit_node", "lunch_destination"]:
            if agent.get(node_field) not in graph:
                errors.append({"type": "AGENT_NODE_NOT_FOUND", "message": f"{agent.get('student_id')} {node_field}: {agent.get(node_field)}"})
    for schedule in schedules:
        for event in schedule["events"]:
            if event["room_id"] not in graph:
                errors.append({"type": "EVENT_ROOM_NOT_FOUND", "message": event["room_id"]})
    edge_set = {normalize_edge_id(u, v) for u, v in graph.edges()}
    required_leg_types = {
        "campus_entry",
        "campus_exit",
        "campus_exit_garage",
        "campus_exit_garage_back_road",
        "campus_exit_garage_via_a",
        "campus_exit_garage_via_e",
        "class_transition",
        "lunch_out",
        "lunch_return",
    }
    seen_leg_types = {route.get("leg_type") for route in routes}
    for leg_type in ["campus_entry", "campus_exit", "lunch_out"]:
        if leg_type not in seen_leg_types:
            warnings.append({"type": "ROUTE_LEG_TYPE_NOT_GENERATED", "message": leg_type})
    for route in routes:
        if route.get("leg_type") not in required_leg_types:
            errors.append({"type": "INVALID_ROUTE_LEG_TYPE", "message": route.get("route_id")})
        if not route["path_nodes"] or route["path_nodes"][0] != route["from_room"] or route["path_nodes"][-1] != route["to_room"]:
            errors.append({"type": "INVALID_ROUTE_ENDPOINTS", "message": route["route_id"]})
        for edge_id in route["path_edges"]:
            if edge_id not in edge_set:
                errors.append({"type": "INVALID_ROUTE_EDGE", "message": edge_id})
    for item in list(node_traffic.values()) + list(edge_traffic.values()):
        if item["total_count"] < 0:
            errors.append({"type": "NEGATIVE_TRAFFIC", "message": item["id"]})
    return {"total_agents": len(agents), "total_schedules": len(schedules), "total_routes": len(routes), "warnings": warnings, "errors": errors}


def count_values(items: list[dict], field: str) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for item in items:
        value = item.get(field)
        if value is not None:
            counts[str(value)] += 1
    return dict(sorted(counts.items()))


def count_values_where(items: list[dict], field: str, filter_field: str, filter_value: str) -> dict[str, int]:
    return count_values([item for item in items if item.get(filter_field) == filter_value], field)


def run_simulation(config: dict) -> dict:
    rng = random.Random(config["random_seed"])
    graph = load_all_graphs()
    _, timetable_by_course = load_timetable(config["timetable_path"])
    curriculum = load_curriculum(config["curriculum_path"])
    warnings = []
    agents = generate_agents(config, rng)
    schedules = []
    routes = []
    route_cache = {}
    route_counter = [0]
    for agent in agents:
        courses = assign_courses_to_agent(agent, curriculum, rng, warnings)
        schedule = match_courses_to_timetable(agent, courses, timetable_by_course, rng, warnings)
        schedules.append(schedule)
        routes.extend(generate_routes_for_schedule(agent, schedule, graph, config, route_cache, route_counter, rng, warnings))
    node_traffic, edge_traffic = accumulate_traffic(routes)
    heatmap = generate_heatmap_data(node_traffic, edge_traffic)
    validation = validate_simulation_outputs(graph, agents, schedules, routes, node_traffic, edge_traffic)
    summary = {
        "random_seed": config["random_seed"],
        "num_students": len(agents),
        "num_schedules": len(schedules),
        "num_routes": len(routes),
        "route_choice_mode": config["route_choice_mode"],
        "route_cache_entries": len(route_cache),
        "year_distribution": count_values(agents, "year"),
        "active_semester_distribution": count_values(agents, "active_semester"),
        "major_distribution": count_values(agents, "major"),
        "major_class_counts": config.get("major_class_counts", {}),
        "transport_mode_distribution": count_values(agents, "transport_mode"),
        "entry_gate_distribution": count_values(agents, "entry_gate"),
        "exit_gate_distribution": count_values(agents, "exit_gate"),
        "entry_node_distribution": count_values(agents, "entry_node"),
        "exit_node_distribution": count_values(agents, "exit_node"),
        "lunch_destination_distribution": count_values(agents, "lunch_destination"),
        "route_leg_type_counts": count_values(routes, "leg_type"),
        "lunch_route_destination_counts": count_values_where(routes, "to_node", "leg_type", "lunch_out"),
        "campus_exit_route_gate_counts": count_values_where(routes, "to_node", "leg_type", "campus_exit"),
        "mental_instability_average": round(sum(float(agent.get("mental_instability_metric", 0)) for agent in agents) / max(1, len(agents)), 3),
        "path_randomness_average": round(sum(float(agent.get("path_randomness", 0)) for agent in agents) / max(1, len(agents)), 3),
        "warnings_count": len(warnings),
        "validation_errors_count": len(validation["errors"]),
    }
    return {
        "agents": agents,
        "schedules": schedules,
        "routes": routes,
        "node_traffic": list(node_traffic.values()),
        "edge_traffic": list(edge_traffic.values()),
        "heatmap": heatmap,
        "summary": summary,
        "warnings": warnings,
        "validation": validation,
    }


def export_all(result: dict, output_dir: str) -> None:
    output = resolve_path(output_dir)
    export_json(result["agents"], str(output / "student_agents.json"))
    export_json(result["schedules"], str(output / "student_schedules.json"))
    export_json(result["routes"], str(output / "generated_routes.json"))
    export_json(result["node_traffic"], str(output / "node_traffic.json"))
    export_json(result["edge_traffic"], str(output / "edge_traffic.json"))
    export_json(result["heatmap"], str(output / "heatmap_data.json"))
    export_json(result["summary"], str(output / "simulation_summary.json"))
    export_json(result["warnings"], str(output / "simulation_warnings.json"))
    export_json(result["validation"], str(output / "simulation_validation_report.json"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/simulation_config.json")
    args = parser.parse_args()
    config = load_config(args.config)
    result = run_simulation(config)
    export_all(result, config["output_dir"])
    print(f"Generated {result['summary']['num_students']} agents")
    print(f"Generated {result['summary']['num_routes']} routes")
    print(f"Route cache entries: {result['summary']['route_cache_entries']}")
    print(f"Validation errors: {result['summary']['validation_errors_count']}")
    print(f"Saved outputs to {config['output_dir']}")


if __name__ == "__main__":
    main()
