import argparse

from workers.ai_analysis.run import run_ai_analysis
from workers.daily_pipeline.generate_briefing import generate_daily_briefing
from workers.daily_pipeline.main import run_daily_pipeline
from workers.shared.config import load_settings
from workers.shared.persistence import PipelineRepository
from workers.shared.supabase_rest import SupabaseRestClient


def run_full_daily_pipeline(ai_limit: int, dry_run: bool = False) -> int:
    collect_status, job_id = run_daily_pipeline(dry_run=dry_run)
    if collect_status != 0 or dry_run:
        return collect_status

    settings = load_settings()
    repository = PipelineRepository(
        SupabaseRestClient(
            supabase_url=settings.supabase_url or "",
            secret_key=settings.supabase_secret_key or "",
        )
    )

    ai_result = run_ai_analysis(limit=ai_limit)
    print(
        "daily_ai="
        f"checked:{ai_result['checked']} "
        f"analyzed:{ai_result['analyzed']} "
        f"failed:{ai_result['failed']}"
    )
    if job_id:
        repository.log_event(
            job_id,
            event_type="info",
            step_name="ai_analysis",
            message=(
                f"Checked {ai_result['checked']} articles; "
                f"analyzed {ai_result['analyzed']}; failed {ai_result['failed']}."
            ),
        )

    briefing_id = generate_daily_briefing(limit=10)
    print(f"daily_briefing={briefing_id}")
    if job_id:
        repository.log_event(
            job_id,
            event_type="info",
            step_name="daily_briefing",
            message=f"Generated daily briefing {briefing_id}.",
        )
    return 0 if ai_result["failed"] == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ai-limit", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    raise SystemExit(
        run_full_daily_pipeline(ai_limit=args.ai_limit, dry_run=args.dry_run)
    )


if __name__ == "__main__":
    main()
