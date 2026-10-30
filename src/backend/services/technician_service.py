from src.backend.repositories import technician_repository as repo
from src.backend.services.exceptions import BusinessError, NotFoundError


VALID_STATUSES = {"AVAILABLE", "BUSY", "UNAVAILABLE"}


def validate_technician(name, center_id, area, availability_status):
    if not isinstance(name, str) or not name.strip():
        raise BusinessError("Ten ky thuat vien khong duoc de trong")

    if type(center_id) is not int or center_id <= 0:
        raise BusinessError("Ma trung tam phai la so nguyen duong")

    if area is not None and not isinstance(area, str):
        raise BusinessError("Khu vuc khong hop le")

    if availability_status not in VALID_STATUSES:
        raise BusinessError("Trang thai kha dung khong hop le")


def list_technicians():
    return repo.list_technicians()


def get_technician(technician_id):
    technician = repo.get_technician(technician_id)
    if technician is None:
        raise NotFoundError("Khong tim thay ky thuat vien")
    return technician


def create_technician(name, center_id, area, availability_status):
    validate_technician(name, center_id, area, availability_status)
    return repo.create_technician(
        name.strip(),
        center_id,
        area.strip() if area is not None else None,
        availability_status
    )


def update_technician(technician_id, name, center_id, area, availability_status):
    validate_technician(name, center_id, area, availability_status)
    current = get_technician(technician_id)

    if repo.has_active_assignments(technician_id):
        if current["center_id"] != center_id:
            raise BusinessError(
                "Khong the doi trung tam khi dang co phan cong"
            )
        if availability_status != "AVAILABLE":
            raise BusinessError(
                "Khong the chuyen sang khong kha dung khi dang co phan cong"
            )

    return repo.update_technician(
        technician_id,
        name.strip(),
        center_id,
        area.strip() if area is not None else None,
        availability_status
    )


def delete_technician(technician_id):
    get_technician(technician_id)

    if repo.has_assignments_or_appointments(technician_id):
        raise BusinessError(
            "Khong the xoa ky thuat vien da co phan cong hoac lich hen"
        )

    return repo.delete_technician(technician_id)
