import { createSupabaseClient } from "@/lib/supabase";

export type DailyBriefingItem = {
  section: string;
  rank: number | null;
  item_summary: string | null;
  article: {
    id: string;
    title: string;
    title_zh: string | null;
    journal: string | null;
    publication_date: string | null;
    doi: string | null;
    pmid: string | null;
    url: string | null;
    access_status: string;
    article_type: string | null;
    score?: {
      total_score: number;
      recommendation_level: string;
    } | null;
  } | null;
};

export type DailyBriefing = {
  id: string;
  briefing_date: string;
  title: string;
  status: string;
  summary: string | null;
  trend_overview: string | null;
  clinical_basic_section: string | null;
  interesting_medicine_section: string | null;
  source_window_start: string;
  source_window_end: string;
  items: DailyBriefingItem[];
  podcast: DailyPodcast | null;
};

export type DailyPodcast = {
  id: string;
  title: string;
  status: string;
  script: string | null;
  transcript: string | null;
  audio_url: string | null;
  audio_storage_path: string | null;
  duration_seconds: number | null;
  voice_name: string | null;
  tts_provider: string | null;
  generated_at: string | null;
};

type DailyBriefingRow = {
  id: string;
  briefing_date: string;
  title: string;
  status: string;
  summary: string | null;
  trend_overview: string | null;
  clinical_basic_section: string | null;
  interesting_medicine_section: string | null;
  source_window_start: string;
  source_window_end: string;
};

type BriefingArticleRow = {
  id: string;
  title: string;
  title_zh: string | null;
  journal: string | null;
  publication_date: string | null;
  doi: string | null;
  pmid: string | null;
  url: string | null;
  access_status: string;
  article_type: string | null;
};

type DailyBriefingItemRow = {
  section: string;
  rank: number | null;
  item_summary: string | null;
  articles: BriefingArticleRow | BriefingArticleRow[] | null;
};

export async function getLatestDailyBriefing(): Promise<DailyBriefing | null> {
  const supabase = createSupabaseClient();
  const { data, error } = await supabase
    .from("daily_briefings")
    .select(
      "id, briefing_date, title, status, summary, trend_overview, clinical_basic_section, interesting_medicine_section, source_window_start, source_window_end",
    )
    .eq("status", "published")
    .order("briefing_date", { ascending: false })
    .limit(1)
    .maybeSingle<DailyBriefingRow>();

  if (error) {
    throw error;
  }
  if (!data) {
    return null;
  }

  return hydrateDailyBriefing(data);
}

export async function getDailyBriefingByDate(
  date: string,
): Promise<DailyBriefing | null> {
  const supabase = createSupabaseClient();
  const { data, error } = await supabase
    .from("daily_briefings")
    .select(
      "id, briefing_date, title, status, summary, trend_overview, clinical_basic_section, interesting_medicine_section, source_window_start, source_window_end",
    )
    .eq("status", "published")
    .eq("briefing_date", date)
    .maybeSingle<DailyBriefingRow>();

  if (error) {
    throw error;
  }
  if (!data) {
    return null;
  }

  return hydrateDailyBriefing(data);
}

async function hydrateDailyBriefing(
  briefing: DailyBriefingRow,
): Promise<DailyBriefing> {
  const supabase = createSupabaseClient();
  const { data, error } = await supabase
    .from("daily_briefing_items")
    .select(
      "section, rank, item_summary, articles(id, title, title_zh, journal, publication_date, doi, pmid, url, access_status, article_type)",
    )
    .eq("daily_briefing_id", briefing.id)
    .order("section", { ascending: true })
    .order("rank", { ascending: true });

  if (error) {
    throw error;
  }

  const rows = (data ?? []) as unknown as DailyBriefingItemRow[];
  const normalizedRows = rows.map((item) => ({
    ...item,
    article: Array.isArray(item.articles) ? item.articles[0] : item.articles,
  }));
  const scores = await getScores(
    normalizedRows.flatMap((item) => item.article?.id ?? []),
  );
  const podcast = await getDailyPodcast(briefing.id);

  return {
    ...briefing,
    items: normalizedRows.map((item) => ({
      section: item.section,
      rank: item.rank,
      item_summary: item.item_summary,
      article: item.article
        ? {
            ...item.article,
            score: scores.get(item.article.id) ?? null,
          }
        : null,
    })),
    podcast,
  };
}

async function getDailyPodcast(briefingId: string): Promise<DailyPodcast | null> {
  const supabase = createSupabaseClient();
  const { data, error } = await supabase
    .from("podcasts")
    .select(
      "id, title, status, script, transcript, audio_url, audio_storage_path, duration_seconds, voice_name, tts_provider, generated_at",
    )
    .eq("podcast_type", "daily")
    .eq("daily_briefing_id", briefingId)
    .in("status", ["script_ready", "audio_ready", "published"])
    .order("generated_at", { ascending: false })
    .limit(1)
    .maybeSingle<DailyPodcast>();

  if (error) {
    throw error;
  }

  return data ?? null;
}

async function getScores(articleIds: string[]) {
  const supabase = createSupabaseClient();
  const uniqueIds = [...new Set(articleIds)];
  if (!uniqueIds.length) {
    return new Map<string, { total_score: number; recommendation_level: string }>();
  }

  const { data, error } = await supabase
    .from("article_scores")
    .select("article_id, total_score, recommendation_level")
    .in("article_id", uniqueIds);

  if (error) {
    throw error;
  }

  return new Map(
    (data ?? []).map((score) => [
      score.article_id,
      {
        total_score: score.total_score,
        recommendation_level: score.recommendation_level,
      },
    ]),
  );
}
