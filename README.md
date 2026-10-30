# Smart CRM – Phân công kỹ thuật viên và lịch hẹn

**Sinh viên:** Nguyễn Minh Trị
**MSSV:** 2374802010517
**Track:** Software Engineering (SE)
**Học phần:** Chuyên đề Tốt nghiệp 1 – Trường Đại học Văn Lang
**Dự án:** Smart CRM – Mekong Mobile
**Luồng nghiệp vụ:** L4 – Phân công kỹ thuật viên và lịch hẹn
**Repository:** https://github.com/Tringuyen2374802010517/smart-crm
**Phiên bản nộp BT2:** `v0.2`

---

## 1. Giới thiệu dự án

Smart CRM – Mekong Mobile là hệ thống hỗ trợ quản lý hoạt động dịch vụ sửa chữa thiết bị.

Trong luồng nghiệp vụ L4, quản lý trung tâm cần xem các phiếu sửa chữa, xác định kỹ thuật viên phù hợp và thực hiện phân công dựa trên các điều kiện nghiệp vụ như tay nghề, trung tâm, trạng thái khả dụng và khối lượng công việc.

Phạm vi thiết kế tổng thể của L4 còn bao gồm thay đổi kỹ thuật viên phụ trách, đặt lịch giao – nhận thiết bị và kiểm tra xung đột lịch hẹn.

Dự án được phát triển qua các giai đoạn:

- **BT1:** Phân tích yêu cầu, thiết kế hệ thống, xây dựng SRS, Use Case, Architecture Diagram, ERD, Wireframe và API Contract.
- **Buổi 8 – Sprint 1:** Triển khai Backend, SQLite, Ticket CRUD và chức năng phân công kỹ thuật viên.
- **Buổi 10 – Sprint 2:** Xây dựng Frontend kết nối REST API, bổ sung unit tests, dữ liệu mẫu và các trạng thái Loading, Empty, Error.
- **Buổi 12 – BT2:** Tích hợp hệ thống, bổ sung Technician CRUD, kiểm thử API, kiểm tra khả năng dựng lại hệ thống và chuẩn bị demo phiên bản `v0.2`.

**Phạm vi đã hiện thực trong BT2:** Quản lý Ticket, quản lý Technician và phân công kỹ thuật viên phù hợp cho Ticket.

**Giới hạn:** Các chức năng quản lý lịch hẹn, thay đổi kỹ thuật viên kèm lý do và kiểm tra xung đột lịch chưa được triển khai đầy đủ trong phiên bản `v0.2`.

---

## 2. Công nghệ và kiến trúc

### 2.1. Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Backend | Python 3.12, FastAPI |
| Frontend | HTML, CSS, JavaScript, Vite |
| Database | SQLite |
| API | REST API |
| Unit Testing | pytest |
| API Testing | FastAPI TestClient, httpx, Swagger UI |
| Version Control | Git, GitHub |
| Thiết kế sơ đồ | Draw.io |
| Môi trường phát triển | macOS, Visual Studio Code |

### 2.2. Phiên bản môi trường đã sử dụng

- Python 3.12.2
- Node.js 24.12.0
- npm 11.6.2
- FastAPI 0.141.1
- Vite 8.3.5
- pytest 9.1.1
- SQLite 3

Các thư viện Python được khai báo với phiên bản cụ thể trong `requirements.txt`.

Các dependencies Frontend được khai báo trong `src/frontend/package.json` và `src/frontend/package-lock.json`.

### 2.3. Kiến trúc hệ thống

Hệ thống sử dụng kiến trúc phân lớp:

```text
Frontend (HTML / CSS / JavaScript / Vite)
                  |
                  | HTTP / REST API
                  v
Backend (FastAPI)
                  |
              API / Routes
                  |
              Service
          (Business Logic)
                  |
              Repository
                  |
                  v
             SQLite Database
```

Vai trò của từng lớp:

- **API / Routes:** Tiếp nhận HTTP request, định nghĩa endpoint, kiểm tra cấu trúc dữ liệu đầu vào và trả response.
- **Service:** Xử lý nghiệp vụ, kiểm tra điều kiện hợp lệ và điều phối các thao tác.
- **Repository:** Thực hiện truy vấn và cập nhật dữ liệu SQLite.
- **Frontend:** Gọi REST API, hiển thị dữ liệu và xử lý tương tác của người dùng.

Các lỗi nghiệp vụ được biểu diễn bằng exception tại tầng Service và chuyển thành HTTP response phù hợp thông qua exception handlers của FastAPI.

Cách tổ chức này giúp tách biệt xử lý HTTP, business logic và thao tác dữ liệu, đồng thời hỗ trợ kiểm thử từng thành phần.

---

## 3. Hướng dẫn Clone, Run và Test

### 3.1. Yêu cầu môi trường

Máy tính cần cài đặt:

- Python 3.12
- Node.js tương thích với Vite 8, khuyến nghị Node.js 24
- npm
- Git
- SQLite 3

Các lệnh dưới đây dành cho macOS/Linux.

### 3.2. Clone repository theo tag v0.2

Mở Terminal tại một thư mục chưa chứa dự án, sau đó chạy:

```bash
git clone --branch v0.2 https://github.com/Tringuyen2374802010517/smart-crm.git
cd smart-crm
```

Lệnh trên tải phiên bản được đánh dấu bằng tag `v0.2`.

**Lưu ý:** Do `v0.2` là annotated tag, Git có thể hiển thị thông báo `detached HEAD`. Đây là trạng thái bình thường khi checkout một tag để kiểm tra phiên bản đã phát hành.

Không cần chuyển sang nhánh `dev` khi kiểm thử bản nộp BT2.

Các lệnh tiếp theo được thực hiện tại thư mục gốc `smart-crm`, trừ khi có hướng dẫn khác.

### 3.3. Tạo môi trường Python

Tạo virtual environment:

```bash
python3.12 -m venv .venv
```

Cài đặt dependencies:

```bash
.venv/bin/python3 -m pip install -r requirements.txt
```

File `requirements.txt` bao gồm các thư viện cần thiết để chạy Backend và bộ kiểm thử, trong đó có FastAPI, Uvicorn, pytest và httpx.

### 3.4. Cấu hình môi trường

Repository có file `.env.example` với các biến cấu hình mẫu:

```dotenv
DATABASE_URL=sqlite:///./smartcrm.db
APP_HOST=127.0.0.1
APP_PORT=8000
SECRET_KEY=
```

File này được cung cấp để mô tả các biến cấu hình dự kiến.

**Trong phiên bản `v0.2`, Backend hiện sử dụng đường dẫn SQLite và cổng chạy theo cấu hình trong mã nguồn/lệnh khởi chạy; các biến trong `.env.example` chưa được nạp tự động.** Vì vậy, không bắt buộc tạo file `.env` để chạy demo.

Không commit file `.env` chứa thông tin nhạy cảm hoặc khóa bí mật thật lên GitHub.

### 3.5. Khởi tạo cơ sở dữ liệu

Dự án sử dụng SQLite với năm bảng:

1. `ticket` – Thông tin phiếu sửa chữa.
2. `technician` – Thông tin kỹ thuật viên.
3. `technician_skill` – Kỹ năng và mức độ thành thạo.
4. `assignment` – Lịch sử phân công kỹ thuật viên.
5. `appointment` – Cấu trúc dữ liệu lịch giao – nhận thiết bị.

Tạo database và các bảng:

```bash
sqlite3 smartcrm.db < docs/schema.sql
```

Nạp dữ liệu mẫu:

```bash
sqlite3 smartcrm.db < docs/seed.sql
```

Dữ liệu mẫu gồm:

- 3 Ticket.
- 3 Technician.
- 3 bản ghi Technician Skill.

Kiểm tra danh sách bảng:

```bash
sqlite3 smartcrm.db ".tables"
```

Kiểm tra ràng buộc khóa ngoại:

```bash
sqlite3 smartcrm.db "PRAGMA foreign_key_check;"
```

Nếu không có dòng lỗi nào được trả về, kiểm tra khóa ngoại đạt yêu cầu.

**Khả năng chạy lại:** `schema.sql` sử dụng `IF NOT EXISTS`; `seed.sql` sử dụng `INSERT OR IGNORE`. Có thể thực thi lại hai script mà không tạo thêm bản ghi mẫu trùng khóa.

Đây là cơ chế khởi tạo dữ liệu lặp lại được, không phải hệ thống migration nâng cấp cấu trúc database giữa các phiên bản.

File `smartcrm.db` được tạo cục bộ và không đưa lên GitHub.

### 3.6. Khởi chạy Backend

Tại thư mục gốc dự án, chạy:

```bash
.venv/bin/python3 -m uvicorn src.backend.main:app --reload --host 127.0.0.1 --port 8000
```

Sau khi Backend khởi chạy, có thể truy cập:

- Swagger UI: http://127.0.0.1:8000/docs
- Kiểm tra database: http://127.0.0.1:8000/db-check
- Danh sách Ticket: http://127.0.0.1:8000/tickets
- Danh sách Technician: http://127.0.0.1:8000/technicians

Giữ Terminal Backend hoạt động trong khi sử dụng Frontend.

### 3.7. Khởi chạy Frontend

Mở Terminal thứ hai tại thư mục gốc dự án.

Chuyển vào thư mục Frontend:

```bash
cd src/frontend
```

Cài đặt dependencies:

```bash
npm ci
```

Khởi chạy Vite:

```bash
npm run dev
```

Truy cập:

http://localhost:5173

Frontend gửi REST API request đến Backend tại `http://localhost:8000`.

Để sử dụng giao diện bình thường, Backend cần đang chạy trên cổng `8000` và Frontend trên cổng `5173`.

### 3.8. Chạy bộ kiểm thử

Mở một Terminal khác tại thư mục gốc dự án.

Chạy toàn bộ bộ kiểm thử:

```bash
.venv/bin/python3 -m pytest -v
```

Kết quả kiểm thử đã ghi nhận cho phiên bản BT2:

**25 tests passed**, gồm:

| Bộ kiểm thử | Số test |
|---|---:|
| Assignment Service | 9 |
| Technician API | 8 |
| Ticket API | 8 |
| **Tổng cộng** | **25** |

Các nhóm trường hợp được kiểm tra gồm:

- **Happy path:** Dữ liệu hợp lệ, thao tác thành công.
- **Boundary case:** Các trường hợp biên của điều kiện nghiệp vụ.
- **Invalid input:** Dữ liệu không hợp lệ, không tìm thấy đối tượng hoặc vi phạm Business Rules.

Chín bài kiểm thử Assignment Service sử dụng mock repository để kiểm tra business logic.

Mười sáu bài kiểm thử API của Ticket và Technician sử dụng database SQLite tạm để tránh ảnh hưởng dữ liệu phát triển.

Các file kiểm thử:

```text
tests/test_assignment_service.py
tests/test_technician_api.py
tests/test_ticket_api.py
```

Kết quả kiểm thử trước đây của Buổi 10 được lưu trong `docs/unit-test-results.txt`. Đây là minh chứng lịch sử cho 9 bài kiểm thử Assignment Service, không thay thế kết quả chạy đầy đủ 25 bài kiểm thử của BT2.

### 3.9. Build Frontend

Tại thư mục gốc dự án, chạy:

```bash
npm --prefix src/frontend run build
```

Frontend sử dụng Vite và đã được kiểm tra build thành công.

Thư mục `dist/` được tạo trong quá trình build và không được commit vào repository.

### 3.10. Kiểm tra khả năng dựng lại hệ thống

Quy trình kiểm tra phiên bản BT2:

1. Clone repository theo tag `v0.2`.
2. Tạo môi trường Python và cài dependencies.
3. Khởi tạo database bằng `schema.sql`.
4. Nạp dữ liệu mẫu bằng `seed.sql`.
5. Khởi chạy Backend.
6. Cài dependencies và khởi chạy Frontend.
7. Kiểm tra API và luồng phân công kỹ thuật viên.
8. Chạy bộ kiểm thử bằng một lệnh pytest.
9. Chạy lại schema và seed để xác nhận dữ liệu không bị nhân đôi.

Quy trình này được thiết kế để giảng viên có thể dựng lại hệ thống từ repository mà không cần sử dụng database hay virtual environment có sẵn trên máy phát triển.

---

## 4. Các chức năng đã triển khai

### 4.1. Ticket CRUD

Module Ticket hỗ trợ đầy đủ các thao tác:

| Method | Endpoint | Chức năng |
|---|---|---|
| GET | `/tickets` | Xem danh sách Ticket |
| GET | `/tickets/{ticket_id}` | Xem chi tiết Ticket |
| POST | `/tickets` | Tạo Ticket |
| PUT | `/tickets/{ticket_id}` | Cập nhật Ticket |
| DELETE | `/tickets/{ticket_id}` | Xóa Ticket |

Ticket mới có trạng thái mặc định `PENDING`.

Các mức độ ưu tiên hợp lệ:

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

### 4.2. Technician CRUD

Module Technician hỗ trợ đầy đủ các thao tác:

| Method | Endpoint | Chức năng |
|---|---|---|
| GET | `/technicians` | Xem danh sách kỹ thuật viên |
| GET | `/technicians/{technician_id}` | Xem chi tiết kỹ thuật viên |
| POST | `/technicians` | Tạo kỹ thuật viên |
| PUT | `/technicians/{technician_id}` | Cập nhật kỹ thuật viên |
| DELETE | `/technicians/{technician_id}` | Xóa kỹ thuật viên |

Dữ liệu đầu vào của Technician gồm:

- `name`
- `center_id`
- `area`
- `availability_status`

Ví dụ xem danh sách kỹ thuật viên:

```bash
curl http://127.0.0.1:8000/technicians
```

Ví dụ tạo kỹ thuật viên:

```bash
curl -X POST http://127.0.0.1:8000/technicians \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nguyen Van A",
    "center_id": 1,
    "area": "HCM",
    "availability_status": "AVAILABLE"
  }'
```

Hai module Ticket và Technician đáp ứng yêu cầu tối thiểu hai thực thể CRUD của track SE trong BT2.

### 4.3. Assignment – Phân công kỹ thuật viên

Các endpoint đã triển khai:

| Method | Endpoint | Chức năng |
|---|---|---|
| GET | `/assignments/eligible-technicians/{ticket_id}` | Xem kỹ thuật viên đủ điều kiện |
| POST | `/assignments/` | Phân công kỹ thuật viên |

Lấy danh sách kỹ thuật viên phù hợp:

```bash
curl http://127.0.0.1:8000/assignments/eligible-technicians/1
```

Thực hiện phân công:

```bash
curl -X POST http://127.0.0.1:8000/assignments/ \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": 1,
    "technician_id": 1
  }'
```

Ví dụ trên yêu cầu Ticket chưa được phân công và kỹ thuật viên đáp ứng đầy đủ các điều kiện nghiệp vụ.

### 4.4. Business Rules

Các quy tắc đã triển khai trong chức năng phân công:

**BR1 – Giới hạn phân công đang hoạt động**

- Mỗi Ticket có tối đa một Assignment đang hoạt động.
- Assignment đang hoạt động được xác định bởi `ended_at IS NULL`.
- SQLite sử dụng unique index để hỗ trợ ngăn phân công trùng.

**BR2 – Điều kiện kỹ thuật viên**

Kỹ thuật viên cần:

- Thuộc cùng trung tâm với Ticket.
- Có trạng thái `AVAILABLE`.
- Có kỹ năng phù hợp với `incident_group`.
- Có mức độ thành thạo `proficiency >= 3`.

**Điều kiện Ticket**

- Ticket phải có trạng thái `PENDING`.
- Ticket chưa có Assignment đang hoạt động.

**Khối lượng công việc**

- `current_workload` được tính từ số Assignment đang hoạt động.
- Danh sách kỹ thuật viên phù hợp được sắp xếp theo khối lượng công việc tăng dần.

Nếu không đáp ứng điều kiện, hệ thống từ chối thao tác bằng thông báo lỗi phù hợp thay vì thực hiện phân công không hợp lệ.

---

## 5. Frontend và luồng nghiệp vụ end-to-end

### 5.1. Các màn hình đã triển khai

Frontend có ba màn hình/chế độ hiển thị chính kết nối REST API:

1. **Ticket List:** Hiển thị danh sách phiếu sửa chữa.
2. **Ticket Detail:** Hiển thị thông tin chi tiết một phiếu.
3. **Technician Assignment:** Hiển thị kỹ thuật viên phù hợp và thực hiện phân công.

Frontend sử dụng dữ liệu trả về từ Backend, không sử dụng danh sách Ticket cố định để mô phỏng kết quả API.

### 5.2. Luồng nghiệp vụ chính

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
Xem chi tiết hoặc mở màn hình phân công
      |
      v
Lấy danh sách kỹ thuật viên phù hợp từ API
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
Frontend hiển thị kết quả
```

Đây là luồng end-to-end đã triển khai cho nghiệp vụ phân công kỹ thuật viên của phiên bản `v0.2`.

### 5.3. Trạng thái giao diện

Frontend xử lý ba trạng thái:

- **Loading:** Hiển thị thông báo khi đang tải dữ liệu từ API.
- **Empty:** Hiển thị thông báo khi không có Ticket hoặc kỹ thuật viên phù hợp.
- **Error:** Hiển thị thông báo khi yêu cầu thất bại hoặc không thể kết nối Backend.

Khi Backend không khả dụng, Frontend xử lý lỗi kết nối và hiển thị thông báo thay vì để ứng dụng treo không phản hồi.

### 5.4. Minh chứng giao diện

Các ảnh chụp được lưu trong `docs/`:

| File | Nội dung |
|---|---|
| `buoi10-ticket-list.png` | Danh sách Ticket |
| `buoi10-ticket-detail.png` | Chi tiết Ticket |
| `buoi10-technician-details.png` | Thông tin kỹ thuật viên |
| `buoi10-assignment-success.png` | Phân công thành công |
| `buoi10-loading-state.png` | Trạng thái Loading |
| `buoi10-empty-state.png` | Trạng thái Empty |
| `buoi10-error-state.png` | Trạng thái Error |

Các ảnh API bổ sung:

- `docs/api-get-tickets-200.png`
- `docs/api-post-tickets-400.png`

---

## 6. Kiểm thử và chất lượng kỹ thuật

### 6.1. Các nhóm kiểm thử

**Assignment Service**

Bộ kiểm thử gồm các trường hợp:

1. Phân công kỹ thuật viên thành công.
2. Không tìm thấy Ticket.
3. Ticket không ở trạng thái `PENDING`.
4. Ticket đã có phân công đang hoạt động.
5. Kỹ thuật viên khác trung tâm.
6. Kỹ thuật viên không khả dụng.
7. Kỹ thuật viên không đủ kỹ năng.
8. Không có kỹ thuật viên phù hợp.
9. Không tìm thấy kỹ thuật viên.

**Ticket API và Technician API**

Các bài kiểm thử API kiểm tra các thao tác CRUD, phản hồi HTTP và những trường hợp dữ liệu không hợp lệ hoặc đối tượng không tồn tại.

### 6.2. Kết quả kiểm thử BT2

Lệnh chạy:

```bash
.venv/bin/python3 -m pytest -v
```

Kết quả đã ghi nhận:

**25/25 tests passed.**

### 6.3. Kiểm tra tính lặp lại của dữ liệu

Chạy lại:

```bash
sqlite3 smartcrm.db < docs/schema.sql
sqlite3 smartcrm.db < docs/seed.sql
```

Kiểm tra số bản ghi mẫu:

```bash
sqlite3 smartcrm.db "SELECT COUNT(*) FROM ticket;"
sqlite3 smartcrm.db "SELECT COUNT(*) FROM technician;"
sqlite3 smartcrm.db "SELECT COUNT(*) FROM technician_skill;"
```

Trên database mẫu mới, kết quả mong đợi sau lần nạp đầu tiên và lần nạp thứ hai lần lượt là:

- Ticket: 3 bản ghi.
- Technician: 3 bản ghi.
- Technician Skill: 3 bản ghi.

Script không tự động cập nhật các bản ghi mẫu đã tồn tại.

### 6.4. Bug Log

Các lỗi đã được ghi nhận tại:

`docs/bug-log.md`

Trong đó có lỗi **BUG-001 – Seed dữ liệu không hỗ trợ chạy lặp lại**.

- Nguyên nhân: Các lệnh `INSERT INTO` ban đầu có thể phát sinh lỗi trùng khóa.
- Cách sửa: Sử dụng `INSERT OR IGNORE`.
- Xác nhận: Chạy lại schema và seed hai lần, dữ liệu không bị nhân đôi.
- Commit sửa lỗi: `42eb9bd`.

---

## 7. Phạm vi và giới hạn triển khai

### 7.1. Chức năng đã triển khai

- Xem danh sách Ticket.
- Xem chi tiết Ticket.
- CRUD Ticket.
- CRUD Technician.
- Xem danh sách kỹ thuật viên đủ điều kiện.
- Kiểm tra trạng thái Ticket.
- Kiểm tra trung tâm, tay nghề và trạng thái kỹ thuật viên.
- Tính và sử dụng khối lượng công việc khi lựa chọn kỹ thuật viên.
- Phân công kỹ thuật viên.
- Ngăn phân công trùng.
- Hiển thị kết quả và thông báo lỗi.
- Kiểm thử tự động và khởi tạo dữ liệu mẫu.

### 7.2. Chức năng chưa triển khai đầy đủ

- Thay đổi kỹ thuật viên phụ trách kèm lý do.
- Đặt lịch giao – nhận thiết bị qua API và Frontend.
- Kiểm tra xung đột lịch hẹn.
- Giao diện riêng để kỹ thuật viên xem phiếu và lịch hẹn được giao.
- Hoàn thiện toàn bộ quy tắc SLA và vòng đời trạng thái theo SRS.

Bảng `appointment` đã được thiết kế trong cơ sở dữ liệu, nhưng chưa có module quản lý lịch hẹn hoàn chỉnh.

### 7.3. Ngoài phạm vi

- Quản lý kho linh kiện.
- Quản lý thanh toán và hóa đơn.
- Toàn bộ quy trình sửa chữa thiết bị.
- Đăng nhập và phân quyền chi tiết.
- Các luồng nghiệp vụ khác ngoài L4.
- Triển khai trong môi trường production.

---

## 8. Tài liệu phân tích, thiết kế và thay đổi

Các tài liệu BT1 và các giai đoạn triển khai tiếp theo được lưu trong `docs/`.

| Tài liệu | Nội dung |
|---|---|
| `srs.md` | Yêu cầu chức năng, phi chức năng, User Stories, Business Rules |
| `usecase-spec.md` | Đặc tả Use Case |
| `usecase.drawio`, `usecase.png` | Use Case Diagram |
| `architecture.md` | Mô tả và lập luận kiến trúc |
| `architecture.drawio`, `architecture.png` | Architecture Diagram |
| `erd.drawio`, `erd.png` | ERD |
| `wireframe.drawio`, `wireframe.png` | Wireframe |
| `api-contract.md` | API Contract |
| `schema.sql` | Cấu trúc database |
| `seed.sql` | Dữ liệu mẫu |
| `thay-doi-thiet-ke.md` | Thay đổi và quyết định thiết kế |
| `ai-disclosure.md` | Khai báo sử dụng công cụ AI |
| `bug-log.md` | Nhật ký lỗi và cách khắc phục |
| `minh-chung-api-buoi8.txt` | Minh chứng API Buổi 8 |
| `minh-chung-phan-cong-buoi8.txt` | Minh chứng phân công Buổi 8 |
| `unit-test-results.txt` | Minh chứng 9 unit tests Buổi 10 |

Tài liệu BT1 được lưu tại:

`docs/CDTN1_Buoi6_2374802010517_NguyenMinhTri.pdf`

Các tài liệu phân tích và thiết kế của BT1 được giữ lại để phục vụ đối chiếu với phiên bản đã hiện thực.

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
│   ├── bug-log.md
│   ├── erd.drawio
│   ├── erd.png
│   ├── schema.sql
│   ├── seed.sql
│   ├── srs.md
│   ├── thay-doi-thiet-ke.md
│   ├── usecase-spec.md
│   ├── usecase.drawio
│   ├── usecase.png
│   ├── wireframe.drawio
│   ├── wireframe.png
│   ├── unit-test-results.txt
│   ├── minh-chung-api-buoi8.txt
│   ├── minh-chung-phan-cong-buoi8.txt
│   └── [các ảnh minh chứng]
├── src/
│   ├── __init__.py
│   ├── backend/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── assignment_api.py
│   │   │   ├── technician_api.py
│   │   │   └── ticket_api.py
│   │   ├── services/
│   │   │   ├── assignment_service.py
│   │   │   ├── technician_service.py
│   │   │   ├── ticket_service.py
│   │   │   └── exceptions.py
│   │   ├── repositories/
│   │   │   ├── assignment_repository.py
│   │   │   ├── technician_repository.py
│   │   │   └── ticket_repository.py
│   │   └── models/
│   └── frontend/
│       ├── api/
│       │   ├── client.js
│       │   └── ticket.api.js
│       ├── public/
│       ├── src/
│       │   ├── main.js
│       │   ├── style.css
│       │   └── pages/
│       │       ├── TicketDetail.js
│       │       └── TechnicianAssignment.js
│       ├── index.html
│       ├── package.json
│       └── package-lock.json
├── tests/
│   ├── test_assignment_service.py
│   ├── test_technician_api.py
│   └── test_ticket_api.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Các thư mục hoặc file được tạo cục bộ như `.venv/`, `node_modules/`, `dist/`, `__pycache__/` và `smartcrm.db` không thuộc nội dung cần commit.

---

## 10. Khai báo sử dụng công cụ AI

Dự án có sử dụng công cụ AI để hỗ trợ một số công việc trong quá trình phân tích, thiết kế, lập trình và kiểm thử.

| Công cụ | Mục đích sử dụng | Cách kiểm chứng |
|---|---|---|
| ChatGPT | Hỗ trợ phân tích yêu cầu, SRS, User Stories, Use Case, kiến trúc, dữ liệu, Backend, Frontend, kiểm thử và tài liệu | Đối chiếu yêu cầu, kiểm tra mã nguồn, chạy test, kiểm thử API và luồng nghiệp vụ |
| Draw.io AI | Hỗ trợ xây dựng sơ đồ kiến trúc, ERD và Wireframe | Kiểm tra quan hệ, thành phần, khóa dữ liệu, bố cục và tính nhất quán |

Sinh viên chịu trách nhiệm kiểm tra, điều chỉnh và giải thích mã nguồn cũng như nội dung được sử dụng trong bài làm.

Chi tiết được ghi tại:

`docs/ai-disclosure.md`

---

## 11. Hướng dẫn demo BT2

Demo tập trung vào luồng nghiệp vụ chính đã triển khai.

### 11.1. Demo luồng thành công

1. Khởi chạy Backend và Frontend theo mục 3.
2. Mở danh sách Ticket trên Frontend.
3. Chọn Ticket có trạng thái `PENDING` và chưa được phân công.
4. Xem thông tin Ticket và danh sách kỹ thuật viên phù hợp.
5. Chọn kỹ thuật viên hợp lệ.
6. Thực hiện phân công.
7. Quan sát thông báo kết quả và trạng thái Ticket.

### 11.2. Demo xử lý lỗi

Có thể kiểm tra các trường hợp:

- Ticket không tồn tại.
- Kỹ thuật viên không tồn tại.
- Kỹ thuật viên không đáp ứng Business Rules.
- Ticket đã được phân công.
- Backend không hoạt động khi Frontend gửi yêu cầu.

Hệ thống cần từ chối yêu cầu không hợp lệ và hiển thị thông báo phù hợp.

### 11.3. Demo kiểm thử

Chạy:

```bash
.venv/bin/python3 -m pytest -v
```

Kết quả đã ghi nhận của phiên bản BT2: **25 tests passed**.

### 11.4. Demo lỗi đã sửa

Mở `docs/bug-log.md` và trình bày BUG-001:

1. Cách tái hiện lỗi seed trùng khóa.
2. Nguyên nhân.
3. Cách sửa bằng `INSERT OR IGNORE`.
4. Kết quả kiểm thử sau khi sửa.

---

## 12. Tổng kết

Phiên bản Smart CRM `v0.2` hiện thực các thành phần kỹ thuật chính của luồng L4:

- Backend FastAPI tổ chức theo API / Service / Repository.
- SQLite với schema và seed có thể chạy lại.
- Hai thực thể Ticket và Technician có đầy đủ CRUD.
- Chức năng phân công kỹ thuật viên theo Business Rules.
- Frontend kết nối REST API với ba màn hình chính.
- Các trạng thái Loading, Empty và Error.
- Bộ kiểm thử tự động gồm 25 test.
- README và tài liệu phục vụ dựng lại, kiểm tra và demo hệ thống.

Dự án tiếp tục kế thừa các tài liệu phân tích, thiết kế của BT1. Những chức năng chưa hoàn thiện, đặc biệt là quản lý lịch hẹn và kiểm tra xung đột lịch, được xác định rõ để tiếp tục phát triển trong các giai đoạn sau.
