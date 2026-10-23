
import pytest
from fastapi import HTTPException

from src.backend.services import assignment_service as service


@pytest.fixture
def mock_repo(monkeypatch):
    ticket = {
        "ticket_id": 10,
        "status": "PENDING",
        "center_id": 1,
        "incident_group": "MAN_HINH",
    }

    technician = {
        "technician_id": 1,
        "center_id": 1,
        "availability_status": "AVAILABLE",
    }

    eligible = [
        {
            "technician_id": 1,
            "name": "Nguyen Van An",
            "proficiency": 4,
        }
    ]

    monkeypatch.setattr(
        service.repo, "get_ticket", lambda ticket_id: ticket
    )
    monkeypatch.setattr(
        service.repo, "get_active_assignment", lambda ticket_id: None
    )
    monkeypatch.setattr(
        service.repo, "get_technician", lambda technician_id: technician
    )
    monkeypatch.setattr(
        service.repo,
        "get_eligible_technicians",
        lambda center_id, incident_group: eligible,
    )
    monkeypatch.setattr(
        service.repo,
        "create_assignment",
        lambda ticket_id, technician_id: {
            "assignment_id": 1,
            "ticket_id": ticket_id,
            "technician_id": technician_id,
        },
    )

    return ticket, technician, eligible


def test_assign_success(mock_repo):
    result = service.assign_technician(10, 1)

    assert result["ticket_id"] == 10
    assert result["technician_id"] == 1


def test_ticket_not_found(mock_repo, monkeypatch):
    monkeypatch.setattr(
        service.repo, "get_ticket", lambda ticket_id: None
    )

    with pytest.raises(HTTPException) as error:
        service.assign_technician(999, 1)

    assert error.value.status_code == 404


def test_ticket_not_pending(mock_repo):
    ticket, _, _ = mock_repo
    ticket["status"] = "COMPLETED"

    with pytest.raises(HTTPException) as error:
        service.assign_technician(10, 1)

    assert error.value.status_code == 400


def test_duplicate_assignment(mock_repo, monkeypatch):
    monkeypatch.setattr(
        service.repo,
        "get_active_assignment",
        lambda ticket_id: {"assignment_id": 99},
    )

    with pytest.raises(HTTPException) as error:
        service.assign_technician(10, 1)

    assert error.value.status_code == 400


def test_technician_different_center(mock_repo):
    _, technician, _ = mock_repo
    technician["center_id"] = 2

    with pytest.raises(HTTPException) as error:
        service.assign_technician(10, 1)

    assert error.value.status_code == 400


def test_technician_unavailable(mock_repo):
    _, technician, _ = mock_repo
    technician["availability_status"] = "BUSY"

    with pytest.raises(HTTPException) as error:
        service.assign_technician(10, 1)

    assert error.value.status_code == 400


def test_technician_insufficient_skill(mock_repo):
    _, _, eligible = mock_repo
    eligible.clear()

    with pytest.raises(HTTPException) as error:
        service.assign_technician(10, 1)

    assert error.value.status_code == 400


def test_empty_eligible_technicians(mock_repo):
    _, _, eligible = mock_repo
    eligible.clear()

    result = service.get_eligible_technicians(10)

    assert result == []


def test_technician_not_found(mock_repo, monkeypatch):
    monkeypatch.setattr(
        service.repo, "get_technician", lambda technician_id: None
    )

    with pytest.raises(HTTPException) as error:
        service.assign_technician(10, 999)

    assert error.value.status_code == 404
