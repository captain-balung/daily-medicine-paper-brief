# Supabase

Apply migrations in order, then apply `seed.sql`.

First-version schema includes:

- Core source metadata
- Articles, topics, scores, and summaries
- Daily and weekly briefing tables
- Pipeline jobs and events
- Profiles, bookmarks, and notes
- System settings and audit logs

Secrets are intentionally not stored in database tables.
