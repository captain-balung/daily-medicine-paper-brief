from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any


@dataclass(frozen=True)
class CandidateArticle:
    source_name: str
    source_type: str
    title: str
    url: str
    abstract: str | None = None
    doi: str | None = None
    pmid: str | None = None
    pmcid: str | None = None
    journal: str | None = None
    publication_date: date | None = None
    authors: list[str] = field(default_factory=list)
    raw_payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PipelineWindow:
    start: datetime
    end: datetime
