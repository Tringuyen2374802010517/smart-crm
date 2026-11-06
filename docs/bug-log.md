# Bug Log – Smart CRM BT2

## BUG-001: Seed dữ liệu không hỗ trợ chạy lặp lại

- **Module:** Database Initialization
- **Mức độ:** Medium
- **Trạng thái:** Fixed
- **Commit sửa lỗi:** `42eb9bd`
- **File liên quan:** `docs/seed.sql`

### 1. Mô tả

Phiên bản seed ban đầu sử dụng `INSERT INTO` với các
khóa chính cố định. Khi chạy lại trên database đã chứa
dữ liệu mẫu, SQLite có thể phát sinh lỗi trùng khóa chính.

### 2. Các bước tái hiện trên phiên bản cũ

Sử dụng `docs/seed.sql` trước commit `42eb9bd`.

1. Tạo database SQLite mới bằng `docs/schema.sql`.
2. Chạy `docs/seed.sql` lần thứ nhất.
3. Chạy lại `docs/seed.sql` lần thứ hai.

### 3. Kết quả mong đợi

Script seed có thể chạy nhiều lần mà không tạo dữ liệu
trùng hoặc phát sinh lỗi khóa chính.

### 4. Nguyên nhân

Các lệnh `INSERT INTO` chưa xử lý trường hợp dữ liệu
mẫu với khóa chính tương ứng đã tồn tại.

### 5. Cách khắc phục

Chuyển các lệnh seed thành `INSERT OR IGNORE INTO`.
Những bản ghi đã tồn tại được giữ nguyên.

### 6. Kiểm thử sau khi sửa

Chạy schema và seed trên database tạm:

- Lần 1: 3 Ticket, 3 Technician, 3 Technician Skill.
- Lần 2: 3 Ticket, 3 Technician, 3 Technician Skill.
- Không phát sinh bản ghi trùng.
- Kết quả: PASS.

### 7. Giới hạn

`INSERT OR IGNORE` chỉ bỏ qua dữ liệu đã tồn tại theo
ràng buộc SQLite; không tự động cập nhật dữ liệu mẫu cũ.

### 8. Minh chứng Before/After
- Before Fix: `docs/screenshots/BUG-001-before.png`.
- After Fix: `docs/screenshots/BUG-001-after.png`.

## BUG-01: API nghiệp vụ cho phép truy cập khi chưa đăng nhập

- **Module:** Backend Authentication / API Security
- **Mức độ:** Major
- **Trạng thái:** Fixed
- **Phát hiện bằng:** Kiểm thử API thủ công bằng curl
- **Commit sửa lỗi:** `6cc8aa3`
- **Branch:** `feature/l4-modern-ui`

### 1. Mô tả lỗi

Các API nghiệp vụ chưa yêu cầu xác thực người dùng.
Request không có Bearer token vẫn có thể truy cập danh sách
phiếu sửa chữa.

### 2. Các bước tái hiện

1. Khởi động FastAPI.
2. Gửi GET /tickets mà không cung cấp Authorization header.
3. Quan sát HTTP status và dữ liệu trả về.

### 3. Expected / Actual trước khi sửa

- **Expected:** HTTP 401 Unauthorized.
- **Actual:** HTTP 200 OK, trả về danh sách phiếu.
- **Kết quả:** FAIL.

### 4. Nguyên nhân gốc

Các business router chưa được gắn dependency xác thực.
Frontend cũng chưa gửi Bearer token nhất quán cho
các request nghiệp vụ.

### 5. Cách khắc phục

- Thêm dependency xác thực cho Tickets, Assignments,
  Technicians và Appointments tại Backend.
- Bổ sung Bearer token vào API client của Frontend.
- Chuyển thao tác hoàn thành phiếu sang sử dụng API client.
- Cập nhật các fixture kiểm thử để đăng nhập bằng tài khoản
  thử nghiệm trên database tạm.
- Bổ sung 12 test bảo mật trong test_business_auth.py.

### 6. Kiểm thử sau khi sửa

- GET /tickets không có token: HTTP 401 — PASS.
- Token sai, token bị thu hồi và request ghi dữ liệu
  không có token: PASS trong bộ test bảo mật.
- Token hợp lệ truy cập GET /tickets: PASS.
- Tại thời điểm sửa BUG-01, toàn bộ pytest: 63 passed, 0 failed, 1 warning.
- Frontend: người thực hiện xác nhận các màn hình
  được kiểm tra hoạt động bình thường.

### 7. Lý do phân loại Major

Lỗi cho phép người chưa đăng nhập truy cập dữ liệu
nghiệp vụ, vi phạm yêu cầu kiểm soát truy cập.
Đã xác nhận truy cập đọc trái phép; chưa thực hiện
đánh giá đầy đủ mọi tác động bảo mật.

### 8. Minh chứng

- Commit sửa lỗi: `6cc8aa3`.
- Test bảo mật: `tests/test_business_auth.py`.
- Before Fix: `docs/screenshots/BUG-01-before.png`.
- After Fix: `docs/screenshots/BUG-01-after.png`.
- Minh chứng kiểm thử bảo mật bổ sung: `docs/screenshots/BUG-01.png`.

---

## BUG-02: Chưa hỗ trợ thay đổi kỹ thuật viên sau khi phân công

- **Module:** Assignment Management
- **Mức độ:** Major (đánh giá theo ảnh hưởng nghiệp vụ)
- **Trạng thái:** Fixed
- **Commit sửa lỗi:** `e601110`
- **Phát hiện bằng:** Rà soát chức năng theo phản hồi BT2
- **Branch:** `feature/l4-modern-ui`
- **Loại:** Missing functionality / Requirement gap

### 1. Mô tả

Phiên bản trước chưa hỗ trợ Manager thay đổi kỹ thuật viên
cho phiếu đã được phân công và ghi nhận lý do thay đổi.

Đây là chức năng còn thiếu so với yêu cầu nghiệp vụ,
không phải lỗi runtime đã được tái hiện.

### 2. Các bước xác minh trước khi sửa

1. Đăng nhập bằng tài khoản Manager.
2. Mở chi tiết phiếu ở trạng thái ASSIGNED.
3. Kiểm tra khả năng thay đổi kỹ thuật viên và nhập lý do.
4. Đối chiếu chức năng hiện có với yêu cầu nghiệp vụ.

### 3. Expected / Actual trước khi sửa

- **Expected:** Manager có thể chọn kỹ thuật viên thay thế
  đủ điều kiện, nhập lý do và lưu lịch sử thay đổi.
- **Actual:** Chưa có luồng đổi kỹ thuật viên hoàn chỉnh
  trên API và giao diện.

### 4. Nguyên nhân

Chức năng phân công ban đầu chỉ xử lý phiếu PENDING.
Luồng thay đổi kỹ thuật viên của phiếu ASSIGNED chưa
được triển khai đầy đủ.

### 5. Cách khắc phục

- Bổ sung API đổi kỹ thuật viên dành cho Manager.
- Kiểm tra kỹ thuật viên thay thế theo trung tâm,
  trạng thái khả dụng, kỹ năng, mức thành thạo
  và giới hạn khối lượng công việc.
- Bắt buộc nhập lý do thay đổi.
- Kết thúc phân công cũ và tạo phân công mới
  trong cùng một transaction.
- Lưu lịch sử phân công trong database.
- Bổ sung API và giao diện xem lịch sử phân công.
- Bổ sung kiểm thử tự động cho chức năng.

### 6. Kiểm thử sau khi sửa

- Đổi kỹ thuật viên phiếu #1 từ #1 sang #8: PASS.
- Phân công cũ có ended_at và change_reason: PASS.
- Phân công mới có ended_at = NULL: PASS.
- Chỉ còn một phân công đang hoạt động: PASS.
- Manager xem được lịch sử hai lần phân công: PASS.
- API history kiểm tra quyền truy cập: PASS.
- Tại thời điểm sửa BUG-02, full regression: 86 passed, 0 failed, 1 warning.
- Frontend Vite build: PASS.

### 7. Minh chứng

- `docs/screenshots/BUG-02-before.png`
- `docs/screenshots/BUG-02-after.png`
- `docs/screenshots/BUG-02-database.png`
- `docs/screenshots/BUG-02-history.png`
- `docs/screenshots/BUG-02-tests.png`
- `tests/test_reassignment.py`
- `tests/test_reassignment_api.py`

### 8. Giới hạn

Chưa thực hiện kiểm thử tải đồng thời nhiều người dùng
trên môi trường production.

---

## BUG-03: Technician có thể thực hiện phân công kỹ thuật viên trái quyền

- **Module:** Assignment Management / Role-Based Access Control
- **Mức độ:** Major
- **Trạng thái:** Fixed
- **Commit sửa lỗi:** `6cc17ba`
- **Phát hiện bằng:** Kiểm thử API tự động với pytest
- **Branch:** `feature/l4-modern-ui`
- **Yêu cầu liên quan:** FR3, US3 trong `docs/srs.md`

### 1. Mô tả lỗi

API `POST /assignments/` yêu cầu người dùng đăng nhập nhưng chưa
kiểm tra vai trò Manager. Do đó, tài khoản Technician vẫn có thể
tạo phân công kỹ thuật viên, mặc dù nghiệp vụ phân công thuộc
trách nhiệm của quản lý trung tâm theo FR3 và US3.

### 2. Các bước tái hiện

1. Khởi tạo database kiểm thử tạm với tài khoản Technician.
2. Tạo phiếu #2 ở trạng thái PENDING và kỹ thuật viên #2 đủ điều kiện.
3. Đăng nhập bằng tài khoản `technician_test`.
4. Gửi `POST /assignments/` với `ticket_id=2` và `technician_id=2`.
5. Quan sát HTTP status và bản ghi phân công trả về.

### 3. Expected / Actual trước khi sửa

- **Expected:** HTTP 403 Forbidden; Technician không được phân công.
- **Actual:** HTTP 201 Created; API tạo assignment #2 cho ticket #2.
- **Kết quả:** FAIL – tái hiện được lỗi phân quyền.

### 4. Nguyên nhân gốc

Router phân công chỉ yêu cầu xác thực ở cấp ứng dụng.
Endpoint tạo phân công chưa sử dụng dependency `require_manager`,
trong khi endpoint thay đổi kỹ thuật viên đã kiểm tra vai trò này.

### 5. Cách khắc phục

- Sử dụng lại dependency `require_manager` đã có.
- Bổ sung `Depends(require_manager)` cho `POST /assignments/`.
- Giữ nguyên các kiểm tra điều kiện nghiệp vụ trong Assignment Service.

### 6. Kiểm thử sau khi sửa

- Technician gọi `POST /assignments/`: HTTP 403 – PASS.
- Test `test_technician_cannot_assign_ticket`: PASS.
- Tại thời điểm sửa BUG-03, full regression: 87 passed, 0 failed, 1 warning.
- Kiểm tra cú pháp Python: PASS.
- `git diff --check`: không phát hiện lỗi định dạng.

### 7. Minh chứng

- Test: `tests/test_bug03_rbac.py`.
- Trước khi sửa: `docs/screenshots/BUG-03-assignment-before.png`.
- Sau khi sửa: `docs/screenshots/BUG-03-after.png`.
- Minh chứng bổ sung về tạo phiếu: `docs/screenshots/BUG-03-before.png`.
- Commit sửa lỗi: `6cc17ba`.

### 8. Giới hạn

Kiểm thử hiện xác nhận việc từ chối Technician tại API tạo phân công.
Chưa xác nhận đầy đủ phân quyền của tất cả endpoint nghiệp vụ khác.
