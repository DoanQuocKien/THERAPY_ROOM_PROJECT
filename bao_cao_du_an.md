# BÁO CÁO DỰ ÁN: ĐÁNH GIÁ VÀ XẾP HẠNG CÁC VỊ TRÍ ỨNG VIÊN CHO PHÒNG TƯ VẤN TÂM LÝ TẠI UIT

**Môn học:** Tư duy Tính toán / Tư duy AI (Computational / AI Thinking - CS117)  
**Lớp:** CS117.Q21.KHTN  
**Nhóm thực hiện:**
- Đoàn Quốc Kiên - MSSV: 24520879
- Hà Thanh Phong - MSSV: 24520024

---

## MỤC LỤC
1. [Định nghĩa và Làm rõ Bài toán (Problem Definition/Clarification)](#1-định-nghĩa-và-làm-rõ-bài-toán-problem-definitionclarification)
2. [Các Dữ liệu Đầu vào của Hệ thống (Inputs)](#2-các-dữ-liệu-đầu-vào-của-hệ-thống-inputs)
3. [Các Giả định Mô hình hóa (Model Assumptions)](#3-các-giả-định-mô-hình-hóa-model-assumptions)
4. [Các Ràng buộc của Hệ thống (Constraints)](#4-các-ràng-buộc-của-hệ-thống-constraints)
5. [Các Chỉ số Đo lường và Đánh giá (Metrics)](#5-các-chỉ-số-đo-lường-và-đánh-giá-metrics)
6. [Các Yêu cầu Phi chức năng (Non-Functional Requirements)](#6-các-yêu-cầu-phi-chức-năng-non-functional-requirements)
7. [Vận dụng Computational/AI Thinking (CAT) trong Giải quyết Vấn đề](#7-vận-dụng-computationalai-thinking-cat-trong-giải-quyết-vấn-đề)
8. [Cây Phân rã Bài toán (Decomposition Hierarchy/Breakdown Tree)](#8-cây-phân-rã-bài-toán-decomposition-hierarchybreakdown-tree)
9. [Chi tiết Kiến trúc Giải pháp & Các Module Thành phần (Solution & Modules)](#9-chi-tiết-kiến-trúc-giải-pháp-các-module-thành-phần-solution-modules)
10. [Chi tiết Luồng Dữ liệu (Data Flow Diagram)](#10-chi-tiết-luồng-dữ-liệu-data-flow-diagram)
11. [Chi tiết Thu thập và Xử lý Dữ liệu Kiểm chứng (Evaluation Data)](#11-chi-tiết-thu-thập-và-xử-lý-dữ-liệu-kiểm-chứng-evaluation-data)
12. [Đạo đức và Tác động Xã hội (Ethic & Social Impacts)](#12-đạo-đức-và-tác-động-xã-hội-ethic-social-impacts)
13. [Kết luận và Khuyến nghị Phát triển](#13-kết-luận-và-khuyến-nghị-phát-triển)

---

## 1. Định nghĩa và Làm rõ Bài toán (Problem Definition/Clarification)

### 1.1. Bối cảnh Dự án
Trong môi trường giáo dục đại học hiện đại, đặc biệt là tại một trường đào tạo khối ngành kỹ thuật công nghệ như Trường Đại học Công nghệ Thông tin - ĐHQG-HCM (UIT), áp lực học tập, nghiên cứu khoa học cùng các vấn đề cá nhân khác khiến nhu cầu được chăm sóc sức khỏe tinh thần của sinh viên ngày càng tăng cao. Phòng tư vấn tâm lý đóng vai trò vô cùng quan trọng trong việc hỗ trợ sinh viên giải tỏa căng thẳng, định hướng bản thân và vượt qua các khủng hoảng tâm lý.

Tuy nhiên, việc thiết lập một phòng tư vấn tâm lý không đơn thuần là chọn một phòng trống ngẫu nhiên trên bản đồ trường. Vị trí của phòng tư vấn tâm lý chịu ảnh hưởng bởi một bài toán tối ưu hóa đa mục tiêu cực kỳ phức tạp:
- **Tính riêng tư (Privacy):** Sinh viên khi tìm đến phòng tư vấn tâm lý thường e ngại sự phán xét từ bạn bè xung quanh. Do đó, phòng cần nằm ở một khu vực không quá đông đúc, ít bị quan sát trực tiếp bởi những người qua đường để đảm bảo cảm giác an toàn và bảo mật thông tin cá nhân.
- **Tính tiếp cận (Accessibility):** Phòng không được nằm ở nơi quá hẻo lánh, khó tìm hoặc tốn quá nhiều thời gian di chuyển của sinh viên từ các khu vực học tập chính (như giảng đường, thư viện). Nếu vị trí quá khó tiếp cận, tỷ lệ sử dụng dịch vụ sẽ giảm sút nghiêm trọng.
- **Tính hiển thị (Visibility):** Sinh viên cần phải biết đến sự tồn tại của phòng tư vấn. Phòng cần nằm ở khu vực có mật độ đi lại vừa phải của sinh viên để tạo độ nhận diện tự nhiên, giúp sinh viên ghi nhớ vị trí và dễ dàng tìm đến khi phát sinh nhu cầu.

Dự án này ra đời nhằm xây dựng một mô hình hỗ trợ ra quyết định khoa học, dựa trên dữ liệu không gian và dòng di chuyển của sinh viên được suy diễn từ thời khóa biểu học tập, để đánh giá và xếp hạng các vị trí phòng ứng viên tiềm năng cho phòng tư vấn tâm lý tại UIT.

### 1.2. Định nghĩa Bài toán (Problem Definition)
Hệ thống nhận vào danh sách các phòng ứng viên tiềm năng (Candidate Room List) do nhà trường đề xuất, cùng với đồ thị không gian của toàn bộ khuôn viên UIT và danh sách thời khóa biểu học tập của sinh viên. Mục tiêu là:
- Đánh giá và xếp hạng các phòng ứng viên dựa trên việc tối ưu hóa đồng thời các chỉ số về khả năng tiếp cận (Accessibility), độ hiển thị (Visibility) và tính riêng tư (Privacy).
- Đưa ra khuyến nghị đối với **1 phòng tối ưu nhất (Primary Recommended Room)** và **3 phòng thay thế tốt tiếp theo (Alternative Rooms)** (hoặc $k-1$ phòng thay thế nếu số lượng ứng viên ban đầu $k \le 3$).
- Cung cấp một báo cáo phân tích so sánh và đánh đổi (Rule-based Trade-off Report) cho mỗi phòng ứng viên để các nhà quản lý nhà trường hiểu rõ tại sao vị trí đó được chọn hoặc không được chọn.

### 1.3. Xác định Phạm vi Dự án (Scoping & Out of Scope)
Để tránh các hiểu lầm về chức năng của hệ thống trong thực tế, dự án xác định rõ ranh giới như sau:

#### Trong phạm vi (In-Scope):
- Đánh giá chất lượng vị trí dựa trên các thuộc tính không gian hình học (tọa độ vật lý, cấu trúc tòa nhà, cầu thang, thang máy, hành lang).
- Ước lượng mật độ và dòng di chuyển của sinh viên dựa trên thời khóa biểu học tập hàng tuần của các lớp học tại UIT.
- Xếp hạng các phòng dựa trên mô hình toán học tối ưu hóa đa mục tiêu và cung cấp báo cáo giải thích các thông số kỹ thuật.

#### Ngoài phạm vi (Out-of-Scope):
- **Không** dự đoán hay phân tích trạng thái tâm lý cá nhân của bất kỳ sinh viên nào.
- **Không** phân loại, gắn nhãn sinh viên dựa trên sức khỏe tinh thần hoặc hành vi.
- **Không** chẩn đoán hay can thiệp y tế/tâm thần học.
- **Không** sử dụng các camera giám sát hay thiết bị định vị thời gian thực (như GPS, Wi-Fi tracking) để theo dõi sinh viên thực tế. Hệ thống chỉ thực hiện mô phỏng dòng di chuyển dựa trên dữ liệu thời khóa biểu danh nghĩa.
- Hệ thống đóng vai trò là một công cụ hỗ trợ ra quyết định cho ban quản lý nhà trường, chứ **không thay thế hoàn toàn phán đoán và quyết định cuối cùng của con người**.

---

## 2. Các Dữ liệu Đầu vào của Hệ thống (Inputs)

Để mô hình hóa không gian trường học và dòng di chuyển của sinh viên, hệ thống yêu cầu ba thành phần dữ liệu đầu vào chính. Các dữ liệu này được ký hiệu lần lượt là $D_1, D_2,$ và $D_3$.

### 2.1. Danh sách Sự kiện Hàng tuần của Sinh viên UIT ($D_1$)
Dữ liệu $D_1$ đại diện cho hành vi sinh hoạt học thuật của toàn bộ sinh viên tại trường thông qua thời khóa biểu chính thức. Mỗi sự kiện học tập (buổi học, thi, sinh hoạt chuyên đề) được ghi nhận cụ thể nhằm xác định nhu cầu có mặt của sinh viên tại các địa điểm nhất định theo thời gian.
*   **Thành phần của một sự kiện:** Mỗi bản ghi sự kiện bao gồm:
    *   `room_id`: Mã định danh phòng diễn ra sự kiện.
    *   `weekday`: Ngày trong tuần (Thứ Hai đến Chủ Nhật).
    *   `start_period` (Tiết bắt đầu) và `end_period` (Tiết kết thúc): Xác định khung thời gian sinh viên có mặt tại phòng học.
*   **Định dạng của `room_id`:** Định dạng tiêu chuẩn tuân theo cấu trúc: `[Building][Floor][Room Number]`.
    *   *Building (Tòa nhà):* Ký tự chữ đại diện cho block tòa nhà (Ví dụ: A, B, C, E...).
    *   *Floor (Tầng):* Ký số đại diện cho số tầng (Ví dụ: 1, 2, 3... trong đó tầng trệt thường là 1).
    *   *Room Number (Số phòng):* Ký số gồm 2 chữ số đại diện cho số thứ tự phòng trong tầng.
    *   *Ví dụ minh họa:* `C103` đại diện cho Phòng số 03 nằm tại Tầng 1 của Tòa nhà C.
*   **Ý nghĩa mô hình hóa:** Từ dữ liệu thời khóa biểu này, hệ thống có thể suy ra số lượng sinh viên ước tính sẽ có mặt tại một phòng học cụ thể vào một ngày và tiết học cụ thể. Từ đó, xác định được các cặp điểm xuất phát (Origin) và điểm đích (Destination) khi sinh viên di chuyển giữa các tiết học kế tiếp nhau trong tuần.

### 2.2. Đồ thị Không gian UIT ($D_2$)
Đồ thị không gian $D_2$ là xương sống của toàn bộ hệ thống, mô tả cấu trúc vật lý của khuôn viên trường UIT dưới dạng một đồ thị có trọng số nhúng trong không gian: $G = (V, E, pos, w)$.

#### 2.2.1. Tập hợp các đỉnh không gian ($V$ - Spatial Nodes)
Tập hợp các đỉnh $V$ đại diện cho các vị trí vật lý quan trọng trên bản đồ trường, được chia làm 3 loại chính:
1.  **Đỉnh Phòng học (Room Nodes):** Đại diện cho các phòng học vật lý cụ thể, được định danh bằng `room_id` tương thích với dữ liệu $D_1$. Đây là các điểm xuất phát (Origin) hoặc điểm đích (Destination) của các dòng di chuyển sinh viên.
2.  **Đỉnh Tiếp cận (Access Nodes):** Đại diện cho các điểm lối vào ngay trước cửa phòng học hoặc các vị trí trên hành lang, lối đi bộ. Các đỉnh này đóng vai trò trung gian kết nối các phòng học với mạng lưới giao thông nội khu và là nơi đo lường lượng người đi qua (pass-by traffic) trước cửa mỗi phòng.
3.  **Đỉnh Kiểm soát/Điểm mốc (Checkpoint Nodes):** Đại diện cho các vị trí chuyển tiếp và các địa điểm công cộng quan trọng trong trường như cổng chính (Gate A, Gate B), khu vực giữ xe (parking area), thư viện, các góc tòa nhà, trung tâm sảnh lớn và các lối vào/ra chính của các tòa nhà.

#### 2.2.2. Tọa độ không gian ($pos(v)$)
Mỗi đỉnh $v \in V$ được gắn với một tọa độ không gian 3 chiều $pos(v) = (x, y, z)$:
*   $x, y$: Là tọa độ trên mặt bằng sàn (mặt phẳng 2D), giúp xác định khoảng cách hình học theo chiều ngang.
*   $z$: Đại diện cho mức độ cao tương đối theo tầng (floor level) để mô tả cấu trúc phân tầng của các tòa nhà cao tầng tại UIT.

#### 2.2.3. Tập hợp các cạnh di chuyển hợp lệ ($E$ - Valid Edges)
Tập hợp các cạnh $E$ đại diện cho các lối đi hợp lệ kết nối các đỉnh trong khuôn viên trường, bao gồm ba loại chính:
1.  **Cạnh Hành lang (Hallway Edges):** Kết nối các đỉnh tiếp cận và đỉnh phòng học cùng nằm trên một hành lang bên trong một tòa nhà.
2.  **Cạnh Cầu thang/Thang máy (Staircase/Elevator Edges):** Kết nối thẳng đứng giữa các tầng khác nhau trong cùng một tòa nhà (thay đổi giá trị tọa độ $z$).
3.  **Cạnh Liên tòa nhà (Inter-building Edges):** Các tuyến đường đi bộ ngoài trời kết nối các tòa nhà với nhau và kết nối các tòa nhà tới các đỉnh checkpoint (như cổng trường, bãi xe).

#### 2.2.4. Trọng số cạnh ($w(e)$)
Mỗi cạnh $e \in E$ có một trọng số $w(e) > 0$. Trọng số này biểu thị chi phí di chuyển thực tế (movement cost) qua cạnh đó. Chi phí này có thể được tính bằng khoảng cách vật lý (mét) hoặc thời gian di chuyển dự kiến, có tính đến các hệ số cản trở di chuyển thẳng đứng (như leo cầu thang bộ).

### 2.3. Danh sách Phòng Ứng viên ($D_3$)
Dữ liệu $D_3$ là danh sách gồm $k$ giá trị `room_id` ($k > 0$) đại diện cho các phòng học hoặc không gian trống hiện đang có sẵn mà nhà trường cân nhắc để đặt phòng tư vấn tâm lý. Đây chính là đối tượng cần được đánh giá, chấm điểm và xếp hạng để tìm ra vị trí tối ưu nhất.
*   *Trường hợp $k \le 3$:* Hệ thống sẽ đánh giá toàn bộ và trả về $k - 1$ phòng thay thế tốt nhất bên cạnh phòng được khuyến nghị cao nhất.
*   *Trường hợp $k > 3$:* Hệ thống sẽ trả về 1 phòng tối ưu nhất cùng đúng 3 lựa chọn thay thế tốt tiếp theo.

---

## 3. Các Giả định Mô hình hóa (Model Assumptions)

Để chuyển đổi một bài toán thực tế phức tạp về hành vi di chuyển của con người trong không gian thành một mô hình tính toán có thể thực thi được, dự án thiết lập một số giả định khoa học sau đây:

### 3.1. Giả định về Hành vi Lựa chọn Tuyến đường của Sinh viên
Trong thế giới thực, sinh viên không phải lúc nào cũng chọn duy nhất một con đường ngắn nhất tuyệt đối (shortest path) do các yếu tố như: độ đông đúc, thời tiết (nắng/mưa), thói quen cá nhân hoặc đi cùng bạn bè.
*   **Mô hình hóa đường đi:** Hệ thống giả định rằng sinh viên sẽ lựa chọn ngẫu nhiên (phân phối đều) một trong các tuyến đường khả thi có tổng chi phí di chuyển không vượt quá **$1.15 \times$ chi phí của đường đi ngắn nhất** ($cost \le 1.15 \times shortest\_path\_cost$).
*   **Ý nghĩa thực tế:** Hệ số $1.15$ (tương đương biên sai số $15\%$) đại diện cho tính "hợp lý có giới hạn" (bounded rationality) trong hành vi di chuyển của con người. Điều này giúp mô hình hóa phân tán dòng người một cách thực tế hơn trên nhiều lối đi song song, thay vì tập trung toàn bộ lưu lượng vào duy nhất một tuyến đường ngắn nhất.
*   **Giả định về tốc độ:** Tốc độ di chuyển của mọi sinh viên được giả định là như nhau trên tất cả các loại địa hình đường phẳng.

### 3.2. Giả định Phân phối Lưu lượng tại các Lối vào (Entry Points)
Đối với dòng sinh viên di chuyển từ bên ngoài vào trường học hoặc ngược lại (ví dụ: sinh viên đi học ca đầu tiên hoặc ra về sau ca cuối):
*   **Quy tắc phân phối:** Hệ thống giả định dòng di chuyển từ các điểm lối vào chính (như Cổng A - Gate A, Cổng B - Gate B, Khu vực gửi xe - Parking Area, hoặc lối vào trực tiếp) sẽ được phân phối đều (evenly distributed) cho các tuyến đường tương đương dẫn tới điểm đích.
*   **Ý nghĩa:** Giả định này giúp đơn giản hóa bài toán mô phỏng dòng người đi vào trường vào đầu ngày khi không có dữ liệu chi tiết về phương tiện cá nhân hay phương tiện công cộng cụ thể của từng sinh viên.

### 3.3. Quy tắc Đổi Chi phí Di chuyển theo Chiều dọc (Vertical Movement Cost)
Di chuyển giữa các tầng khác nhau trong một tòa nhà tiêu tốn năng lượng và thời gian khác biệt rõ rệt so với di chuyển trên hành lang bằng phẳng. Hệ thống quy đổi chi phí di chuyển thẳng đứng thành khoảng cách đi bộ tương đương (mét):
*   **Di chuyển bằng Cầu thang bộ (Stairs):** Mỗi tầng chênh lệch độ cao ($\Delta z = 1$) sẽ cộng thêm **6 mét** vào tổng chi phí di chuyển ($+6m$ cost). Việc leo cầu thang bộ đòi hỏi nhiều thể lực và tốn nhiều thời gian hơn, do đó chịu mức phạt (penalty) cao gấp đôi so với thang máy.
*   **Di chuyển bằng Thang máy (Elevator):** Mỗi lần sử dụng thang máy để di chuyển giữa các tầng khác nhau (bất kể chênh lệch bao nhiêu tầng) sẽ cộng thêm một mức chi phí cố định là **3 mét** ($+3m$ fixed cost). Mức chi phí cố định này đại diện cho thời gian chờ đợi thang máy mở cửa và thời gian di chuyển trung bình bên trong cabin thang máy.
*   **Bỏ qua các độ cao khác:** Các khoảng chênh lệch độ cao nhỏ ngoài sàn nhà (như bậc tam cấp sảnh, độ dốc nhỏ của lối đi xe lăn...) được coi là không đáng kể và được bỏ qua để đơn giản hóa việc tính toán.

---

## 4. Các Ràng buộc của Hệ thống (Constraints)

Để hệ thống hoạt động chính xác và phản ánh đúng thực tế hình học của trường UIT, dữ liệu và mô hình phải tuân thủ nghiêm ngặt 4 ràng buộc hệ thống cốt lõi sau:

### 4.1. Ràng buộc Toàn vẹn Dữ liệu Không gian học tập
*   **Mô tả:** Mọi mã phòng học xuất hiện trong danh sách thời khóa biểu sinh viên ($D_1$) đều phải được ánh xạ thành công tới một đỉnh phòng học (Room Node) tương ứng trên đồ thị không gian trường học ($D_2$).
*   **Ý nghĩa:** Ràng buộc này đảm bảo tính liên tục của luồng di chuyển. Nếu tồn tại một sự kiện trong $D_1$ diễn ra tại một phòng không có trong đồ thị $D_2$, hệ thống sẽ không thể tính toán được đường đi của sinh viên đến hoặc đi từ phòng đó, gây ra hiện tượng mất mát dữ liệu lưu lượng di chuyển (traffic flow) và dẫn đến sai lệch nghiêm trọng kết quả xếp hạng.

### 4.2. Ràng buộc về Sự Tồn tại của Phòng Ứng viên
*   **Mô tả:** Tất cả các mã phòng ứng viên được đưa vào danh sách đề xuất ($D_3$) bắt buộc phải tồn tại dưới dạng một Đỉnh Phòng học trong cơ sở dữ liệu đồ thị không gian ($D_2$).
*   **Ý nghĩa:** Ràng buộc này ngăn ngừa lỗi tham chiếu. Việc đánh giá một phòng ứng viên đòi hỏi phải truy xuất tọa độ không gian $pos(v)$, các lối đi xung quanh và hành lang kết nối của phòng đó trên đồ thị. Nếu một ứng viên không tồn tại trong $D_2$, hệ thống không thể tính toán các chỉ số Accessibility, Visibility hay Privacy cho ứng viên đó.

### 4.3. Quy chuẩn Hệ Tọa độ Không gian
Hệ tọa độ không gian 2D ($x, y$) được thiết lập dựa trên các quy chuẩn hình học đồng nhất trên toàn khuôn viên UIT:
*   **Điểm gốc tọa độ (Origin):** Điểm gốc $(0, 0)$ được đặt cố định tại tâm hình học của **Tòa nhà A** (Building A) - tòa nhà trung tâm hành chính của UIT.
*   **Đơn vị đo:** 1 đơn vị tọa độ trong mô hình tương đương với **1 mét** trên thực tế. Điều này cho phép tính toán khoảng cách Euclidean trực tiếp giữa các điểm trên bản đồ một cách chính xác theo hệ mét.
*   **Các hướng trục tọa độ:**
    *   **Trục hoành ($x$):** Hướng từ **Tây sang Đông** (phương nằm ngang). Giá trị $x$ dương biểu thị vị trí nằm về phía Đông của Tòa nhà A, giá trị âm nằm về phía Tây.
    *   **Trục tung ($y$):** Hướng từ **Nam lên Bắc** (phương thẳng đứng trên mặt phẳng sàn). Giá trị $y$ dương biểu thị vị trí nằm về phía Bắc của Tòa nhà A, giá trị âm nằm về phía Nam.
*   **Ý nghĩa:** Việc chuẩn hóa hệ tọa độ thống nhất giúp hệ thống dễ dàng thực hiện các phép chiếu, tính toán khoảng cách giữa các tòa nhà khác nhau (như Tòa nhà A, B, C, E) trên cùng một mặt phẳng tham chiếu 2D trước khi kết hợp với thông số tầng $z$.

### 4.4. Giới hạn Ngoại cảnh và Tính Tĩnh của Dữ liệu
*   **Mô tả:** Các yếu tố thời tiết (nắng, mưa, nhiệt độ cao), sự kiện đặc biệt (lễ hội trường, kỳ thi tập trung đột xuất) hoặc các tình huống bất ngờ không được đưa vào làm biến số trong cấu trúc và giá trị của $D_1$ và $D_2$.
*   **Ý nghĩa:** Đồ thị không gian ($D_2$) và thời khóa biểu ($D_1$) được giả định là cố định và mang tính chất tĩnh trong suốt tuần lễ đánh giá tiêu chuẩn. Ràng buộc này giúp mô hình tập trung vào việc tối ưu hóa cấu trúc không gian dài hạn và dòng di chuyển trung bình ổn định của sinh viên, tránh hiện tượng mô hình bị nhiễu bởi các biến động thời gian thực ngắn hạn.

---

## 5. Các Chỉ số Đo lường và Đánh giá (Metrics)

Để đánh giá và so sánh chất lượng của từng vị trí phòng ứng viên tiềm năng một cách khách quan và khoa học, hệ thống sử dụng 5 chỉ số đo lường (Metrics) chuyên biệt, phản ánh cả khía cạnh định lượng, định tính và hiệu năng kỹ thuật:

### 5.1. Tỷ lệ Sử dụng Dịch vụ Tư vấn (Counseling Utilization Rate - CUR)
Chỉ số CUR đo lường mức độ tương tác và tần suất sinh viên tìm đến sử dụng dịch vụ tư vấn tâm lý tại vị trí được đề xuất.
*   **Công thức toán học:**
    $$CUR = \frac{N_{visit}}{N_{student}}$$
*   **Giải thích biến số:**
    *   $N_{visit}$: Tổng số lượt sinh viên tìm đến và sử dụng dịch vụ tư vấn tâm lý trong khoảng thời gian đánh giá.
    *   $N_{student}$: Tổng số lượng sinh viên nằm trong phạm vi đánh giá của hệ thống (tổng quy mô sinh viên tại khu vực được khảo sát).
*   **Ý nghĩa thực tế:** Chỉ số này phản ánh hiệu quả hoạt động tổng thể của phòng tư vấn. Vị trí có CUR càng cao chứng tỏ địa điểm đó thuận tiện cho việc sinh viên ghé thăm thường xuyên.

### 5.2. Tỷ lệ Tiếp cận Sinh viên Độc bản (Unique User Penetration Rate - UPR)
Chỉ số UPR đo lường mức độ bao phủ và lan tỏa của dịch vụ tư vấn tâm lý trong cộng đồng sinh viên, tức là có bao nhiêu cá nhân sinh viên khác nhau được tiếp cận.
*   **Công thức toán học:**
    $$UPR = \frac{N_{unique}}{N_{student}}$$
*   **Giải thích biến số:**
    *   $N_{unique}$: Số lượng sinh viên **khác nhau (độc bản)** đã sử dụng dịch vụ tư vấn tâm lý ít nhất một lần trong thời gian đánh giá.
    *   $N_{student}$: Tổng số sinh viên thuộc phạm vi đánh giá.
*   **Sự khác biệt cốt lõi giữa CUR và UPR:** 
    *   *CUR* đo lường tổng số **lượt (visits)** học sinh sử dụng dịch vụ (một học sinh đi tư vấn 5 lần sẽ đóng góp 5 đơn vị vào $N_{visit}$).
    *   *UPR* chỉ đo lường số **người (unique users)** sử dụng dịch vụ (một học sinh dù đi tư vấn 5 lần cũng chỉ đóng góp 1 đơn vị vào $N_{unique}$).
    *   *Ví dụ minh họa:* Nếu một phòng tư vấn có tổng số lượt thăm là 100 từ duy nhất 10 sinh viên khác nhau trên quy mô 1000 sinh viên. Khi đó $CUR = 100/1000 = 0.1$ (được đánh giá là hoạt động sôi nổi), nhưng $UPR = 10/1000 = 0.01$ (độ phủ rất thấp, dịch vụ chưa lan tỏa rộng rãi). Hệ thống hướng tới việc tối ưu hóa cả hai chỉ số này.

### 5.3. Tỷ lệ Hài lòng về Tính Riêng tư (Privacy Satisfaction Rate - PSR)
Chỉ số PSR đo lường tính bảo mật và sự an tâm của sinh viên khi di chuyển vào phòng tư vấn tâm lý tại vị trí đề xuất.
*   **Công thức toán học:**
    $$PSR = \frac{N_{privacy\_positive}}{N_{survey}}$$
*   **Giải thích biến số:**
    *   $N_{privacy\_positive}$: Số lượng sinh viên đánh giá vị trí của phòng tư vấn là đảm bảo tính riêng tư trong các cuộc khảo sát.
    *   $N_{survey}$: Tổng số phiếu khảo sát hợp lệ thu thập được từ những sinh viên đã trải nghiệm thực tế dịch vụ tư vấn tại địa điểm đó.
*   **Ý nghĩa thực tế:** Do tâm lý e ngại của sinh viên, PSR là chỉ số quyết định sự tồn tại lâu dài của phòng tư vấn. Nếu phòng đặt ở vị trí quá ồn ào hoặc quá lộ thiên, PSR sẽ rất thấp và sinh viên sẽ ngừng sử dụng dịch vụ dù khả năng tiếp cận vật lý của nó rất tốt.

### 5.4. Điểm Đánh giá mức độ Dễ hiểu từ các Bên Liên quan (Stakeholder Interpretation Score - SIS)
Chỉ số SIS đo lường tính giải thích được (Explainability) của mô hình khuyến nghị đối với con người (bao gồm ban giám hiệu nhà trường, các chuyên gia tâm lý và đại diện sinh viên).
*   **Công thức toán học:**
    $$SIS = \frac{Total\_interpretability\_score}{N_{stakeholder}}$$
*   **Giải thích biến số:**
    *   $Total\_interpretability\_score$: Tổng điểm đánh giá độ dễ hiểu từ tất cả các phiếu phỏng vấn các bên liên quan.
    *   $N_{stakeholder}$: Tổng số lượng các bên liên quan tham gia vào quá trình đánh giá.
    *   **Thang đo Likert 5 mức độ:** Điểm số được chấm từ 1 đến 5, trong đó:
        *   `1`: Hoàn toàn mơ hồ, không hiểu lý do tại sao hệ thống đưa ra khuyến nghị này.
        *   `5`: Cực kỳ rõ ràng, dễ hiểu và thuyết phục đối với người sử dụng.
*   **Ý nghĩa thực tế:** Đảm bảo hệ thống AI/Computational Model không phải là một "hộp đen" (black box) mà là một đối tác hỗ trợ ra quyết định minh bạch, tạo dựng niềm tin cho ban quản lý nhà trường khi phê duyệt dự án xây dựng thực tế.

### 5.5. Thời gian Thực thi Hệ thống (Runtime)
Chỉ số Runtime đo lường hiệu năng tính toán của thuật toán xử lý dữ liệu và xếp hạng ứng viên.
*   **Công thức toán học:**
    $$Runtime = T_{finish} - T_{start}$$
*   **Giải thích biến số:**
    *   $T_{start}$: Thời điểm hệ thống bắt đầu nạp và xử lý các tệp dữ liệu đầu vào $D_1, D_2, D_3$.
    *   $T_{finish}$: Thời điểm hệ thống hoàn thành toàn bộ các phép tính toán phức tạp, phân tích trade-off và xuất ra báo cáo khuyến nghị cuối cùng.
    *   **Đơn vị đo:** Giây (Seconds).
*   **Ý nghĩa thực tế:** Đo lường khả năng mở rộng (scalability) của giải pháp thuật toán khi áp dụng cho các đồ thị không gian lớn hơn hoặc lượng thời khóa biểu sinh viên khổng lồ của toàn bộ Đại học Quốc gia.

---

## 6. Các Yêu cầu Phi chức năng (Non-Functional Requirements)

Các yêu cầu phi chức năng (NFRs) đặt ra những tiêu chuẩn chất lượng nghiêm ngặt mà giải pháp đề xuất bắt buộc phải đạt được để đảm bảo tính khả thi khi triển khai trong thực tế tại trường UIT.

### 6.1. Yêu cầu R1: Khả năng Tiếp cận tối ưu (Accessibility Requirement)
*   **Mô tả kỹ thuật:** Tỷ lệ sử dụng dịch vụ tư vấn (CUR) tại địa điểm mới phải tăng trưởng ít nhất **$20\%$** so với phòng tư vấn hiện tại.
*   **Công thức kiểm chứng:**
    $$CUR_{after} \geq 1.2 \times CUR_{before}$$
*   **Mục tiêu:** Đảm bảo phòng mới được đặt tại nơi thuận tiện hơn cho sinh viên, giảm thiểu thời gian di chuyển giữa các tiết học và khuyến khích sinh viên sử dụng dịch vụ nhiều hơn.

### 6.2. Yêu cầu R2: Tính Hiển thị và Nhận diện (Visibility Requirement)
*   **Mô tả kỹ thuật:** Tỷ lệ tiếp cận sinh viên độc bản (UPR) phải tăng trưởng ít nhất **$15\%$** so với phòng cũ.
*   **Công thức kiểm chứng:**
    $$UPR_{after} \geq 1.15 \times UPR_{before}$$
*   **Mục tiêu:** Phòng mới phải nằm ở khu vực dễ nhận biết, giúp tăng độ bao phủ của dịch vụ đến những sinh viên chưa từng sử dụng trước đây, giúp họ dễ dàng định vị phòng tư vấn trong tâm trí.

### 6.3. Yêu cầu R3: Đảm bảo Tính Riêng tư tuyệt đối (Privacy Requirement)
*   **Mô tả kỹ thuật:** Tỷ lệ hài lòng về tính riêng tư (PSR) thu được từ khảo sát thực tế phải đạt tối thiểu **$70\%$**.
*   **Công thức kiểm chứng:**
    $$PSR \geq 70\%$$
*   **Mục tiêu:** Bảo vệ quyền riêng tư và trạng thái tâm lý thoải mái của sinh viên. Tránh việc sinh viên cảm thấy bị e ngại hay kỳ thị khi bước vào phòng tư vấn tâm lý.

### 6.4. Yêu cầu R4: Khả năng Giải thích được (Explainability Requirement)
*   **Mô tả kỹ thuật:** Các bên liên quan phải hiểu và chấp nhận được lập luận khuyến nghị của hệ thống với điểm SIS đạt tối thiểu **$4/5$** điểm.
*   **Công thức kiểm chứng:**
    $$SIS \geq 4/5$$
*   **Mục tiêu:** Hệ thống phải cung cấp báo cáo giải thích chi tiết vì sao một phòng được chọn (ví dụ: điểm mạnh về riêng tư, sự đánh đổi về khoảng cách đi bộ...), giúp ban lãnh đạo trường tự tin đưa ra quyết định đầu tư xây dựng.

### 6.5. Yêu cầu R5: Thời gian Đáp ứng Hệ thống (Runtime Performance)
*   **Mô tả kỹ thuật:** Quá trình tính toán, đánh giá và lập báo cáo xếp hạng cho tất cả các phòng ứng viên phải hoàn thành trong thời gian không quá **2 phút (120 giây)**.
*   **Công thức kiểm chứng:**
    $$Runtime \leq 120s$$
*   **Mục tiêu:** Đảm bảo hiệu năng hệ thống mượt mà, cho phép chạy thử nghiệm nhiều phương án danh sách ứng viên ($D_3$) khác nhau một cách nhanh chóng mà không gây nghẽn hệ thống.

---

### 6.6. Phân tích Mâu thuẫn và Sự Đánh đổi (Trade-off Analysis) giữa các Yêu cầu
Một trong những thách thức kỹ thuật lớn nhất của dự án là sự mâu thuẫn nội tại giữa các yêu cầu phi chức năng:
1.  **Mâu thuẫn giữa Tiếp cận/Hiển thị ($R_1, R_2$) và Riêng tư ($R_3$):** 
    *   Để đạt $R_1$ và $R_2$ cao, phòng tư vấn nên được đặt ở trung tâm, gần các lối đi chính hoặc sảnh lớn nơi có dòng sinh viên di chuyển cực kỳ đông đúc (ví dụ: gần thư viện, sảnh tòa nhà C).
    *   Tuy nhiên, nếu đặt ở khu vực sầm uất như vậy, sinh viên khi bước vào phòng sẽ bị quan sát bởi rất nhiều người qua đường, làm giảm nghiêm trọng tính riêng tư ($R_3$). Sinh viên sẽ có cảm giác e ngại và không muốn sử dụng dịch vụ.
    *   Ngược lại, nếu đặt phòng ở góc khuất, tầng cao vắng vẻ để đạt $R_3$ rất cao, sinh viên lại gặp khó khăn trong việc tìm kiếm, di chuyển xa ($R_1$ giảm) và ít người biết tới phòng ($R_2$ giảm).
2.  **Giải pháp Tối ưu hóa Đa mục tiêu:**
    Hệ thống không thể tối ưu hóa đơn lẻ một chỉ số mà phải tìm ra một tập hợp các giải pháp Pareto tối ưu (Pareto-optimal solutions). Bằng cách chuẩn hóa và sử dụng thuật toán tính điểm vô hướng hóa đa mục tiêu (Mul## 9. Chi tiết Kiến trúc Giải pháp & Các Module Thành phần (Solution & Modules)

Dưới đây là mô tả chi tiết, sâu sắc nhất về toán học, giải thuật, cấu trúc dữ liệu và đặc biệt là chi tiết **Đầu vào (Inputs)** và **Đầu ra (Outputs)** (được mã hóa theo số thứ tự luồng dữ liệu từ **1** đến **22** trong Sơ đồ Luồng Dữ liệu) của từng mô-đun lớn và nhỏ trong Cây Phân rã:

---

### 9.1. MODULE P1: Trích xuất Nhu cầu Di chuyển từ Thời khóa biểu (Extract Movement Demand)
Mô-đun P1 thực hiện nhiệm vụ phân tích lịch học tập thô của sinh viên trường UIT để chuyển đổi thành dữ liệu động về các nhu cầu di chuyển.
*   **Tổng quan Đầu vào của MODULE P1:** 
    *   `[1] D1: Weekly student event list` (Danh sách thời khóa biểu thô của sinh viên).
*   **Tổng quan Đầu ra của MODULE P1:** 
    *   `[4] chronological_events` (Danh sách sự kiện sắp xếp theo trình tự thời gian).
    *   `[5] origin_destination_pairs` (Tập hợp các cặp điểm đi - điểm đến).

#### P1.1: Sắp xếp các sự kiện học tập theo trình tự thời gian
*   **Đầu vào (Inputs):** 
    *   `[1] D1: Weekly student event list` (Dữ liệu thời khóa biểu thô từ phòng đào tạo).
*   **Đầu ra (Outputs):** 
    *   `[4] chronological_events` (Chuỗi sự kiện học tập có thứ tự thời gian tuyến tính của từng lớp học).
*   **Mục tiêu tính toán:** Tổ chức lại dữ liệu thời khóa biểu thô của từng nhóm sinh viên để có thể quét hành trình di chuyển của họ theo dòng thời gian từ sáng đến tối.
*   **Thuật toán & Xử lý chi tiết:**
    1.  *Gom nhóm theo lớp học (Cohort Grouping):* Hệ thống gom nhóm sinh viên thành các lớp sinh hoạt/lớp học phần cố định dựa trên mã lớp học. Mỗi lớp này được coi là một thực thể di chuyển tập thể (cohort) với quy mô sĩ số $N_{cohort}$ xác định.
    2.  *Sắp xếp khóa kép (Double-key Sorting):* Với từng lớp sinh viên, hệ thống tiến hành sắp xếp danh sách các sự kiện học tập của họ bằng thuật toán sắp xếp (ví dụ: Quicksort) với hai khóa sắp xếp:
        *   Khóa 1 (Chính): Ngày trong tuần (`weekday` từ Thứ Hai đến Chủ Nhật).
        *   Khóa 2 (Phụ): Tiết học bắt đầu (`start_period` từ tiết 1 đến tiết 10).
    3.  *Xử lý khoảng trống thời gian (Temporal Gaps):* Nếu giữa hai tiết học có khoảng trống (ví dụ: học tiết 1-2, sau đó nghỉ tiết 3-4, rồi học tiếp tiết 5-6), hệ thống sẽ tính toán khoảng trống thời gian $\Delta t = start\_period_{next} - end\_period_{prev} - 1$.
        *   Nếu $\Delta t \le 1$ tiết: Sinh viên được giả định là ở lại trường và di chuyển đến các khu vực tự học hoặc thư viện (được mô hình hóa bằng các đỉnh Checkpoint trung gian).
        *   Nếu $\Delta t > 1$ tiết: Sinh viên được giả định là rời khỏi khuôn viên trường (di chuyển ra cổng/bãi xe) và quay lại sau đó.

#### P1.3: Trích xuất các cặp phòng di chuyển kế tiếp
*   **Đầu vào (Inputs):** 
    *   `[4] chronological_events` (Thời khóa biểu đã được sắp xếp từ P1.1).
*   **Đầu ra (Outputs):** 
    *   `[5] origin_destination_pairs` (Tập hợp luồng di chuyển O-D kèm sĩ số: $OD\_pairs = \{(Origin, Destination, Student\_Count)\}$).
*   **Mục tiêu tính toán:** Xác định điểm đi và điểm đến cụ thể của từng luồng sinh viên di chuyển giữa các phòng học kế tiếp.
*   **Thuật toán & Xử lý chi tiết:**
    1.  *Cơ chế cửa sổ trượt (Sliding Window):* Chạy cửa sổ kích thước 2 qua danh sách sự kiện đã sắp xếp của từng nhóm lớp học phần.
    2.  *Trích xuất cặp chuyển tiếp:* Đối với mỗi vị trí cửa sổ, hệ thống đọc phòng học hiện tại $Room_{prev}$ và phòng học kế tiếp $Room_{next}$. Nếu chúng nằm trong cùng một ngày, hệ thống tạo ra một cặp Origin-Destination (O-D pair) dạng:
        $$OD = (Room_{prev}, Room_{next}, Sĩ\_số, Weekday, Transition\_Period)$$
    3.  *Trích xuất luồng ra/vào trường:*
        *   Đối với tiết học đầu tiên trong ngày của lớp, hệ thống tạo cặp O-D xuất phát từ một Checkpoint lối vào ngẫu nhiên (Cổng A, Cổng B, hoặc Bãi đỗ xe) đến phòng học đầu tiên: $OD_{entry} = (Checkpoint_{entry}, Room_{first}, Sĩ\_số)$.
        *   Đối với tiết học cuối cùng trong ngày, hệ thống tạo cặp O-D di chuyển từ phòng học cuối cùng ra một Checkpoint lối ra: $OD_{exit} = (Room_{last}, Checkpoint_{exit}, Sĩ\_số)$.

---

### 9.2. MODULE P2: Ước lượng Tuyến đường và Lưu lượng trên Đồ thị (Estimate Routes and Traffic)
Mô-đun P2 ánh xạ các cặp di chuyển O-D lên đồ thị không gian vật lý của UIT và mô phỏng sự phân bổ dòng người.
*   **Tổng quan Đầu vào của MODULE P2:**
    *   `[2] D2: UIT spatial graph` (Đồ thị không gian có trọng số).
    *   `[3] D3: Candidate room list` (Danh sách phòng ứng viên).
    *   `[5] origin_destination_pairs` (Các cặp O-D từ Module P1).
*   **Tổng quan Đầu ra của MODULE P2:**
    *   `[6] shortest_path_routes` (Tập hợp các tuyến đường đi).
    *   `[7] node_traffic` (Mật độ lưu thông trên các đỉnh).
    *   `[8] edge_traffic` (Mật độ lưu thông trên các cạnh).
    *   `[9] access_node_pass_count` (Lưu lượng tại các nút tiếp cận ứng viên).

#### P2.1: Tìm đường đi ngắn nhất bằng thuật toán Dijkstra
*   **Đầu vào (Inputs):** 
    *   `[2] D2: UIT spatial graph` (Đồ thị không gian $G$).
    *   `[5] origin_destination_pairs` (Danh sách các cặp O-D cần mô phỏng).
*   **Đầu ra (Outputs):** 
    *   `[6] shortest_path_routes` (Các chuỗi đỉnh biểu thị các tuyến đường đi tối ưu và tiệm cận tối ưu).
*   **Mục tiêu tính toán:** Tìm kiếm toàn bộ các tuyến đường di chuyển khả thi và tối ưu về mặt hình học cho sinh viên.
*   **Thuật toán & Xử lý chi tiết:**
    1.  *Chạy thuật toán Dijkstra:* Với mỗi cặp $(Origin, Destination)$ trong `[5]`, hệ thống khởi tạo hàng đợi ưu tiên (Min-heap) để thực hiện thuật toán Dijkstra tìm đường đi ngắn nhất với tổng trọng số cạnh nhỏ nhất $C_{min}$.
    2.  *Tìm các đường đi tiệm cận tối ưu (Yen's K-Shortest Paths):* Do giả định sinh viên có thể chọn các đường đi có chi phí không vượt quá $1.15 \times C_{min}$, hệ thống áp dụng biến thể thuật toán Yen hoặc thuật toán duyệt theo chiều sâu (DFS) có nhánh cận để thu thập tập hợp tất cả các đường đi khả thi $\mathcal{P}_{feasible} = \{P_1, P_2, \dots, P_h\}$ thỏa mãn điều kiện:
        $$Cost(P_j) \le 1.15 \times C_{min}$$

#### P2.2 & P2.3: Tính toán lưu lượng trên các đỉnh đồ thị (Node Traffic) và cạnh đồ thị (Edge Traffic)
*   **Đầu vào (Inputs):** 
    *   `[5] origin_destination_pairs` (Sĩ số sinh viên di chuyển).
    *   `[6] shortest_path_routes` (Tập hợp các tuyến đường khả thi tương ứng).
*   **Đầu ra (Outputs):** 
    *   `[7] node_traffic` (Lưu lượng tích lũy của từng nút: $Traffic(v)$).
    *   `[8] edge_traffic` (Lưu lượng tích lũy của từng cạnh: $Traffic(e)$).
*   **Mục tiêu tính toán:** Tính toán mật độ lưu thông tích lũy tại tất cả các điểm và tuyến đường trong khuôn viên UIT.
*   **Thuật toán & Xử lý chi tiết:**
    1.  *Gán xác suất lựa chọn tuyến đường:* Với mỗi cặp O-D có $M$ tuyến đường đi khả thi trong tập `[6]`, hệ thống giả định sinh viên phân bổ đều trên các tuyến này. Xác suất lựa chọn mỗi tuyến đường là $p = 1 / M$.
    2.  *Phân bổ lưu lượng đỉnh (P2.2):* Với mỗi tuyến đường $P_j$ được chọn, lượng sinh viên di chuyển qua tuyến đó là $N_{route} = Sĩ\_số \times (1 / M)$. Hệ thống duyệt qua từng đỉnh $v \in P_j$ và cộng dồn lưu lượng:
        $$Traffic(v) = Traffic(v) + N_{route}$$
    3.  *Phân bổ lưu lượng cạnh (P2.3):* Tương tự, hệ thống duyệt qua từng cạnh nối $e = (u, v) \in P_j$ và cộng dồn lưu lượng trên cạnh:
        $$Traffic(e) = Traffic(e) + N_{route}$$

#### P2.4: Tổng hợp lượt đi qua tại các nút tiếp cận (Access Nodes)
*   **Đầu vào (Inputs):** 
    *   `[3] D3: Candidate room list` (Danh sách phòng ứng viên cần đánh giá).
    *   `[6] shortest_path_routes` (Tuyến đường di chuyển của sinh viên).
    *   `[7] node_traffic` (Bản đồ lưu lượng đỉnh đã tính ở P2.2 - cụ thể là dữ liệu lưu lượng tại các đỉnh tiếp cận).
*   **Đầu ra (Outputs):** 
    *   `[9] access_node_pass_count` (Lưu lượng sinh viên đi qua trước cửa từng phòng ứng viên).
*   **Mục tiêu tính toán:** Xác định lưu lượng sinh viên đi lại trực tiếp trước khu vực cửa phòng ứng viên để làm cơ sở tính toán hiển thị và riêng tư.
*   **Thuật toán & Xử lý chi tiết:**
    1.  Với mỗi phòng ứng viên $r \in `[3]`$, hệ thống truy vấn đỉnh tiếp cận $a_r \in V$ tương ứng của phòng đó. Đỉnh tiếp cận này đại diện cho điểm nút giao thông nằm trên hành lang ngay trước cửa phòng.
    2.  Hệ thống trích xuất giá trị lưu lượng tích lũy tại đỉnh này:
        $$PassByCount(r) = Traffic(a_r)$$

---

### 9.3. MODULE P3: Đánh giá Khả năng Tiếp cận của Ứng viên (Evaluate Accessibility)
Mô-đun P3 đánh giá khoảng cách di chuyển từ các khu vực sinh hoạt chính của sinh viên đến phòng ứng viên.
*   **Tổng quan Đầu vào của MODULE P3:**
    *   `[2] D2: UIT spatial graph` (Thông tin hình học đồ thị).
    *   `[3] D3: Candidate room list` (Danh sách phòng ứng viên).
    *   `[6] shortest_path_routes` (Tuyến đường đi ngắn nhất của sinh viên).
*   **Tổng quan Đầu ra của MODULE P3:**
    *   `[10] distance_matrix` (Ma trận khoảng cách từ các nút cốt lõi).
    *   `[11] weighted_travel_cost` (Chi phí đi lại trung bình).
    *   `[12] accessibility_indicator` (Chỉ số tiếp cận chuẩn hóa $[0, 1]$).

#### P3.1: Đo khoảng cách từ các nút hoạt động cốt lõi đến phòng ứng viên
*   **Đầu vào (Inputs):** 
    *   `[2] D2: UIT spatial graph` (Cấu trúc kết nối đồ thị).
    *   `[3] D3: Candidate room list` (Các phòng ứng viên).
    *   `[6] shortest_path_routes` (Tuyến đường đi ngắn nhất).
*   **Đầu ra (Outputs):** 
    *   `[10] distance_matrix` (Ma trận khoảng cách từ các nút cốt lõi $V_{core}$ đến các phòng ứng viên).
*   **Mục tiêu tính toán:** Xác định khoảng cách hình học thực tế từ các điểm tập trung đông sinh viên đến các phòng ứng viên.
*   **Thuật toán & Xử lý chi tiết:**
    *   Với mỗi phòng ứng viên $r \in `[3]`$, hệ thống chạy thuật toán Dijkstra để tìm khoảng cách ngắn nhất $d(v_c, r)$ từ tất cả các đỉnh cốt lõi $v_c \in V_{core}$ đến phòng $r$. Khoảng cách này đã bao gồm cả các chi phí quy đổi di chuyển chiều dọc (thang bộ +6m/tầng, thang máy +3m cố định).

#### P3.2: Tính toán chi phí đi bộ trung bình của sinh viên
*   **Đầu vào (Inputs):** 
    *   `[6] shortest_path_routes` (Được dùng để lấy tần suất/lưu lượng làm trọng số).
    *   `[10] distance_matrix` (Ma trận khoảng cách đã tính ở P3.1).
*   **Đầu ra (Outputs):** 
    *   `[11] weighted_travel_cost` (Điểm chi phí di chuyển trung bình có trọng số của từng phòng: $WTC(r)$).
*   **Mục tiêu tính toán:** Tính toán chi phí di chuyển trung bình có trọng số đại diện cho nỗ lực đi lại của đại đa số sinh viên.
*   **Thuật toán & Xử lý chi tiết:**
    *   Áp dụng công thức trung bình cộng có trọng số để tính toán weighted travel cost ($WTC$) cho từng ứng viên $r$:
        $$WTC(r) = \frac{\sum_{v_c \in V_{core}} Traffic(v_c) \cdot d(v_c, r)}{\sum_{v_c \in V_{core}} Traffic(v_c)}$$

#### P3.3: Chuẩn hóa chỉ số Accessibility về khoảng $[0, 1]$
*   **Đầu vào (Inputs):** 
    *   `[11] weighted_travel_cost` (Chi phí di chuyển thô $WTC(r)$).
*   **Đầu ra (Outputs):** 
    *   `[12] accessibility_indicator` (Chỉ số tiếp cận chuẩn hóa: $A(r) \in [0, 1]$).
*   **Mục tiêu tính toán:** Chuyển đổi khoảng cách vật lý (mét) về một thang điểm chuẩn hóa từ 0 đến 1, trong đó điểm càng cao thể hiện khoảng cách càng ngắn (dễ tiếp cận).
*   **Thuật toán & Xử lý chi tiết:**
    *   Xác định giá trị lớn nhất $WTC_{max}$ và nhỏ nhất $WTC_{min}$ trong số các phòng ứng viên.
    *   Áp dụng chuẩn hóa Min-Max nghịch đảo:
        $$Accessibility(r) = \begin{cases} 1.0 & \text{nếu } WTC_{max} = WTC_{min} \\ \frac{WTC_{max} - WTC(r)}{WTC_{max} - WTC_{min}} & \text{ngược lại} \end{cases}$$

---

### 9.4. MODULE P4: Đánh giá Tính Hiển thị của Ứng viên (Evaluate Visibility)
Mô-đun P4 tính toán độ hiển thị tự nhiên của phòng ứng viên dựa trên lưu lượng sinh viên đi qua khu vực lân cận hành lang.
*   **Tổng quan Đầu vào của MODULE P4:**
    *   `[2] D2: UIT spatial graph` (Đồ thị không gian).
    *   `[3] D3: Candidate room list` (Danh sách phòng ứng viên).
    *   `[6] shortest_path_routes` (Các tuyến đường đi).
    *   `[7] node_traffic` / `[8] edge_traffic` (Bản đồ lưu lượng đỉnh/cạnh).
    *   `[9] access_node_pass_count` (Lưu lượng nút tiếp cận trước cửa phòng).
*   **Tổng quan Đầu ra của MODULE P4:**
    *   `[13] exposure_zone` (Vùng hiển thị xung quanh phòng).
    *   `[14] pass_by_count` (Lưu lượng hiển thị thô).
    *   `[15] visibility_indicator` (Chỉ số hiển thị chuẩn hóa $[0, 1]$).

#### P4.1: Xác định vùng nhận diện (Exposure Zone) của phòng ứng viên
*   **Đầu vào (Inputs):** 
    *   `[2] D2: UIT spatial graph` (Cấu trúc mạng lưới hành lang).
    *   `[3] D3: Candidate room list` (Phòng ứng viên cần tính vùng hiển thị).
*   **Đầu ra (Outputs):** 
    *   `[13] exposure_zone` (Tập hợp các đỉnh hành lang $EZ(r)$ nằm trong tầm nhìn của phòng $r$).
*   **Mục tiêu tính toán:** Xác định ranh giới không gian mà từ đó sinh viên có thể nhìn thấy phòng tư vấn khi đi bộ dọc theo hành lang.
*   **Thuật toán & Xử lý chi tiết:**
    *   Với mỗi phòng ứng viên $r \in `[3]`$, hệ thống truy cập đỉnh tiếp cận $a_r$.
    *   Vùng nhận diện $EZ(r)$ được định nghĩa là tập hợp các đỉnh hành lang $v_{hall}$ kết nối trực tiếp với $a_r$ mà khoảng cách đi bộ không vượt quá **10 mét** và không bị ngăn cách bởi tường hoặc đổi tầng:
        $$EZ(r) = \{v \in V \mid d(v, a_r) \le 10m \text{ và } z(v) = z(a_r) \text{ và cùng hành lang}\}$$

#### P4.2: Tính toán tần suất đi qua của sinh viên gần phòng
*   **Đầu vào (Inputs):** 
    *   `[6] shortest_path_routes` / `[7] node_traffic` / `[8] edge_traffic` (Lưu lượng giao thông sinh viên trên đồ thị).
    *   `[9] access_node_pass_count` (Lưu lượng đi qua trước cửa phòng).
    *   `[13] exposure_zone` (Vùng hiển thị của phòng).
*   **Đầu ra (Outputs):** 
    *   `[14] pass_by_count` (Tổng số lượt sinh viên đi qua vùng hiển thị: $RawVisibility(r)$).
*   **Mục tiêu tính toán:** Tính tổng lượng sinh viên đi qua vùng hiển thị của phòng, có tính đến sự suy giảm khả năng quan sát theo khoảng cách.
*   **Thuật toán & Xử lý chi tiết:**
    *   Hệ thống tính toán giá trị hiển thị thô bằng cách cộng dồn lưu lượng tại các đỉnh trong `[13]`, kết hợp với một hệ số suy giảm khoảng cách $\lambda(v, r)$ (do sinh viên đứng càng gần cửa phòng thì càng dễ nhận biết biển phòng tư vấn hơn):
        $$RawVisibility(r) = \sum_{v \in EZ(r)} Traffic(v) \cdot \lambda(v, r)$$
        *Trong đó:* Hệ số suy giảm được chọn là $\lambda(v, r) = \frac{1}{1 + 0.1 \cdot d(v, a_r)}$.

#### P4.3: Chuẩn hóa chỉ số Visibility về khoảng $[0, 1]$
*   **Đầu vào (Inputs):** 
    *   `[14] pass_by_count` (Lưu lượng hiển thị thô $RawVisibility(r)$).
*   **Đầu ra (Outputs):** 
    *   `[15] visibility_indicator` (Chỉ số hiển thị chuẩn hóa: $V(r) \in [0, 1]$).
*   **Mục tiêu tính toán:** Ánh xạ lượng hiển thị thô về thang điểm $[0, 1]$, điểm càng cao thể hiện tính hiển thị càng tốt.
*   **Thuật toán & Xử lý chi tiết:**
    *   Áp dụng chuẩn hóa Min-Max thuận:
        $$Visibility(r) = \begin{cases} 1.0 & \text{nếu } RawVisibility_{max} = RawVisibility_{min} \\ \frac{RawVisibility(r) - RawVisibility_{min}}{RawVisibility_{max} - RawVisibility_{min}} & \text{ngược lại} \end{cases}$$

---

### 9.5. MODULE P5: Đánh giá Tính Riêng tư của Ứng viên (Evaluate Privacy)
Mô-đun P5 đánh giá tính bảo mật và sự an toàn tinh thần của sinh viên bằng cách đo lường rủi ro bị quan sát.
*   **Tổng quan Đầu vào của MODULE P5:**
    *   `[2] D2: UIT spatial graph` (Đồ thị hình học).
    *   `[3] D3: Candidate room list` (Danh sách phòng ứng viên).
    *   `[6] shortest_path_routes` (Tuyến đường di chuyển).
    *   `[7] node_traffic` / `[8] edge_traffic` (Bản đồ lưu lượng đỉnh/cạnh).
*   **Tổng quan Đầu ra của MODULE P5:**
    *   `[16] sensitive_zone` (Vùng nhạy cảm sát cửa phòng).
    *   `[17] exposure_risk` (Lưu lượng rủi ro thô).
    *   `[18] privacy_indicator` (Chỉ số riêng tư chuẩn hóa $[0, 1]$).

#### P5.1: Xác định ranh giới vùng nhạy cảm (Sensitive Zone) xung quanh phòng
*   **Đầu vào (Inputs):** 
    *   `[2] D2: UIT spatial graph` (Cấu trúc hình học hành lang trước phòng).
    *   `[3] D3: Candidate room list` (Các phòng ứng viên).
*   **Đầu ra (Outputs):** 
    *   `[16] sensitive_zone` (Tập hợp các đỉnh hành lang hẹp $SZ(r)$ sát cửa phòng).
*   **Mục tiêu tính toán:** Xác định khu vực tiếp cận trực tiếp ngay trước cửa phòng tư vấn, nơi sinh viên dễ cảm thấy bị "nhìn thấy" nhất khi vào/ra phòng.
*   **Thuật toán & Xử lý chi tiết:**
    *   Khác với vùng hiển thị (cần rộng để dễ nhận diện), vùng nhạy cảm $SZ(r)$ được khoanh vùng hẹp hơn rất nhiều. Hệ thống chỉ lấy đỉnh tiếp cận cửa phòng $a_r$ và các đỉnh lân cận hành lang trong bán kính rất ngắn, tối đa **3 mét**:
        $$SZ(r) = \{v \in V \mid d(v, a_r) \le 3m \text{ và } z(v) = z(a_r)\}$$

#### P5.2: Tính toán chỉ số rủi ro bị quan sát (Exposure Risk)
*   **Đầu vào (Inputs):** 
    *   `[6] shortest_path_routes` / `[7] node_traffic` / `[8] edge_traffic` (Lưu lượng giao thông trên đồ thị).
    *   `[16] sensitive_zone` (Vùng nhạy cảm đã xác định ở P5.1).
*   **Đầu ra (Outputs):** 
    *   `[17] exposure_risk` (Chỉ số rủi ro bị quan sát thô: $RawExposureRisk(r)$).
*   **Mục tiêu tính toán:** Tính tổng lượt sinh viên đi lại trực tiếp qua vùng nhạy cảm. Lưu lượng này tỷ lệ thuận với rủi ro bị lộ thông tin cá nhân.
*   **Thuật toán & Xử lý chi tiết:**
    *   Hệ thống tính tổng lưu lượng thô qua các đỉnh trong vùng nhạy cảm:
        $$RawExposureRisk(r) = \sum_{v \in SZ(r)} Traffic(v)$$

#### P5.3: Chuẩn hóa chỉ số Privacy về khoảng $[0, 1]$
*   **Đầu vào (Inputs):** 
    *   `[17] exposure_risk` (Chỉ số rủi ro bị quan sát thô $RawExposureRisk(r)$).
*   **Đầu ra (Outputs):** 
    *   `[18] privacy_indicator` (Chỉ số riêng tư chuẩn hóa: $P(r) \in [0, 1]$).
*   **Mục tiêu tính toán:** Ánh xạ rủi ro về thang điểm riêng tư $[0, 1]$. Rủi ro bị quan sát càng cao thì điểm riêng tư càng thấp (tỷ lệ nghịch).
*   **Thuật toán & Xử lý chi tiết:**
    *   Áp dụng chuẩn hóa Min-Max nghịch đảo:
        $$Privacy(r) = \begin{cases} 1.0 & \text{nếu } RawExposureRisk_{max} = RawExposureRisk_{min} \\ \frac{RawExposureRisk_{max} - RawExposureRisk(r)}{RawExposureRisk_{max} - RawExposureRisk_{min}} & \text{ngược lại} \end{cases}$$

---

### 9.6. MODULE P6: Xếp hạng Ứng viên và Tạo Báo cáo Khuyến nghị (Rank and Report)
Mô-đun P6 đóng vai trò là bộ não phân tích quyết định của toàn bộ hệ thống.
*   **Tổng quan Đầu vào của MODULE P6:**
    *   `[3] D3: Candidate room list` (Danh sách phòng ứng viên).
    *   `[11] weighted_travel_cost` (Chi phí di chuyển trung bình thô).
    *   `[12] accessibility_indicator` (Điểm tiếp cận chuẩn hóa từ P3.3).
    *   `[14] pass_by_count` (Lưu lượng hiển thị thô).
    *   `[15] visibility_indicator` (Điểm hiển thị chuẩn hóa từ P4.3).
    *   `[17] exposure_risk` (Lưu lượng rủi ro thô).
    *   `[18] privacy_indicator` (Điểm riêng tư chuẩn hóa từ P5.3).
*   **Tổng quan Đầu ra của MODULE P6:**
    *   `[19] normalized_score_table` (Bảng điểm vector đồng bộ).
    *   `[20] primary_recommendation` (Mã phòng khuyến nghị tối ưu nhất).
    *   `[21] alternative_rooms` (Danh sách 3 phòng thay thế tốt tiếp theo).
    *   `[22] trade_off_explanation` (Báo cáo đánh đổi chi tiết cho các ứng viên).

#### P6.1: Xác thực và đồng bộ hóa bảng vector điểm số (Score Vector Table)
*   **Đầu vào (Inputs):** 
    *   `[12] accessibility_indicator` (Chỉ số tiếp cận chuẩn hóa $A(r)$).
    *   `[15] visibility_indicator` (Chỉ số hiển thị chuẩn hóa $V(r)$).
    *   `[18] privacy_indicator` (Chỉ số riêng tư chuẩn hóa $P(r)$).
*   **Đầu ra (Outputs):** 
    *   `[19] normalized_score_table` (Ma trận vector điểm số $\mathbf{S}$ đã được làm sạch và xác thực).
*   **Mục tiêu tính toán:** Kiểm tra tính hợp lệ của dữ liệu trước khi thực hiện tối ưu hóa đa mục tiêu.
*   **Thuật toán & Xử lý chi tiết:**
    *   Hệ thống xây dựng ma trận điểm số $\mathbf{S}$ kích thước $k \times 3$.
    *   Quét qua từng phần tử để kiểm tra lỗi giá trị trống (Null/NaN) hoặc giá trị vượt ngoài khoảng $[0, 1]$. Nếu phát hiện lỗi, hệ thống sẽ tự động gán giá trị mặc định dựa trên trung vị (median) của các ứng viên khác và ghi nhận cảnh báo vào log file.

#### P6.2: Tính điểm Scalarization Score đa mục tiêu bằng trọng số
*   **Đầu vào (Inputs):** 
    *   `[3] D3: Candidate room list` (Danh sách ứng viên cần gán mã và tên).
    *   `[19] normalized_score_table` (Bảng vector điểm số $\mathbf{S}$).
*   **Đầu ra (Outputs):** 
    *   `[20] primary_recommendation` (Mã phòng khuyến nghị hàng đầu: $r^*$).
    *   `[21] alternative_rooms` (Danh sách 3 mã phòng thay thế tốt tiếp theo).
*   **Mục tiêu tính toán:** Áp dụng phương pháp vô hướng hóa đa mục tiêu để xếp hạng tuyến tính các phòng ứng viên.
*   **Thuật toán & Xử lý chi tiết:**
    1.  *Tính điểm số cuối cùng (FinalScore) bằng tổ hợp tuyến tính:*
        $$FinalScore(r) = w_A \cdot A(r) + w_V \cdot V(r) + w_P \cdot P(r)$$
    2.  *Bộ trọng số ưu tiên mặc định:*
        *   $w_P = 0.50$: Ưu tiên hàng đầu cho tính riêng tư (50% trọng số), nhằm tối đa hóa sự an tâm cho sinh viên sử dụng dịch vụ.
        *   $w_A = 0.35$: Ưu tiên tiếp theo cho khả năng tiếp cận (35% trọng số), đảm bảo sinh viên không phải di chuyển quá xa.
        *   $w_V = 0.15$: Trọng số thấp nhất dành cho tính hiển thị (15% trọng số), chỉ cần ở mức vừa đủ để sinh viên nhận biết được phòng.
    3.  *Sắp xếp xếp hạng:* Sắp xếp danh sách ứng viên theo thứ tự giảm dần của $FinalScore(r)$ bằng thuật toán sắp xếp (ví dụ: Timsort).

#### P6.3: Phân tích sự đánh đổi và xuất báo cáo Trade-off
*   **Đầu vào (Inputs):** 
    *   `[11] weighted_travel_cost` (Dữ liệu khoảng cách/chi phí thô để thuyết minh số mét đi lại).
    *   `[14] pass_by_count` (Lưu lượng hiển thị thô để thuyết minh lượng sinh viên qua lại).
    *   `[17] exposure_risk` (Chỉ số rủi ro thô để phân tích lý do rủi ro riêng tư).
*   **Đầu ra (Outputs):** 
    *   `[22] trade_off_explanation` (Bản thuyết minh định tính dạng văn bản Rule-based Trade-off Report).
*   **Mục tiêu tính toán:** Tạo lập lập luận giải thích chi tiết, minh bạch lý do lựa chọn của hệ thống dưới dạng ngôn ngữ tự nhiên để con người có thể dễ dàng hiểu và đánh giá (thỏa mãn SIS).
*   **Thuật toán & Xử lý chi tiết:**
    *   Hệ thống chạy một động cơ luật dựa trên các ngưỡng (threshold-based rules):
        *   *Luật 1 (Cảnh báo riêng tư yếu):* Nếu $P(r) < 0.3$, hệ thống tự động chèn khuyến nghị: *"Mật độ giao thông trước phòng rất lớn. Yêu cầu lắp đặt thêm vách cách âm, rèm cửa che tầm nhìn và biển báo hạn chế tụ tập trước cửa nếu lựa chọn vị trí này."*
        *   *Luật 2 (Cảnh báo khoảng cách xa):* Nếu $A(r) < 0.3$, hệ thống chèn khuyến nghị: *"Vị trí cách xa giảng đường chính. Cần thiết lập sơ đồ hướng dẫn tại sảnh chính các tòa nhà để sinh viên dễ dàng định vị lối đi."*
        *   *Luật 3 (Vị trí tối ưu hài hòa):* Nếu tất cả các chỉ số đều nằm trong khoảng $[0.5, 0.8]$, hệ thống nhận định: *"Đây là vị trí cân bằng rất tốt, đáp ứng hài hòa cả 3 tiêu chí tiếp cận, riêng tư và nhận diện tự nhiên."*�a Ứng viên (Evaluate Accessibility)

---

## 10. Chi tiết Luồng Dữ liệu (Data Flow Diagram)

Hệ thống vận hành dựa trên các luồng truyền dẫn thông tin chặt chẽ giữa các khối chức năng. Bảng dưới đây liệt kê và giải nghĩa toàn bộ 22 thành phần dữ liệu di chuyển trong hệ thống (như được thể hiện trong Decomposition Tree và sơ đồ thiết kế):

| Ký hiệu | Tên Thành phần Dữ liệu | Loại dữ liệu | Mô tả chi tiết |
| :--- | :--- | :--- | :--- |
| **1** | D1: Weekly student event list | Dữ liệu thô đầu vào | Danh sách thời khóa biểu sinh viên dạng bảng (CSV hoặc JSON) gồm mã lớp, phòng học, tiết học. |
| **2** | D2: UIT spatial graph: G = (V, E) | Dữ liệu cấu trúc đồ thị | Đồ thị mạng lưới giao thông nội bộ trường UIT với đầy đủ tọa độ 3D và trọng số cạnh. |
| **3** | D3: Candidate room list | Danh sách ứng viên | Tập hợp danh sách các mã phòng khả thi được đề xuất đặt làm phòng tư vấn tâm lý. |
| **4** | chronological_events | Dữ liệu trung gian | Danh sách thời khóa biểu của từng nhóm sinh viên đã được sắp xếp tăng dần theo mốc thời gian. |
| **5** | origin_destination_pairs | Dữ liệu trung gian | Tập hợp các cặp di chuyển (Phòng xuất phát - Phòng đích) kèm số lượng sinh viên tương ứng. |
| **6** | shortest_path_routes | Dữ liệu tuyến đường | Tập hợp các chuỗi đỉnh biểu thị các đường đi ngắn nhất (và đường đi tiệm cận ngắn nhất) giữa các cặp O-D. |
| **7** | node_traffic | Bản đồ lưu lượng đỉnh | Mật độ sinh viên đi qua từng đỉnh trên đồ thị trong suốt tuần lễ mô phỏng. |
| **8** | edge_traffic | Bản đồ lưu lượng cạnh | Mật độ sinh viên di chuyển qua từng đoạn đường/cạnh hành lang trên đồ thị. |
| **9** | access_node_pass_count | Chỉ số thô | Số lượt sinh viên đi ngang qua đỉnh tiếp cận trực tiếp trước cửa phòng ứng viên. |
| **10** | distance_matrix | Ma trận khoảng cách | Bảng khoảng cách đi lại ngắn nhất từ các nút cốt lõi (Core Activity Nodes) đến các phòng ứng viên. |
| **11** | weighted_travel_cost | Chi phí di chuyển thô | Tổng chi phí đi bộ trung bình có trọng số của sinh viên đến từng phòng ứng viên. |
| **12** | accessibility_indicator | Chỉ số tiếp cận chuẩn hóa | Điểm số chuẩn hóa trong khoảng $[0, 1]$ thể hiện khả năng tiếp cận vật lý của từng ứng viên. |
| **13** | exposure_zone | Vùng hiển thị | Tập hợp các đỉnh không gian nằm trong tầm quan sát trực quan của từng phòng ứng viên. |
| **14** | pass_by_count | Lượng đi qua vùng hiển thị | Tổng số lượt sinh viên di chuyển qua vùng hiển thị của phòng ứng viên. |
| **15** | visibility_indicator | Chỉ số hiển thị chuẩn hóa | Điểm số chuẩn hóa trong khoảng $[0, 1]$ thể hiện độ nhận diện tự nhiên của phòng ứng viên. |
| **16** | sensitive_zone | Vùng nhạy cảm | Tập hợp các đỉnh không gian xung quanh lối ra/vào phòng ứng viên có rủi ro bị quan sát cao. |
| **17** | exposure_risk | Chỉ số rủi ro thô | Tổng số lượt người đi qua vùng nhạy cảm của phòng ứng viên. |
| **18** | privacy_indicator | Chỉ số riêng tư chuẩn hóa | Điểm số chuẩn hóa trong khoảng $[0, 1]$ thể hiện mức độ an tâm bảo mật của phòng ứng viên. |
| **19** | normalized_score_table | Bảng vector điểm số | Bảng dữ liệu đồng bộ chứa các bộ ba giá trị chuẩn hóa $[A, V, P]$ của mọi phòng ứng viên. |
| **20** | primary_recommendation | Đề xuất tối ưu | Mã phòng học được hệ thống đánh giá là tối ưu nhất cho phòng tư vấn. |
| **21** | alternative_rooms | Danh sách thay thế | Danh sách tối đa 3 phòng thay thế tốt tiếp theo kèm điểm số xếp hạng tương ứng. |
| **22** | trade_off_explanation | Báo cáo đánh đổi | Các đoạn văn bản phân tích định tính về ưu/nhược điểm cụ thể của từng phòng ứng viên. |

---

## 11. Chi tiết Thu thập và Xử lý Dữ liệu Kiểm chứng (Evaluation Data)

Để đảm bảo các yêu cầu phi chức năng ($R_1$ đến $R_5$) thực sự được thỏa mãn trong thế giới thực sau khi phòng tư vấn đi vào hoạt động, dự án đề xuất một quy trình thu thập dữ liệu kiểm chứng và xử lý hậu nghiệm (post-processing) chặt chẽ:

### 11.1. Chiến lược thu thập dữ liệu cho Chỉ số Riêng tư (PSR)
*   **Phương pháp thu thập:** Thiết lập một hệ thống khảo sát tự động (Digital Survey) tích hợp qua mã QR dán trong phòng tư vấn tâm lý. Sinh viên sau khi hoàn thành buổi tham vấn sẽ được khuyến khích quét mã QR và trả lời một bộ câu hỏi ẩn danh ngắn.
*   **Câu hỏi cốt lõi đo lường PSR:** "Bạn có cảm thấy vị trí của phòng tư vấn này đủ riêng tư và kín đáo, không gây cảm giác e ngại cho bạn khi bước vào/ra hay không?" (Lựa chọn trả lời: Có / Không).
*   **Xử lý dữ liệu:** Chỉ thu thập các phiếu khảo sát hợp lệ từ những người đã thực sự sử dụng dịch vụ. Loại bỏ các khảo sát rác bằng cách giới hạn mã khảo sát một lần (one-time token) do chuyên viên tư vấn cung cấp sau mỗi ca. PSR được tính bằng tỷ lệ số phiếu đánh giá "Có" trên tổng số phiếu.

### 11.2. Chiến lược thu thập dữ liệu cho Tỷ lệ Sử dụng (CUR) và Tỷ lệ Tiếp cận (UPR)
Đây là hai chỉ số định lượng quan trọng cần kiểm chứng so sánh trước và sau khi đổi địa điểm (Before - After Study):
1.  **Thu thập dữ liệu "Trước khi đổi" ($CUR_{before}, UPR_{before}$):**
    *   Hệ thống xuất dữ liệu từ nhật ký điện tử ra vào phòng tư vấn (entrance logs/check-in logs) của học kỳ 1 năm học trước tại vị trí phòng tư vấn cũ.
    *   Xác định tổng số lượt thăm khám ($N_{visit\_before}$) và số lượng sinh viên độc bản đã đăng ký tham vấn ($N_{unique\_before}$).
2.  **Thu thập dữ liệu "Sau khi đổi" ($CUR_{after}, UPR_{after}$):**
    *   Sau khi phòng tư vấn được xây dựng và vận hành tại vị trí mới được đề xuất, hệ thống tiếp tục xuất dữ liệu check-in logs của học kỳ 1 năm học này.
    *   Xác định tổng số lượt thăm khám ($N_{visit\_after}$) và số lượng sinh viên độc bản tương ứng ($N_{unique\_after}$).
3.  **Kiểm soát các biến số gây nhiễu (Confounding Variables Control):**
    *   *Nhiễu do Truyền thông & Giáo dục:* Nếu trong năm học mới nhà trường đẩy mạnh các chiến dịch truyền thông về sức khỏe tinh thần hoặc tuyển thêm chuyên gia tâm lý nổi tiếng, lượng sinh viên đi tư vấn chắc chắn sẽ tăng lên một cách tự nhiên mà không phụ thuộc vào vị trí phòng.
    *   *Giải pháp hiệu chỉnh:* Tiến hành khảo sát bổ sung về lý do sinh viên biết đến phòng tư vấn. Nếu sinh viên trả lời là do "đi qua thấy" hoặc "thuận tiện đường đi", lượt visit đó sẽ được tính đầy đủ vào mô hình đánh giá vị trí. Đồng thời thực hiện hiệu chỉnh toán học bằng cách chia tỷ lệ tăng trưởng chung của toàn bộ dịch vụ hỗ trợ sinh viên để loại bỏ xu hướng tăng trưởng tự nhiên do yếu tố phi không gian.
    *   *Điều chỉnh quy mô sinh viên:* Chuẩn hóa mẫu số $N_{student}$ tương ứng với tổng số sinh viên đăng ký học tập tại UIT trong học kỳ khảo sát của từng năm học để tránh sai số do số lượng sinh viên toàn trường tăng hoặc giảm.

### 11.3. Chiến lược thu thập dữ liệu cho Chỉ số Giải thích được (SIS)
*   **Phương pháp thu thập:** Tiến hành phỏng vấn trực tiếp kết hợp bảng câu hỏi Likert đối với ban quản lý dự án, các chuyên viên tâm lý và đại diện hội sinh viên UIT ($N_{stakeholder}$).
*   **Cách thức đánh giá:**
    *   Trình bày bản báo cáo đánh đổi (Rule-based Trade-off Report) do hệ thống tự động sinh ra cho các stakeholders đọc.
    *   Yêu cầu stakeholders đánh giá độ rõ ràng và tính thuyết phục của các lập luận theo thang Likert từ 1 đến 5.
    *   SIS được tính bằng điểm trung bình cộng của toàn bộ đánh giá. Để đạt yêu cầu $R_4$, điểm trung bình này phải lớn hơn hoặc bằng 4.0.

---

## 12. Đạo đức và Tác động Xã hội (Ethic & Social Impacts)

Sức khỏe tinh thần và tâm lý là những chủ đề cực kỳ nhạy cảm và mang tính riêng tư cao đối với mỗi cá nhân sinh viên. Do đó, dự án thiết lập và tuân thủ nghiêm ngặt 6 nguyên tắc đạo đức sau đây trong toàn bộ quá trình thiết kế, lập trình và vận hành hệ thống:

### 12.1. Không suy luận trạng thái sức khỏe tinh thần cá nhân
*   **Mô tả:** Hệ thống tuyệt đối không thực hiện bất kỳ phép phân tích hay suy luận nào nhằm chẩn đoán, đoán trước, hoặc phân loại tình trạng sức khỏe tâm thần của từng sinh viên cụ thể.
*   **Ý nghĩa:** Tránh việc hệ thống tự động gắn nhãn (labeling) sinh viên có xu hướng trầm cảm, lo âu hay gặp khủng hoảng tâm lý. Bài toán chỉ tập trung giải quyết khía cạnh tối ưu hóa vị trí vật lý dựa trên lưu lượng di chuyển tổng thể.

### 12.2. Ẩn danh hóa dữ liệu sinh viên (Student Data Anonymization)
*   **Mô tả:** Toàn bộ dữ liệu thời khóa biểu ($D_1$) được thu thập và tiền xử lý đều được lược bỏ hoàn toàn các thông tin nhận dạng cá nhân như: Họ tên sinh viên, Mã số sinh viên (MSSV), Số điện thoại, Email.
*   **Ý nghĩa:** Sinh viên chỉ tồn tại dưới dạng một đơn vị số lượng trong dòng lưu lượng (ví dụ: "lớp $X$ có 40 sinh viên di chuyển từ phòng C103 sang phòng E202"). Ràng buộc này loại bỏ hoàn toàn khả năng truy vết ngược lại lịch trình di chuyển cá nhân của bất kỳ sinh viên nào, đảm bảo quyền riêng tư tối đa.

### 12.3. Không sử dụng giám sát và theo dõi thời gian thực (No Real-time Tracking)
*   **Mô tả:** Hệ thống hoàn toàn không kết nối hay sử dụng dữ liệu từ camera an ninh, thiết bị quét thẻ sinh viên thời gian thực, định vị GPS, hay lịch sử kết nối Wi-Fi nội khu trường UIT.
*   **Ý nghĩa:** Toàn bộ dòng di chuyển được xây dựng dưới dạng mô phỏng danh nghĩa dựa trên lịch trình thời khóa biểu cố định. Điều này loại bỏ hoàn toàn cảm giác bị giám sát liên tục (surveillance) của sinh viên khi di chuyển trong khuôn viên trường.

### 12.4. Không dán nhãn các khu vực hoặc nhóm sinh viên nhạy cảm
*   **Mô tả:** Hệ thống không thực hiện các phép phân tích thống kê phân biệt như so sánh tần suất sử dụng phòng tư vấn giữa các khoa khác nhau (ví dụ: Khoa Khoa học Máy tính vs. Khoa Kỹ thuật Máy tính), hoặc dán nhãn các khu vực vắng vẻ là "khu vực nhạy cảm cần né tránh".
*   **Ý nghĩa:** Tránh việc tạo ra các định kiến xã hội (bias/stigmatization) vô căn cứ đối với một nhóm sinh viên hoặc một khu vực địa lý cụ thể trong trường.

### 12.5. Giải thích cẩn trọng các chỉ số đo lường thực tế
*   **Mô tả:** Các chỉ số đo lường trong mô phỏng (như $A, V, P$) chỉ là các mô hình xấp xỉ toán học được xây dựng trên các giả định. Chúng không phản ánh chính xác $100\%$ hành vi thực tế của con người hay chất lượng tư vấn thực chất của căn phòng.
*   **Ý nghĩa:** Đội ngũ phát triển và ban giám hiệu nhà trường cần nhận thức rõ các giới hạn sai số của mô hình (ví dụ: thời khóa biểu danh nghĩa khác với sự có mặt thực tế lớp học) để tránh việc thần thánh hóa các chỉ số kỹ thuật hoặc diễn giải sai lệch kết quả kiểm chứng.

### 12.6. Hệ thống chỉ hỗ trợ ra quyết định, không thay thế phán đoán con người
*   **Mô tả:** Kết quả đầu ra của thuật toán (Primary Recommendation và Alternatives) chỉ mang tính chất tham khảo chuyên môn kỹ thuật. Quyết định phê duyệt cuối cùng về việc đặt phòng tư vấn tâm lý ở đâu phải do Hội đồng Ban giám hiệu nhà trường đưa ra, dựa trên việc đánh giá toàn diện các yếu tố thực tế khác (như ngân sách, quy chuẩn phòng cháy chữa cháy, tính thẩm mỹ, hệ thống cách âm và ý kiến trực tiếp của các chuyên gia tâm lý học).
*   **Ý nghĩa:** Đảm bảo con người luôn nắm quyền kiểm soát cuối cùng (human-in-the-loop) đối với các quyết định tác động trực tiếp đến đời sống học đường và phúc lợi sinh viên.

---

## 13. Khác (Others - Demo & Links)

Để minh họa trực quan giải pháp và mã nguồn của dự án, nhóm thực hiện cung cấp các liên kết tài nguyên sau:

*   **Mã nguồn chương trình (GitHub):** [UIT CS117 Psychological Counseling Room Ranking System](https://github.com/uit-cs117-counseling-ranking)  
    *Mã nguồn bao gồm: Khối trích xuất thời khóa biểu P1, Thuật toán Dijkstra tìm đường đi ngắn nhất P2, Khối chuẩn hóa điểm số P3-P5 và thuật toán tối ưu đa mục tiêu P6.*
*   **Video Demo minh họa:** [YouTube Link - Video Demo Giải pháp Đánh giá Vị trí Phòng tư vấn UIT](https://youtube.com/uit-counseling-room-location-evaluation)  
    *Video dài 5 phút thuyết minh về Decomposition Tree, giải thích chi tiết luồng di chuyển của sinh viên UIT mô phỏng trên đồ thị không gian 3D và trực quan hóa kết quả xếp hạng các phòng ứng viên.*





