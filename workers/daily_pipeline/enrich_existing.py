import argparse

from workers.daily_pipeline.enrichment import enrich_articles
from workers.shared.config import load_settings
from workers.shared.persistence import PipelineRepository
from workers.shared.supabase_rest import SupabaseRestClient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    settings = load_settings()
    repository = PipelineRepository(
        SupabaseRestClient(
            supabase_url=settings.supabase_url or "",
            secret_key=settings.supabase_secret_key or "",
        )
    )
    result = enrich_articles(repository, settings, limit=args.limit)
    print(
        "enrichment="
        f"checked:{result['checked']} "
        f"enriched:{result['enriched']} "
        f"failed:{result['failed']}"
    )


if __name__ == "__main__":
    main()
