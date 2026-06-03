SYSTEM_PROMPT = """You are a careful medical research intelligence assistant.
Use professional Traditional Chinese. Retain important English medical terms.
Do not claim full-text analysis when only title, abstract, and metadata are provided.
Do not give direct clinical treatment instructions.
Return the analysis by calling the save_article_analysis tool.
"""


def article_analysis_prompt(article: dict) -> str:
    return f"""Analyze this medical literature item for a nephrologist/internist audience.

Use only the provided title, abstract, and metadata.

Required JSON shape:
{{
  "primary_topic": "one of: nephrology, dialysis, ckd, cardiovascular, metabolism, geriatrics, internal_medicine, ai_medicine, basic_translational, drug_safety_guidelines, interesting_medicine",
  "secondary_topics": ["topic slug"],
  "topic_confidence": 0.0,
  "study_type": "Randomized controlled trial | Meta-analysis | Systematic review | Guideline | Cohort study | Case-control study | Cross-sectional study | Case report | Case series | Basic science | Animal study | Cell study | Omics study | AI model study | Regulatory alert | Public health announcement | Editorial | News | Commentary",
  "evidence_strength": 1,
  "scores": {{
    "clinical_impact": 1,
    "evidence_strength": 1,
    "novelty": 1,
    "specialty_relevance": 1,
    "teaching_research_value": 1,
    "podcast_suitability": 1
  }},
  "recommendation_level": "must_read | important | worth_tracking | background | low_priority",
  "scoring_rationale": "Traditional Chinese, concise",
  "title_zh": "Traditional Chinese title",
  "one_sentence_summary": "Traditional Chinese",
  "background": "Traditional Chinese",
  "methods": "Traditional Chinese",
  "main_findings": "Traditional Chinese",
  "author_conclusion": "Traditional Chinese",
  "clinical_implications": "Traditional Chinese, no direct instructions",
  "basic_mechanism": "Traditional Chinese",
  "clinical_basic_translation": "Traditional Chinese",
  "limitations": "Traditional Chinese; include abstract-only limitation",
  "taiwan_relevance": "Traditional Chinese",
  "teaching_use": "Traditional Chinese",
  "research_use": "Traditional Chinese",
  "access_warning": "Traditional Chinese warning based on access_status"
}}

Scoring: every score must be integer 1-5. evidence_strength cannot be 5 unless the item is a large RCT, official guideline, or high-quality meta-analysis.

Article:
id: {article.get("id")}
title: {article.get("title")}
journal: {article.get("journal")}
publisher: {article.get("publisher")}
publication_date: {article.get("publication_date")}
doi: {article.get("doi")}
pmid: {article.get("pmid")}
access_status: {article.get("access_status")}
is_open_access: {article.get("is_open_access")}
abstract:
{article.get("abstract") or "(no abstract provided)"}
"""
