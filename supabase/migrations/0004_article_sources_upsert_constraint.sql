alter table public.article_sources
  add constraint article_sources_source_id_source_identifier_key
  unique (source_id, source_identifier);
