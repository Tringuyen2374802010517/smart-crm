# SRS Rút Gọn – Smart CRM Mekong Mobile

**Sinh viên:** Nguyễn Minh Trị  
**MSSV:** 2374802010517  
**Track:** SE  
**Luồng nghiệp vụ:** L4 – Phân công kỹ thuật viên và lịch hẹn

---

## 1. Giới thiệu và phạm vi

### 1.1. Bối cảnh

Smart CRM – Mekong Mobile hỗ trợ hoạt động quản lý dịch vụ sửa chữa thiết bị. Trong luồng L4, quản lý trung tâm cần phân công kỹ thuật viên phù hợp cho các phiếu cần xử lý và quản lý lịch giao – nhận máy.

### 1.2. Phạm vi

Hệ thống hỗ trợ:

- Xem các phiếu đang cần phân công kỹ thuật viên.
- Xem các kỹ thuật viên đang khả dụng.
- Kiểm tra kỹ năng và trung tâm của kỹ thuật viên.
- Phân công kỹ thuật viên cho phiếu.
- Thay đổi kỹ thuật viên phụ trách và ghi nhận lý do.
- Đặt lịch giao – nhận máy.
- Kiểm tra trùng lịch trước khi xác nhận lịch hẹn.
- Cho phép kỹ thuật viên xem công việc và lịch hẹn được giao.

### 1.3. Ngoài phạm vi

Bài tập không thực hiện:

- Quản lý toàn bộ quy trình CRM của Mekong Mobile.
- Quản lý thanh toán và hóa đơn.
- Quản lý kho và linh kiện.
- Xây dựng chức năng đăng nhập và phân quyền chi tiết.
- Triển khai hệ thống thực tế.

### 1.4. Bảng thuật ngữ

| Thuật ngữ | Giải thích |
|---|---|
| Phiếu (Ticket) | Phiếu ghi nhận yêu cầu hoặc sự cố cần được xử lý |
| Kỹ thuật viên (Technician) | Nhân viên kỹ thuật được phân công xử lý phiếu |
| Phân công (Assignment) | Việc gán kỹ thuật viên phụ trách một phiếu |
| Lịch hẹn (Appointment) | Thời gian giao hoặc nhận máy đã được lên lịch |
| Proficiency | Mức độ thành thạo của kỹ thuật viên đối với nhóm sự cố |
| Workload | Khối lượng công việc hiện tại của kỹ thuật viên |
| Trung tâm (Center) | Trung tâm nơi phiếu và kỹ thuật viên được quản lý |

---

## 2. Các bên liên quan và vai trò người dùng

| Vai trò | Trách nhiệm |
|---|---|
| Quản lý trung tâm | Xem phiếu cần phân công, xem kỹ thuật viên khả dụng, kiểm tra điều kiện phân công, phân công hoặc thay đổi kỹ thuật viên, đặt lịch và kiểm tra trùng lịch |
| Kỹ thuật viên | Xem các phiếu và lịch hẹn được giao cho mình |
| Khách hàng | Liên quan đến hoạt động giao – nhận máy nhưng không trực tiếp thực hiện chức năng quản lý trong phạm vi bài tập |

---

## 3. Yêu cầu chức năng và User Story

### 3.1. Functional Requirements

**FR1 – Xem phiếu cần phân công**  
Hệ thống phải cho phép quản lý trung tâm xem danh sách các phiếu đang cần phân công kỹ thuật viên.

**FR2 – Xem kỹ thuật viên khả dụng**  
Hệ thống phải cho phép quản lý trung tâm xem danh sách kỹ thuật viên khả dụng cùng thông tin về kỹ năng, khu vực và khối lượng công việc hiện tại.

**FR3 – Phân công kỹ thuật viên**  
Hệ thống phải cho phép quản lý trung tâm phân công kỹ thuật viên cho một phiếu.

**FR4 – Thay đổi kỹ thuật viên**  
Hệ thống phải cho phép quản lý trung tâm thay đổi kỹ thuật viên phụ trách và ghi nhận lý do thay đổi.

**FR5 – Đặt lịch giao – nhận máy**  
Hệ thống phải cho phép quản lý trung tâm tạo lịch giao – nhận máy cho phiếu.

**FR6 – Xem công việc được giao**  
Hệ thống phải cho phép kỹ thuật viên xem các phiếu và lịch hẹn được giao cho mình.

**FR7 – Kiểm tra điều kiện phân công**  
Hệ thống phải kiểm tra kỹ thuật viên có mức proficiency phù hợp và thuộc cùng trung tâm trước khi xác nhận phân công.

**FR8 – Kiểm tra trùng lịch**  
Hệ thống phải kiểm tra xung đột lịch trước khi xác nhận lịch giao – nhận máy.

### 3.2. User Stories và MoSCoW

**US1 – MUST**  
Là quản lý trung tâm, tôi muốn xem các phiếu đang cần phân công để biết phiếu nào cần được xử lý.

**US2 – MUST**  
Là quản lý trung tâm, tôi muốn xem các kỹ thuật viên đang khả dụng cùng kỹ năng, khu vực và khối lượng công việc để lựa chọn kỹ thuật viên phù hợp.

**US3 – MUST**  
Là quản lý trung tâm, tôi muốn phân công một kỹ thuật viên cho phiếu để xác định người chịu trách nhiệm xử lý.

**US4 – SHOULD**  
Là quản lý trung tâm, tôi muốn thay đổi kỹ thuật viên phụ trách và ghi nhận lý do để xử lý trường hợp cần điều chỉnh phân công.

**US5 – SHOULD**  
Là quản lý trung tâm, tôi muốn đặt lịch giao – nhận máy để xác định thời gian thực hiện việc giao hoặc nhận thiết bị.

**US6 – COULD**  
Là kỹ thuật viên, tôi muốn xem các phiếu và lịch hẹn được giao để theo dõi công việc của mình.

**US7 – SHOULD**  
Là quản lý trung tâm, tôi muốn hệ thống kiểm tra kỹ năng và trung tâm của kỹ thuật viên trước khi phân công để tránh phân công không phù hợp.

**US8 – SHOULD**  
Là quản lý trung tâm, tôi muốn hệ thống kiểm tra trùng lịch trước khi xác nhận lịch giao – nhận máy để tránh xung đột lịch.

### 3.3. Acceptance Criteria cho các User Story MUST

#### US1 – Xem phiếu cần phân công

**AC1**

- **Given** quản lý trung tâm đang sử dụng hệ thống.
- **When** quản lý mở danh sách phiếu cần phân công.
- **Then** hệ thống hiển thị các phiếu đang chờ phân công kỹ thuật viên.

**AC2**

- **Given** danh sách có nhiều phiếu.
- **When** hệ thống hiển thị danh sách.
- **Then** mỗi phiếu hiển thị các thông tin cần thiết như mã phiếu, tiêu đề, mức ưu tiên, trạng thái và trung tâm.

#### US2 – Xem kỹ thuật viên khả dụng

**AC1**

- **Given** quản lý đã chọn một phiếu cần phân công.
- **When** quản lý yêu cầu xem kỹ thuật viên khả dụng.
- **Then** hệ thống hiển thị danh sách các kỹ thuật viên đang khả dụng.

**AC2**

- **Given** danh sách kỹ thuật viên khả dụng được hiển thị.
- **When** quản lý xem thông tin kỹ thuật viên.
- **Then** hệ thống hiển thị kỹ năng, khu vực, khối lượng công việc và trạng thái khả dụng.

#### US3 – Phân công kỹ thuật viên

**AC1**

- **Given** quản lý đã chọn phiếu và một kỹ thuật viên phù hợp.
- **When** quản lý xác nhận phân công.
- **Then** hệ thống ghi nhận kỹ thuật viên phụ trách phiếu.

**AC2**

- **Given** kỹ thuật viên không đáp ứng điều kiện phân công.
- **When** quản lý thực hiện phân công.
- **Then** hệ thống từ chối phân công và thông báo lý do.

---

## 4. Yêu cầu phi chức năng

**NFR1 – Hiệu năng danh sách**  
Hệ thống phải hiển thị danh sách phiếu hoặc kỹ thuật viên trong thời gian không quá **2 giây** với tối đa **100 bản ghi**.

**NFR2 – Hiệu năng thao tác**  
Hệ thống phải phản hồi thao tác phân công kỹ thuật viên hoặc đặt lịch trong thời gian không quá **2 giây**.

**NFR3 – Khả dụng thao tác**  
Người quản lý phải có thể hoàn thành quy trình phân công kỹ thuật viên trong tối đa **5 bước tương tác chính**, tính từ danh sách phiếu cần phân công.

---

## 5. Ràng buộc và Business Rules

**BR1 – Phân công kỹ thuật viên**  
Tại một thời điểm, một phiếu chỉ được gán cho tối đa một kỹ thuật viên. Khi thay đổi kỹ thuật viên phải ghi nhận lý do thay đổi.

**BR2 – Điều kiện kỹ thuật viên**  
Kỹ thuật viên chỉ được phân công cho nhóm sự cố mà kỹ thuật viên có mức proficiency **≥ 3** và phải thuộc cùng trung tâm.

**BR3 – Trạng thái phiếu**  
Trạng thái phiếu phải tuân theo vòng đời quy định, không được chuyển ngược trạng thái và mọi thay đổi trạng thái phải được ghi nhận.

**BR4 – Thời hạn cam kết**  
Thời hạn cam kết xử lý theo mức ưu tiên:

- CAO: 24 giờ.
- TRUNG_BINH: 72 giờ.
- THAP: 120 giờ.

Ngày làm việc được tính từ **Thứ Hai đến Thứ Bảy**.

---

## 6. Traceability Matrix

| FR | User Story | Use Case | MoSCoW |
|---|---|---|---|
| FR1 | US1 | UC1 – Xem phiếu cần phân công | MUST |
| FR2 | US2 | UC2 – Xem kỹ thuật viên khả dụng | MUST |
| FR3 | US3 | UC3 – Phân công kỹ thuật viên | MUST |
| FR4 | US4 | UC4 – Thay đổi kỹ thuật viên phụ trách | SHOULD |
| FR5 | US5 | UC5 – Đặt lịch giao – nhận máy | SHOULD |
| FR6 | US6 | UC6 – Xem công việc và lịch hẹn được giao | COULD |
| FR7 | US7 | UC7 – Kiểm tra điều kiện phân công | SHOULD |
| FR8 | US8 | UC8 – Kiểm tra trùng lịch | SHOULD |