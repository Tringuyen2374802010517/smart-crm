# TEST REPORT – SMART CRM L4

- Sinh viên: Nguyễn Minh Trị
- MSSV: 2374802010517
- Track: Software Engineering (SE)
- Ngày kiểm thử: 06/11/2026
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
- Full regression mới nhất sau khi sửa BUG-03: 87 PASS, 0 FAIL, 1 warning.

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
