# 10_SIMULATION_IMPLEMENTATION_TASKS.md

# CS117 Node 1.2 — Simulation Implementation Tasks

## 1. Document status

```txt
Document: 10_SIMULATION_IMPLEMENTATION_TASKS.md
Node: 1.2 - Student Route Simulation
Purpose: Tell Codex how to implement the simulation pipeline
```

This file tells Codex how to implement the route simulation after the following files exist:

```txt
07_NODE_1_2_ROUTE_SIMULATION_FRAMEWORK.md
08_TIMETABLE_INPUT_SPEC.md
09_CURRICULUM_INPUT_SPEC_P1.md
09_CURRICULUM_INPUT_SPEC_P2.md
```

The implementation must remain simple:

```txt
Python
JSON / CSV
NetworkX
Matplotlib / Plotly optional
No backend
No database
No web app
```

---

## 2. High-level goal

Generate simulated weekly movement routes for thousands of virtual students.

Inputs:

```txt
1. Campus graph and building graphs from Node 1.1
2. Normalized timetable data
3. Normalized curriculum data
4. Simulation config
```

Outputs:

```txt
student_agents.json
student_schedules.json
generated_routes.json
node_traffic.json
edge_traffic.json
heatmap_data.json
simulation_summary.json
```

---

## 3. Required input files

Graph inputs:

```txt
data/graphs/campus_graph.json
data/graphs/building_a_graph.json
data/graphs/building_b_graph.json
data/graphs/building_c_graph.json
data/graphs/building_d_graph.json
data/graphs/building_e_graph.json
```

Normalized academic data:

```txt
data/normalized/normalized_timetable.json
data/normalized/normalized_curriculum_all.json
```

Config:

```txt
simulation_config.json
```

---

## 4. Required output directory

All outputs should be written to:

```txt
outputs/node_1_2/
```

Expected files:

```txt
outputs/node_1_2/student_agents.json
outputs/node_1_2/student_schedules.json
outputs/node_1_2/generated_routes.json
outputs/node_1_2/node_traffic.json
outputs/node_1_2/edge_traffic.json
outputs/node_1_2/heatmap_data.json
outputs/node_1_2/simulation_summary.json
outputs/node_1_2/simulation_warnings.json
```

---

## 5. Recommended project files

Create:

```txt
simulate_students.py
graph_loader.py
agent_generation.py
course_assignment.py
timetable_matching.py
route_generation.py
traffic_accumulation.py
simulation_export.py
validate_simulation.py
```

If this is too much for the first version, Codex may implement everything in:

```txt
simulate_students.py
```

but the functions must still be separated clearly.

---

# 6. Configuration file

Create:

```txt
simulation_config.json
```

Example:

```json
{
  "random_seed": 42,
  "num_students": 5000,
  "route_choice_mode": "utility_based_choice",
  "k_shortest_paths": 3,
  "default_walking_speed_mps": 1.25,
  "enable_route_cache": true,
  "enable_congestion_feedback": false,
  "output_dir": "outputs/node_1_2",
  "majors": {
    "CNTT": 0.15,
    "HTTT": 0.12,
    "AI": 0.10,
    "KTMT": 0.10,
    "KHDL": 0.10,
    "KHMT": 0.13,
    "SE": 0.15,
    "NT": 0.10,
    "ATTT": 0.05
  },
  "years": {
    "1": 0.28,
    "2": 0.27,
    "3": 0.25,
    "4": 0.20
  },
  "behavior_profiles": {
    "efficient": 0.35,
    "familiar": 0.25,
    "new_student": 0.15,
    "crowd_avoiding": 0.15,
    "explorer": 0.10
  }
}
```

Rules:

```txt
All random choices must use the configured random seed.
If probabilities do not sum exactly to 1.0, normalize them.
```

---

# 7. Task 1 — Load and merge graphs

Create:

```python
def load_all_graphs(graph_paths: list[str]) -> nx.Graph:
    pass
```

The function should load:

```txt
campus graph
building graph A
building graph B
building graph C
building graph D
building graph E
```

and merge them into one global graph:

```txt
G_UIT
```

Each node must preserve metadata:

```txt
id
label
type
building
floor
x
y
zone
accessible
```

Each edge must preserve metadata:

```txt
source
target
distance
type
bidirectional
accessible
```

Only accessible nodes and edges should be used for routing.

---

## 7.1. Edge ID normalization

Create:

```python
def normalize_edge_id(u: str, v: str) -> str:
    return "__".join(sorted([u, v]))
```

Use this for undirected traffic counting.

---

# 8. Task 2 — Load normalized timetable

Create:

```python
def load_timetable(path: str) -> list[dict]:
    pass
```

Expected input:

```txt
data/normalized/normalized_timetable.json
```

Each event must contain at least:

```txt
event_id
course_code
course_name
room_id
building
floor
day
start_period
end_period
start_time
end_time
```

Build indexes:

```python
events_by_course_code: dict[str, list[dict]]
events_by_room_id: dict[str, list[dict]]
events_by_day: dict[str, list[dict]]
```

---

# 9. Task 3 — Load normalized curriculum

Create:

```python
def load_curriculum(path: str) -> dict:
    pass
```

Expected input:

```txt
data/normalized/normalized_curriculum_all.json
```

Build indexes:

```python
courses_by_major: dict[str, list[dict]]
sample_plan_by_major_year: dict[tuple[str, int], list[dict]]
sample_plan_by_major_semester: dict[tuple[str, int], list[dict]]
elective_pools_by_major: dict[str, dict[str, list[str]]]
```

---

# 10. Task 4 — Generate student agents

Create:

```python
def generate_agents(config: dict) -> list[dict]:
    pass
```

Each agent should follow:

```json
{
  "student_id": "S000001",
  "major": "AI",
  "year": 2,
  "semester_preference": [3, 4],
  "class_group": "AI_YEAR2_GROUP01",
  "behavior_profile": "efficient",
  "walking_speed_mps": 1.25,
  "familiarity": 0.55,
  "schedule_density": 0.70
}
```

Rules:

```txt
year 1 -> semesters 1, 2
year 2 -> semesters 3, 4
year 3 -> semesters 5, 6
year 4 -> semesters 7, 8
```

Suggested familiarity:

```txt
year 1 -> 0.30 to 0.50
year 2 -> 0.45 to 0.65
year 3 -> 0.60 to 0.80
year 4 -> 0.70 to 0.90
```

Behavior profile adjustment:

```txt
year 1 should have higher probability of new_student
year 3-4 should have higher probability of familiar
students with dense schedules should have higher probability of efficient
```

---

# 11. Task 5 — Assign courses to agents

Create:

```python
def assign_courses_to_agent(agent: dict, curriculum: dict, rng) -> list[dict]:
    pass
```

Priority:

```txt
1. Use sample_teaching_plan for the agent's major and year.
2. If sample plan is incomplete, use curriculum_courses with recommended_year.
3. If a sample plan item is a placeholder elective, sample from the matching elective pool.
4. If no course pool exists, skip and log warning.
```

Return course list:

```json
[
  {
    "course_code": "CS106",
    "course_name": "Trí tuệ nhân tạo",
    "credits": 4,
    "stress_weight": 3,
    "source": "sample_teaching_plan"
  }
]
```

Do not assign graduation courses to year 1-3 agents.

---

## 11.1. Handling electives

If a sample plan item has:

```json
"placeholder_type": "major_elective"
```

then sample from:

```txt
major_elective pool
```

If it has:

```json
"placeholder_type": "interdisciplinary_elective"
```

then sample from:

```txt
interdisciplinary_elective pool
```

Do not sample duplicate course codes for the same student unless no alternative exists.

---

# 12. Task 6 — Match courses to timetable events

Create:

```python
def match_courses_to_timetable(agent: dict, courses: list[dict], timetable_index: dict, rng) -> list[dict]:
    pass
```

For each course:

```txt
course_code -> possible timetable events
```

Selection rule:

```txt
1. Prefer timetable events whose course_code matches exactly.
2. If multiple sections exist, sample one section.
3. Avoid overlapping events in the student's schedule.
4. If no event exists, skip course and log COURSE_NOT_FOUND_IN_TIMETABLE.
```

Output:

```json
{
  "student_id": "S000001",
  "events": [
    {
      "event_id": "EVT_001234",
      "day": "Mon",
      "start_time": "07:30",
      "end_time": "09:10",
      "course_code": "CS106",
      "course_name": "Trí tuệ nhân tạo",
      "room_id": "C205",
      "building": "C",
      "floor": 2,
      "stress_weight": 3
    }
  ]
}
```

Sort events by:

```txt
day_index, start_time
```

---

# 13. Task 7 — Generate routes

Create:

```python
def generate_routes_for_schedule(agent: dict, schedule: dict, G: nx.Graph, config: dict, route_cache: dict) -> list[dict]:
    pass
```

For each day, consider consecutive events.

Generate route only if:

```txt
same day
event_i.end_time <= event_j.start_time
from_room != to_room
both rooms exist in graph
```

Route result:

```json
{
  "route_id": "R000001",
  "student_id": "S000001",
  "day": "Mon",
  "from_event_id": "EVT_001",
  "to_event_id": "EVT_002",
  "from_room": "C205",
  "to_room": "B1.14",
  "route_choice_mode": "utility_based_choice",
  "behavior_profile": "efficient",
  "path_nodes": [],
  "path_edges": [],
  "total_distance": 0,
  "estimated_walk_time_seconds": 0,
  "number_of_buildings_passed": 0,
  "number_of_floor_changes": 0,
  "transition_available_minutes": 20,
  "is_late_risk": false
}
```

---

## 13.1. Route mode: shortest_path

Use Dijkstra:

```python
nx.shortest_path(G, source, target, weight="distance")
```

Cost:

```txt
distance
```

This is the baseline.

---

## 13.2. Route mode: k_shortest_paths

Use:

```python
nx.shortest_simple_paths(G, source, target, weight="distance")
```

Take first K paths.

If graph is large, stop after K.

Default:

```txt
K = 3
```

Select path using distance-based softmax:

```txt
P(route_i) = exp(-cost_i / temperature) / sum_j exp(-cost_j / temperature)
```

---

## 13.3. Route mode: utility_based_choice

Generate K candidate paths.

For each path compute:

```txt
route_cost =
    distance_weight * total_distance
  + stair_weight * number_of_floor_changes
  + building_change_weight * number_of_buildings_passed
  + turn_weight * approximate_turn_count
  + congestion_weight * expected_congestion
  - familiarity_weight * familiarity_bonus
  + random_noise
```

Then sample using softmax.

Suggested profile weights:

```json
{
  "efficient": {
    "distance_weight": 1.3,
    "stair_weight": 0.8,
    "building_change_weight": 0.5,
    "turn_weight": 0.4,
    "congestion_weight": 0.2,
    "familiarity_weight": 0.2,
    "temperature": 0.4
  },
  "familiar": {
    "distance_weight": 1.0,
    "stair_weight": 0.6,
    "building_change_weight": 0.5,
    "turn_weight": 0.4,
    "congestion_weight": 0.2,
    "familiarity_weight": 1.0,
    "temperature": 0.6
  },
  "new_student": {
    "distance_weight": 1.0,
    "stair_weight": 0.8,
    "building_change_weight": 0.7,
    "turn_weight": 1.2,
    "congestion_weight": 0.2,
    "familiarity_weight": 0.1,
    "temperature": 0.5
  },
  "crowd_avoiding": {
    "distance_weight": 0.9,
    "stair_weight": 0.6,
    "building_change_weight": 0.5,
    "turn_weight": 0.5,
    "congestion_weight": 1.3,
    "familiarity_weight": 0.3,
    "temperature": 0.7
  },
  "explorer": {
    "distance_weight": 0.7,
    "stair_weight": 0.5,
    "building_change_weight": 0.4,
    "turn_weight": 0.3,
    "congestion_weight": 0.2,
    "familiarity_weight": 0.2,
    "temperature": 1.2
  }
}
```

Important:

```txt
Do not describe behavior profiles as mental health diagnoses.
They are only simulation parameters.
```

---

# 14. Route cache

Use route caching.

Cache key:

```python
(source_room, target_room, behavior_profile, route_choice_mode)
```

For shortest path:

```python
route_cache[(source, target, "any", "shortest_path")]
```

For utility-based route choice:

```python
route_cache[(source, target, profile, "utility_based_choice")]
```

If congestion feedback is disabled, cached routes are safe.

If congestion feedback is enabled, cache should include a time window:

```python
(source, target, profile, mode, time_window)
```

---

# 15. Task 8 — Traffic accumulation

Create:

```python
def accumulate_traffic(routes: list[dict]) -> tuple[dict, dict]:
    pass
```

For every route:

```txt
For each node in path_nodes:
    node_traffic[node_id].total_count += 1

For each edge in path_edges:
    edge_traffic[edge_id].total_count += 1
```

Also count by time window:

```txt
morning
noon
afternoon
evening
all_day
weekly
```

Time window rules:

```txt
morning:    before 11:30
noon:       11:30 - 13:30
afternoon:  13:30 - 17:30
evening:    after 17:30
```

---

# 16. Task 9 — Stress-weighted traffic

In addition to pure traffic, compute stress-weighted traffic.

For a route from event A to event B:

```txt
route_stress = max(stress_weight(A), stress_weight(B))
```

or:

```txt
route_stress = average(stress_weight(A), stress_weight(B))
```

Use the first version for simplicity:

```txt
max
```

For every node/edge in the path:

```txt
stress_traffic += route_stress
```

This output will be used later by Node 2.1.

---

# 17. Task 10 — Heatmap generation

Create:

```python
def generate_heatmap_data(node_traffic: dict, edge_traffic: dict) -> dict:
    pass
```

Output:

```json
{
  "scope": "campus",
  "time_window": "weekly",
  "items": [
    {
      "id": "UIT-OUTDOOR-C-FRONT",
      "type": "node",
      "value": 340,
      "normalized_value": 0.82,
      "stress_value": 620,
      "normalized_stress_value": 0.75
    }
  ]
}
```

Normalize values:

```txt
normalized_value = value / max_value
normalized_stress_value = stress_value / max_stress_value
```

If max is zero, normalized value should be zero.

---

# 18. Task 11 — Export outputs

Create:

```python
def export_json(data, path: str) -> None:
    pass
```

Export:

```txt
student_agents.json
student_schedules.json
generated_routes.json
node_traffic.json
edge_traffic.json
heatmap_data.json
simulation_summary.json
simulation_warnings.json
```

---

# 19. Task 12 — Validation

Create:

```python
def validate_simulation_outputs(...):
    pass
```

Check:

```txt
1. Every student has valid major, year, profile.
2. Every assigned course has course_code.
3. Every timetable event has valid room_id.
4. Every room_id used in routes exists in graph.
5. Every route starts at from_room.
6. Every route ends at to_room.
7. Every path edge exists in graph.
8. Traffic counts are non-negative.
9. Node traffic equals route node traversals.
10. Edge traffic equals route edge traversals.
11. Simulation is reproducible with fixed random seed.
```

Write report:

```txt
outputs/node_1_2/simulation_validation_report.json
```

---

# 20. Main script

Create:

```txt
simulate_students.py
```

Expected command:

```bash
python simulate_students.py --config simulation_config.json
```

Pipeline inside script:

```python
def main():
    config = load_config("simulation_config.json")
    rng = init_random(config["random_seed"])

    G = load_all_graphs(config["graph_paths"])
    timetable = load_timetable(config["timetable_path"])
    curriculum = load_curriculum(config["curriculum_path"])

    agents = generate_agents(config)
    schedules = []
    routes = []
    warnings = []

    route_cache = {}

    for agent in agents:
        courses = assign_courses_to_agent(agent, curriculum, rng)
        schedule = match_courses_to_timetable(agent, courses, timetable, rng)
        student_routes = generate_routes_for_schedule(agent, schedule, G, config, route_cache)

        schedules.append(schedule)
        routes.extend(student_routes)

    node_traffic, edge_traffic = accumulate_traffic(routes)
    heatmap = generate_heatmap_data(node_traffic, edge_traffic)

    export_all_outputs(...)
    validate_simulation_outputs(...)
```

---

# 21. Performance requirements

The code should support:

```txt
1,000 - 10,000 simulated students
one full weekly timetable
thousands of route queries
```

Do:

```txt
Use route cache.
Use dictionaries for lookup.
Use sets for room existence checks.
Avoid nested loops over all events when matching courses.
Index timetable by course_code.
Index curriculum by major/year.
```

Avoid:

```txt
Scanning all timetable rows for every student and every course.
Running Dijkstra repeatedly for identical source-target pairs.
Writing huge debug logs.
Storing unnecessary per-step coordinates.
```

---

# 22. Minimum viable version

If time is limited, implement this first:

```txt
1. Load global graph.
2. Load normalized timetable.
3. Load normalized curriculum.
4. Generate 1000 students.
5. Assign courses using sample teaching plan.
6. Match timetable by course_code.
7. Generate shortest_path routes.
8. Accumulate traffic.
9. Export node_traffic and edge_traffic.
```

After that, add:

```txt
k_shortest_paths
utility_based_choice
stress-weighted traffic
heatmap
profile-specific behavior
```

---

# 23. Acceptance criteria

Node 1.2 is successful if:

```txt
1. The simulator runs from one command.
2. It generates at least 1000 virtual students.
3. It creates weekly schedules for students.
4. It generates routes between consecutive classes.
5. Routes can cross buildings through campus graph.
6. It accumulates node traffic and edge traffic.
7. It exports heatmap-compatible JSON.
8. It uses route caching.
9. It logs missing rooms/courses instead of crashing.
10. The output is reproducible with a fixed random seed.
```

---

# 24. Important reporting note

In the report, describe this as:

```txt
agent-based simulation
```

Do not describe it as real student tracking.

Do not claim that the generated routes are exact real behavior.

Correct wording:

```txt
The generated routes approximate plausible movement patterns based on curriculum, timetable, and graph-based route choice assumptions.
```

Incorrect wording:

```txt
This shows exactly how students move.
```

---

# 25. Connection to later nodes

Node 1.2 produces:

```txt
traffic
stress-weighted traffic
route exposure
heatmap data
```

These will support:

```txt
Node 2.1 - Stress Heatmap
Node 2.2 - Visibility and Privacy Scoring
Node 3.1 - Final Counseling Room Placement Optimization
```

The key handoff files are:

```txt
node_traffic.json
edge_traffic.json
heatmap_data.json
generated_routes.json
```
