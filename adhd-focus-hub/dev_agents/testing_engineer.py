"""Quality assurance and testing agent."""

from textwrap import dedent
from .base import BaseDevAgent


class TestingEngineer(BaseDevAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="Testing Engineer",
            goal="Ensure the application is well tested and reliable",
            backstory=dedent(
                """
                You focus on automated testing and code quality. You write unit
                and integration tests and report issues clearly to the team.
                """
            ),
            tools=self.get_specialized_tools(),
            llm=llm,
        )

    def get_specialized_tools(self):
        return []
