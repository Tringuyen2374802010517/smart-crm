from src.backend.api.auth_api import require_user
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from src.backend.services import assignment_service as service


router = APIRouter(prefix="/assignments", tags=["Assignments"])


class AssignmentCreate(BaseModel):
    ticket_id: int
    technician_id: int


@router.get("/eligible-technicians/{ticket_id}")
def get_eligible_technicians(ticket_id: int):
    return service.get_eligible_technicians(ticket_id)


@router.post("/", status_code=201)
def create_assignment(data: AssignmentCreate):
    return service.assign_technician(
        data.ticket_id,
        data.technician_id
    )


class ReassignmentInput(BaseModel):
    technician_id: int
    reason: str = Field(min_length=1, max_length=255)


def require_manager(
    authorization: str | None = Header(default=None),
):
    user, _ = require_user(authorization)

    if user["role"] != "MANAGER":
        raise HTTPException(
            status_code=403,
            detail="Chi quan ly trung tam duoc thay doi ky thuat vien",
        )

    return user



@router.get("/ticket/{ticket_id}/reassignment-candidates")
def get_reassignment_candidates(
    ticket_id: int,
    manager=Depends(require_manager),
):
    return service.get_reassignment_candidates(ticket_id)


@router.put("/ticket/{ticket_id}/reassign")
def reassign_assignment(
    ticket_id: int,
    data: ReassignmentInput,
    manager=Depends(require_manager),
):
    return service.reassign_technician(
        ticket_id,
        data.technician_id,
        data.reason,
    )


@router.get("/ticket/{ticket_id}/detail")
def get_ticket_assignment_detail(ticket_id: int):
    from src.backend.repositories.assignment_repository import get_connection

    with get_connection() as db:
        ticket = db.execute(
            "SELECT ticket_id, status FROM ticket WHERE ticket_id = ?",
            (ticket_id,)
        ).fetchone()

        if ticket is None:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Không tìm thấy phiếu")

        row = db.execute(
            """
            SELECT
                a.assignment_id,
                a.ticket_id,
                a.technician_id,
                a.assigned_at,
                a.ended_at,
                a.change_reason,
                tech.name AS technician_name,
                tech.area AS technician_area,
                tech.center_id AS technician_center_id,
                tech.availability_status
            FROM assignment a
            JOIN technician tech
              ON tech.technician_id = a.technician_id
            WHERE a.ticket_id = ?
            ORDER BY
                CASE WHEN a.ended_at IS NULL THEN 0 ELSE 1 END,
                a.assigned_at DESC,
                a.assignment_id DESC
            LIMIT 1
            """,
            (ticket_id,)
        ).fetchone()

        return {
            "ticket_id": ticket_id,
            "ticket_status": ticket["status"],
            "assignment": dict(row) if row else None,
        }


@router.get("/ticket/{ticket_id}/history")
def get_assignment_history(
    ticket_id: int,
    manager=Depends(require_manager),
):
    from src.backend.repositories import assignment_repository as repo

    if repo.get_ticket(ticket_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy phiếu",
        )

    return repo.get_assignment_history(ticket_id)
