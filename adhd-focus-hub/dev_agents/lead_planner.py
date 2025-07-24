"""Lead Planner agent for feature breakdown and roadmapping."""

from textwrap import dedent
from .base import BaseDevAgent


class LeadPlanner(BaseDevAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="Lead Planner",
            goal="Break down features and create implementation roadmaps",
            backstory=dedent(
                """
                You collaborate with the team to plan new features.
                Your strength is decomposing big ideas into actionable tasks
                with realistic timelines and clear priorities.
                """
            ),
            tools=self.get_specialized_tools(),
            llm=llm,
        )

    def get_specialized_tools(self):
        return []
