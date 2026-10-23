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

Trong luồng nghiệp vụ L4, quản lý trung tâm cần phân công kỹ thuật viên cho các phiếu dựa trên tay nghề, địa bàn, trạng thái khả dụng và khối lượng công việc hiện tại. Đồng thời, hệ thống được thiết kế để hỗ trợ đặt lịch giao – nhận máy và kiểm tra xung đột lịch hẹn.

Mục tiêu của dự án là xây dựng các chức năng cốt lõi của luồng L4 dựa trên tài liệu phân tích và thiết kế đã thực hiện trong BT1.

Ở giai đoạn Buổi 8, dự án tập trung triển khai Backend, cơ sở dữ liệu, Ticket CRUD và chức năng phân công kỹ thuật viên cơ bản.

Đến Buổi 10, dự án đã bổ sung Frontend kết nối REST API, dữ liệu mẫu có thể tái tạo, unit tests cho business logic và các trạng thái giao diện cần thiết.

---

## 2. Công nghệ và môi trường

### 2.1. Công nghệ sử dụng

| Thành phần | Công nghệ / Công cụ |
|---|---|
| Ngôn ngữ Backend | Python 3.12 |
| Backend Framework | FastAPI |
| Frontend | JavaScript, HTML, CSS, Vite |
| Database | SQLite |
| API | REST API |
| Unit Testing | pytest |
| API Testing | FastAPI TestClient, Swagger UI |
| Version Control | Git, GitHub |
| Development Tool | Visual Studio Code |
| Diagram / Wireframe | Draw.io |

### 2.2. Môi trường phát triển đã kiểm thử

- Python 3.12.2
- Node.js v24.12.0
- npm 11.6.2
- FastAPI 0.141.1
- Vite 8.3.5 (phiên bản thực tế khi build)
- pytest 9.1.1
- SQLite 3
- macOS

Các dependencies Python được khai báo trong `requirements.txt`.

Các dependencies Frontend được khai báo trong `src/frontend/package.json` và `src/frontend/package-lock.json`.

### 2.3. Cấu trúc kiến trúc

Dự án được tổ chức theo kiến trúc 3 lớp:

```text
Frontend (HTML / CSS / JavaScript / Vite)
                  |
                  | HTTP / REST API
                  v
Backend (FastAPI)
                  |
          API / Routes
                  |
          Service / Business Logic
                  |
             Repository
                  |
                  v
           SQLite Database
```

Backend tách biệt việc tiếp nhận HTTP Request, kiểm tra Business Rules và truy vấn dữ liệu.

Frontend sử dụng REST API để lấy dữ liệu Ticket, hiển thị kỹ thuật viên phù hợp và gửi yêu cầu phân công.

---

## 3. Hướng dẫn Clone, Run và Test

### 3.1. Yêu cầu môi trường

Máy tính cần có:

- Python 3.12
- Node.js tương thích với Vite 8, khuyến nghị Node.js 24
- npm
- Git
- SQLite 3

Các lệnh bên dưới được viết cho macOS/Linux.

### 3.2. Clone repository

```bash
git clone https://github.com/Tringuyen2374802010517/smart-crm.git
cd smart-crm
git switch dev
```

Nếu đã có repository trên máy phát triển:

```bash
cd ~/Downloads/smart-crm
```

### 3.3. Tạo môi trường Python

Tại thư mục gốc dự án:

```bash
python3.12 -m venv .venv
```

Cài đặt dependencies:

```bash
.venv/bin/python3 -m pip install -r requirements.txt
```

Các thư viện phục vụ kiểm thử như `pytest` và `httpx` đã được bổ sung vào `requirements.txt`.

### 3.4. Khởi tạo cơ sở dữ liệu

Dự án sử dụng SQLite với 5 bảng:

1. `ticket` – Thông tin phiếu cần xử lý.
2. `technician` – Thông tin kỹ thuật viên.
3. `technician_skill` – Kỹ năng và mức độ thành thạo.
4. `assignment` – Lịch sử phân công kỹ thuật viên.
5. `appointment` – Thông tin lịch giao – nhận máy.

Trên database mới, chạy:

```bash
sqlite3 smartcrm.db < docs/schema.sql
```

Sau đó tạo dữ liệu mẫu:

```bash
sqlite3 smartcrm.db < docs/seed.sql
```

**Lưu ý:** Chỉ chạy các lệnh khởi tạo trên database mới. Không chạy lại script seed trên database đang có dữ liệu trùng khóa chính.

Script `docs/seed.sql` tạo:

- 3 Ticket mẫu.
- 3 kỹ thuật viên.
- 3 bản ghi kỹ năng.

Dữ liệu mẫu có các trường hợp kỹ thuật viên khả dụng, không khả dụng, khác trung tâm và không đủ mức độ thành thạo để kiểm thử Business Rules.

Kiểm tra các bảng:

```bash
sqlite3 smartcrm.db ".tables"
```

Kiểm tra khóa ngoại:

```bash
sqlite3 smartcrm.db "PRAGMA foreign_key_check;"
```

Nếu không có dòng lỗi nào được trả về thì kiểm tra khóa ngoại đạt yêu cầu.

File `smartcrm.db` được tạo cục bộ và không đưa lên GitHub.

### 3.5. Khởi chạy Backend

Tại thư mục gốc dự án:

```bash
.venv/bin/python3 -m uvicorn src.backend.main:app --reload --host 127.0.0.1 --port 8000
```

Sau khi Backend khởi chạy, truy cập:

- Swagger UI: http://127.0.0.1:8000/docs
- Kiểm tra database: http://127.0.0.1:8000/db-check
- Danh sách Ticket: http://127.0.0.1:8000/tickets

Giữ Terminal Backend hoạt động trong quá trình sử dụng Frontend.

### 3.6. Khởi chạy Frontend

Mở Terminal thứ hai tại thư mục gốc dự án.

Cài đặt dependencies Frontend:

```bash
cd src/frontend
npm ci
```

Khởi chạy Vite:

```bash
npm run dev
```

Truy cập địa chỉ được Vite hiển thị trên Terminal, thông thường:

http://localhost:5173

Frontend gửi yêu cầu đến Backend đang chạy tại `http://127.0.0.1:8000`.

### 3.7. Chạy unit tests

Mở Terminal tại thư mục gốc dự án:

```bash
.venv/bin/python3 -m pytest tests/test_assignment_service.py -v
```

Kết quả kiểm thử đã ghi nhận trên môi trường phát triển:

**9 passed**

Bộ unit tests kiểm tra các trường hợp:

1. Phân công kỹ thuật viên thành công.
2. Không tìm thấy Ticket.
3. Ticket không ở trạng thái PENDING.
4. Ticket đã có phân công đang hoạt động.
5. Kỹ thuật viên khác trung tâm.
6. Kỹ thuật viên không khả dụng.
7. Kỹ thuật viên không đủ kỹ năng.
8. Không có kỹ thuật viên phù hợp (boundary case).
9. Không tìm thấy kỹ thuật viên.

Các unit tests sử dụng mock repository để kiểm tra business logic, không trực tiếp thay đổi database SQLite.

Minh chứng kết quả kiểm thử:

`docs/unit-test-results.txt`

### 3.8. Build Frontend

Tại thư mục gốc dự án:

```bash
npm --prefix src/frontend run build
```

Kết quả đã kiểm thử trên môi trường phát triển:

- Vite 8.3.5
- 9 modules transformed
- Build thành công trong 809 ms

Thư mục `dist/` được tạo khi build và được loại trừ khỏi Git.

### 3.9. Kiểm tra trên môi trường mới

Quy trình kiểm tra fresh clone cần xác nhận:

- Clone repository thành công.
- Cài đặt Python dependencies thành công.
- Cài đặt Frontend dependencies thành công.
- Tạo database và seed dữ liệu thành công.
- Backend khởi chạy thành công.
- Frontend kết nối được API.
- Unit tests chạy thành công.

**Trạng thái:** Đã kiểm tra riêng schema, seed, Frontend build và unit tests trên môi trường phát triển. Kiểm thử fresh clone hoàn chỉnh cần được thực hiện trước khi nộp bài.

---

## 4. Phạm vi

### 4.1. Trong phạm vi

Các chức năng thuộc luồng L4 bao gồm:

- Xem danh sách các phiếu cần phân công.
- Xem danh sách kỹ thuật viên khả dụng.
- Kiểm tra tay nghề, trung tâm và trạng thái khả dụng của kỹ thuật viên.
- Phân công kỹ thuật viên cho phiếu.
- Thay đổi kỹ thuật viên phụ trách và ghi nhận lý do.
- Đặt lịch giao – nhận máy.
- Kiểm tra xung đột lịch trước khi xác nhận.
- Cho phép kỹ thuật viên xem các phiếu và lịch hẹn được giao.

Đây là phạm vi nghiệp vụ tổng thể của luồng L4. Không phải tất cả chức năng đã được triển khai trong phiên bản Buổi 10.

### 4.2. Ngoài phạm vi

Dự án không tập trung triển khai:

- Tiếp nhận và phân loại toàn bộ yêu cầu bảo hành.
- Quản lý kho linh kiện.
- Quản lý thanh toán và hóa đơn.
- Xử lý toàn bộ quy trình sửa chữa thiết bị.
- Chức năng đăng nhập và phân quyền chi tiết.
- Các luồng nghiệp vụ khác ngoài L4.
- Triển khai hệ thống trong môi trường vận hành thực tế.

---

## 5. Tài liệu phân tích và thiết kế BT1

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
| `seed.sql` | Dữ liệu mẫu phục vụ demo và kiểm thử |
| `wireframe.drawio` | Source Wireframe |
| `wireframe.png` | Wireframe các màn hình |
| `api-contract.md` | API Contract dành cho track SE |
| `ai-disclosure.md` | Khai báo sử dụng công cụ AI |
| `thay-doi-thiet-ke.md` | Ghi nhận phản hồi BT1 và quyết định điều chỉnh thiết kế |
| `minh-chung-api-buoi8.txt` | Minh chứng kiểm thử Ticket API |
| `minh-chung-phan-cong-buoi8.txt` | Minh chứng Assignment, SQLite và danh sách API |
| `unit-test-results.txt` | Kết quả 9 unit tests Buổi 10 |

Báo cáo BT1 được lưu tại:

`docs/CDTN1_Buoi6_2374802010517_NguyenMinhTri.pdf`

---

## 6. Backend và Business Rules

### 6.1. Ticket API

| Method | Endpoint | Chức năng |
|---|---|---|
| GET | `/tickets` | Xem danh sách Ticket |
| GET | `/tickets/{ticket_id}` | Xem chi tiết Ticket |
| POST | `/tickets` | Tạo Ticket mới |
| PUT | `/tickets/{ticket_id}` | Cập nhật Ticket |
| DELETE | `/tickets/{ticket_id}` | Xóa Ticket |

Ticket mới được tạo với trạng thái mặc định `PENDING`.

Các mức ưu tiên hợp lệ:

- `CAO`
- `TRUNG_BINH`
- `THAP`

Ví dụ tạo Ticket:

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

### 6.2. Assignment API

| Method | Endpoint | Chức năng |
|---|---|---|
| GET | `/assignments/eligible-technicians/{ticket_id}` | Xem kỹ thuật viên đủ điều kiện phân công |
| POST | `/assignments/` | Phân công kỹ thuật viên cho Ticket |

Ví dụ lấy danh sách kỹ thuật viên phù hợp:

```bash
curl http://127.0.0.1:8000/assignments/eligible-technicians/1
```

Ví dụ phân công:

```bash
curl -X POST http://127.0.0.1:8000/assignments/ \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": 1,
    "technician_id": 1
  }'
```

Các ví dụ Assignment yêu cầu database có dữ liệu phù hợp và Ticket chưa được phân công.

### 6.3. Business Rules đã triển khai

**BR1 – Giới hạn phân công đang hoạt động**

- Mỗi Ticket chỉ có tối đa một Assignment đang hoạt động.
- Assignment đang hoạt động có `ended_at IS NULL`.
- SQLite sử dụng unique index để hỗ trợ ngăn phân công trùng.

**BR2 – Điều kiện kỹ thuật viên**

Kỹ thuật viên phải:

- Thuộc cùng trung tâm với Ticket.
- Có trạng thái `AVAILABLE`.
- Có kỹ năng phù hợp với `incident_group`.
- Có `proficiency >= 3`.

**Điều kiện trạng thái Ticket**

- Ticket phải ở trạng thái `PENDING`.
- Ticket chưa có Assignment đang hoạt động.

**Khối lượng công việc**

- `current_workload` được tính từ số Assignment đang hoạt động của kỹ thuật viên.
- Danh sách kỹ thuật viên phù hợp được sắp xếp theo khối lượng công việc tăng dần.

### 6.4. Business Rules chưa hoàn thiện

Các chức năng sau vẫn cần tiếp tục phát triển:

- Thay đổi kỹ thuật viên phụ trách và ghi nhận lý do.
- Quản lý lịch giao – nhận máy.
- Kiểm tra xung đột lịch hẹn.
- Hoàn thiện các quy tắc SLA và vòng đời trạng thái theo SRS.

Bảng `appointment` đã được thiết kế trong database nhưng chưa có API quản lý lịch hẹn hoàn chỉnh.

---

## 7. Trạng thái triển khai Buổi 8

### 7.1. Các công việc đã hoàn thành tại Buổi 8

**Phân tích và điều chỉnh thiết kế**

- Đã xem xét phản hồi BT1.
- Đã tạo `docs/thay-doi-thiet-ke.md`.
- Đã xác định các nội dung tài liệu và sơ đồ cần tiếp tục hoàn thiện.

**Cấu trúc mã nguồn**

- Đã tổ chức Backend theo kiến trúc API / Routes → Service → Repository → SQLite.
- Đã kết nối Ticket Router và Assignment Router với ứng dụng FastAPI.
- Đã kiểm tra các endpoint được đăng ký trong OpenAPI.

**Cơ sở dữ liệu**

- Đã khởi tạo SQLite từ `docs/schema.sql`.
- Đã tạo 5 bảng dữ liệu.
- Đã tạo dữ liệu mẫu Ticket, Technician và Technician Skill trên môi trường phát triển.
- Đã kiểm tra ràng buộc khóa ngoại.
- Đã kiểm tra dữ liệu Assignment được lưu vào SQLite.

**Module Ticket CRUD**

- Xem danh sách Ticket.
- Xem chi tiết Ticket.
- Tạo Ticket.
- Cập nhật Ticket.
- Xóa Ticket.

**Module phân công kỹ thuật viên**

- Xem danh sách kỹ thuật viên đủ điều kiện.
- Phân công kỹ thuật viên cho Ticket.
- Kiểm tra trạng thái PENDING.
- Kiểm tra cùng trung tâm.
- Kiểm tra AVAILABLE.
- Kiểm tra proficiency từ 3 trở lên.
- Ngăn phân công trùng.
- Tính current_workload.

### 7.2. Kết quả kiểm thử API Buổi 8

| Test Case | Kết quả mong đợi | Kết quả |
|---|---|---|
| GET `/tickets` | HTTP 200 | PASS |
| POST `/tickets` với tiêu đề rỗng | HTTP 400 | PASS |
| POST `/tickets` với dữ liệu hợp lệ | HTTP 201 | PASS |
| GET kỹ thuật viên phù hợp cho Ticket chưa phân công | HTTP 200 | PASS |
| POST Assignment hợp lệ | HTTP 201 | PASS |
| POST Assignment với kỹ thuật viên không khả dụng | HTTP 400 | PASS |
| POST Assignment với kỹ thuật viên khác trung tâm | HTTP 400 | PASS |
| POST Assignment trùng Ticket | HTTP 400 | PASS |
| GET kỹ thuật viên phù hợp cho Ticket đã phân công | HTTP 400 | PASS |

**Tổng kết Buổi 8: 9/9 trường hợp kiểm thử API đã thực hiện thành công.**

Đây là kết quả kiểm thử API được ghi nhận tại Buổi 8, khác với bộ 9 unit tests tự động được bổ sung tại Buổi 10.

Minh chứng:

- `docs/minh-chung-api-buoi8.txt`
- `docs/minh-chung-phan-cong-buoi8.txt`

### 7.3. Hạn chế tại thời điểm Buổi 8

- Frontend chưa được triển khai.
- Chưa có bộ unit tests tự động hoàn chỉnh.
- Chưa có script seed dữ liệu riêng.
- Chưa hoàn thiện chức năng thay đổi kỹ thuật viên.
- Chưa triển khai module lịch hẹn.

Các mục Frontend, unit tests và seed dữ liệu đã được bổ sung trong quá trình thực hiện Buổi 10.

---

## 8. Trạng thái triển khai Buổi 10

### 8.1. Frontend

Đã triển khai giao diện Frontend bằng JavaScript và Vite, kết nối Backend thông qua REST API.

Các chức năng giao diện đã thực hiện:

- Hiển thị danh sách Ticket.
- Xem thông tin chi tiết Ticket.
- Mở giao diện phân công kỹ thuật viên.
- Hiển thị danh sách kỹ thuật viên phù hợp từ API.
- Gửi yêu cầu phân công kỹ thuật viên.
- Hiển thị thông báo sau khi phân công thành công.
- Vô hiệu hóa nút phân công đối với Ticket đã được phân công.

Frontend có xử lý các trạng thái:

- Loading – Đang tải dữ liệu.
- Empty – Không có dữ liệu phù hợp.
- Error – Không thể tải hoặc xử lý yêu cầu.

Đã kiểm tra luồng hiển thị Ticket và phân công kỹ thuật viên trên môi trường phát triển.

### 8.2. Tích hợp Frontend – Backend – Database

Luồng chính đã được kiểm tra:

```text
Mở Frontend
      |
      v
Xem danh sách Ticket
      |
      v
Chọn Ticket chưa phân công
      |
      v
Xem kỹ thuật viên phù hợp
      |
      v
Chọn kỹ thuật viên
      |
      v
Gửi POST /assignments/
      |
      v
Backend kiểm tra Business Rules
      |
      v
Lưu Assignment vào SQLite
      |
      v
Hiển thị thông báo thành công
```

Đã xác nhận Assignment được lưu trong SQLite và API từ chối phân công trùng.

### 8.3. Dữ liệu mẫu

Đã tạo file:

`docs/seed.sql`

Script đã được kiểm tra trên database tạm riêng, không ảnh hưởng database phát triển hiện tại.

Kết quả:

| Bảng | Số bản ghi | Kết quả |
|---|---:|---|
| ticket | 3 | PASS |
| technician | 3 | PASS |
| technician_skill | 3 | PASS |
| Kiểm tra khóa ngoại | Không có lỗi | PASS |

### 8.4. Unit tests

Đã tạo:

`tests/test_assignment_service.py`

Bộ kiểm thử sử dụng pytest và monkeypatch để kiểm tra business logic của Assignment Service.

Kết quả:

**9/9 unit tests PASSED**

Bao gồm trường hợp biên khi không có kỹ thuật viên đủ điều kiện.

Minh chứng:

`docs/unit-test-results.txt`

### 8.5. Frontend build

Đã chạy:

```bash
npm --prefix src/frontend run build
```

Kết quả:

- Vite 8.3.5
- 9 modules transformed
- Build thành công

### 8.6. Các hạng mục cần kiểm tra trước khi nộp

- Hoàn thiện và kiểm tra ảnh chụp màn hình minh chứng trong `docs/`.
- Kiểm thử fresh clone đầy đủ.
- Kiểm tra README khớp với mã nguồn và tài liệu thiết kế.
- Kiểm tra lịch sử Git commit theo yêu cầu giảng viên.
- Rà soát toàn bộ checklist Buổi 10.

### 8.7. Các chức năng chưa triển khai

- Thay đổi kỹ thuật viên và ghi nhận lý do.
- Đặt lịch giao – nhận máy qua API và Frontend.
- Kiểm tra xung đột lịch hẹn.
- Giao diện riêng cho kỹ thuật viên xem phiếu và lịch hẹn được giao.

Các nội dung trên thuộc phạm vi thiết kế tổng thể và cần được tiếp tục triển khai trong các giai đoạn sau.

---

## 9. Cấu trúc thư mục

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
│   ├── seed.sql
│   ├── srs.md
│   ├── usecase-spec.md
│   ├── usecase.drawio
│   ├── usecase.png
│   ├── wireframe.drawio
│   ├── wireframe.png
│   ├── thay-doi-thiet-ke.md
│   ├── minh-chung-api-buoi8.txt
│   ├── minh-chung-phan-cong-buoi8.txt
│   └── unit-test-results.txt
├── src/
│   ├── __init__.py
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── ticket_api.py
│   │   │   └── assignment_api.py
│   │   ├── services/
│   │   │   ├── ticket_service.py
│   │   │   └── assignment_service.py
│   │   ├── repositories/
│   │   │   ├── ticket_repository.py
│   │   │   └── assignment_repository.py
│   │   └── models/
│   └── frontend/
│       ├── api/
│       ├── public/
│       ├── src/
│       │   └── pages/
│       ├── index.html
│       ├── package.json
│       └── package-lock.json
├── tests/
│   └── test_assignment_service.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

File `smartcrm.db` được tạo trong quá trình chạy và lưu cục bộ, không đưa lên GitHub.

Các thư mục `.venv/`, `node_modules/` và `dist/` cũng được loại trừ khỏi Git.

---

## 10. Khai báo sử dụng công cụ AI

| Công cụ | Mục đích sử dụng | Cách kiểm tra / chỉnh sửa |
|---|---|---|
| ChatGPT | Hỗ trợ phân tích yêu cầu, xây dựng SRS, User Stories, Acceptance Criteria, Use Case Specification, Architecture, Data Model, SQL DDL, API Contract, triển khai Backend, Frontend và unit tests | Đối chiếu yêu cầu bài tập, kiểm tra mã nguồn, thực thi lệnh, kiểm thử API, Frontend và business logic |
| Draw.io AI | Hỗ trợ xây dựng Architecture Diagram, ERD và Wireframe | Kiểm tra thành phần, quan hệ, PK/FK, bố cục và tính nhất quán với SRS |

Sinh viên chịu trách nhiệm rà soát, kiểm chứng và điều chỉnh nội dung trước khi sử dụng.

Chi tiết được trình bày tại:

`docs/ai-disclosure.md`

---

## 11. Ghi chú

Dự án Smart CRM – Mekong Mobile tập trung vào luồng nghiệp vụ L4: Phân công kỹ thuật viên và lịch hẹn.

BT1 tập trung vào phân tích và thiết kế hệ thống.

Từ Buổi 8, dự án bắt đầu triển khai Backend, cơ sở dữ liệu, Ticket CRUD và chức năng phân công kỹ thuật viên.

Đến Buổi 10, dự án đã bổ sung Frontend kết nối REST API, script dữ liệu mẫu, bộ unit tests và hướng dẫn chạy hệ thống.

Các chức năng thay đổi kỹ thuật viên, quản lý lịch hẹn và kiểm tra xung đột lịch vẫn cần tiếp tục phát triển.

Trước khi nộp bài, cần xác nhận lại khả năng chạy trên môi trường fresh clone, minh chứng giao diện và lịch sử Git commit.