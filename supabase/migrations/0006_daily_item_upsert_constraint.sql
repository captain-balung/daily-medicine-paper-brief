alter table public.daily_briefing_items
  add constraint daily_briefing_items_briefing_article_section_key
  unique (daily_briefing_id, article_id, section);
