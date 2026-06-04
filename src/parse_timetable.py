from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

from graph_utils import load_all_graphs


ROOT = Path(__file__).resolve().parents[1]


DAY_MAP = {
    "mon": "Mon",
    "monday": "Mon",
    "thu 2": "Mon",
    "tue": "Tue",
    "tuesday": "Tue",
    "thu 3": "Tue",
    "wed": "Wed",
    "wednesday": "Wed",
    "thu 4": "Wed",
    "thu": "Thu",
    "thursday": "Thu",
    "thu 5": "Thu",
    "fri": "Fri",
    "friday": "Fri",
    "thu 6": "Fri",
    "sat": "Sat",
    "saturday": "Sat",
    "thu 7": "Sat",
    "sun": "Sun",
    "sunday": "Sun",
    "chu nhat": "Sun",
}
PERIOD_TIME = {
    1: ("07:30", "08:15"),
    2: ("08:15", "09:00"),
    3: ("09:15", "10:00"),
    4: ("10:00", "10:45"),
    5: ("10:45", "11:30"),
    6: ("13:00", "13:45"),
    7: ("13:45", "14:30"),
    8: ("14:45", "15:30"),
    9: ("15:30", "16:15"),
    10: ("16:15", "17:00"),
}


def normalize_course_code(raw_code: str | None) -> str:
    if raw_code is None:
        return ""
    return re.sub(r"\s+", "", str(raw_code)).upper()


def normalize_room_id(raw_room: str | None) -> str:
    if raw_room is None:
        return ""
    value = re.sub(r"\s+", "", str(raw_room)).upper()
    match = re.match(r"^E0+(\d+\..+)$", value)
    if match:
        return f"E{match.group(1)}"
    return value


def infer_building_and_floor(room_id: str) -> tuple[str | None, int | None]:
    if not room_id:
        return None, None
    if room_id.startswith(("A-", "D-")):
        match = re.search(r"-F(\d+)-", room_id)
        return room_id[0], int(match.group(1)) if match else None
    if room_id.startswith("B"):
        match = re.match(r"B(\d+)\.", room_id)
        return "B", int(match.group(1)) if match else None
    if room_id.startswith("C"):
        match = re.match(r"C(\d)", room_id)
        return "C", int(match.group(1)) if match else None
    if room_id.startswith("E"):
        match = re.match(r"E(\d+)\.", room_id)
        return "E", int(match.group(1)) if match else None
    return None, None


def normalize_day(raw_day: str | None) -> str | None:
    if raw_day is None:
        return None
    value = str(raw_day).strip().lower()
    value = value.replace("ứ", "u").replace("ủ", "u").replace("ậ", "a").replace("ả", "a")
    return DAY_MAP.get(value, DAY_MAP.get(value[:3]))


def parse_periods(raw_period: str | int | None) -> tuple[int | None, int | None]:
    if raw_period is None:
        return None, None
    numbers = [int(item) for item in re.findall(r"\d+", str(raw_period))]
    if not numbers:
        return None, None
    return min(numbers), max(numbers)


def load_raw_timetable(path: str):
    source = Path(path)
    if not source.is_absolute():
        source = ROOT / source
    if not source.exists():
        return seed_timetable_rows()
    if source.suffix.lower() == ".json":
        return json.loads(source.read_text(encoding="utf-8"))
    if source.suffix.lower() == ".csv":
        with source.open("r", encoding="utf-8-sig", newline="") as file:
            return list(csv.DictReader(file))
    raise ValueError(f"Unsupported timetable input format: {source.suffix}")


def seed_timetable_rows() -> list[dict]:
    courses = [
        ("IT001", "Intro Programming", "B1.22"),
        ("MA006", "Calculus", "C102"),
        ("MA003", "Linear Algebra", "C205"),
        ("SS006", "General Law", "A-F1-TOP-ROOM-01"),
        ("ENG01", "English 1", "E1.1"),
        ("IT002", "OOP", "B2.14"),
        ("IT003", "Data Structures", "C205"),
        ("MA004", "Discrete Math", "C213"),
        ("IT004", "Database", "B3.10"),
        ("IT005", "Networks", "C315"),
        ("IT007", "Operating Systems", "E3.2"),
        ("CS106", "Artificial Intelligence", "C205"),
        ("CS114", "Machine Learning", "E4.2"),
        ("CS112", "Algorithm Analysis", "B4.12"),
        ("DS200", "Big Data Analysis", "E8.1"),
        ("DS201", "Deep Learning DS", "C315"),
        ("CE103", "Microprocessors", "B5.10"),
        ("CE224", "Embedded Systems", "E6.1"),
        ("IS201", "Information Systems Analysis", "B1.14"),
        ("IS210", "DBMS", "C205"),
        ("SE104", "Software Engineering Intro", "B2.08"),
        ("SE113", "Software Testing", "E4.4"),
        ("NT101", "Network Fundamentals", "C207"),
        ("NT118", "Mobile Networking Apps", "E3.4"),
        ("AT101", "Security Fundamentals", "C209"),
        ("CS117", "Computational Thinking", "A-F1-TOP-ROOM-03"),
    ]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    periods = [(1, 3), (4, 5), (6, 7), (8, 10)]
    rows = []
    index = 0
    for course_code, course_name, room_id in courses:
        for section in range(2):
            day = days[(index + section) % len(days)]
            start_period, end_period = periods[(index + section) % len(periods)]
            rows.append({
                "course_code": course_code,
                "course_name": course_name,
                "class_group": f"{course_code}.G{section + 1}",
                "section_id": f"{course_code}.G{section + 1}.1",
                "room_id": room_id,
                "day": day,
                "start_period": start_period,
                "end_period": end_period,
                "event_type": "lecture",
                "source_file": "seed",
                "raw_sheet": "seed",
            })
        index += 1
    return rows


def normalize_timetable(raw_data) -> list[dict]:
    events = []
    for index, row in enumerate(raw_data, start=1):
        course_code = normalize_course_code(row.get("course_code") or row.get("Course") or row.get("Ma MH"))
        room_id = normalize_room_id(row.get("room_id") or row.get("room") or row.get("Phong"))
        building, floor = infer_building_and_floor(room_id)
        start_period, end_period = parse_periods(row.get("period") or row.get("Tiet") or row.get("start_period"))
        if row.get("end_period"):
            _, explicit_end = parse_periods(row.get("end_period"))
            end_period = explicit_end
        start_time = row.get("start_time") or (PERIOD_TIME[start_period][0] if start_period in PERIOD_TIME else None)
        end_time = row.get("end_time") or (PERIOD_TIME[end_period][1] if end_period in PERIOD_TIME else None)
        events.append({
            "event_id": f"EVT_{index:06d}",
            "source_file": row.get("source_file"),
            "raw_sheet": row.get("raw_sheet"),
            "academic_year": row.get("academic_year"),
            "semester": row.get("semester"),
            "week_pattern": row.get("week_pattern", "weekly"),
            "course_code": course_code,
            "course_name": str(row.get("course_name") or row.get("Course Name") or course_code).strip(),
            "class_group": row.get("class_group"),
            "section_id": row.get("section_id"),
            "room_id": room_id,
            "building": building,
            "floor": floor,
            "day": normalize_day(row.get("day")) or row.get("day"),
            "start_period": start_period,
            "end_period": end_period,
            "start_time": start_time,
            "end_time": end_time,
            "event_type": row.get("event_type", "unknown"),
            "capacity_estimate": row.get("capacity_estimate"),
            "notes": row.get("notes", ""),
        })
    return events


def validate_timetable(events: list[dict], graph_room_ids: set[str] | None = None) -> dict:
    warnings = []
    errors = []
    seen = set()
    valid_days = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}
    for event in events:
        event_id = event["event_id"]
        if event_id in seen:
            errors.append({"event_id": event_id, "type": "DUPLICATE_EVENT_ID", "message": "Duplicate event_id."})
        seen.add(event_id)
        for field in ["course_code", "room_id", "day", "start_period", "end_period", "start_time", "end_time"]:
            if event.get(field) in (None, ""):
                errors.append({"event_id": event_id, "type": "MISSING_FIELD", "message": f"Missing {field}."})
        if event.get("day") not in valid_days:
            errors.append({"event_id": event_id, "type": "INVALID_DAY", "message": f"Invalid day {event.get('day')}."})
        if event.get("start_period") and event.get("end_period") and event["start_period"] > event["end_period"]:
            errors.append({"event_id": event_id, "type": "INVALID_PERIOD", "message": "start_period > end_period."})
        if graph_room_ids and event.get("room_id") not in graph_room_ids:
            warnings.append({"event_id": event_id, "type": "ROOM_NOT_FOUND_IN_GRAPH", "message": f"Room {event.get('room_id')} does not exist in graph."})
    return {
        "total_events": len(events),
        "valid_events": max(0, len(events) - len(errors)),
        "invalid_events": len(errors),
        "warnings": warnings,
        "errors": errors,
    }


def export_normalized_timetable(events: list[dict], output_path: str) -> None:
    output = Path(output_path)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(events, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw/TKB Phong.xlsx")
    parser.add_argument("--output", default="data/normalized/normalized_timetable.json")
    args = parser.parse_args()

    raw = load_raw_timetable(args.input)
    events = normalize_timetable(raw)
    graph = load_all_graphs()
    graph_room_ids = {node_id for node_id, attrs in graph.nodes(data=True) if attrs.get("type") == "room"}
    report = validate_timetable(events, graph_room_ids)
    export_normalized_timetable(events, args.output)
    report_path = ROOT / "outputs" / "validation" / "timetable_validation_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {args.output}")
    print(f"Saved {report_path}")


if __name__ == "__main__":
    main()
