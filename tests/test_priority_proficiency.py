import pytest

from src.backend.repositories.assignment_repository import required_proficiency


@pytest.mark.parametrize(
    "priority,expected",
    [
        ("THAP", 2),
        ("TRUNG_BINH", 3),
        ("CAO", 4),
    ],
)
def test_priority_threshold(priority, expected):
    assert required_proficiency(priority) == expected


def test_invalid_priority():
    with pytest.raises(ValueError):
        required_proficiency("KHONG_HOP_LE")


@pytest.mark.parametrize(
    "priority,proficiency,expected",
    [
        ("THAP", 1, False),
        ("TRUNG_BINH", 3, True),
        ("CAO", 3, False),
    ],
)
def test_proficiency_boundary(priority, proficiency, expected):
    assert (proficiency >= required_proficiency(priority)) is expected
