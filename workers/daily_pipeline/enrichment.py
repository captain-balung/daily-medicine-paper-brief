from workers.collectors.crossref import CrossrefEnricher
from workers.collectors.unpaywall import UnpaywallChecker
from workers.shared.config import Settings
from workers.shared.persistence import PipelineRepository


def enrich_articles(
    repository: PipelineRepository,
    settings: Settings,
    limit: int = 100,
) -> dict[str, int]:
    crossref = CrossrefEnricher(settings=settings)
    unpaywall = UnpaywallChecker(settings=settings)
    articles = repository.list_articles_for_enrichment(limit=limit)

    enriched = 0
    failed = 0

    for article in articles:
        try:
            doi = article.get("doi")
            raw_metadata = article.get("raw_metadata") or {}

            crossref_metadata = crossref.fetch_metadata(doi)
            access = unpaywall.check(doi)

            merged_metadata = {
                **raw_metadata,
                "crossref": _compact_crossref(crossref_metadata),
                "unpaywall": access.raw_metadata or {},
            }

            publisher = crossref_metadata.get("publisher") or article.get("publisher")
            repository.update_article_enrichment(
                article["id"],
                publisher=publisher,
                access_status=access.access_status,
                is_open_access=access.is_open_access,
                full_text_available=access.is_open_access,
                full_text_source=access.best_oa_url,
                raw_metadata=merged_metadata,
            )
            enriched += 1
        except Exception:
            failed += 1

    return {"checked": len(articles), "enriched": enriched, "failed": failed}


def _compact_crossref(metadata: dict) -> dict:
    if not metadata:
        return {}

    return {
        "doi": metadata.get("DOI"),
        "publisher": metadata.get("publisher"),
        "container_title": metadata.get("container-title"),
        "type": metadata.get("type"),
        "published": metadata.get("published-print") or metadata.get("published-online"),
        "license": metadata.get("license"),
        "is_referenced_by_count": metadata.get("is-referenced-by-count"),
        "relation": metadata.get("relation"),
    }
