# 08_TIMETABLE_INPUT_SPEC.md

# CS117 Node 1.2 — Timetable Input Specification

## 1. Document status

```txt
Document: 08_TIMETABLE_INPUT_SPEC.md
Node: 1.2 - Student Route Simulation
Data batch: DATA PART 1
Purpose: Define the standard input format for classroom timetable data
```

This file defines how the timetable data should be normalized before it is used by the student route simulation.

The raw timetable file may come from:

```txt
TKB Phòng.xlsx
```

or another equivalent file.

Codex must not assume that the raw Excel file is already clean.

The goal is to convert the raw timetable into a clean intermediate file:

```txt
normalized_timetable.json
```

or:

```txt
normalized_timetable.csv
```

The simulation should use the normalized file, not the raw Excel file directly.

---

## 2. Role of timetable data in Node 1.2

The timetable data provides the spatio-temporal anchor points for student movement.

Each timetable row answers:

```txt
Which course happens in which room, on which day, and at what time?
```

Example concept:

```txt
Course CS117 happens in room C205 on Monday from 07:30 to 09:10.
```

The route simulation will later use consecutive timetable events to generate movement:

```txt
previous room -> next room
```

For example:

```txt
C205 -> B1.14
```

---

## 3. Raw timetable input

Expected raw file:

```txt
TKB Phòng.xlsx
```

Codex should inspect the actual sheet names and columns before writing the parser.

Do not hard-code column positions unless the file structure is verified.

The parser should be tolerant of:

```txt
merged cells
empty rows
extra header rows
Vietnamese column names
multiple sheets
room-based grouping
course-based grouping
weekday names in Vietnamese
period-based schedules
```

---

## 4. Normalized timetable output

Create one normalized file:

```txt
data/normalized/normalized_timetable.json
```

Preferred structure:

```json
[
  {
    "event_id": "EVT_000001",
    "source_file": "TKB Phòng.xlsx",
    "raw_sheet": "Sheet1",
    "academic_year": null,
    "semester": null,
    "week_pattern": "weekly",

    "course_code": "CS117",
    "course_name": "Tư duy tính toán",
    "class_group": "CS117.O21",
    "section_id": "CS117.O21.1",

    "room_id": "C205",
    "building": "C",
    "floor": 2,

    "day": "Mon",
    "start_period": 1,
    "end_period": 3,
    "start_time": "07:30",
    "end_time": "09:10",

    "event_type": "lecture",
    "capacity_estimate": null,
    "notes": ""
  }
]
```

---

## 5. Required fields

Every normalized timetable event must contain:

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

If some fields are missing in the raw file, Codex should infer them if possible.

If inference is not possible, set the value to `null` and add a warning.

---

## 6. Optional fields

The following fields are optional but useful:

```txt
source_file
raw_sheet
academic_year
semester
week_pattern
class_group
section_id
event_type
capacity_estimate
teacher
notes
```

Do not block the pipeline if optional fields are missing.

---

## 7. Field definitions

## 7.1. `event_id`

Unique ID for each scheduled event.

Format:

```txt
EVT_000001
EVT_000002
...
```

This ID must be generated during normalization.

---

## 7.2. `course_code`

The course code.

Examples:

```txt
CS117
IT001
IT002
MA006
SS007
ENG01
```

Rules:

```txt
Trim spaces.
Convert to uppercase.
Keep dots or numbers if they are part of the official code.
```

---

## 7.3. `course_name`

Vietnamese course name.

Examples:

```txt
Tư duy tính toán
Nhập môn Lập trình
Lập trình hướng đối tượng
Giải tích
Triết học Mác - Lênin
```

Rules:

```txt
Keep Vietnamese accents.
Normalize repeated spaces.
Do not translate.
```

---

## 7.4. `class_group`

Class or section group from the timetable.

Examples:

```txt
CS117.O21
IT001.N11
MA006.O12
```

If not available:

```json
"class_group": null
```

---

## 7.5. `section_id`

A more specific section identifier.

If the raw timetable already has a class group and a practice/lecture group, combine them.

Example:

```txt
CS117.O21.1
CS117.O21.2
```

If not available:

```json
"section_id": null
```

---

## 7.6. `room_id`

Room ID must match the graph node room ID whenever possible.

Examples:

```txt
A-F1-TOP-ROOM-01
B1.14
C205
E3.2
D-F1-ROOM-01
```

For official room IDs such as `B1.14`, `C205`, `E3.2`, keep them unchanged.

For approximate rooms created in the graph, use the graph's room node ID.

Rules:

```txt
Trim spaces.
Convert building letter to uppercase.
Normalize room naming.
```

---

## 7.7. `building`

Extract building ID from room ID.

Examples:

```txt
A
B
C
D
E
```

Mapping examples:

```txt
B1.14 -> B
C205  -> C
E3.2  -> E
```

For custom graph IDs:

```txt
A-F1-TOP-ROOM-01 -> A
D-F1-ROOM-01     -> D
```

---

## 7.8. `floor`

Extract floor from room ID.

Examples:

```txt
B1.14 -> 1
B9.02 -> 9
C205  -> 2
C315  -> 3
E3.2  -> 3
E12.2 -> 12
```

If floor cannot be inferred:

```json
"floor": null
```

and add a warning.

---

## 7.9. `day`

Use English short format internally:

```txt
Mon
Tue
Wed
Thu
Fri
Sat
Sun
```

Vietnamese mapping:

```txt
Thứ 2 -> Mon
Thứ 3 -> Tue
Thứ 4 -> Wed
Thứ 5 -> Thu
Thứ 6 -> Fri
Thứ 7 -> Sat
Chủ nhật -> Sun
```

---

## 7.10. `start_period` and `end_period`

Use integer periods.

Example:

```json
"start_period": 1,
"end_period": 3
```

If the raw file has a list such as:

```txt
1-3
1,2,3
Tiết 1-3
```

normalize to:

```txt
start_period = 1
end_period = 3
```

---

## 7.11. `start_time` and `end_time`

Use 24-hour format:

```txt
HH:MM
```

Example:

```txt
07:30
09:10
13:00
15:30
```

If raw timetable only contains periods, use a period-to-time mapping.

Suggested mapping:

```json
{
  "1": ["07:30", "08:15"],
  "2": ["08:15", "09:00"],
  "3": ["09:15", "10:00"],
  "4": ["10:00", "10:45"],
  "5": ["10:45", "11:30"],
  "6": ["13:00", "13:45"],
  "7": ["13:45", "14:30"],
  "8": ["14:45", "15:30"],
  "9": ["15:30", "16:15"],
  "10": ["16:15", "17:00"]
}
```

If UIT's official period mapping differs, update this config later.

---

## 7.12. `event_type`

Possible values:

```txt
lecture
practice
lab
exam
unknown
```

Default:

```txt
unknown
```

Suggested inference:

```txt
If course has practice hours > 0 and room is lab-like -> lab/practice
Otherwise -> lecture
```

Do not overfit this in the first version.

---

## 8. Room normalization rules

Create a helper function:

```python
def normalize_room_id(raw_room: str) -> str:
    pass
```

Rules:

```txt
Remove extra spaces.
Convert letters to uppercase.
Keep dot notation for B and E rooms.
Keep compact notation for C rooms.
```

Examples:

```txt
" b1.14 " -> "B1.14"
"c205"    -> "C205"
"E03.2"   -> "E3.2" or keep as "E03.2" if graph uses that format
```

Important:

```txt
The normalized room ID must match the room node ID in the graph.
```

If graph uses `E3.2`, convert `E03.2` to `E3.2`.

If graph uses `E03.2`, keep leading zero.

Pick one convention and use it consistently.

---

## 9. Course normalization rules

Create a helper function:

```python
def normalize_course_code(raw_code: str) -> str:
    pass
```

Rules:

```txt
Trim spaces.
Uppercase.
Remove line breaks.
Keep letters and digits.
```

Examples:

```txt
" it001 " -> "IT001"
"CS 117"  -> "CS117"
"ma006"   -> "MA006"
```

---

## 10. Validation rules

After parsing timetable data, run validation.

## 10.1. Required validation

Check:

```txt
1. event_id is unique.
2. course_code is not empty.
3. room_id is not empty.
4. day is valid.
5. start_period <= end_period.
6. start_time < end_time.
7. building can be inferred.
8. floor can be inferred.
9. room_id exists in the global graph, if graph files are available.
```

---

## 10.2. Warning-level validation

Do not fail immediately, but record warnings for:

```txt
1. Missing course_name.
2. Missing class_group.
3. Missing section_id.
4. Missing event_type.
5. Unknown room not found in graph.
6. Course code not found in curriculum file.
7. Overlapping events in the same room.
```

---

## 11. Output validation report

Create:

```txt
outputs/validation/timetable_validation_report.json
```

Structure:

```json
{
  "total_events": 0,
  "valid_events": 0,
  "invalid_events": 0,
  "warnings": [
    {
      "event_id": "EVT_000123",
      "type": "ROOM_NOT_FOUND_IN_GRAPH",
      "message": "Room C999 does not exist in graph."
    }
  ],
  "errors": []
}
```

---

## 12. Parser requirements for Codex

Codex should create:

```txt
parse_timetable.py
```

Expected functions:

```python
def load_raw_timetable(path: str):
    pass

def normalize_timetable(raw_data) -> list[dict]:
    pass

def normalize_room_id(raw_room: str) -> str:
    pass

def normalize_course_code(raw_code: str) -> str:
    pass

def infer_building_and_floor(room_id: str) -> tuple[str | None, int | None]:
    pass

def validate_timetable(events: list[dict], graph_room_ids: set[str] | None = None) -> dict:
    pass

def export_normalized_timetable(events: list[dict], output_path: str) -> None:
    pass
```

---

## 13. Expected command

```bash
python parse_timetable.py \
  --input "data/raw/TKB Phòng.xlsx" \
  --output "data/normalized/normalized_timetable.json"
```

---

## 14. Output files

```txt
data/normalized/normalized_timetable.json
outputs/validation/timetable_validation_report.json
```

---

## 15. How this connects to simulation

The route simulation will later load:

```txt
normalized_timetable.json
```

and use it to generate student schedules.

The simulation should never depend directly on messy Excel formatting.

The normalized timetable is the stable interface between raw data and route generation.

---

## 16. Notes for future update

This file only defines the timetable normalization interface.

After the real timetable structure is fully inspected, update this file with:

```txt
actual sheet names
actual column names
actual period format
actual class group format
actual examples from the file
```

Do not change the normalized schema unless absolutely necessary.
