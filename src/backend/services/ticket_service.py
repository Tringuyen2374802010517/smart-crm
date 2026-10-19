from fastapi import HTTPException

from src.backend.repositories import ticket_repository as repo


VALID_PRIORITIES = {"CAO", "TRUNG_BINH", "THAP"}


def validate_ticket(title, incident_group, priority, center_id):
    if not isinstance(title, str) or not title.strip():
        raise HTTPException(status_code=400, detail="Tieu de khong duoc de trong")

    if not isinstance(incident_group, str) or not incident_group.strip():
        raise HTTPException(status_code=400, detail="Nhom su co khong duoc de trong")

    if priority not in VALID_PRIORITIES:
        raise HTTPException(status_code=400, detail="Muc uu tien khong hop le")

    if type(center_id) is not int or center_id <= 0:
        raise HTTPException(status_code=400, detail="Ma trung tam phai la so nguyen duong")


def list_tickets():
    return repo.get_all_tickets()


def get_ticket(ticket_id):
    ticket = repo.get_ticket_by_id(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Khong tim thay phieu")
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

    with repo.get_connection() as connection:
        related = connection.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM assignment WHERE ticket_id = ?)
                +
                (SELECT COUNT(*) FROM appointment WHERE ticket_id = ?)
            """,
            (ticket_id, ticket_id)
        ).fetchone()[0]

    if related > 0:
        raise HTTPException(
            status_code=400,
            detail="Khong the xoa phieu da co phan cong hoac lich hen"
        )

    return repo.delete_ticket(ticket_id)
