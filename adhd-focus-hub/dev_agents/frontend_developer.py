"""Frontend development agent."""

from textwrap import dedent
from .base import BaseDevAgent


class FrontendDeveloper(BaseDevAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="Frontend Developer",
            goal="Build and maintain the user interface",
            backstory=dedent(
                """
                You develop responsive user interfaces and ensure cross-browser
                compatibility. Accessibility and performance guide your work.
                """
            ),
            tools=self.get_specialized_tools(),
            llm=llm,
        )

    def get_specialized_tools(self):
        return []
