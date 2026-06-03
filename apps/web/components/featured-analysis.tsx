import { ArticleCard } from "@/components/article-card";
import type { DailyBriefingItem } from "@/lib/daily-briefings";

export function FeaturedAnalysis({
  mustRead,
  deepDive,
}: {
  mustRead: DailyBriefingItem[];
  deepDive?: DailyBriefingItem | null;
}) {
  const featured = mustRead.slice(0, 3);
  const featuredIds = new Set(
    featured.map((item) => item.article?.id).filter(Boolean),
  );
  const deepDiveIsExtra =
    deepDive?.article?.id && !featuredIds.has(deepDive.article.id);

  if (!featured.length && !deepDiveIsExtra) {
    return null;
  }

  return (
    <>
      <article className="panel wide section-intro">
        <h2>Featured analysis</h2>
        <p>
          The table above gives the full ranking overview. These cards expand
          the highest-priority papers for closer reading.
        </p>
      </article>

      {featured.map((item) => (
        <ArticleCard
          item={item}
          key={`${item.section}-${item.rank}-${item.article?.id}`}
        />
      ))}

      {deepDiveIsExtra ? (
        <article className="wide">
          <ArticleCard item={deepDive} />
        </article>
      ) : null}
    </>
  );
}
