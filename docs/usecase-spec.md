
# Use Case Specification – Smart CRM Mekong Mobile

**Sinh viên:** Nguyễn Minh Trị
**MSSV:** 2374802010517
**Track:** SE
**Luồng nghiệp vụ:** L4 – Phân công kỹ thuật viên và lịch hẹn

---

## 1. Tổng quan

Tài liệu mô tả các Use Case thuộc luồng L4 của Smart CRM – Mekong Mobile, bao gồm xem phiếu chờ phân công, xem kỹ thuật viên khả dụng, phân công hoặc thay đổi kỹ thuật viên, đặt lịch giao – nhận máy và xem công việc được giao.

### 1.1. Actors

| Actor | Vai trò |
|---|---|
| Quản lý trung tâm | Thực hiện phân công, thay đổi kỹ thuật viên và quản lý lịch hẹn |
| Kỹ thuật viên | Xem phiếu và lịch hẹn được giao |

### 1.2. Danh sách Use Case

| ID | Tên Use Case | User Story | FR |
|---|---|---|---|
| UC1 | Xem phiếu cần phân công | US1 | FR1 |
| UC2 | Xem kỹ thuật viên khả dụng | US2 | FR2 |
| UC3 | Phân công kỹ thuật viên | US3 | FR3 |
| UC4 | Thay đổi kỹ thuật viên phụ trách | US4 | FR4 |
| UC5 | Đặt lịch giao – nhận máy | US5 | FR5 |
| UC6 | Xem công việc và lịch hẹn được giao | US6 | FR6 |
| UC7 | Kiểm tra điều kiện phân công | US3 | FR7 |
| UC8 | Kiểm tra trùng lịch | US5 | FR8 |

UC7 được UC3 sử dụng thông qua quan hệ `<<include>>`. UC8 được UC5 sử dụng thông qua quan hệ `<<include>>`.

---

## 2. UC1 – Xem phiếu cần phân công

### 2.1. Thông tin chung

| Thuộc tính | Nội dung |
|---|---|
| Use Case ID | UC1 |
| Primary Actor | Quản lý trung tâm |
| Goal | Xem danh sách phiếu đang chờ phân công |
| Related User Story | US1 – MUST |
| Related FR | FR1 |
| Precondition | Quản lý trung tâm đang sử dụng hệ thống |
| Postcondition | Danh sách phiếu cần phân công được hiển thị; dữ liệu không thay đổi |

### 2.2. Main Flow

1. Quản lý trung tâm chọn chức năng xem phiếu cần phân công.
2. Hệ thống truy xuất các phiếu có trạng thái PENDING.
3. Hệ thống hiển thị danh sách phiếu với mã phiếu, tiêu đề, mức ưu tiên, trạng thái và trung tâm.
4. Quản lý trung tâm xem và lựa chọn phiếu cần xử lý.

### 2.3. Alternative/Exception Flow

**A1 – Không có phiếu chờ phân công**

- Tại bước 2, nếu không có phiếu phù hợp, hệ thống hiển thị danh sách trống và thông báo không có phiếu cần phân công.

**E1 – Không thể tải danh sách**

- Nếu xảy ra lỗi truy xuất dữ liệu, hệ thống thông báo không thể tải danh sách và không hiển thị thông tin sai lệch.

---

## 3. UC2 – Xem kỹ thuật viên khả dụng

### 3.1. Thông tin chung

| Thuộc tính | Nội dung |
|---|---|
| Use Case ID | UC2 |
| Primary Actor | Quản lý trung tâm |
| Goal | Xem các kỹ thuật viên khả dụng để lựa chọn người phù hợp |
| Related User Story | US2 – MUST |
| Related FR | FR2 |
| Precondition | Phiếu cần phân công đã được lựa chọn |
| Postcondition | Danh sách kỹ thuật viên khả dụng được hiển thị; dữ liệu không thay đổi |

### 3.2. Main Flow

1. Quản lý trung tâm chọn một phiếu cần phân công.
2. Quản lý yêu cầu xem kỹ thuật viên khả dụng.
3. Hệ thống xác định các kỹ thuật viên có trạng thái AVAILABLE.
4. Hệ thống hiển thị thông tin kỹ năng, khu vực, khối lượng công việc và trạng thái khả dụng.
5. Quản lý xem danh sách và lựa chọn kỹ thuật viên để xem xét phân công.

### 3.3. Alternative/Exception Flow

**A1 – Không có kỹ thuật viên khả dụng**

- Nếu không có kỹ thuật viên AVAILABLE, hệ thống hiển thị thông báo chưa có kỹ thuật viên khả dụng.

**E1 – Không thể tải dữ liệu**

- Nếu xảy ra lỗi truy xuất dữ liệu kỹ thuật viên, hệ thống thông báo lỗi và cho phép thực hiện lại thao tác.

**Ghi chú:** Trạng thái AVAILABLE chỉ là một điều kiện ban đầu. Điều kiện kỹ năng, trung tâm và trạng thái phiếu phải được kiểm tra trước khi xác nhận phân công theo UC7.

---

## 4. UC3 – Phân công kỹ thuật viên

### 4.1. Thông tin chung

| Thuộc tính | Nội dung |
|---|---|
| Use Case ID | UC3 |
| Primary Actor | Quản lý trung tâm |
| Goal | Phân công một kỹ thuật viên đủ điều kiện cho phiếu |
| Related User Story | US3 – MUST |
| Related FR | FR3 |
| Included Use Case | UC7 – Kiểm tra điều kiện phân công |
| Precondition | Phiếu tồn tại, có trạng thái PENDING và chưa có phân công đang hoạt động |
| Postcondition | Một bản ghi phân công hợp lệ được tạo và xác định kỹ thuật viên phụ trách phiếu |

### 4.2. Main Flow

1. Quản lý trung tâm mở danh sách phiếu cần phân công.
2. Quản lý chọn một phiếu có trạng thái PENDING.
3. Hệ thống hiển thị danh sách kỹ thuật viên khả dụng.
4. Quản lý chọn một kỹ thuật viên.
5. Hệ thống thực hiện UC7 – Kiểm tra điều kiện phân công.
6. Nếu các điều kiện hợp lệ, hệ thống cho phép tiếp tục.
7. Quản lý xác nhận phân công.
8. Hệ thống kiểm tra lại các điều kiện có thể thay đổi trước khi ghi nhận.
9. Hệ thống tạo bản ghi phân công, bảo đảm một phiếu không có hai phân công đang hoạt động.
10. Hệ thống thông báo phân công thành công.

### 4.3. Alternative/Exception Flow

**E1 – Kỹ thuật viên không đủ điều kiện**

- Tại bước 5, nếu kỹ thuật viên không AVAILABLE, proficiency dưới 3 hoặc không cùng trung tâm, hệ thống từ chối và thông báo lý do.
- Quản lý quay lại bước 4 để chọn kỹ thuật viên khác.

**E2 – Phiếu không hợp lệ**

- Nếu phiếu không còn PENDING hoặc đã có phân công đang hoạt động, hệ thống từ chối tạo phân công mới.

**E3 – Điều kiện thay đổi khi xác nhận**

- Tại bước 8, nếu kỹ thuật viên không còn khả dụng hoặc điều kiện phiếu thay đổi, hệ thống không ghi nhận phân công và yêu cầu quản lý kiểm tra lại.

**E4 – Lỗi ghi dữ liệu**

- Nếu không thể lưu bản ghi phân công, hệ thống thông báo thất bại và không xác nhận phân công thành công.

---

## 5. UC4 – Thay đổi kỹ thuật viên phụ trách

### 5.1. Thông tin chung

| Thuộc tính | Nội dung |
|---|---|
| Use Case ID | UC4 |
| Primary Actor | Quản lý trung tâm |
| Goal | Thay đổi kỹ thuật viên phụ trách và lưu lý do |
| Related User Story | US4 – SHOULD |
| Related FR | FR4 |
| Precondition | Phiếu có kỹ thuật viên đang phụ trách |
| Postcondition | Kỹ thuật viên phụ trách được thay đổi hợp lệ; lý do được ghi nhận |

### 5.2. Main Flow

1. Quản lý trung tâm mở phiếu đã có kỹ thuật viên phụ trách.
2. Quản lý chọn chức năng thay đổi kỹ thuật viên.
3. Hệ thống hiển thị kỹ thuật viên hiện tại và danh sách kỹ thuật viên có thể thay thế.
4. Quản lý chọn kỹ thuật viên mới.
5. Quản lý nhập lý do thay đổi.
6. Hệ thống kiểm tra điều kiện của kỹ thuật viên mới theo BR2 và bảo đảm lý do không để trống.
7. Quản lý xác nhận thay đổi.
8. Hệ thống kết thúc phân công cũ và ghi nhận phân công mới, bảo đảm không có hai phân công đang hoạt động đồng thời.
9. Hệ thống lưu lý do thay đổi và thông báo thành công.

### 5.3. Alternative/Exception Flow

**E1 – Không nhập lý do**

- Tại bước 6, nếu lý do để trống, hệ thống yêu cầu nhập lý do trước khi tiếp tục.

**E2 – Kỹ thuật viên mới không đủ điều kiện**

- Nếu kỹ thuật viên không AVAILABLE, proficiency dưới 3 hoặc không cùng trung tâm, hệ thống từ chối thay đổi và thông báo lý do.

**E3 – Lỗi cập nhật phân công**

- Nếu thao tác cập nhật thất bại, hệ thống không xác nhận thay đổi thành công và phải bảo toàn phân công hợp lệ trước đó.

**Ghi chú:** UC4 kiểm tra điều kiện kỹ thuật viên mới theo BR2 bằng quy trình riêng, không bao gồm UC7 vì UC7 chỉ áp dụng cho phân công mới đối với phiếu PENDING chưa có phân công đang hoạt động.

---

## 6. UC5 – Đặt lịch giao – nhận máy

### 6.1. Thông tin chung

| Thuộc tính | Nội dung |
|---|---|
| Use Case ID | UC5 |
| Primary Actor | Quản lý trung tâm |
| Goal | Tạo lịch giao hoặc nhận máy hợp lệ cho phiếu |
| Related User Story | US5 – SHOULD |
| Related FR | FR5 |
| Included Use Case | UC8 – Kiểm tra trùng lịch |
| Precondition | Phiếu cần đặt lịch tồn tại trong hệ thống |
| Postcondition | Lịch hẹn hợp lệ được ghi nhận cho phiếu |

### 6.2. Main Flow

1. Quản lý trung tâm chọn phiếu cần đặt lịch.
2. Quản lý chọn chức năng đặt lịch giao – nhận máy.
3. Quản lý nhập loại lịch hẹn, thời gian bắt đầu và thời gian kết thúc.
4. Hệ thống kiểm tra tính hợp lệ của thông tin nhập.
5. Hệ thống thực hiện UC8 – Kiểm tra trùng lịch.
6. Nếu không có xung đột, hệ thống cho phép tiếp tục.
7. Quản lý xác nhận đặt lịch.
8. Hệ thống kiểm tra lại xung đột trước khi ghi nhận.
9. Hệ thống lưu lịch hẹn cho phiếu.
10. Hệ thống thông báo đặt lịch thành công.

### 6.3. Alternative/Exception Flow

**E1 – Thông tin thời gian không hợp lệ**

- Nếu thiếu thời gian hoặc thời gian kết thúc không sau thời gian bắt đầu, hệ thống yêu cầu chỉnh sửa.

**E2 – Trùng lịch hẹn**

- Nếu UC8 phát hiện xung đột, hệ thống từ chối xác nhận và thông báo để quản lý chọn thời gian khác.

**E3 – Lịch thay đổi khi xác nhận**

- Nếu tại bước 8 xuất hiện lịch hẹn mới gây xung đột, hệ thống không lưu lịch và yêu cầu kiểm tra lại.

**E4 – Lỗi lưu lịch hẹn**

- Nếu không thể lưu lịch hẹn, hệ thống thông báo thất bại.

---

## 7. UC6 – Xem công việc và lịch hẹn được giao

### 7.1. Thông tin chung

| Thuộc tính | Nội dung |
|---|---|
| Use Case ID | UC6 |
| Primary Actor | Kỹ thuật viên |
| Goal | Theo dõi phiếu và lịch hẹn được giao |
| Related User Story | US6 – COULD |
| Related FR | FR6 |
| Precondition | Hệ thống xác định được kỹ thuật viên cần xem dữ liệu |
| Postcondition | Danh sách công việc và lịch hẹn được hiển thị; dữ liệu không thay đổi |

### 7.2. Main Flow

1. Kỹ thuật viên truy cập chức năng xem công việc được giao.
2. Hệ thống xác định mã kỹ thuật viên tương ứng.
3. Hệ thống truy xuất các phiếu đang được phân công cho kỹ thuật viên.
4. Hệ thống truy xuất các lịch hẹn liên quan đến công việc được giao.
5. Hệ thống hiển thị danh sách phiếu và lịch hẹn để kỹ thuật viên theo dõi.

### 7.3. Alternative/Exception Flow

**A1 – Chưa có công việc được giao**

- Nếu không có phiếu hoặc lịch hẹn phù hợp, hệ thống hiển thị danh sách trống.

**E1 – Không xác định được kỹ thuật viên**

- Nếu không có mã kỹ thuật viên hợp lệ, hệ thống không trả về dữ liệu công việc của kỹ thuật viên khác.

**Ghi chú:** Chức năng đăng nhập và phân quyền chi tiết nằm ngoài phạm vi bài tập. Việc xác định kỹ thuật viên trong UC6 chỉ mô tả yêu cầu nghiệp vụ, không khẳng định đã có cơ chế xác thực hoàn chỉnh.

---

## 8. UC7 – Kiểm tra điều kiện phân công

### 8.1. Thông tin chung

| Thuộc tính | Nội dung |
|---|---|
| Use Case ID | UC7 |
| Primary Actor | Không có actor khởi tạo trực tiếp; được UC3 gọi |
| Goal | Xác nhận phiếu và kỹ thuật viên đủ điều kiện phân công |
| Related User Story | US3 – MUST |
| Related FR | FR7 |
| Relationship | UC3 `<<include>>` UC7 |
| Precondition | Đã xác định phiếu và kỹ thuật viên cần kiểm tra |
| Postcondition | Hệ thống trả về kết quả hợp lệ hoặc lý do từ chối |

### 8.2. Main Flow

1. UC3 gửi thông tin phiếu và kỹ thuật viên cần kiểm tra.
2. Hệ thống kiểm tra phiếu có trạng thái PENDING.
3. Hệ thống kiểm tra phiếu chưa có phân công đang hoạt động.
4. Hệ thống kiểm tra kỹ thuật viên có trạng thái AVAILABLE.
5. Hệ thống kiểm tra kỹ thuật viên thuộc cùng trung tâm với phiếu.
6. Hệ thống kiểm tra proficiency của kỹ thuật viên đối với nhóm sự cố của phiếu đạt tối thiểu 3.
7. Nếu tất cả điều kiện được đáp ứng, hệ thống trả về kết quả hợp lệ cho UC3.

### 8.3. Exception Flow

**E1 – Phiếu không đủ điều kiện**

- Nếu phiếu không PENDING hoặc đã có phân công đang hoạt động, hệ thống trả về kết quả không hợp lệ.

**E2 – Kỹ thuật viên không đủ điều kiện**

- Nếu kỹ thuật viên không AVAILABLE, khác trung tâm hoặc proficiency dưới 3, hệ thống trả về lý do không hợp lệ.

**E3 – Thiếu dữ liệu kiểm tra**

- Nếu không tìm thấy phiếu, kỹ thuật viên hoặc dữ liệu kỹ năng cần thiết, hệ thống không cho phép xác nhận phân công.

---

## 9. UC8 – Kiểm tra trùng lịch

### 9.1. Thông tin chung

| Thuộc tính | Nội dung |
|---|---|
| Use Case ID | UC8 |
| Primary Actor | Không có actor khởi tạo trực tiếp; được UC5 gọi |
| Goal | Phát hiện xung đột thời gian trước khi lưu lịch hẹn |
| Related User Story | US5 – SHOULD |
| Related FR | FR8 |
| Relationship | UC5 `<<include>>` UC8 |
| Precondition | Có thông tin phiếu và khoảng thời gian lịch hẹn cần kiểm tra |
| Postcondition | Hệ thống trả về kết quả có hoặc không có xung đột |

### 9.2. Main Flow

1. UC5 gửi thông tin lịch hẹn dự kiến.
2. Hệ thống xác định đối tượng hoặc tài nguyên cần kiểm tra trùng lịch.
3. Hệ thống truy xuất các lịch hẹn hiện có liên quan đến đối tượng đó.
4. Hệ thống so sánh khoảng thời gian dự kiến với các lịch hẹn hiện có.
5. Nếu không có khoảng thời gian chồng lấn, hệ thống trả về kết quả không trùng lịch cho UC5.

### 9.3. Exception Flow

**E1 – Phát hiện xung đột**

- Nếu lịch hẹn dự kiến chồng lấn với lịch hiện có của cùng đối tượng hoặc tài nguyên, hệ thống trả về kết quả trùng lịch.
- UC5 không cho phép xác nhận lịch hẹn đó.

**E2 – Thiếu thông tin thời gian**

- Nếu thiếu dữ liệu cần thiết để xác định xung đột, hệ thống trả về kết quả không hợp lệ và không xác nhận lịch.

**Quy tắc kiểm tra:** Hai khoảng thời gian được xem là chồng lấn khi:

`start_new < end_existing` và `end_new > start_existing`.

Điều kiện này áp dụng cho hai khoảng thời gian có thời điểm bắt đầu và kết thúc hợp lệ; hai lịch chỉ tiếp giáp nhau tại một mốc thời gian không bị xem là chồng lấn.

---

## 10. Liên kết Business Rules và NFR

| Quy tắc | Use Case liên quan |
|---|---|
| BR1 – Một phân công đang hoạt động trên mỗi phiếu; thay đổi cần lý do | UC3, UC4, UC7 |
| BR2 – AVAILABLE, proficiency ≥ 3, cùng trung tâm | UC2, UC3, UC4, UC7 |
| BR3 – Phiếu PENDING và chưa có phân công đang hoạt động | UC1, UC3, UC7 |
| BR4 – Thời hạn cam kết theo ưu tiên | UC1 (thông tin ưu tiên phục vụ theo dõi) |
| NFR1 – Hiển thị danh sách ≤ 2 giây với ≤ 100 bản ghi | UC1, UC2 |
| NFR2 – Phản hồi phân công hoặc đặt lịch ≤ 2 giây | UC3, UC5 |
| NFR3 – Phân công trong tối đa 5 bước tương tác chính | UC3 |

**Lưu ý:** Các bước trong Main Flow mô tả tương tác giữa actor và hệ thống, không đồng nghĩa mỗi bước là một lần nhấp chuột. NFR3 phải được kiểm tra dựa trên số bước tương tác thực tế của người quản lý.

---

## 11. Ghi chú đồng bộ tài liệu

- Tài liệu này sử dụng 6 User Stories: US1–US6.
- UC7 thuộc yêu cầu kiểm tra của US3, không tạo User Story riêng.
- UC8 thuộc yêu cầu kiểm tra của US5, không tạo User Story riêng.
- Sơ đồ `docs/usecase.drawio` cần thể hiện đầy đủ UC1–UC8 và hai quan hệ `<<include>>` chính.
- UC4 không có quan hệ `<<include>>` với UC7; UC4 thực hiện kiểm tra điều kiện kỹ thuật viên theo BR2 trong quy trình thay đổi phân công riêng.
- Các trường hợp ngoại lệ và điều kiện kiểm tra được mô tả như yêu cầu thiết kế, không khẳng định toàn bộ đã được lập trình hoặc kiểm thử thành công.
