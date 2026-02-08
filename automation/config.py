"""Configuration objects for the 101 Automations branding campaign."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time
from typing import Iterable, List, Sequence


DEFAULT_KEYWORDS: Sequence[str] = (
    "lifehack",
    "hack",
    "automation",
    "workflow",
    "n8n",
    "Make.com",
    "zapier.com",
    "agentic",
)


@dataclass(slots=True)
class CampaignConfig:
    """High level configuration for the daily automation campaign."""

    daily_run_time: time = time(hour=7, minute=30)
    keywords: Sequence[str] = DEFAULT_KEYWORDS
    reddit_sources: Sequence[str] = ("/r/automation", "/r/lifehacks", "/r/nocode")
    twitter_accounts: Sequence[str] = ("automationanyw", "n8n_io", "zapier")
    banned_terms: Sequence[str] = ("crime", "illegal", "exploit")
    minimum_score: int = 15
    max_automations: int = 3
    prompt_template: str = (
        "Create a production ready automation named '{title}'. "
        "The workflow should address: {summary}. Provide clear setup steps, "
        "required tools, one real-world deployment suggestion, and optional enhancements."
    )

    def keyword_query(self) -> str:
        """Join keywords into a space separated query."""

        return " ".join(self.keywords)

    def combined_keywords(self) -> str:
        """Return keywords formatted for analytics in logs or prompts."""

        return ", ".join(self.keywords)

    def banned(self, text: str) -> bool:
        """Check whether any banned term is present in ``text``."""

        lowered = text.lower()
        return any(term.lower() in lowered for term in self.banned_terms)

    def as_dict(self) -> dict[str, object]:
        """Return a dictionary representation suitable for debugging."""

        return {
            "daily_run_time": self.daily_run_time.strftime("%H:%M"),
            "keywords": list(self.keywords),
            "reddit_sources": list(self.reddit_sources),
            "twitter_accounts": list(self.twitter_accounts),
            "banned_terms": list(self.banned_terms),
            "minimum_score": self.minimum_score,
            "max_automations": self.max_automations,
        }


def unique_keywords(*blocks: Iterable[str]) -> List[str]:
    """Flatten keyword blocks and remove duplicates while preserving order."""

    seen: set[str] = set()
    result: List[str] = []
    for block in blocks:
        for word in block:
            lowered = word.lower()
            if lowered not in seen:
                seen.add(lowered)
                result.append(word)
    return result


__all__ = ["CampaignConfig", "DEFAULT_KEYWORDS", "unique_keywords"]
