import argparse

from workers.ai_analysis.anthropic_client import AnthropicClient
from workers.shared.config import load_settings
from workers.shared.persistence import PipelineRepository
from workers.shared.supabase_rest import SupabaseRestClient


SYSTEM_PROMPT = """You write professional Traditional Chinese medical podcast scripts.
Audience: nephrologists, internists, residents, researchers, and medical teachers in Taiwan.
Use a clear spoken style. Retain essential English medical terms.
Do not give direct treatment instructions. Do not imply full-text analysis.
Be explicit that the content is AI-assisted and based on abstracts, metadata, and source links.
Return only the script text, with section headings.
"""


def generate_daily_podcast_script(briefing_id: str) -> str:
    settings = load_settings()
    repository = PipelineRepository(
        SupabaseRestClient(
            supabase_url=settings.supabase_url or "",
            secret_key=settings.supabase_secret_key or "",
        )
    )
    bundle = repository.get_daily_briefing_bundle(briefing_id)
    if not bundle:
        raise RuntimeError(f"Daily briefing not found: {briefing_id}")

    client = AnthropicClient(settings)
    script = client.create_text(
        system=SYSTEM_PROMPT,
        user=_podcast_prompt(bundle),
        max_tokens=3600,
    )
    podcast_id = repository.save_daily_podcast_script(
        briefing_id=briefing_id,
        title=f"{bundle['briefing']['briefing_date']} Daily Medicine Podcast Script",
        script=script,
    )
    print(f"daily_podcast_script={podcast_id}")
    return podcast_id


def _podcast_prompt(bundle: dict) -> str:
    briefing = bundle["briefing"]
    items = [item for item in bundle["items"] if item.get("section") == "must_read"]
    if not items:
        items = bundle["items"]

    article_lines = []
    for index, item in enumerate(items[:5], start=1):
        article = item.get("article") or {}
        summary = item.get("summary") or {}
        score = item.get("score") or {}
        article_lines.append(
            f"""Article {index}
Chinese title: {article.get("title_zh") or article.get("title")}
Original title: {article.get("title")}
Journal: {article.get("journal")}
Study type: {article.get("article_type")}
Access status: {article.get("access_status")}
Score: {score.get("total_score")}
Podcast suitability: {score.get("podcast_suitability")}
One sentence: {summary.get("one_sentence_summary") or item.get("item_summary")}
Clinical implications: {summary.get("clinical_implications")}
Clinical-basic translation: {summary.get("clinical_basic_translation")}
Limitations: {summary.get("limitations")}
Taiwan relevance: {summary.get("taiwan_relevance")}
Teaching/research use: {summary.get("teaching_use") or summary.get("research_use")}
"""
        )

    return f"""Create an 8-12 minute daily medical podcast script from this briefing.

Required structure:
1. 開場：date, what this episode covers, one safety sentence.
2. 今日快速重點：3-5 concise bullets written as spoken lines.
3. 逐篇導讀：for each selected article, explain why it matters, what the evidence can and cannot support, and how it might inform clinical thinking, teaching, or research.
4. 臨床與基礎轉譯：connect clinical findings with mechanism when possible.
5. 今日 take-home messages：3 short points.
6. 結尾聲明：AI-assisted, abstract/metadata/source-link based, not clinical decision advice.

Style:
- Conversational but professional.
- Avoid hype.
- Use paragraph breaks suitable for reading aloud.
- Keep English medical terms where they improve precision.
- Do not mention audio production or TTS.

Briefing:
date: {briefing.get("briefing_date")}
title: {briefing.get("title")}
summary: {briefing.get("summary")}
overview: {briefing.get("trend_overview")}
clinical_basic_section: {briefing.get("clinical_basic_section")}
interesting_medicine_section: {briefing.get("interesting_medicine_section")}

Articles:
{chr(10).join(article_lines)}
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("briefing_id")
    args = parser.parse_args()
    generate_daily_podcast_script(args.briefing_id)


if __name__ == "__main__":
    main()
