import pytest
from rbac import ROLE_ACCESS, allowed_departments
from rag import retrieve

QUERIES = [
    "What was the marketing report about for Q3 2024?",
    "What is the leave policy?",
    "What are the financial highlights?",
    "What is the salary of an employee?",
]


def test_unknown_role_has_no_access():
    assert allowed_departments("hacker") == []


def test_employee_only_general():
    assert allowed_departments("employee") == ["general"]


def test_c_level_sees_all():
    assert set(allowed_departments("c_level")) == {
        "finance", "hr", "marketing", "engineering", "general"
    }


@pytest.mark.parametrize("role", list(ROLE_ACCESS))
@pytest.mark.parametrize("q", QUERIES)
def test_retrieval_never_leaks(role, q):
    allowed = set(allowed_departments(role))
    for d in retrieve(q, role):
        assert d.metadata["department"] in allowed


def test_unknown_role_retrieves_nothing():
    assert retrieve("anything", "hacker") == []