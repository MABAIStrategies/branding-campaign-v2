# Branding Campaign: 101 Automations

This repository contains an extendable automation pipeline that powers the daily
"101 Automations" branding campaign for **MAB Innovation Labs LLC**. It encodes
all five stages of the requested workflow:

1. **Daily trigger** – the campaign is intended to run every morning at 7:30 AM.
   Use `cron`, Airflow, or another scheduler to invoke `python main.py` at the
   desired time.
2. **Agent Trend Finder** – collects trending automation-focused workflows from
   Reddit and Twitter, filtered by productivity keywords and safety rules.
3. **Agent 2 (Analyzer)** – parses the selected ideas into step-by-step
   breakdowns with explicit IF/THEN conditions ready for Codex prompts.
4. **Codex generation & Sora integration** – turns each parsed workflow into a
   Python starter template plus an educational 10-second video script that ends
   with the signature logo bounce animation before handing it to Sora 2.
5. **Social publishing** – once the Sora draft is available, the assets are
   pushed to TikTok, Sora, and Twitter through configurable webhooks.

## Project structure

```
automation/
  config.py          # shared configuration, keywords, and safety rules
  trend_finder.py    # Reddit and Twitter aggregation
  task_parser.py     # converts summaries into steps and IF/THEN logic
  code_generator.py  # produces code skeletons and the Sora video script
  video.py           # lightweight Sora client (stub-friendly)
  social_poster.py   # webhook-based publishing to social platforms
  pipeline.py        # orchestrates the end-to-end campaign
main.py               # CLI entry point used by the daily scheduler
```

## Running locally

1. Create and activate a virtual environment, then install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Export credentials for optional integrations (Twitter, Sora, TikTok webhooks):

   ```bash
   export TWITTER_BEARER_TOKEN="..."
   export SORA_API_KEY="..."
   export TIKTOK_WEBHOOK_URL="https://..."
   export TWITTER_WEBHOOK_URL="https://..."
   export SORA_SHARE_URL="https://..."
   ```

3. Run the campaign manually:

   ```bash
   python main.py --json
   ```

   The command prints a structured summary containing the selected automations,
   their generated code scaffolds, Sora submission status, and social publishing
   results.

## Scheduling the daily task

Add the following cron entry to trigger the pipeline every day at 7:30 AM:

```
30 7 * * * /usr/bin/env -S bash -lc 'cd /path/to/branding-campaign-v2 && source .venv/bin/activate && python main.py --json'
```

This ensures the latest campaign assets are produced and distributed across your
marketing channels each morning.
