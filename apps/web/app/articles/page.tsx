import { ArticleCard } from "@/components/article-card";
import { getAnalyzedArticleItems } from "@/lib/articles";

export const dynamic = "force-dynamic";

export default async function ArticlesIndexPage() {
  const items = await getAnalyzedArticleItems(50);
  const openAccessCount = items.filter(
    (item) => item.article?.access_status === "OPEN_ACCESS",
  ).length;

  return (
    <main className="page">
      <h1 className="page-title">文章列表</h1>
      <p className="lede">
        依 AI importance score 排序的已分析文章。目前顯示最新可讀的分析結果。
      </p>

      <section className="stats-row">
        <div className="panel stat-panel">
          <span className="stat-value">{items.length}</span>
          <span className="stat-label">已分析文章</span>
        </div>
        <div className="panel stat-panel">
          <span className="stat-value">{openAccessCount}</span>
          <span className="stat-label">Open access</span>
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
            <h2>尚無已分析文章</h2>
            <p>請先執行 AI analysis pipeline。</p>
          </article>
        )}
      </section>
    </main>
  );
}
