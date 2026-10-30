
# API Contract – Smart CRM Mekong Mobile

**Sinh viên:** Nguyễn Minh Trị
**MSSV:** 2374802010517
**Track:** SE
**Luồng nghiệp vụ:** L4 – Phân công kỹ thuật viên và lịch hẹn

**Trạng thái tài liệu:** API Contract mô tả thiết kế mục tiêu của luồng L4. Các endpoint trong tài liệu không mặc nhiên là những endpoint đã được triển khai.

**Phạm vi Sprint 1 (Buổi 8):** Backend hiện triển khai CRUD Ticket, truy vấn kỹ thuật viên đủ điều kiện và tạo phân công kỹ thuật viên. Các chức năng thay đổi phân công, đặt lịch giao – nhận máy và xem công việc của kỹ thuật viên thuộc kế hoạch phát triển tiếp theo.

---

## 1. Danh sách API thiết kế mục tiêu

| Method | Endpoint | Chức năng | Use Case |
|---|---|---|---|
| GET | `/api/tickets/unassigned` | Lấy danh sách phiếu cần phân công | UC1 |
| GET | `/api/technicians/available` | Lấy danh sách kỹ thuật viên khả dụng | UC2 |
| POST | `/api/tickets/{ticket_id}/assignments` | Phân công kỹ thuật viên và kiểm tra điều kiện phân công | UC3, UC7 |
| PUT | `/api/tickets/{ticket_id}/assignments` | Thay đổi kỹ thuật viên phụ trách | UC4 |
| POST | `/api/tickets/{ticket_id}/appointments` | Tạo lịch giao – nhận máy và kiểm tra trùng lịch | UC5, UC8 |
| GET | `/api/technicians/{technician_id}/work` | Xem công việc và lịch hẹn được giao | UC6 |

**Lưu ý:** Các endpoint trên là thiết kế mục tiêu. Đường dẫn và phạm vi triển khai thực tế của Sprint 1 được đối chiếu tại Mục 9.

---

## 2. GET /api/tickets/unassigned

### Mục đích

Lấy danh sách các phiếu đang cần được phân công kỹ thuật viên.

Chỉ lấy các phiếu có trạng thái `PENDING` và chưa có phân công đang hoạt động.

### Response – 200 OK

```json
[
  {
    "ticket_id": 1001,
    "title": "Không có mạng",
    "incident_group": "Network",
    "priority": "CAO",
    "status": "PENDING",
    "center_id": 1
  }
]
```

---

## 3. GET /api/technicians/available

### Mục đích

Lấy danh sách kỹ thuật viên khả dụng để hỗ trợ quản lý lựa chọn kỹ thuật viên phù hợp cho một phiếu.

### Query Parameter

```text
ticket_id=1001
```

### Điều kiện lựa chọn

- Kỹ thuật viên có trạng thái `AVAILABLE`.
- Thuộc cùng trung tâm với phiếu.
- Có `proficiency >= 3` đối với nhóm sự cố của phiếu.
- Phiếu có trạng thái `PENDING` và chưa có phân công đang hoạt động.

### Response – 200 OK

```json
[
  {
    "technician_id": 201,
    "name": "Nguyễn An",
    "center_id": 1,
    "area": "Q1",
    "availability_status": "AVAILABLE",
    "current_workload": 2,
    "incident_group": "Network",
    "proficiency": 4
  }
]
```

---

## 4. POST /api/tickets/{ticket_id}/assignments

### Mục đích

Phân công kỹ thuật viên cho một phiếu đang chờ xử lý.

API thực hiện **UC7 – Kiểm tra điều kiện phân công** trước khi ghi nhận phân công.

### Điều kiện kiểm tra

- Phiếu tồn tại và có trạng thái `PENDING`.
- Phiếu chưa có phân công đang hoạt động.
- Kỹ thuật viên có trạng thái `AVAILABLE`.
- Kỹ thuật viên thuộc cùng trung tâm với phiếu.
- Kỹ thuật viên có `proficiency >= 3` đối với `incident_group` của phiếu.

### Request

```json
{
  "technician_id": 201
}
```

### Response – 201 Created

```json
{
  "assignment_id": 301,
  "ticket_id": 1001,
  "technician_id": 201,
  "assigned_at": "2026-10-02T19:00:00",
  "ended_at": null
}
```

### Error – 400 Bad Request

```json
{
  "message": "Technician does not meet assignment conditions."
}
```

### Error – 409 Conflict

```json
{
  "message": "Ticket already has an active technician assignment."
}
```

**Quy tắc BR1:** Tại một thời điểm, mỗi phiếu chỉ có tối đa một phân công đang hoạt động.

---

## 5. PUT /api/tickets/{ticket_id}/assignments

### Mục đích

Thay đổi kỹ thuật viên đang phụ trách phiếu và ghi nhận lý do thay đổi.

Đây là quy trình riêng của UC4, không sử dụng quan hệ `<<include>>` với UC7 vì UC7 kiểm tra điều kiện tạo phân công mới đối với phiếu `PENDING` chưa có phân công đang hoạt động.

### Điều kiện kiểm tra

- Phiếu đã có kỹ thuật viên đang phụ trách.
- Kỹ thuật viên mới đáp ứng các điều kiện của BR2.
- Lý do thay đổi không được để trống.
- Phân công cũ được kết thúc trước khi tạo phân công mới.
- Không tồn tại đồng thời hai phân công đang hoạt động trên cùng một phiếu.

### Request

```json
{
  "technician_id": 202,
  "change_reason": "Kỹ thuật viên hiện tại không còn khả dụng."
}
```

### Response – 200 OK

```json
{
  "ticket_id": 1001,
  "technician_id": 202,
  "change_reason": "Kỹ thuật viên hiện tại không còn khả dụng.",
  "message": "Technician assignment updated successfully."
}
```

### Error – 400 Bad Request

```json
{
  "message": "New technician does not meet assignment conditions."
}
```

**Trạng thái triển khai:** Chưa triển khai trong Sprint 1.

---

## 6. POST /api/tickets/{ticket_id}/appointments

### Mục đích

Tạo lịch giao hoặc nhận máy cho một phiếu.

API thực hiện **UC8 – Kiểm tra trùng lịch** trước khi ghi nhận lịch hẹn.

### Điều kiện kiểm tra

- Phiếu và kỹ thuật viên tồn tại.
- Có đầy đủ `start_time` và `end_time`.
- `end_time` phải lớn hơn `start_time`.
- Không có lịch hẹn chồng lấn của cùng kỹ thuật viên trong khoảng thời gian dự kiến.

Hai lịch được xác định chồng lấn khi:

```text
start_new < end_existing
AND
end_new > start_existing
```

Hai lịch chỉ tiếp giáp tại thời điểm kết thúc và bắt đầu không được xem là chồng lấn.

### Request

```json
{
  "technician_id": 201,
  "appointment_type": "GIAO_MAY",
  "start_time": "2026-10-03T09:00:00",
  "end_time": "2026-10-03T10:00:00",
  "status": "SCHEDULED"
}
```

### Response – 201 Created

```json
{
  "appointment_id": 401,
  "ticket_id": 1001,
  "technician_id": 201,
  "appointment_type": "GIAO_MAY",
  "start_time": "2026-10-03T09:00:00",
  "end_time": "2026-10-03T10:00:00",
  "status": "SCHEDULED"
}
```

### Error – 400 Bad Request

```json
{
  "message": "Appointment end time must be later than start time."
}
```

### Error – 409 Conflict

```json
{
  "message": "Appointment time conflicts with an existing appointment."
}
```

**Trạng thái triển khai:** Chưa triển khai API và logic kiểm tra trùng lịch trong Sprint 1. Cấu trúc bảng `appointment` đã được thiết kế với `start_time` và `end_time`.

---

## 7. GET /api/technicians/{technician_id}/work

### Mục đích

Cho phép kỹ thuật viên xem các phiếu và lịch hẹn được giao.

### Response – 200 OK

```json
{
  "technician_id": 201,
  "tickets": [
    {
      "ticket_id": 1001,
      "title": "Không có mạng",
      "incident_group": "Network",
      "priority": "CAO",
      "status": "ASSIGNED"
    }
  ],
  "appointments": [
    {
      "appointment_id": 401,
      "ticket_id": 1001,
      "appointment_type": "GIAO_MAY",
      "start_time": "2026-10-03T09:00:00",
      "end_time": "2026-10-03T10:00:00",
      "status": "SCHEDULED"
    }
  ]
}
```

**Trạng thái triển khai:** Chưa triển khai trong Sprint 1.

---

## 8. Quy tắc xử lý chính

### BR1 – Quy tắc phân công

- Một phiếu chỉ có tối đa một kỹ thuật viên đang phụ trách tại một thời điểm.
- Khi thay đổi kỹ thuật viên phải ghi nhận lý do.
- Phân công cũ phải được kết thúc trước khi ghi nhận phân công mới.

### BR2 – Điều kiện kỹ thuật viên

- Kỹ thuật viên phải có trạng thái `AVAILABLE`.
- Có `proficiency >= 3` đối với nhóm sự cố của phiếu.
- Thuộc cùng trung tâm với phiếu.

### BR3 – Điều kiện trạng thái phiếu

- Chỉ tạo phân công mới cho phiếu `PENDING` chưa có phân công đang hoạt động.
- Thay đổi kỹ thuật viên được xử lý theo quy trình riêng của UC4.

### BR4 – Thời hạn cam kết

| Priority | Thời hạn |
|---|---|
| CAO | 24 giờ |
| TRUNG_BINH | 72 giờ |
| THAP | 120 giờ |

Ngày làm việc được tính từ Thứ Hai đến Thứ Bảy.

### Quy tắc lịch hẹn

- `start_time` và `end_time` là bắt buộc.
- `end_time > start_time`.
- Phải kiểm tra trùng lịch trước khi xác nhận.
- Không được ghi nhận lịch hẹn nếu phát hiện xung đột.

---

## 9. Đối chiếu API Sprint 1 và API thiết kế

### 9.1. API đã được lập trình trong Sprint 1

| Method | Endpoint thực tế | Chức năng | Trạng thái |
|---|---|---|---|
| GET | `/tickets` | Lấy danh sách tất cả phiếu | Đã lập trình |
| GET | `/tickets/{ticket_id}` | Xem chi tiết phiếu | Đã lập trình |
| POST | `/tickets` | Tạo phiếu | Đã lập trình |
| PUT | `/tickets/{ticket_id}` | Cập nhật phiếu | Đã lập trình |
| DELETE | `/tickets/{ticket_id}` | Xóa phiếu khi không có phân công hoặc lịch hẹn liên quan | Đã lập trình |
| GET | `/assignments/eligible-technicians/{ticket_id}` | Lấy danh sách kỹ thuật viên đủ điều kiện | Đã lập trình |
| POST | `/assignments/` | Tạo phân công kỹ thuật viên | Đã lập trình |

**Lưu ý:** Trạng thái "Đã lập trình" được xác định theo mã nguồn backend, không đồng nghĩa tất cả API đã vượt qua kiểm thử.

### 9.2. Khác biệt giữa thiết kế mục tiêu và Sprint 1

| Use Case | API thiết kế mục tiêu | Tình trạng Sprint 1 |
|---|---|---|
| UC1 | `GET /api/tickets/unassigned` | Chưa có endpoint lọc riêng; `GET /tickets` hiện lấy tất cả phiếu |
| UC2 | `GET /api/technicians/available?ticket_id=1001` | Có chức năng tương ứng tại `GET /assignments/eligible-technicians/{ticket_id}` |
| UC3, UC7 | `POST /api/tickets/{ticket_id}/assignments` | Có chức năng tương ứng tại `POST /assignments/`, truyền `ticket_id` và `technician_id` trong body |
| UC4 | `PUT /api/tickets/{ticket_id}/assignments` | Chưa triển khai |
| UC5, UC8 | `POST /api/tickets/{ticket_id}/appointments` | Chưa triển khai |
| UC6 | `GET /api/technicians/{technician_id}/work` | Chưa triển khai |

### 9.3. Request thực tế của API phân công Sprint 1

**POST `/assignments/`**

```json
{
  "ticket_id": 1001,
  "technician_id": 201
}
```

Backend kiểm tra trạng thái phiếu, phân công đang hoạt động, trạng thái kỹ thuật viên, trung tâm và mức proficiency trước khi tạo phân công.

### 9.4. Quy ước phản hồi lỗi

Các ví dụ ở Mục 2–7 mô tả **response dự kiến của API thiết kế mục tiêu**.

Backend Sprint 1 sử dụng FastAPI và `HTTPException`; phản hồi lỗi có thể sử dụng trường `detail` thay vì `message`. Do đó không được dùng ví dụ response thiết kế để khẳng định kết quả kiểm thử API hiện tại.

---

## 10. Giới hạn triển khai và hướng phát triển

Trong Sprint 1, hệ thống tập trung vào các chức năng nền tảng:

- CRUD Ticket.
- Truy vấn kỹ thuật viên đủ điều kiện.
- Tạo phân công kỹ thuật viên.
- Kiểm tra các điều kiện nghiệp vụ trước khi phân công.
- Lưu dữ liệu trên SQLite.

Các chức năng chưa triển khai gồm:

- Thay đổi kỹ thuật viên phụ trách và lưu lý do.
- Đặt lịch giao – nhận máy thông qua API.
- Kiểm tra xung đột lịch hẹn.
- Xem danh sách công việc và lịch hẹn của kỹ thuật viên.
- Endpoint chuyên biệt lấy danh sách phiếu chưa được phân công.

Các chức năng này được giữ trong SRS, Use Case Specification và API Contract để phục vụ thiết kế tổng thể luồng L4, không được xem là kết quả lập trình đã hoàn thành trong Buổi 8.

---

## 11. Tài liệu liên quan

- `docs/srs.md` – Yêu cầu phần mềm, User Stories và Business Rules.
- `docs/usecase-spec.md` – Đặc tả UC1–UC8.
- `docs/usecase.drawio` – Sơ đồ Use Case.
- `docs/architecture.md` – Mô tả kiến trúc.
- `docs/architecture.drawio` – Sơ đồ kiến trúc.
- `docs/erd.drawio` – Sơ đồ cơ sở dữ liệu.
- `docs/schema.sql` – SQL DDL.
- `docs/thay-doi-thiet-ke.md` – Nhật ký thay đổi thiết kế.

---

## Phụ lục – API thực tế sau v0.2

Danh sách dưới đây được trích xuất từ OpenAPI Schema của mã nguồn hiện tại. Các endpoint thiết kế ở phần trước được giữ lại để đối chiếu với BT1.

### Ticket

| Method | Endpoint |
|---|---|
| GET | `/tickets` |
| POST | `/tickets` |
| GET | `/tickets/{ticket_id}` |
| PUT | `/tickets/{ticket_id}` |
| DELETE | `/tickets/{ticket_id}` |
| PATCH | `/tickets/{ticket_id}/complete` |

### Technician

| Method | Endpoint |
|---|---|
| GET | `/technicians` |
| POST | `/technicians` |
| GET | `/technicians/{technician_id}` |
| PUT | `/technicians/{technician_id}` |
| DELETE | `/technicians/{technician_id}` |

### Assignment

| Method | Endpoint |
|---|---|
| POST | `/assignments/` |
| GET | `/assignments/eligible-technicians/{ticket_id}` |
| GET | `/assignments/ticket/{ticket_id}/detail` |

### Appointment

| Method | Endpoint |
|---|---|
| GET | `/appointments` |
| POST | `/appointments` |
| POST | `/appointments/check` |
| GET | `/appointments/context/{ticket_id}` |
| GET | `/appointments/ticket/{ticket_id}` |

### Authentication

| Method | Endpoint |
|---|---|
| POST | `/auth/login` |
| POST | `/auth/logout` |
| GET | `/auth/me` |

### Giới hạn cần lưu ý

- OpenAPI Schema xác nhận endpoint được đăng ký, không tự xác nhận API hoạt động đúng.
- Frontend đã có cơ chế đăng nhập, nhưng các Business API chưa được bảo vệ đồng bộ bằng xác thực token.
- Các quy tắc phân công hiện tại sử dụng ngưỡng tay nghề THAP >= 2, TRUNG_BINH >= 3 và CAO >= 4.
- Cần chạy lại kiểm thử trước khi công bố kết quả BT2.
