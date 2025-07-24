"""Project management agent."""

from textwrap import dedent
from .base import BaseDevAgent


class ProjectManager(BaseDevAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="Project Manager",
            goal="Coordinate tasks and timelines for the dev team",
            backstory=dedent(
                """
                You keep the project on track by prioritizing work and
                communicating status. You help remove blockers for the
                developers and keep stakeholders informed.
                """
            ),
            tools=self.get_specialized_tools(),
            llm=llm,
        )

    def get_specialized_tools(self):
        return []
