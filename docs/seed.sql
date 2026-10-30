-- Smart CRM - Sample data for L4
-- Safe to run repeatedly; existing seed IDs are preserved.

PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

INSERT OR IGNORE INTO ticket
(ticket_id, title, incident_group, priority, status, center_id)
VALUES
(1, 'Sua man hinh dien thoai', 'MAN_HINH', 'CAO', 'PENDING', 1),
(2, 'Kiem tra loi man hinh', 'MAN_HINH', 'TRUNG_BINH', 'PENDING', 1),
(3, 'Sua thiet bi tai trung tam 2', 'MAN_HINH', 'THAP', 'PENDING', 2);

INSERT OR IGNORE INTO technician
(technician_id, name, center_id, area, availability_status)
VALUES
(1, 'Nguyen Van An', 1, 'TP HCM', 'AVAILABLE'),
(2, 'Tran Minh Binh', 1, 'TP HCM', 'BUSY'),
(3, 'Le Quoc Cuong', 2, 'Can Tho', 'AVAILABLE');

INSERT OR IGNORE INTO technician_skill
(technician_skill_id, technician_id, incident_group, proficiency)
VALUES
(1, 1, 'MAN_HINH', 4),
(2, 2, 'MAN_HINH', 5),
(3, 3, 'MAN_HINH', 2);

COMMIT;
