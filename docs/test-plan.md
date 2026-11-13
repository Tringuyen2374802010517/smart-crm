# TEST PLAN – SMART CRM L4

- Sinh viên: Nguyễn Minh Trị
- MSSV: 2374802010517
- Track: Software Engineering (SE)
- Phiên bản kiểm thử: Buổi 14 – 06/11/2026

## 1. Mục tiêu và phạm vi

Kiểm tra các chức năng chính của luồng L4:
quản lý phiếu, phân công kỹ thuật viên,
thay đổi kỹ thuật viên, lịch sử phân công,
đặt lịch hẹn và xác thực người dùng.

Tập trung kiểm tra yêu cầu nghiệp vụ,
tính đúng đắn của dữ liệu và kiểm soát truy cập.

Ngoài phạm vi: kiểm thử tải production,
kiểm thử hiệu năng quy mô lớn và pentest chuyên sâu.

## 2. Môi trường và dữ liệu

- Backend: Python, FastAPI.
- Frontend: Vite, JavaScript.
- Database: SQLite.
- Automated testing: pytest.
- Trình duyệt: môi trường phát triển trên macOS.
- Dữ liệu: phiếu sửa chữa, kỹ thuật viên,
  phân công và lịch hẹn trong database kiểm thử.
- Vai trò: Manager, Technician và người chưa đăng nhập.

## 3. Phương pháp kiểm thử

- Functional: kiểm tra luồng nghiệp vụ hợp lệ.
- Boundary: kiểm tra giá trị biên và giới hạn.
- Invalid input: kiểm tra dữ liệu không hợp lệ.
- Security/Data: kiểm tra xác thực, phân quyền
  và tính nhất quán của database.
- Regression: chạy lại pytest sau khi sửa lỗi.

Mỗi test case ghi nhận Expected, Actual,
Status và đường dẫn ảnh minh chứng.
Không đánh dấu PASS nếu chưa thực thi.

## 4. Tiêu chí hoàn thành

- Thực thi và ghi nhận 10–12 test case.
- Bao phủ các nhóm kiểm thử đã xác định.
- Không còn test case Critical/Major thất bại
  chưa được xử lý hoặc giải thích.
- Lỗi phát hiện được ghi vào Bug Log,
  kèm cách tái hiện và minh chứng sửa lỗi.
- Chạy full regression bằng pytest.
- Lưu ảnh kiểm thử trong docs/screenshots/.

## 5. Phụ lục BT3 – Packaging, Deployment and Security

Ngày cập nhật: 10/11/2026.

### 5.1. Mục tiêu

Kiểm tra khả năng đóng gói, triển khai, vận hành và bảo vệ API của Smart CRM trong môi trường Docker.

### 5.2. Môi trường

- Docker Desktop và Docker Compose.
- Backend: FastAPI, Python 3.12.
- Frontend: Vite, Nginx.
- Database: SQLite lưu trên Docker named volume.
- Môi trường triển khai chính: frontend 5173, backend 8000.
- Môi trường clean-room: frontend 15173, backend 18000.
- Automated regression: pytest.

### 5.3. Các trường hợp kiểm thử

| ID | Hạng mục | Kết quả mong đợi |
|---|---|---|
| BT3-TC-01 | Docker Compose deployment | Backend và frontend khởi động thành công, healthcheck đạt |
| BT3-TC-02 | Backend healthcheck | GET /health trả HTTP 200 và database connected |
| BT3-TC-03 | Frontend | Giao diện tải thành công với HTTP 200 |
| BT3-TC-04 | SQLite persistence | Dữ liệu được giữ nguyên sau khi recreate backend container |
| BT3-TC-05 | Clean-room deployment | Hệ thống triển khai trên cổng riêng, volume độc lập |
| BT3-TC-06 | Nginx reverse proxy | GET /api/health được chuyển tiếp đến backend thành công |
| BT3-TC-07 | Authentication | Đăng nhập qua frontend proxy và truy vấn /api/auth/me thành công |
| BT3-TC-08 | Unauthenticated API | Bốn API nghiệp vụ đại diện trả HTTP 401 khi không có token |
| BT3-TC-09 | Regression | Toàn bộ bài kiểm thử pytest hoàn thành, không có test thất bại |

### 5.4. Tiêu chí hoàn thành

- Ghi nhận kết quả thực tế và trạng thái từng trường hợp kiểm thử.
- Lưu log regression tại docs/test-results-bt3.txt.
- Lưu ảnh minh chứng cần thiết tại docs/screenshots/.
- Không đánh dấu PASS cho trường hợp chưa được kiểm chứng.
- Ghi rõ giới hạn của kiểm thử bảo mật và môi trường triển khai.
