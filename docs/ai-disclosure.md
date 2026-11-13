# AI Disclosure

## Smart CRM – Mekong Mobile

**Luồng nghiệp vụ:** L4 – Phân công kỹ thuật viên và lịch hẹn
**Track:** SE

---

## 1. Thông tin sử dụng AI

| Công cụ AI | Mục đích sử dụng | Nội dung được hỗ trợ | Cách kiểm tra / chỉnh sửa |
|---|---|---|---|
| ChatGPT | Hỗ trợ phân tích, soạn thảo tài liệu và xây dựng nội dung sơ đồ | SRS, User Stories, Acceptance Criteria, Use Case Specification, Use Case Diagram, Architecture, Data Model, SQL DDL, Wireframe và API Contract | Đối chiếu với phạm vi L4, yêu cầu BT1 và case study; kiểm tra và chỉnh sửa nội dung để bảo đảm phù hợp với yêu cầu bài tập |
| Draw.io AI | Hỗ trợ tạo sơ đồ và wireframe | Architecture Diagram, ERD và Wireframe | Kiểm tra lại thành phần, quan hệ, PK/FK, trường dữ liệu, bố cục và phạm vi chức năng trước khi lưu |

---

## 2. Nội dung do sinh viên thực hiện

Sinh viên xác định phạm vi L4 – Phân công kỹ thuật viên và lịch hẹn, lựa chọn nội dung phù hợp với yêu cầu bài tập, kiểm tra kết quả do AI hỗ trợ và chịu trách nhiệm đối với nội dung cuối cùng được đưa vào bài nộp.

Các kết quả do AI hỗ trợ được sinh viên kiểm tra và chỉnh sửa trước khi sử dụng. Nội dung được đối chiếu với yêu cầu BT1, case study Smart CRM – Mekong Mobile và phạm vi nghiệp vụ đã chọn.

---

## 3. Cam kết

Tôi xác nhận đã khai báo việc sử dụng công cụ AI trong quá trình thực hiện BT1. Tôi đã kiểm tra, chỉnh sửa và chịu trách nhiệm về tính phù hợp của toàn bộ nội dung trong bài nộp.

**Sinh viên:** Nguyễn Minh Trị
**MSSV:** 2374802010517
**Track:** SE
**Luồng:** L4 – Phân công kỹ thuật viên và lịch hẹn
**Ngày khai báo:** 02/10/2026

---

## 4. Bổ sung khai báo sử dụng AI trong BT2

**Giai đoạn:** Sprint 1 – BT2
**Ngày cập nhật:** 30/10/2026

| Công cụ AI | Nội dung hỗ trợ | Cách kiểm chứng |
|---|---|---|
| ChatGPT | Hỗ trợ phân tích và hướng dẫn triển khai CRUD cho Ticket và Technician; tổ chức Controller/API, Service, Repository; xử lý lỗi nghiệp vụ; xây dựng và rà soát test cases; cải thiện schema, seed, README và Bug Log | Sinh viên thực hiện các thao tác trong repository, kiểm tra thay đổi bằng Git, chạy pytest, kiểm tra API và đối chiếu với yêu cầu BT2 |
| ChatGPT | Hỗ trợ hướng dẫn kiểm tra khả năng tái lập dự án và quy trình Git | Kiểm tra fresh clone, cài đặt dependencies, khởi tạo SQLite, chạy 25 bài kiểm thử, build frontend và xác nhận commit trên GitHub |

### Kết quả kiểm chứng

- 25/25 bài kiểm thử pytest thành công trên bản clone cục bộ.
- Frontend build thành công bằng `npm run build`.
- Khởi tạo schema và seed trên database mới thành công.
- Clone repository trực tiếp từ GitHub thành công tại commit `82f35f3`.
- Các thay đổi được lưu trong lịch sử Git và có thể đối chiếu.

### Cam kết

Tôi đã kiểm tra kết quả được AI hỗ trợ, thực hiện các thao tác triển khai và kiểm thử trên môi trường phát triển, đồng thời chịu trách nhiệm về nội dung bài nộp BT2.

**Sinh viên:** Nguyễn Minh Trị
**MSSV:** 2374802010517

---

## 5. Bổ sung khai báo sử dụng AI trong BT3

**Giai đoạn:** Buổi 16 – Đóng gói prototype và tài liệu kỹ thuật

**Ngày cập nhật:** 13/11/2026

| Công cụ AI | Mục đích sử dụng | Nội dung được hỗ trợ | Cách kiểm chứng / chỉnh sửa |
|---|---|---|---|
| ChatGPT | Hỗ trợ hướng dẫn triển khai và rà soát kỹ thuật | Docker Compose, Nginx reverse proxy, healthcheck, Deployment Guide | Sinh viên chạy Docker trên máy, kiểm tra container healthy, giao diện và API trên môi trường clean-room |
| ChatGPT | Hỗ trợ tổ chức tài liệu kiểm thử | Test Plan, Test Report, Bug Log và regression evidence | Đối chiếu test case, kết quả pytest, ảnh minh chứng và fixing commits trong Git |
| ChatGPT | Hỗ trợ rà soát API và bảo mật | API Reference, OpenAPI, phân quyền và Security Checklist | Đối chiếu mã nguồn, schema, HTTP 200/401/403 và ghi rõ những trường hợp chưa kiểm chứng |
| ChatGPT | Hỗ trợ kiểm tra khả năng tái lập | Deployment Guide, seed idempotency và quy trình phát hành | Chạy thử trên SQLite và Docker clean-room riêng biệt; kiểm tra kết quả trước khi kết luận |

**Giới hạn:** Các ví dụ request/response minh họa không được xem là kết quả kiểm thử runtime. Việc triển khai từ GitHub public tag v1.0 chỉ được xác nhận sau khi thực hiện thành công.

**Cam kết:** Sinh viên kiểm tra, chỉnh sửa và chịu trách nhiệm về nội dung cuối cùng của BT3.

**Sinh viên:** Nguyễn Minh Trị

**MSSV:** 2374802010517

## 6. Cập nhật khai báo AI – Hoàn thiện tài liệu BT3

**Ngày cập nhật:** 14/11/2026

- Công cụ: ChatGPT.
- Nội dung hỗ trợ: Rà soát tính nhất quán giữa README, Test Report, Deployment Guide, Design Changes và AI Disclosure; hướng dẫn ghi nhận minh chứng triển khai Render.
- Cách kiểm chứng: Sinh viên đối chiếu cấu hình Dockerfile, Nginx, startup script, kết quả kiểm thử và các ảnh minh chứng thực tế.
- Giới hạn: Nội dung hướng dẫn không thay thế việc kiểm tra cấu hình Render thực tế hoặc xác nhận bảo mật production.
- Cam kết: Sinh viên kiểm tra, chỉnh sửa và chịu trách nhiệm về tài liệu cuối cùng.
