import Link from "next/link";
import { getLatestDailyBriefing } from "@/lib/daily-briefings";

export const dynamic = "force-dynamic";

export default async function DailyIndexPage() {
  const briefing = await getLatestDailyBriefing();

  return (
    <main className="page">
      <h1 className="page-title">每日簡報</h1>
      <p className="lede">已發布的每日醫學文獻簡報。</p>

      {briefing ? (
        <section className="grid">
          <article className="panel wide">
            <h2>{briefing.title}</h2>
            <p>{briefing.summary?.replace("Today: ", "今日重點：")}</p>
            <div className="metadata">
              <span>{briefing.status}</span>
              <span>
                {new Date(briefing.source_window_start).toLocaleString("zh-TW")} to{" "}
                {new Date(briefing.source_window_end).toLocaleString("zh-TW")}
              </span>
            </div>
            <Link
              className="text-link"
              href={`/daily/${briefing.briefing_date.slice(0, 10)}`}
            >
              開啟完整簡報
            </Link>
          </article>
        </section>
      ) : (
        <section className="grid">
          <article className="panel wide">
            <h2>尚無簡報</h2>
            <p>目前沒有已發布的每日簡報。</p>
          </article>
        </section>
      )}
    </main>
  );
}
