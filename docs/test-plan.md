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
