# CS117 - Detailed Problem Breakdown

## Đánh giá và đề xuất vị trí phù hợp để triển khai phòng tư vấn tâm lý trong khuôn viên UIT

---

# 0. Nguyên tắc thiết kế cuối cùng

Tài liệu này mô tả bài toán theo đúng hướng **Input → Processing → Output → Evaluation**.

Bài toán không được xem là một ứng dụng phần mềm hoàn chỉnh. Bài toán được xem là một quy trình tính toán: với các dữ liệu đầu vào đã được chuẩn hóa, ta tính toán và đưa ra vị trí phù hợp nhất để đặt phòng tư vấn tâm lý tại UIT.

## In-scope

Sau khi rà soát lại, bài toán chỉ giữ lại ba trục đánh giá chính:

```txt
Accessibility + Visibility + Privacy
```

Trong đó:

- **Accessibility**: sinh viên có thể tiếp cận phòng tư vấn thuận lợi hay không.
- **Visibility**: sinh viên có cơ hội nhận diện sự tồn tại của phòng tư vấn hay không.
- **Privacy**: sinh viên có cảm thấy ít bị phơi bày khi tiếp cận hoặc sử dụng phòng tư vấn hay không.

## Out-of-scope

Dữ liệu CTĐT/KHDG/số tín chỉ/academic pressure bị loại khỏi mô hình chính vì không thể ngoại suy nhu cầu tư vấn tâm lý của sinh viên chỉ từ dữ liệu học tập. Bài toán không cố gắng suy luận trạng thái tâm lý, mức độ stress, hay nhu cầu hỗ trợ tâm lý của từng nhóm sinh viên.

---

# 1. Định nghĩa bài toán

## 1.1. Tên bài toán

**Đánh giá và đề xuất vị trí phù hợp để triển khai phòng tư vấn tâm lý trong khuôn viên UIT**

## 1.2. Phát biểu bài toán

UIT cần lựa chọn một phòng hoặc vị trí phù hợp để triển khai phòng tư vấn tâm lý cho sinh viên.

Với các dữ liệu đầu vào đã được chuẩn hóa gồm:

- thời khóa biểu học tập,
- đồ thị không gian UIT,
- danh sách các phòng ứng viên,

bài toán cần tính toán và đề xuất một vị trí phù hợp nhất, đồng thời cung cấp các vị trí thay thế và giải thích vì sao vị trí đó được đề xuất.

Bài toán không nhằm dự đoán tâm lý cá nhân, không phân loại sinh viên, không chẩn đoán sức khỏe tinh thần, và không mô phỏng đầy đủ hành vi thật của sinh viên. Bài toán chỉ đánh giá vị trí đặt phòng tư vấn dựa trên các đặc điểm không gian và luồng di chuyển được suy ra từ thời khóa biểu.

---

# 2. Input

## D1. Dữ liệu thời khóa biểu học tập

Dữ liệu thời khóa biểu mô tả việc sinh viên hoặc lớp học phần có mặt ở phòng nào, vào thời điểm nào trong tuần.

Trong phạm vi bài toán, dữ liệu thời khóa biểu được giả định đã được chuyển hóa về dạng thuận lợi cho tính toán.

### Cấu trúc thời khóa biểu tiêu chuẩn của UIT

Tất cả thời khóa biểu của sinh viên UIT trong 1 tuần đi học thông thường.

### Vai trò của D1 trong bài toán

D1 được sử dụng để trích xuất các cặp di chuyển giữa các phòng học theo thời gian.

Ví dụ:

```txt
Sinh viên S001:
Thứ 2, tiết 1-3: C103
Thứ 2, tiết 4-5: B204

=> transition: C103 → B204
```

Các transition này không phải lộ trình thật tuyệt đối, mà là nhu cầu di chuyển bắt buộc hoặc có khả năng xảy ra giữa các vị trí học tập.

---

## D2. Đồ thị không gian UIT

D2 là biểu diễn không gian của UIT dưới dạng đồ thị vô hướng có trọng số:

G=(V,E)

Trong đó:

- V là tập node
- E là tập edge

Node gồm:
- Room Node
- Access Node
- Hub Node

Edge gồm:
- Room–Access
- Hallway
- Stair/Elevator
- Inter-building

Mỗi edge có trọng số biểu diễn khoảng cách hoặc chi phí di chuyển.

---

## D3. Danh sách vị trí ứng viên

D3 là danh sách các phòng có thể được xem xét để đặt phòng tư vấn tâm lý, do stakeholder cung cấp.

---

# 3. Output

Output của bài toán gồm:

```txt
- Vị trí đề xuất chính
- Danh sách vị trí thay thế
- Bảng điểm giải thích cho từng vị trí
- Báo cáo trade-off giữa Accessibility, Visibility và Privacy
```

Mỗi candidate trong output gồm:

```txt
candidate_room
accessibility_indicator
visibility_indicator
privacy_indicator
final_rank
explanation
```

Lưu ý: các chỉ số accessibility/visibility/privacy là **thông số giải thích bên trong mô hình**, không phải metric thành công cuối cùng của dự án.

---

# 4. Requirements

## Functional

### R1. Accessibility

Vị trí được đề xuất phải giúp sinh viên tiếp cận dịch vụ tư vấn dễ dàng hơn so với vị trí hiện tại hoặc so với đa số vị trí ứng viên khác.

### R2. Visibility

Vị trí được đề xuất phải có cơ hội được sinh viên nhận diện trong quá trình di chuyển trong trường.

### R3. Privacy

Vị trí được đề xuất phải hạn chế cảm giác bị phơi bày khi sinh viên tiếp cận hoặc sử dụng dịch vụ tư vấn.

## Non-functional

## R4. Explainability

Kết quả đề xuất phải giải thích được vì sao một vị trí được chọn, đặc biệt khi có đánh đổi giữa accessibility, visibility và privacy.

## R5. Runtime

Với dữ liệu đầu vào đã được chuyển hóa đúng định dạng, quy trình tính toán phải hoàn thành trong thời gian chấp nhận được.

Trong phạm vi đồ án, mục tiêu thời gian chạy là:

```txt
Runtime <= 10 giây
```

trên bộ dữ liệu UIT đã chuẩn hóa.

---

# 5. Constraints

## C1. Thời khóa biểu phải ở dạng bảng

Mỗi thời khóa biểu được tiêu chuẩn có dạng bảng:

```txt
Hàng:   Tiết 1 2 3 4 5 | Trưa | Tiết 6 7 8 9 10 | Sau 17h
Cột:    Thứ 2, Thứ 3, Thứ 4, Thứ 5, Thứ 6, Thứ 7
```

Một môn học có thể kéo dài nhiều tiết liên tục.

Mỗi ô hoặc cụm ô trong thời khóa biểu cần có ít nhất:

```txt
- Mã môn học
- Tên môn học nếu có
- Phòng học
```

Phòng học của UIT được giả định có định dạng:

```txt
[Tòa][Tầng][Số hiệu phòng]
```

Ví dụ:

```txt
C103 = Tòa C, tầng 1, phòng 03
B204 = Tòa B, tầng 2, phòng 04
```
## C2. Đồ thị khuôn viên trường phải được quy định sẵn

- Graph phải là đồ thị vô hướng có trọng số.
- Trọng số edge phải dương.
- Mọi candidate room phải tồn tại trong graph.
- Mọi room node phải kết nối tới ít nhất một access node.
- Đồ thị khuôn viên trường được xây dựng tĩnh, không tự động phản ánh các biến động vật lý tạm thời


## C3. Không tính tiết bù

Dữ liệu thời khóa biểu chỉ xét các lịch học chính thức theo tuần.

Các tiết học bù, học thay, hoặc lịch học phát sinh tạm thời không được tính vào mô hình.

Lý do:

- tiết bù không phản ánh luồng di chuyển ổn định,
- tiết bù có thể gây nhiễu khi ước lượng traffic thường kỳ,
- bài toán cần đánh giá vị trí dựa trên hoạt động lặp lại trong trường.

---

## C4. Không có dữ liệu quan sát lộ trình thực tế

Từ thời khóa biểu, hệ thống chỉ biết sinh viên cần có mặt ở phòng nào và vào thời điểm nào. Hệ thống không có dữ liệu GPS, camera, check-in hoặc quan sát thực địa để biết lộ trình thật của sinh viên.

Vì vậy, bài toán chỉ được phép ước lượng lộ trình di chuyển từ thời khóa biểu và graph không gian, không khẳng định đó là lộ trình thực tế tuyệt đối.

---

## C5. Bài toán chỉ xét tập phòng ứng viên được cung cấp

D3 được giữ đơn giản:

```txt
candidate_rooms = [room_id_1, room_id_2, ..., room_id_k]
```

Mỗi candidate là một phòng đã tồn tại trong đồ thị `G`.

Ví dụ:

```txt
A105
B203
C102
E201
```

Nếu một phòng không nằm trong danh sách ứng viên, hệ thống không đề xuất phòng đó.

Bài toán là:

```txt
ranking trên candidate rooms
```

không phải:

```txt
tìm kiếm mọi vị trí có thể trong toàn bộ trường
```

---

## C6 Không suy luận tâm lý sinh viên

Hệ thống không dùng CTĐT, KHDG, tín chỉ hoặc loại môn học để suy luận mức độ stress hoặc nhu cầu tư vấn của sinh viên.

Bài toán chỉ dùng dữ liệu không gian và thời khóa biểu để đánh giá vị trí.

---

# 6. Assumptions

## A1. Thời khóa biểu phản ánh hoạt động học tập ổn định

Thời khóa biểu chính thức được xem là nguồn dữ liệu đủ đại diện cho các luồng di chuyển thường xuyên của sinh viên trong trường.

## A2. Sinh viên có xu hướng chọn tuyến đường chi phí thấp

Khi không có dữ liệu quan sát thực tế, hệ thống giả định sinh viên thường chọn tuyến đường ngắn hoặc thuận tiện giữa hai phòng học liên tiếp. Nếu có nhiều tuyến đường có chi phí tương đương, tức không dài hơn 15% so với tuyến ngắn nhất, lưu lượng được chia đều cho các tuyến đó.

## A3. Đi ngang qua access node tạo ra cơ hội nhận diện

Nếu một tuyến đường đi qua node giao giữa đường đi và phòng ứng viên, hệ thống xem đó là một cơ hội để sinh viên nhận diện sự tồn tại của phòng tư vấn.

## A4. Privacy được đánh giá qua mức độ phơi bày không gian

Một candidate được xem là kém riêng tư hơn nếu lối vào hoặc vùng chờ của nó nằm gần các tuyến di chuyển đông hoặc các node chốt có nhiều người đi qua.

## A5. Candidate list đã được stakeholder chấp nhận trước.

Một phòng nằm trong danh sách ứng viên được giả định là đã đủ điều kiện tối thiểu để được xem xét trong phạm vi bài toán.

## A6. Phân bố sinh viên qua các cổng được giả định cân bằng khi thiếu dữ liệu

Khi không có dữ liệu thống kê về phương tiện di chuyển, hệ thống giả định tỉ lệ sinh viên đi qua các cổng chính là tương đương nhau. Ví dụ, tỉ lệ sinh viên đi xe máy qua khu nhà xe/cổng A được giả định tương đương với tỉ lệ sinh viên đi xe buýt qua các cổng liên quan.

---

# 7. Decomposition Hierarchy / Breakdown Tree

## Root Problem

**Đề xuất vị trí phù hợp nhất để đặt phòng tư vấn tâm lý trong UIT dựa trên Accessibility, Visibility và Privacy.**

Input:

```txt
D1. Thời khóa biểu chuẩn hóa
D2. Đồ thị vô hướng có trọng số của UIT
D3. Danh sách phòng ứng viên
```

Output:

```txt
Vị trí đề xuất chính, danh sách vị trí thay thế và giải thích trade-off.
```

---

## P1. Trích xuất nhu cầu di chuyển từ thời khóa biểu

Input:

```txt
- Thời khóa biểu chuẩn hóa D1
```

Output:

```txt
- Danh sách các cặp di chuyển room_i → room_j
```

Mục tiêu:

Chuyển thời khóa biểu thành các cặp phòng liên tiếp mà sinh viên hoặc nhóm sinh viên có khả năng cần di chuyển giữa chúng.

### P1.1. Sắp xếp các event theo thời gian

Input:

```txt
- Danh sách event trong thời khóa biểu
```

Output:

```txt
- Danh sách event theo từng sinh viên/nhóm sinh viên, sắp xếp theo ngày và tiết học
```

Giải pháp:

Sắp xếp event theo:

```txt
student_id/group_id → day_of_week → start_period
```

### P1.2. Loại bỏ tiết bù

Input:

```txt
- Danh sách event đã sắp xếp
```

Output:

```txt
- Danh sách event chính thức, không gồm tiết bù
```

Giải pháp:

Lọc bỏ các event có nhãn:

```txt
makeup = true
```

hoặc nằm ngoài lịch học chính thức theo tuần.

### P1.3. Trích xuất cặp di chuyển liên tiếp

Input:

```txt
- Danh sách event chính thức đã sắp xếp
```

Output:

```txt
- origin_destination_pairs
```

Giải pháp:

Với mỗi sinh viên/nhóm sinh viên trong cùng một ngày, lấy các cặp event liên tiếp:

```txt
room_i → room_j
```

nếu `room_i != room_j`.

---

## P2. Ước lượng tuyến đường và lưu lượng trên graph

Input:

```txt
- origin_destination_pairs
- đồ thị UIT G = (V, E)
```

Output:

```txt
- estimated_routes
- node_traffic
- edge_traffic
- access_node_pass_count
```

Mục tiêu:

Ước lượng các tuyến đường sinh viên có khả năng đi qua và tổng hợp lưu lượng trên node/edge.

### P2.1. Tìm đường đi giữa hai phòng

Input:

```txt
- origin room
- destination room
- graph G
```

Output:

```txt
- route = danh sách node/edge trên đường đi
```

Giải pháp:

Dùng Dijkstra hoặc shortest path trên đồ thị vô hướng có trọng số.

### P2.2. Tổng hợp node traffic

Input:

```txt
- estimated_routes
```

Output:

```txt
- node_traffic[v]
```

Giải pháp:

Đếm số lần mỗi node xuất hiện trong các tuyến đường ước lượng.

### P2.3. Tổng hợp edge traffic

Input:

```txt
- estimated_routes
```

Output:

```txt
- edge_traffic[e]
```

Giải pháp:

Đếm số lần mỗi edge xuất hiện trong các tuyến đường ước lượng.

### P2.4. Tổng hợp lượt đi ngang access node

Input:

```txt
- estimated_routes
- access nodes của các phòng ứng viên
```

Output:

```txt
- access_node_pass_count[candidate]
```

Giải pháp:

Với mỗi route, nếu route đi qua access node của một candidate, tăng bộ đếm của candidate đó.

---

## P3. Đánh giá Accessibility của candidate

Input:

```txt
- graph G
- candidate rooms
- node_traffic
- origin activity nodes
```

Output:

```txt
- accessibility_indicator cho từng candidate
```

Mục tiêu:

Đánh giá candidate có thuận tiện để sinh viên tiếp cận hay không.

### P3.1. Tính khoảng cách từ các node hoạt động đến candidate

Input:

```txt
- candidate room
- activity nodes có traffic
- graph G
```

Output:

```txt
- distance(activity_node, candidate)
```

Giải pháp:

Dùng shortest path từ các activity node đến candidate.

### P3.2. Tính chi phí tiếp cận có trọng số

Input:

```txt
- distances
- traffic weight của activity nodes
```

Output:

```txt
- Average Weighted Travel Cost
```

Giải pháp:

Tính trung bình khoảng cách đến candidate, có trọng số theo traffic của từng node hoạt động.

### P3.3. Chuẩn hóa chỉ số Accessibility

Input:

```txt
- Average Weighted Travel Cost của tất cả candidates
```

Output:

```txt
- accessibility_indicator trong khoảng [0, 1]
```

Giải pháp:

Chuẩn hóa sao cho chi phí thấp tương ứng với điểm accessibility cao.

---

## P4. Đánh giá Visibility của candidate

Input:

```txt
- candidate rooms
- access nodes
- node_traffic
- edge_traffic
- access_node_pass_count
```

Output:

```txt
- visibility_indicator cho từng candidate
```

Mục tiêu:

Đánh giá candidate có cơ hội được sinh viên nhận diện khi di chuyển trong trường hay không.

### P4.1. Xác định vùng nhận diện của candidate

Input:

```txt
- access node của candidate
- các node/edge lân cận
```

Output:

```txt
- exposure_zone(candidate)
```

Giải pháp:

Lấy access node của candidate và các node/edge lân cận trong bán kính graph nhất định.

### P4.2. Tính lượt đi ngang candidate

Input:

```txt
- access_node_pass_count
```

Output:

```txt
- pass_by_count(candidate)
```

Giải pháp:

Dùng số route đi qua access node hoặc exposure zone của candidate.

### P4.3. Chuẩn hóa chỉ số Visibility

Input:

```txt
- pass_by_count của tất cả candidates
```

Output:

```txt
- visibility_indicator trong khoảng [0, 1]
```

Giải pháp:

Chuẩn hóa sao cho candidate có nhiều lượt đi ngang hơn có visibility cao hơn.

---

## P5. Đánh giá Privacy của candidate

Input:

```txt
- candidate rooms
- access nodes
- node_traffic
- edge_traffic
- node chốt gần candidate
```

Output:

```txt
- privacy_indicator cho từng candidate
```

Mục tiêu:

Đánh giá mức độ phơi bày không gian của candidate khi sinh viên tiếp cận phòng.

### P5.1. Xác định vùng nhạy cảm của candidate

Input:

```txt
- room node
- access node
- node chốt lân cận
```

Output:

```txt
- sensitive_zone(candidate)
```

Giải pháp:

Vùng nhạy cảm gồm access node, các node gần cửa phòng, và nếu có, node đại diện khu vực chờ.

### P5.2. Tính exposure risk

Input:

```txt
- sensitive_zone
- node_traffic
- edge_traffic
```

Output:

```txt
- exposure_risk(candidate)
```

Giải pháp:

Tổng hợp traffic đi qua các node/edge thuộc vùng nhạy cảm. Traffic càng cao thì rủi ro phơi bày càng cao.

### P5.3. Chuẩn hóa chỉ số Privacy

Input:

```txt
- exposure_risk của tất cả candidates
```

Output:

```txt
- privacy_indicator trong khoảng [0, 1]
```

Giải pháp:

Chuẩn hóa sao cho exposure risk thấp tương ứng với privacy cao.

---

## P6. Xếp hạng candidate và sinh giải thích

Input:

```txt
- accessibility_indicator
- visibility_indicator
- privacy_indicator
- candidate rooms
```

Output:

```txt
- ranked_candidates
- primary_recommendation
- alternative_recommendations
- trade_off_explanation
```

Mục tiêu:

Kết hợp các chỉ số để xếp hạng các phòng ứng viên và giải thích kết quả.

### P6.1. Chuẩn hóa và kiểm tra chỉ số

Input:

```txt
- accessibility_indicator
- visibility_indicator
- privacy_indicator
```

Output:

```txt
- normalized_score_table
```

Giải pháp:

Đảm bảo các chỉ số cùng nằm trong thang [0, 1] và cùng chiều tốt hơn.

### P6.2. Tính điểm xếp hạng

Input:

```txt
- normalized_score_table
- trọng số của Accessibility, Visibility, Privacy
```

Output:

```txt
- final_score(candidate)
```

Giải pháp:

Tính điểm tổng hợp:

```txt
final_score = α * accessibility + β * visibility + γ * privacy
```

với:

```txt
α + β + γ = 1
```

### P6.3. Sinh giải thích trade-off

Input:

```txt
- final_score
- từng chỉ số thành phần
```

Output:

```txt
- explanation cho từng candidate top-k
```

Giải pháp:

So sánh các candidate theo từng tiêu chí và mô tả vì sao candidate được xếp cao.

---

# 8. Evaluation Metrics

Phần này đánh giá hiệu quả thực sự của lời giải sau khi vị trí được áp dụng, không chỉ đánh giá các chỉ số nội bộ của mô hình.

Các chỉ số nội bộ như:

```txt
Average Weighted Travel Cost
pass_by_count
exposure_risk
accessibility_indicator
visibility_indicator
privacy_indicator
```

được dùng để giải thích và tạo ranking, nhưng không phải metric cuối cùng để chứng minh hiệu quả thực tế.

---

## M1. Counseling Utilization Rate (CUR)

### Công thức

```txt
CUR = N_visit / N_student
```

Trong đó:

```txt
N_visit   = số lượt sử dụng dịch vụ tư vấn trong kỳ đánh giá
N_student = tổng số sinh viên thuộc phạm vi phục vụ
```

Nếu muốn chuẩn hóa theo tháng:

```txt
CUR_month = N_visit_month / N_student
```

### Ý nghĩa

CUR đo mức độ dịch vụ tư vấn thực sự được sử dụng.

Nếu vị trí mới tốt hơn, kỳ vọng CUR sẽ tăng so với vị trí cũ hoặc so với giai đoạn trước khi thay đổi.

### Requirement liên quan

```txt
R1 Accessibility
R2 Visibility
```

Vì một vị trí dễ tiếp cận và dễ nhận diện hơn thường có khả năng làm tăng số lượt sử dụng dịch vụ.

---

## M2. Unique User Penetration Rate (UPR)

### Công thức

```txt
UPR = N_unique / N_student
```

Trong đó:

```txt
N_unique  = số sinh viên khác nhau đã sử dụng dịch vụ trong kỳ đánh giá
N_student = tổng số sinh viên thuộc phạm vi phục vụ
```

### Ý nghĩa

UPR đo độ phủ của dịch vụ trong cộng đồng sinh viên.

CUR có thể tăng vì một nhóm nhỏ sinh viên sử dụng nhiều lần, còn UPR cho biết dịch vụ có tiếp cận được nhiều sinh viên khác nhau hay không.

### Requirement liên quan

```txt
R1 Accessibility
R2 Visibility
```

---

## M3. Location Impact Ratio (LIR)

### Công thức

```txt
LIR = CUR_after / CUR_before
```

Trong đó:

```txt
CUR_before = Counseling Utilization Rate trước khi thay đổi vị trí
CUR_after  = Counseling Utilization Rate sau khi áp dụng vị trí được đề xuất
```

### Ý nghĩa

LIR đo tác động tương đối của việc thay đổi vị trí.

```txt
LIR > 1  : mức sử dụng dịch vụ tăng
LIR = 1  : không thay đổi
LIR < 1  : mức sử dụng dịch vụ giảm
```

### Requirement liên quan

```txt
R1 Accessibility
R2 Visibility
Overall solution effectiveness
```

---

## M4. Relative Improvement (RI)

### Công thức

```txt
RI = ((CUR_after - CUR_before) / CUR_before) * 100%
```

### Ý nghĩa

RI cho biết mức tăng hoặc giảm phần trăm của tỉ lệ sử dụng dịch vụ sau khi thay đổi vị trí.

Ví dụ:

```txt
CUR_before = 1.5%
CUR_after  = 2.4%

RI = ((2.4 - 1.5) / 1.5) * 100% = 60%
```

Nghĩa là tỉ lệ sử dụng dịch vụ tăng 60%.

### Requirement liên quan

```txt
Overall solution effectiveness
```

---

## M5. Repeat Visit Rate (RVR)

### Công thức

```txt
RVR = N_return / N_unique
```

Trong đó:

```txt
N_return = số sinh viên quay lại sử dụng dịch vụ ít nhất một lần
N_unique = số sinh viên khác nhau đã từng sử dụng dịch vụ
```

### Ý nghĩa

RVR không đo riêng privacy, nhưng là một tín hiệu thực tế cho thấy sinh viên không chỉ đến một lần rồi dừng lại.

Nếu privacy quá kém, trải nghiệm tiếp cận có thể làm sinh viên ngại quay lại. Tuy nhiên, RVR cũng chịu ảnh hưởng bởi chất lượng tư vấn, lịch hẹn và nhiều yếu tố ngoài vị trí, nên cần diễn giải cẩn thận.

### Requirement liên quan

```txt
R3 Privacy
Overall service acceptability
```

---

## M6. Privacy Satisfaction Rate (PSR)

### Công thức

Dựa trên khảo sát ẩn danh sau khi sử dụng dịch vụ.

```txt
PSR = N_privacy_positive / N_survey
```

Trong đó:

```txt
N_privacy_positive = số phản hồi đánh giá mức riêng tư đạt ngưỡng tích cực
N_survey           = tổng số phản hồi khảo sát hợp lệ
```

Ví dụ với thang Likert 1-5:

```txt
positive nếu privacy_rating >= 4
```

### Ý nghĩa

PSR là metric thực tế trực tiếp hơn cho Privacy so với exposure risk nội bộ.

### Requirement liên quan

```txt
R3 Privacy
```

---

## M7. Stakeholder Interpretation Score (SIS)

### Công thức

Dựa trên đánh giá của stakeholder hoặc chuyên gia bằng thang Likert 1-5.

```txt
SIS = average(score_interpretability)
```

Trong đó `score_interpretability` đánh giá các câu hỏi như:

```txt
- Báo cáo có dễ hiểu không?
- Có thấy rõ vì sao vị trí A xếp trên vị trí B không?
- Trade-off giữa accessibility, visibility và privacy có được giải thích rõ không?
```

### Ý nghĩa

SIS đo mức độ stakeholder hiểu và chấp nhận được lời giải thích của hệ thống.

### Requirement liên quan

```txt
R4 Explainability
```

---

## Bảng ánh xạ Requirement - Real-world Metric

| Requirement | Real-world Metric chính | Metric phụ / hỗ trợ | Ý nghĩa |
|---|---|---|---|
| R1. Accessibility | CUR, LIR, RI | UPR | Nếu vị trí dễ tiếp cận hơn, mức sử dụng dịch vụ kỳ vọng tăng |
| R2. Visibility | UPR, CUR | LIR, RI | Nếu vị trí dễ được nhận diện hơn, nhiều sinh viên khác nhau có khả năng sử dụng hơn |
| R3. Privacy | PSR | RVR | Nếu vị trí đủ riêng tư, sinh viên đánh giá trải nghiệm tiếp cận tốt hơn và có thể quay lại |
| R4. Explainability | SIS | Trade-off report completeness | Stakeholder hiểu được vì sao vị trí được đề xuất |
| Runtime requirement | Runtime seconds | Pass/Fail dưới 10s | Giải pháp có chạy trong thời gian chấp nhận được không |

---

# 9. Solution Algorithm

Input:

```txt
D1. Thời khóa biểu chuẩn hóa
D2. Đồ thị không gian UIT
D3. Danh sách phòng ứng viên
```

Output:

```txt
Vị trí đề xuất chính, các vị trí thay thế, bảng điểm giải thích và trade-off report.
```

Thuật toán:

```txt
Step 1.
Đọc thời khóa biểu đã chuẩn hóa.

Step 2.
Sắp xếp event theo sinh viên/nhóm sinh viên, ngày học và tiết học.

Step 3.
Trích xuất các cặp di chuyển liên tiếp room_i → room_j.

Step 4.
Với mỗi cặp di chuyển, tìm đường đi ngắn nhất trên graph UIT.

Step 5.
Tổng hợp node traffic, edge traffic và access node pass count.

Step 6.
Với mỗi candidate, tính accessibility_indicator.

Step 7.
Với mỗi candidate, tính visibility_indicator.

Step 8.
Với mỗi candidate, tính privacy_indicator.

Step 9.
Chuẩn hóa các chỉ số thành phần.

Step 10.
Tính final_score cho từng candidate.

Step 11.
Xếp hạng candidates.

Step 12.
Xuất vị trí đề xuất chính, vị trí thay thế và giải thích trade-off.
```

---

# 10. Mapping Solution với Breakdown Tree

| Solution Step | Breakdown Node |
|---|---|
| Step 1-3 | P1.1, P1.2 |
| Step 4 | P1.3 |
| Step 5 | P2.1 |
| Step 6 | P2.2, P2.3, P2.4 |
| Step 7 | P3 |
| Step 8 | P4 |
| Step 9 | P5 |
| Step 10-13 | P6 |

---

# 11. Ethical & Social Issues

## 11.1. Không suy luận sức khỏe tâm lý cá nhân

Bài toán không dùng dữ liệu học tập để suy luận stress, nguy cơ tâm lý hoặc nhu cầu tư vấn của từng sinh viên.

## 11.2. Ẩn danh dữ liệu sinh viên

Nếu dữ liệu thời khóa biểu có student_id, mã định danh phải được ẩn danh trước khi xử lý.

## 11.3. Không theo dõi thời gian thực

Mô hình không sử dụng GPS, camera hoặc dữ liệu định vị thời gian thực.

## 11.4. Không gán nhãn khu vực hoặc nhóm sinh viên

Không được kết luận rằng một tòa nhà, ngành học hoặc nhóm sinh viên có vấn đề tâm lý dựa trên traffic hoặc vị trí.

## 11.5. Metric thực tế cần diễn giải cẩn thận

Các real-world metrics như CUR, UPR, RVR có thể chịu ảnh hưởng bởi nhiều yếu tố ngoài vị trí, như chất lượng tư vấn, truyền thông, lịch hẹn và chính sách nhà trường.

Do đó, chúng được dùng để đánh giá hiệu quả tổng thể sau triển khai, không để quy kết nguyên nhân tuyệt đối.

## 11.6. Vai trò hỗ trợ ra quyết định

Kết quả của bài toán là công cụ hỗ trợ ra quyết định. Quyết định cuối cùng vẫn thuộc về nhà trường và các bên liên quan.
