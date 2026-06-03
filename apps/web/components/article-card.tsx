import type { DailyBriefingItem } from "@/lib/daily-briefings";
import Link from "next/link";

export function ArticleCard({ item }: { item: DailyBriefingItem }) {
  const article = item.article;
  if (!article) {
    return null;
  }

  return (
    <article className="panel article-card">
      <div className="card-kicker">
        <span className="badge">{article.article_type ?? "Article"}</span>
        <span className="badge">{article.access_status}</span>
        {article.score ? (
          <span className="badge">Score {article.score.total_score}</span>
        ) : null}
      </div>
      <h2>
        <Link className="title-link" href={`/articles/${article.id}`}>
          {article.title_zh ?? article.title}
        </Link>
      </h2>
      <p className="original-title">{article.title}</p>
      <p>{item.item_summary}</p>
      <div className="metadata">
        <span>{article.journal ?? "Unknown journal"}</span>
        {article.pmid ? <span>PMID {article.pmid}</span> : null}
        {article.doi ? <span>DOI {article.doi}</span> : null}
      </div>
      <div className="link-row">
        {article.url ? (
          <a className="text-link" href={article.url} target="_blank">
            Source
          </a>
        ) : null}
        <Link className="text-link" href={`/articles/${article.id}`}>
          閱讀分析
        </Link>
      </div>
    </article>
  );
}
