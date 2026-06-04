# UIT Campus Graph And Route Simulation

This project models UIT campus movement as weighted graphs and uses those graphs to simulate student routes between scheduled classes.

The graph data covers:

- Campus outdoor paths, gates, building entrances, and canteen links
- Building A detailed floor graphs
- Simplified Building B, C, D, and E floor graphs
- Room access nodes embedded on corridor roads
- Shortest-path demos and generated graph images
- Node 1.2 student route simulation using normalized timetable and curriculum JSON

## Quick Start

Run all commands from the project root:

```bash
cd D:/CS117/THERAPY_ROOM_PROJECT
```

Install dependencies once:

```bash
pip install networkx matplotlib
```

Validate the full campus/building graph:

```bash
python src/validate_all_graphs.py
```

Generate the most useful graph images:

```bash
python src/visualize_building_a.py
python src/visualize_campus.py
python src/visualize_building.py B
```

Run shortest-path demos:

```bash
python src/shortest_path_demo.py
python src/shortest_path_global.py
```

Run the student route simulation:

```bash
python src/simulate_students.py --config config/simulation_config.json
python src/validate_simulation.py
```

Generate weekly whole-campus heatmap visuals:

```bash
python src/visualize_weekly_heatmap.py
python src/visualize_weekly_heatmap.py --metric stress --output outputs/heatmaps/weekly_graph_stress_heatmap.html
```

## Project Layout

```txt
THERAPY_ROOM_PROJECT/
  src/                 Python scripts
  config/              Simulation configuration
  data/
    graphs/            Campus and building graph JSON
    normalized/        Timetable and curriculum JSON used by simulation
  assets/              Optional floor plan images
  outputs/             Generated images, reports, and simulation results
```

Important files:

- `config/simulation_config.json`: simulation settings and input/output paths
- `data/graphs/campus_graph.json`: outdoor campus graph
- `data/graphs/building_a_graph.json`: detailed Building A graph
- `data/graphs/building_b_graph.json` to `building_e_graph.json`: other building graphs
- `data/normalized/normalized_timetable.json`: normalized timetable input
- `data/normalized/normalized_curriculum_all.json`: merged normalized curriculum input

## Academic Input Data

You can provide parsed timetable and curriculum data yourself. Place the files here:

```txt
data/normalized/normalized_timetable.json
data/normalized/normalized_curriculum_all.json
```

The simulation reads those paths from `config/simulation_config.json`.

Optional seed/parser scripts are still available:

```bash
python src/parse_timetable.py
python src/parse_curriculum.py --part PART_1
python src/parse_curriculum.py --part PART_2
python src/merge_curriculum_parts.py
```

Use those only when you want the project to generate or normalize seed academic data.

After changing timetable or curriculum JSON, audit and repair simple coverage gaps:

```bash
python src/repair_academic_coverage.py --dry-run
python src/repair_academic_coverage.py
```

The repair script appends clearly marked `INF_...` inferred timetable events only when it can find a related donor event and a non-overlapping graph room. Bigger unresolved gaps are written to `outputs/validation/academic_coverage_repair_report.json`.

## Simulation Behavior

The route simulation now models whole-day sample movement for each scheduled class day:

```txt
entry gate -> first class -> class/lunch movements -> final exit gate
```

Student cohort handling:

- Year 1 uses active semester `2`
- Year 2 uses active semester `4`
- Year 3 uses active semester `6`
- Year 4 uses active semester `8`

The full `semester_preference` field is still stored as `[1, 2]`, `[3, 4]`, `[5, 6]`, or `[7, 8]`, but course assignment prioritizes the active second semester for the current dataset.

Gate behavior:

- Each student receives an `entry_gate`.
- Students also receive a `transport_mode`, `entry_node`, and `exit_node`.
- Personal-transport students use the garage node, which links back to Gate A.
- Public-transport students enter mostly through Gate B and exit mostly through Gate A.

Garage behavior:

- The graph includes `UIT-GARAGE`.
- The garage links to Gate A, Building A ring left/top, Building B by a long back road, and Building E by a rough E/A crossing route.
- Personal-transport share defaults to `70%`.
- If a personal-transport student's final class is in Building B:
  - `50%` use the direct B back road to the garage
  - `50%` route through Building A toward the garage
- If the final class is in Building C:
  - `90%` route through E toward the garage
  - `10%` route through A toward the garage
- If the final class is in Building E:
  - `100%` route through E toward the garage
- Gate A public-transport entry is biased through Building A ring bottom right.
- Garage entry is biased through Building A ring left middle/top left.

Lunch behavior:

- Lunch movement is inserted when a student's class day crosses the lunch window.
- Lunch destinations are weighted in `config/simulation_config.json`.
- The default split is:
  - `54%` leave through `UIT-GATE-A`
  - `18%` leave through `UIT-GATE-B`
  - `18%` go to `UIT-CANTEEN`
  - `10%` go to the Building A library

Major population behavior:

- Major sampling uses `major_class_counts` in `config/simulation_config.json`.
- The assumption is that each class has the same size in each year.
- Normalized curriculum uses real major codes:
  - `TTNT`: Trí tuệ nhân tạo
  - `ATTT`: An toàn thông tin
  - `CNTT`: Công nghệ thông tin
  - `TMDT`: Thương mại điện tử
  - `HTTT`: Hệ thống thông tin
  - `CTTT`: Hệ thống thông tin chương trình tiên tiến
  - `KHDL`: Khoa học dữ liệu
  - `KHMT`: Khoa học máy tính
  - `KTMT`: Kỹ thuật máy tính
  - `MMTT`: Mạng máy tính và truyền thông dữ liệu
  - `KTPM`: Kỹ thuật phần mềm
  - `TKVM`: Thiết kế vi mạch
  - `TTDPT`: Truyền thông đa phương tiện
- Class-count weighting:
  - `KHMT`, `HTTT`: 4 classes
  - `TMDT`, `MMTT`, `TKVM`, `TTDPT`, `CTTT`: 2 classes
  - `TTNT`: 1 class
  - all other listed majors: 3 classes

Path randomness:

- Each student gets a `mental_instability_metric` and derived `path_randomness`.
- Higher `path_randomness` increases stochastic route choice temperature and random utility noise.
- This is a simulation assumption for route variability, not a diagnosis and not real student tracking.

## Graph Modeling Notes

Rooms are represented with an access node on the corridor path:

```txt
main path -> access node -> next access/main path
                  |
                room node
```

This means shortest paths move along corridor/access nodes and enter a room only when the room is the start or destination.

Building A details:

- Floor 1 uses an outer ring plus center corridors.
- Corner room access nodes sit on the outer ring roads, not on the center intersection.
- Floor 2 uses a diamond-like ring road without a center intersection.
- Floor 2 room access nodes sit directly on the diamond ring roads near the ring nodes.

## Common Commands

Regenerate graph JSON for campus and Buildings B to E:

```bash
python src/generate_multi_building_graphs.py
```

Validate all graph files:

```bash
python src/validate_all_graphs.py
```

Visualize one building:

```bash
python src/visualize_building.py B
python src/visualize_building.py C
python src/visualize_building.py D
python src/visualize_building.py E
```

Run simulation with a custom config:

```bash
python src/simulate_students.py --config config/simulation_config.json
```

Validate simulation output:

```bash
python src/validate_simulation.py --output-dir outputs/node_1_2
```

Generate scrollable weekly heatmap HTML:

```bash
python src/visualize_weekly_heatmap.py
python src/visualize_weekly_heatmap.py --metric stress --output outputs/heatmaps/weekly_graph_stress_heatmap.html
```

## Outputs

Generated files are kept out of the source folders.

Graph image outputs:

- `outputs/buildings/a/`
- `outputs/buildings/b/`
- `outputs/buildings/c/`
- `outputs/buildings/d/`
- `outputs/buildings/e/`
- `outputs/campus/`
- `outputs/paths/`

Simulation outputs:

- `outputs/node_1_2/student_agents.json`
- `outputs/node_1_2/student_schedules.json`
- `outputs/node_1_2/generated_routes.json`
- `outputs/node_1_2/node_traffic.json`
- `outputs/node_1_2/edge_traffic.json`
- `outputs/node_1_2/heatmap_data.json`
- `outputs/node_1_2/simulation_summary.json`
- `outputs/node_1_2/simulation_validation_report.json`

Heatmap outputs:

- `outputs/heatmaps/weekly_graph_heatmap.html`
- `outputs/heatmaps/weekly_graph_stress_heatmap.html`

The heatmap HTML draws the campus graph plus each building floor in one large scrollable SVG. Every graph node and edge is included; nodes or edges with no observed weekly traffic render in grey.

Validation reports:

- `outputs/validation/`
- `outputs/node_1_2/simulation_output_validation_report.json`

## Optional Floor Plan Images

If source map images are available, place them here:

```txt
assets/building_a_floor_1.jpg
assets/building_a_floor_2.jpg
```

`src/visualize_building_a.py` draws the graph over those images when they exist. If they are missing, the graph still renders normally.

## Troubleshooting

If a command cannot find a JSON file, make sure you are running it from the project root.

If simulation produces no routes, check that timetable `room_id` values match room node IDs in `data/graphs/`.

If graph validation fails, check for:

- Missing node IDs referenced by edges
- Duplicate node IDs
- Disconnected accessible graph sections
- Rooms without matching `ROOM-ID-ACCESS` nodes
