from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json

from workers.shared.config import Settings


class AnthropicClient:
    base_url = "https://api.anthropic.com/v1/messages"

    def __init__(self, settings: Settings) -> None:
        if not settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is missing.")

        self.api_key = settings.anthropic_api_key
        self.model = settings.anthropic_model

    def create_json(self, system: str, user: str, max_tokens: int = 2200) -> dict:
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": 0.2,
            "system": system,
            "messages": [{"role": "user", "content": user}],
            "tools": [_article_analysis_tool()],
            "tool_choice": {"type": "tool", "name": "save_article_analysis"},
        }
        request = Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=60) as response:
                message = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Anthropic API error {exc.code}: {body}") from exc

        for block in message.get("content", []):
            if block.get("type") == "tool_use" and block.get("name") == "save_article_analysis":
                return block.get("input", {})

        text = "\n".join(
            block.get("text", "")
            for block in message.get("content", [])
            if block.get("type") == "text"
        )
        return _parse_json_text(text)


def _parse_json_text(text: str) -> dict:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"Anthropic response did not contain JSON: {text[:200]}")

    return json.loads(stripped[start : end + 1])


def _article_analysis_tool() -> dict:
    string_field = {"type": "string"}
    score_field = {"type": "integer", "minimum": 1, "maximum": 5}

    return {
        "name": "save_article_analysis",
        "description": "Save structured medical literature analysis.",
        "input_schema": {
            "type": "object",
            "properties": {
                "primary_topic": string_field,
                "secondary_topics": {"type": "array", "items": string_field},
                "topic_confidence": {"type": "number"},
                "study_type": string_field,
                "evidence_strength": score_field,
                "scores": {
                    "type": "object",
                    "properties": {
                        "clinical_impact": score_field,
                        "evidence_strength": score_field,
                        "novelty": score_field,
                        "specialty_relevance": score_field,
                        "teaching_research_value": score_field,
                        "podcast_suitability": score_field,
                    },
                    "required": [
                        "clinical_impact",
                        "evidence_strength",
                        "novelty",
                        "specialty_relevance",
                        "teaching_research_value",
                    ],
                },
                "recommendation_level": string_field,
                "scoring_rationale": string_field,
                "title_zh": string_field,
                "one_sentence_summary": string_field,
                "background": string_field,
                "methods": string_field,
                "main_findings": string_field,
                "author_conclusion": string_field,
                "clinical_implications": string_field,
                "basic_mechanism": string_field,
                "clinical_basic_translation": string_field,
                "limitations": string_field,
                "taiwan_relevance": string_field,
                "teaching_use": string_field,
                "research_use": string_field,
                "access_warning": string_field,
            },
            "required": [
                "primary_topic",
                "secondary_topics",
                "topic_confidence",
                "study_type",
                "evidence_strength",
                "scores",
                "recommendation_level",
                "scoring_rationale",
                "title_zh",
                "one_sentence_summary",
                "limitations",
            ],
        },
    }
