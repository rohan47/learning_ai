"""Frontend architecture specialist."""

from textwrap import dedent
from .base import BaseDevAgent


class FrontendArchitect(BaseDevAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="Frontend Architect",
            goal="Design efficient frontend applications and component systems",
            backstory=dedent(
                """
                You architect modern web frontends with an eye for usability and
                maintainability. You set guidelines for component reuse and
                performance.
                """
            ),
            tools=self.get_specialized_tools(),
            llm=llm,
        )

    def get_specialized_tools(self):
        return []
