# NHẬT KÝ THAY ĐỔI THIẾT KẾ
## Smart CRM – Mekong Mobile
- Sinh viên: Nguyễn Minh Trị
- MSSV: 2374802010517
- Luồng: L4 – Phân công kỹ thuật viên và lịch hẹn
- Track: Software Engineering (SE)
- Ngày ghi nhận: 19/10/2026

## Sau phản hồi Bài tập 1 – Buổi 8

### TD-01 – Chuẩn hóa thông tin báo cáo
- Phản hồi của GV: Trang bìa thiếu link GitHub, mã luồng, track, lớp, ngày nộp; tên file chưa đúng mẫu.
- Quyết định: SỬA.
- Lý do: Bảo đảm giảng viên xác định được bài làm, repository và phiên bản tài liệu.
- Ảnh hưởng: Cập nhật trang bìa, tên file PDF và thông tin nộp bài ở các báo cáo tiếp theo.

### TD-02 – Bổ sung đặc tả Use Case trong báo cáo
- Phản hồi của GV: Báo cáo chỉ dẫn tới file usecase-spec.md, thiếu đặc tả trực tiếp.
- Quyết định: SỬA.
- Lý do: Giảng viên cần kiểm tra đầy đủ luồng xử lý mà không phải mở tài liệu khác.
- Ảnh hưởng: Bổ sung UC3 và UC5 vào báo cáo; cập nhật luồng chính, tiền/hậu điều kiện và ngoại lệ.

### TD-03 – Chuẩn hóa User Stories và MoSCoW
- Phản hồi của GV: Có 8 User Stories, vượt yêu cầu 5–7; chưa ghi rõ WON'T.
- Quyết định: SỬA.
- Lý do: Đáp ứng giới hạn đề bài và làm rõ phạm vi triển khai.
- Ảnh hưởng: Rà soát, gộp User Stories phù hợp; cập nhật SRS, ma trận truy vết và mục WON'T.

### TD-04 – Bổ sung chú thích sơ đồ
- Phản hồi của GV: Use Case, Architecture, ERD và Wireframe thiếu chú thích ký hiệu.
- Quyết định: SỬA.
- Lý do: Giúp người đọc hiểu đúng quan hệ, thành phần và luồng xử lý.
- Ảnh hưởng: Chỉnh sửa các file .drawio và xuất lại hình PNG.

### TD-05 – Làm rõ phạm vi kiến trúc
- Phản hồi của GV: Sơ đồ kiến trúc chưa ghi rõ NGOÀI PHẠM VI.
- Quyết định: SỬA.
- Lý do: Phân biệt chức năng L4 với các chức năng CRM không triển khai.
- Ảnh hưởng: Cập nhật architecture.drawio, architecture.png và architecture.md.

### TD-06 – Đưa SQL DDL vào báo cáo
- Phản hồi của GV: PDF chưa có SQL DDL skeleton.
- Quyết định: SỬA.
- Lý do: Cần chứng minh ERD có thể chuyển thành cấu trúc CSDL thực tế.
- Ảnh hưởng: Đưa DDL của 5 bảng vào báo cáo và sử dụng làm cơ sở tạo database ở Sprint 1.

### TD-07 – Hoàn thiện phụ lục sử dụng AI
- Phản hồi của GV: Thiếu cột Đã kiểm chứng thế nào và dòng cam kết có họ tên, MSSV, ngày.
- Quyết định: SỬA.
- Lý do: Minh bạch việc sử dụng AI và trách nhiệm kiểm tra sản phẩm.
- Ảnh hưởng: Cập nhật docs/ai-disclosure.md và phụ lục AI trong báo cáo.

### TD-08 – Bổ sung bảng thuật ngữ trong báo cáo
- Phản hồi của GV: Báo cáo thiếu bảng thuật ngữ.
- Quyết định: SỬA.
- Lý do: Giúp người đọc hiểu các thuật ngữ nghiệp vụ và kỹ thuật.
- Ảnh hưởng: Đưa bảng thuật ngữ từ SRS vào báo cáo và rà soát nội dung.

### TD-09 – Bảo đảm khả năng kiểm tra repository
- Phản hồi của GV: Không kiểm tra được repository và các file .drawio gốc.
- Quyết định: SỬA.
- Lý do: Giảng viên cần truy cập được tài liệu nguồn để đối chiếu với báo cáo.
- Ảnh hưởng: Kiểm tra quyền truy cập GitHub, nhánh nộp bài, đường dẫn tài liệu và các file .drawio.

## Trạng thái thực hiện
Các quyết định trên được ghi nhận trong Buổi 8.
Trạng thái: ĐÃ LÊN KẾ HOẠCH – CHƯA XÁC NHẬN HOÀN THÀNH.
Chỉ đánh dấu hoàn thành sau khi tài liệu, sơ đồ và repository
được cập nhật và kiểm chứng thực tế.

## Điều chỉnh phạm vi triển khai Sprint 1 – Buổi 10

### TD-10 – Ưu tiên luồng phân công kỹ thuật viên
- Quyết định: Triển khai trước luồng xem phiếu chờ phân công, xem kỹ thuật viên đủ điều kiện và thực hiện phân công.
- Lý do: Ưu tiên hoàn thiện luồng nghiệp vụ cốt lõi L4 từ Frontend đến API, Service và Database; bảo đảm có thể kiểm thử bằng dữ liệu thực.
- Ảnh hưởng: Các chức năng mở rộng tiếp tục được giữ trong tài liệu thiết kế nhưng không được đánh dấu là đã triển khai.

### TD-11 – Hoãn các chức năng mở rộng
- Quyết định: CHƯA TRIỂN KHAI thay đổi kỹ thuật viên kèm lý do (FR4/US4), đặt lịch giao – nhận (FR5/US5), kiểm tra xung đột lịch (FR8) và giao diện kỹ thuật viên xem công việc được giao (FR6/US6).
- Lý do: Giới hạn phạm vi Sprint 1 để tập trung kiểm chứng luồng phân công, các quy tắc nghiệp vụ và các trạng thái giao diện.
- Ảnh hưởng: Chưa có API hoặc giao diện hoàn chỉnh cho các chức năng trên. Cần tiếp tục triển khai và kiểm thử trong giai đoạn sau.
- Trạng thái: Đã ghi nhận quyết định phạm vi; chưa hoàn thành các chức năng được hoãn.

---

## Cập nhật thiết kế sau phiên bản v0.2

Ngày ghi nhận: 30/10/2026.

### TD-12 – Điều chỉnh ngưỡng tay nghề theo mức ưu tiên

- Quyết định: SỬA quy tắc lọc kỹ thuật viên.
- Nội dung: THAP yêu cầu proficiency >= 2; TRUNG_BINH >= 3; CAO >= 4.
- Lý do: Mức độ ưu tiên của phiếu cần được phản ánh trong yêu cầu năng lực kỹ thuật viên.
- Ảnh hưởng: Assignment Service, Repository, SRS và tài liệu kiến trúc.
- Trạng thái: Đã cập nhật mã nguồn và tài liệu; chờ kiểm thử lại.

### TD-13 – Bổ sung chức năng lịch hẹn

- Quyết định: TRIỂN KHAI BỔ SUNG sau Sprint 1.
- Nội dung: API xem lịch, lấy ngữ cảnh phiếu, kiểm tra xung đột và tạo lịch hẹn; bổ sung giao diện đặt lịch.
- Lý do: Tiếp tục hoàn thiện luồng L4 đã được xác định trong SRS.
- Ảnh hưởng: Appointment API, Frontend và API Contract.
- Trạng thái: Đã ghi nhận endpoint; chờ kiểm thử tích hợp.

### TD-14 – Bổ sung đăng nhập và quản lý phiên

- Quyết định: TRIỂN KHAI BỔ SUNG.
- Nội dung: API đăng nhập, kiểm tra phiên, đăng xuất và giao diện yêu cầu đăng nhập.
- Lý do: Bổ sung khả năng nhận diện người dùng khi thao tác trên giao diện.
- Ảnh hưởng: Authentication API, Frontend và Database.
- Giới hạn: Các Business API chưa được bảo vệ đồng bộ bằng xác thực.
- Trạng thái: Đã ghi nhận endpoint; chờ kiểm thử lại.

### TD-15 – Mở rộng giao diện nghiệp vụ

- Quyết định: TRIỂN KHAI BỔ SUNG.
- Nội dung: Màn hình danh sách phiếu, chi tiết phiếu, phân công kỹ thuật viên và đặt lịch hẹn.
- Lý do: Hỗ trợ thao tác luồng L4 trực tiếp trên giao diện.
- Ảnh hưởng: Các thành phần Frontend và tài liệu README.
- Trạng thái: Đã cập nhật mã nguồn; chờ kiểm thử tích hợp.

## Ghi chú kiểm chứng

Các trạng thái trên phản ánh thay đổi đã ghi nhận trong mã nguồn
và tài liệu. Chỉ xác nhận chức năng hoàn thành sau khi kiểm thử
Backend, Frontend và các quy tắc nghiệp vụ thành công.

TD-10 và TD-11 vẫn được giữ nguyên như lịch sử quyết định Sprint 1.

---

## Cập nhật sau kiểm thử Buổi 14

Ngày ghi nhận: 06/11/2026.

### TD-16 – Bảo vệ API nghiệp vụ bằng xác thực

- Quyết định: SỬA.
- Lý do: Kiểm thử phát hiện API nghiệp vụ cho phép
  truy cập khi chưa đăng nhập (BUG-01).
- Nội dung: Bổ sung xác thực Bearer token cho các
  business router và cập nhật Frontend API client.
- Minh chứng: Commit `6cc8aa3`, BUG-01.
- Trạng thái: Đã sửa và kiểm thử.

### TD-17 – Hoàn thiện thay đổi kỹ thuật viên kèm lý do

- Quyết định: TRIỂN KHAI BỔ SUNG.
- Lý do: Hoàn thiện FR4/US4 đã được hoãn tại TD-11.
- Nội dung: Manager có thể thay đổi kỹ thuật viên
  của phiếu ASSIGNED, bắt buộc nhập lý do.
- Quy tắc: Kỹ thuật viên mới phải đủ điều kiện về
  trung tâm, trạng thái, kỹ năng và workload.
- Dữ liệu: Kết thúc phân công cũ, tạo phân công mới
  trong cùng transaction và giữ lịch sử.
- Giao diện: Bổ sung form đổi kỹ thuật viên và
  bảng lịch sử phân công.
- Minh chứng: Commit `e601110`, BUG-02.
- Kiểm thử: 86 passed, 0 failed, 1 warning.
- Trạng thái: Đã triển khai và kiểm thử.

### TD-18 – Kiểm soát quyền tạo phân công kỹ thuật viên

- Quyết định: SỬA.
- Lý do: BUG-03 cho phép Technician tạo phân công
  thông qua API dù FR3/US3 quy định Manager thực hiện.
- Nội dung: Bổ sung dependency `require_manager`
  cho endpoint `POST /assignments/`.
- Expected: Technician nhận HTTP 403 Forbidden.
- Minh chứng: Commit `6cc17ba`, BUG-03.
- Kiểm thử: Tại thời điểm sửa lỗi, 87 passed,
  0 failed, 1 warning.
- Trạng thái: Đã sửa và kiểm thử.

### Ghi chú

TD-11 phản ánh quyết định phạm vi tại Sprint 1.
TD-17 ghi nhận việc hoàn thiện chức năng trong
giai đoạn sau, không thay thế lịch sử TD-11.

BUG-02 được phân loại là Requirement Gap,
không phải lỗi runtime đã được tái hiện.

---

## Cập nhật thiết kế BT3 – Buổi 16

Ngày ghi nhận: 13/11/2026.

### TD-19 – Đóng gói hệ thống bằng Docker Compose

- Quyết định: Đóng gói Backend FastAPI và Frontend thành các container riêng.
- Lý do: Hỗ trợ triển khai prototype nhất quán và giảm phụ thuộc vào cấu hình máy phát triển.
- Ảnh hưởng: compose.yaml, Dockerfiles, .env.example và Deployment Guide.
- Kiểm chứng: Docker Compose chạy thành công, các container ở trạng thái healthy.

### TD-20 – Sử dụng Nginx reverse proxy

- Quyết định: Frontend Nginx chuyển tiếp các yêu cầu API đến Backend trong mạng Docker.
- Lý do: Hạn chế vấn đề cấu hình API URL và hỗ trợ truy cập qua cùng một origin.
- Ảnh hưởng: Cấu hình Nginx, Frontend build và Docker deployment.
- Kiểm chứng: Giao diện và API hoạt động qua reverse proxy trong clean-room.

### TD-21 – Bổ sung healthcheck và kiểm tra tái lập

- Quyết định: Kiểm tra trạng thái container, triển khai trên clean-room riêng và xác minh seed idempotency.
- Lý do: Tăng khả năng tái lập và tránh tác động đến database phát triển.
- Ảnh hưởng: Docker Compose, scripts/init_db.py, tài liệu triển khai và ảnh minh chứng.
- Kiểm chứng: Clean-room deployment thành công; chạy seed hai lần không tạo dữ liệu trùng trong database kiểm thử.
- Ghi chú lịch sử: Tại thời điểm TD-21, chưa xác nhận triển khai từ GitHub public tag v1.0. Việc fresh clone và kiểm chứng Docker đã được thực hiện sau đó; xem TD-24.

### TD-22 – Mở rộng kiểm thử và tài liệu kỹ thuật

- Quyết định: Bổ sung regression evidence, API Reference, Security Checklist và AI Disclosure cho BT3.
- Lý do: Đáp ứng yêu cầu kiểm thử, bảo mật và bàn giao prototype.
- Ảnh hưởng: docs/test-report.md, docs/api-reference-bt3.md, docs/checklist-bao-mat.md và docs/ai-disclosure.md.
- Kiểm chứng: 87 pytest PASS; 11/11 HTTP 401 PASS; 4/4 HTTP 403 PASS; 28 API được tài liệu hóa.
- Giới hạn: Không phải mọi API đều đã được kiểm thử request/response thực tế.

### TD-23 – Triển khai công khai trên Render

- Quyết định: Sử dụng Render Web Service với Dockerfile riêng để triển khai công khai prototype.
- Lý do: Cung cấp môi trường demo qua URL công khai và đáp ứng phần điểm cộng BT3.
- Kiến trúc: Nginx lắng nghe cổng 10000, chuyển tiếp API đến FastAPI trên localhost:8000.
- Dữ liệu: SQLite tại `/app/data/smartcrm.db`; cần đối chiếu cấu hình lưu trữ thực tế trên Render.
- Ảnh hưởng: `Dockerfile.render`, `nginx.render.conf`, `scripts/render-start.sh` và Deployment Guide.
- Minh chứng: Bảy ảnh tại `evidence/Render/`, gồm triển khai, đăng nhập, phân công và kiểm tra dữ liệu.
- Giới hạn: Không khẳng định mọi cấu hình production security đã được kiểm chứng.

### TD-24 – Đồng bộ kết quả kiểm thử và tài liệu phát hành BT3

- Quyết định: Giữ kết quả kiểm thử cũ như lịch sử và bổ sung kết quả mới nhất.
- Kiểm chứng: 100 pytest PASS, 0 failed, 1 warning; 11/11 HTTP 401 và 4/4 HTTP 403.
- Kiểm chứng tái lập: Đã fresh clone từ GitHub public tag v1.0 trong môi trường Docker độc lập.
- Giới hạn: Cần đồng bộ lại tag v1.0 sau commit tài liệu cuối cùng.
