# 02 System Architecture

## 1. Summary

The architecture uses:

1. GitHub for source control.
2. Vercel for Next.js web frontend.
3. Supabase for PostgreSQL, Auth, RLS, Storage, and pgvector.
4. Render for Python workers, daily cron, weekly cron, AI pipeline, and Podcast generation.

## 2. High-Level Architecture

```text
GitHub
  ├── apps/web         → Vercel deploys Next.js
  ├── workers         → Render runs Python pipelines
  ├── supabase        → migrations and policies
  └── docs            → specifications

Vercel
  ├── Daily briefing pages
  ├── Weekly briefing pages
  ├── Article pages
  ├── Podcast player
  ├── Initial Setup Dashboard
  └── Admin review UI

Supabase
  ├── PostgreSQL
  ├── Auth
  ├── RLS
  ├── Storage
  └── pgvector

Render
  ├── Daily cron
  ├── Weekly cron
  ├── Data collectors
  ├── AI summarization
  ├── Podcast generation
  └── Supabase writes
```

## 3. Component Responsibilities

### GitHub

Stores:
1. Web code.
2. Worker code.
3. Database migrations.
4. Prompt templates.
5. Documentation.
6. Tests.

### Vercel

Responsible for:
1. Website rendering.
2. Lightweight APIs.
3. Authenticated pages.
4. Admin UI.
5. Podcast player.

Not responsible for:
1. Full daily pipeline.
2. Large AI jobs.
3. Full Podcast generation.
4. Background queue processing.
5. Secret-heavy processing.

### Supabase

Responsible for:
1. Article metadata.
2. Summaries.
3. Scores.
4. Daily and weekly briefings.
5. Podcasts.
6. User profiles.
7. Bookmarks and notes.
8. Storage for audio, transcripts, PDFs, exports.
9. pgvector embeddings.
10. RLS and Auth.

### Render

Responsible for:
1. Daily 06:00 Taiwan pipeline.
2. Weekly Sunday pipeline.
3. Data collection.
4. Deduplication.
5. OA checking.
6. AI analysis.
7. Briefing generation.
8. TTS and MP3 generation.
9. File upload to Supabase.
10. Pipeline logs.

## 4. Runtime Flows

### Initial Setup Flow

```text
Admin opens app
  ↓
Check system status
  ↓
If incomplete → Initial Setup Dashboard
  ↓
Admin verifies secrets, sources, topic weights, rules
  ↓
Run test pipeline
  ↓
Status becomes READY
  ↓
Scheduled automation enabled
```

### Daily Pipeline Flow

```text
Render cron at UTC 22:00
  ↓
Create pipeline_job
  ↓
Collect previous 24h data
  ↓
Normalize DOI / PMID
  ↓
Deduplicate
  ↓
Check access status
  ↓
AI classify and score
  ↓
AI summarize
  ↓
Generate daily briefing
  ↓
Generate Podcast script
  ↓
Generate MP3
  ↓
Upload to Supabase Storage
  ↓
Write records to Supabase
  ↓
Vercel displays page
```

### Weekly Pipeline Flow

```text
Render cron Saturday UTC 22:00
  ↓
Read prior 7 days
  ↓
Rerank and synthesize
  ↓
Generate weekly top 10
  ↓
Generate topic sections
  ↓
Generate teaching/research materials
  ↓
Generate weekly Podcast
  ↓
Publish or draft
```

## 5. Environment Variables

### Render backend-only

1. SUPABASE_URL
2. SUPABASE_SERVICE_ROLE_KEY
3. DATABASE_URL
4. OPENAI_API_KEY
5. TTS_API_KEY
6. NCBI_API_KEY
7. UNPAYWALL_EMAIL
8. CROSSREF_MAILTO
9. WORKER_INTERNAL_SECRET
10. TZ=Asia/Taipei

### Vercel public-safe

1. NEXT_PUBLIC_SUPABASE_URL
2. NEXT_PUBLIC_SUPABASE_ANON_KEY
3. NEXT_PUBLIC_SITE_URL

Never expose:
1. SUPABASE_SERVICE_ROLE_KEY
2. OPENAI_API_KEY
3. TTS_API_KEY
4. DATABASE_URL
5. WORKER_INTERNAL_SECRET

## 6. Suggested Repository Structure

```text
apps/
  web/
    app/
    components/
    lib/
    types/

workers/
  collectors/
  daily_pipeline/
  weekly_pipeline/
  ai_analysis/
  podcast/
  shared/

supabase/
  migrations/
  policies/
  seed.sql

docs/
  00_project_roadmap.md
  ...
```

## 7. Future Queue Architecture

MVP can run a full script in Render Cron. Future production can use:
1. Render Cron as trigger.
2. Redis / Render Key Value queue.
3. Celery worker.
4. Step-level retry.
5. Parallel article analysis.
6. Dead-letter queue.

## 8. Architecture Constraints

1. Do not run long jobs in Vercel routes.
2. Do not store secrets in browser.
3. Do not store paid full text without authorization.
4. Do not publish if setup status is not READY.
5. Do not use AI output without source and evidence labels.
