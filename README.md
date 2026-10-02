# Smart CRM – Phân công kỹ thuật viên và lịch hẹn

**Sinh viên:** Nguyễn Minh Trị  
**MSSV:** 2374802010517  
**Track:** SE  
**Học phần:** Chuyên đề Tốt nghiệp 1 – Trường Đại học Văn Lang  
**Luồng nghiệp vụ:** L4 – Phân công kỹ thuật viên và lịch hẹn

---

## 1. Mô tả bài toán

Quản lý trung tâm phân công kỹ thuật viên cho phiếu dựa trên tay nghề, địa bàn và khối lượng công việc hiện tại, đồng thời đặt lịch giao – nhận máy và kiểm tra trùng lịch.

---

## 2. Phạm vi

### Trong phạm vi

- Xem các phiếu cần phân công.
- Xem danh sách kỹ thuật viên khả dụng.
- Phân công kỹ thuật viên cho phiếu.
- Kiểm tra điều kiện phân công dựa trên tay nghề, trung tâm và trạng thái khả dụng.
- Thay đổi kỹ thuật viên phụ trách và ghi nhận lý do.
- Đặt lịch giao – nhận máy.
- Kiểm tra xung đột lịch trước khi xác nhận.
- Kỹ thuật viên xem các phiếu và lịch hẹn được giao.

### Ngoài phạm vi

- Tiếp nhận và phân loại yêu cầu bảo hành.
- Quản lý kho linh kiện.
- Xử lý toàn bộ quá trình sửa chữa thiết bị.
- Các chức năng thuộc các luồng nghiệp vụ khác ngoài L4.

---

## 3. Tài liệu BT1

Các tài liệu phân tích và thiết kế được lưu trong thư mục `docs/`:

- `srs.md` – SRS rút gọn.
- `usecase.drawio` – Source Use Case Diagram.
- `usecase.png` – Use Case Diagram.
- `usecase-spec.md` – Đặc tả Use Case.
- `architecture.md` – Mô tả và lập luận kiến trúc.
- `architecture.drawio` – Source Architecture Diagram.
- `architecture.png` – Architecture Diagram.
- `erd.drawio` – Source ERD.
- `erd.png` – Entity Relationship Diagram.
- `schema.sql` – SQL DDL skeleton.
- `wireframe.drawio` – Source Wireframe.
- `wireframe.png` – Wireframe 3 màn hình.
- `api-contract.md` – API Contract dành cho track SE.
- `ai-disclosure.md` – Khai báo sử dụng AI.

---

## 4. Kiến trúc và công nghệ định hướng

| Thành phần | Công nghệ / Công cụ |
|---|---|
| Architecture / Diagram | Draw.io |
| Wireframe | Draw.io |
| Backend | Python 3.12, FastAPI |
| Database | SQLite |
| API | REST API |
| Version Control | Git, GitHub |
| Development Tool | Visual Studio Code |

Kiến trúc được định hướng theo 3 lớp:

`Frontend / Web Interface → Backend API / Business Logic → Database / Smart CRM Data`

---

## 5. Cấu trúc thư mục

```text
smart-crm/
├── docs/
│   ├── srs.md
│   ├── usecase.drawio
│   ├── usecase.png
│   ├── usecase-spec.md
│   ├── architecture.md
│   ├── architecture.drawio
│   ├── architecture.png
│   ├── erd.drawio
│   ├── erd.png
│   ├── schema.sql
│   ├── wireframe.drawio
│   ├── wireframe.png
│   ├── api-contract.md
│   └── ai-disclosure.md
├── src/
│   ├── backend/
│   └── frontend/
├── tests/
├── .env.example
├── .gitignore
└── README.md
```

---

## 6. Khai báo sử dụng công cụ AI

| Công cụ | Mục đích sử dụng | Cách kiểm tra / chỉnh sửa |
|---|---|---|
| ChatGPT | Hỗ trợ phân tích, soạn thảo SRS, User Stories, Acceptance Criteria, Use Case Specification, Architecture, Data Model, SQL DDL, Wireframe và API Contract | Đối chiếu với phạm vi L4, yêu cầu BT1 và case study; kiểm tra và chỉnh sửa nội dung trước khi sử dụng |
| Draw.io AI | Hỗ trợ tạo Architecture Diagram, ERD và Wireframe | Kiểm tra thành phần, quan hệ, PK/FK, trường dữ liệu, bố cục và phạm vi chức năng trước khi lưu |

Chi tiết việc sử dụng AI được trình bày tại `docs/ai-disclosure.md`.

---

## 7. Ghi chú

Repository này tập trung vào các tài liệu phân tích và thiết kế cho BT1 của luồng L4. Phạm vi BT1 không yêu cầu triển khai đầy đủ hệ thống.