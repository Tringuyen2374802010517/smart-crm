
# Smart CRM – Phân công kỹ thuật viên và lịch hẹn

**Sinh viên:** Nguyễn Minh Trị  
**MSSV:** 2374802010517  
**Track:** SE – Software Engineering  
**Học phần:** Chuyên đề Tốt nghiệp 1 – Trường Đại học Văn Lang  
**Luồng nghiệp vụ:** L4 – Phân công kỹ thuật viên và lịch hẹn  
**Repository:** https://github.com/Tringuyen2374802010517/smart-crm

---

## 1. Mô tả bài toán

Smart CRM – Mekong Mobile là dự án hỗ trợ quản lý hoạt động dịch vụ sửa chữa thiết bị.

Trong luồng nghiệp vụ L4, quản lý trung tâm cần phân công kỹ thuật viên cho các phiếu dựa trên tay nghề, địa bàn, trạng thái khả dụng và khối lượng công việc hiện tại. Đồng thời, hệ thống hỗ trợ đặt lịch giao – nhận máy và kiểm tra xung đột lịch hẹn.

Mục tiêu của dự án là xây dựng các chức năng cốt lõi của luồng L4 dựa trên tài liệu phân tích và thiết kế đã thực hiện trong BT1.

---

## 2. Yêu cầu môi trường và cách chạy

### 2.1. Công nghệ sử dụng

| Thành phần | Công nghệ / Công cụ |
|---|---|
| Ngôn ngữ Backend | Python 3.12 |
| Backend Framework | FastAPI |
| Database | SQLite |
| API | REST API |
| Version Control | Git, GitHub |
| Development Tool | Visual Studio Code |
| Diagram / Wireframe | Draw.io |

### 2.2. Cấu hình môi trường

Yêu cầu máy tính đã cài đặt:

- Python 3.12
- Git
- SQLite
- Trình soạn thảo mã nguồn, khuyến nghị Visual Studio Code

Di chuyển đến thư mục dự án:

```bash
cd ~/Downloads/smart-crm
```

Tạo môi trường Python ảo nếu chưa có:

```bash
python3.12 -m venv .venv
```

Cài đặt các thư viện cần thiết:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

### 2.3. Khởi tạo cơ sở dữ liệu

Dự án sử dụng SQLite với 5 bảng chính:

1. `ticket`
2. `technician`
3. `technician_skill`
4. `assignment`
5. `appointment`

Khi thiết lập cơ sở dữ liệu mới, chạy:

```bash
sqlite3 smartcrm.db < docs/schema.sql
```

**Lưu ý:** Chỉ chạy lệnh khởi tạo bảng trên database mới, chưa có các bảng. Không chạy lại trực tiếp trên database đã được khởi tạo.

Kiểm tra danh sách bảng:

```bash
sqlite3 smartcrm.db ".tables"
```

Kiểm tra ràng buộc khóa ngoại:

```bash
sqlite3 smartcrm.db "PRAGMA foreign_key_check;"
```

### 2.4. Khởi chạy Backend

Từ thư mục gốc dự án, chạy:

```bash
.venv/bin/python -m uvicorn src.backend.main:app --host 127.0.0.1 --port 8000
```

Sau khi Backend khởi chạy, truy cập:

- API Documentation: http://127.0.0.1:8000/docs
- Kiểm tra database: http://127.0.0.1:8000/db-check
- Danh sách Ticket: http://127.0.0.1:8000/tickets

### 2.5. Kiểm thử API

Module Ticket hỗ trợ các endpoint:

| Method | Endpoint | Chức năng |
|---|---|---|
| GET | `/tickets` | Xem danh sách phiếu |
| GET | `/tickets/{ticket_id}` | Xem chi tiết phiếu |
| POST | `/tickets` | Tạo phiếu mới |
| PUT | `/tickets/{ticket_id}` | Cập nhật phiếu |
| DELETE | `/tickets/{ticket_id}` | Xóa phiếu |

Ví dụ tạo Ticket bằng `curl`:

```bash
curl -X POST http://127.0.0.1:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sua man hinh dien thoai",
    "incident_group": "MAN_HINH",
    "priority": "CAO",
    "center_id": 1
  }'
```

Các mức ưu tiên hợp lệ:

- `CAO`
- `TRUNG_BINH`
- `THAP`

Ticket mới được tạo với trạng thái mặc định `PENDING`.

---

## 3. Phạm vi

### 3.1. Trong phạm vi

Các chức năng thuộc luồng L4 bao gồm:

- Xem danh sách các phiếu cần phân công.
- Xem danh sách kỹ thuật viên khả dụng.
- Kiểm tra tay nghề, trung tâm và trạng thái khả dụng của kỹ thuật viên.
- Phân công kỹ thuật viên cho phiếu.
- Thay đổi kỹ thuật viên phụ trách và ghi nhận lý do.
- Đặt lịch giao – nhận máy.
- Kiểm tra xung đột lịch trước khi xác nhận.
- Cho phép kỹ thuật viên xem các phiếu và lịch hẹn được giao.

### 3.2. Ngoài phạm vi

Dự án không tập trung triển khai:

- Tiếp nhận và phân loại toàn bộ yêu cầu bảo hành.
- Quản lý kho linh kiện.
- Quản lý thanh toán và hóa đơn.
- Xử lý toàn bộ quy trình sửa chữa thiết bị.
- Chức năng đăng nhập và phân quyền chi tiết.
- Các luồng nghiệp vụ khác ngoài L4.
- Triển khai hệ thống trong môi trường vận hành thực tế.

---

## 4. Tài liệu phân tích và thiết kế BT1

Các tài liệu được lưu trong thư mục `docs/`.

| Tài liệu | Nội dung |
|---|---|
| `srs.md` | SRS rút gọn, FR, NFR, User Stories, Business Rules và Traceability Matrix |
| `usecase.drawio` | Source Use Case Diagram |
| `usecase.png` | Hình ảnh Use Case Diagram |
| `usecase-spec.md` | Đặc tả Use Case |
| `architecture.md` | Mô tả và lập luận kiến trúc |
| `architecture.drawio` | Source Architecture Diagram |
| `architecture.png` | Hình ảnh Architecture Diagram |
| `erd.drawio` | Source Entity Relationship Diagram |
| `erd.png` | Hình ảnh ERD |
| `schema.sql` | SQL DDL tạo bảng và chỉ mục |
| `wireframe.drawio` | Source Wireframe |
| `wireframe.png` | Wireframe các màn hình |
| `api-contract.md` | API Contract dành cho track SE |
| `ai-disclosure.md` | Khai báo sử dụng công cụ AI |
| `thay-doi-thiet-ke.md` | Ghi nhận phản hồi BT1 và quyết định điều chỉnh thiết kế |
| `minh-chung-api-buoi8.txt` | Kết quả kiểm thử API trong Buổi 8 |

Báo cáo BT1 được lưu tại:

`docs/CDTN1_Buoi6_2374802010517_NguyenMinhTri.pdf`

---

## 5. Kiến trúc và thiết kế hệ thống

### 5.1. Kiến trúc tổng quan

Dự án sử dụng kiến trúc 3 lớp:

```text
Frontend / Web Interface
          |
          v
Backend API / Business Logic
          |
          v
Database / Smart CRM Data
```

### 5.2. Frontend

Frontend dự kiến cung cấp giao diện để quản lý trung tâm và kỹ thuật viên thực hiện các thao tác thuộc luồng L4.

Trong Buổi 8, Frontend chưa được triển khai.

### 5.3. Backend

Backend sử dụng FastAPI và được tổ chức theo các thành phần:

- **API / Routes:** Tiếp nhận HTTP Request và trả về HTTP Response.
- **Services:** Kiểm tra dữ liệu và xử lý logic nghiệp vụ.
- **Repositories:** Truy vấn và cập nhật dữ liệu SQLite.
- **Models:** Thư mục dành cho các mô hình dữ liệu.

Luồng xử lý:

```text
HTTP Request
     |
     v
API / Routes
     |
     v
Service / Business Logic
     |
     v
Repository
     |
     v
SQLite Database
```

### 5.4. Database

Database được thiết kế cho luồng L4 với 5 bảng:

- `ticket`: Thông tin phiếu cần xử lý.
- `technician`: Thông tin kỹ thuật viên.
- `technician_skill`: Kỹ năng và mức độ thành thạo.
- `assignment`: Lịch sử phân công kỹ thuật viên.
- `appointment`: Lịch giao – nhận máy.

Các ràng buộc quan trọng trong thiết kế:

- Một Ticket có tối đa một Assignment đang hoạt động.
- Kỹ thuật viên cần có mức proficiency từ 3 trở lên đối với nhóm sự cố.
- Kỹ thuật viên phải thuộc cùng trung tâm với Ticket.
- Ticket cần ở trạng thái `PENDING` và chưa có phân công đang hoạt động trước khi phân công mới.

Các quy tắc phân công và lịch hẹn thuộc phạm vi thiết kế L4, chưa được triển khai đầy đủ trong Backend Buổi 8.

---

## 6. Trạng thái triển khai Buổi 8

### 6.1. Các công việc đã hoàn thành

**Phân tích và điều chỉnh thiết kế**

- Đã xem xét phản hồi BT1.
- Đã tạo tài liệu `docs/thay-doi-thiet-ke.md` để ghi nhận quyết định sửa đổi.
- Đã xác định các nội dung thiết kế cần tiếp tục hoàn thiện.

**Cấu trúc mã nguồn**

- Đã tạo cấu trúc Backend theo các lớp API, Service và Repository.
- Đã kết nối Ticket Router với ứng dụng FastAPI.

**Cơ sở dữ liệu**

- Đã khởi tạo SQLite từ `docs/schema.sql`.
- Đã tạo thành công 5 bảng dữ liệu.
- Đã kiểm tra ràng buộc khóa ngoại.

**Module Ticket CRUD**

Đã triển khai các thao tác:

- Xem danh sách Ticket.
- Xem chi tiết Ticket.
- Tạo Ticket.
- Cập nhật Ticket.
- Xóa Ticket.

**Kiểm thử API**

Đã kiểm thử thành công các trường hợp:

| Test Case | Kết quả mong đợi | Kết quả |
|---|---|---|
| GET `/tickets` | HTTP 200 | PASS |
| POST `/tickets` với tiêu đề rỗng | HTTP 400 | PASS |
| POST `/tickets` với dữ liệu hợp lệ | HTTP 201 | PASS |

**Tổng kết: 3/3 bài kiểm thử đã thực hiện thành công.**

Minh chứng được lưu tại:

`docs/minh-chung-api-buoi8.txt`

### 6.2. Các công việc chưa hoàn thành

- Hoàn thiện toàn bộ các điều chỉnh tài liệu và sơ đồ theo phản hồi BT1.
- Tạo dữ liệu mẫu kỹ thuật viên và kỹ năng.
- Xây dựng module phân công kỹ thuật viên.
- Kiểm tra đầy đủ Business Rules của luồng L4.
- Xây dựng module lịch hẹn và kiểm tra xung đột lịch.
- Triển khai Frontend.
- Bổ sung unit test cho Business Logic.
- Kiểm thử đầy đủ các trường hợp cập nhật và xóa Ticket.

### 6.3. Định hướng triển khai tiếp theo

Trong các buổi tiếp theo, dự án sẽ tiếp tục:

1. Hoàn thiện dữ liệu mẫu và các tài liệu thiết kế cần điều chỉnh.
2. Xây dựng module Technician.
3. Xây dựng chức năng Assignment theo Business Rules.
4. Xây dựng chức năng Appointment và kiểm tra trùng lịch.
5. Bổ sung unit test và minh chứng kiểm thử.

---

## 7. Cấu trúc thư mục

```text
smart-crm/
├── docs/
│   ├── ai-disclosure.md
│   ├── api-contract.md
│   ├── architecture.md
│   ├── architecture.drawio
│   ├── architecture.png
│   ├── erd.drawio
│   ├── erd.png
│   ├── schema.sql
│   ├── srs.md
│   ├── usecase-spec.md
│   ├── usecase.drawio
│   ├── usecase.png
│   ├── wireframe.drawio
│   ├── wireframe.png
│   ├── thay-doi-thiet-ke.md
│   └── minh-chung-api-buoi8.txt
├── src/
│   ├── __init__.py
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── ticket_api.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── ticket_service.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   └── ticket_repository.py
│   │   └── models/
│   │       └── __init__.py
│   └── frontend/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

File `smartcrm.db` được tạo trong quá trình khởi tạo và sử dụng SQLite.

---

## 8. Khai báo sử dụng công cụ AI

| Công cụ | Mục đích sử dụng | Cách kiểm tra / chỉnh sửa |
|---|---|---|
| ChatGPT | Hỗ trợ phân tích yêu cầu, xây dựng tài liệu SRS, User Stories, Acceptance Criteria, Use Case Specification, Architecture, Data Model, SQL DDL, API Contract và hỗ trợ triển khai Backend | Đối chiếu với yêu cầu bài tập, kiểm tra mã nguồn, thực thi lệnh và kiểm thử API |
| Draw.io AI | Hỗ trợ xây dựng Architecture Diagram, ERD và Wireframe | Kiểm tra thành phần, quan hệ, PK/FK, bố cục và tính nhất quán với SRS |

Sinh viên chịu trách nhiệm rà soát, kiểm chứng và điều chỉnh nội dung trước khi sử dụng.

Chi tiết được trình bày tại:

`docs/ai-disclosure.md`

---

## 9. Ghi chú

Dự án Smart CRM – Mekong Mobile tập trung vào luồng nghiệp vụ L4: Phân công kỹ thuật viên và lịch hẹn.

BT1 tập trung vào phân tích và thiết kế hệ thống. Từ Buổi 8, dự án bắt đầu triển khai Backend và cơ sở dữ liệu theo thiết kế đã xây dựng.

Tại thời điểm cập nhật README, module Ticket CRUD đã được xây dựng và kiểm thử một số trường hợp cơ bản. Các chức năng nghiệp vụ chính của L4 sẽ tiếp tục được triển khai trong những buổi tiếp theo.
