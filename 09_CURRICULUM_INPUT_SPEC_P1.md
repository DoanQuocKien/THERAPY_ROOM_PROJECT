# 09_CURRICULUM_INPUT_SPEC_P1.md

# CS117 Node 1.2 — Curriculum Input Specification Part 1

## 1. Document status

```txt
Document: 09_CURRICULUM_INPUT_SPEC_P1.md
Node: 1.2 - Student Route Simulation
Data batch: DATA PART 1
Purpose: Define normalized curriculum format for the first batch of majors
```

This document defines how curriculum data should be normalized for the student route simulation.

The raw curriculum source for this batch is:

```txt
Ngành, CTDT và VD KHDG.docx
```

This is Part 1 only.

More majors will be added later in:

```txt
09_CURRICULUM_INPUT_SPEC_P2.md
09_CURRICULUM_INPUT_SPEC_P3.md
...
```

The schema in this file must remain consistent across all parts.

---

## 2. Role of curriculum data in Node 1.2

Curriculum data is used to decide which courses a simulated student is likely to take.

The basic mapping is:

```txt
major + year + semester -> candidate courses
```

Example:

```txt
Công Nghệ Thông Tin + year 1 + semester 1
-> IT001, MA006, MA003, IE005, SS006, ENG01, ME001
```

This allows the simulation to generate realistic student schedules instead of assigning random courses.

---

## 3. Normalized output files

Create:

```txt
data/normalized/normalized_curriculum_p1.json
```

Optional CSV version:

```txt
data/normalized/normalized_curriculum_p1.csv
```

Later, all parts can be merged into:

```txt
data/normalized/normalized_curriculum_all.json
```

---

## 4. Top-level JSON structure

Recommended JSON structure:

```json
{
  "data_part": "PART_1",
  "source_file": "Ngành, CTDT và VD KHDG.docx",
  "majors": [
    {
      "major_id": "CNTT",
      "major_name": "Công Nghệ Thông Tin",
      "degree": "Cử nhân",
      "total_credits_min": 125,
      "curriculum_courses": [],
      "sample_teaching_plan": []
    }
  ]
}
```

---

## 5. Major schema

Each major must follow this structure:

```json
{
  "major_id": "CNTT",
  "major_name": "Công Nghệ Thông Tin",
  "degree": "Cử nhân",
  "total_credits_min": 125,
  "curriculum_courses": [],
  "sample_teaching_plan": [],
  "notes": ""
}
```

Required fields:

```txt
major_id
major_name
degree
curriculum_courses
sample_teaching_plan
```

Optional fields:

```txt
total_credits_min
notes
```

---

## 6. Course schema

Each course in `curriculum_courses` should follow:

```json
{
  "course_code": "IT001",
  "course_name": "Nhập môn Lập trình",
  "credits": 4,
  "theory_hours": 3,
  "practice_hours": 1,
  "course_block": "general_education",
  "course_group": "math_cs_natural_science",
  "is_required": true,
  "is_elective": false,
  "recommended_semester": 1,
  "recommended_year": 1,
  "stress_weight": 2,
  "notes": ""
}
```

Required fields:

```txt
course_code
course_name
credits
course_block
is_required
is_elective
```

Recommended fields:

```txt
theory_hours
practice_hours
course_group
recommended_semester
recommended_year
stress_weight
```

---

## 7. Sample teaching plan schema

Each item in `sample_teaching_plan` should follow:

```json
{
  "semester": 1,
  "year": 1,
  "course_code": "IT001",
  "course_name": "Nhập môn Lập trình",
  "credits": 4,
  "theory_hours": 3,
  "practice_hours": 1,
  "is_required": true,
  "notes": ""
}
```

Rules:

```txt
semester 1-2 -> year 1
semester 3-4 -> year 2
semester 5-6 -> year 3
semester 7-8 -> year 4
```

Function:

```python
def semester_to_year(semester: int) -> int:
    return (semester + 1) // 2
```

---

## 8. Course block categories

Use these standard `course_block` values:

```txt
general_education
professional_foundation
major_required
major_elective
free_elective
graduation
physical_defense
unknown
```

---

## 9. Course group categories

Use these standard `course_group` values:

```txt
politics_law
math_cs_natural_science
foreign_language
physical_education
national_defense
professional_foundation
major_direction
free_elective
graduation
other
unknown
```

---

## 10. Stress weight convention

This value will be used later for stress heatmap estimation.

Use a simple 1-3 scale first:

```txt
1 = low academic pressure
2 = medium academic pressure
3 = high academic pressure
```

Suggested default mapping:

```txt
general_education -> 1
foreign_language -> 1
physical_education -> 1
professional_foundation -> 2
programming / lab / system course -> 3
major_required -> 3
major_elective -> 2 or 3
graduation / thesis / project -> 3
```

This is only a simulation heuristic, not a clinical or psychological measurement.

---

## 11. Part 1 majors

This file should include the first batch of majors from the provided curriculum document.

At minimum, Part 1 currently includes:

```txt
CNTT - Công Nghệ Thông Tin
HTTT - Hệ Thống Thông Tin
```

If the raw document contains more majors in Part 1, Codex should parse them using the same schema.

Do not create a different schema per major.

---

# 12. Major: Công Nghệ Thông Tin

## 12.1. Major metadata

```json
{
  "major_id": "CNTT",
  "major_name": "Công Nghệ Thông Tin",
  "degree": "Cử nhân",
  "total_credits_min": 125
}
```

---

## 12.2. General education courses

Include at least:

```txt
SS003 - Tư tưởng Hồ Chí Minh
SS007 - Triết học Mác – Lênin
SS008 - Kinh tế chính trị Mác – Lênin
SS009 - Chủ nghĩa xã hội khoa học
SS010 - Lịch sử Đảng Cộng sản Việt Nam
SS006 - Pháp luật đại cương

MA006 - Giải tích
MA003 - Đại số tuyến tính
MA004 - Cấu trúc rời rạc
MA005 - Xác suất thống kê
IT001 - Nhập môn lập trình

ENG01 - Anh văn 1
ENG02 - Anh văn 2
ENG03 - Anh văn 3

PE231 - Giáo dục thể chất 1
PE232 - Giáo dục thể chất 2
ME001 - Giáo dục quốc phòng
SS004 - Kỹ năng nghề nghiệp
```

---

## 12.3. Professional foundation courses

Include at least:

```txt
IE005 - Giới thiệu ngành Công nghệ Thông tin
IT002 - Lập trình hướng đối tượng
IT003 - Cấu trúc dữ liệu và giải thuật
IT004 - Cơ sở dữ liệu
IT005 - Nhập môn mạng máy tính
IT012 - Tổ chức và cấu trúc máy tính II
IT007 - Hệ điều hành

IE101 - Cơ sở hạ tầng công nghệ thông tin
IE103 - Quản lý thông tin
IE104 - Internet và công nghệ Web
IE105 - Nhập môn bảo đảm và an ninh thông tin
IE106 - Thiết kế giao diện người dùng
IE108 - Phân tích thiết kế phần mềm
```

---

## 12.4. Major elective / direction courses

The CNTT curriculum contains several professional direction and elective courses.

Examples:

```txt
IE213 - Kỹ thuật phát triển hệ thống Web
IE307 - Công nghệ lập trình đa nền tảng cho ứng dụng di động
IE233 - Phân tích và mô hình mạng xã hội
IE403 - Khai thác dữ liệu truyền thông xã hội
DS300 - Hệ khuyến nghị
IE203 - Hệ thống quản trị qui trình nghiệp vụ
IE204 - Tối ưu hóa công cụ tìm kiếm
IE303 - Công nghệ Java
IE310 - Tư duy thiết kế
IE301 - Quản trị quan hệ khách hàng
DS322 - Thiết kế hệ thống học máy

IE201 - Xử lý dữ liệu thống kê
IE221 - Kỹ thuật lập trình Python
DS108 - Tiền xử lý và xây dựng bộ dữ liệu
IE313 - Phân tích và trực quan dữ liệu
IE212 - Công nghệ Dữ liệu lớn
IE302 - Kiến trúc và tích hợp hệ thống
IE402 - Hệ thống thông tin địa lý 3 chiều
DS307 - Phân tích dữ liệu truyền thông xã hội
DS317 - Khai phá dữ liệu trong doanh nghiệp
IE102 - Các công nghệ nền
IE231 - Quản trị doanh nghiệp công nghệ thông tin
```

For simulation, these can be sampled for year 3 and year 4 students.

---

## 12.5. CNTT sample teaching plan

Use the sample teaching plan as the preferred course assignment guide.

### Semester 1

```txt
IT001
MA006
MA003
IE005
SS006
ENG01
ME001
```

### Semester 2

```txt
IT002
IT003
SS004
MA004
ENG02
```

### Semester 3

```txt
IT004
IT005
IT012
MA005
ENG03
```

### Semester 4

```txt
SS003
SS007
IT007
IE101
IE103
```

### Semester 5

```txt
SS008
SS009
IE104
IE106
PE231
major_elective >= 4 credits
```

### Semester 6

```txt
SS010
IE105
IE108
PE232
major_elective >= 10 credits
```

### Semester 7

```txt
IE400 optional if graduation option 2
major_elective >= 12 credits
```

### Semester 8

One of:

```txt
IE505
IE501
IE502
```

---

# 13. Major: Hệ Thống Thông Tin

## 13.1. Major metadata

```json
{
  "major_id": "HTTT",
  "major_name": "Hệ Thống Thông Tin",
  "degree": "Cử nhân",
  "total_credits_min": null
}
```

---

## 13.2. General education courses

Include at least:

```txt
SS003 - Tư tưởng Hồ Chí Minh
SS007 - Triết học Mác - Lênin
SS008 - Kinh tế chính trị Mác - Lênin
SS009 - Chủ nghĩa xã hội khoa học
SS010 - Lịch sử Đảng Cộng sản Việt Nam

MA006 - Giải tích
MA003 - Đại số tuyến tính
MA004 - Cấu trúc rời rạc
MA005 - Xác suất thống kê
IT001 - Nhập môn Lập trình

ENG01 - Anh văn 1
ENG02 - Anh văn 2
ENG03 - Anh văn 3

PE231 - Giáo dục thể chất 1
PE232 - Giáo dục thể chất 2
ME001 - Giáo dục quốc phòng
SS004 - Kỹ năng nghề nghiệp
SS006 - Pháp luật đại cương
```

---

## 13.3. Professional foundation courses

Include at least:

```txt
IT002 - Lập trình hướng đối tượng
IT003 - Cấu trúc dữ liệu và giải thuật
IT004 - Cơ sở dữ liệu
IT005 - Nhập môn mạng máy tính
IT010 - Tổ chức và cấu trúc máy tính
IT007 - Hệ điều hành
IS005 - Giới thiệu ngành Hệ thống thông tin
```

---

## 13.4. HTTT management direction courses

Examples:

```txt
IS336 - Hoạch định nguồn lực doanh nghiệp
IS201 - Phân tích thiết kế hệ thống thông tin
IS210 - Hệ quản trị cơ sở dữ liệu
IS208 - Quản lý dự án công nghệ thông tin
IS216 - Lập trình Java
IS207 - Phát triển ứng dụng web
NT118 - Phát triển ứng dụng trên thiết bị di động
IS211 - Cơ sở dữ liệu phân tán
IS405 - Dữ liệu lớn
IS252 - Khai thác dữ liệu
IS217 - Kho dữ liệu và OLAP
IS403 - Phân tích dữ liệu kinh doanh
```

---

## 13.5. HTTT medical direction courses

Examples:

```txt
IS344 - Quản trị nguồn lực y tế
IS201 - Phân tích thiết kế hệ thống thông tin
IS346 - Quản lý dự án công nghệ thông tin y tế
IS216 - Lập trình Java
IS207 - Phát triển ứng dụng web
IS348 - Dịch tễ học
IS349 - Hệ thống y tế
IS360 - Quản lý chăm sóc và điều trị
IS361 - Quản lý chuỗi cung ứng dược và thiết bị y tế
IS362 - Quản trị tài chính và bảo hiểm y tế
IS345 - AI trong y tế
IS347 - Thống kê y học
DS312 - Xử lý ảnh Y khoa
IS217 - Kho dữ liệu và OLAP
```

For simulation, assign a specialization to year 3 and year 4 HTTT agents:

```txt
httq_management
httq_medical
```

Use probability split:

```txt
management: 0.7
medical: 0.3
```

This can be changed later.

---

## 13.6. HTTT sample teaching plan

Use the sample teaching plan as the preferred guide.

### Semester 1

```txt
IT001
MA006
MA003
IT010
IS005
ENG01
ME001
```

### Semester 2

```txt
IT002
IT003
MA004
MA005
ENG02
```

### Semester 3

```txt
IT004
IT005
SS007
SS008
ENG03
SS006
SS004
```

### Semester 4 and later

The raw curriculum contains different plans depending on specialization.

Codex should parse the specialization sections separately.

Required normalized fields:

```txt
major_id = HTTT
specialization = management or medical
semester
course_code
course_name
credits
```

---

# 14. Curriculum parser requirements

Codex should create:

```txt
parse_curriculum.py
```

Expected functions:

```python
def load_raw_curriculum(path: str):
    pass

def normalize_course_code(raw_code: str) -> str:
    pass

def normalize_course_name(raw_name: str) -> str:
    pass

def infer_course_block(section_title: str) -> str:
    pass

def infer_course_group(section_title: str) -> str:
    pass

def infer_stress_weight(course: dict) -> int:
    pass

def semester_to_year(semester: int) -> int:
    pass

def parse_curriculum_part_1(raw_doc) -> dict:
    pass

def export_curriculum(data: dict, output_path: str) -> None:
    pass

def validate_curriculum(data: dict) -> dict:
    pass
```

---

## 15. Validation rules

Run validation after parsing.

Check:

```txt
1. major_id is unique.
2. course_code is not empty.
3. course_name is not empty.
4. credits is numeric or null.
5. is_required and is_elective are not both true.
6. recommended_semester is between 1 and 8 if present.
7. recommended_year is between 1 and 4 if present.
8. sample_teaching_plan course_code exists in curriculum_courses.
9. duplicated course_code within the same major is allowed only if it appears in multiple categories, but should be flagged as warning.
```

---

## 16. Output validation report

Create:

```txt
outputs/validation/curriculum_p1_validation_report.json
```

Structure:

```json
{
  "data_part": "PART_1",
  "total_majors": 0,
  "total_courses": 0,
  "warnings": [],
  "errors": []
}
```

---

## 17. How this connects to timetable matching

After normalization, the simulator will match:

```txt
curriculum course_code
```

with:

```txt
timetable course_code
```

If a curriculum course has no matching timetable entry, do not crash.

Instead:

```txt
1. skip that course for this simulation run
2. log warning COURSE_NOT_FOUND_IN_TIMETABLE
3. optionally sample another course from the same semester/category
```

---

## 18. Course assignment logic

For each simulated student:

```txt
major_id + year -> possible semesters
```

Mapping:

```txt
year 1 -> semester 1 or 2
year 2 -> semester 3 or 4
year 3 -> semester 5 or 6
year 4 -> semester 7 or 8
```

Preferred assignment:

```txt
Use sample_teaching_plan first.
If no sample plan exists, use curriculum_courses by recommended_year.
If still missing, use course_block and course_group.
```

---

## 19. Recommended output example

Example normalized major:

```json
{
  "major_id": "CNTT",
  "major_name": "Công Nghệ Thông Tin",
  "degree": "Cử nhân",
  "total_credits_min": 125,
  "curriculum_courses": [
    {
      "course_code": "IT001",
      "course_name": "Nhập môn Lập trình",
      "credits": 4,
      "theory_hours": 3,
      "practice_hours": 1,
      "course_block": "general_education",
      "course_group": "math_cs_natural_science",
      "is_required": true,
      "is_elective": false,
      "recommended_semester": 1,
      "recommended_year": 1,
      "stress_weight": 2,
      "notes": ""
    }
  ],
  "sample_teaching_plan": [
    {
      "semester": 1,
      "year": 1,
      "course_code": "IT001",
      "course_name": "Nhập môn Lập trình",
      "credits": 4,
      "theory_hours": 3,
      "practice_hours": 1,
      "is_required": true,
      "notes": ""
    }
  ]
}
```

---

## 20. Notes for future parts

Future curriculum parts must use the same schema.

Do not introduce new field names unless necessary.

Use these same fields:

```txt
major_id
major_name
degree
total_credits_min
curriculum_courses
sample_teaching_plan

course_code
course_name
credits
theory_hours
practice_hours
course_block
course_group
is_required
is_elective
recommended_semester
recommended_year
stress_weight
notes
```

When Part 2 arrives, create:

```txt
09_CURRICULUM_INPUT_SPEC_P2.md
```

and keep the same structure.
