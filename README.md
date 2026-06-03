# Daily Medicine Paper Brief

Medical research intelligence MVP for daily Chinese briefings.

## MVP scope

- Core sources: PubMed, Crossref, Unpaywall
- AI provider: Anthropic
- Publication mode: auto-publish after setup and safety checks pass
- Audio, podcast, and TTS are intentionally out of scope for the first version
- No manual review flow in the first version

## Project layout

```text
apps/web/       Next.js web app
workers/        Python collection and briefing workers
supabase/       SQL migrations and seed data
01-harness/     Original project specifications
```

## Web deployment

The web app can be deployed to Vercel from this repository. See
`docs/deployment_vercel.md`.

## Worker deployment

The daily cloud pipeline can be deployed as a Render Cron Job from `render.yaml`.
See `docs/render_cron.md`.

## Environment

Copy `.env.example` into local environment files as needed. Do not commit `.env`.

Frontend:

```env
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=
```

Worker:

```env
SUPABASE_URL=
SUPABASE_SECRET_KEY=
ANTHROPIC_API_KEY=
NCBI_API_KEY=
UNPAYWALL_EMAIL=
CROSSREF_MAILTO=
```

## Local worker commands

```bash
python -m workers.health
python -m workers.daily_pipeline.main --dry-run
python -m workers.daily_pipeline.main
python -m workers.ai_analysis.run --limit 10
python -m workers.daily_pipeline.generate_briefing --limit 10
python -m workers.daily_pipeline.full_run --ai-limit 10
```
