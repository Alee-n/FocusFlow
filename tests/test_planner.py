from services.planner_service import generate_plan
from services.planner_service import format_duration


def test_generate_plan_study():

    result = generate_plan(
        "study",
        120,
        "medium",
        "ai"
    )

    assert result["task"] == "Study"
    assert len(result["plan"]) > 0


def test_generate_plan_work():

    result = generate_plan(
        "work",
        180,
        "high",
        "smart"
    )

    assert result["task"] == "Work"
    assert len(result["plan"]) > 0


def test_format_duration_minutes():

    assert format_duration(45) == "45 mins"


def test_format_duration_hours():

    assert format_duration(120) == "2 hr"


def test_format_duration_mixed():

    assert format_duration(150) == "2 hr 30 mins"