# Daily Medicine Paper Brief Roadmap

Last updated: 2026-06-05

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
- Homepage and daily briefing pages use a two-level hierarchy: Top Ranking table for overview and `Featured analysis` cards for deeper reading.
- `/articles` supports filtering by access status, article type, minimum score, and sorting by score, clinical impact, or publication date.
- `/articles/[id]` uses a journal-club layout with bottom line, why it matters, study design, key findings, limitations, ranking rationale, source/access, and relevance sections.
- Copyright-safe presentation is in place: pages show source/use notices, article detail pages no longer republish full original abstracts, and source links are emphasized for original abstract/full text/license verification.
- `/daily` shows a recent daily briefing list so new automated runs are easy to find.
- Daily pipeline updates `pipeline_jobs.total_analyzed` after AI analysis.

### Podcast

- Daily podcast script generation is implemented.
- Podcast scripts are stored in Supabase `podcasts`.
- Daily podcast scripts target an approximately 7-minute morning commute format.
- Daily podcast scripts use a fixed humorous host opening, rendered at 1.5x speed before the normal briefing body.
- OpenAI TTS defaults to `marin`, uses segment-specific voice instructions, and reads the main briefing body at 1.05x speed.
- Manual OpenAI TTS audio generation is implemented.
- MP3 files are uploaded to Supabase Storage.
- MP4 podcast videos are generated from daily briefing visual cards and podcast audio.
- MP4 files are uploaded to Supabase Storage bucket `podcast-videos`.
- Homepage and daily pages display the podcast script and audio player when audio is available.
- Homepage and daily pages display a video player when podcast video is available.
- Render daily pipeline generates podcast audio after the script when `OPENAI_API_KEY` is configured.
- Render daily pipeline generates podcast video after podcast audio.
- `/admin/status` shows podcast video readiness.
- Render Cron now installs `workers/requirements.txt`, including `pillow` and `imageio-ffmpeg`.
- Render Cron environment was updated to `TTS_VOICE=marin`, `PYTHONIOENCODING=utf-8`, and `PODCAST_VIDEO_BUCKET=podcast-videos`.
- Render CLI is installed locally at `C:\Users\Cool\.local\bin\render.exe` and authenticated as `captain.balung@gmail.com`.

## Deferred

- TTS provider comparison and voice tuning.
- Weekly briefing.
- Search, filters, bookmarks, notes, and personalization.
- Full admin dashboard.
- Human review workflow.

## Next Recommended Work

1. Verify the next scheduled Render Cron run on 2026-06-06 at 06:30 Taiwan time.
2. Confirm the next automated audio uses `marin` and the current podcast speed settings.
3. Review the next automated MP4 on the Daily page and decide whether the visual-card format is good enough for continued use.
4. Tune OpenAI TTS voice, speed, and pronunciation for medical terms if needed.
5. Review ranking rationale wording with physician feedback.
6. Review copyright-safe wording with legal or publisher-policy feedback if the project becomes public-facing beyond friend review.
7. Explore weekly briefing once daily review stabilizes.

## Operating Notes

- The first version now includes daily briefing, podcast script, and optional OpenAI TTS audio.
- The current version also includes optional Supabase-hosted podcast video.
- Audio generation is optional in the pipeline and is skipped if `OPENAI_API_KEY` is not configured.
- Video generation depends on podcast audio and Python packages from `workers/requirements.txt`.
- Physician feedback can be collected conversationally; no feedback UI is planned for now.
- Pipeline status is public read-only and does not expose backend secrets.
- Do not expose backend secrets in Vercel or the browser.
