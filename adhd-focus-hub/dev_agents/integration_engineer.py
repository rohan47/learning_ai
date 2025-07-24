"""Integration agent handling CI/CD and system cohesion."""

from textwrap import dedent
from .base import BaseDevAgent


class IntegrationEngineer(BaseDevAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="Integration Engineer",
            goal="Manage CI/CD pipelines and integrate services",
            backstory=dedent(
                """
                You coordinate infrastructure, deployment pipelines and
                service integration. You ensure components work together
                smoothly across environments.
                """
            ),
            tools=self.get_specialized_tools(),
            llm=llm,
        )

    def get_specialized_tools(self):
        return []
