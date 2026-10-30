import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/appointments", tags=["Appointments"])

DB_PATH = Path(__file__).resolve().parents[3] / "smartcrm.db"
VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


class AppointmentInput(BaseModel):
    ticket_id: int
    appointment_type: str
    start_time: datetime


def connection():
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def normalize_time(value):
    if value.tzinfo is None:
        value = value.replace(tzinfo=VN_TZ)
    return value.astimezone(timezone.utc)


def get_assignment(db, ticket_id):
    return db.execute(
        """
        SELECT a.technician_id
        FROM assignment a
        JOIN ticket t ON t.ticket_id = a.ticket_id
        WHERE a.ticket_id = ?
          AND a.ended_at IS NULL
          AND t.status = 'ASSIGNED'
        """,
        (ticket_id,)
    ).fetchone()


def check_conflict(db, technician_id, start, end):
    rows = db.execute(
        """
        SELECT appointment_id, start_time, end_time
        FROM appointment
        WHERE technician_id = ?
          AND status = 'SCHEDULED'
        """,
        (technician_id,)
    ).fetchall()

    for row in rows:
        existing_start = normalize_time(
            datetime.fromisoformat(row["start_time"])
        )
        existing_end = normalize_time(
            datetime.fromisoformat(row["end_time"])
        )

        if start < existing_end and end > existing_start:
            return dict(row)

    return None


def validate_appointment(db, data):
    if data.appointment_type not in ("DELIVERY", "PICKUP"):
        raise HTTPException(
            status_code=400,
            detail="Loại lịch phải là DELIVERY hoặc PICKUP"
        )

    ticket = db.execute(
        "SELECT ticket_id FROM ticket WHERE ticket_id = ?",
        (data.ticket_id,)
    ).fetchone()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu")

    assignment = get_assignment(db, data.ticket_id)

    if assignment is None:
        raise HTTPException(
            status_code=400,
            detail="Phiếu chưa có kỹ thuật viên đang phụ trách"
        )

    start = normalize_time(data.start_time)
    end = start + timedelta(minutes=60)

    if start <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Thời gian hẹn phải ở tương lai"
        )

    conflict = check_conflict(
        db, assignment["technician_id"], start, end
    )

    return assignment["technician_id"], start, end, conflict


@router.get("")
def list_appointments():
    with connection() as db:
        rows = db.execute(
            """
            SELECT a.*, t.title AS ticket_title,
                   tech.name AS technician_name
            FROM appointment a
            JOIN ticket t ON t.ticket_id = a.ticket_id
            JOIN technician tech
              ON tech.technician_id = a.technician_id
            ORDER BY a.start_time DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]


@router.get("/ticket/{ticket_id}")
def ticket_appointments(ticket_id: int):
    with connection() as db:
        rows = db.execute(
            """
            SELECT * FROM appointment
            WHERE ticket_id = ?
            ORDER BY start_time DESC
            """,
            (ticket_id,)
        ).fetchall()

        return [dict(row) for row in rows]


@router.post("/check")
def check_appointment(data: AppointmentInput):
    with connection() as db:
        technician_id, start, end, conflict = validate_appointment(
            db, data
        )

        return {
            "available": conflict is None,
            "technician_id": technician_id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "duration_minutes": 60,
            "conflict": conflict,
        }


@router.post("", status_code=201)
def create_appointment(data: AppointmentInput):
    db = connection()

    try:
        db.execute("BEGIN IMMEDIATE")

        technician_id, start, end, conflict = validate_appointment(
            db, data
        )

        if conflict:
            raise HTTPException(
                status_code=409,
                detail="Kỹ thuật viên đã có lịch hẹn trùng thời gian"
            )

        cursor = db.execute(
            """
            INSERT INTO appointment
                (ticket_id, technician_id, appointment_type,
                 start_time, end_time, status)
            VALUES (?, ?, ?, ?, ?, 'SCHEDULED')
            """,
            (
                data.ticket_id,
                technician_id,
                data.appointment_type,
                start.isoformat(),
                end.isoformat(),
            )
        )

        appointment_id = cursor.lastrowid
        db.commit()

        return {
            "appointment_id": appointment_id,
            "ticket_id": data.ticket_id,
            "technician_id": technician_id,
            "appointment_type": data.appointment_type,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "status": "SCHEDULED",
        }

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@router.get("/context/{ticket_id}")
def appointment_context(ticket_id: int):
    with connection() as db:
        row = db.execute(
            """
            SELECT
                t.ticket_id,
                t.title,
                t.status AS ticket_status,
                a.technician_id,
                tech.name AS technician_name
            FROM ticket t
            LEFT JOIN assignment a
              ON a.ticket_id = t.ticket_id
             AND a.ended_at IS NULL
            LEFT JOIN technician tech
              ON tech.technician_id = a.technician_id
            WHERE t.ticket_id = ?
            """,
            (ticket_id,)
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Không tìm thấy phiếu sửa chữa"
            )

        return dict(row)
