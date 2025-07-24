"""Documentation writer agent."""

from textwrap import dedent
from .base import BaseDevAgent


class DocsWriter(BaseDevAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="Docs Writer",
            goal="Update project documentation and READMEs",
            backstory=dedent(
                """
                You craft and maintain clear, concise documentation for the
                project. You ensure setup guides, contribution docs, and API
                references are easy to follow.
                """
            ),
            tools=self.get_specialized_tools(),
            llm=llm,
        )

    def get_specialized_tools(self):
        return []
