"""Backend architecture specialist."""

from textwrap import dedent
from .base import BaseDevAgent


class BackendArchitect(BaseDevAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="Backend Architect",
            goal="Design scalable backend systems and APIs",
            backstory=dedent(
                """
                You are an experienced software architect focusing on backend
                services. You ensure code is maintainable, well-tested and
                follows best practices.
                """
            ),
            tools=self.get_specialized_tools(),
            llm=llm,
        )

    def get_specialized_tools(self):
        return []
