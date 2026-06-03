# Render Cron Deployment

This project uses a Render Cron Job for the cloud daily pipeline.

## Schedule

Render cron expressions use UTC. The configured schedule is:

```text
30 22 * * *
```

That is 06:30 Taiwan time every day.

## Service

The Blueprint service is defined in `render.yaml`:

```text
daily-medicine-paper-brief-daily-pipeline
```

The job command is:

```bash
python -m workers.render_daily
```

Render Cron Jobs do not support the free instance type. The Blueprint omits
`plan`, so Render uses its default paid cron instance type for a new service.

`workers.render_daily` validates required environment variables before running:

```bash
python -m workers.daily_pipeline.full_run --ai-limit 10
```

The full run collects/enriches articles, analyzes up to `DAILY_AI_LIMIT` new
articles, generates the daily briefing, generates a daily podcast script, and
generates OpenAI TTS audio for the script.

## Required Render Secrets

Render will prompt for these during initial Blueprint creation:

```env
SUPABASE_SECRET_KEY=
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
```

Optional:

```env
NCBI_API_KEY=
```

`NCBI_API_KEY` improves PubMed API reliability, but the MVP can run without it.
`OPENAI_API_KEY` is required for TTS audio generation.

Do not commit these values.

## Create the Render Cron Job

1. Open Render Dashboard.
2. Choose **Blueprints** or **New +** then **Blueprint**.
3. Connect `captain-balung/daily-medicine-paper-brief`.
4. Select the repository root so Render can read `render.yaml`.
5. Fill the prompted secret values.
6. Create / sync the Blueprint.
7. Open the cron job and use **Trigger Run** once to test it.

## Verify a Run

After a successful run:

1. The Render job log should show `daily_ai=...` and `daily_briefing=...`.
2. Supabase should contain a published daily briefing for the Taiwan date.
3. The Vercel site should show the updated briefing because it reads Supabase live data.
