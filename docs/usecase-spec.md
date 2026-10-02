# Use Case Specification

## Smart CRM – Mekong Mobile

**Luồng nghiệp vụ:** L4 – Phân công kỹ thuật viên và lịch hẹn  
**Track:** SE

---

## UC3 – Phân công kỹ thuật viên

### 1. Thông tin chung

| Thuộc tính | Nội dung |
|---|---|
| Use Case ID | UC3 |
| Tên Use Case | Phân công kỹ thuật viên |
| Primary Actor | Quản lý trung tâm |
| Goal | Phân công một kỹ thuật viên phù hợp cho phiếu cần xử lý. |
| Related User Story | US3 |
| Included Use Case | UC7 – Kiểm tra điều kiện phân công |
| Precondition | Phiếu chưa có kỹ thuật viên phụ trách và quản lý trung tâm đang sử dụng hệ thống. |
| Postcondition | Phiếu được ghi nhận với kỹ thuật viên phụ trách đã được phân công. |

### 2. Main Flow

1. Quản lý trung tâm mở danh sách các phiếu cần phân công.
2. Quản lý trung tâm chọn một phiếu cần xử lý.
3. Hệ thống hiển thị danh sách kỹ thuật viên đang khả dụng cùng thông tin kỹ năng, khu vực và khối lượng công việc hiện tại.
4. Quản lý trung tâm chọn một kỹ thuật viên.
5. Hệ thống thực hiện **UC7 – Kiểm tra điều kiện phân công**.
6. Nếu kỹ thuật viên đáp ứng điều kiện, hệ thống cho phép tiếp tục phân công.
7. Quản lý trung tâm xác nhận phân công.
8. Hệ thống ghi nhận kỹ thuật viên là người phụ trách phiếu.
9. Hệ thống thông báo phân công thành công.

### 3. Exception Flow

#### E1 – Kỹ thuật viên không đáp ứng điều kiện phân công

- Tại bước 5, nếu kỹ thuật viên có mức proficiency < 3 hoặc không thuộc cùng trung tâm, hệ thống không cho phép tiếp tục phân công.
- Hệ thống thông báo kỹ thuật viên không đáp ứng điều kiện phân công.
- Quản lý trung tâm quay lại bước 4 để chọn kỹ thuật viên khác.

#### E2 – Kỹ thuật viên không còn khả dụng

- Tại bước 7, nếu kỹ thuật viên được chọn không còn khả dụng, hệ thống không thực hiện phân công.
- Hệ thống thông báo kỹ thuật viên không còn khả dụng.
- Quản lý trung tâm quay lại bước 3 để xem lại danh sách kỹ thuật viên khả dụng.

---

## UC5 – Đặt lịch giao – nhận máy

### 1. Thông tin chung

| Thuộc tính | Nội dung |
|---|---|
| Use Case ID | UC5 |
| Tên Use Case | Đặt lịch giao – nhận máy |
| Primary Actor | Quản lý trung tâm |
| Goal | Tạo lịch giao hoặc nhận máy cho phiếu. |
| Related User Story | US5 |
| Included Use Case | UC8 – Kiểm tra trùng lịch |
| Precondition | Phiếu tồn tại trong hệ thống và quản lý trung tâm đang sử dụng hệ thống. |
| Postcondition | Lịch giao – nhận máy hợp lệ được ghi nhận cho phiếu. |

### 2. Main Flow

1. Quản lý trung tâm chọn phiếu cần đặt lịch giao – nhận máy.
2. Quản lý trung tâm chọn chức năng đặt lịch.
3. Quản lý trung tâm nhập thông tin lịch giao – nhận máy.
4. Hệ thống thực hiện **UC8 – Kiểm tra trùng lịch**.
5. Nếu không có xung đột lịch, hệ thống cho phép tiếp tục đặt lịch.
6. Quản lý trung tâm xác nhận đặt lịch.
7. Hệ thống ghi nhận lịch hẹn cho phiếu.
8. Hệ thống thông báo đặt lịch thành công.

### 3. Exception Flow

#### E1 – Trùng lịch hẹn

- Tại bước 4, nếu thời gian được chọn bị trùng với lịch hẹn hiện có, hệ thống không cho phép xác nhận lịch.
- Hệ thống thông báo xảy ra xung đột lịch hẹn.
- Quản lý trung tâm quay lại bước 3 để chọn thời gian khác.