alter table public.podcasts
  add column if not exists video_storage_path text,
  add column if not exists video_url text,
  add column if not exists video_generated_at timestamptz;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'podcast-videos',
  'podcast-videos',
  true,
  209715200,
  array['video/mp4']::text[]
)
on conflict (id) do update set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;
