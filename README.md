# Branding Campaign Automation Dashboard

A Next.js dashboard for monitoring and controlling the branding automation pipeline while surfacing
trending ideas from Reddit and Twitter.

## Getting Started

1. Install dependencies:

   ```bash
   npm install
   ```

2. Run the development server:

   ```bash
   npm run dev
   ```

   The dashboard is available at http://localhost:3000.

## Available API Routes

- `POST /api/automation/trigger` – trigger a specific automation pipeline by passing a `pipelineId`.
- `GET /api/automation/status` – fetch the latest automation snapshot.
- `POST /api/automation/status` – refresh and retrieve the snapshot in a single call.

## Deployment

The project includes a `vercel.json` configuration, making it ready to deploy to Vercel.

## Preview

Open `public/preview.html` in a browser to view a static approximation of the dashboard UI without
running the Next.js server.
