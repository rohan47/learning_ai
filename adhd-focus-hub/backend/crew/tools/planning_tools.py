"""Planning tools for the ADHD Focus Hub CrewAI agents."""

import json
from typing import Dict, Any, List, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class TimeEstimationInput(BaseModel):
    """Input schema for time estimation tool."""
    task_description: str = Field(..., description="Description of the task to estimate")
    complexity_level: str = Field(..., description="Low, Medium, or High complexity")
    user_context: str = Field(default="", description="Additional context about the user's ADHD challenges")


class TaskBreakdownInput(BaseModel):
    """Input schema for task breakdown tool."""
    task_description: str = Field(..., description="Description of the task to break down")
    estimated_time: int = Field(..., description="Total estimated time in minutes")
    user_context: str = Field(default="", description="Additional context about the user's ADHD challenges")


class PriorityAssessmentInput(BaseModel):
    """Input schema for priority assessment tool."""
    tasks: List[str] = Field(..., description="List of task descriptions to prioritize")
    deadline_info: str = Field(default="", description="Information about deadlines and urgency")
    user_context: str = Field(default="", description="Additional context about the user's ADHD challenges")


class TimeEstimationTool(BaseTool):
    """Tool for estimating time needed for tasks with ADHD considerations."""
    
    name: str = "time_estimation_tool"
    description: str = "Estimates time needed for tasks considering ADHD challenges like planning fallacy and hyperfocus"
    args_schema: Type[BaseModel] = TimeEstimationInput
    
    def _run(self, task_description: str, complexity_level: str, user_context: str = "") -> str:
        """
        Estimate time for a task with ADHD considerations.
        
        Args:
            task_description: Description of the task
            complexity_level: Low, Medium, or High
            user_context: Additional context about user's ADHD
        
        Returns:
            JSON string with time estimation and ADHD accommodations
        """
        
        # Base time estimates by complexity
        base_times = {
            "Low": 15,      # 15 minutes
            "Medium": 45,   # 45 minutes
            "High": 120     # 2 hours
        }
        
        base_time = base_times.get(complexity_level, 45)
        
        # ADHD tax - additional time for transitions, distractions, etc.
        adhd_multiplier = 1.5
        
        # Calculate total time with ADHD considerations
        estimated_time = int(base_time * adhd_multiplier)
        
        # Add buffer time for unexpected challenges
        buffer_time = int(estimated_time * 0.3)
        total_time = estimated_time + buffer_time
        
        result = {
            "task": task_description,
            "complexity": complexity_level,
            "base_time_minutes": base_time,
            "adhd_adjusted_time": estimated_time,
            "buffer_time": buffer_time,
            "total_estimated_time": total_time,
            "recommendations": [
                "Use a timer to track actual time spent",
                "Build in breaks every 25-30 minutes",
                "Prepare workspace in advance to minimize setup time",
                "Have fidget tools or background music ready if helpful"
            ]
        }
        
        return json.dumps(result, indent=2)


class TaskBreakdownTool(BaseTool):
    """Tool for breaking down tasks into ADHD-friendly subtasks."""
    
    name: str = "task_breakdown_tool"
    description: str = "Breaks down complex tasks into smaller, manageable steps optimized for ADHD brains"
    args_schema: Type[BaseModel] = TaskBreakdownInput
    
    def _run(self, task_description: str, estimated_time: int, user_context: str = "") -> str:
        """
        Break down a task into ADHD-friendly subtasks.
        
        Args:
            task_description: Description of the main task
            estimated_time: Total estimated time in minutes
            user_context: Additional context about user's ADHD
        
        Returns:
            JSON string with task breakdown and timing
        """
        
        # Optimal subtask length for ADHD (15-25 minutes)
        optimal_chunk = 20
        num_chunks = max(1, estimated_time // optimal_chunk)
        
        # Generate generic subtasks (in a real implementation, this would use AI)
        subtasks = []
        chunk_time = estimated_time // num_chunks
        
        for i in range(int(num_chunks)):
            subtasks.append({
                "step": i + 1,
                "description": f"Step {i + 1} of {task_description}",
                "estimated_minutes": chunk_time,
                "energy_level": "Medium" if i < num_chunks // 2 else "Low",
                "tips": [
                    "Set a timer for this step",
                    "Celebrate completion before moving to next step",
                    "Take a 5-minute break if needed"
                ]
            })
        
        result = {
            "original_task": task_description,
            "total_estimated_time": estimated_time,
            "number_of_steps": len(subtasks),
            "subtasks": subtasks,
            "overall_tips": [
                "Do the hardest steps when you have the most energy",
                "It's okay to do steps out of order if that works better",
                "Mark off completed steps for a sense of progress",
                "If you get stuck, move to a different step and come back"
            ]
        }
        
        return json.dumps(result, indent=2)


class PriorityAssessmentTool(BaseTool):
    """Tool for assessing and prioritizing tasks with ADHD considerations."""
    
    name: str = "priority_assessment_tool"
    description: str = "Prioritizes tasks considering ADHD challenges like importance vs urgency and interest-based motivation"
    args_schema: Type[BaseModel] = PriorityAssessmentInput
    
    def _run(self, tasks: List[str], deadline_info: str = "", user_context: str = "") -> str:
        """
        Prioritize tasks with ADHD-friendly criteria.
        
        Args:
            tasks: List of task descriptions
            deadline_info: Information about deadlines
            user_context: Additional context about user's ADHD
        
        Returns:
            JSON string with prioritized tasks and reasoning
        """
        
        prioritized_tasks = []
        
        for i, task in enumerate(tasks):
            # Simple prioritization logic (in real implementation, would be more sophisticated)
            priority_score = len(tasks) - i  # Reverse order for demo
            
            task_info = {
                "task": task,
                "priority_level": "High" if priority_score > len(tasks) * 0.7 else 
                                "Medium" if priority_score > len(tasks) * 0.3 else "Low",
                "priority_score": priority_score,
                "reasoning": [
                    "Consider your energy levels throughout the day",
                    "Match task difficulty to your current focus ability",
                    "Look for quick wins to build momentum"
                ],
                "suggested_timing": "Morning" if priority_score > len(tasks) * 0.5 else "Afternoon"
            }
            
            prioritized_tasks.append(task_info)
        
        # Sort by priority score
        prioritized_tasks.sort(key=lambda x: x["priority_score"], reverse=True)
        
        result = {
            "total_tasks": len(tasks),
            "deadline_context": deadline_info,
            "prioritized_tasks": prioritized_tasks,
            "adhd_priority_tips": [
                "Start with either the easiest task (for momentum) or most interesting (for engagement)",
                "Group similar tasks together to reduce context switching",
                "Schedule high-priority, low-interest tasks during your peak focus times",
                "Don't be afraid to re-prioritize as your energy and interest change"
            ]
        }
        
        return json.dumps(result, indent=2)
