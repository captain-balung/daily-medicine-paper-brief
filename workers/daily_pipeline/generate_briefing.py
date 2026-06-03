import argparse

from workers.shared.config import load_settings
from workers.shared.persistence import PipelineRepository
from workers.shared.supabase_rest import SupabaseRestClient
from workers.shared.time_window import daily_window


def generate_daily_briefing(limit: int = 10) -> str:
    settings = load_settings()
    window = daily_window(settings.timezone)
    repository = PipelineRepository(
        SupabaseRestClient(
            supabase_url=settings.supabase_url or "",
            secret_key=settings.supabase_secret_key or "",
        )
    )
    items = repository.list_top_analyzed_articles(limit=limit)
    briefing_id = repository.save_daily_briefing(
        briefing_date=window.end.date().isoformat(),
        source_window_start=window.start.isoformat(),
        source_window_end=window.end.isoformat(),
        top_items=items,
    )
    print(f"daily_briefing_id={briefing_id}")
    print(f"items={min(len(items), 5)}")
    return briefing_id


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    generate_daily_briefing(limit=args.limit)


if __name__ == "__main__":
    main()
