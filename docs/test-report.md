# TEST REPORT – SMART CRM L4

- Sinh viên: Nguyễn Minh Trị
- MSSV: 2374802010517
- Track: Software Engineering (SE)
- Ngày kiểm thử TC-01–TC-12: 06/11/2026; cập nhật regression BT3: 14/11/2026
- Công cụ: pytest 9.1.1, Python 3.12.2
- Kết quả: 12 passed, 0 failed, 1 warning (0.35s)
- Log: `docs/test-results-buoi14.txt`

## 1. Kết quả kiểm thử

| TC ID | Chức năng | Bước kiểm thử | Dữ liệu đầu vào | Expected | Actual | Status | Evidence |
|---|---|---|---|---|---|---|---|
| TC-01 | Phân công thành công | Gọi Assignment Service với mock repository | Ticket 10, technician 1 | Trả về ticket_id=10, technician_id=1 | Hai giá trị được assert đúng | PASS | `docs/test-results-buoi14.txt`; `docs/screenshots/TC-01.png` |
| TC-02 | Tạo lịch hẹn | Gọi API tạo lịch bằng dữ liệu fixture | `make_input()` | Lịch có status SCHEDULED, technician_id=1 | Hai giá trị được assert đúng | PASS | `docs/test-results-buoi14.txt`; `docs/screenshots/TC-02.png` |
| TC-03 | Đổi kỹ thuật viên | Manager gửi PUT đổi kỹ thuật viên; kiểm tra DB | Ticket 1, technician mới 2, lý do từ `payload()` | HTTP 200; phân công cũ kết thúc, lưu lý do; phân công mới hoạt động | HTTP 200; DB có 2 bản ghi, bản ghi mới chưa có ended_at | PASS | `docs/test-results-buoi14.txt`; `docs/screenshots/TC-03.png` |
| TC-04 | Giới hạn workload | Tạo 5 phân công, thử phân công thứ 6 | Technician 1, tickets 1–6 | Không còn đủ điều kiện; từ chối phân công thứ 6 | Danh sách đủ điều kiện rỗng; phát sinh ValueError | PASS | `docs/test-results-buoi14.txt`; `docs/screenshots/TC-04.png` |
| TC-05 | Hai lịch liền kề | Tạo hai lịch tại mốc 48h và 49h | Tickets 1, 2; hours=48,49 | Cho phép tạo hai lịch riêng | Hai appointment_id khác nhau | PASS | `docs/test-results-buoi14.txt`; `docs/screenshots/TC-05.png` |
| TC-06 | Priority không hợp lệ | POST tạo phiếu với priority INVALID | `priority="INVALID"` | HTTP 400 | HTTP 400 | PASS | `docs/test-results-buoi14.txt`; `docs/screenshots/TC-06.png` |
| TC-07 | Lý do đổi trống | Manager gửi PUT đổi kỹ thuật viên với lý do rỗng | `reason=""` | HTTP 422; giữ phân công cũ | HTTP 422; technician đang hoạt động vẫn là 1 | PASS | `docs/test-results-buoi14.txt`; `docs/screenshots/TC-07.png` |
| TC-08 | API không token | GET /tickets không Authorization | Không có token | HTTP 401 | HTTP 401 | PASS | `docs/test-results-buoi14.txt`; `docs/screenshots/TC-08.png` |
| TC-09 | Technician không được đổi phân công | Technician gửi PUT đổi kỹ thuật viên | Token `technician_test` | HTTP 403; giữ phân công cũ | HTTP 403; technician đang hoạt động vẫn là 1 | PASS | `docs/test-results-buoi14.txt`; `docs/screenshots/TC-09.png` |
| TC-10 | Token bị thu hồi | Logout rồi GET /tickets bằng token cũ | Token đã logout | Logout HTTP 200; GET HTTP 401 | Cả hai mã trạng thái đúng | PASS | `docs/test-results-buoi14.txt`; `docs/screenshots/TC-10.png` |
| TC-11 | Phân công trùng thất bại | Phân công ticket 1 hai lần | Ticket 1, technician 1 | Lần thứ hai bị từ chối; trạng thái phiếu vẫn ASSIGNED | ValueError; ticket status vẫn ASSIGNED | PASS | `docs/test-results-buoi14.txt`; `docs/screenshots/TC-11.png` |
| TC-12 | Lưu lịch sử phân công | Phân công rồi đổi kỹ thuật viên, truy vấn DB | Ticket 1; technician 1→2; reason="Technician A unavailable" | Có 2 bản ghi; đúng 1 active; lưu lý do | Tất cả điều kiện DB và status được assert đúng | PASS | `docs/test-results-buoi14.txt`; `docs/screenshots/TC-12.png` |

## 2. Tổng hợp

- Happy Path / Functional: TC-01 đến TC-03.
- Boundary: TC-04 và TC-05.
- Invalid Input: TC-06 và TC-07.
- Security / Authorization: TC-08 đến TC-10.
- Data Integrity / Regression: TC-11 và TC-12.
- Tổng cộng: 12 PASS, 0 FAIL.
- Full regression sau khi sửa BUG-03: 87 PASS, 0 FAIL, 1 warning.
- Full regression mới nhất (14/11/2026): 100 PASS, 0 FAIL, 1 warning (1.09s); log: `docs/test-results-bt3-latest.txt`.

## 3. Giới hạn

TC-01 sử dụng mock repository, không xác nhận
thao tác database thực tế.

TC-11 xác nhận lần phân công trùng bị từ chối
và trạng thái phiếu vẫn ASSIGNED; chưa chứng minh
toàn bộ transaction rollback trong mọi tình huống.

TC-05 xác nhận hai lịch liền kề được tạo thành công,
không thay thế kiểm thử mọi trường hợp xung đột lịch.

Cảnh báo Starlette là DeprecationWarning từ thư viện,
không phải test failure.

## 4. Minh chứng

- Log kiểm thử: `docs/test-results-buoi14.txt`.
- Mã nguồn: thư mục `tests/`.
- Ảnh kiểm thử TC-01 đến TC-12: đã lưu đầy đủ trong `docs/screenshots/`.

## 5. Phụ lục BT3 – Packaging, Deployment and Security

Ngày kiểm thử: 10/11/2026.

### 5.1. Kết quả kiểm thử triển khai

| ID | Hạng mục | Kết quả thực tế | Status |
|---|---|---|---|
| BT3-TC-01 | Docker Compose deployment | Backend và frontend khởi động, healthcheck healthy | PASS |
| BT3-TC-02 | Backend healthcheck | GET /health trả HTTP 200, database connected | PASS |
| BT3-TC-03 | Frontend | HTTP 200, giao diện tải thành công | PASS |
| BT3-TC-04 | SQLite persistence | Số lượng dữ liệu không thay đổi sau khi recreate backend container | PASS |
| BT3-TC-05 | Clean-room deployment | Frontend 15173, backend 18000 hoạt động với volume độc lập | PASS |
| BT3-TC-06 | Nginx reverse proxy | GET /api/health trả HTTP 200 thông qua Nginx | PASS |
| BT3-TC-07 | Authentication | POST /api/auth/login và GET /api/auth/me trả HTTP 200; role MANAGER | PASS |
| BT3-TC-08 | Unauthenticated API | GET /tickets, /technicians, /appointments và /assignments/eligible-technicians/1 đều trả HTTP 401 | PASS |
| BT3-TC-09 | Regression | pytest: 87 passed, 0 failed, 1 warning trong 0.97 giây | PASS |

### 5.2. Tổng hợp

- Tổng cộng: 9 PASS, 0 FAIL trong phạm vi các trường hợp BT3 đã kiểm thử.
- Regression lịch sử: 87 PASS, 0 FAIL, 1 warning.
- Regression mới nhất (14/11/2026): 100 PASS, 0 FAIL, 1 warning (1.06s); log: `docs/test-results-bt3-latest.txt`.
- Log regression: docs/test-results-bt3.txt.
- Frontend production build và Docker build check đã thực hiện thành công.
- Tại thời điểm kiểm thử ban đầu, clean-room được tạo từ bản clone của repository cục bộ. Sau đó, đã thực hiện fresh clone từ GitHub public tag v1.0 và kiểm chứng Docker trong môi trường độc lập. Bản tag cuối cần được đồng bộ sau commit tài liệu.

### 5.3. Kiểm thử bảo mật và giới hạn

- Bốn endpoint nghiệp vụ đại diện từ chối truy cập không có token với HTTP 401.
- Đăng nhập và truy vấn thông tin người dùng qua Nginx reverse proxy hoạt động.
- Phân quyền MANAGER được kiểm tra ở mã nguồn và đã có kiểm thử tự động trong bộ regression.
- Chưa kiểm thử độc lập đầy đủ các tình huống token hết hạn, rate limiting và kiểm thử xâm nhập.
- HTTPS và các biện pháp production hardening chưa được xác nhận đầy đủ.
- Kết quả phù hợp phạm vi triển khai và kiểm thử học thuật, không phải chứng nhận bảo mật production.

### 5.4. Minh chứng

- Log tự động: docs/test-results-bt3.txt.
- Mã nguồn kiểm thử: tests/.
- Ảnh giao diện clean-room và kết quả regression đã được chụp; việc đưa vào docs/screenshots/ sẽ hoàn tất ở bước tổng hợp minh chứng.
- Các kết quả triển khai Docker, persistence, reverse proxy và authentication đã được xác nhận qua Terminal trong quá trình BT3.

## 6. BT3 Final Verification Update

The earlier 87-passed regression result in Section 5 records an earlier testing stage and is retained for historical traceability.

Latest observed regression result:

- 100 tests passed.
- 0 tests failed.
- 1 deprecation warning.

Additional verification evidence:

- Public GitHub `v1.0` tag was used in an isolated fresh-clone Docker verification.
- Backend and frontend health checks returned HTTP 200.
- Unauthenticated business GET checks: 11/11 returned HTTP 401.
- TECHNICIAN authorization checks: 4/4 returned HTTP 403.
- Seed initialization was repeated without duplicate demo records.

The final `v1.0` release tag must be synchronized after the documentation changes are committed.

Evidence is stored under `evidence/C1/`, `evidence/C2/`, `evidence/C3/`, `evidence/C6/`, and `evidence/C8/`.
