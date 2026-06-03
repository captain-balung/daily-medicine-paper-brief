# 05 Database Schema

## 1. Purpose

This document defines Supabase PostgreSQL tables, indexes, RLS concepts, Storage buckets, and pgvector use.

## 2. Naming Conventions

1. Tables use plural snake_case.
2. Primary key: `id uuid primary key default gen_random_uuid()`.
3. Timestamps: `created_at`, `updated_at`.
4. Foreign keys: `{entity}_id`.
5. JSON payloads: `jsonb`.
6. Secrets must not be stored in normal tables.

## 3. Core Tables

### 3.1 `sources`

Fields:
1. id uuid primary key.
2. name text.
3. source_type text.
4. base_url text nullable.
5. is_enabled boolean default true.
6. priority_level text.
7. last_success_at timestamptz nullable.
8. last_error_at timestamptz nullable.
9. last_error_message text nullable.
10. config jsonb.
11. created_at timestamptz.
12. updated_at timestamptz.

Indexes:
1. source_type.
2. is_enabled.

### 3.2 `articles`

Fields:
1. id uuid primary key.
2. title text.
3. title_zh text.
4. normalized_title text.
5. abstract text.
6. journal text.
7. publisher text.
8. publication_date date.
9. doi text unique nullable.
10. pmid text unique nullable.
11. pmcid text nullable.
12. url text.
13. language text default 'en'.
14. article_type text.
15. access_status text.
16. is_preprint boolean default false.
17. is_open_access boolean default false.
18. full_text_available boolean default false.
19. full_text_source text nullable.
20. raw_metadata jsonb.
21. processing_status text.
22. created_at timestamptz.
23. updated_at timestamptz.

Indexes:
1. doi.
2. pmid.
3. publication_date.
4. access_status.
5. processing_status.
6. title/abstract full-text index optional.

### 3.3 `article_sources`

Fields:
1. id uuid.
2. article_id uuid FK articles.
3. source_id uuid FK sources.
4. source_url text.
5. source_identifier text.
6. raw_payload jsonb.
7. collected_at timestamptz.

Unique:
1. source_id + source_identifier when not null.

### 3.4 `topics`

Fields:
1. id uuid.
2. slug text unique.
3. name_en text.
4. name_zh text.
5. description text.
6. default_weight integer.
7. is_active boolean.
8. created_at timestamptz.

Default topics:
1. nephrology.
2. dialysis.
3. ckd.
4. cardiovascular.
5. metabolism.
6. geriatrics.
7. internal_medicine.
8. ai_medicine.
9. basic_translational.
10. drug_safety_guidelines.
11. interesting_medicine.

### 3.5 `article_topics`

Fields:
1. id uuid.
2. article_id uuid FK.
3. topic_id uuid FK.
4. relevance_score numeric.
5. is_primary boolean.
6. assigned_by text.
7. created_at timestamptz.

Unique:
1. article_id + topic_id.

### 3.6 `article_scores`

Fields:
1. id uuid.
2. article_id uuid FK.
3. clinical_impact integer.
4. evidence_strength integer.
5. novelty integer.
6. specialty_relevance integer.
7. teaching_research_value integer.
8. total_score integer.
9. recommendation_level text.
10. podcast_suitability integer.
11. scoring_rationale text.
12. created_at timestamptz.

### 3.7 `article_summaries`

Fields:
1. id uuid.
2. article_id uuid FK.
3. summary_version integer.
4. one_sentence_summary text.
5. background text.
6. methods text.
7. main_findings text.
8. author_conclusion text.
9. clinical_implications text.
10. basic_mechanism text.
11. clinical_basic_translation text.
12. limitations text.
13. taiwan_relevance text.
14. teaching_use text.
15. research_use text.
16. preprint_warning text.
17. access_warning text.
18. generated_by text.
19. created_at timestamptz.

### 3.8 `daily_briefings`

Fields:
1. id uuid.
2. briefing_date date unique.
3. title text.
4. status text.
5. summary text.
6. trend_overview text.
7. deep_dive_article_id uuid nullable.
8. clinical_basic_section text.
9. interesting_medicine_section text.
10. tracking_topics jsonb.
11. source_window_start timestamptz.
12. source_window_end timestamptz.
13. published_at timestamptz.
14. created_at timestamptz.
15. updated_at timestamptz.

### 3.9 `daily_briefing_items`

Fields:
1. id uuid.
2. daily_briefing_id uuid FK.
3. article_id uuid FK.
4. section text.
5. rank integer.
6. item_summary text.
7. created_at timestamptz.

### 3.10 `weekly_briefings`

Fields:
1. id uuid.
2. week_start_date date.
3. week_end_date date.
4. iso_week text unique.
5. title text.
6. status text.
7. weekly_summary text.
8. top_ten_summary text.
9. clinical_basic_themes jsonb.
10. research_questions jsonb.
11. teaching_materials jsonb.
12. interesting_medicine_highlights jsonb.
13. conclusion text.
14. published_at timestamptz.
15. created_at timestamptz.
16. updated_at timestamptz.

### 3.11 `weekly_briefing_items`

Fields:
1. id uuid.
2. weekly_briefing_id uuid FK.
3. article_id uuid FK.
4. section text.
5. rank integer.
6. item_summary text.
7. created_at timestamptz.

### 3.12 `podcasts`

Fields:
1. id uuid.
2. podcast_type text: daily or weekly.
3. daily_briefing_id uuid nullable.
4. weekly_briefing_id uuid nullable.
5. title text.
6. status text.
7. script text.
8. transcript text.
9. audio_storage_path text.
10. audio_url text.
11. duration_seconds integer.
12. voice_name text.
13. tts_provider text.
14. is_ai_generated boolean default true.
15. generated_at timestamptz.
16. created_at timestamptz.
17. updated_at timestamptz.

### 3.13 `profiles`

Fields:
1. id uuid FK auth.users.
2. display_name text.
3. role text.
4. institution text.
5. department text.
6. created_at timestamptz.
7. updated_at timestamptz.

Roles:
1. admin.
2. physician.
3. resident.
4. nurse.
5. research_assistant.
6. viewer.

### 3.14 `bookmarks`

Fields:
1. id uuid.
2. user_id uuid FK profiles.
3. article_id uuid FK articles.
4. bookmark_type text.
5. created_at timestamptz.

Unique:
1. user_id + article_id + bookmark_type.

### 3.15 `notes`

Fields:
1. id uuid.
2. user_id uuid FK profiles.
3. article_id uuid nullable.
4. daily_briefing_id uuid nullable.
5. weekly_briefing_id uuid nullable.
6. note_text text.
7. visibility text.
8. created_at timestamptz.
9. updated_at timestamptz.

### 3.16 `topic_watchlists`

Fields:
1. id uuid.
2. user_id uuid FK profiles.
3. topic_id uuid FK topics.
4. custom_query text nullable.
5. is_active boolean.
6. created_at timestamptz.

### 3.17 `article_embeddings`

Requires pgvector.

Fields:
1. id uuid.
2. article_id uuid FK articles.
3. embedding_type text.
4. content text.
5. embedding vector.
6. model_name text.
7. created_at timestamptz.

Do not embed unauthorized paywalled full text.

### 3.18 `pipeline_jobs`

Fields:
1. id uuid.
2. job_type text.
3. status text.
4. target_date date.
5. target_week text.
6. source_window_start timestamptz.
7. source_window_end timestamptz.
8. started_at timestamptz.
9. finished_at timestamptz.
10. total_candidates integer.
11. total_articles_saved integer.
12. total_analyzed integer.
13. total_failed integer.
14. error_message text.
15. metadata jsonb.
16. triggered_by text.
17. retry_of uuid nullable.
18. created_at timestamptz.

### 3.19 `pipeline_job_events`

Fields:
1. id uuid.
2. pipeline_job_id uuid FK.
3. event_type text.
4. step_name text.
5. message text.
6. metadata jsonb.
7. created_at timestamptz.

### 3.20 `system_settings`

Non-secret settings only.

Fields:
1. id uuid.
2. key text unique.
3. value jsonb.
4. description text.
5. updated_by uuid nullable.
6. updated_at timestamptz.

Allowed:
1. system status.
2. topic weights.
3. source enabled flags.
4. publication rules.
5. safety settings.

Not allowed:
1. API keys.
2. passwords.
3. service role keys.

### 3.21 `audit_logs`

Fields:
1. id uuid.
2. actor_user_id uuid nullable.
3. action text.
4. entity_type text.
5. entity_id uuid nullable.
6. before_value jsonb.
7. after_value jsonb.
8. ip_address text.
9. user_agent text.
10. created_at timestamptz.

## 4. Storage Buckets

### `podcast-audio`

Paths:
1. podcasts/daily/YYYY-MM-DD.mp3
2. podcasts/weekly/YYYY-WW.mp3

### `transcripts`

Stores:
1. Podcast scripts.
2. Podcast transcripts.

### `uploaded-pdfs`

Private. User must confirm legal access.

### `exports`

Stores exported PDF, Word, PowerPoint, CSV.

## 5. RLS Concepts

1. Published briefings may be public or authenticated depending on mode.
2. Bookmarks are visible only to owner.
3. Notes are visible only to owner unless shared.
4. Draft briefings are admin-only.
5. Pipeline logs are admin-only.
6. Service role bypasses RLS only in Render worker.
7. Uploaded PDFs are private.

## 6. Acceptance Criteria

1. All MVP tables can be migrated.
2. Articles can be deduplicated.
3. Briefings can link to articles.
4. Podcasts can link to briefings.
5. Users can bookmark and note.
6. Pipeline jobs are tracked.
7. RLS protects user data.
8. pgvector can store embeddings.
9. No secrets are stored in normal tables.
