import { ArticleCard } from "@/components/article-card";
import { getAnalyzedArticleItems } from "@/lib/articles";

export const dynamic = "force-dynamic";

export default async function ArticlesIndexPage() {
  const items = await getAnalyzedArticleItems(50);
  const openAccessCount = items.filter(
    (item) => item.article?.access_status === "OPEN_ACCESS",
  ).length;
  const unknownAccessCount = items.filter(
    (item) => item.article?.access_status === "UNKNOWN",
  ).length;

  return (
    <main className="page">
      <h1 className="page-title">Analyzed articles</h1>
      <p className="lede">
        Articles are sorted by AI importance score. Each card now shows the
        ranking rationale and whether full-text access metadata is known.
      </p>

      <section className="stats-row">
        <div className="panel stat-panel">
          <span className="stat-value">{items.length}</span>
          <span className="stat-label">Analyzed articles</span>
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
        {items.length ? (
          items.map((item) => (
            <ArticleCard
              item={item}
              key={`${item.section}-${item.rank}-${item.article?.id}`}
            />
          ))
        ) : (
          <article className="panel wide">
            <h2>No analyzed articles yet</h2>
            <p>Please run the AI analysis pipeline first.</p>
          </article>
        )}
      </section>
    </main>
  );
}
