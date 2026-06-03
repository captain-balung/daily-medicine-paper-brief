# 08 API Contracts

## 1. Purpose

This document defines API contracts for the Next.js web app, Supabase, and Render worker interactions.

## 2. Principles

1. User-facing APIs enforce auth and role checks.
2. Admin APIs require admin.
3. Internal pipeline APIs require internal secret.
4. No API exposes secrets.
5. Long-running tasks are handled by Render worker, not Vercel route handlers.
6. APIs return JSON.

## 3. Common Response Format

Success:
```json
{
  "ok": true,
  "data": {}
}
```

Error:
```json
{
  "ok": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}
```

## 4. Read APIs

### Get Daily Briefing

```http
GET /api/daily/:date
```

Example:
```http
GET /api/daily/2026-06-03
```

Response includes:
1. briefing_date.
2. title.
3. status.
4. summary.
5. trend_overview.
6. podcast.
7. sections.
8. source list.

Errors:
1. DAILY_BRIEFING_NOT_FOUND.
2. BRIEFING_NOT_PUBLISHED.
3. UNAUTHORIZED.

### Get Weekly Briefing

```http
GET /api/weekly/:iso_week
```

Response includes:
1. weekly_summary.
2. top_ten.
3. topic_sections.
4. clinical_basic_themes.
5. research_questions.
6. teaching_materials.
7. podcast.

### Get Article

```http
GET /api/articles/:id
```

Response includes:
1. article metadata.
2. topics.
3. scores.
4. summary.
5. access status.
6. source URLs.

### List Articles

```http
GET /api/articles
```

Query parameters:
1. topic.
2. date_from.
3. date_to.
4. study_type.
5. access_status.
6. min_score.
7. q.
8. page.
9. page_size.

### Search

```http
GET /api/search?q=...
```

MVP: keyword search.  
Future: semantic search.

## 5. User APIs

### Create Bookmark

```http
POST /api/bookmarks
```

Request:
```json
{
  "article_id": "...",
  "bookmark_type": "read_later"
}
```

### Delete Bookmark

```http
DELETE /api/bookmarks/:id
```

### List My Bookmarks

```http
GET /api/me/bookmarks
```

### Create Note

```http
POST /api/notes
```

Request:
```json
{
  "article_id": "...",
  "note_text": "...",
  "visibility": "private"
}
```

### Update Note

```http
PATCH /api/notes/:id
```

### Delete Note

```http
DELETE /api/notes/:id
```

## 6. Admin APIs

All require admin role.

### Get System Status

```http
GET /api/admin/system-status
```

Response includes:
1. status.
2. checks.
3. failed checks.
4. next action.

### Update Publication Rules

```http
PATCH /api/admin/publication-rules
```

Request:
```json
{
  "daily_publication_mode": "draft_first",
  "weekly_publication_mode": "review_required",
  "require_podcast_before_publish": true
}
```

### Update Topic Weights

```http
PATCH /api/admin/topic-weights
```

### Update Source Activation

```http
PATCH /api/admin/sources/:id
```

### Preview Daily Draft

```http
GET /api/admin/daily/:date/preview
```

### Publish Daily Briefing

```http
POST /api/admin/daily/:date/publish
```

Rules:
1. Must pass safety check.
2. Must have sources.
3. Must have access labels.
4. Must include disclaimer.
5. Podcast required if publication rule requires it.

### Publish Weekly Briefing

```http
POST /api/admin/weekly/:iso_week/publish
```

## 7. Pipeline Job APIs

### Create Daily Pipeline Job

```http
POST /api/admin/pipelines/daily
```

Request:
```json
{
  "target_date": "2026-06-03",
  "mode": "manual_rerun"
}
```

This creates a job record. The full job is executed by Render worker.

### Create Weekly Pipeline Job

```http
POST /api/admin/pipelines/weekly
```

Request:
```json
{
  "iso_week": "2026-W23",
  "mode": "manual_rerun"
}
```

### Internal Worker Status Update

```http
POST /api/internal/pipeline-status
```

Headers:
```text
Authorization: Bearer <WORKER_INTERNAL_SECRET>
```

Request:
```json
{
  "pipeline_job_id": "...",
  "status": "running",
  "step_name": "ai_summary",
  "message": "Processed 10 articles"
}
```

## 8. Authorization Matrix

| Endpoint | Public | Authenticated | Admin | Internal |
|---|---:|---:|---:|---:|
| GET published daily | optional | yes | yes | yes |
| GET draft daily | no | no | yes | no |
| Publish daily | no | no | yes | no |
| Bookmark | no | yes | yes | no |
| Notes | no | yes | yes | no |
| Pipeline logs | no | no | yes | no |
| Internal status update | no | no | no | yes |

## 9. Error Codes

1. UNAUTHORIZED.
2. FORBIDDEN.
3. NOT_FOUND.
4. VALIDATION_ERROR.
5. SETUP_REQUIRED.
6. PIPELINE_NOT_READY.
7. DAILY_BRIEFING_NOT_FOUND.
8. WEEKLY_BRIEFING_NOT_FOUND.
9. ARTICLE_NOT_FOUND.
10. PODCAST_NOT_FOUND.
11. SAFETY_CHECK_FAILED.
12. SOURCE_UNAVAILABLE.
13. INTERNAL_ERROR.

## 10. Acceptance Criteria

1. Daily briefing can be fetched.
2. Weekly briefing can be fetched.
3. Article page can be fetched.
4. Bookmarks and notes work.
5. Admin can preview and publish.
6. Pipeline jobs can be created.
7. Worker can update status.
8. Unauthorized users cannot access admin APIs.
9. No API exposes secrets.
10. Long jobs are not executed in Vercel APIs.
