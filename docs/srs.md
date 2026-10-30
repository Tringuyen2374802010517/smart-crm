SRS Rút Gọn – Smart CRM Mekong Mobile
Sinh viên: Nguyễn Minh Trị

MSSV: 2374802010517

Track: SE

Luồng nghiệp vụ: L4 – Phân công kỹ thuật viên và lịch hẹn
1. Giới thiệu và phạm vi
1.1. Bối cảnh
Smart CRM – Mekong Mobile hỗ trợ hoạt động quản lý dịch vụ sửa chữa thiết bị. Trong luồng L4, quản lý trung tâm cần phân công kỹ thuật viên phù hợp cho các phiếu cần xử lý và quản lý lịch giao – nhận máy.
1.2. Phạm vi
Hệ thống hỗ trợ:
- Xem các phiếu đang cần phân công kỹ thuật viên.
- Xem các kỹ thuật viên đang khả dụng.
- Kiểm tra trạng thái khả dụng, kỹ năng và trung tâm của kỹ thuật viên.
- Phân công kỹ thuật viên cho phiếu.
- Thay đổi kỹ thuật viên phụ trách và ghi nhận lý do.
- Đặt lịch giao – nhận máy.
- Kiểm tra trùng lịch trước khi xác nhận lịch hẹn.
- Cho phép kỹ thuật viên xem công việc và lịch hẹn được giao.
1.3. Ngoài phạm vi
Bài tập không thực hiện:
- Quản lý toàn bộ quy trình CRM của Mekong Mobile.
- Quản lý thanh toán và hóa đơn.
- Quản lý kho và linh kiện.
- Xây dựng chức năng đăng nhập và phân quyền chi tiết.
- Triển khai hệ thống thực tế.
1.4. Bảng thuật ngữ
Thuật ngữ	Giải thích
Phiếu (Ticket)	Phiếu ghi nhận yêu cầu hoặc sự cố cần được xử lý
Kỹ thuật viên (Technician)	Nhân viên kỹ thuật được phân công xử lý phiếu
Phân công (Assignment)	Việc gán kỹ thuật viên phụ trách một phiếu
Lịch hẹn (Appointment)	Thời gian giao hoặc nhận máy đã được lên lịch
Proficiency	Mức độ thành thạo của kỹ thuật viên đối với nhóm sự cố
Workload	Khối lượng công việc hiện tại của kỹ thuật viên
Trung tâm (Center)	Trung tâm nơi phiếu và kỹ thuật viên được quản lý
PENDING	Trạng thái phiếu đang chờ phân công
AVAILABLE	Trạng thái kỹ thuật viên đang khả dụng
MoSCoW	Phương pháp phân loại mức độ ưu tiên yêu cầu thành MUST, SHOULD, COULD và WON'T


2. Các bên liên quan và vai trò người dùng
Vai trò	Trách nhiệm
Quản lý trung tâm	Xem phiếu cần phân công, xem kỹ thuật viên khả dụng, kiểm tra điều kiện phân công, phân công hoặc thay đổi kỹ thuật viên, đặt lịch và kiểm tra trùng lịch
Kỹ thuật viên	Xem các phiếu và lịch hẹn được giao cho mình
Khách hàng	Liên quan đến hoạt động giao – nhận máy nhưng không trực tiếp thực hiện chức năng quản lý trong phạm vi bài tập


3. Yêu cầu chức năng và User Stories
3.1. Functional Requirements
FR1 – Xem phiếu cần phân công

Hệ thống phải cho phép quản lý trung tâm xem danh sách các phiếu đang chờ phân công kỹ thuật viên.

FR2 – Xem kỹ thuật viên khả dụng

Hệ thống phải cho phép quản lý trung tâm xem danh sách kỹ thuật viên khả dụng cùng thông tin về kỹ năng, khu vực và khối lượng công việc hiện tại.

FR3 – Phân công kỹ thuật viên

Hệ thống phải cho phép quản lý trung tâm phân công một kỹ thuật viên phù hợp cho một phiếu đang chờ phân công.

FR4 – Thay đổi kỹ thuật viên

Hệ thống phải cho phép quản lý trung tâm thay đổi kỹ thuật viên phụ trách và ghi nhận lý do thay đổi.

FR5 – Đặt lịch giao – nhận máy

Hệ thống phải cho phép quản lý trung tâm tạo lịch giao – nhận máy cho phiếu.

FR6 – Xem công việc được giao

Hệ thống phải cho phép kỹ thuật viên xem các phiếu và lịch hẹn được giao cho mình.

FR7 – Kiểm tra điều kiện phân công

Trước khi xác nhận phân công, hệ thống phải kiểm tra trạng thái khả dụng của kỹ thuật viên, mức proficiency phù hợp, trung tâm và tình trạng phân công hiện tại của phiếu.

FR8 – Kiểm tra trùng lịch

Hệ thống phải kiểm tra xung đột lịch trước khi xác nhận lịch giao – nhận máy.
3.2. User Stories và MoSCoW
MUST HAVE
US1 – Xem phiếu cần phân công

Là quản lý trung tâm, tôi muốn xem các phiếu đang chờ phân công để xác định phiếu cần xử lý.

US2 – Xem kỹ thuật viên khả dụng

Là quản lý trung tâm, tôi muốn xem các kỹ thuật viên đang khả dụng cùng thông tin kỹ năng, khu vực và khối lượng công việc để lựa chọn người phù hợp.

US3 – Phân công kỹ thuật viên

Là quản lý trung tâm, tôi muốn phân công kỹ thuật viên đáp ứng điều kiện về trạng thái khả dụng, kỹ năng và trung tâm cho một phiếu để xác định người chịu trách nhiệm xử lý.
SHOULD HAVE
US4 – Thay đổi kỹ thuật viên

Là quản lý trung tâm, tôi muốn thay đổi kỹ thuật viên phụ trách và ghi nhận lý do để điều chỉnh phân công khi cần thiết.

US5 – Đặt lịch giao – nhận máy

Là quản lý trung tâm, tôi muốn đặt lịch giao – nhận máy có kiểm tra trùng lịch để tránh xung đột thời gian.
COULD HAVE
US6 – Xem công việc được giao

Là kỹ thuật viên, tôi muốn xem các phiếu và lịch hẹn được giao để theo dõi công việc của mình.
WON'T HAVE – Trong phạm vi bài tập
Không triển khai:
- Chức năng thanh toán và xuất hóa đơn.
- Chức năng quản lý kho và linh kiện.
- Chức năng đăng nhập và phân quyền chi tiết.
- Toàn bộ quy trình CRM.
- Triển khai hệ thống thực tế.
Các nội dung WON'T được xác định là ngoài phạm vi, không phải User Stories cần triển khai trong bài tập này.
3.3. Acceptance Criteria cho các User Story MUST
US1 – Xem phiếu cần phân công
AC1 – Hiển thị phiếu chờ phân công
- Given: Quản lý trung tâm đang sử dụng hệ thống.
- When: Quản lý mở danh sách phiếu cần phân công.
- Then: Hệ thống hiển thị các phiếu có trạng thái PENDING.
AC2 – Hiển thị thông tin phiếu
- Given: Danh sách có nhiều phiếu.
- When: Hệ thống hiển thị danh sách.
- Then: Mỗi phiếu có mã phiếu, tiêu đề, mức ưu tiên, trạng thái và trung tâm.
US2 – Xem kỹ thuật viên khả dụng
AC1 – Hiển thị kỹ thuật viên khả dụng
- Given: Quản lý đã chọn một phiếu cần phân công.
- When: Quản lý yêu cầu xem kỹ thuật viên khả dụng.
- Then: Hệ thống hiển thị danh sách kỹ thuật viên có trạng thái AVAILABLE đáp ứng điều kiện lựa chọn.
AC2 – Hiển thị thông tin kỹ thuật viên
- Given: Danh sách kỹ thuật viên khả dụng được hiển thị.
- When: Quản lý xem thông tin kỹ thuật viên.
- Then: Hệ thống hiển thị kỹ năng, khu vực, khối lượng công việc và trạng thái khả dụng theo dữ liệu được quản lý.
AC3 – Không đề xuất kỹ thuật viên không phù hợp
- Given: Kỹ thuật viên không đáp ứng điều kiện về kỹ năng hoặc trung tâm.
- When: Hệ thống xác định danh sách kỹ thuật viên đủ điều kiện cho phiếu.
- Then: Kỹ thuật viên đó không xuất hiện trong danh sách đủ điều kiện.
US3 – Phân công kỹ thuật viên
AC1 – Phân công thành công
- Given: Phiếu có trạng thái PENDING, chưa có phân công đang hoạt động và kỹ thuật viên đáp ứng các điều kiện.
- When: Quản lý xác nhận phân công.
- Then: Hệ thống tạo bản ghi phân công và xác định kỹ thuật viên phụ trách phiếu.
AC2 – Từ chối kỹ thuật viên không phù hợp
- Given: Kỹ thuật viên không AVAILABLE, không cùng trung tâm hoặc có proficiency thấp hơn ngưỡng yêu cầu theo mức ưu tiên của phiếu.
- When: Quản lý thực hiện phân công.
- Then: Hệ thống từ chối phân công và thông báo lý do.
AC3 – Ngăn phân công trùng
- Given: Phiếu đã có phân công đang hoạt động.
- When: Quản lý cố gắng phân công thêm kỹ thuật viên.
- Then: Hệ thống từ chối tạo phân công mới.
4. Yêu cầu phi chức năng
NFR1 – Hiệu năng danh sách

Hệ thống phải hiển thị danh sách phiếu hoặc kỹ thuật viên trong thời gian không quá 2 giây với tối đa 100 bản ghi.

NFR2 – Hiệu năng thao tác

Hệ thống phải phản hồi thao tác phân công kỹ thuật viên trong thời gian không quá 2 giây trong điều kiện kiểm thử xác định. Thời gian phản hồi được tính từ khi API tiếp nhận yêu cầu đến khi API hoàn tất trả kết quả; không bao gồm thời gian truyền mạng và hiển thị giao diện.

Điều kiện kiểm thử đề xuất:
- Bộ dữ liệu gồm 100 phiếu (Ticket), 50 kỹ thuật viên (Technician) và các dữ liệu kỹ năng, phân công liên quan.
- Có 5 người dùng đồng thời gửi yêu cầu phân công hợp lệ trong môi trường kiểm thử xác định.
- Thực hiện ít nhất 30 yêu cầu hợp lệ; ghi nhận thời gian phản hồi từng yêu cầu.
- Tiêu chí đạt: Ít nhất 95% số yêu cầu có thời gian phản hồi không quá 2 giây.
Đối với chức năng đặt lịch giao – nhận máy, mục tiêu phản hồi cũng là không quá 2 giây; việc đo kiểm sẽ thực hiện khi chức năng này được triển khai. Các điều kiện và ngưỡng trên là tiêu chí kiểm thử dự kiến, chưa phải kết quả đo thực tế.

NFR3 – Khả dụng thao tác

Người quản lý phải có thể hoàn thành quy trình phân công kỹ thuật viên trong tối đa 5 bước tương tác chính, tính từ danh sách phiếu cần phân công.

Các NFR là tiêu chí mục tiêu của hệ thống; việc đạt các tiêu chí cần được kiểm chứng bằng thử nghiệm tương ứng.
5. Ràng buộc và Business Rules
BR1 – Phân công kỹ thuật viên

Tại một thời điểm, một phiếu chỉ được gán cho tối đa một kỹ thuật viên đang phụ trách. Khi thay đổi kỹ thuật viên phải ghi nhận lý do thay đổi.

BR2 – Điều kiện kỹ thuật viên

Kỹ thuật viên chỉ được phân công khi:
- Có trạng thái AVAILABLE.
- Có kỹ năng phù hợp với nhóm sự cố của phiếu.
- Đáp ứng ngưỡng proficiency theo mức ưu tiên:
  - THAP: proficiency ≥ 2.
  - TRUNG_BINH: proficiency ≥ 3.
  - CAO: proficiency ≥ 4.
- Proficiency được đánh giá trên thang điểm từ 1 đến 5.
- Thuộc cùng trung tâm với phiếu.
BR3 – Điều kiện trạng thái phiếu

Hệ thống chỉ cho phép tạo phân công mới đối với các phiếu có trạng thái PENDING và chưa có phân công đang hoạt động.

Trường hợp thay đổi kỹ thuật viên phụ trách được xử lý theo quy trình riêng của FR4, phải bảo đảm không tồn tại đồng thời hai phân công đang hoạt động cho cùng một phiếu.

BR4 – Thời hạn cam kết

Thời hạn cam kết xử lý theo mức ưu tiên:
- CAO: 24 giờ.
- TRUNG_BINH: 72 giờ.
- THAP: 120 giờ.
Ngày làm việc được tính từ Thứ Hai đến Thứ Bảy.
Ghi chú về phạm vi dữ liệu trung tâm: ticket.center_id và technician.center_id dùng để kiểm tra điều kiện cùng trung tâm theo BR2. Bảng center nằm ngoài phạm vi mô hình dữ liệu của bài tập, vì vậy hai trường này chưa được ràng buộc bằng khóa ngoại đến bảng center. Đây là giới hạn thiết kế cần được xem xét nếu mở rộng hệ thống, không phải xác nhận rằng toàn vẹn tham chiếu đã được bảo đảm.
6. Traceability Matrix
FR	User Story	Use Case	MoSCoW
FR1	US1	UC1 – Xem phiếu cần phân công	MUST
FR2	US2	UC2 – Xem kỹ thuật viên khả dụng	MUST
FR3	US3	UC3 – Phân công kỹ thuật viên	MUST
FR4	US4	UC4 – Thay đổi kỹ thuật viên phụ trách	SHOULD
FR5	US5	UC5 – Đặt lịch giao – nhận máy	SHOULD
FR6	US6	UC6 – Xem công việc và lịch hẹn được giao	COULD
FR7	US3	UC7 – Kiểm tra điều kiện phân công	MUST
FR8	US5	UC8 – Kiểm tra trùng lịch	SHOULD


Ghi chú:
- FR7 là yêu cầu kiểm tra bắt buộc trong quá trình thực hiện US3.
- FR8 là yêu cầu kiểm tra bắt buộc trong quá trình thực hiện US5.
- UC7 và UC8 là các chức năng hỗ trợ, cần được thể hiện nhất quán trong đặc tả Use Case và sơ đồ.
- Việc phân loại MUST/SHOULD/COULD thể hiện mức ưu tiên triển khai, không có nghĩa các điều kiện kiểm tra trong một chức năng được phép bỏ qua khi chức năng đó được triển khai.
7. Liên kết tài liệu thiết kế
Các tài liệu liên quan trong repository:
- docs/usecase-spec.md: Đặc tả Use Case.
- docs/usecase.drawio: Sơ đồ Use Case gốc.
- docs/architecture.md: Mô tả kiến trúc hệ thống.
- docs/architecture.drawio: Sơ đồ kiến trúc gốc.
- docs/erd.drawio: Sơ đồ thực thể và quan hệ.
- docs/schema.sql: Định nghĩa cấu trúc cơ sở dữ liệu bằng SQL DDL.
- docs/thay-doi-thiet-ke.md: Nhật ký quyết định điều chỉnh thiết kế theo phản hồi BT1.
Các tài liệu trên cần được đồng bộ theo SRS sau khi hoàn tất chỉnh sửa.
8. Lịch sử điều chỉnh
Phiên bản	Nội dung
1.0	SRS ban đầu cho luồng L4
1.1	Chuẩn hóa User Stories thành 6 mục, bổ sung WON'T, cập nhật Acceptance Criteria, Business Rules và Traceability Matrix theo kế hoạch xử lý phản hồi BT1
1.2	Bổ sung điều kiện kiểm thử và cách đo NFR2; làm rõ giới hạn khóa ngoại center_id theo góp ý BT1


Trạng thái: Đã cập nhật nội dung SRS; chưa xác nhận đồng bộ hoàn tất với tất cả sơ đồ và đặc tả Use Case.