"""End-to-end orchestration for the 101 Automations campaign."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import List

from .code_generator import CodexGenerator, GeneratedAutomation
from .config import CampaignConfig
from .social_poster import PublishResult, SocialPublisher
from .task_parser import AutomationAnalyzer
from .trend_finder import TrendFinder, TrendingAutomation
from .video import SoraVideoClient, SoraVideoResponse

logger = logging.getLogger(__name__)


class CampaignPipeline:
    """Coordinates all agents to deliver the daily automation drop."""

    def __init__(self, config: CampaignConfig | None = None) -> None:
        self.config = config or CampaignConfig()
        self.trend_finder = TrendFinder(self.config)
        self.analyzer = AutomationAnalyzer()
        self.generator = CodexGenerator(self.config)
        self.video_client = SoraVideoClient()
        self.publisher = SocialPublisher()

    def run(self) -> List[dict[str, object]]:
        logger.info("Starting campaign run for %s", datetime.utcnow().isoformat())
        trending = self.trend_finder.fetch_trending()
        logger.info("Pulled %s candidate automations", len(trending))

        campaign_results: List[dict[str, object]] = []
        for automation in trending:
            parsed = self.analyzer.parse(automation)
            generated = self.generator.generate(parsed)
            video = self.video_client.render_video(generated)
            caption = self._build_caption(automation, generated)
            publish_results = self.publisher.publish_all(video, caption)
            campaign_results.append(
                {
                    "automation": automation,
                    "parsed": parsed,
                    "generated": generated,
                    "video": video,
                    "publish": publish_results,
                }
            )
        logger.info("Campaign run completed with %s automations", len(campaign_results))
        return campaign_results

    def _build_caption(
        self, automation: TrendingAutomation, generated: GeneratedAutomation
    ) -> str:
        return (
            f"Automation Spotlight: {automation.title}\n"
            f"Try it today to {automation.summary[:140]}...\n"
            f"Code & breakdown inside. #automation #workflow #MABInnovationLabs"
        )


def run_daily_campaign() -> List[dict[str, object]]:
    """Convenience function used by schedulers or CLI wrappers."""

    pipeline = CampaignPipeline()
    return pipeline.run()


__all__ = ["CampaignPipeline", "run_daily_campaign"]
