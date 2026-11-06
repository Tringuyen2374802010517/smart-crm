
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
        ticket["incident_group"],
        ticket["priority"]
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
        ticket["incident_group"],
        ticket["priority"]
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




def get_reassignment_candidates(ticket_id):
    ticket = repo.get_ticket(ticket_id)

    if ticket is None:
        raise NotFoundError("Khong tim thay phieu")

    if ticket["status"] != "ASSIGNED":
        raise BusinessError("Chi duoc doi ky thuat vien cua phieu ASSIGNED")

    active_assignment = repo.get_active_assignment(ticket_id)

    if active_assignment is None:
        raise BusinessError("Phieu chua co phan cong dang hoat dong")

    technicians = repo.get_eligible_technicians(
        ticket["center_id"],
        ticket["incident_group"],
        ticket["priority"],
    )

    return [
        technician
        for technician in technicians
        if technician["technician_id"] != active_assignment["technician_id"]
    ]


def reassign_technician(ticket_id, technician_id, reason):
    if not isinstance(reason, str) or not reason.strip():
        raise BusinessError("Bat buoc nhap ly do thay doi")

    reason = reason.strip()

    if len(reason) > 255:
        raise BusinessError("Ly do thay doi toi da 255 ky tu")

    if repo.get_ticket(ticket_id) is None:
        raise NotFoundError("Khong tim thay phieu")

    if repo.get_technician(technician_id) is None:
        raise NotFoundError("Khong tim thay ky thuat vien")

    try:
        return repo.reassign_technician(
            ticket_id, technician_id, reason
        )
    except ValueError as error:
        raise BusinessError(str(error)) from error


def complete_ticket(ticket_id):
    ticket = repo.get_ticket(ticket_id)

    if ticket is None:
        raise NotFoundError("Khong tim thay phieu")

    if ticket["status"] != "ASSIGNED":
        raise BusinessError("Chi co the hoan thanh phieu ASSIGNED")

    if not repo.get_active_assignment(ticket_id):
        raise BusinessError("Phieu khong co phan cong dang hoat dong")

    try:
        return repo.complete_ticket(ticket_id)
    except ValueError as error:
        raise BusinessError(str(error)) from error
