"""Thin client for sending video prompts to Sora."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass

import requests

from .code_generator import GeneratedAutomation

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class SoraVideoResponse:
    """Metadata returned after requesting a video render."""

    prompt_id: str
    status: str
    url: str | None


class SoraVideoClient:
    """Send educational prompts to Sora for video generation."""

    def __init__(self, base_url: str | None = None, api_key_env: str = "SORA_API_KEY") -> None:
        self.base_url = base_url or os.getenv("SORA_API_URL", "https://api.sora2.ai/v1")
        self.api_key_env = api_key_env

    def render_video(self, automation: GeneratedAutomation) -> SoraVideoResponse:
        """Submit the automation video script to Sora for rendering."""

        api_key = os.getenv(self.api_key_env)
        if not api_key:
            logger.warning("%s not configured; returning stubbed Sora response", self.api_key_env)
            return SoraVideoResponse(prompt_id="stub", status="skipped", url=None)

        payload = {
            "title": automation.title,
            "script": automation.video_script,
            "length_seconds": 10,
            "branding": {
                "logo_animation": "pixar-style-drop",
                "brand_colors": ["#0C1E7F", "#6F2CF5", "#1BA1E2"],
                "narrator": "founder",
            },
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            f"{self.base_url}/videos",
            headers=headers,
            data=json.dumps(payload),
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return SoraVideoResponse(
            prompt_id=str(data.get("id", "unknown")),
            status=str(data.get("status", "queued")),
            url=data.get("assets", {}).get("preview_url"),
        )


__all__ = ["SoraVideoClient", "SoraVideoResponse"]
