import json
import pytest
from backend.crew.tools.planning_tools import (
    TimeEstimationTool,
    TaskBreakdownTool,
    PriorityAssessmentTool,
)


def test_time_estimation():
    tool = TimeEstimationTool()
    result = tool._run(
        task_description="Write a research paper on ADHD productivity",
        complexity_level="High",
        user_context="beginner",
    )
    data = json.loads(result)
    assert data["task"] == "Write a research paper on ADHD productivity"
    assert "total_estimated_time" in data


def test_task_breakdown():
    tool = TaskBreakdownTool()
    result = tool._run(
        task_description="Write a comprehensive research paper on ADHD productivity strategies",
        estimated_time=120,
        user_context="",
    )
    data = json.loads(result)
    assert data["total_estimated_time"] == 120
    assert len(data["subtasks"]) >= 1


def test_priority_assessment():
    tool = PriorityAssessmentTool()
    result = tool._run(
        tasks=[
            "Write research paper (urgent deadline)",
            "Clean room (routine)",
            "Call doctor (urgent)",
            "Learn new creative skill (fun)",
        ],
        deadline_info="research paper due tomorrow",
        user_context="",
    )
    data = json.loads(result)
    assert data["total_tasks"] == 4
    assert len(data["prioritized_tasks"]) == 4

