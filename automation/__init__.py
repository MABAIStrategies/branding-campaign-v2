"""Automation workflow package for Branding Campaign: 101 Automations."""

from .config import CampaignConfig
from .trend_finder import TrendFinder, TrendingAutomation
from .task_parser import AutomationAnalyzer
from .code_generator import CodexGenerator
from .video import SoraVideoClient
from .social_poster import SocialPublisher
from .pipeline import run_daily_campaign

__all__ = [
    "CampaignConfig",
    "TrendFinder",
    "TrendingAutomation",
    "AutomationAnalyzer",
    "CodexGenerator",
    "SoraVideoClient",
    "SocialPublisher",
    "run_daily_campaign",
]
