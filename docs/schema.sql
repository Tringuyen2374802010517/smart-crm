-- Smart CRM – Mekong Mobile
-- Business Flow: L4 – Phân công kỹ thuật viên và lịch hẹn
-- Track: SE

-- =====================================================
-- 1. TICKET
-- =====================================================

CREATE TABLE ticket (
    ticket_id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    incident_group VARCHAR(255) NOT NULL,
    priority VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    center_id INTEGER NOT NULL
);

-- =====================================================
-- 2. TECHNICIAN
-- =====================================================

CREATE TABLE technician (
    technician_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    center_id INTEGER NOT NULL,
    area VARCHAR(255),
    availability_status VARCHAR(50) NOT NULL,
    current_workload INTEGER NOT NULL DEFAULT 0
);

-- =====================================================
-- 3. TECHNICIAN_SKILL
-- =====================================================

CREATE TABLE technician_skill (
    technician_skill_id INTEGER PRIMARY KEY,
    technician_id INTEGER NOT NULL,
    incident_group VARCHAR(255) NOT NULL,
    proficiency INTEGER NOT NULL,

    FOREIGN KEY (technician_id)
        REFERENCES technician(technician_id),

    CHECK (proficiency >= 1 AND proficiency <= 5)
);

-- =====================================================
-- 4. ASSIGNMENT
-- =====================================================

CREATE TABLE assignment (
    assignment_id INTEGER PRIMARY KEY,
    ticket_id INTEGER NOT NULL,
    technician_id INTEGER NOT NULL,
    assigned_at DATETIME NOT NULL,
    ended_at DATETIME,
    change_reason VARCHAR(255),

    FOREIGN KEY (ticket_id)
        REFERENCES ticket(ticket_id),

    FOREIGN KEY (technician_id)
        REFERENCES technician(technician_id)
);

-- =====================================================
-- 5. APPOINTMENT
-- =====================================================

CREATE TABLE appointment (
    appointment_id INTEGER PRIMARY KEY,
    ticket_id INTEGER NOT NULL,
    technician_id INTEGER NOT NULL,
    appointment_type VARCHAR(50) NOT NULL,
    scheduled_at DATETIME NOT NULL,
    status VARCHAR(50) NOT NULL,

    FOREIGN KEY (ticket_id)
        REFERENCES ticket(ticket_id),

    FOREIGN KEY (technician_id)
        REFERENCES technician(technician_id)
);