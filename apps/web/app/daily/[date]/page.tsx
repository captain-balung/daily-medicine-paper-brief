import { notFound } from "next/navigation";
import { ArticleCard } from "@/components/article-card";
import { PodcastPanel } from "@/components/podcast-panel";
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
          <h2>Source window</h2>
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
            <h2>Clinical-basic translation</h2>
            <p>{briefing.clinical_basic_section}</p>
          </article>
        ) : null}

        {briefing.podcast?.script ? (
          <PodcastPanel podcast={briefing.podcast} />
        ) : null}

        <article className="panel wide">
          <h2>Notes</h2>
          <p>
            This briefing is AI-generated from source metadata and article
            analysis. It should be used for research awareness and discussion,
            not as clinical guidance.
          </p>
        </article>
      </section>
    </main>
  );
}
