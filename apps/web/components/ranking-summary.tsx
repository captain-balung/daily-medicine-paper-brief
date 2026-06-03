import type { DailyBriefingItem } from "@/lib/daily-briefings";
import { accessStatusLabel, recommendationLabel } from "@/lib/labels";
import Link from "next/link";

export function RankingSummary({ items }: { items: DailyBriefingItem[] }) {
  const rankedItems = items
    .filter((item) => item.article)
    .sort((a, b) => (a.rank ?? 999) - (b.rank ?? 999));

  if (!rankedItems.length) {
    return null;
  }

  return (
    <article className="panel wide ranking-summary">
      <h2>Today&apos;s Top Ranking</h2>
      <div className="ranking-table-wrap">
        <table className="ranking-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Article</th>
              <th>Score</th>
              <th>Why ranked</th>
              <th>Access</th>
            </tr>
          </thead>
          <tbody>
            {rankedItems.map((item, index) => {
              const article = item.article;
              if (!article) {
                return null;
              }

              return (
                <tr key={`${item.section}-${item.rank}-${article.id}`}>
                  <td>{index + 1}</td>
                  <td>
                    <Link className="title-link" href={`/articles/${article.id}`}>
                      {article.title_zh ?? article.title}
                    </Link>
                  </td>
                  <td>
                    {article.score ? (
                      <>
                        <strong>{article.score.total_score}</strong>
                        <span>{recommendationLabel(article.score.recommendation_level)}</span>
                      </>
                    ) : (
                      "-"
                    )}
                  </td>
                  <td>{article.score?.scoring_rationale ?? item.item_summary ?? "-"}</td>
                  <td>{accessStatusLabel(article.access_status)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </article>
  );
}
