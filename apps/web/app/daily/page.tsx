import Link from "next/link";
import { ContentNotice } from "@/components/content-notice";
import { getDailyBriefingList } from "@/lib/daily-briefings";

export const dynamic = "force-dynamic";

export default async function DailyIndexPage() {
  const briefings = await getDailyBriefingList(14);

  return (
    <main className="page">
      <h1 className="page-title">Daily briefings</h1>
      <p className="lede">
        Browse the latest published daily medicine briefings. New Render Cron
        output should appear here after each successful morning run.
      </p>

      <section className="grid">
        <ContentNotice />

        {briefings.length ? (
          briefings.map((briefing) => (
            <article className="panel daily-list-card" key={briefing.id}>
              <div className="card-kicker">
                <span className="badge">{briefing.status}</span>
                <span className="badge">{briefing.briefing_date}</span>
              </div>
              <h2>
                <Link
                  className="title-link"
                  href={`/daily/${briefing.briefing_date.slice(0, 10)}`}
                >
                  {briefing.title}
                </Link>
              </h2>
              <p>{briefing.summary?.replace("Today: ", "今日重點：")}</p>
              <div className="metadata">
                <span>
                  {new Date(briefing.source_window_start).toLocaleString("zh-TW")} to{" "}
                  {new Date(briefing.source_window_end).toLocaleString("zh-TW")}
                </span>
              </div>
              <Link
                className="text-link"
                href={`/daily/${briefing.briefing_date.slice(0, 10)}`}
              >
                Open briefing
              </Link>
            </article>
          ))
        ) : (
          <article className="panel wide">
            <h2>No daily briefings yet</h2>
            <p>Run the daily pipeline to publish the first briefing.</p>
          </article>
        )}
      </section>
    </main>
  );
}
