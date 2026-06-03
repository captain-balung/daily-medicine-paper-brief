import argparse

from workers.collectors.pubmed import PubMedCollector
from workers.daily_pipeline.enrichment import enrich_articles
from workers.shared.config import load_settings
from workers.shared.persistence import PipelineRepository
from workers.shared.supabase_rest import SupabaseRestClient
from workers.shared.time_window import daily_window


def run_daily_pipeline(dry_run: bool = False) -> tuple[int, str | None]:
    settings = load_settings()
    checks = settings.health_checks()
    missing = [name for name, ok in checks.items() if not ok]

    if missing:
        print("status=setup_required")
        print("missing=" + ",".join(missing))
        return (1, None)

    window = daily_window(settings.timezone)
    print(f"status=running dry_run={dry_run}")
    print(f"window_start={window.start.isoformat()}")
    print(f"window_end={window.end.isoformat()}")

    repository = None
    job_id = None
    if not dry_run:
        repository = PipelineRepository(
            SupabaseRestClient(
                supabase_url=settings.supabase_url or "",
                secret_key=settings.supabase_secret_key or "",
            )
        )
        job_id = repository.create_job("daily", window)

    collector = PubMedCollector(settings=settings)
    try:
        candidates = collector.collect(window)
        print(f"source=pubmed candidates={len(candidates)}")

        for candidate in candidates[:5]:
            print(
                "candidate="
                f"pmid:{candidate.pmid or ''} "
                f"doi:{candidate.doi or ''} "
                f"title:{candidate.title[:120]}"
            )

        if dry_run:
            print("status=dry_run_succeeded")
            return (0, None)

        saved = repository.save_articles(candidates) if repository else 0
        enrichment_result = (
            enrich_articles(repository, settings, limit=max(len(candidates), 1))
            if repository
            else {"checked": 0, "enriched": 0, "failed": 0}
        )
        if repository and job_id:
            repository.log_event(
                job_id,
                event_type="info",
                step_name="pubmed_collect",
                message=f"Collected {len(candidates)} PubMed candidates; saved {saved}.",
            )
            repository.log_event(
                job_id,
                event_type="info",
                step_name="core_enrichment",
                message=(
                    f"Checked {enrichment_result['checked']} articles; "
                    f"enriched {enrichment_result['enriched']}; "
                    f"failed {enrichment_result['failed']}."
                ),
            )
            repository.finish_job(
                job_id,
                status="partial_success"
                if enrichment_result["failed"]
                else "succeeded",
                total_candidates=len(candidates),
                total_articles_saved=saved,
                total_failed=enrichment_result["failed"],
            )

        print(f"saved_articles={saved}")
        print(
            "enrichment="
            f"checked:{enrichment_result['checked']} "
            f"enriched:{enrichment_result['enriched']} "
            f"failed:{enrichment_result['failed']}"
        )
        print("status=succeeded")
        return (0, job_id)
    except Exception as exc:
        if repository and job_id:
            repository.finish_job(
                job_id,
                status="failed",
                total_candidates=0,
                total_articles_saved=0,
                total_failed=1,
                error_message=str(exc),
            )
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    status, _job_id = run_daily_pipeline(dry_run=args.dry_run)
    raise SystemExit(status)


if __name__ == "__main__":
    main()
