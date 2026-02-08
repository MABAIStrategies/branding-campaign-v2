"""Command line entry point for the Branding Campaign: 101 Automations pipeline."""

from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime

from automation import CampaignConfig, run_daily_campaign


def configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the 101 Automations daily campaign")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON output summarizing the run",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_logging(args.verbose)
    logging.getLogger(__name__).info("Executing campaign at %s", datetime.utcnow().isoformat())

    results = run_daily_campaign()

    if args.json:
        payload = []
        for item in results:
            automation = item["automation"]
            parsed = item["parsed"]
            generated = item["generated"]
            video = item["video"]
            publish = item["publish"]
            payload.append(
                {
                    "title": automation.title,
                    "source": automation.source,
                    "url": automation.url,
                    "code": generated.code,
                    "video_script": generated.video_script,
                    "video_status": video.status,
                    "publish": [
                        {
                            "platform": result.platform,
                            "status": result.status,
                            "url": result.url,
                        }
                        for result in publish
                    ],
                    "steps": parsed.steps,
                    "conditions": parsed.conditions,
                }
            )
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
