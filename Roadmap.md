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
- Public RLS policies configured for published briefings, articles, summaries, scores, topics, podcast scripts, podcast audio, and read-only pipeline status.
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
- `UNKNOWN` access status is displayed as `Full text unknown` with explanatory help text.
- Top Ranking includes topic weighting for nephrology, CKD, dialysis, cardiovascular, metabolism, AI medicine, internal medicine, and basic-translational topics.
- Article cards show ranking rationale, score signals, recommendation level, and access-status explanation.
- `/admin/status` shows recent pipeline jobs, pipeline events, latest briefing status, podcast script status, and podcast audio status.
- Homepage and daily briefing pages show a `Today's Top Ranking` summary table.
- `/articles` supports filtering by access status, article type, minimum score, and sorting by score, clinical impact, or publication date.
- `/articles/[id]` uses a journal-club layout with bottom line, why it matters, study design, key findings, limitations, ranking rationale, source/access, and relevance sections.

### Podcast

- Daily podcast script generation is implemented.
- Podcast scripts are stored in Supabase `podcasts`.
- Manual OpenAI TTS audio generation is implemented.
- MP3 files are uploaded to Supabase Storage.
- Homepage and daily pages display the podcast script and audio player when audio is available.
- Render daily pipeline generates podcast audio after the script when `OPENAI_API_KEY` is configured.

## Deferred

- TTS provider comparison and voice tuning.
- Weekly briefing.
- Search, filters, bookmarks, notes, and personalization.
- Full admin dashboard.
- Human review workflow.

## Next Recommended Work

1. Review the first automated podcast audio run from Render Cron.
2. Tune OpenAI TTS voice, speed, and pronunciation for medical terms if needed.
3. Adjust podcast prompt style if physician feedback asks for a different tone or depth.
4. Review ranking rationale wording with physician feedback.
5. Add discussion prompts or take-home questions if physician readers want more journal-club support.

## Operating Notes

- The first version now includes daily briefing, podcast script, and optional OpenAI TTS audio.
- Audio generation is optional in the pipeline and is skipped if `OPENAI_API_KEY` is not configured.
- Physician feedback can be collected conversationally; no feedback UI is planned for now.
- Pipeline status is public read-only and does not expose backend secrets.
- Do not expose backend secrets in Vercel or the browser.
