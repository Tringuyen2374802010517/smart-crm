from fastapi import APIRouter
from pydantic import BaseModel

from src.backend.services import ticket_service as service


router = APIRouter(prefix="/tickets", tags=["Tickets"])


class TicketInput(BaseModel):
    title: str
    incident_group: str
    priority: str
    center_id: int


@router.get("")
def list_tickets():
    return service.list_tickets()


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int):
    return service.get_ticket(ticket_id)


@router.post("", status_code=201)
def create_ticket(data: TicketInput):
    return service.create_ticket(
        data.title,
        data.incident_group,
        data.priority,
        data.center_id
    )


@router.put("/{ticket_id}")
def update_ticket(ticket_id: int, data: TicketInput):
    return service.update_ticket(
        ticket_id,
        data.title,
        data.incident_group,
        data.priority,
        data.center_id
    )


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int):
    service.delete_ticket(ticket_id)
    return {"message": "Xoa phieu thanh cong"}
