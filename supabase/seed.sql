insert into public.topics (slug, name_en, name_zh, default_weight, is_active)
values
  ('nephrology', 'Nephrology', 'Nephrology', 5, true),
  ('dialysis', 'Dialysis', 'Dialysis', 5, true),
  ('ckd', 'CKD', 'CKD', 5, true),
  ('cardiovascular', 'Cardiovascular Medicine', 'Cardiovascular Medicine', 4, true),
  ('metabolism', 'Metabolism', 'Metabolism', 4, true),
  ('geriatrics', 'Geriatrics', 'Geriatrics', 4, true),
  ('internal_medicine', 'Internal Medicine', 'Internal Medicine', 3, true),
  ('ai_medicine', 'AI Medicine and Digital Health', 'AI Medicine and Digital Health', 4, true),
  ('basic_translational', 'Basic and Translational Research', 'Basic and Translational Research', 3, true),
  ('drug_safety_guidelines', 'Drug Safety and Guideline Updates', 'Drug Safety and Guideline Updates', 4, true),
  ('interesting_medicine', 'Interesting Medicine', 'Interesting Medicine', 2, true)
on conflict (slug) do update set
  name_en = excluded.name_en,
  name_zh = excluded.name_zh,
  default_weight = excluded.default_weight,
  is_active = excluded.is_active;

insert into public.sources (name, source_type, base_url, priority_level, is_enabled, config)
values
  ('PubMed', 'literature_api', 'https://pubmed.ncbi.nlm.nih.gov', 'high', true, '{"mvp": true}'::jsonb),
  ('Crossref', 'metadata_api', 'https://api.crossref.org', 'high', true, '{"mvp": true}'::jsonb),
  ('Unpaywall', 'access_api', 'https://api.unpaywall.org', 'high', true, '{"mvp": true}'::jsonb)
on conflict do nothing;

insert into public.system_settings (key, value, description)
values
  ('system_status', '"SETUP_REQUIRED"'::jsonb, 'Human-first setup gate status'),
  ('publication_rules', '{"daily_publication_mode":"auto_publish","weekly_publication_mode":"deferred","require_review":false,"require_podcast_before_publish":false}'::jsonb, 'MVP auto-publish rules'),
  ('mvp_sources', '["pubmed","crossref","unpaywall"]'::jsonb, 'Core first-version source set'),
  ('safety_settings', '{"preprint_warning":true,"evidence_label":true,"limitations":true,"source_citation":true,"medical_disclaimer":true,"paid_full_text_restriction":true}'::jsonb, 'Required medical and copyright safety settings')
on conflict (key) do update set
  value = excluded.value,
  description = excluded.description,
  updated_at = now();
