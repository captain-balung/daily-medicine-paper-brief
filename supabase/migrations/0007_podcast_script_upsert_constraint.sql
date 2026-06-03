do $$
begin
  if not exists (
    select 1
    from pg_constraint
    where conname = 'podcasts_daily_unique'
  ) then
    alter table public.podcasts
      add constraint podcasts_daily_unique unique (podcast_type, daily_briefing_id);
  end if;
end $$;
