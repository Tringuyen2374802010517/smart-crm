# Architecture – Smart CRM Mekong Mobile

**Luồng nghiệp vụ:** L4 – Phân công kỹ thuật viên và lịch hẹn  
**Track:** SE

---

## 1. Kiến trúc tổng quan

Hệ thống sử dụng kiến trúc 3 lớp đơn giản gồm:

1. Frontend / Web Interface
2. Backend API / Business Logic
3. Database / Smart CRM Data

Luồng trao đổi chính:

Frontend / Web Interface → Backend API / Business Logic → Database / Smart CRM Data

---

## 2. Thành phần kiến trúc

### 2.1. Frontend / Web Interface

Frontend cung cấp giao diện cho Quản lý trung tâm và Kỹ thuật viên thực hiện các chức năng thuộc luồng L4.

Trách nhiệm chính:

- Hiển thị danh sách phiếu cần phân công.
- Hiển thị danh sách kỹ thuật viên khả dụng.
- Cho phép quản lý chọn và phân công kỹ thuật viên.
- Cho phép thay đổi kỹ thuật viên phụ trách.
- Cho phép nhập thông tin lịch giao – nhận máy.
- Hiển thị thông báo khi kỹ thuật viên không đáp ứng điều kiện phân công.
- Hiển thị thông báo khi xảy ra xung đột lịch.
- Cho phép kỹ thuật viên xem công việc và lịch hẹn được giao.

### 2.2. Backend API / Business Logic

Backend tiếp nhận yêu cầu từ Frontend, xử lý các quy tắc nghiệp vụ và trao đổi dữ liệu với Database.

Trách nhiệm chính:

- Truy vấn các phiếu cần phân công.
- Truy vấn danh sách kỹ thuật viên khả dụng.
- Tính khối lượng công việc hiện tại (`current_workload`) của mỗi kỹ thuật viên bằng cách đếm số bản ghi Assignment đang hoạt động (`ended_at IS NULL`), thay vì lưu trực tiếp trong bảng Technician.
- Xử lý phân công và thay đổi kỹ thuật viên.
- Thực hiện UC7 – Kiểm tra điều kiện phân công.
- Kiểm tra proficiency ≥ 3 và kỹ thuật viên thuộc cùng trung tâm.
- Xử lý việc tạo lịch giao – nhận máy.
- Thực hiện UC8 – Kiểm tra trùng lịch.
- Truy vấn công việc và lịch hẹn của kỹ thuật viên.
- Ghi nhận dữ liệu phân công và lịch hẹn hợp lệ vào Database.

### 2.3. Database / Smart CRM Data

Database lưu trữ dữ liệu cần thiết cho luồng L4.

Các nhóm dữ liệu chính:

- Phiếu (Ticket).
- Kỹ thuật viên (Technician).
- Kỹ năng của kỹ thuật viên (Technician Skill).
- Phân công kỹ thuật viên (Assignment).
- Lịch hẹn (Appointment).

---

## 3. Luồng xử lý chính

### 3.1. Phân công kỹ thuật viên

1. Quản lý trung tâm chọn phiếu cần phân công trên Frontend.
2. Frontend gửi yêu cầu tới Backend API.
3. Backend lấy dữ liệu kỹ thuật viên từ Database.
4. Quản lý chọn kỹ thuật viên.
5. Backend kiểm tra điều kiện phân công theo UC7.
6. Nếu hợp lệ, Backend ghi nhận phân công vào Database.
7. Frontend hiển thị kết quả cho Quản lý trung tâm.

### 3.2. Đặt lịch giao – nhận máy

1. Quản lý trung tâm nhập thông tin lịch trên Frontend.
2. Frontend gửi thông tin lịch tới Backend API.
3. Backend kiểm tra trùng lịch theo UC8 bằng dữ liệu trong Database.
4. Nếu không có xung đột, Backend ghi nhận lịch hẹn.
5. Frontend hiển thị kết quả cho Quản lý trung tâm.

---

## 4. Lập luận lựa chọn kiến trúc

**NFR1:** Vì NFR1 yêu cầu hệ thống hiển thị danh sách phiếu hoặc kỹ thuật viên trong thời gian không quá 2 giây với tối đa 100 bản ghi, tôi chọn Backend API chỉ truy vấn và trả về các dữ liệu cần thiết cho giao diện, đánh đổi là cần thiết kế truy vấn và API phù hợp để hạn chế dữ liệu không cần thiết.

**NFR2:** Vì NFR2 yêu cầu thao tác phân công kỹ thuật viên hoặc đặt lịch phản hồi trong thời gian không quá 2 giây, tôi chọn xử lý các Business Rule tại Backend trước khi ghi dữ liệu vào Database, đánh đổi là Backend phải đảm nhận nhiều logic nghiệp vụ hơn.

**NFR3:** Vì NFR3 yêu cầu quy trình phân công kỹ thuật viên hoàn thành trong tối đa 5 bước tương tác chính, tôi chọn thiết kế Frontend tập trung vào luồng chọn phiếu → xem kỹ thuật viên → chọn kỹ thuật viên → xác nhận phân công, đánh đổi là giao diện được thiết kế chuyên biệt hơn cho luồng L4.