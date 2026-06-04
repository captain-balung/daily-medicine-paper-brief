import { createClient, type SupabaseClient } from "@supabase/supabase-js";

export type PipelineJob = {
  id: string;
  job_type: string;
  status: string;
  target_date: string | null;
  started_at: string | null;
  finished_at: string | null;
  total_candidates: number;
  total_articles_saved: number;
  total_analyzed: number;
  total_failed: number;
  error_message: string | null;
  created_at: string;
  events: PipelineJobEvent[];
};

export type PipelineJobEvent = {
  event_type: string;
  step_name: string;
  message: string | null;
  created_at: string;
};

export type TodayPublicationStatus = {
  briefingDate: string | null;
  briefingStatus: string | null;
  hasPodcastScript: boolean;
  hasPodcastAudio: boolean;
  hasPodcastVideo: boolean;
  audioUrl: string | null;
  videoUrl: string | null;
};

export type SystemStatus = {
  configured: boolean;
  message: string | null;
  jobs: PipelineJob[];
  today: TodayPublicationStatus | null;
};

type PipelineJobRow = Omit<PipelineJob, "events">;

type DailyBriefingRow = {
  id: string;
  briefing_date: string;
  status: string;
};

type PodcastRow = {
  script: string | null;
  audio_url: string | null;
  video_url: string | null;
};

export async function getSystemStatus(): Promise<SystemStatus> {
  const supabaseUrl =
    process.env.SUPABASE_URL ?? process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey =
    process.env.SUPABASE_SECRET_KEY ??
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY;

  if (!supabaseUrl || !supabaseKey) {
    return {
      configured: false,
      message:
        "Supabase URL and key are required for the status page.",
      jobs: [],
      today: null,
    };
  }

  const supabase = createClient(supabaseUrl, supabaseKey, {
    auth: { persistSession: false },
  });

  const { data: jobRows, error: jobError } = await supabase
    .from("pipeline_jobs")
    .select(
      "id, job_type, status, target_date, started_at, finished_at, total_candidates, total_articles_saved, total_analyzed, total_failed, error_message, created_at",
    )
    .order("created_at", { ascending: false })
    .limit(5);

  if (jobError) {
    throw jobError;
  }

  const jobs = await Promise.all(
    ((jobRows ?? []) as PipelineJobRow[]).map(async (job) => {
      const { data: events, error: eventsError } = await supabase
        .from("pipeline_job_events")
        .select("event_type, step_name, message, created_at")
        .eq("pipeline_job_id", job.id)
        .order("created_at", { ascending: true });

      if (eventsError) {
        throw eventsError;
      }

      return {
        ...job,
        events: (events ?? []) as PipelineJobEvent[],
      };
    }),
  );

  const today = await getTodayPublicationStatus(supabase);

  return {
    configured: true,
    message: null,
    jobs,
    today,
  };
}

async function getTodayPublicationStatus(
  supabase: SupabaseClient,
): Promise<TodayPublicationStatus | null> {
  const { data: briefing, error: briefingError } = await supabase
    .from("daily_briefings")
    .select("id, briefing_date, status")
    .order("briefing_date", { ascending: false })
    .limit(1)
    .maybeSingle<DailyBriefingRow>();

  if (briefingError) {
    throw briefingError;
  }
  if (!briefing) {
    return null;
  }

  const { data: podcast, error: podcastError } = await supabase
    .from("podcasts")
    .select("script, audio_url, video_url")
    .eq("daily_briefing_id", briefing.id)
    .order("generated_at", { ascending: false })
    .limit(1)
    .maybeSingle<PodcastRow>();

  if (podcastError) {
    throw podcastError;
  }

  return {
    briefingDate: briefing.briefing_date,
    briefingStatus: briefing.status,
    hasPodcastScript: Boolean(podcast?.script),
    hasPodcastAudio: Boolean(podcast?.audio_url),
    hasPodcastVideo: Boolean(podcast?.video_url),
    audioUrl: podcast?.audio_url ?? null,
    videoUrl: podcast?.video_url ?? null,
  };
}
