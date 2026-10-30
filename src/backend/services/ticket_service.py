from src.backend.services.exceptions import BusinessError, NotFoundError

from src.backend.repositories import ticket_repository as repo


VALID_PRIORITIES = {"CAO", "TRUNG_BINH", "THAP"}


def validate_ticket(title, incident_group, priority, center_id):
    if not isinstance(title, str) or not title.strip():
        raise BusinessError("Tieu de khong duoc de trong")

    if not isinstance(incident_group, str) or not incident_group.strip():
        raise BusinessError("Nhom su co khong duoc de trong")

    if priority not in VALID_PRIORITIES:
        raise BusinessError("Muc uu tien khong hop le")

    if type(center_id) is not int or center_id <= 0:
        raise BusinessError("Ma trung tam phai la so nguyen duong")


def list_tickets():
    return repo.get_all_tickets()


def get_ticket(ticket_id):
    ticket = repo.get_ticket_by_id(ticket_id)
    if ticket is None:
        raise NotFoundError("Khong tim thay phieu")
    return ticket


def create_ticket(title, incident_group, priority, center_id):
    validate_ticket(title, incident_group, priority, center_id)
    return repo.create_ticket(
        title.strip(),
        incident_group.strip(),
        priority,
        center_id
    )


def update_ticket(ticket_id, title, incident_group, priority, center_id):
    validate_ticket(title, incident_group, priority, center_id)
    get_ticket(ticket_id)

    return repo.update_ticket(
        ticket_id,
        title.strip(),
        incident_group.strip(),
        priority,
        center_id
    )


def delete_ticket(ticket_id):
    get_ticket(ticket_id)

    related = repo.has_related_records(ticket_id)

    if related > 0:
        raise BusinessError("Khong the xoa phieu da co phan cong hoac lich hen")

    return repo.delete_ticket(ticket_id)
