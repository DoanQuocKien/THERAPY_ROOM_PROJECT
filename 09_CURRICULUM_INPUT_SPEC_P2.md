# 09_CURRICULUM_INPUT_SPEC_P2.md

# CS117 Node 1.2 — Curriculum Input Specification Part 2

## 1. Document status

```txt
Document: 09_CURRICULUM_INPUT_SPEC_P2.md
Node: 1.2 - Student Route Simulation
Data batch: DATA PART 2
Purpose: Define normalized curriculum format for the remaining majors
```

This document extends:

```txt
09_CURRICULUM_INPUT_SPEC_P1.md
```

The schema in this file must stay consistent with Part 1.

Raw source file:

```txt
Ngành, CTDT và VD KHDG 2.docx
```

This file contains the remaining major curriculum data and sample teaching plans.

---

## 2. Important schema consistency rule

Do not create a new schema for Part 2.

Use the same top-level structure as Part 1:

```json
{
  "data_part": "PART_2",
  "source_file": "Ngành, CTDT và VD KHDG 2.docx",
  "majors": []
}
```

Each major must use:

```json
{
  "major_id": "AI",
  "major_name": "Trí Tuệ Nhân Tạo",
  "degree": "Cử nhân",
  "total_credits_min": null,
  "curriculum_courses": [],
  "sample_teaching_plan": [],
  "notes": ""
}
```

Each course must use:

```json
{
  "course_code": "CS106",
  "course_name": "Trí tuệ nhân tạo",
  "credits": 4,
  "theory_hours": 3,
  "practice_hours": 1,
  "course_block": "professional_foundation",
  "course_group": "major_direction",
  "is_required": true,
  "is_elective": false,
  "recommended_semester": 4,
  "recommended_year": 2,
  "stress_weight": 3,
  "notes": ""
}
```

---

## 3. Output files

Create:

```txt
data/normalized/normalized_curriculum_p2.json
```

Optional CSV version:

```txt
data/normalized/normalized_curriculum_p2.csv
```

After Part 1 and Part 2 are parsed, merge into:

```txt
data/normalized/normalized_curriculum_all.json
```

Merged structure:

```json
{
  "data_parts": ["PART_1", "PART_2"],
  "majors": []
}
```

---

## 4. Major IDs

Use these normalized major IDs.

```txt
CNTT  - Công Nghệ Thông Tin
HTTT  - Hệ Thống Thông Tin
AI    - Trí Tuệ Nhân Tạo
KTMT  - Kỹ Thuật Máy Tính
KHDL  - Khoa Học Dữ Liệu
KHMT  - Khoa Học Máy Tính
SE    - Công Nghệ Phần Mềm
NT    - Mạng Máy Tính Và Truyền Thông Dữ Liệu
ATTT  - An Toàn Thông Tin
```

Part 1 already covers some majors.

Part 2 should add all remaining majors found in the raw document.

If a major appears in both Part 1 and Part 2, Codex must not duplicate it. Instead, merge missing courses and log a warning:

```txt
DUPLICATE_MAJOR_MERGED
```

---

## 5. Standard course block values

Use exactly the same `course_block` values as Part 1:

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

## 6. Standard course group values

Use exactly the same `course_group` values as Part 1:

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

## 7. Required parser behavior

The curriculum document is not guaranteed to be machine-clean.

Codex must handle:

```txt
Vietnamese section titles
tables split across pages
merged cells
missing practice hour column
courses marked as Bắt buộc
courses marked as Chọn
course groups such as "Chọn 1/2" or "Chọn 1/4"
sample teaching plans by semester
graduation options
free electives
major electives
```

Do not fail if a course has missing `practice_hours`.

Use:

```json
"practice_hours": null
```

when the value is unavailable.

---

# 8. Major: Trí Tuệ Nhân Tạo

## 8.1. Major metadata

```json
{
  "major_id": "AI",
  "major_name": "Trí Tuệ Nhân Tạo",
  "degree": "Cử nhân",
  "total_credits_min": null
}
```

---

## 8.2. General education courses

Include at least:

```txt
SS003 - Tư tưởng Hồ Chí Minh
SS006 - Pháp luật đại cương
SS007 - Triết học Mác – Lênin
SS008 - Kinh tế chính trị Mác – Lênin
SS009 - Chủ nghĩa xã hội khoa học
SS010 - Lịch sử Đảng Cộng sản Việt Nam

MA003 - Đại số tuyến tính
MA004 - Cấu trúc rời rạc
MA005 - Xác suất thống kê
MA006 - Giải tích
CS115 - Toán cho Khoa học máy tính

ENG01 - Anh văn 1
ENG02 - Anh văn 2
ENG03 - Anh văn 3

PE231 - Giáo dục thể chất 1
PE232 - Giáo dục thể chất 2
ME001 - Giáo dục quốc phòng
SS004 - Kỹ năng nghề nghiệp
```

---

## 8.3. AI professional foundation courses

Include at least:

```txt
IT001 - Nhập môn lập trình
IT002 - Lập trình hướng đối tượng
SE104 - Nhập môn Công nghệ phần mềm
CS111 - Nguyên lý và phương pháp lập trình
CS311 - Kỹ thuật lập trình Trí tuệ nhân tạo
CS116 - Lập trình Python cho Máy học

IT003 - Cấu trúc dữ liệu và giải thuật
CS112 - Phân tích và thiết kế thuật toán

IT012 - Tổ chức và cấu trúc máy tính II
IT007 - Hệ điều hành
IT005 - Nhập môn mạng máy tính

IT004 - Cơ sở dữ liệu

CS106 - Trí tuệ nhân tạo
CS114 - Máy học
AI002 - Tư duy Trí tuệ nhân tạo
CS221 - Xử lý ngôn ngữ tự nhiên
CS231 - Nhập môn Thị giác máy tính
CS214 - Biểu diễn tri thức và suy luận
CS232 - Tính toán đa phương tiện

AI001 - Giới thiệu ngành Trí tuệ nhân tạo
```

Rules:

```txt
Courses marked "BB" are required.
Courses in "Chọn 1/2" or "Chọn 1/4" groups are elective choice groups.
```

Represent choice groups using:

```json
"choice_group": "AI_FOUNDATION_PROGRAMMING_1",
"choice_rule": "choose_1_of_2"
```

or:

```json
"choice_group": "AI_ML_AI_CHOICE_1",
"choice_rule": "choose_1_of_4"
```

---

## 8.4. AI major elective courses

Include examples:

```txt
CS211 - Trí tuệ nhân tạo nâng cao
CS315 - Máy học nâng cao
CS410 - Mạng Neural và Thuật giải di truyền
CS431 - Các kĩ thuật học sâu và ứng dụng
CS217 - Các hệ cơ sở tri thức
CS316 - Các hệ giải bài toán thông minh
CS312 - Hệ thống đa tác tử
CS229 - Ngữ nghĩa học tính toán
CS226 - Ngôn ngữ học máy tính
CS222 - Xử lý ngôn ngữ tự nhiên nâng cao
CS323 - Các hệ thống hỏi-đáp
CS321 - Ngôn ngữ học ngữ liệu
CS325 - Dịch máy
CS331 - Thị giác máy tính nâng cao
CS532 - Thị giác máy tính trong tương tác người – máy
CS338 - Nhận dạng
CS313 - Khai thác dữ liệu và ứng dụng
CS336 - Truy vấn thông tin đa phương tiện
CS337 - Xử lý âm thanh và tiếng nói
CS535 - Tổng hợp tiếng nói
AI301 - Khởi nghiệp và sáng tạo
AI302 - Kỹ thuật viết báo cáo và trình bày
CS317 - Phát triển và vận hành hệ thống máy học
```

These courses should usually be assigned to year 3 or year 4 agents.

---

## 8.5. AI interdisciplinary electives

The AI curriculum includes interdisciplinary elective suggestions from other majors.

Examples:

```txt
DS103 - Thu thập và tiền xử lý dữ liệu
DS200 - Phân tích dữ liệu lớn
DS201 - Deep Learning trong khoa học dữ liệu

CE340 - Trí tuệ nhân tạo cho hệ thống nhúng
CE344 - Trí tuệ nhân tạo cho IoT

IS211 - Cơ sở dữ liệu phân tán
IS403 - Phân tích dữ liệu kinh doanh

SE113 - Kiểm chứng phần mềm
SE357 - Kỹ thuật phân tích yêu cầu
SE358 - Quản lý dự án phát triển phần mềm

NT538 - Giải thuật xử lý song song và phân bố
NT539 - AI ứng dụng trong mạng và truyền thông

CS519 - Phương pháp luận nghiên cứu khoa học
CS529 - Các vấn đề nghiên cứu và ứng dụng trong khoa học máy tính
CS333 - Đồ họa game
CS527 - Thực tại ảo
CS523 - Cấu trúc dữ liệu và giải thuật nâng cao
CS551 - Thực tập
```

Mark these as:

```json
"course_block": "free_elective",
"course_group": "major_direction",
"is_required": false,
"is_elective": true
```

---

## 8.6. AI graduation courses

Include:

```txt
AI505 - Khóa luận tốt nghiệp
AI504 - Đồ án tốt nghiệp tại doanh nghiệp
AI503 - Đồ án tốt nghiệp

CS409 - Hệ suy diễn mờ
CS405 - Logic mờ và ứng dụng
CS406 - Xử lý ảnh và ứng dụng
CS419 - Truy xuất thông tin
CS412 - Web ngữ nghĩa
```

Graduation courses should usually be assigned only to year 4 agents.

---

## 8.7. AI sample teaching plan

Use the sample teaching plan as preferred assignment.

### Semester 1

```txt
IT001
MA006
MA003
AI001
ENG01
SS004
SS006
ME001
```

### Semester 2

```txt
IT002
IT003
IT012
MA004
MA005
ENG02
```

### Semester 3

```txt
IT004
IT007
ENG03
AI002
CS115
```

### Semester 4

```txt
IT005
CS112
CS106
CS114
SS007
PE231
```

### Semester 5

```txt
foundation_programming_elective_1
foundation_programming_elective_2
major_elective_1
interdisciplinary_elective_1
SS008
SS009
```

### Semester 6

```txt
major_elective_2
major_elective_3
interdisciplinary_elective_2
SS003
SS010
PE232
```

### Semester 7

One of:

```txt
AI505
AI504
AI503 + graduation_topic_course
```

---

# 9. Major: Kỹ Thuật Máy Tính

## 9.1. Major metadata

```json
{
  "major_id": "KTMT",
  "major_name": "Kỹ Thuật Máy Tính",
  "degree": "Cử nhân",
  "total_credits_min": null
}
```

---

## 9.2. KTMT general education courses

Include at least:

```txt
SS003 - Tư tưởng Hồ Chí Minh
SS006 - Pháp luật đại cương
SS007 - Triết học Mác – Lênin
SS008 - Kinh tế chính trị Mác – Lênin
SS009 - Chủ nghĩa xã hội khoa học
SS010 - Lịch sử Đảng Cộng sản Việt Nam

MA006 - Giải tích
MA003 - Đại số tuyến tính
MA004 - Cấu trúc rời rạc
MA005 - Xác suất thống kê
PH002 - Nhập môn mạch số
IT001 - Nhập môn Lập trình

ENG01 - Anh văn 1
ENG02 - Anh văn 2
ENG03 - Anh văn 3

ME001 - Giáo dục Quốc phòng
PE231 - Giáo dục thể chất 1
PE232 - Giáo dục thể chất 2
```

---

## 9.3. KTMT professional foundation courses

Include at least:

```txt
IT002 - Lập trình hướng đối tượng
IT003 - Cấu trúc dữ liệu và giải thuật
IT004 - Cơ sở dữ liệu
IT005 - Nhập môn mạng máy tính
IT006 - Kiến trúc máy tính
IT007 - Hệ điều hành
CE005 - Giới thiệu ngành KTMT
CE103 - Vi xử lý – vi điều khiển
CE118 - Thiết kế luận lý số
CE119 - Thực hành Kiến trúc Máy tính
CE122 - Phân tích mạch kỹ thuật
CE124 - Các thiết bị và mạch điện tử
CE212 - Điều khiển tự động
CE224 - Thiết kế hệ thống nhúng
```

Mark these as:

```json
"course_block": "professional_foundation",
"is_required": true
```

Most CE/IT lab-heavy courses should use:

```json
"stress_weight": 3
```

---

## 9.4. KTMT major elective courses

The KTMT curriculum includes directional elective groups.

### Embedded Systems and IoT direction

```txt
CE232 - Thiết kế hệ thống nhúng không dây
CE439 - Lập trình song song và Hệ thống phân tán
CE339 - Công nghệ IoT và Ứng dụng
CE340 - Trí tuệ nhân tạo cho hệ thống nhúng
CE410 - Kỹ thuật hệ thống máy tính
CE342 - Hệ thống thông minh
CE348 - Công nghệ cảm biến trong IoT
CE437 - Chuyên đề thiết kế hệ thống nhúng 1
CE438 - Chuyên đề thiết kế hệ thống nhúng 2
```

### Robotics and AI direction

```txt
CE233 - Kỹ thuật Robot
CE347 - Điều khiển thông minh cho robot
CE440 - Hệ thống định vị với ứng dụng AI
CE320 - Logic mờ cho ứng dụng hệ thống nhúng
CE406 - Tương tác người – máy
CE441 - Chuyên đề thiết kế Robotics và AI 1
CE442 - Chuyên đề thiết kế Robotics và AI 2
```

Represent direction using:

```json
"specialization": "embedded_iot"
```

or:

```json
"specialization": "robotics_ai"
```

---

## 9.5. KTMT project and graduation courses

Include:

```txt
CE201 - Đồ án 1
CE206 - Đồ án 2
CE502 - Thực tập doanh nghiệp
CE505 - Khóa luận tốt nghiệp
CE507 - Đồ án tốt nghiệp tại doanh nghiệp
CE508 - Đồ án tốt nghiệp
CE510 - Chuyên đề tốt nghiệp định hướng Hệ thống nhúng và IoT
CE511 - Chuyên đề tốt nghiệp định hướng Robotic và AI
```

Project/graduation courses should usually be assigned to year 3 and year 4 agents.

---

# 10. Major: Khoa Học Dữ Liệu

## 10.1. Major metadata

```json
{
  "major_id": "KHDL",
  "major_name": "Khoa Học Dữ Liệu",
  "degree": "Cử nhân",
  "total_credits_min": null
}
```

---

## 10.2. KHDL parsing rule

Codex should parse all KHDL sections using the same schema.

The raw document contains data science courses such as:

```txt
DS005 - Giới thiệu ngành Khoa học dữ liệu
DS103 - Thu thập và tiền xử lý dữ liệu
DS200 - Phân tích dữ liệu lớn
DS201 - Deep Learning trong Khoa học dữ liệu
DS304 - Thiết kế và phân tích thực nghiệm
DS307 - Phân tích dữ liệu truyền thông xã hội
DS315 - Phân tích Kho dữ liệu
DS325 - Thiết kế ứng dụng với dữ liệu chuyên sâu
DS104 - Tính toán song song và phân tán
DS317 - Khai phá dữ liệu trong doanh nghiệp
DS322 - Thiết kế hệ thống Học máy
DS318 - Đạo đức trong Trí tuệ nhân tạo và Khoa học dữ liệu
DS306 - Phân tích dữ liệu lớn trong tài chính
DS305 - Phân tích dữ liệu chuỗi thời gian và ứng dụng
DS204 - Đồ án Khoa học dữ liệu và ứng dụng
DS207 - Đồ án
DS302 - Phân tích thống kê đa biến
DS303 - Thống kê Bayes
DS308 - Mô hình đồ thị xác suất
DS311 - Kỹ năng nghiên cứu và viết bài báo khoa học
DS323 - Viết báo cáo kỹ thuật và thuyết trình
DS309 - Thực tập doanh nghiệp
```

KHDL courses generally have high academic load.

Suggested stress weights:

```txt
DS foundation courses -> 2
DS machine learning / big data / project courses -> 3
statistics / math-heavy electives -> 3
writing / presentation courses -> 1 or 2
```

---

## 10.3. KHDL sample teaching plan

If the raw document contains a sample teaching plan, parse it into:

```json
"sample_teaching_plan": []
```

Expected early semesters may contain common foundation courses such as:

```txt
IT001
MA006
MA003
SS006
DS005
ENG01
ME001
IT010
SS004
IT003
```

Codex must not invent missing semesters.

If a semester is not clearly parsed, leave it out and log a warning:

```txt
KHDL_SAMPLE_PLAN_INCOMPLETE
```

---

# 11. Other remaining majors

The document may contain additional majors, such as:

```txt
KHMT - Khoa Học Máy Tính
SE   - Công Nghệ Phần Mềm
NT   - Mạng Máy Tính Và Truyền Thông Dữ Liệu
ATTT - An Toàn Thông Tin
```

Codex should parse them if they appear in the raw document.

Use this generic structure for each remaining major:

```json
{
  "major_id": "KHMT",
  "major_name": "Khoa Học Máy Tính",
  "degree": "Cử nhân",
  "total_credits_min": null,
  "curriculum_courses": [],
  "sample_teaching_plan": [],
  "notes": "Parsed from DATA PART 2"
}
```

Do not skip a major just because this Markdown does not list every course manually.

This file gives parser rules and examples. The parser should still extract all tables available in the raw document.

---

# 12. Handling electives and choice groups

Some curricula contain abstract rows such as:

```txt
Môn tự chọn ngành 1
Môn tự chọn ngành 2
Môn học tự chọn liên ngành 1
Môn cơ sở ngành-Lập trình 1: tự chọn
```

These are not real course codes.

Represent them in `sample_teaching_plan` using placeholders:

```json
{
  "semester": 5,
  "year": 3,
  "course_code": null,
  "course_name": "Môn tự chọn ngành 1",
  "credits": 4,
  "is_required": false,
  "is_elective": true,
  "placeholder_type": "major_elective",
  "notes": "Choose from major_elective course pool"
}
```

Later, during simulation, replace placeholders by sampling from matching elective pools.

---

# 13. Elective sampling pools

Create pools per major:

```json
{
  "major_id": "AI",
  "pools": {
    "major_elective": ["CS211", "CS315", "CS410", "CS431"],
    "interdisciplinary_elective": ["DS103", "CE340", "IS403", "SE113"],
    "graduation_topic": ["CS409", "CS405", "CS406", "CS419", "CS412"]
  }
}
```

For KTMT:

```json
{
  "major_id": "KTMT",
  "pools": {
    "embedded_iot": ["CE232", "CE439", "CE339", "CE340", "CE410"],
    "robotics_ai": ["CE233", "CE347", "CE440", "CE320", "CE406"],
    "graduation_topic": ["CE510", "CE511"]
  }
}
```

For KHDL:

```json
{
  "major_id": "KHDL",
  "pools": {
    "data_analysis": ["DS304", "DS307", "DS200", "DS315", "DS325"],
    "machine_learning": ["DS201", "DS322", "DS317", "DS318"],
    "statistics": ["DS302", "DS303", "DS308"],
    "project": ["DS204", "DS207", "DS309"]
  }
}
```

---

# 14. Validation rules for Part 2

Run the same validation as Part 1.

Additional Part 2 checks:

```txt
1. Choice groups must have at least 2 courses.
2. Placeholder electives must include placeholder_type.
3. Every placeholder_type should have a matching elective pool.
4. Graduation options should not be assigned to year 1-3 unless explicitly allowed.
5. Direction-specific courses should include specialization field if applicable.
6. Courses marked BB or Bắt buộc should have is_required = true.
7. Courses marked Tự chọn or Chọn should have is_elective = true.
```

---

## 15. Output validation report

Create:

```txt
outputs/validation/curriculum_p2_validation_report.json
```

Structure:

```json
{
  "data_part": "PART_2",
  "source_file": "Ngành, CTDT và VD KHDG 2.docx",
  "total_majors": 0,
  "total_courses": 0,
  "total_sample_plan_items": 0,
  "warnings": [],
  "errors": []
}
```

---

# 16. Merge rules for all curriculum parts

After parsing both parts, create:

```txt
merge_curriculum_parts.py
```

Input:

```txt
data/normalized/normalized_curriculum_p1.json
data/normalized/normalized_curriculum_p2.json
```

Output:

```txt
data/normalized/normalized_curriculum_all.json
```

Merge rules:

```txt
1. Merge by major_id.
2. Within each major, merge courses by course_code.
3. If the same course appears twice with identical information, keep one.
4. If the same course appears twice with different course_block values, keep both only if they are genuinely used in different roles; otherwise keep the more specific block.
5. Merge sample_teaching_plan by major_id + semester + course_code.
6. Keep source_part metadata for traceability.
```

Each course should include:

```json
"source_part": "PART_2"
```

or:

```json
"source_part": "PART_1"
```

---

# 17. How this file connects to simulation

The simulation should not directly read Word documents.

Pipeline:

```txt
raw DOCX curriculum
        ↓
parse_curriculum.py
        ↓
normalized_curriculum_p1.json
normalized_curriculum_p2.json
        ↓
merge_curriculum_parts.py
        ↓
normalized_curriculum_all.json
        ↓
simulate_students.py
```

The simulation uses only:

```txt
normalized_curriculum_all.json
```

---

# 18. Important note

Do not manually hard-code every course in simulation scripts.

Courses should come from normalized curriculum files.

This Markdown gives parsing and modeling instructions only.

If the raw curriculum document changes, only the normalization step should need updating.
