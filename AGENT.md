# Development Agents for Codex

This repository uses CrewAI-based development agents located in `adhd-focus-hub/dev_agents/`. They streamline planning, implementation, and testing when working with Codex.

## Agents

| Agent | Role |
|-------|------|
| **LeadPlanner** | Break down features and create a roadmap. |
| **BackendDeveloper** | Work on the FastAPI backend. |
| **FrontendDeveloper** | Implement the React/TypeScript frontend. |
| **QATester** | Execute tests and report results. |
| **DocsWriter** | Update project documentation. |

## Usage

Before running any agents, set your `OPENAI_API_KEY` environment variable:
```bash
export OPENAI_API_KEY=your_openai_api_key
```

Start Codex with any combination of these agents. Example:

```bash
codex agents start LeadPlanner BackendDeveloper FrontendDeveloper QATester DocsWriter
```

The agents are imported from the `adhd_focus_hub.dev_agents` package.

## Testing

After code changes, run:

```bash
python adhd-focus-hub/test_tools.py
```

Include the output of this script in your pull request summary.
