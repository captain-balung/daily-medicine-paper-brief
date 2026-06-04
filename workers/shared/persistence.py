from datetime import UTC, datetime

from workers.shared.models import CandidateArticle, PipelineWindow
from workers.shared.normalization import normalize_title
from workers.shared.podcast_style import (
    FAST_OPENING_SPEED,
    FIXED_DAILY_PODCAST_OPENING,
    NORMAL_PODCAST_SPEED,
)
from workers.shared.supabase_rest import SupabaseRestClient


class PipelineRepository:
    def __init__(self, client: SupabaseRestClient) -> None:
        self.client = client
        self._source_ids: dict[str, str] = {}

    def create_job(self, job_type: str, window: PipelineWindow) -> str:
        rows = self.client.insert(
            "pipeline_jobs",
            {
                "job_type": job_type,
                "status": "running",
                "source_window_start": window.start.isoformat(),
                "source_window_end": window.end.isoformat(),
                "started_at": datetime.now(UTC).isoformat(),
                "triggered_by": "manual",
            },
        )
        return rows[0]["id"]

    def finish_job(
        self,
        job_id: str,
        status: str,
        total_candidates: int,
        total_articles_saved: int,
        total_failed: int = 0,
        error_message: str | None = None,
    ) -> None:
        self.client.patch(
            "pipeline_jobs",
            {"id": f"eq.{job_id}"},
            {
                "status": status,
                "finished_at": datetime.now(UTC).isoformat(),
                "total_candidates": total_candidates,
                "total_articles_saved": total_articles_saved,
                "total_failed": total_failed,
                "error_message": error_message,
            },
        )

    def update_job_counts(
        self,
        job_id: str,
        *,
        total_analyzed: int | None = None,
        total_failed: int | None = None,
    ) -> None:
        payload = {}
        if total_analyzed is not None:
            payload["total_analyzed"] = total_analyzed
        if total_failed is not None:
            payload["total_failed"] = total_failed
        if not payload:
            return

        self.client.patch("pipeline_jobs", {"id": f"eq.{job_id}"}, payload)

    def log_event(
        self,
        job_id: str,
        event_type: str,
        step_name: str,
        message: str,
        metadata: dict | None = None,
    ) -> None:
        self.client.insert(
            "pipeline_job_events",
            {
                "pipeline_job_id": job_id,
                "event_type": event_type,
                "step_name": step_name,
                "message": message,
                "metadata": metadata or {},
            },
            returning=False,
        )

    def save_articles(self, articles: list[CandidateArticle]) -> int:
        saved = 0
        source_id = self._source_id("PubMed")

        for article in articles:
            article_rows = self.client.upsert(
                "articles",
                {
                    "title": article.title,
                    "normalized_title": normalize_title(article.title),
                    "abstract": article.abstract,
                    "journal": article.journal,
                    "publication_date": article.publication_date.isoformat()
                    if article.publication_date
                    else None,
                    "doi": article.doi,
                    "pmid": article.pmid,
                    "pmcid": article.pmcid,
                    "url": article.url,
                    "access_status": "UNKNOWN",
                    "is_preprint": False,
                    "is_open_access": False,
                    "full_text_available": False,
                    "raw_metadata": article.raw_payload,
                    "processing_status": "collected",
                },
                on_conflict="pmid",
            )
            if not article_rows:
                continue

            self.client.upsert(
                "article_sources",
                {
                    "article_id": article_rows[0]["id"],
                    "source_id": source_id,
                    "source_url": article.url,
                    "source_identifier": article.pmid,
                    "raw_payload": article.raw_payload,
                },
                on_conflict="source_id,source_identifier",
                returning=False,
            )
            saved += 1

        return saved

    def list_articles_for_enrichment(self, limit: int = 100) -> list[dict]:
        return self.client.get(
            "articles",
            {
                "select": "id,title,doi,publisher,raw_metadata,access_status",
                "doi": "not.is.null",
                "order": "created_at.desc",
                "limit": str(limit),
            },
        )

    def list_articles_for_ai(self, limit: int = 3) -> list[dict]:
        return self.client.get(
            "articles",
            {
                "select": "id,title,abstract,journal,publisher,publication_date,doi,pmid,access_status,is_open_access",
                "abstract": "not.is.null",
                "processing_status": "neq.analyzed",
                "order": "created_at.desc",
                "limit": str(limit),
            },
        )

    def update_article_enrichment(
        self,
        article_id: str,
        *,
        publisher: str | None,
        access_status: str,
        is_open_access: bool,
        full_text_available: bool,
        full_text_source: str | None,
        raw_metadata: dict,
    ) -> None:
        self.client.patch(
            "articles",
            {"id": f"eq.{article_id}"},
            {
                "publisher": publisher,
                "access_status": access_status,
                "is_open_access": is_open_access,
                "full_text_available": full_text_available,
                "full_text_source": full_text_source,
                "raw_metadata": raw_metadata,
                "processing_status": "enriched",
            },
        )

    def save_ai_analysis(self, article_id: str, analysis: dict) -> None:
        topic_slug = analysis.get("primary_topic") or "internal_medicine"
        topic_id = self._topic_id(topic_slug)
        secondary_topics = analysis.get("secondary_topics") or []
        scores = analysis.get("scores") or {}
        evidence_strength = _score(
            scores.get("evidence_strength") or analysis.get("evidence_strength")
        )

        self.client.upsert(
            "article_topics",
            {
                "article_id": article_id,
                "topic_id": topic_id,
                "relevance_score": analysis.get("topic_confidence") or 0.5,
                "is_primary": True,
                "assigned_by": "anthropic",
            },
            on_conflict="article_id,topic_id",
            returning=False,
        )

        for slug in secondary_topics[:3]:
            if slug == topic_slug:
                continue
            try:
                self.client.upsert(
                    "article_topics",
                    {
                        "article_id": article_id,
                        "topic_id": self._topic_id(slug),
                        "relevance_score": 0.5,
                        "is_primary": False,
                        "assigned_by": "anthropic",
                    },
                    on_conflict="article_id,topic_id",
                    returning=False,
                )
            except RuntimeError:
                continue

        component_scores = {
            "clinical_impact": _score(scores.get("clinical_impact")),
            "evidence_strength": evidence_strength,
            "novelty": _score(scores.get("novelty")),
            "specialty_relevance": _score(scores.get("specialty_relevance")),
            "teaching_research_value": _score(scores.get("teaching_research_value")),
        }
        total_score = sum(component_scores.values())

        self.client.upsert(
            "article_scores",
            {
                "article_id": article_id,
                **component_scores,
                "total_score": total_score,
                "recommendation_level": analysis.get("recommendation_level")
                or _recommendation_level(total_score),
                "podcast_suitability": _score(scores.get("podcast_suitability")),
                "scoring_rationale": analysis.get("scoring_rationale"),
            },
            on_conflict="article_id",
            returning=False,
        )

        self.client.upsert(
            "article_summaries",
            {
                "article_id": article_id,
                "summary_version": 1,
                "one_sentence_summary": analysis.get("one_sentence_summary")
                or "Summary unavailable; manual review is required.",
                "background": analysis.get("background"),
                "methods": analysis.get("methods"),
                "main_findings": analysis.get("main_findings"),
                "author_conclusion": analysis.get("author_conclusion"),
                "clinical_implications": analysis.get("clinical_implications"),
                "basic_mechanism": analysis.get("basic_mechanism"),
                "clinical_basic_translation": analysis.get(
                    "clinical_basic_translation"
                ),
                "limitations": analysis.get("limitations")
                or "Analysis is based only on title, abstract, and metadata.",
                "taiwan_relevance": analysis.get("taiwan_relevance"),
                "teaching_use": analysis.get("teaching_use"),
                "research_use": analysis.get("research_use"),
                "access_warning": analysis.get("access_warning"),
                "generated_by": "anthropic",
            },
            on_conflict="article_id,summary_version",
            returning=False,
        )

        self.client.patch(
            "articles",
            {"id": f"eq.{article_id}"},
            {
                "title_zh": analysis.get("title_zh"),
                "article_type": analysis.get("study_type"),
                "processing_status": "analyzed",
            },
        )

    def list_top_analyzed_articles(self, limit: int = 10) -> list[dict]:
        candidate_limit = max(limit * 5, 50)
        score_rows = self.client.get(
            "article_scores",
            {
                "select": "article_id,total_score,recommendation_level,scoring_rationale",
                "order": "total_score.desc",
                "limit": str(candidate_limit),
            },
        )
        topic_slugs_by_article = self._article_topic_slugs(
            [score["article_id"] for score in score_rows]
        )

        bundles = []
        for score in score_rows:
            article_rows = self.client.get(
                "articles",
                {
                    "select": "id,title,title_zh,journal,publisher,publication_date,doi,pmid,url,access_status,article_type",
                    "id": f"eq.{score['article_id']}",
                    "limit": "1",
                },
            )
            summary_rows = self.client.get(
                "article_summaries",
                {
                    "select": "one_sentence_summary,clinical_implications,limitations,taiwan_relevance,teaching_use,research_use,clinical_basic_translation",
                    "article_id": f"eq.{score['article_id']}",
                    "summary_version": "eq.1",
                    "limit": "1",
                },
            )
            if article_rows and summary_rows:
                bundles.append(
                    {
                        "article": article_rows[0],
                        "summary": summary_rows[0],
                        "score": score,
                        "ranking_score": score["total_score"]
                        + _topic_boost(topic_slugs_by_article.get(score["article_id"], [])),
                    }
                )

        return sorted(bundles, key=lambda item: item["ranking_score"], reverse=True)[:limit]

    def _article_topic_slugs(self, article_ids: list[str]) -> dict[str, list[str]]:
        if not article_ids:
            return {}

        rows = self.client.get(
            "article_topics",
            {
                "select": "article_id,topics(slug)",
                "article_id": f"in.({','.join(article_ids)})",
            },
        )
        slugs_by_article: dict[str, list[str]] = {}
        for row in rows:
            topic = row.get("topics")
            if isinstance(topic, list):
                topic = topic[0] if topic else None
            slug = topic.get("slug") if isinstance(topic, dict) else None
            if slug:
                slugs_by_article.setdefault(row["article_id"], []).append(slug)

        return slugs_by_article

    def save_daily_briefing(
        self,
        briefing_date: str,
        source_window_start: str,
        source_window_end: str,
        top_items: list[dict],
    ) -> str:
        top_titles = [
            item["article"].get("title_zh") or item["article"].get("title")
            for item in top_items[:5]
        ]
        title = f"{briefing_date} Daily Medicine Brief"
        summary = "Today: " + "; ".join(top_titles[:3]) if top_titles else "No publishable articles yet."
        trend_overview = (
            "This MVP briefing is generated from PubMed Core source data, "
            "Crossref metadata, Unpaywall access labels, and Anthropic analysis."
        )
        clinical_basic = _first_non_empty(
            [item["summary"].get("clinical_basic_translation") for item in top_items]
        )
        interesting = _first_non_empty(
            [item["summary"].get("teaching_use") for item in reversed(top_items)]
        )

        rows = self.client.upsert(
            "daily_briefings",
            {
                "briefing_date": briefing_date,
                "title": title,
                "status": "published",
                "summary": summary,
                "trend_overview": trend_overview,
                "deep_dive_article_id": top_items[0]["article"]["id"]
                if top_items
                else None,
                "clinical_basic_section": clinical_basic,
                "interesting_medicine_section": interesting,
                "tracking_topics": [],
                "source_window_start": source_window_start,
                "source_window_end": source_window_end,
                "published_at": datetime.now(UTC).isoformat(),
            },
            on_conflict="briefing_date",
        )
        briefing_id = rows[0]["id"]

        for index, item in enumerate(top_items[:5], start=1):
            self.client.upsert(
                "daily_briefing_items",
                {
                    "daily_briefing_id": briefing_id,
                    "article_id": item["article"]["id"],
                    "section": "must_read",
                    "rank": index,
                    "item_summary": item["summary"].get("one_sentence_summary"),
                },
                on_conflict="daily_briefing_id,article_id,section",
                returning=False,
            )

        if top_items:
            self.client.upsert(
                "daily_briefing_items",
                {
                    "daily_briefing_id": briefing_id,
                    "article_id": top_items[0]["article"]["id"],
                    "section": "deep_dive",
                    "rank": 1,
                    "item_summary": top_items[0]["summary"].get(
                        "clinical_implications"
                    )
                    or top_items[0]["summary"].get("one_sentence_summary"),
                },
                on_conflict="daily_briefing_id,article_id,section",
                returning=False,
            )

        return briefing_id

    def get_daily_briefing_bundle(self, briefing_id: str) -> dict | None:
        briefing_rows = self.client.get(
            "daily_briefings",
            {
                "select": "id,briefing_date,title,summary,trend_overview,clinical_basic_section,interesting_medicine_section,source_window_start,source_window_end",
                "id": f"eq.{briefing_id}",
                "limit": "1",
            },
        )
        if not briefing_rows:
            return None

        item_rows = self.client.get(
            "daily_briefing_items",
            {
                "select": "section,rank,item_summary,articles(id,title,title_zh,journal,doi,pmid,access_status,article_type)",
                "daily_briefing_id": f"eq.{briefing_id}",
                "order": "section.asc,rank.asc",
            },
        )
        article_ids = []
        normalized_items = []
        for row in item_rows:
            article = row.get("articles")
            if isinstance(article, list):
                article = article[0] if article else None
            if article:
                article_ids.append(article["id"])
            normalized_items.append({**row, "article": article})

        summaries = self._summaries_by_article(article_ids)
        scores = self._scores_by_article(article_ids)

        return {
            "briefing": briefing_rows[0],
            "items": [
                {
                    **item,
                    "summary": summaries.get(item["article"]["id"], {})
                    if item.get("article")
                    else {},
                    "score": scores.get(item["article"]["id"], {})
                    if item.get("article")
                    else {},
                }
                for item in normalized_items
            ],
        }

    def save_daily_podcast_script(
        self,
        *,
        briefing_id: str,
        title: str,
        script: str,
        voice_name: str | None = None,
    ) -> str:
        rows = self.client.upsert(
            "podcasts",
            {
                "podcast_type": "daily",
                "daily_briefing_id": briefing_id,
                "title": title,
                "status": "script_ready",
                "script": script,
                "transcript": script,
                "duration_seconds": _estimated_duration_seconds(script),
                "voice_name": voice_name,
                "tts_provider": None,
                "is_ai_generated": True,
                "generated_at": datetime.now(UTC).isoformat(),
            },
            on_conflict="podcast_type,daily_briefing_id",
        )
        return rows[0]["id"]

    def get_podcast(self, podcast_id: str) -> dict | None:
        rows = self.client.get(
            "podcasts",
            {
                "select": "id,podcast_type,daily_briefing_id,weekly_briefing_id,title,status,script,transcript,audio_storage_path,audio_url,video_storage_path,video_url,video_generated_at,duration_seconds,voice_name,tts_provider,generated_at",
                "id": f"eq.{podcast_id}",
                "limit": "1",
            },
        )
        return rows[0] if rows else None

    def update_podcast_audio(
        self,
        podcast_id: str,
        *,
        audio_storage_path: str,
        audio_url: str,
        voice_name: str,
        tts_provider: str,
        duration_seconds: int | None = None,
    ) -> None:
        payload = {
            "status": "audio_ready",
            "audio_storage_path": audio_storage_path,
            "audio_url": audio_url,
            "voice_name": voice_name,
            "tts_provider": tts_provider,
            "updated_at": datetime.now(UTC).isoformat(),
        }
        if duration_seconds:
            payload["duration_seconds"] = duration_seconds

        self.client.patch(
            "podcasts",
            {"id": f"eq.{podcast_id}"},
            payload,
        )

    def update_podcast_video(
        self,
        podcast_id: str,
        *,
        video_storage_path: str,
        video_url: str,
    ) -> None:
        self.client.patch(
            "podcasts",
            {"id": f"eq.{podcast_id}"},
            {
                "video_storage_path": video_storage_path,
                "video_url": video_url,
                "video_generated_at": datetime.now(UTC).isoformat(),
                "updated_at": datetime.now(UTC).isoformat(),
            },
        )

    def _summaries_by_article(self, article_ids: list[str]) -> dict[str, dict]:
        if not article_ids:
            return {}

        rows = self.client.get(
            "article_summaries",
            {
                "select": "article_id,one_sentence_summary,clinical_implications,clinical_basic_translation,limitations,taiwan_relevance,teaching_use,research_use",
                "article_id": f"in.({','.join(article_ids)})",
                "summary_version": "eq.1",
            },
        )
        return {row["article_id"]: row for row in rows}

    def _scores_by_article(self, article_ids: list[str]) -> dict[str, dict]:
        if not article_ids:
            return {}

        rows = self.client.get(
            "article_scores",
            {
                "select": "article_id,total_score,recommendation_level,scoring_rationale,podcast_suitability",
                "article_id": f"in.({','.join(article_ids)})",
            },
        )
        return {row["article_id"]: row for row in rows}

    def _source_id(self, name: str) -> str:
        if name in self._source_ids:
            return self._source_ids[name]

        rows = self.client.get("sources", {"select": "id", "name": f"eq.{name}"})
        if not rows:
            raise RuntimeError(f"Missing source row: {name}")

        self._source_ids[name] = rows[0]["id"]
        return self._source_ids[name]

    def _topic_id(self, slug: str) -> str:
        rows = self.client.get("topics", {"select": "id", "slug": f"eq.{slug}"})
        if not rows:
            raise RuntimeError(f"Missing topic row: {slug}")
        return rows[0]["id"]


def _score(value) -> int:
    try:
        return max(1, min(5, int(value)))
    except Exception:
        return 1


def _recommendation_level(total_score: int) -> str:
    if total_score >= 22:
        return "must_read"
    if total_score >= 18:
        return "important"
    if total_score >= 14:
        return "worth_tracking"
    if total_score >= 10:
        return "background"
    return "low_priority"


def _topic_boost(topic_slugs: list[str]) -> int:
    boosts = {
        "nephrology": 5,
        "dialysis": 5,
        "ckd": 5,
        "cardiovascular": 2,
        "metabolism": 2,
        "ai_medicine": 2,
        "internal_medicine": 1,
        "basic_translational": 1,
    }
    return min(8, sum(boosts.get(slug, 0) for slug in set(topic_slugs)))


def _estimated_duration_seconds(script: str) -> int:
    # Mandarin medical narration is usually around 280-340 compact characters per minute.
    compact_script = "".join(script.split())
    compact_opening = "".join(FIXED_DAILY_PODCAST_OPENING.split())
    chars_per_minute = 310

    if compact_script.startswith(compact_opening):
        opening_seconds = len(compact_opening) / (
            chars_per_minute * FAST_OPENING_SPEED
        ) * 60
        rest_seconds = (len(compact_script) - len(compact_opening)) / (
            chars_per_minute * NORMAL_PODCAST_SPEED
        ) * 60
        return max(60, round(opening_seconds + rest_seconds))

    return max(60, round(len(compact_script) / chars_per_minute * 60))


def _first_non_empty(values: list[str | None]) -> str | None:
    for value in values:
        if value:
            return value
    return None
