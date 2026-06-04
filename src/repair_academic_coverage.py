from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

from graph_utils import load_all_graphs


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_SEMESTERS = {2, 4, 6, 8}
DAY_ORDER = {"Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6, "Sun": 7}
TECH_PREFIXES = {"AI", "AT", "CE", "CS", "DS", "IE", "IS", "IT", "NT", "SE"}


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def load_json(path: str | Path) -> Any:
    return json.loads(resolve_path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, data: Any) -> None:
    output = resolve_path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def canonical_course_code(raw_code: Any) -> str:
    if raw_code is None:
        return ""
    code = "".join(str(raw_code).upper().split())
    if code.endswith(".1") or code.endswith(".2"):
        return code[:-2]
    return code


def course_prefix(code: str) -> str:
    return "".join(char for char in code if char.isalpha())


def optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def infer_year_from_semester(semester: int | None) -> int | None:
    return (semester + 1) // 2 if semester is not None else None


def collect_course_metadata(curriculum: dict) -> dict[str, dict]:
    metadata: dict[str, dict] = {}
    for major in curriculum.get("majors", []):
        major_id = major.get("major_id", "UNKNOWN")
        for course in major.get("curriculum_courses", []):
            code = canonical_course_code(course.get("course_code"))
            if not code:
                continue
            semester = optional_int(course.get("recommended_semester"))
            year = optional_int(course.get("recommended_year")) or infer_year_from_semester(semester)
            item = metadata.setdefault(code, {
                "course_code": code,
                "course_name": course.get("course_name") or code,
                "majors": set(),
                "semesters": set(),
                "years": set(),
                "groups": set(),
                "blocks": set(),
                "stress_weight": course.get("stress_weight", 2),
            })
            item["majors"].add(major_id)
            if semester is not None:
                item["semesters"].add(semester)
            if year is not None:
                item["years"].add(year)
            if course.get("course_group"):
                item["groups"].add(course["course_group"])
            if course.get("course_block"):
                item["blocks"].add(course["course_block"])

        for plan_item in major.get("sample_teaching_plan", []):
            code = canonical_course_code(plan_item.get("course_code"))
            if not code:
                continue
            semester = optional_int(plan_item.get("semester"))
            year = optional_int(plan_item.get("year")) or infer_year_from_semester(semester)
            item = metadata.setdefault(code, {
                "course_code": code,
                "course_name": plan_item.get("course_name") or code,
                "majors": set(),
                "semesters": set(),
                "years": set(),
                "groups": set(),
                "blocks": set(),
                "stress_weight": 2,
            })
            item["majors"].add(major_id)
            if semester is not None:
                item["semesters"].add(semester)
            if year is not None:
                item["years"].add(year)
    return metadata


def serializable_metadata(item: dict) -> dict:
    return {
        "course_code": item["course_code"],
        "course_name": item["course_name"],
        "majors": sorted(item["majors"]),
        "semesters": sorted(item["semesters"]),
        "years": sorted(item["years"]),
        "groups": sorted(item["groups"]),
        "blocks": sorted(item["blocks"]),
        "stress_weight": item["stress_weight"],
    }


def active_curriculum_codes(metadata: dict[str, dict]) -> set[str]:
    return {
        code
        for code, item in metadata.items()
        if item["semesters"] & ACTIVE_SEMESTERS
        and "graduation" not in item["blocks"]
    }


def timetable_by_code(timetable: list[dict]) -> dict[str, list[dict]]:
    by_code: dict[str, list[dict]] = defaultdict(list)
    for event in timetable:
        by_code[canonical_course_code(event.get("course_code"))].append(event)
    return by_code


def periods_overlap(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    return a_start <= b_end and b_start <= a_end


def room_is_free(timetable: list[dict], room_id: str, day: str, start_period: int, end_period: int) -> bool:
    for event in timetable:
        if event.get("room_id") != room_id or event.get("day") != day:
            continue
        event_start = optional_int(event.get("start_period"))
        event_end = optional_int(event.get("end_period"))
        if event_start is None or event_end is None:
            continue
        if periods_overlap(start_period, end_period, event_start, event_end):
            return False
    return True


def graph_rooms() -> list[dict]:
    graph = load_all_graphs()
    rooms = []
    for node_id, attrs in graph.nodes(data=True):
        if attrs.get("type") == "room":
            rooms.append({
                "room_id": node_id,
                "building": attrs.get("building"),
                "floor": attrs.get("floor"),
            })
    return sorted(rooms, key=lambda item: item["room_id"])


def choose_free_room(timetable: list[dict], donor_event: dict, rooms: list[dict]) -> dict | None:
    day = donor_event.get("day")
    start_period = optional_int(donor_event.get("start_period"))
    end_period = optional_int(donor_event.get("end_period"))
    if not day or start_period is None or end_period is None:
        return None

    donor_building = donor_event.get("building")
    donor_floor = donor_event.get("floor")
    preferred = [
        room for room in rooms
        if room.get("building") == donor_building and room.get("floor") == donor_floor
    ]
    secondary = [
        room for room in rooms
        if room.get("building") == donor_building and room not in preferred
    ]
    fallback = [room for room in rooms if room not in preferred and room not in secondary]
    for room in preferred + secondary + fallback:
        if room_is_free(timetable, room["room_id"], day, start_period, end_period):
            return room
    return None


def donor_score(missing: dict, donor: dict) -> int:
    missing_prefix = course_prefix(missing["course_code"])
    donor_prefix = course_prefix(donor["course_code"])
    if missing_prefix == "PE" and donor_prefix != "PE":
        return 0
    if missing_prefix in TECH_PREFIXES and donor_prefix not in TECH_PREFIXES:
        return 0
    if not missing["groups"] and not missing["blocks"] and missing_prefix != donor_prefix:
        return 0
    score = 0
    if missing["semesters"] & donor["semesters"]:
        score += 50
    if missing["years"] & donor["years"]:
        score += 20
    if missing_prefix == donor_prefix:
        score += 30
    elif missing_prefix in TECH_PREFIXES and donor_prefix in TECH_PREFIXES:
        score += 15
    if missing["groups"] & donor["groups"]:
        score += 25
    if missing["blocks"] & donor["blocks"]:
        score += 10
    return score


def choose_donor_event(missing_code: str, metadata: dict[str, dict], by_code: dict[str, list[dict]]) -> tuple[str, dict, int] | None:
    missing = metadata.get(missing_code)
    if not missing:
        return None
    candidates = []
    for donor_code, events in by_code.items():
        donor = metadata.get(donor_code)
        if not donor or donor_code == missing_code:
            continue
        score = donor_score(missing, donor)
        if score >= 75:
            sorted_events = sorted(events, key=lambda event: (
                DAY_ORDER.get(event.get("day"), 99),
                optional_int(event.get("start_period")) or 99,
                event.get("room_id") or "",
            ))
            candidates.append((score, len(events), donor_code, sorted_events[0]))
    if not candidates:
        return None
    score, _, donor_code, donor_event = sorted(candidates, reverse=True, key=lambda item: (item[0], item[1], item[2]))[0]
    return donor_code, donor_event, score


def next_inferred_event_id(timetable: list[dict], index: int) -> str:
    existing = {event.get("event_id") for event in timetable}
    while True:
        event_id = f"INF_{index:06d}"
        if event_id not in existing:
            return event_id
        index += 1


def make_inferred_event(event_id: str, missing: dict, donor_code: str, donor_event: dict, room: dict, score: int) -> dict:
    event = deepcopy(donor_event)
    event.update({
        "event_id": event_id,
        "source_file": "inferred_from_curriculum_statistics",
        "raw_sheet": "inferred",
        "raw_room_id": room["room_id"],
        "course_code": missing["course_code"],
        "course_name": missing["course_name"],
        "class_group": f"{missing['course_code']}.INFERRED",
        "section_id": f"{missing['course_code']}.INFERRED",
        "room_id": room["room_id"],
        "building": room.get("building"),
        "floor": room.get("floor"),
        "event_type": "inferred_class",
        "capacity_estimate": donor_event.get("capacity_estimate", 60),
        "enrollment_estimate": donor_event.get("enrollment_estimate", donor_event.get("capacity_estimate", 60)),
        "raw_cell_text": f"{missing['course_code']}.INFERRED",
        "raw_detail_text": f"Inferred from {donor_code}; donor score {score}.",
        "period_span_confidence": "inferred",
        "notes": (
            f"Inferred missing timetable event from related course {donor_code}; "
            "practice sections ending in .1/.2 are treated as the same course family. "
            "Generated only after checking room-time availability."
        ),
    })
    return event


def major_year_course_gaps(curriculum: dict) -> list[dict]:
    gaps = []
    for major in curriculum.get("majors", []):
        major_id = major.get("major_id")
        active_by_year: dict[int, list[str]] = defaultdict(list)
        for course in major.get("curriculum_courses", []):
            semester = optional_int(course.get("recommended_semester"))
            if semester in ACTIVE_SEMESTERS:
                active_by_year[infer_year_from_semester(semester)].append(canonical_course_code(course.get("course_code")))
        for year in [1, 2, 3, 4]:
            if not active_by_year.get(year):
                gaps.append({"major": major_id, "year": year, "active_semester": year * 2})
    return gaps


def warning_missing_course_codes(warnings_path: str | None) -> set[str]:
    if not warnings_path:
        return set()
    path = resolve_path(warnings_path)
    if not path.exists():
        return set()
    warnings = load_json(path)
    codes = set()
    for warning in warnings:
        if warning.get("type") != "COURSE_NOT_FOUND_IN_TIMETABLE":
            continue
        match = re.search(r"for ([A-Z0-9.]+)", warning.get("message", ""))
        if match:
            codes.add(canonical_course_code(match.group(1).rstrip(".")))
    return codes


def repair_timetable(timetable_path: str, curriculum_path: str, output_path: str, dry_run: bool, warnings_path: str | None) -> dict:
    timetable = load_json(timetable_path)
    curriculum = load_json(curriculum_path)
    metadata = collect_course_metadata(curriculum)
    by_code = timetable_by_code(timetable)
    timetable_course_count_before = len(by_code)
    rooms = graph_rooms()

    active_codes = active_curriculum_codes(metadata)
    missing_codes_from_warnings = warning_missing_course_codes(warnings_path)
    target_codes = active_codes | missing_codes_from_warnings
    missing_codes = sorted(code for code in target_codes if code not in by_code)
    added = []
    unresolved = []
    next_index = 1

    if not dry_run:
        backup_path = resolve_path("outputs/validation/normalized_timetable_before_repair.json")
        if not backup_path.exists():
            write_json(backup_path, timetable)

    for missing_code in missing_codes:
        donor = choose_donor_event(missing_code, metadata, by_code)
        if donor is None:
            if missing_code not in metadata:
                unresolved.append({
                    "course_code": missing_code,
                    "reason": "Course appears in simulation warnings but not in normalized curriculum metadata.",
                })
                continue
            unresolved.append({
                "course_code": missing_code,
                "reason": "No related timetabled donor reached the conservative similarity threshold.",
                "course": serializable_metadata(metadata[missing_code]),
            })
            continue
        donor_code, donor_event, score = donor
        room = choose_free_room(timetable, donor_event, rooms)
        if room is None:
            unresolved.append({
                "course_code": missing_code,
                "reason": "No non-overlapping graph room found for the donor time pattern.",
                "donor_course_code": donor_code,
                "donor_event_id": donor_event.get("event_id"),
                "donor_score": score,
                "course": serializable_metadata(metadata[missing_code]),
            })
            continue

        event_id = next_inferred_event_id(timetable, next_index)
        next_index += 1
        inferred_event = make_inferred_event(event_id, metadata[missing_code], donor_code, donor_event, room, score)
        timetable.append(inferred_event)
        by_code[missing_code].append(inferred_event)
        added.append({
            "course_code": missing_code,
            "event_id": event_id,
            "donor_course_code": donor_code,
            "donor_event_id": donor_event.get("event_id"),
            "donor_score": score,
            "room_id": room["room_id"],
            "day": inferred_event.get("day"),
            "start_period": inferred_event.get("start_period"),
            "end_period": inferred_event.get("end_period"),
        })

    if not dry_run:
        write_json(timetable_path, timetable)

    report = {
        "dry_run": dry_run,
        "timetable_path": str(resolve_path(timetable_path)),
        "curriculum_path": str(resolve_path(curriculum_path)),
        "active_curriculum_course_count": len(active_codes),
        "warning_missing_course_count": len(missing_codes_from_warnings),
        "timetable_course_count_before": timetable_course_count_before,
        "missing_target_course_count_before": len(missing_codes),
        "inferred_events_added": added,
        "inferred_event_count": len(added),
        "unresolved_missing_courses": unresolved,
        "unresolved_missing_course_count": len(unresolved),
        "major_year_course_gaps": major_year_course_gaps(curriculum),
    }
    write_json(output_path, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timetable", default="data/normalized/normalized_timetable.json")
    parser.add_argument("--curriculum", default="data/normalized/normalized_curriculum_all.json")
    parser.add_argument("--report", default="outputs/validation/academic_coverage_repair_report.json")
    parser.add_argument("--warnings", default="outputs/node_1_2/simulation_warnings.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    report = repair_timetable(args.timetable, args.curriculum, args.report, args.dry_run, args.warnings)
    print(f"Missing target courses before repair: {report['missing_target_course_count_before']}")
    print(f"Inferred events added: {report['inferred_event_count']}")
    print(f"Unresolved missing courses: {report['unresolved_missing_course_count']}")
    print(f"Major/year course gaps: {len(report['major_year_course_gaps'])}")
    print(f"Saved {resolve_path(args.report)}")


if __name__ == "__main__":
    main()
