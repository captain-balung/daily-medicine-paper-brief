alter table public.sources enable row level security;
alter table public.topics enable row level security;
alter table public.articles enable row level security;
alter table public.article_sources enable row level security;
alter table public.article_topics enable row level security;
alter table public.article_scores enable row level security;
alter table public.article_summaries enable row level security;
alter table public.daily_briefings enable row level security;
alter table public.daily_briefing_items enable row level security;
alter table public.weekly_briefings enable row level security;
alter table public.weekly_briefing_items enable row level security;
alter table public.podcasts enable row level security;
alter table public.pipeline_jobs enable row level security;
alter table public.pipeline_job_events enable row level security;

create policy "Public can read enabled sources"
  on public.sources for select
  using (is_enabled = true);

create policy "Public can read active topics"
  on public.topics for select
  using (is_active = true);

create policy "Public can read published daily briefings"
  on public.daily_briefings for select
  using (status = 'published');

create policy "Public can read published weekly briefings"
  on public.weekly_briefings for select
  using (status = 'published');

create policy "Public can read published daily briefing items"
  on public.daily_briefing_items for select
  using (
    exists (
      select 1
      from public.daily_briefings b
      where b.id = daily_briefing_id
        and b.status = 'published'
    )
  );

create policy "Public can read published weekly briefing items"
  on public.weekly_briefing_items for select
  using (
    exists (
      select 1
      from public.weekly_briefings b
      where b.id = weekly_briefing_id
        and b.status = 'published'
    )
  );

create policy "Public can read articles used in published briefings"
  on public.articles for select
  using (
    exists (
      select 1
      from public.daily_briefing_items i
      join public.daily_briefings b on b.id = i.daily_briefing_id
      where i.article_id = articles.id
        and b.status = 'published'
    )
    or exists (
      select 1
      from public.weekly_briefing_items i
      join public.weekly_briefings b on b.id = i.weekly_briefing_id
      where i.article_id = articles.id
        and b.status = 'published'
    )
  );

create policy "Public can read sources for published articles"
  on public.article_sources for select
  using (
    exists (
      select 1
      from public.daily_briefing_items i
      join public.daily_briefings b on b.id = i.daily_briefing_id
      where i.article_id = article_sources.article_id
        and b.status = 'published'
    )
    or exists (
      select 1
      from public.weekly_briefing_items i
      join public.weekly_briefings b on b.id = i.weekly_briefing_id
      where i.article_id = article_sources.article_id
        and b.status = 'published'
    )
  );

create policy "Public can read topics for published articles"
  on public.article_topics for select
  using (
    exists (
      select 1
      from public.daily_briefing_items i
      join public.daily_briefings b on b.id = i.daily_briefing_id
      where i.article_id = article_topics.article_id
        and b.status = 'published'
    )
    or exists (
      select 1
      from public.weekly_briefing_items i
      join public.weekly_briefings b on b.id = i.weekly_briefing_id
      where i.article_id = article_topics.article_id
        and b.status = 'published'
    )
  );

create policy "Public can read scores for published articles"
  on public.article_scores for select
  using (
    exists (
      select 1
      from public.daily_briefing_items i
      join public.daily_briefings b on b.id = i.daily_briefing_id
      where i.article_id = article_scores.article_id
        and b.status = 'published'
    )
    or exists (
      select 1
      from public.weekly_briefing_items i
      join public.weekly_briefings b on b.id = i.weekly_briefing_id
      where i.article_id = article_scores.article_id
        and b.status = 'published'
    )
  );

create policy "Public can read summaries for published articles"
  on public.article_summaries for select
  using (
    exists (
      select 1
      from public.daily_briefing_items i
      join public.daily_briefings b on b.id = i.daily_briefing_id
      where i.article_id = article_summaries.article_id
        and b.status = 'published'
    )
    or exists (
      select 1
      from public.weekly_briefing_items i
      join public.weekly_briefings b on b.id = i.weekly_briefing_id
      where i.article_id = article_summaries.article_id
        and b.status = 'published'
    )
  );

create policy "Public can read podcasts linked to published briefings"
  on public.podcasts for select
  using (
    exists (
      select 1
      from public.daily_briefings b
      where b.id = podcasts.daily_briefing_id
        and b.status = 'published'
    )
    or exists (
      select 1
      from public.weekly_briefings b
      where b.id = podcasts.weekly_briefing_id
        and b.status = 'published'
    )
  );
