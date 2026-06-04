import type { DailyPodcast } from "@/lib/daily-briefings";

export function PodcastPanel({ podcast }: { podcast: DailyPodcast }) {
  return (
    <article className="panel wide podcast-script">
      <div className="card-kicker">
        <span className="badge">
          {podcast.video_url
            ? "Podcast 影片"
            : podcast.audio_url
              ? "Podcast 音檔"
              : "Podcast 稿"}
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
      {podcast.video_url ? (
        <div className="video-block">
          <video controls preload="metadata" src={podcast.video_url}>
            Your browser does not support the video element.
          </video>
          <p>
            本影片由 AI 生成每日醫學簡報、語音與視覺卡片；請以原始文獻與臨床判斷為準。
          </p>
        </div>
      ) : null}
      {podcast.audio_url ? (
        <div className="audio-block">
          <audio controls preload="metadata" src={podcast.audio_url}>
            Your browser does not support the audio element.
          </audio>
          <p>
            本音檔由 AI 生成，僅供醫學文獻導讀與討論使用；請自行查核原始來源。
          </p>
        </div>
      ) : null}
      {podcast.script ? <pre>{podcast.script}</pre> : null}
    </article>
  );
}
