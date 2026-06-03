import type { DailyPodcast } from "@/lib/daily-briefings";

export function PodcastPanel({ podcast }: { podcast: DailyPodcast }) {
  return (
    <article className="panel wide podcast-script">
      <div className="card-kicker">
        <span className="badge">
          {podcast.audio_url ? "Podcast 音檔" : "Podcast 稿"}
        </span>
        {podcast.duration_seconds ? (
          <span className="badge">
            約 {Math.max(1, Math.round(podcast.duration_seconds / 60))} 分鐘
          </span>
        ) : null}
        {podcast.voice_name ? (
          <span className="badge">Voice {podcast.voice_name}</span>
        ) : null}
      </div>
      <h2>{podcast.title}</h2>
      {podcast.audio_url ? (
        <div className="audio-block">
          <audio controls preload="metadata" src={podcast.audio_url}>
            Your browser does not support the audio element.
          </audio>
          <p>此音檔由 AI 文字轉語音產生，內容仍以原始文獻與摘要來源為準。</p>
        </div>
      ) : null}
      {podcast.script ? <pre>{podcast.script}</pre> : null}
    </article>
  );
}
