import { ArticleCard } from "@/components/article-card";
import { getLatestDailyBriefing } from "@/lib/daily-briefings";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const briefing = await getLatestDailyBriefing();

  if (!briefing) {
    return (
      <main className="page">
        <h1 className="page-title">Today&apos;s Medicine Brief</h1>
        <p className="lede">No published briefing is available yet.</p>
      </main>
    );
  }

  const mustRead = briefing.items.filter((item) => item.section === "must_read");

  return (
    <main className="page">
      <h1 className="page-title">{briefing.title}</h1>
      <p className="lede">{briefing.summary?.replace("Today: ", "今日重點：")}</p>

      <section className="grid">
        <article className="panel wide">
          <h2>今日總覽</h2>
          <p>
            本日簡報由 PubMed Core source、Crossref metadata、Unpaywall access
            label 與 Anthropic AI 分析自動產生。
          </p>
          <span className="badge">Published</span>
        </article>

        {mustRead.map((item) => (
          <ArticleCard
            item={item}
            key={`${item.section}-${item.rank}-${item.article?.id}`}
          />
        ))}

        {briefing.clinical_basic_section ? (
          <article className="panel wide">
            <h2>臨床與基礎轉譯</h2>
            <p>{briefing.clinical_basic_section}</p>
          </article>
        ) : null}
      </section>
    </main>
  );
}
