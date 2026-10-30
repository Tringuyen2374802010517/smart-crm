from fastapi import APIRouter
from pydantic import BaseModel

from src.backend.services import technician_service as service


router = APIRouter(prefix="/technicians", tags=["Technicians"])


class TechnicianInput(BaseModel):
    name: str
    center_id: int
    area: str | None = None
    availability_status: str


@router.get("")
def list_technicians():
    return service.list_technicians()


@router.get("/{technician_id}")
def get_technician(technician_id: int):
    return service.get_technician(technician_id)


@router.post("", status_code=201)
def create_technician(data: TechnicianInput):
    return service.create_technician(
        data.name,
        data.center_id,
        data.area,
        data.availability_status
    )


@router.put("/{technician_id}")
def update_technician(technician_id: int, data: TechnicianInput):
    return service.update_technician(
        technician_id,
        data.name,
        data.center_id,
        data.area,
        data.availability_status
    )


@router.delete("/{technician_id}")
def delete_technician(technician_id: int):
    service.delete_technician(technician_id)
    return {"message": "Xoa ky thuat vien thanh cong"}
