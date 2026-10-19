from fastapi import APIRouter
from pydantic import BaseModel

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