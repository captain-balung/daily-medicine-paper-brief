import argparse

from workers.ai_analysis.anthropic_client import AnthropicClient
from workers.shared.config import load_settings
from workers.shared.persistence import PipelineRepository
from workers.shared.podcast_style import FIXED_DAILY_PODCAST_OPENING
from workers.shared.supabase_rest import SupabaseRestClient


TARGET_PODCAST_MINUTES = 7
TARGET_ARTICLE_COUNT = 3

SYSTEM_PROMPT = f"""You write professional Traditional Chinese medical podcast scripts.
Audience: nephrologists, internists, residents, researchers, and medical teachers in Taiwan.
Use a clear spoken style. Retain essential English medical terms.
Do not give direct treatment instructions. Do not imply full-text analysis.
Be explicit that the content is AI-assisted and based on abstracts, metadata, and source links.
Target a concise {TARGET_PODCAST_MINUTES}-minute morning commute briefing.
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
    generated_body = client.create_text(
        system=SYSTEM_PROMPT,
        user=_podcast_prompt(bundle),
        max_tokens=2200,
    )
    script = f"{FIXED_DAILY_PODCAST_OPENING}\n\n{generated_body.strip()}"
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
    for index, item in enumerate(items[:TARGET_ARTICLE_COUNT], start=1):
        article = item.get("article") or {}
        summary = item.get("summary") or {}
        score = item.get("score") or {}
        article_lines.append(
            f"""Article {index}
Chinese title: {article.get("title_zh") or article.get("title")}
Original title: {article.get("title")}
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

    return f"""Create a concise approximately {TARGET_PODCAST_MINUTES}-minute daily medical podcast script from this briefing.

Hard length rules:
- Target about 1,100-1,400 Traditional Chinese characters total.
- Cover only the top {TARGET_ARTICLE_COUNT} selected articles in detail.
- Keep each article segment around 70-90 seconds.
- Use short spoken sentences.
- Do not read journal names, PMID, DOI, or long disclaimers aloud unless essential.

Required structure:
1. Start directly with today's three themes, about 30 seconds: exactly three spoken bullets.
2. Top three articles: for each article, answer what was asked, how it was studied, what was found, why it matters, and the key limitation.
3. Short deep-dive bridge: one concise paragraph connecting clinical meaning or mechanism across the papers.
4. Take-home messages, about 20 seconds: exactly three short points.
5. Closing notice: one sentence only, saying this is AI-assisted literature briefing based on abstracts, metadata, and source links, not clinical decision advice.

Style:
- Conversational but professional.
- Avoid hype.
- Prefer compact paragraphs over long monologues.
- Use paragraph breaks suitable for reading aloud.
- Keep English medical terms where they improve precision.
- Do not mention audio production or TTS.
- Do not write a host introduction, greeting, or opening monologue. A fixed opening will be inserted before your script.

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
