create policy "Public can read pipeline job status"
  on public.pipeline_jobs for select
  using (true);

create policy "Public can read pipeline job events"
  on public.pipeline_job_events for select
  using (true);
