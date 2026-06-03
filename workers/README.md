# Workers

Python workers run collection, analysis, and briefing generation outside Vercel.

First-version scope:

- Daily pipeline only
- Core sources: PubMed, Crossref, Unpaywall
- Anthropic for AI analysis
- Auto-publish after readiness and safety checks pass
- Daily podcast script generation
- Manual OpenAI TTS audio generation for podcast script trials

## Local health check

```bash
python -m workers.health
```

## Daily dry run

```bash
python -m workers.daily_pipeline.main --dry-run
```

## Generate podcast audio manually

```bash
python -m workers.daily_pipeline.generate_podcast_audio <podcast-id>
```

This uses `OPENAI_API_KEY`, uploads MP3 output to the public
`podcast-audio` Supabase Storage bucket, and updates the podcast row.
