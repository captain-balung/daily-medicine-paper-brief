# 11 Development Tasks

## 1. Purpose

This document breaks the project into Codex-friendly tasks. Each task should be small, testable, reviewable, and mapped to the project roadmap.

## 2. Task Template

Each task should include:
1. Goal.
2. Files likely affected.
3. Acceptance criteria.
4. Tests or verification.
5. Security notes.

---

## Phase 0 — Specification and Repo

### Task 001 — Create repository structure

Goal: Create apps, workers, supabase, docs folders.

Acceptance criteria:
1. Folder structure exists.
2. docs/00–11 exists.
3. No secrets committed.

### Task 002 — Initialize Next.js app

Goal: Create `apps/web` with Next.js + TypeScript + Tailwind.

Acceptance criteria:
1. Local run works.
2. Build succeeds.
3. Basic layout exists.

### Task 003 — Initialize Python worker skeleton

Goal: Create worker folders and health check.

Acceptance criteria:
1. `workers/daily_pipeline/main.py` exists.
2. `workers/weekly_pipeline/main.py` exists.
3. Health check command runs.
4. No secrets printed.

---

## Phase 1 — Supabase Foundation

### Task 004 — Create initial migrations

Goal: Create MVP database tables.

Tables:
1. sources.
2. articles.
3. article_sources.
4. topics.
5. article_topics.
6. article_scores.
7. article_summaries.
8. daily_briefings.
9. daily_briefing_items.
10. weekly_briefings.
11. weekly_briefing_items.
12. podcasts.
13. profiles.
14. bookmarks.
15. notes.
16. pipeline_jobs.
17. pipeline_job_events.
18. system_settings.
19. audit_logs.

Acceptance criteria:
1. Migrations apply.
2. Primary keys and indexes exist.
3. No secrets table exists.

### Task 005 — Seed default topics

Goal: Insert core topics.

Acceptance criteria:
1. All topic slugs inserted.
2. Default weights exist.
3. Active flags set.

### Task 006 — Seed default sources

Goal: Insert initial sources.

Acceptance criteria:
1. PubMed, Crossref, Europe PMC, Unpaywall exist.
2. Key journals exist.
3. Preprint and regulatory sources exist.
4. Priority levels assigned.

---

## Phase 2 — Human-First Setup

### Task 007 — Build Initial Setup Dashboard

Goal: Create `/admin/setup`.

Acceptance criteria:
1. Shows system status.
2. Shows setup checklist.
3. Shows secrets status without values.
4. Shows source status.
5. Shows test pipeline button.

### Task 008 — Implement system status

Goal: Store and read system status.

Acceptance criteria:
1. Status in system_settings.
2. Admin sees status.
3. Incomplete setup redirects to dashboard.

### Task 009 — Implement readiness check

Goal: Check Supabase, Storage, secrets, sources, safety settings.

Acceptance criteria:
1. Pass/fail per check.
2. No secret values returned.
3. READY only if all required checks pass.

---

## Phase 3 — Data Collection

### Task 010 — PubMed collector

Acceptance criteria:
1. Accepts start/end time.
2. Returns normalized candidates.
3. Includes PMID/title/abstract/journal/date.
4. Handles empty response.

### Task 011 — Crossref collector

Acceptance criteria:
1. Enriches by DOI.
2. Handles missing DOI.
3. Captures license metadata when available.

### Task 012 — Europe PMC collector

Acceptance criteria:
1. Enriches PMID/DOI.
2. Detects PMCID.
3. Detects full-text availability.

### Task 013 — Unpaywall checker

Acceptance criteria:
1. DOI input returns OA status.
2. Handles no DOI.
3. Stores best OA location.

### Task 014 — RSS collector

Acceptance criteria:
1. Supports configured feeds.
2. Returns title, URL, date, summary.
3. Handles source failure gracefully.

### Task 015 — Deduplication engine

Acceptance criteria:
1. Duplicate DOI not inserted twice.
2. PMID duplicates merge.
3. RSS/PubMed duplicates merge.
4. Source links preserved.

---

## Phase 4 — AI Analysis

### Task 016 — Topic classification

Acceptance criteria:
1. Primary topic returned.
2. Secondary topics returned.
3. article_topics saved.
4. Low confidence handled.

### Task 017 — Study type and evidence labeling

Acceptance criteria:
1. Study type classified.
2. Evidence level assigned.
3. Preprint not given highest evidence score.

### Task 018 — Importance scoring

Acceptance criteria:
1. Five component scores generated.
2. Total score calculated.
3. Recommendation level assigned.
4. Rationale stored.

### Task 019 — Article summary generator

Acceptance criteria:
1. One-sentence summary exists.
2. Background/methods/findings exist.
3. Clinical implications exist.
4. Basic mechanism exists.
5. Limitations exist.
6. Warnings included when needed.

---

## Phase 5 — Daily Briefing

### Task 020 — Daily briefing generator

Acceptance criteria:
1. Selects top 5 must-read articles.
2. Creates specialty sections.
3. Includes deep dive.
4. Includes interesting medicine.
5. Saves briefing and items.

### Task 021 — Daily briefing page

Acceptance criteria:
1. Displays all sections.
2. Shows article cards.
3. Shows source list.
4. Shows evidence/access badges.
5. Handles missing podcast.

### Task 022 — Home page

Acceptance criteria:
1. Shows latest briefing.
2. Shows podcast player.
3. Shows top 5.
4. Shows interesting medicine item.

---

## Phase 6 — Podcast

### Task 023 — Podcast script generator

Acceptance criteria:
1. Opening.
2. Top 5 studies.
3. Specialty briefs.
4. Clinical-basic translation.
5. Interesting medicine.
6. Closing.
7. Script saved.

### Task 024 — TTS MP3 generation

Acceptance criteria:
1. MP3 generated.
2. Uploaded to Supabase Storage.
3. Podcast record updated.
4. Transcript saved.
5. Failure handled.

### Task 025 — Podcast player

Acceptance criteria:
1. Plays MP3.
2. Shows duration if available.
3. Shows transcript.
4. Shows AI disclosure.

---

## Phase 7 — Weekly Briefing

### Task 026 — Weekly briefing generator

Acceptance criteria:
1. Reads prior 7 days.
2. Selects top 10.
3. Creates topic summaries.
4. Creates research questions.
5. Creates teaching materials.
6. Selects interesting medicine highlights.
7. Saves weekly briefing.

### Task 027 — Weekly briefing page

Acceptance criteria:
1. Displays weekly summary.
2. Displays top 10.
3. Displays topic sections.
4. Displays weekly podcast.
5. Displays source list.

---

## Phase 8 — Knowledge Base

### Task 028 — Authentication

Acceptance criteria:
1. Users can log in.
2. Profiles row created.
3. Roles assigned.
4. Admin pages protected.

### Task 029 — Bookmarks

Acceptance criteria:
1. Add bookmark.
2. Remove bookmark.
3. List bookmarks.
4. RLS protects user bookmarks.

### Task 030 — Notes

Acceptance criteria:
1. Add note.
2. Edit note.
3. Delete note.
4. Notes private by default.

### Task 031 — Basic search

Acceptance criteria:
1. Keyword search.
2. Topic filter.
3. Date filter.
4. Score filter.
5. Access filter.

### Task 032 — Semantic search

Acceptance criteria:
1. Store embeddings.
2. Query related articles.
3. Do not embed unauthorized full text.

---

## Phase 9 — Admin Review

### Task 033 — Admin dashboard

Acceptance criteria:
1. Shows system status.
2. Shows latest jobs.
3. Shows errors.
4. Shows drafts.
5. Has rerun links.

### Task 034 — Daily review page

Acceptance criteria:
1. Preview draft.
2. Edit summary.
3. Approve publish.
4. Reject/rerun.
5. Audit log written.

### Task 035 — Pipeline logs page

Acceptance criteria:
1. List jobs.
2. Show job details.
3. Show step events.
4. Show errors.
5. Admin only.

---

## Phase 10 — Deployment

### Task 036 — Vercel deployment

Acceptance criteria:
1. Build succeeds.
2. Env vars configured.
3. Production URL works.
4. No backend secrets exposed.

### Task 037 — Render daily cron

Acceptance criteria:
1. Schedule `0 22 * * *`.
2. Runs daily worker.
3. Writes pipeline job.
4. Manual trigger works.

### Task 038 — Render weekly cron

Acceptance criteria:
1. Schedule `0 22 * * SAT`.
2. Runs weekly worker.
3. Writes weekly briefing.
4. Manual trigger works.

### Task 039 — Error alerting

Acceptance criteria:
1. Failure creates alert.
2. Alert visible in admin.
3. Optional webhook/email sent.
4. Error includes failed step.

---

## Phase 11 — Institutional Version

### Task 040 — Role-specific views

Acceptance criteria:
1. Physician version.
2. Resident teaching version.
3. Nurse care-point version.
4. Research assistant literature version.

### Task 041 — Journal club module

Acceptance criteria:
1. Tag article as journal_club.
2. Journal club page exists.
3. Export list.

### Task 042 — Library access links

Acceptance criteria:
1. Article page shows institutional access link.
2. No credentials stored.
3. Access status remains visible.

---

## Final MVP Checklist

1. Setup dashboard.
2. Daily pipeline.
3. AI analysis.
4. Daily briefing page.
5. Daily Podcast.
6. Weekly briefing.
7. Supabase database.
8. Supabase Storage.
9. Vercel deployment.
10. Render cron.
11. Basic admin.
12. Security rules.
13. No paid full-text storage.
14. Preprint warnings.
15. Medical disclaimer.
