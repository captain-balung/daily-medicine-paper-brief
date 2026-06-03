import { ArticleCard } from "@/components/article-card";
import { getAnalyzedArticleItems } from "@/lib/articles";
import type { DailyBriefingItem } from "@/lib/daily-briefings";

export const dynamic = "force-dynamic";

type ArticlesSearchParams = {
  access?: string;
  type?: string;
  minScore?: string;
  sort?: string;
};

export default async function ArticlesIndexPage({
  searchParams,
}: {
  searchParams: Promise<ArticlesSearchParams>;
}) {
  const params = await searchParams;
  const allItems = await getAnalyzedArticleItems(100);
  const filteredItems = applyArticleFilters(allItems, params);
  const articleTypes = getArticleTypes(allItems);
  const openAccessCount = filteredItems.filter(
    (item) => item.article?.access_status === "OPEN_ACCESS",
  ).length;
  const unknownAccessCount = filteredItems.filter(
    (item) => item.article?.access_status === "UNKNOWN",
  ).length;

  return (
    <main className="page">
      <h1 className="page-title">Analyzed articles</h1>
      <p className="lede">
        Filter and sort analyzed papers by access status, article type, score,
        and ranking signal.
      </p>

      <FilterPanel params={params} articleTypes={articleTypes} />

      <section className="stats-row">
        <div className="panel stat-panel">
          <span className="stat-value">{filteredItems.length}</span>
          <span className="stat-label">Visible articles</span>
        </div>
        <div className="panel stat-panel">
          <span className="stat-value">{openAccessCount}</span>
          <span className="stat-label">Open access</span>
        </div>
        <div className="panel stat-panel">
          <span className="stat-value">{unknownAccessCount}</span>
          <span className="stat-label">Full text unknown</span>
        </div>
      </section>

      <section className="grid">
        {filteredItems.length ? (
          filteredItems.map((item) => (
            <ArticleCard
              item={item}
              key={`${item.section}-${item.rank}-${item.article?.id}`}
            />
          ))
        ) : (
          <article className="panel wide">
            <h2>No matching articles</h2>
            <p>Try clearing filters or lowering the minimum score.</p>
          </article>
        )}
      </section>
    </main>
  );
}

function FilterPanel({
  params,
  articleTypes,
}: {
  params: ArticlesSearchParams;
  articleTypes: string[];
}) {
  return (
    <form className="panel wide filter-panel" action="/articles">
      <label>
        <span>Access</span>
        <select name="access" defaultValue={params.access ?? "all"}>
          <option value="all">All access states</option>
          <option value="OPEN_ACCESS">Open access</option>
          <option value="UNKNOWN">Full text unknown</option>
          <option value="ABSTRACT_ONLY">Only abstract</option>
          <option value="INSTITUTIONAL_ACCESS_NEEDED">Institutional access</option>
        </select>
      </label>

      <label>
        <span>Article type</span>
        <select name="type" defaultValue={params.type ?? "all"}>
          <option value="all">All types</option>
          {articleTypes.map((type) => (
            <option value={type} key={type}>
              {type}
            </option>
          ))}
        </select>
      </label>

      <label>
        <span>Minimum score</span>
        <select name="minScore" defaultValue={params.minScore ?? "0"}>
          <option value="0">Any score</option>
          <option value="15">15+</option>
          <option value="16">16+</option>
          <option value="17">17+</option>
          <option value="18">18+</option>
        </select>
      </label>

      <label>
        <span>Sort</span>
        <select name="sort" defaultValue={params.sort ?? "score_desc"}>
          <option value="score_desc">Score high to low</option>
          <option value="score_asc">Score low to high</option>
          <option value="clinical_desc">Clinical impact high to low</option>
          <option value="newest">Newest publication</option>
          <option value="oldest">Oldest publication</option>
        </select>
      </label>

      <div className="filter-actions">
        <button type="submit">Apply</button>
        <a className="text-link" href="/articles">
          Clear
        </a>
      </div>
    </form>
  );
}

function applyArticleFilters(
  items: DailyBriefingItem[],
  params: ArticlesSearchParams,
): DailyBriefingItem[] {
  const minScore = Number(params.minScore ?? 0);
  const access = params.access ?? "all";
  const type = params.type ?? "all";
  const sort = params.sort ?? "score_desc";

  const filtered = items.filter((item) => {
    const article = item.article;
    if (!article) {
      return false;
    }
    if (access !== "all" && article.access_status !== access) {
      return false;
    }
    if (type !== "all" && article.article_type !== type) {
      return false;
    }
    if ((article.score?.total_score ?? 0) < minScore) {
      return false;
    }
    return true;
  });

  filtered.sort((a, b) => {
    const articleA = a.article;
    const articleB = b.article;
    if (!articleA || !articleB) {
      return 0;
    }

    switch (sort) {
      case "score_asc":
        return (articleA.score?.total_score ?? 0) - (articleB.score?.total_score ?? 0);
      case "clinical_desc":
        return (
          (articleB.score?.clinical_impact ?? 0) -
          (articleA.score?.clinical_impact ?? 0)
        );
      case "newest":
        return dateValue(articleB.publication_date) - dateValue(articleA.publication_date);
      case "oldest":
        return dateValue(articleA.publication_date) - dateValue(articleB.publication_date);
      case "score_desc":
      default:
        return (articleB.score?.total_score ?? 0) - (articleA.score?.total_score ?? 0);
    }
  });

  return filtered.map((item, index) => ({
    ...item,
    rank: index + 1,
  }));
}

function getArticleTypes(items: DailyBriefingItem[]): string[] {
  return [...new Set(items.map((item) => item.article?.article_type).filter(Boolean))]
    .sort((a, b) => String(a).localeCompare(String(b))) as string[];
}

function dateValue(value: string | null) {
  return value ? new Date(value).getTime() : 0;
}
