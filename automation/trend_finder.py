"""Agent that collects daily automation trends from Reddit and Twitter."""

from __future__ import annotations

from dataclasses import dataclass
import logging
import os
from typing import List

import requests

from .config import CampaignConfig

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class TrendingAutomation:
    """Small data container describing a trending automation idea."""

    title: str
    summary: str
    url: str
    source: str
    score: int

    def describe(self) -> str:
        return f"[{self.source}] {self.title} ({self.score} pts) -> {self.url}"


class TrendFinder:
    """Gather trending automation posts across social platforms."""

    reddit_search_url = "https://www.reddit.com/search.json"
    reddit_user_agent = "mab-innovation-labs-101-automations/0.1"
    twitter_recent_url = "https://api.twitter.com/2/tweets/search/recent"

    def __init__(self, config: CampaignConfig | None = None) -> None:
        self.config = config or CampaignConfig()

    # --- Public API -----------------------------------------------------
    def fetch_trending(self) -> List[TrendingAutomation]:
        """Return the top automation ideas aggregated across sources."""

        reddit_entries = self._fetch_reddit_trends()
        twitter_entries = self._fetch_twitter_trends()
        combined = reddit_entries + twitter_entries
        combined.sort(key=lambda item: item.score, reverse=True)

        unique: List[TrendingAutomation] = []
        seen_titles: set[str] = set()
        for entry in combined:
            canonical = entry.title.strip().lower()
            if canonical in seen_titles:
                continue
            if self.config.banned(entry.title) or self.config.banned(entry.summary):
                continue
            seen_titles.add(canonical)
            unique.append(entry)
            if len(unique) >= self.config.max_automations:
                break

        logger.info("Selected %s automations:", len(unique))
        for automation in unique:
            logger.info("%s", automation.describe())
        return unique

    # --- Reddit ---------------------------------------------------------
    def _fetch_reddit_trends(self) -> List[TrendingAutomation]:
        params = {
            "q": self.config.keyword_query(),
            "limit": 25,
            "sort": "hot",
            "t": "day",
            "type": "link",
        }
        headers = {"User-Agent": self.reddit_user_agent}
        response = requests.get(self.reddit_search_url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        payload = response.json()

        entries: List[TrendingAutomation] = []
        for item in payload.get("data", {}).get("children", []):
            data = item.get("data", {})
            score = int(data.get("score", 0))
            subreddit = data.get("subreddit_name_prefixed", "reddit")
            title = data.get("title", "Untitled automation idea")
            summary = data.get("selftext", "")
            url = data.get("url", "")
            if score < self.config.minimum_score:
                continue
            if self.config.banned(title + " " + summary):
                continue
            entries.append(
                TrendingAutomation(
                    title=title,
                    summary=summary or data.get("link_flair_text", ""),
                    url=url or f"https://www.reddit.com{data.get('permalink', '')}",
                    source=subreddit,
                    score=score,
                )
            )
        return entries

    # --- Twitter --------------------------------------------------------
    def _fetch_twitter_trends(self) -> List[TrendingAutomation]:
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        if not bearer_token:
            logger.warning("TWITTER_BEARER_TOKEN not configured; skipping Twitter ingestion")
            return []

        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "mab-innovation-labs-101-automations/0.1",
        }
        params = {
            "query": self._twitter_query(),
            "expansions": "author_id",
            "tweet.fields": "created_at,public_metrics,text",
            "max_results": 50,
        }
        response = requests.get(self.twitter_recent_url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()
        tweets = payload.get("data", [])
        metrics_by_id = {
            tweet["id"]: tweet.get("public_metrics", {}) for tweet in tweets
        }

        entries: List[TrendingAutomation] = []
        for tweet in tweets:
            metrics = metrics_by_id.get(tweet["id"], {})
            score = int(metrics.get("like_count", 0)) + int(metrics.get("retweet_count", 0))
            text = tweet.get("text", "")
            if score < self.config.minimum_score:
                continue
            if self.config.banned(text):
                continue
            entries.append(
                TrendingAutomation(
                    title=text[:80] + ("…" if len(text) > 80 else ""),
                    summary=text,
                    url=f"https://twitter.com/i/web/status/{tweet['id']}",
                    source="twitter",
                    score=score,
                )
            )
        return entries

    def _twitter_query(self) -> str:
        keywords = " OR ".join(self.config.keywords)
        safe_filter = " -crime -illegal -exploit"
        return f"({keywords}) {safe_filter} lang:en"


__all__ = ["TrendFinder", "TrendingAutomation"]
