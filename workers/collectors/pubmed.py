from datetime import date
from urllib.parse import urlencode
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from workers.shared.config import Settings
from workers.shared.models import CandidateArticle, PipelineWindow
from workers.shared.normalization import normalize_doi, normalize_pmid


class PubMedCollector:
    source_name = "PubMed"
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self, settings: Settings, retmax: int = 50) -> None:
        self.settings = settings
        self.retmax = retmax

    def collect(self, window: PipelineWindow) -> list[CandidateArticle]:
        pmids = self.search_pmids(window)
        if not pmids:
            return []

        return self.fetch_articles(pmids)

    def search_pmids(self, window: PipelineWindow) -> list[str]:
        params = {
            "db": "pubmed",
            "term": self._query_term(),
            "retmode": "json",
            "retmax": str(self.retmax),
            "sort": "pub+date",
            "datetype": "pdat",
            "mindate": window.start.strftime("%Y/%m/%d"),
            "maxdate": window.end.strftime("%Y/%m/%d"),
        }
        if self.settings.ncbi_api_key:
            params["api_key"] = self.settings.ncbi_api_key

        root = self._get_json("esearch.fcgi", params)
        return [
            normalize_pmid(pmid)
            for pmid in root.get("esearchresult", {}).get("idlist", [])
            if normalize_pmid(pmid)
        ]

    def fetch_articles(self, pmids: list[str]) -> list[CandidateArticle]:
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
        }
        if self.settings.ncbi_api_key:
            params["api_key"] = self.settings.ncbi_api_key

        xml_text = self._get_text("efetch.fcgi", params)
        root = ET.fromstring(xml_text)
        articles = []

        for article_node in root.findall(".//PubmedArticle"):
            article = self._parse_article(article_node)
            if article:
                articles.append(article)

        return articles

    def _parse_article(self, node: ET.Element) -> CandidateArticle | None:
        pmid = normalize_pmid(_text(node, ".//MedlineCitation/PMID"))
        title = _join_text(node, ".//Article/ArticleTitle")
        if not pmid or not title:
            return None

        journal = _text(node, ".//Article/Journal/Title")
        abstract = _abstract_text(node)
        doi = normalize_doi(_article_id(node, "doi"))
        publication_date = _publication_date(node)
        authors = _authors(node)

        return CandidateArticle(
            source_name=self.source_name,
            source_type="literature_api",
            title=title,
            abstract=abstract,
            url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            doi=doi,
            pmid=pmid,
            journal=journal,
            publication_date=publication_date,
            authors=authors,
            raw_payload={"pmid": pmid},
        )

    def _get_json(self, endpoint: str, params: dict[str, str]) -> dict:
        import json

        return json.loads(self._get_text(endpoint, params))

    def _get_text(self, endpoint: str, params: dict[str, str]) -> str:
        url = f"{self.base_url}/{endpoint}?{urlencode(params)}"
        with urlopen(url, timeout=30) as response:
            return response.read().decode("utf-8")

    def _query_term(self) -> str:
        return (
            "(kidney OR renal OR nephrology OR dialysis OR hemodialysis OR "
            "peritoneal dialysis OR CKD OR chronic kidney disease OR acute kidney "
            "injury OR proteinuria OR electrolyte OR acid-base OR glomerular OR "
            "cardiorenal OR vascular calcification) OR "
            "(heart failure OR cardiovascular outcomes OR diabetes OR obesity OR "
            "SGLT2 OR GLP-1 OR finerenone OR hypertension OR metabolic syndrome OR "
            "fatty liver) OR "
            "(frailty OR sarcopenia OR dementia OR falls OR polypharmacy OR aging "
            "OR long-term care) OR "
            "(artificial intelligence OR machine learning OR large language model "
            "OR clinical decision support OR digital health OR remote monitoring "
            "OR wearable OR medical AI)"
        )


def _text(node: ET.Element, path: str) -> str | None:
    match = node.find(path)
    if match is None or match.text is None:
        return None

    value = match.text.strip()
    return value or None


def _join_text(node: ET.Element, path: str) -> str | None:
    match = node.find(path)
    if match is None:
        return None

    value = "".join(match.itertext()).strip()
    return value or None


def _abstract_text(node: ET.Element) -> str | None:
    parts = []
    for abstract_node in node.findall(".//Article/Abstract/AbstractText"):
        label = abstract_node.attrib.get("Label")
        text = " ".join("".join(abstract_node.itertext()).split())
        if not text:
            continue
        parts.append(f"{label}: {text}" if label else text)

    return "\n".join(parts) if parts else None


def _article_id(node: ET.Element, id_type: str) -> str | None:
    for article_id in node.findall(".//PubmedData/ArticleIdList/ArticleId"):
        if article_id.attrib.get("IdType") == id_type and article_id.text:
            return article_id.text.strip()

    return None


def _authors(node: ET.Element) -> list[str]:
    authors = []
    for author in node.findall(".//Article/AuthorList/Author"):
        last_name = _text(author, "./LastName")
        fore_name = _text(author, "./ForeName")
        collective = _text(author, "./CollectiveName")
        if collective:
            authors.append(collective)
        elif last_name and fore_name:
            authors.append(f"{fore_name} {last_name}")
        elif last_name:
            authors.append(last_name)

    return authors


def _publication_date(node: ET.Element) -> date | None:
    date_node = node.find(".//Article/Journal/JournalIssue/PubDate")
    if date_node is None:
        return None

    year = _text(date_node, "./Year")
    month = _text(date_node, "./Month")
    day = _text(date_node, "./Day")
    if not year or not year.isdigit():
        return None

    return date(
        int(year),
        _parse_month(month) if month else 1,
        int(day) if day and day.isdigit() else 1,
    )


def _parse_month(value: str | None) -> int:
    if not value:
        return 1
    if value.isdigit():
        return max(1, min(12, int(value)))

    months = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }
    return months.get(value[:3].lower(), 1)
