import os

from workers.daily_pipeline.full_run import run_full_daily_pipeline
from workers.shared.config import load_settings


def main() -> None:
    settings = load_settings()
    missing = [
        name
        for name, value in {
            "SUPABASE_URL": settings.supabase_url,
            "SUPABASE_SECRET_KEY": settings.supabase_secret_key,
            "ANTHROPIC_API_KEY": settings.anthropic_api_key,
            "UNPAYWALL_EMAIL": settings.unpaywall_email,
            "CROSSREF_MAILTO": settings.crossref_mailto,
        }.items()
        if not value
    ]
    if settings.publication_mode != "auto_publish":
        missing.append("PUBLICATION_MODE=auto_publish")
    if set(settings.mvp_sources) != {"pubmed", "crossref", "unpaywall"}:
        missing.append("MVP_SOURCES=pubmed,crossref,unpaywall")

    if missing:
        print("render_daily=blocked")
        print("missing=" + ",".join(missing))
        raise SystemExit(2)

    ai_limit = int(os.getenv("DAILY_AI_LIMIT", "10"))
    raise SystemExit(run_full_daily_pipeline(ai_limit=ai_limit))


if __name__ == "__main__":
    main()
