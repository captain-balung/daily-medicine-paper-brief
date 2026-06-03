alter table public.article_scores
  add constraint article_scores_article_id_key
  unique (article_id);

alter table public.article_summaries
  add constraint article_summaries_article_id_summary_version_key
  unique (article_id, summary_version);
