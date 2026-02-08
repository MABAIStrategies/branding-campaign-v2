"""Post the generated campaign assets to marketing channels."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Dict, Optional

import requests

from .video import SoraVideoResponse

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class PublishResult:
    """Return value capturing social publishing outcomes."""

    platform: str
    status: str
    url: str | None = None


class SocialPublisher:
    """Push daily assets to TikTok, Sora 2, and Twitter."""

    def __init__(self) -> None:
        self.tiktok_webhook = os.getenv("TIKTOK_WEBHOOK_URL")
        self.twitter_webhook = os.getenv("TWITTER_WEBHOOK_URL")
        self.sora_share_url = os.getenv("SORA_SHARE_URL")

    def publish_all(self, video: SoraVideoResponse, caption: str) -> list[PublishResult]:
        results: list[PublishResult] = []
        results.append(self._publish_tiktok(video, caption))
        results.append(self._publish_twitter(video, caption))
        results.append(self._publish_sora(video))
        return results

    def _publish_tiktok(self, video: SoraVideoResponse, caption: str) -> PublishResult:
        if not self.tiktok_webhook:
            logger.warning("TIKTOK_WEBHOOK_URL not configured; skipping TikTok post")
            return PublishResult(platform="tiktok", status="skipped")
        payload = {"caption": caption, "video_url": video.url}
        return self._post_json(self.tiktok_webhook, payload, platform="tiktok")

    def _publish_twitter(self, video: SoraVideoResponse, caption: str) -> PublishResult:
        if not self.twitter_webhook:
            logger.warning("TWITTER_WEBHOOK_URL not configured; skipping Twitter post")
            return PublishResult(platform="twitter", status="skipped")
        payload = {"status": caption, "media": video.url}
        return self._post_json(self.twitter_webhook, payload, platform="twitter")

    def _publish_sora(self, video: SoraVideoResponse) -> PublishResult:
        if not self.sora_share_url:
            logger.warning("SORA_SHARE_URL not configured; skipping Sora share")
            return PublishResult(platform="sora", status="skipped")
        payload = {"prompt_id": video.prompt_id, "video_url": video.url}
        return self._post_json(self.sora_share_url, payload, platform="sora")

    def _post_json(self, url: str, payload: Dict[str, Optional[str]], platform: str) -> PublishResult:
        response = requests.post(url, json=payload, timeout=15)
        if response.ok:
            logger.info("Posted %s update", platform)
            return PublishResult(platform=platform, status="posted", url=response.headers.get("Location"))
        logger.error("Failed to post %s update: %s", platform, response.text)
        return PublishResult(platform=platform, status="failed")


__all__ = ["SocialPublisher", "PublishResult"]
