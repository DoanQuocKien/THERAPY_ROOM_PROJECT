from __future__ import annotations

from graph_utils import load_all_graphs, shortest_path


SAMPLES = [
    ("A-F1-TOP-ROOM-01", "C205"),
    ("B1.22", "E12.2"),
    ("UIT-GATE-A", "D-F1-ROOM-04"),
]


def summarize(path: list[str]) -> tuple[list[str], list[str]]:
    buildings = []
    floors = []
    for node_id in path:
        if node_id.startswith("UIT-"):
            building = "UIT"
            floor = "campus"
        else:
            building = node_id[0]
            floor = "unknown"
            parts = node_id.split("-")
            for part in parts:
                if part.startswith("F"):
                    floor = part
                    break
            if "." in node_id and node_id[1].isdigit():
                floor = f"F{node_id[1]}"
        if building not in buildings:
            buildings.append(building)
        if floor not in floors:
            floors.append(floor)
    return buildings, floors


def print_path(start: str, end: str) -> None:
    graph = load_all_graphs()
    path, distance = shortest_path(graph, start, end)
    buildings, floors = summarize(path)
    print(f"Start: {start}")
    print(f"End:   {end}")
    print("Shortest path:")
    for index, node_id in enumerate(path):
        prefix = "   " if index == 0 else "-> "
        print(f"{prefix}{node_id}")
    print(f"Total distance: {distance:.1f}")
    print(f"Number of nodes: {len(path)}")
    print(f"Buildings passed: {', '.join(buildings)}")
    print(f"Floors passed: {', '.join(floors)}")
    print()


def main() -> None:
    for start, end in SAMPLES:
        print_path(start, end)


if __name__ == "__main__":
    main()
