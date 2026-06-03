import re
import string


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None

    doi = value.strip().lower()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    doi = doi.rstrip(".,;")
    return doi or None


def normalize_pmid(value: str | None) -> str | None:
    if not value:
        return None

    pmid = value.strip()
    return pmid if pmid.isdigit() else None


def normalize_title(value: str | None) -> str | None:
    if not value:
        return None

    title = value.lower()
    title = title.translate(str.maketrans("", "", string.punctuation))
    title = re.sub(r"\s+", " ", title).strip()
    return title or None
