from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


COMMON_COURSES = [
    ("IT001", "Intro Programming", 4, 1),
    ("MA006", "Calculus", 4, 1),
    ("MA003", "Linear Algebra", 3, 1),
    ("SS006", "General Law", 2, 1),
    ("ENG01", "English 1", 3, 1),
    ("IT002", "Object-Oriented Programming", 4, 2),
    ("IT003", "Data Structures", 4, 2),
    ("MA004", "Discrete Math", 3, 2),
    ("IT004", "Database", 4, 3),
    ("IT005", "Computer Networks", 4, 3),
    ("IT007", "Operating Systems", 4, 4),
]
MAJOR_PLANS = {
    "CNTT": {
        "name": "Cong Nghe Thong Tin",
        "semesters": {1: ["IT001", "MA006", "MA003", "SS006", "ENG01"], 2: ["IT002", "IT003", "MA004"], 3: ["IT004", "IT005"], 4: ["IT007", "CS117"]},
        "extra": [("CS117", "Computational Thinking", 3, 4), ("IE104", "Internet and Web Technology", 3, 5)],
    },
    "HTTT": {
        "name": "He Thong Thong Tin",
        "semesters": {1: ["IT001", "MA006", "MA003", "ENG01"], 2: ["IT002", "IT003", "MA004"], 3: ["IT004", "IT005"], 4: ["IS201", "IS210"]},
        "extra": [("IS201", "Information Systems Analysis", 4, 4), ("IS210", "DBMS", 4, 4)],
    },
    "AI": {
        "name": "Tri Tue Nhan Tao",
        "semesters": {1: ["IT001", "MA006", "MA003", "SS006"], 2: ["IT002", "IT003", "MA004"], 3: ["IT004", "IT007"], 4: ["CS106", "CS114", "CS112"]},
        "extra": [("CS106", "Artificial Intelligence", 4, 4), ("CS114", "Machine Learning", 4, 4), ("CS112", "Algorithm Analysis", 4, 4), ("DS201", "Deep Learning DS", 3, 6)],
    },
    "KTMT": {
        "name": "Ky Thuat May Tinh",
        "semesters": {1: ["IT001", "MA006", "MA003"], 2: ["IT002", "IT003"], 3: ["IT005", "CE103"], 4: ["CE224"]},
        "extra": [("CE103", "Microprocessors", 4, 3), ("CE224", "Embedded Systems", 4, 4), ("CE340", "AI for Embedded Systems", 3, 6)],
    },
    "KHDL": {
        "name": "Khoa Hoc Du Lieu",
        "semesters": {1: ["IT001", "MA006", "MA003"], 2: ["IT003", "MA004"], 3: ["IT004", "MA005"], 4: ["DS200", "DS201"]},
        "extra": [("DS200", "Big Data Analysis", 4, 4), ("DS201", "Deep Learning DS", 4, 4), ("DS307", "Social Media Data Analysis", 3, 6)],
    },
    "KHMT": {
        "name": "Khoa Hoc May Tinh",
        "semesters": {1: ["IT001", "MA006", "MA003"], 2: ["IT002", "IT003"], 3: ["IT004", "IT005"], 4: ["CS106", "CS112"]},
        "extra": [("CS106", "Artificial Intelligence", 4, 4), ("CS112", "Algorithm Analysis", 4, 4)],
    },
    "SE": {
        "name": "Cong Nghe Phan Mem",
        "semesters": {1: ["IT001", "MA006", "MA003"], 2: ["IT002", "IT003"], 3: ["IT004", "SE104"], 4: ["SE113"]},
        "extra": [("SE104", "Software Engineering Intro", 4, 3), ("SE113", "Software Testing", 3, 4)],
    },
    "NT": {
        "name": "Mang May Tinh Va Truyen Thong",
        "semesters": {1: ["IT001", "MA006"], 2: ["IT002", "IT003"], 3: ["IT005", "NT101"], 4: ["NT118"]},
        "extra": [("NT101", "Network Fundamentals", 4, 3), ("NT118", "Mobile Networking Apps", 3, 4)],
    },
    "ATTT": {
        "name": "An Toan Thong Tin",
        "semesters": {1: ["IT001", "MA006"], 2: ["IT002", "IT003"], 3: ["IT005", "AT101"], 4: ["CS112"]},
        "extra": [("AT101", "Security Fundamentals", 4, 3), ("CS112", "Algorithm Analysis", 4, 4)],
    },
}


ROOT = Path(__file__).resolve().parents[1]


def normalize_course_code(raw_code: str | None) -> str:
    if raw_code is None:
        return ""
    return re.sub(r"\s+", "", str(raw_code)).upper()


def normalize_course_name(raw_name: str | None) -> str:
    if raw_name is None:
        return ""
    return re.sub(r"\s+", " ", str(raw_name)).strip()


def semester_to_year(semester: int) -> int:
    return (semester + 1) // 2


def infer_course_block(section_title: str) -> str:
    value = section_title.lower()
    if "elective" in value:
        return "major_elective"
    if "graduation" in value:
        return "graduation"
    if "general" in value:
        return "general_education"
    return "professional_foundation"


def infer_course_group(section_title: str) -> str:
    value = section_title.lower()
    if "math" in value:
        return "math_cs_natural_science"
    if "language" in value:
        return "foreign_language"
    if "elective" in value:
        return "major_direction"
    return "professional_foundation"


def infer_stress_weight(course: dict) -> int:
    code = course.get("course_code", "")
    block = course.get("course_block", "")
    if block == "general_education" or code.startswith("ENG"):
        return 1
    if code.startswith(("CS", "DS", "CE", "SE", "NT", "AT")):
        return 3
    return 2


def make_course(code: str, name: str, credits: int | None, semester: int, source_part: str) -> dict:
    code = normalize_course_code(code)
    block = "general_education" if code.startswith(("MA", "SS", "ENG")) else "professional_foundation"
    course = {
        "course_code": code,
        "course_name": normalize_course_name(name),
        "credits": credits,
        "theory_hours": None,
        "practice_hours": None,
        "course_block": block,
        "course_group": infer_course_group(block),
        "is_required": True,
        "is_elective": False,
        "recommended_semester": semester,
        "recommended_year": semester_to_year(semester),
        "stress_weight": 2,
        "source_part": source_part,
        "notes": "",
    }
    course["stress_weight"] = infer_stress_weight(course)
    return course


def build_major(major_id: str, source_part: str) -> dict:
    spec = MAJOR_PLANS[major_id]
    course_by_code = {}
    for code, name, credits, semester in COMMON_COURSES + spec["extra"]:
        course_by_code[code] = make_course(code, name, credits, semester, source_part)
    sample = []
    for semester, codes in spec["semesters"].items():
        for code in codes:
            course = course_by_code.get(code) or make_course(code, code, 3, semester, source_part)
            course_by_code[code] = course
            sample.append({
                "semester": semester,
                "year": semester_to_year(semester),
                "course_code": course["course_code"],
                "course_name": course["course_name"],
                "credits": course["credits"],
                "theory_hours": course["theory_hours"],
                "practice_hours": course["practice_hours"],
                "is_required": True,
                "notes": "",
            })
    return {
        "major_id": major_id,
        "major_name": spec["name"],
        "degree": "Cu nhan",
        "total_credits_min": None,
        "curriculum_courses": list(course_by_code.values()),
        "sample_teaching_plan": sample,
        "elective_pools": {
            "major_elective": [course["course_code"] for course in course_by_code.values() if course["recommended_year"] >= 3],
        },
        "notes": f"Seed normalized data for {source_part}",
    }


def parse_curriculum_part(part: str) -> dict:
    if part == "PART_1":
        major_ids = ["CNTT", "HTTT"]
        source_file = "Nganh CTDT VD KHDG.docx"
    else:
        major_ids = ["AI", "KTMT", "KHDL", "KHMT", "SE", "NT", "ATTT"]
        source_file = "Nganh CTDT VD KHDG 2.docx"
    return {
        "data_part": part,
        "source_file": source_file,
        "majors": [build_major(major_id, part) for major_id in major_ids],
    }


def load_raw_curriculum(path: str):
    source = Path(path)
    if not source.is_absolute():
        source = ROOT / source
    if source.exists() and source.suffix.lower() == ".json":
        return json.loads(source.read_text(encoding="utf-8"))
    return None


def export_curriculum(data: dict, output_path: str) -> None:
    output = Path(output_path)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_curriculum(data: dict) -> dict:
    warnings = []
    errors = []
    major_ids = [major["major_id"] for major in data["majors"]]
    for major_id in sorted({major_id for major_id in major_ids if major_ids.count(major_id) > 1}):
        errors.append({"type": "DUPLICATE_MAJOR", "message": f"Duplicate major {major_id}."})
    total_courses = 0
    for major in data["majors"]:
        course_codes = [course["course_code"] for course in major["curriculum_courses"]]
        total_courses += len(course_codes)
        for course in major["curriculum_courses"]:
            if not course.get("course_code"):
                errors.append({"type": "MISSING_COURSE_CODE", "message": f"{major['major_id']} has empty course code."})
            if course.get("is_required") and course.get("is_elective"):
                errors.append({"type": "INVALID_REQUIRED_ELECTIVE", "message": f"{course['course_code']} is both required and elective."})
        for item in major["sample_teaching_plan"]:
            if item.get("course_code") and item["course_code"] not in course_codes:
                warnings.append({"type": "PLAN_COURSE_NOT_IN_CURRICULUM", "message": f"{major['major_id']} plan references {item['course_code']}."})
    return {
        "data_part": data.get("data_part"),
        "source_file": data.get("source_file"),
        "total_majors": len(data["majors"]),
        "total_courses": total_courses,
        "total_sample_plan_items": sum(len(major["sample_teaching_plan"]) for major in data["majors"]),
        "warnings": warnings,
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=["PART_1", "PART_2"], default="PART_1")
    parser.add_argument("--input", default="")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    data = load_raw_curriculum(args.input) if args.input else None
    if data is None:
        data = parse_curriculum_part(args.part)
    part_suffix = f"p{args.part[-1]}"
    output = args.output or f"data/normalized/normalized_curriculum_{part_suffix}.json"
    export_curriculum(data, output)
    report = validate_curriculum(data)
    report_path = ROOT / "outputs" / "validation" / f"curriculum_{part_suffix}_validation_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {output}")
    print(f"Saved {report_path}")


if __name__ == "__main__":
    main()
