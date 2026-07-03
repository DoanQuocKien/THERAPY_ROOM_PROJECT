# 07_NODE_1_2_ROUTE_SIMULATION_FRAMEWORK.md

# CS117 Node 1.2 — Student Route Simulation Framework

## 1. Goal

This document defines the high-level framework for **Node 1.2: Student Route Simulation**.

The goal of Node 1.2 is to generate simulated student movement routes across the UIT campus based on:

```txt
1. The full campus graph from Node 1.1
2. Weekly classroom timetable data
3. Curriculum data for each major
4. Student cohort assumptions
5. Route choice behavior assumptions
```

This is not a real tracking system.
This is not based on real personal student data.
This is an **agent-based simulation** for computational thinking and spatial analysis.

The output of this node will be used later to generate:

```txt
1. Simulated student routes
2. Node traffic counts
3. Edge traffic counts
4. Movement heatmaps
5. Visibility score for counseling room placement
```

---

## 2. Important scope rule

Keep the implementation simple.

Use:

```txt
Python
JSON / CSV
NetworkX
Matplotlib / Plotly if needed
```

Do not build:

```txt
backend
database
web app
login system
complex frontend
real-time system
```

This project should remain a lightweight local simulation tool.

---

## 3. Required reference files

This framework assumes that the following files will exist later.

The exact format of these files will be defined in separate Markdown documents.

```txt
campus_graph.json
building_a_graph.json
building_b_graph.json
building_c_graph.json
building_d_graph.json
building_e_graph.json

timetable_data.csv or timetable_data.json
curriculum_data.csv or curriculum_data.json
```

Important:

```txt
The timetable and curriculum formats are NOT defined in this file.
They will be documented later in separate files.
```

Expected future specification files:

```txt
08_TIMETABLE_INPUT_SPEC.md
09_CURRICULUM_INPUT_SPEC.md
10_SIMULATION_IMPLEMENTATION_TASKS.md
```

---

## 4. Conceptual model

Node 1.2 uses an agent-based simulation model.

Each simulated student is an agent.

Each agent has:

```txt
student_id
major
year
class_group
behavior_profile
weekly_schedule
generated_routes
```

Each agent moves from one scheduled class to the next.

For example:

```txt
Monday 07:30 - 09:10
Course: CS117
Room: C205

Monday 09:30 - 11:10
Course: MA005
Room: B1.14
```

The simulation generates a route:

```txt
C205 → ... → B1.14
```

using the graph from Node 1.1.

---

## 5. Why not only shortest path?

The baseline route is the shortest path.

However, real human movement is not always perfectly shortest-path optimal.

Therefore, the simulation should support multiple route choice modes:

```txt
1. shortest_path
2. k_shortest_paths
3. utility_based_choice
```

The default baseline is:

```txt
shortest_path
```

The recommended realistic mode is:

```txt
utility_based_choice
```

---

## 6. Route choice modes

## 6.1. Mode 1 — shortest_path

This is the simplest mode.

For each pair of rooms:

```txt
source_room → target_room
```

Run Dijkstra on the full UIT graph.

Cost:

```txt
cost(edge) = distance
```

Use this mode as the baseline.

---

## 6.2. Mode 2 — k_shortest_paths

Instead of generating only one path, generate several reasonable candidate paths.

Example:

```txt
route_1: 120 distance units
route_2: 135 distance units
route_3: 148 distance units
```

Then select one route based on probability.

Shorter routes should have higher probability, but longer reasonable routes may still be selected.

This creates route diversity.

---

## 6.3. Mode 3 — utility_based_choice

This is the preferred mode for the final simulation.

Each route is scored by a utility/cost function.

Example:

```txt
route_cost =
    distance_weight   * total_distance
  + turn_weight       * number_of_turns
  + congestion_weight * expected_congestion
  - familiarity_bonus * familiarity_score
  + stair_penalty     * number_of_stair_transitions
  + randomness_noise
```

The route with lower cost is more likely to be selected.

This keeps the simulation more realistic than pure shortest path while still remaining simple enough to code.

---

## 7. Behavior profiles

Each simulated student should be assigned one behavior profile.

Recommended profiles:

```txt
efficient
familiar
new_student
crowd_avoiding
explorer
```

---

## 7.1. efficient

The student mainly wants to arrive quickly.

Characteristics:

```txt
high distance penalty
low randomness
low exploration
```

Suggested use:

```txt
students with dense schedules
students with short transition time
```

---

## 7.2. familiar

The student prefers familiar routes.

Characteristics:

```txt
medium distance penalty
high familiarity bonus
medium randomness
```

Suggested use:

```txt
year 3 and year 4 students
```

---

## 7.3. new_student

The student prefers easy-to-understand routes.

Characteristics:

```txt
high turn penalty
high visibility preference
low familiarity
```

Suggested use:

```txt
year 1 students
```

---

## 7.4. crowd_avoiding

The student avoids crowded paths.

Characteristics:

```txt
high congestion penalty
medium distance penalty
```

Important:

```txt
This is only a simulation profile.
Do not describe this as a mental health diagnosis.
```

---

## 7.5. explorer

The student sometimes takes slightly longer paths.

Characteristics:

```txt
higher randomness
lower distance penalty
higher exploration
```

Suggested use:

```txt
small percentage of agents
used to create realistic variation
```

---

## 8. Student agent schema

Each generated student should follow this structure:

```json
{
  "student_id": "S000001",
  "major": "KHMT",
  "year": 2,
  "class_group": "KHMT2024_A",
  "behavior_profile": "familiar",
  "walking_speed": 1.25,
  "familiarity": 0.75,
  "schedule_density": 0.60
}
```

Required fields:

```txt
student_id
major
year
class_group
behavior_profile
walking_speed
familiarity
schedule_density
```

Optional fields:

```txt
stress_sensitivity
notes
```

Do not use any real student identity.

All students are simulated agents.

---

## 9. Schedule event schema

Each student schedule is a list of events.

```json
{
  "student_id": "S000001",
  "events": [
    {
      "day": "Mon",
      "start_time": "07:30",
      "end_time": "09:10",
      "course_code": "CS117",
      "course_name": "Tư duy tính toán",
      "room_id": "C205",
      "building": "C",
      "floor": 2
    }
  ]
}
```

Required fields:

```txt
day
start_time
end_time
course_code
room_id
building
floor
```

The exact source format of timetable data will be defined later in:

```txt
08_TIMETABLE_INPUT_SPEC.md
```

---

## 10. Curriculum reference

The curriculum file will define which courses are likely to be taken by students of each major and year.

Conceptual mapping:

```txt
major + year → list of possible courses
```

Example:

```json
{
  "major": "KHMT",
  "year": 2,
  "courses": [
    "CS117",
    "DSA",
    "MA005"
  ]
}
```

The exact source format of curriculum data will be defined later in:

```txt
09_CURRICULUM_INPUT_SPEC.md
```

---

## 11. Route output schema

Each generated route should follow this structure:

```json
{
  "route_id": "R000001",
  "student_id": "S000001",
  "day": "Mon",
  "from_event_index": 0,
  "to_event_index": 1,
  "from_room": "C205",
  "to_room": "B1.14",
  "route_choice_mode": "utility_based_choice",
  "behavior_profile": "familiar",
  "path_nodes": [
    "C205",
    "C205-ACCESS",
    "C-F2-CORRIDOR-03",
    "C-F1-BUILDING-ENTRANCE",
    "UIT-OUTDOOR-C-FRONT",
    "UIT-OUTDOOR-B-FRONT",
    "B-F1-BUILDING-ENTRANCE",
    "B1.14-ACCESS",
    "B1.14"
  ],
  "path_edges": [],
  "total_distance": 180.0,
  "estimated_walk_time_seconds": 145,
  "number_of_buildings_passed": 2,
  "number_of_floor_changes": 1
}
```

Required fields:

```txt
route_id
student_id
day
from_room
to_room
route_choice_mode
behavior_profile
path_nodes
total_distance
estimated_walk_time_seconds
```

---

## 12. Traffic output schema

After generating all routes, accumulate traffic on nodes and edges.

## 12.1. Node traffic

```json
{
  "node_id": "UIT-OUTDOOR-C-FRONT",
  "total_count": 340,
  "morning_count": 120,
  "noon_count": 90,
  "afternoon_count": 110,
  "evening_count": 20
}
```

## 12.2. Edge traffic

```json
{
  "edge_id": "UIT-OUTDOOR-C-FRONT__UIT-INTERSECTION-CANTEEN",
  "source": "UIT-OUTDOOR-C-FRONT",
  "target": "UIT-INTERSECTION-CANTEEN",
  "total_count": 280,
  "morning_count": 100,
  "noon_count": 75,
  "afternoon_count": 90,
  "evening_count": 15
}
```

---

## 13. Heatmap output schema

Heatmap data should be derived from node and edge traffic.

```json
{
  "scope": "campus",
  "time_window": "morning",
  "items": [
    {
      "id": "UIT-OUTDOOR-C-FRONT",
      "type": "node",
      "value": 340,
      "normalized_value": 0.82
    }
  ]
}
```

Potential time windows:

```txt
morning
noon
afternoon
evening
all_day
weekly
```

---

## 14. Simulation pipeline

The full simulation pipeline should be:

```txt
Step 1:
  Load all building graphs and campus graph.

Step 2:
  Merge all graphs into one global graph G_UIT.

Step 3:
  Load timetable data.
  The format will be specified later.

Step 4:
  Load curriculum data.
  The format will be specified later.

Step 5:
  Generate N simulated student agents.

Step 6:
  Assign major, year, class group, and behavior profile to each agent.

Step 7:
  Assign courses to each agent based on curriculum.

Step 8:
  Match assigned courses to timetable sections and rooms.

Step 9:
  Sort each student's weekly events by day and time.

Step 10:
  For each consecutive pair of events:
      generate route from previous room to next room.

Step 11:
  Accumulate node and edge traffic.

Step 12:
  Export all simulation outputs.
```

---

## 15. Recommended output files

Node 1.2 should generate:

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

## 16. Performance requirements

The simulation should support thousands of students.

Target scale:

```txt
1,000 to 10,000 simulated students
1 week of schedules
multiple route queries per student
```

To avoid unnecessary repeated computation:

```txt
Use route caching.
```

Recommended cache key:

```txt
(source_room, target_room, behavior_profile, route_choice_mode)
```

Example:

```python
route_cache[(source_room, target_room, profile, mode)] = route_result
```

Many students will share the same room-to-room transitions, so caching will greatly reduce repeated Dijkstra calls.

---

## 17. Important optimization notes

Do not run Dijkstra blindly for every transition if the same transition appears many times.

Use:

```txt
1. route cache
2. precomputed room node list
3. edge ID normalization
4. lightweight JSON output
5. batch traffic accumulation
```

Recommended edge ID format:

```txt
source__target
```

For bidirectional edges, normalize:

```txt
min(source, target)__max(source, target)
```

---

## 18. Validation checklist

The simulation is valid if:

```txt
1. Every generated student has a major and year.
2. Every generated student has a behavior profile.
3. Every scheduled event has a valid room.
4. Every room exists in the global graph.
5. Every route has at least one path.
6. Every route starts at the correct source room.
7. Every route ends at the correct target room.
8. Traffic counts are non-negative.
9. Edge traffic only counts valid graph edges.
10. Global graph remains connected.
11. Simulation output can be reproduced using a fixed random seed.
```

---

## 19. Random seed

The simulation must support fixed random seed.

Example:

```python
RANDOM_SEED = 42
```

This is important because the result should be reproducible for report writing and debugging.

---

## 20. Configuration file

Create a config file later:

```txt
simulation_config.json
```

Suggested fields:

```json
{
  "random_seed": 42,
  "num_students": 5000,
  "route_choice_mode": "utility_based_choice",
  "k_shortest_paths": 3,
  "default_walking_speed": 1.25,
  "enable_route_cache": true,
  "output_dir": "outputs/node_1_2"
}
```

---

## 21. Expected implementation files

Codex should eventually create:

```txt
simulation_config.json

simulate_students.py
generate_agents.py
assign_courses.py
match_timetable.py
route_generation.py
traffic_accumulation.py
export_simulation_outputs.py
validate_simulation.py
```

But in the first implementation, it is acceptable to keep the code simpler:

```txt
simulate_students.py
```

with helper functions inside one file.

---

## 22. Things not to do

Do not:

```txt
1. Use real student personal data.
2. Claim the simulation represents exact real behavior.
3. Diagnose mental health from route choice.
4. Overcomplicate the app architecture.
5. Build a web app.
6. Build a database.
7. Make the simulation depend on manual clicking.
```

---

## 23. How Node 1.2 connects to later nodes

Node 1.2 produces traffic and route data.

These outputs will later support:

```txt
Node 2.1:
  Stress heatmap generation

Node 2.2:
  Visibility/privacy quantification

Node 3.1:
  Multi-objective optimization for counseling room placement
```

Main idea:

```txt
More simulated traffic through a node
→ higher visibility potential
→ stronger candidate for counseling room placement
```

But visibility must later be balanced against privacy and stigma risk.

---

## 24. Summary

Node 1.2 should simulate student movement using:

```txt
agent-based simulation
curriculum-based course assignment
timetable-based room matching
graph-based route generation
traffic accumulation
heatmap export
```

The implementation should be simple, reproducible, and compatible with the graph JSON files from Node 1.1.

The timetable and curriculum input formats will be defined later in separate Markdown files.
