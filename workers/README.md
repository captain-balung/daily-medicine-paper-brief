# Workers

Python workers run collection, analysis, and briefing generation outside Vercel.

First-version scope:

- Daily pipeline only
- Core sources: PubMed, Crossref, Unpaywall
- Anthropic for AI analysis
- Auto-publish after readiness and safety checks pass
- No podcast, audio, or TTS

## Local health check

```bash
python -m workers.health
```

## Daily dry run

```bash
python -m workers.daily_pipeline.main --dry-run
```
