import argparse

from workers.ai_analysis.anthropic_client import AnthropicClient
from workers.ai_analysis.prompts import SYSTEM_PROMPT, article_analysis_prompt
from workers.shared.config import load_settings
from workers.shared.persistence import PipelineRepository
from workers.shared.supabase_rest import SupabaseRestClient


def run_ai_analysis(limit: int) -> dict[str, int]:
    settings = load_settings()
    repository = PipelineRepository(
        SupabaseRestClient(
            supabase_url=settings.supabase_url or "",
            secret_key=settings.supabase_secret_key or "",
        )
    )
    client = AnthropicClient(settings=settings)

    articles = repository.list_articles_for_ai(limit=limit)
    analyzed = 0
    failed = 0

    for article in articles:
        try:
            result = client.create_json(
                system=SYSTEM_PROMPT,
                user=article_analysis_prompt(article),
            )
            repository.save_ai_analysis(article_id=article["id"], analysis=result)
            analyzed += 1
            print(f"analyzed=pmid:{article.get('pmid')} title:{article.get('title', '')[:80]}")
        except Exception as exc:
            failed += 1
            print(f"failed=pmid:{article.get('pmid')} error:{exc}")

    return {"checked": len(articles), "analyzed": analyzed, "failed": failed}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    result = run_ai_analysis(limit=args.limit)
    print(
        "ai_analysis="
        f"checked:{result['checked']} "
        f"analyzed:{result['analyzed']} "
        f"failed:{result['failed']}"
    )


if __name__ == "__main__":
    main()
