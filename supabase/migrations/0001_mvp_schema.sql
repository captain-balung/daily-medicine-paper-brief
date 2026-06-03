create extension if not exists pgcrypto;

create table if not exists public.sources (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  source_type text not null,
  base_url text,
  is_enabled boolean not null default true,
  priority_level text not null default 'normal',
  last_success_at timestamptz,
  last_error_at timestamptz,
  last_error_message text,
  config jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists sources_source_type_idx on public.sources (source_type);
create index if not exists sources_is_enabled_idx on public.sources (is_enabled);

create table if not exists public.articles (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  title_zh text,
  normalized_title text,
  abstract text,
  journal text,
  publisher text,
  publication_date date,
  doi text unique,
  pmid text unique,
  pmcid text,
  url text,
  language text not null default 'en',
  article_type text,
  access_status text not null default 'UNKNOWN',
  is_preprint boolean not null default false,
  is_open_access boolean not null default false,
  full_text_available boolean not null default false,
  full_text_source text,
  raw_metadata jsonb not null default '{}'::jsonb,
  processing_status text not null default 'collected',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists articles_publication_date_idx on public.articles (publication_date);
create index if not exists articles_access_status_idx on public.articles (access_status);
create index if not exists articles_processing_status_idx on public.articles (processing_status);

create table if not exists public.article_sources (
  id uuid primary key default gen_random_uuid(),
  article_id uuid not null references public.articles(id) on delete cascade,
  source_id uuid not null references public.sources(id) on delete cascade,
  source_url text,
  source_identifier text,
  raw_payload jsonb not null default '{}'::jsonb,
  collected_at timestamptz not null default now()
);

create unique index if not exists article_sources_identifier_idx
  on public.article_sources (source_id, source_identifier)
  where source_identifier is not null;

create table if not exists public.topics (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  name_en text not null,
  name_zh text not null,
  description text,
  default_weight integer not null default 3,
  is_active boolean not null default true,
  created_at timestamptz not null default now()
);

create table if not exists public.article_topics (
  id uuid primary key default gen_random_uuid(),
  article_id uuid not null references public.articles(id) on delete cascade,
  topic_id uuid not null references public.topics(id) on delete cascade,
  relevance_score numeric,
  is_primary boolean not null default false,
  assigned_by text not null default 'ai',
  created_at timestamptz not null default now(),
  unique (article_id, topic_id)
);

create table if not exists public.article_scores (
  id uuid primary key default gen_random_uuid(),
  article_id uuid not null references public.articles(id) on delete cascade,
  clinical_impact integer not null,
  evidence_strength integer not null,
  novelty integer not null,
  specialty_relevance integer not null,
  teaching_research_value integer not null,
  total_score integer not null,
  recommendation_level text not null,
  podcast_suitability integer,
  scoring_rationale text,
  created_at timestamptz not null default now()
);

create table if not exists public.article_summaries (
  id uuid primary key default gen_random_uuid(),
  article_id uuid not null references public.articles(id) on delete cascade,
  summary_version integer not null default 1,
  one_sentence_summary text not null,
  background text,
  methods text,
  main_findings text,
  author_conclusion text,
  clinical_implications text,
  basic_mechanism text,
  clinical_basic_translation text,
  limitations text not null,
  taiwan_relevance text,
  teaching_use text,
  research_use text,
  preprint_warning text,
  access_warning text,
  generated_by text not null default 'anthropic',
  created_at timestamptz not null default now()
);

create table if not exists public.daily_briefings (
  id uuid primary key default gen_random_uuid(),
  briefing_date date not null unique,
  title text not null,
  status text not null default 'draft',
  summary text,
  trend_overview text,
  deep_dive_article_id uuid references public.articles(id),
  clinical_basic_section text,
  interesting_medicine_section text,
  tracking_topics jsonb not null default '[]'::jsonb,
  source_window_start timestamptz not null,
  source_window_end timestamptz not null,
  published_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.daily_briefing_items (
  id uuid primary key default gen_random_uuid(),
  daily_briefing_id uuid not null references public.daily_briefings(id) on delete cascade,
  article_id uuid not null references public.articles(id) on delete cascade,
  section text not null,
  rank integer,
  item_summary text,
  created_at timestamptz not null default now()
);

create table if not exists public.weekly_briefings (
  id uuid primary key default gen_random_uuid(),
  week_start_date date not null,
  week_end_date date not null,
  iso_week text not null unique,
  title text not null,
  status text not null default 'draft',
  weekly_summary text,
  top_ten_summary text,
  clinical_basic_themes jsonb not null default '[]'::jsonb,
  research_questions jsonb not null default '[]'::jsonb,
  teaching_materials jsonb not null default '[]'::jsonb,
  interesting_medicine_highlights jsonb not null default '[]'::jsonb,
  conclusion text,
  published_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.weekly_briefing_items (
  id uuid primary key default gen_random_uuid(),
  weekly_briefing_id uuid not null references public.weekly_briefings(id) on delete cascade,
  article_id uuid not null references public.articles(id) on delete cascade,
  section text not null,
  rank integer,
  item_summary text,
  created_at timestamptz not null default now()
);

create table if not exists public.podcasts (
  id uuid primary key default gen_random_uuid(),
  podcast_type text not null,
  daily_briefing_id uuid references public.daily_briefings(id) on delete cascade,
  weekly_briefing_id uuid references public.weekly_briefings(id) on delete cascade,
  title text not null,
  status text not null default 'deferred',
  script text,
  transcript text,
  audio_storage_path text,
  audio_url text,
  duration_seconds integer,
  voice_name text,
  tts_provider text,
  is_ai_generated boolean not null default true,
  generated_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  role text not null default 'viewer',
  institution text,
  department text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.bookmarks (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.profiles(id) on delete cascade,
  article_id uuid not null references public.articles(id) on delete cascade,
  bookmark_type text not null default 'read_later',
  created_at timestamptz not null default now(),
  unique (user_id, article_id, bookmark_type)
);

create table if not exists public.notes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.profiles(id) on delete cascade,
  article_id uuid references public.articles(id) on delete cascade,
  daily_briefing_id uuid references public.daily_briefings(id) on delete cascade,
  weekly_briefing_id uuid references public.weekly_briefings(id) on delete cascade,
  note_text text not null,
  visibility text not null default 'private',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.pipeline_jobs (
  id uuid primary key default gen_random_uuid(),
  job_type text not null,
  status text not null default 'queued',
  target_date date,
  target_week text,
  source_window_start timestamptz,
  source_window_end timestamptz,
  started_at timestamptz,
  finished_at timestamptz,
  total_candidates integer not null default 0,
  total_articles_saved integer not null default 0,
  total_analyzed integer not null default 0,
  total_failed integer not null default 0,
  error_message text,
  metadata jsonb not null default '{}'::jsonb,
  triggered_by text not null default 'system',
  retry_of uuid references public.pipeline_jobs(id),
  created_at timestamptz not null default now()
);

create index if not exists pipeline_jobs_status_idx on public.pipeline_jobs (status);
create index if not exists pipeline_jobs_job_type_idx on public.pipeline_jobs (job_type);

create table if not exists public.pipeline_job_events (
  id uuid primary key default gen_random_uuid(),
  pipeline_job_id uuid not null references public.pipeline_jobs(id) on delete cascade,
  event_type text not null,
  step_name text not null,
  message text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.system_settings (
  id uuid primary key default gen_random_uuid(),
  key text not null unique,
  value jsonb not null,
  description text,
  updated_by uuid references public.profiles(id),
  updated_at timestamptz not null default now()
);

create table if not exists public.audit_logs (
  id uuid primary key default gen_random_uuid(),
  actor_user_id uuid references public.profiles(id),
  action text not null,
  entity_type text not null,
  entity_id uuid,
  before_value jsonb,
  after_value jsonb,
  ip_address text,
  user_agent text,
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;
alter table public.bookmarks enable row level security;
alter table public.notes enable row level security;
alter table public.system_settings enable row level security;
alter table public.audit_logs enable row level security;

create policy "Users can read own profile"
  on public.profiles for select
  using (auth.uid() = id);

create policy "Users can read own bookmarks"
  on public.bookmarks for select
  using (auth.uid() = user_id);

create policy "Users can manage own bookmarks"
  on public.bookmarks for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "Users can read own notes"
  on public.notes for select
  using (auth.uid() = user_id);

create policy "Users can manage own notes"
  on public.notes for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
