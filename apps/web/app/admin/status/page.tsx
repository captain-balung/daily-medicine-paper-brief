import { getSystemStatus } from "@/lib/system-status";

export const dynamic = "force-dynamic";

export default async function SystemStatusPage() {
  const status = await getSystemStatus();
  const latestJob = status.jobs[0];

  return (
    <main className="page">
      <h1 className="page-title">System status</h1>
      <p className="lede">
        Check whether the daily pipeline collected papers, analyzed articles,
        published the briefing, and generated podcast audio and video.
      </p>

      {!status.configured ? (
        <section className="panel wide">
          <h2>Status page needs server configuration</h2>
          <p>{status.message}</p>
        </section>
      ) : (
        <>
          <section className="stats-row status-stats">
            <StatusStat
              label="Latest job"
              value={latestJob?.status ?? "No jobs"}
              tone={latestJob?.status === "succeeded" ? "good" : "warning"}
            />
            <StatusStat
              label="Candidates"
              value={latestJob?.total_candidates ?? 0}
            />
            <StatusStat
              label="Saved articles"
              value={latestJob?.total_articles_saved ?? 0}
            />
            <StatusStat
              label="AI analyzed"
              value={latestJob ? getAnalyzedCount(latestJob) : 0}
            />
          </section>

          {status.today ? (
            <section className="panel wide">
              <h2>Latest published content</h2>
              <ul className="status-list">
                <StatusRow label="Briefing date" value={status.today.briefingDate} />
                <StatusRow label="Briefing status" value={status.today.briefingStatus} />
                <StatusRow
                  label="Podcast script"
                  value={status.today.hasPodcastScript ? "Ready" : "Missing"}
                />
                <StatusRow
                  label="Podcast audio"
                  value={status.today.hasPodcastAudio ? "Ready" : "Missing"}
                />
                <StatusRow
                  label="Podcast video"
                  value={status.today.hasPodcastVideo ? "Ready" : "Missing"}
                />
              </ul>
              {status.today.videoUrl ? (
                <p>
                  <a className="text-link" href={status.today.videoUrl} target="_blank">
                    Open latest video
                  </a>
                </p>
              ) : null}
              {status.today.audioUrl ? (
                <p>
                  <a className="text-link" href={status.today.audioUrl} target="_blank">
                    Open latest audio
                  </a>
                </p>
              ) : null}
            </section>
          ) : null}

          <section className="grid">
            {status.jobs.map((job) => (
              <article className="panel job-panel" key={job.id}>
                <div className="card-kicker">
                  <span className="badge">{job.job_type}</span>
                  <span
                    className={`badge ${
                      job.status === "succeeded" ? "" : "badge-warning"
                    }`}
                  >
                    {job.status}
                  </span>
                </div>
                <h2>{job.target_date ?? "No target date"}</h2>
                <ul className="status-list">
                  <StatusRow label="Started" value={formatDateTime(job.started_at)} />
                  <StatusRow label="Finished" value={formatDateTime(job.finished_at)} />
                  <StatusRow label="Collected" value={job.total_candidates} />
                  <StatusRow label="Saved" value={job.total_articles_saved} />
                  <StatusRow label="Analyzed" value={getAnalyzedCount(job)} />
                  <StatusRow label="Failed" value={job.total_failed} />
                </ul>
                {job.error_message ? (
                  <p className="rationale-note">{job.error_message}</p>
                ) : null}
                <div className="event-list">
                  {job.events.map((event) => (
                    <div className="event-row" key={`${job.id}-${event.created_at}-${event.step_name}`}>
                      <strong>{event.step_name}</strong>
                      <span>{event.message ?? event.event_type}</span>
                    </div>
                  ))}
                </div>
              </article>
            ))}
          </section>
        </>
      )}
    </main>
  );
}

function StatusStat({
  label,
  value,
  tone,
}: {
  label: string;
  value: string | number;
  tone?: "good" | "warning";
}) {
  return (
    <div className="panel stat-panel">
      <span className={`stat-value ${tone === "warning" ? "stat-warning" : ""}`}>
        {value}
      </span>
      <span className="stat-label">{label}</span>
    </div>
  );
}

function StatusRow({
  label,
  value,
}: {
  label: string;
  value: string | number | null;
}) {
  return (
    <li className="status-row">
      <span>{label}</span>
      <strong>{value ?? "-"}</strong>
    </li>
  );
}

function formatDateTime(value: string | null) {
  if (!value) {
    return "-";
  }

  return new Date(value).toLocaleString("zh-TW");
}

function getAnalyzedCount(job: Awaited<ReturnType<typeof getSystemStatus>>["jobs"][number]) {
  if (job.total_analyzed > 0) {
    return job.total_analyzed;
  }

  const analysisEvent = job.events.find((event) => event.step_name === "ai_analysis");
  const match = analysisEvent?.message?.match(/analyzed (\d+)/i);
  return match ? Number(match[1]) : 0;
}
