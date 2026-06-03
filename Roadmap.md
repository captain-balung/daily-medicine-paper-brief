# Daily Medicine Paper Brief Roadmap

Last updated: 2026-06-03

## Current Status

The project is in a working Core MVP state.

Production:
- Web: https://daily-medicine-paper-brief.vercel.app
- GitHub: https://github.com/captain-balung/daily-medicine-paper-brief
- Render Cron: `daily-medicine-paper-brief-daily-pipeline`
- Schedule: daily 06:30 Taiwan time

## Completed

### Foundation

- Next.js web app scaffolded.
- Supabase schema migrations applied.
- Public RLS policies configured for published briefings, articles, summaries, scores, topics, and podcast scripts.
- Vercel production deployment is live.
- Render CLI installed locally and Render workspace configured.

### Daily Pipeline

- PubMed collection works.
- Crossref enrichment works.
- Unpaywall access labeling works.
- Deduplication by PMID/DOI is in place.
- Anthropic AI analysis works.
- Daily briefing generation works.
- Render Cron runs the daily pipeline in the cloud.
- Manual Render job test succeeded on 2026-06-03.

### Web Experience

- Homepage shows latest daily briefing.
- `/daily` and `/daily/YYYY-MM-DD` pages work.
- `/articles` list works.
- `/articles/[id]` detail pages work.
- `UNKNOWN` access status is displayed as `全文狀態待確認`.
- Top Ranking includes topic weighting for nephrology, CKD, dialysis, cardiovascular, metabolism, AI medicine, internal medicine, and basic-translational topics.

### Podcast

- Daily podcast script generation is implemented.
- Podcast scripts are stored in Supabase `podcasts`.
- Manual OpenAI TTS audio generation is implemented.
- MP3 files are uploaded to Supabase Storage.
- Homepage and daily pages display the podcast script and audio player when audio is available.
- Render daily pipeline is being updated to generate audio after the script.

## Deferred

- TTS provider comparison and voice tuning.
- Weekly briefing.
- Search, filters, bookmarks, notes, and personalization.
- Full admin dashboard.
- Human review workflow.

## Next Recommended Work

1. Review the first podcast script for tone, length, and medical depth.
2. Adjust podcast prompt style if needed.
3. Improve article list filtering and sorting for physician review.
4. Add visible ranking rationale to explain why each article is selected.
5. Monitor the first overnight Render Cron run.

## Operating Notes

- The first version remains text-first: daily briefing plus podcast script.
- Audio/TTS should start only after the script style is stable.
- Physician feedback can be collected conversationally; no feedback UI is planned for now.
- Do not expose backend secrets in Vercel or the browser.
