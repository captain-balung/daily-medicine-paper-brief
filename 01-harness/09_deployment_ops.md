# 09 Deployment and Operations

## 1. Purpose

This document defines deployment, environment variables, cron setup, monitoring, backups, manual reruns, and recovery.

## 2. Environments

### Local

1. Local Next.js app.
2. Local Python worker.
3. Supabase local or staging.
4. Mock AI responses.
5. Test fixtures.

### Staging

1. Vercel preview.
2. Supabase staging.
3. Render staging worker.
4. Test secrets.
5. Cron disabled or limited.

### Production

1. Vercel production.
2. Supabase production.
3. Render production worker.
4. Daily cron enabled.
5. Weekly cron enabled.
6. Alerts enabled.

## 3. Vercel Setup

Responsibilities:
1. Host Next.js.
2. Show daily/weekly briefings.
3. Show article pages.
4. Show admin UI.
5. Show podcast player.

Build:
```text
Root: apps/web
Build command: npm run build
```

Vercel env:
1. NEXT_PUBLIC_SUPABASE_URL.
2. NEXT_PUBLIC_SUPABASE_ANON_KEY.
3. NEXT_PUBLIC_SITE_URL.

Never place:
1. SUPABASE_SERVICE_ROLE_KEY.
2. OPENAI_API_KEY.
3. TTS_API_KEY.
4. DATABASE_URL.
5. WORKER_INTERNAL_SECRET in public env.

## 4. Supabase Setup

Required:
1. PostgreSQL.
2. Auth.
3. Storage.
4. RLS.
5. pgvector.

Steps:
1. Create project.
2. Enable pgcrypto and vector.
3. Apply migrations.
4. Apply RLS policies.
5. Insert seed topics.
6. Insert seed sources.
7. Create admin profile.

Buckets:
1. podcast-audio.
2. transcripts.
3. uploaded-pdfs.
4. exports.

Auth:
1. Email login or Google OAuth for MVP.
2. Future SSO.

## 5. Render Setup

### Daily Cron

Schedule:
```text
0 22 * * *
```

Command:
```bash
python -m workers.daily_pipeline.main
```

### Weekly Cron

Schedule:
```text
0 22 * * SAT
```

Command:
```bash
python -m workers.weekly_pipeline.main
```

### Render Env

Required:
1. SUPABASE_URL.
2. SUPABASE_SERVICE_ROLE_KEY.
3. SUPABASE_STORAGE_BUCKET_PODCASTS.
4. SUPABASE_STORAGE_BUCKET_TRANSCRIPTS.
5. DATABASE_URL.
6. OPENAI_API_KEY.
7. TTS_API_KEY.
8. NCBI_API_KEY.
9. UNPAYWALL_EMAIL.
10. CROSSREF_MAILTO.
11. WORKER_INTERNAL_SECRET.
12. TZ=Asia/Taipei.

Optional:
1. SENTRY_DSN.
2. SLACK_WEBHOOK_URL.
3. EMAIL_ALERT_TO.
4. MAX_ARTICLES_PER_DAY.
5. MAX_AI_SUMMARY_PER_RUN.

## 6. Initial Deployment Sequence

1. Create GitHub repo.
2. Create Supabase project.
3. Apply migrations.
4. Create storage buckets.
5. Configure Auth.
6. Deploy Vercel.
7. Deploy Render worker.
8. Set environment variables.
9. Open Initial Setup Dashboard.
10. Confirm sources.
11. Confirm publication mode.
12. Run test pipeline.
13. Review test draft.
14. Publish first test briefing.
15. Enable daily cron.
16. Enable weekly cron.

## 7. Monitoring

Track:
1. Job start/end/duration.
2. Candidate count.
3. Saved article count.
4. AI analyzed count.
5. Failure count.
6. TTS status.
7. Storage upload status.
8. Publication status.
9. Source health.
10. Website errors.

## 8. Alerting

Alert admin when:
1. Daily pipeline fails.
2. Weekly pipeline fails.
3. No articles collected.
4. All AI analysis fails.
5. Podcast generation fails.
6. Storage upload fails.
7. Supabase connection fails.
8. A source fails repeatedly.
9. System status becomes FAILED.

Channels:
1. Admin dashboard.
2. Email.
3. Slack webhook.
4. Future Line or hospital channel.

## 9. Manual Operations

Admin can rerun:
1. Entire daily pipeline.
2. Collection only.
3. AI only.
4. Podcast only.
5. Publish only.
6. Weekly pipeline.

Rerun inputs:
1. Date or ISO week.
2. Mode.
3. Overwrite or version.

## 10. Backup Strategy

Database:
1. Supabase automated backup.
2. Manual backup before major migrations.
3. Export critical tables periodically.

Storage:
1. Podcast audio backup.
2. Transcript backup.
3. Private PDF backup policy.

Configuration:
1. Topic weights.
2. Source activation.
3. Publication rules.
4. Safety settings.

Do not export secrets in plain text.

## 11. Cost Monitoring

Track:
1. Vercel usage.
2. Supabase database size.
3. Supabase storage.
4. Render worker hours.
5. LLM tokens.
6. TTS cost.
7. Embedding cost.

Controls:
1. Limit max analyzed articles.
2. Summarize candidate pool only.
3. Use abstract-only summaries for paywalled articles.
4. Avoid unnecessary podcast regeneration.
5. Cache when allowed.

## 12. Recovery

### Daily failure

1. Check job log.
2. Identify step.
3. Fix source/API/secret.
4. Manual rerun.
5. Publish acceptable draft.

### Website failure

1. Check Vercel logs.
2. Roll back deployment.
3. Check Supabase connection.
4. Verify env vars.

### Migration failure

1. Stop deploy.
2. Restore backup if needed.
3. Fix migration.
4. Test staging.
5. Apply production.

## 13. Production Readiness Checklist

1. Vercel works.
2. Supabase migrations applied.
3. RLS enabled.
4. Storage buckets configured.
5. Render daily cron tested.
6. Render weekly cron tested.
7. Test pipeline passed.
8. Podcast tested.
9. Medical disclaimer visible.
10. Preprint warning visible.
11. Paid full-text policy visible.
12. Admin account created.
13. Alerts configured.
14. Manual rerun tested.
15. Service key not exposed.

## 14. Acceptance Criteria

1. Daily pipeline runs.
2. Weekly pipeline runs.
3. Website displays results.
4. Podcast plays.
5. Failures notify admin.
6. Rerun works.
7. Backup strategy exists.
8. Secrets are protected.
