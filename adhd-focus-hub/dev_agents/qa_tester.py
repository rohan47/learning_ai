"""QA Tester agent responsible for running automated tests."""

from textwrap import dedent
from .base import BaseDevAgent


class QATester(BaseDevAgent):
    def __init__(self, llm=None):
        super().__init__(
            role="QA Tester",
            goal="Execute unit tests and report results",
            backstory=dedent(
                """
                You ensure the codebase remains reliable by writing and running
                automated tests. You communicate failures clearly and help
                maintain overall quality.
                """
            ),
            tools=self.get_specialized_tools(),
            llm=llm,
        )

    def get_specialized_tools(self):
        return []
