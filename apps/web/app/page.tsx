import { ContentNotice } from "@/components/content-notice";
import { FeaturedAnalysis } from "@/components/featured-analysis";
import { PodcastPanel } from "@/components/podcast-panel";
import { RankingSummary } from "@/components/ranking-summary";
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
  const deepDive = briefing.items.find((item) => item.section === "deep_dive");

  return (
    <main className="page">
      <h1 className="page-title">{briefing.title}</h1>
      <p className="lede">{briefing.summary?.replace("Today: ", "今日重點：")}</p>

      <section className="grid">
        <article className="panel wide">
          <h2>Daily overview</h2>
          <p>
            This briefing is generated from PubMed Core source data, Crossref
            metadata, Unpaywall access labels, Anthropic analysis, and optional
            OpenAI TTS podcast audio.
          </p>
          <span className="badge">Published</span>
        </article>

        <ContentNotice />

        <RankingSummary items={mustRead} />

        <FeaturedAnalysis mustRead={mustRead} deepDive={deepDive} />

        {briefing.clinical_basic_section ? (
          <article className="panel wide">
            <h2>Clinical-basic translation</h2>
            <p>{briefing.clinical_basic_section}</p>
          </article>
        ) : null}

        {briefing.podcast?.script ? (
          <PodcastPanel podcast={briefing.podcast} />
        ) : null}
      </section>
    </main>
  );
}
