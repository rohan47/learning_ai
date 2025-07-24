"""Backend development agent."""

from textwrap import dedent
from .base import BaseDevAgent


class BackendDeveloper(BaseDevAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="Backend Developer",
            goal="Implement backend features and fix bugs",
            backstory=dedent(
                """
                You implement API endpoints, database models and business logic.
                You keep the codebase clean and write unit tests where needed.
                """
            ),
            tools=self.get_specialized_tools(),
            llm=llm,
        )

    def get_specialized_tools(self):
        return []
