"""Agent that translates automation ideas into explicit tasks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .trend_finder import TrendingAutomation


@dataclass(slots=True)
class ParsedTask:
    """Structured task representation for Codex prompt engineering."""

    title: str
    steps: List[str]
    conditions: List[str]

    def to_narrative(self) -> str:
        """Render a readable walkthrough used for social scripting."""

        joined_steps = "\n".join(f"- {step}" for step in self.steps)
        joined_conditions = "\n".join(f"* {cond}" for cond in self.conditions)
        return (
            f"Workflow: {self.title}\n\n"
            f"Steps:\n{joined_steps}\n\n"
            f"IF/THEN Rules:\n{joined_conditions}"
        )


class AutomationAnalyzer:
    """Break trending automations into step-by-step instructions."""

    def parse(self, automation: TrendingAutomation) -> ParsedTask:
        summary = automation.summary.strip() or automation.title
        sentences = self._split_sentences(summary)
        steps = self._derive_steps(sentences)
        conditions = self._derive_conditions(sentences)
        return ParsedTask(title=automation.title, steps=steps, conditions=conditions)

    # --- Sentence processing helpers -----------------------------------
    def _split_sentences(self, text: str) -> List[str]:
        parts = [
            segment.strip()
            for segment in text.replace("\n", " ").split(".")
            if segment.strip()
        ]
        if not parts:
            return [text]
        return parts

    def _derive_steps(self, sentences: Iterable[str]) -> List[str]:
        steps: List[str] = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            if sentence.lower().startswith(("if ", "when ", "once ")):
                continue
            steps.append(sentence)
        if not steps:
            steps.append("Investigate the linked resource and document the workflow steps.")
        return steps

    def _derive_conditions(self, sentences: Iterable[str]) -> List[str]:
        conditions: List[str] = []
        for sentence in sentences:
            lowered = sentence.lower()
            if lowered.startswith("if "):
                conditions.append(sentence)
            elif " if " in lowered or " when " in lowered:
                conditions.append(sentence)
        if not conditions:
            conditions.append("If the automation has branching logic, outline each branch clearly.")
        return conditions


__all__ = ["AutomationAnalyzer", "ParsedTask"]
