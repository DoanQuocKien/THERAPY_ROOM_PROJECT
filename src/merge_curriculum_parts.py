from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    source = Path(path)
    if not source.is_absolute():
        source = ROOT / source
    return json.loads(source.read_text(encoding="utf-8"))


def merge_parts(paths: list[str]) -> dict:
    majors: dict[str, dict] = {}
    warnings = []
    data_parts = []
    for path in paths:
        data = load(path)
        data_parts.append(data.get("data_part"))
        for major in data["majors"]:
            major_id = major["major_id"]
            if major_id not in majors:
                majors[major_id] = major
                continue
            warnings.append({"type": "DUPLICATE_MAJOR_MERGED", "message": f"Merged duplicate major {major_id}."})
            existing = majors[major_id]
            existing_courses = {course["course_code"]: course for course in existing["curriculum_courses"]}
            for course in major["curriculum_courses"]:
                existing_courses.setdefault(course["course_code"], course)
            existing["curriculum_courses"] = list(existing_courses.values())
            plan_keys = {(item["semester"], item.get("course_code")) for item in existing["sample_teaching_plan"]}
            for item in major["sample_teaching_plan"]:
                key = (item["semester"], item.get("course_code"))
                if key not in plan_keys:
                    existing["sample_teaching_plan"].append(item)
                    plan_keys.add(key)
    return {"data_parts": data_parts, "majors": list(majors.values()), "warnings": warnings}


def main() -> None:
    paths = [
        "data/normalized/normalized_curriculum_p1.json",
        "data/normalized/normalized_curriculum_p2.json",
    ]
    merged = merge_parts(paths)
    output = ROOT / "data" / "normalized" / "normalized_curriculum_all.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
