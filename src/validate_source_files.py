from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from graph_utils import load_all_graphs


ROOT = Path(__file__).resolve().parents[1]
NS_MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL_NS = "{http://schemas.openxmlformats.org/package/2006/relationships}"
DOCX_TEXT_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
COURSE_RE = re.compile(r"\b([A-Z]{2,6}\d{2,4})\b", re.IGNORECASE)


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def load_json(path: str | Path) -> Any:
    return json.loads(resolve_path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, data: Any) -> None:
    output = resolve_path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def canonical_course_code(raw: Any) -> str:
    if raw is None:
        return ""
    value = "".join(str(raw).upper().split())
    if value.endswith(".1") or value.endswith(".2"):
        value = value[:-2]
    match = COURSE_RE.search(value)
    return match.group(1).upper() if match else value


def extract_course_codes(text: str) -> list[str]:
    return [canonical_course_code(match.group(1)) for match in COURSE_RE.finditer(text or "")]


def parse_shared_strings(zip_file: zipfile.ZipFile) -> list[str]:
    try:
        raw = zip_file.read("xl/sharedStrings.xml")
    except KeyError:
        return []
    root = ET.fromstring(raw)
    strings = []
    for si in root.findall(f"{NS_MAIN}si"):
        parts = [node.text or "" for node in si.iter(f"{NS_MAIN}t")]
        strings.append("".join(parts))
    return strings


def workbook_sheet_map(zip_file: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(zip_file.read("xl/workbook.xml"))
    rels = ET.fromstring(zip_file.read("xl/_rels/workbook.xml.rels"))
    rel_by_id = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall(f"{REL_NS}Relationship")
    }
    sheets = {}
    for sheet in workbook.findall(f"{NS_MAIN}sheets/{NS_MAIN}sheet"):
        name = sheet.attrib["name"]
        relationship_id = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
        target = rel_by_id[relationship_id].replace("\\", "/")
        if not target.startswith("xl/"):
            target = f"xl/{target}"
        sheets[name] = target
    return sheets


def cell_text(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.iter(f"{NS_MAIN}t")).strip()
    value = cell.find(f"{NS_MAIN}v")
    if value is None or value.text is None:
        return ""
    if cell_type == "s":
        index = int(value.text)
        return shared_strings[index].strip() if index < len(shared_strings) else ""
    return value.text.strip()


def extract_xlsx_text(path: str | Path) -> dict[str, list[str]]:
    source = resolve_path(path)
    with zipfile.ZipFile(source) as zip_file:
        shared_strings = parse_shared_strings(zip_file)
        sheets = workbook_sheet_map(zip_file)
        output: dict[str, list[str]] = {}
        for sheet_name, target in sheets.items():
            root = ET.fromstring(zip_file.read(target))
            texts = []
            for cell in root.iter(f"{NS_MAIN}c"):
                text = cell_text(cell, shared_strings)
                if text:
                    texts.append(text)
            output[sheet_name] = texts
    return output


def extract_docx_text(path: str | Path) -> str:
    source = resolve_path(path)
    with zipfile.ZipFile(source) as zip_file:
        chunks = []
        for name in sorted(zip_file.namelist()):
            if not name.startswith("word/") or not name.endswith(".xml"):
                continue
            if not any(part in name for part in ["document", "footnotes", "endnotes", "header", "footer"]):
                continue
            root = ET.fromstring(zip_file.read(name))
            chunks.extend(node.text or "" for node in root.iter(f"{DOCX_TEXT_NS}t"))
    return " ".join(chunks)


def source_timetable_codes(xlsx_path: str | Path) -> dict:
    sheet_texts = extract_xlsx_text(xlsx_path)
    codes_by_sheet = {}
    total = Counter()
    for sheet, texts in sheet_texts.items():
        counter = Counter()
        for text in texts:
            counter.update(extract_course_codes(text))
        codes_by_sheet[sheet] = dict(sorted(counter.items()))
        total.update(counter)
    return {
        "sheet_count": len(sheet_texts),
        "texts_by_sheet": {sheet: len(texts) for sheet, texts in sheet_texts.items()},
        "course_code_counts": dict(sorted(total.items())),
        "course_codes_by_sheet": codes_by_sheet,
    }


def source_curriculum_codes(docx_paths: list[str | Path]) -> dict:
    by_file = {}
    total = Counter()
    for path in docx_paths:
        source = resolve_path(path)
        text = extract_docx_text(source)
        counter = Counter(extract_course_codes(text))
        by_file[source.name] = {
            "text_length": len(text),
            "course_code_counts": dict(sorted(counter.items())),
        }
        total.update(counter)
    return {
        "file_count": len(docx_paths),
        "course_code_counts": dict(sorted(total.items())),
        "course_codes_by_file": by_file,
    }


def normalized_timetable_summary(timetable: list[dict], graph_room_ids: set[str]) -> dict:
    codes = Counter(canonical_course_code(event.get("course_code")) for event in timetable)
    inferred = [event for event in timetable if str(event.get("event_id", "")).startswith("INF_")]
    duplicate_event_ids = [
        event_id for event_id, count in Counter(event.get("event_id") for event in timetable).items()
        if event_id and count > 1
    ]
    missing_fields = []
    invalid_rooms = []
    room_day_period = defaultdict(list)
    for event in timetable:
        for field in ["event_id", "course_code", "room_id", "day", "start_period", "end_period", "start_time", "end_time"]:
            if event.get(field) in (None, ""):
                missing_fields.append({"event_id": event.get("event_id"), "field": field})
        if event.get("room_id") not in graph_room_ids:
            invalid_rooms.append({"event_id": event.get("event_id"), "room_id": event.get("room_id")})
        key = (event.get("room_id"), event.get("day"), event.get("start_period"), event.get("end_period"))
        room_day_period[key].append(event.get("event_id"))
    room_time_conflicts = [
        {"room_id": key[0], "day": key[1], "start_period": key[2], "end_period": key[3], "event_ids": values}
        for key, values in room_day_period.items()
        if key[0] and key[1] and key[2] is not None and len(values) > 1
    ]
    return {
        "event_count": len(timetable),
        "inferred_event_count": len(inferred),
        "course_count": len(codes),
        "course_code_counts": dict(sorted(codes.items())),
        "duplicate_event_ids": duplicate_event_ids,
        "missing_field_count": len(missing_fields),
        "missing_fields": missing_fields[:100],
        "invalid_room_count": len(invalid_rooms),
        "invalid_rooms": invalid_rooms[:100],
        "exact_room_time_conflict_count": len(room_time_conflicts),
        "exact_room_time_conflicts": room_time_conflicts[:100],
    }


def normalized_curriculum_summary(curriculum: dict) -> dict:
    course_codes = Counter()
    plan_codes = Counter()
    plan_not_in_curriculum = []
    duplicate_courses = []
    missing_course_fields = []
    for major in curriculum.get("majors", []):
        major_id = major.get("major_id")
        major_course_codes = [canonical_course_code(course.get("course_code")) for course in major.get("curriculum_courses", [])]
        course_set = set(major_course_codes)
        for code, count in Counter(major_course_codes).items():
            if code and count > 1:
                duplicate_courses.append({"major_id": major_id, "course_code": code, "count": count})
        for course in major.get("curriculum_courses", []):
            code = canonical_course_code(course.get("course_code"))
            if code:
                course_codes[code] += 1
            for field in ["course_code", "course_name"]:
                if course.get(field) in (None, ""):
                    missing_course_fields.append({"major_id": major_id, "course_code": code, "field": field})
        for item in major.get("sample_teaching_plan", []):
            code = canonical_course_code(item.get("course_code"))
            if code:
                plan_codes[code] += 1
                if code not in course_set:
                    plan_not_in_curriculum.append({"major_id": major_id, "course_code": code})
    return {
        "major_count": len(curriculum.get("majors", [])),
        "major_ids": [major.get("major_id") for major in curriculum.get("majors", [])],
        "curriculum_course_entry_count": sum(len(major.get("curriculum_courses", [])) for major in curriculum.get("majors", [])),
        "unique_curriculum_course_count": len(course_codes),
        "sample_plan_entry_count": sum(len(major.get("sample_teaching_plan", [])) for major in curriculum.get("majors", [])),
        "unique_sample_plan_course_count": len(plan_codes),
        "duplicate_course_count": len(duplicate_courses),
        "duplicate_courses": duplicate_courses[:100],
        "missing_course_field_count": len(missing_course_fields),
        "missing_course_fields": missing_course_fields[:100],
        "plan_not_in_curriculum_count": len(plan_not_in_curriculum),
        "plan_not_in_curriculum": plan_not_in_curriculum[:200],
        "course_code_counts": dict(sorted(course_codes.items())),
        "sample_plan_code_counts": dict(sorted(plan_codes.items())),
    }


def compare_code_sets(source_codes: set[str], normalized_codes: set[str], ignored_normalized_prefixes: tuple[str, ...] = ()) -> dict:
    normalized_filtered = {
        code for code in normalized_codes
        if code and not code.startswith(ignored_normalized_prefixes)
    }
    return {
        "source_code_count": len(source_codes),
        "normalized_code_count": len(normalized_filtered),
        "source_missing_from_normalized_count": len(source_codes - normalized_filtered),
        "source_missing_from_normalized": sorted(source_codes - normalized_filtered),
        "normalized_missing_from_source_count": len(normalized_filtered - source_codes),
        "normalized_missing_from_source": sorted(normalized_filtered - source_codes),
    }


def validate_sources(args: argparse.Namespace) -> dict:
    graph = load_all_graphs()
    graph_room_ids = {node_id for node_id, attrs in graph.nodes(data=True) if attrs.get("type") == "room"}
    timetable = load_json(args.timetable_json)
    curriculum = load_json(args.curriculum_json)

    xlsx_source = source_timetable_codes(args.xlsx)
    docx_source = source_curriculum_codes(args.docx)
    timetable_summary = normalized_timetable_summary(timetable, graph_room_ids)
    curriculum_summary = normalized_curriculum_summary(curriculum)

    xlsx_codes = set(xlsx_source["course_code_counts"])
    timetable_codes = set(timetable_summary["course_code_counts"])
    docx_codes = set(docx_source["course_code_counts"])
    curriculum_codes = set(curriculum_summary["course_code_counts"])

    report = {
        "source_files": {
            "xlsx": str(resolve_path(args.xlsx)),
            "docx": [str(resolve_path(path)) for path in args.docx],
        },
        "normalized_files": {
            "timetable_json": str(resolve_path(args.timetable_json)),
            "curriculum_json": str(resolve_path(args.curriculum_json)),
        },
        "xlsx_source": xlsx_source,
        "docx_source": docx_source,
        "normalized_timetable": timetable_summary,
        "normalized_curriculum": curriculum_summary,
        "timetable_source_vs_json": compare_code_sets(xlsx_codes, timetable_codes, ignored_normalized_prefixes=("INF",)),
        "curriculum_source_vs_json": compare_code_sets(docx_codes, curriculum_codes),
    }
    write_json(args.output, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xlsx", default="TKB Phòng.xlsx")
    parser.add_argument("--docx", nargs="+", default=["Ngành, CTDT và VD KHDG.docx", "Ngành, CTDT và VD KHDG 2.docx"])
    parser.add_argument("--timetable-json", default="data/normalized/normalized_timetable.json")
    parser.add_argument("--curriculum-json", default="data/normalized/normalized_curriculum_all.json")
    parser.add_argument("--output", default="outputs/validation/source_file_validation_report.json")
    args = parser.parse_args()
    report = validate_sources(args)
    print(f"Saved {resolve_path(args.output)}")
    print(f"XLSX source codes: {report['timetable_source_vs_json']['source_code_count']}")
    print(f"Timetable JSON codes: {report['timetable_source_vs_json']['normalized_code_count']}")
    print(f"XLSX codes missing from JSON: {report['timetable_source_vs_json']['source_missing_from_normalized_count']}")
    print(f"Timetable JSON codes missing from XLSX: {report['timetable_source_vs_json']['normalized_missing_from_source_count']}")
    print(f"DOCX source codes: {report['curriculum_source_vs_json']['source_code_count']}")
    print(f"Curriculum JSON codes: {report['curriculum_source_vs_json']['normalized_code_count']}")
    print(f"DOCX codes missing from JSON: {report['curriculum_source_vs_json']['source_missing_from_normalized_count']}")
    print(f"Curriculum JSON codes missing from DOCX: {report['curriculum_source_vs_json']['normalized_missing_from_source_count']}")


if __name__ == "__main__":
    main()
