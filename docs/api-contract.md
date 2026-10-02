# API Contract – Smart CRM Mekong Mobile

**Luồng nghiệp vụ:** L4 – Phân công kỹ thuật viên và lịch hẹn  
**Track:** SE

---

## 1. Danh sách API

| Method | Endpoint | Chức năng | Use Case |
|---|---|---|---|
| GET | `/api/tickets/unassigned` | Lấy danh sách phiếu cần phân công | UC1 |
| GET | `/api/technicians/available` | Lấy danh sách kỹ thuật viên khả dụng | UC2 |
| POST | `/api/tickets/{ticket_id}/assignments` | Phân công kỹ thuật viên và kiểm tra điều kiện phân công | UC3, UC7 |
| PUT | `/api/tickets/{ticket_id}/assignments` | Thay đổi kỹ thuật viên phụ trách | UC4 |
| POST | `/api/tickets/{ticket_id}/appointments` | Tạo lịch giao – nhận máy và kiểm tra trùng lịch | UC5, UC8 |
| GET | `/api/technicians/{technician_id}/work` | Xem công việc và lịch hẹn được giao | UC6 |

---

## 2. GET /api/tickets/unassigned

### Mục đích

Lấy danh sách các phiếu đang cần được phân công kỹ thuật viên.

### Response – 200 OK

```json
[
  {
    "ticket_id": 1001,
    "title": "Không có mạng",
    "incident_group": "Network",
    "priority": "HIGH",
    "status": "PENDING",
    "center_id": 1
  }
]
```

---

## 3. GET /api/technicians/available

### Mục đích

Lấy danh sách kỹ thuật viên khả dụng để hỗ trợ quản lý lựa chọn kỹ thuật viên cho một phiếu.

### Query Parameter

```text
ticket_id=1001
```

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

Phân công kỹ thuật viên cho phiếu.

API thực hiện **UC7 – Kiểm tra điều kiện phân công** trước khi ghi nhận phân công.

Điều kiện kiểm tra:

- Kỹ thuật viên có `proficiency >= 3` đối với `incident_group` của phiếu.
- Kỹ thuật viên và phiếu thuộc cùng trung tâm.
- Kỹ thuật viên đang khả dụng.

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

---

## 5. PUT /api/tickets/{ticket_id}/assignments

### Mục đích

Thay đổi kỹ thuật viên đang phụ trách phiếu và ghi nhận lý do thay đổi.

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

---

## 6. POST /api/tickets/{ticket_id}/appointments

### Mục đích

Tạo lịch giao hoặc nhận máy cho phiếu.

API thực hiện **UC8 – Kiểm tra trùng lịch** trước khi ghi nhận lịch hẹn.

### Request

```json
{
  "technician_id": 201,
  "appointment_type": "GIAO_MAY",
  "scheduled_at": "2026-10-03T09:00:00",
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
  "scheduled_at": "2026-10-03T09:00:00",
  "status": "SCHEDULED"
}
```

### Error – 409 Conflict

```json
{
  "message": "Appointment time conflicts with an existing appointment."
}
```

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
      "priority": "HIGH",
      "status": "ASSIGNED"
    }
  ],
  "appointments": [
    {
      "appointment_id": 401,
      "ticket_id": 1001,
      "appointment_type": "GIAO_MAY",
      "scheduled_at": "2026-10-03T09:00:00",
      "status": "SCHEDULED"
    }
  ]
}
```

---

## 8. Quy tắc xử lý chính

- Một phiếu chỉ có tối đa một kỹ thuật viên đang phụ trách tại một thời điểm.
- Khi thay đổi kỹ thuật viên, hệ thống phải lưu lý do thay đổi.
- Kỹ thuật viên phải có `proficiency >= 3` đối với nhóm sự cố của phiếu.
- Kỹ thuật viên phải thuộc cùng trung tâm với phiếu.
- Hệ thống phải kiểm tra khả dụng của kỹ thuật viên trước khi phân công.
- Hệ thống phải kiểm tra xung đột lịch trước khi tạo lịch hẹn.