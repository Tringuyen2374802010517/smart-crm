
from src.backend.services.exceptions import BusinessError, NotFoundError

from src.backend.repositories import assignment_repository as repo


def get_eligible_technicians(ticket_id):
    ticket = repo.get_ticket(ticket_id)

    if ticket is None:
        raise NotFoundError("Khong tim thay phieu")

    if ticket["status"] != "PENDING":
        raise BusinessError("Phieu khong o trang thai PENDING")

    if repo.get_active_assignment(ticket_id):
        raise BusinessError("Phieu da co ky thuat vien phu trach")

    return repo.get_eligible_technicians(
        ticket["center_id"],
        ticket["incident_group"]
    )


def assign_technician(ticket_id, technician_id):
    ticket = repo.get_ticket(ticket_id)

    if ticket is None:
        raise NotFoundError("Khong tim thay phieu")

    if ticket["status"] != "PENDING":
        raise BusinessError("Chi duoc phan cong phieu PENDING")

    if repo.get_active_assignment(ticket_id):
        raise BusinessError("Phieu da co phan cong dang hoat dong")

    technician = repo.get_technician(technician_id)

    if technician is None:
        raise NotFoundError("Khong tim thay ky thuat vien")

    if technician["center_id"] != ticket["center_id"]:
        raise BusinessError("Ky thuat vien khac trung tam")

    if technician["availability_status"] != "AVAILABLE":
        raise BusinessError("Ky thuat vien khong kha dung")

    eligible = repo.get_eligible_technicians(
        ticket["center_id"],
        ticket["incident_group"]
    )

    eligible_ids = {
        item["technician_id"] for item in eligible
    }

    if technician_id not in eligible_ids:
        raise BusinessError("Ky thuat vien khong du ky nang")

    try:
        return repo.create_assignment(ticket_id, technician_id)
    except Exception as error:
        import sqlite3

        if isinstance(error, sqlite3.IntegrityError):
            raise BusinessError("Khong the tao phan cong trung lap hoac khong hop le") from error
        raise
