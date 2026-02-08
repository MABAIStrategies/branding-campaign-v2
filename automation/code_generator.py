"""Generate code blueprints and video scripts for automation workflows."""

from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent
from typing import List

from .config import CampaignConfig
from .task_parser import ParsedTask


@dataclass(slots=True)
class GeneratedAutomation:
    """Artifacts produced by the Codex generation agent."""

    title: str
    code: str
    video_script: str


class CodexGenerator:
    """Translate parsed tasks into runnable automation templates."""

    def __init__(self, config: CampaignConfig | None = None) -> None:
        self.config = config or CampaignConfig()

    def generate(self, task: ParsedTask) -> GeneratedAutomation:
        code = self._generate_code(task)
        video_script = self._generate_video_script(task)
        return GeneratedAutomation(title=task.title, code=code, video_script=video_script)

    def _generate_code(self, task: ParsedTask) -> str:
        """Create a Python-style automation skeleton using the parsed steps."""

        steps_literal = "\n".join(f"    '{step}'," for step in task.steps)
        conditions_literal = "\n".join(f"    '{condition}'," for condition in task.conditions)
        template = f'''"""Automation workflow generated for {task.title}."""

from typing import List


WORKFLOW_STEPS: List[str] = [
{steps_literal}
]

CONDITIONAL_RULES: List[str] = [
{conditions_literal}
]


def run_workflow(context: dict) -> None:
    """Execute the automation sequentially, respecting IF/THEN logic."""

    for step in WORKFLOW_STEPS:
        print(f"Executing: {step}")
    for rule in CONDITIONAL_RULES:
        print(f"Evaluating condition: {rule}")
    print("Automation complete. Customize integrations for production use.")


if __name__ == "__main__":
    run_workflow({{}})
'''
        return dedent(template).strip()

    def _generate_video_script(self, task: ParsedTask) -> str:
        """Build a 10-second instructional script referencing company branding."""

        intro = (
            "Open with me on screen: 'Today's automation spotlight is {title}. Here's how to launch it before your first coffee.'"
        ).format(title=task.title)
        walkthrough = " ".join(
            f"Step {index + 1}: {step}."
            for index, step in enumerate(task.steps[:3])
        )
        use_case = (
            "Common use case: deploy this inside a workflow platform like n8n or Zapier to {goal}."
        ).format(goal=task.steps[0].lower() if task.steps else "streamline your routine")
        deployment = "Deploy it where your team collaborates—Slack, Teams, or customer CRMs."
        outro = (
            "End with the company logo drop-in animation that mirrors the Pixar lamp bounce before fade out."
        )

        return " ".join([intro, walkthrough, use_case, deployment, outro])


__all__ = ["CodexGenerator", "GeneratedAutomation"]
