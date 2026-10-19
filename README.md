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

Ở giai đoạn Buổi 8, dự án tập trung triển khai Backend, cơ sở dữ liệu, Ticket CRUD và chức năng phân công kỹ thuật viên cơ bản.

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
| API Testing | FastAPI TestClient, Swagger UI |

### 2.2. Cấu hình môi trường

Yêu cầu máy tính đã cài đặt Python 3.12, Git và SQLite. Khuyến nghị sử dụng Visual Studio Code để chỉnh sửa mã nguồn.

Clone repository nếu chưa có dự án:

```bash
git clone https://github.com/Tringuyen2374802010517/smart-crm.git
cd smart-crm
git switch dev
```

Nếu đã có dự án trên máy Mac đang sử dụng:

```bash
cd ~/Downloads/smart-crm
```

Tạo môi trường Python ảo:

```bash
python3.12 -m venv .venv
```

Cài đặt thư viện:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Để chạy các ví dụ kiểm thử sử dụng `TestClient`, môi trường hiện tại cần thư viện `httpx2`. Nếu chưa có trong `requirements.txt`, cài bổ sung:

```bash
.venv/bin/python -m pip install httpx2==2.14.0
```

**Lưu ý:** Cần cập nhật `requirements.txt` để các môi trường mới có thể cài đặt đầy đủ thư viện kiểm thử bằng một lệnh.

### 2.3. Khởi tạo cơ sở dữ liệu

Dự án sử dụng SQLite với 5 bảng chính:

1. `ticket` – Lưu thông tin phiếu.
2. `technician` – Lưu thông tin kỹ thuật viên.
3. `technician_skill` – Lưu kỹ năng và mức độ thành thạo.
4. `assignment` – Lưu lịch sử phân công kỹ thuật viên.
5. `appointment` – Lưu thông tin lịch giao – nhận máy.

Khởi tạo cơ sở dữ liệu mới:

```bash
sqlite3 smartcrm.db < docs/schema.sql
```

**Lưu ý:** Chỉ thực hiện lệnh này trên database mới chưa có bảng. Không chạy lại trực tiếp trên database đã được khởi tạo.

Kiểm tra danh sách bảng:

```bash
sqlite3 smartcrm.db ".tables"
```

Kiểm tra khóa ngoại:

```bash
sqlite3 smartcrm.db "PRAGMA foreign_key_check;"
```

Database đã được sử dụng trong quá trình phát triển để tạo dữ liệu mẫu Ticket, Technician, Technician Skill và Assignment.

Dữ liệu mẫu hiện tại được lưu cục bộ trong `smartcrm.db`, chưa có script seed riêng để tự động tạo lại trên máy khác.

### 2.4. Khởi chạy Backend

Từ thư mục gốc dự án, chạy:

```bash
.venv/bin/python -m uvicorn src.backend.main:app --host 127.0.0.1 --port 8000
```

Sau khi Backend khởi chạy, truy cập:

- API Documentation: http://127.0.0.1:8000/docs
- Kiểm tra database: http://127.0.0.1:8000/db-check
- Danh sách Ticket: http://127.0.0.1:8000/tickets

Có thể sử dụng Swagger UI để xem các endpoint và gửi yêu cầu kiểm thử.

### 2.5. Danh sách API đã triển khai

**Ticket API**

| Method | Endpoint | Chức năng |
|---|---|---|
| GET | `/tickets` | Xem danh sách Ticket |
| GET | `/tickets/{ticket_id}` | Xem chi tiết Ticket |
| POST | `/tickets` | Tạo Ticket mới |
| PUT | `/tickets/{ticket_id}` | Cập nhật Ticket |
| DELETE | `/tickets/{ticket_id}` | Xóa Ticket |

**Assignment API**

| Method | Endpoint | Chức năng |
|---|---|---|
| GET | `/assignments/eligible-technicians/{ticket_id}` | Xem kỹ thuật viên đủ điều kiện phân công |
| POST | `/assignments/` | Phân công kỹ thuật viên cho Ticket |

### 2.6. Ví dụ sử dụng API

**Tạo Ticket**

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

**Xem kỹ thuật viên đủ điều kiện**

```bash
curl http://127.0.0.1:8000/assignments/eligible-technicians/1
```

Trong ví dụ này, `1` là mã Ticket. API chỉ trả về danh sách kỹ thuật viên nếu Ticket tồn tại, đang ở trạng thái `PENDING` và chưa có phân công đang hoạt động.

**Phân công kỹ thuật viên**

```bash
curl -X POST http://127.0.0.1:8000/assignments/ \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": 1,
    "technician_id": 1
  }'
```

**Lưu ý:** Các ví dụ Assignment yêu cầu database đã có dữ liệu Ticket, Technician và Technician Skill phù hợp. Nếu Ticket đã được phân công, hệ thống sẽ từ chối tạo phân công trùng.

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

Đây là phạm vi nghiệp vụ của dự án; không phải tất cả chức năng đã được triển khai ở Buổi 8.

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
| `minh-chung-api-buoi8.txt` | Minh chứng kiểm thử Ticket API |
| `minh-chung-phan-cong-buoi8.txt` | Minh chứng Assignment, SQLite và danh sách API |

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

Trong Buổi 8, Backend và Database đã được triển khai. Frontend hiện vẫn ở giai đoạn thiết kế.

### 5.2. Frontend

Frontend dự kiến cung cấp giao diện để quản lý trung tâm và kỹ thuật viên thực hiện các thao tác thuộc luồng L4.

Các màn hình được thiết kế trong tài liệu Wireframe nhưng chưa triển khai thành giao diện hoạt động.

### 5.3. Backend

Backend sử dụng FastAPI và được tổ chức theo các thành phần:

- **API / Routes:** Tiếp nhận HTTP Request và trả về HTTP Response.
- **Services:** Kiểm tra dữ liệu và xử lý logic nghiệp vụ.
- **Repositories:** Truy vấn và cập nhật dữ liệu SQLite.
- **Models:** Thư mục dành cho các mô hình dữ liệu, chưa triển khai thành module riêng.

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

Các quy tắc phân công đã được triển khai:

- Một Ticket chỉ có tối đa một Assignment đang hoạt động.
- Kỹ thuật viên phải có mức proficiency từ 3 trở lên đối với nhóm sự cố.
- Kỹ thuật viên phải thuộc cùng trung tâm với Ticket.
- Kỹ thuật viên phải có trạng thái `AVAILABLE`.
- Ticket phải ở trạng thái `PENDING` và chưa có phân công đang hoạt động.
- Khối lượng công việc hiện tại được tính bằng số Assignment chưa kết thúc.

Các quy tắc thay đổi kỹ thuật viên và kiểm tra trùng lịch vẫn cần tiếp tục triển khai.

---

## 6. Trạng thái triển khai Buổi 8

### 6.1. Các công việc đã hoàn thành

**Phân tích và điều chỉnh thiết kế**

- Đã xem xét phản hồi BT1.
- Đã tạo tài liệu `docs/thay-doi-thiet-ke.md` để ghi nhận các quyết định điều chỉnh.
- Đã xác định những nội dung tài liệu và sơ đồ cần tiếp tục hoàn thiện.

**Cấu trúc mã nguồn**

- Đã tổ chức Backend theo kiến trúc API / Routes → Service → Repository → SQLite.
- Đã kết nối Ticket Router và Assignment Router với ứng dụng FastAPI.
- Đã kiểm tra các endpoint được đăng ký trong OpenAPI.

**Cơ sở dữ liệu**

- Đã khởi tạo SQLite từ `docs/schema.sql`.
- Đã tạo thành công 5 bảng dữ liệu.
- Đã tạo dữ liệu mẫu Ticket, Technician và Technician Skill.
- Đã kiểm tra ràng buộc khóa ngoại.
- Đã kiểm tra dữ liệu Assignment được lưu vào SQLite.

**Module Ticket CRUD**

Đã triển khai các chức năng:

- Xem danh sách Ticket.
- Xem chi tiết Ticket.
- Tạo Ticket.
- Cập nhật Ticket.
- Xóa Ticket.

**Module phân công kỹ thuật viên**

Đã triển khai:

- Xem danh sách kỹ thuật viên đủ điều kiện phân công.
- Phân công kỹ thuật viên cho Ticket.
- Kiểm tra trạng thái `PENDING` của Ticket.
- Kiểm tra kỹ thuật viên cùng trung tâm.
- Kiểm tra trạng thái `AVAILABLE`.
- Kiểm tra proficiency từ 3 trở lên.
- Ngăn phân công trùng cho một Ticket.
- Tính `current_workload` từ các Assignment đang hoạt động.

**Kiểm thử API**

Các trường hợp đã kiểm thử:

| Test Case | Kết quả mong đợi | Kết quả |
|---|---|---|
| GET `/tickets` | HTTP 200 | PASS |
| POST `/tickets` với tiêu đề rỗng | HTTP 400 | PASS |
| POST `/tickets` với dữ liệu hợp lệ | HTTP 201 | PASS |
| GET kỹ thuật viên đủ điều kiện cho Ticket chưa phân công | HTTP 200 | PASS |
| POST Assignment hợp lệ | HTTP 201 | PASS |
| POST Assignment với kỹ thuật viên không khả dụng | HTTP 400 | PASS |
| POST Assignment với kỹ thuật viên khác trung tâm | HTTP 400 | PASS |
| POST Assignment trùng Ticket | HTTP 400 | PASS |
| GET kỹ thuật viên đủ điều kiện cho Ticket đã phân công | HTTP 400 | PASS |

**Tổng kết: 9/9 trường hợp kiểm thử API đã thực hiện thành công.**

Đây là kết quả kiểm thử thủ công thông qua FastAPI TestClient, chưa phải bộ unit test tự động hoàn chỉnh.

Ngoài ra, đã kiểm tra dữ liệu phân công trong SQLite và xác nhận không có lỗi khóa ngoại trong cơ sở dữ liệu hiện tại.

Minh chứng được lưu tại:

- `docs/minh-chung-api-buoi8.txt`
- `docs/minh-chung-phan-cong-buoi8.txt`

### 6.2. Các công việc chưa hoàn thành

- Hoàn thiện toàn bộ các điều chỉnh tài liệu và sơ đồ theo phản hồi BT1.
- Kiểm thử đầy đủ các trường hợp cập nhật và xóa Ticket.
- Hoàn thiện các Business Rules còn lại của luồng L4.
- Xây dựng chức năng thay đổi kỹ thuật viên và ghi nhận lý do.
- Xây dựng module lịch hẹn và kiểm tra xung đột lịch.
- Triển khai Frontend.
- Bổ sung unit test tự động cho Business Logic.
- Bổ sung script seed dữ liệu để dễ dàng tái tạo môi trường trên máy khác.

### 6.3. Định hướng triển khai tiếp theo

Trong các buổi tiếp theo, dự án sẽ tiếp tục:

1. Hoàn thiện các tài liệu thiết kế cần điều chỉnh theo phản hồi BT1.
2. Bổ sung unit test cho các Business Rules.
3. Xây dựng chức năng thay đổi kỹ thuật viên phụ trách.
4. Xây dựng module Appointment và kiểm tra trùng lịch.
5. Hoàn thiện dữ liệu mẫu, Frontend và kiểm thử hệ thống.

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
│   ├── minh-chung-api-buoi8.txt
│   └── minh-chung-phan-cong-buoi8.txt
├── src/
│   ├── __init__.py
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── ticket_api.py
│   │   │   └── assignment_api.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ticket_service.py
│   │   │   └── assignment_service.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── ticket_repository.py
│   │   │   └── assignment_repository.py
│   │   └── models/
│   │       └── __init__.py
│   └── frontend/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

File `smartcrm.db` được tạo trong quá trình phát triển và lưu tại máy cục bộ, không đưa lên GitHub.

---

## 8. Khai báo sử dụng công cụ AI

| Công cụ | Mục đích sử dụng | Cách kiểm tra / chỉnh sửa |
|---|---|---|
| ChatGPT | Hỗ trợ phân tích yêu cầu, xây dựng tài liệu SRS, User Stories, Acceptance Criteria, Use Case Specification, Architecture, Data Model, SQL DDL, API Contract và triển khai Backend | Đối chiếu với yêu cầu bài tập, kiểm tra mã nguồn, thực thi lệnh và kiểm thử API |
| Draw.io AI | Hỗ trợ xây dựng Architecture Diagram, ERD và Wireframe | Kiểm tra thành phần, quan hệ, PK/FK, bố cục và tính nhất quán với SRS |

Sinh viên chịu trách nhiệm rà soát, kiểm chứng và điều chỉnh nội dung trước khi sử dụng.

Chi tiết được trình bày tại:

`docs/ai-disclosure.md`

---

## 9. Ghi chú

Dự án Smart CRM – Mekong Mobile tập trung vào luồng nghiệp vụ L4: Phân công kỹ thuật viên và lịch hẹn.

BT1 tập trung vào phân tích và thiết kế hệ thống. Từ Buổi 8, dự án bắt đầu triển khai Backend và cơ sở dữ liệu theo thiết kế đã xây dựng.

Tại thời điểm cập nhật README, dự án đã triển khai module Ticket CRUD và chức năng phân công kỹ thuật viên cơ bản, bao gồm kiểm tra điều kiện nghiệp vụ, xử lý REST API và lưu dữ liệu vào SQLite.

Các chức năng thay đổi kỹ thuật viên, quản lý lịch hẹn, kiểm tra trùng lịch và Frontend sẽ tiếp tục được phát triển trong các giai đoạn tiếp theo.