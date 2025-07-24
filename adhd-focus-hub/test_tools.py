#!/usr/bin/env python3
"""Test script to verify planning tools work correctly."""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from crew.tools.planning_tools import TimeEstimationTool, TaskBreakdownTool, PriorityAssessmentTool

def test_time_estimation():
    """Test the time estimation tool."""
    print("=== Testing Time Estimation Tool ===")
    tool = TimeEstimationTool()
    result = tool._run(
        task_description="Write a research paper on ADHD productivity",
        complexity_level="high",
        user_experience="beginner"
    )
    print("Result:", result)
    print()

def test_task_breakdown():
    """Test the task breakdown tool."""
    print("=== Testing Task Breakdown Tool ===")
    tool = TaskBreakdownTool()
    result = tool._run(
        task_title="Research Paper",
        task_description="Write a comprehensive research paper on ADHD productivity strategies",
        estimated_duration=120
    )
    print("Result:", result)
    print()

def test_priority_assessment():
    """Test the priority assessment tool."""
    print("=== Testing Priority Assessment Tool ===")
    tool = PriorityAssessmentTool()
    result = tool._run(
        tasks=[
            "Write research paper (urgent deadline)",
            "Clean room (routine)",
            "Call doctor (urgent)",
            "Learn new creative skill (fun)"
        ],
        deadline_info={"research_paper": "tomorrow"},
        energy_level=6
    )
    print("Result:", result)
    print()

if __name__ == "__main__":
    test_time_estimation()
    test_task_breakdown()
    test_priority_assessment()
