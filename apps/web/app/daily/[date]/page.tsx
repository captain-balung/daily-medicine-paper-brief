import { notFound } from "next/navigation";
import { ArticleCard } from "@/components/article-card";
import { getDailyBriefingByDate } from "@/lib/daily-briefings";

export const dynamic = "force-dynamic";

export default async function DailyBriefingPage({
  params,
}: {
  params: Promise<{ date: string }>;
}) {
  const { date } = await params;
  const briefing = await getDailyBriefingByDate(date);
  if (!briefing) {
    notFound();
  }

  const mustRead = briefing.items.filter((item) => item.section === "must_read");
  const deepDive = briefing.items.find((item) => item.section === "deep_dive");

  return (
    <main className="page">
      <h1 className="page-title">{briefing.title}</h1>
      <p className="lede">{briefing.summary?.replace("Today: ", "今日重點：")}</p>

      <section className="grid">
        <article className="panel wide">
          <h2>資料時間窗</h2>
          <p>
            {new Date(briefing.source_window_start).toLocaleString("zh-TW")} to{" "}
            {new Date(briefing.source_window_end).toLocaleString("zh-TW")}
          </p>
        </article>

        {mustRead.map((item) => (
          <ArticleCard
            item={item}
            key={`${item.section}-${item.rank}-${item.article?.id}`}
          />
        ))}

        {deepDive ? (
          <article className="wide">
            <ArticleCard item={deepDive} />
          </article>
        ) : null}

        {briefing.clinical_basic_section ? (
          <article className="panel wide">
            <h2>臨床與基礎轉譯</h2>
            <p>{briefing.clinical_basic_section}</p>
          </article>
        ) : null}

        {briefing.podcast?.script ? (
          <article className="panel wide podcast-script">
            <div className="card-kicker">
              <span className="badge">Podcast 稿</span>
              {briefing.podcast.duration_seconds ? (
                <span className="badge">
                  約 {Math.max(1, Math.round(briefing.podcast.duration_seconds / 60))} 分鐘
                </span>
              ) : null}
            </div>
            <h2>{briefing.podcast.title}</h2>
            <pre>{briefing.podcast.script}</pre>
          </article>
        ) : null}

        <article className="panel wide">
          <h2>聲明</h2>
          <p>
            本簡報為 AI 輔助整理，根據 metadata、摘要與來源連結產生，不構成臨床決策建議。
          </p>
        </article>
      </section>
    </main>
  );
}
