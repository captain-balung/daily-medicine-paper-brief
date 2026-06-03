import { createSupabaseClient } from "@/lib/supabase";
import type { DailyBriefingItem } from "@/lib/daily-briefings";

export type ArticleDetail = {
  id: string;
  title: string;
  title_zh: string | null;
  abstract: string | null;
  journal: string | null;
  publisher: string | null;
  publication_date: string | null;
  doi: string | null;
  pmid: string | null;
  url: string | null;
  access_status: string;
  article_type: string | null;
  is_open_access: boolean;
  score: {
    clinical_impact: number;
    evidence_strength: number;
    novelty: number;
    specialty_relevance: number;
    teaching_research_value: number;
    total_score: number;
    recommendation_level: string;
    scoring_rationale: string | null;
  } | null;
  summary: {
    one_sentence_summary: string;
    background: string | null;
    methods: string | null;
    main_findings: string | null;
    author_conclusion: string | null;
    clinical_implications: string | null;
    basic_mechanism: string | null;
    clinical_basic_translation: string | null;
    limitations: string;
    taiwan_relevance: string | null;
    teaching_use: string | null;
    research_use: string | null;
    access_warning: string | null;
  } | null;
  topics: string[];
};

type ArticleRow = Omit<ArticleDetail, "score" | "summary" | "topics">;

export async function getAnalyzedArticleItems(
  limit: number = 50,
): Promise<DailyBriefingItem[]> {
  const supabase = createSupabaseClient();
  const { data, error } = await supabase
    .from("article_scores")
    .select("article_id, total_score, recommendation_level")
    .order("total_score", { ascending: false })
    .limit(limit);

  if (error) {
    throw error;
  }

  const items: DailyBriefingItem[] = [];
  for (const score of data ?? []) {
    const article = await getArticleCardRow(score.article_id);
    const summary = await getArticleSummary(score.article_id);
    if (!article) {
      continue;
    }

    items.push({
      section: "analyzed",
      rank: items.length + 1,
      item_summary: summary?.one_sentence_summary ?? null,
      article: {
        ...article,
        score: {
          total_score: score.total_score,
          recommendation_level: score.recommendation_level,
        },
      },
    });
  }

  return items;
}

export async function getArticleDetail(
  id: string,
): Promise<ArticleDetail | null> {
  const supabase = createSupabaseClient();
  const { data: article, error } = await supabase
    .from("articles")
    .select(
      "id, title, title_zh, abstract, journal, publisher, publication_date, doi, pmid, url, access_status, article_type, is_open_access",
    )
    .eq("id", id)
    .maybeSingle<ArticleRow>();

  if (error) {
    throw error;
  }
  if (!article) {
    return null;
  }

  const [score, summary, topics] = await Promise.all([
    getArticleScore(id),
    getArticleSummary(id),
    getArticleTopics(id),
  ]);

  return {
    ...article,
    score,
    summary,
    topics,
  };
}

async function getArticleScore(id: string): Promise<ArticleDetail["score"]> {
  const supabase = createSupabaseClient();
  const { data, error } = await supabase
    .from("article_scores")
    .select(
      "clinical_impact, evidence_strength, novelty, specialty_relevance, teaching_research_value, total_score, recommendation_level, scoring_rationale",
    )
    .eq("article_id", id)
    .maybeSingle<ArticleDetail["score"]>();

  if (error) {
    throw error;
  }

  return data ?? null;
}

async function getArticleCardRow(id: string) {
  const supabase = createSupabaseClient();
  const { data, error } = await supabase
    .from("articles")
    .select(
      "id, title, title_zh, journal, publication_date, doi, pmid, url, access_status, article_type",
    )
    .eq("id", id)
    .maybeSingle();

  if (error) {
    throw error;
  }

  return data;
}

async function getArticleSummary(id: string): Promise<ArticleDetail["summary"]> {
  const supabase = createSupabaseClient();
  const { data, error } = await supabase
    .from("article_summaries")
    .select(
      "one_sentence_summary, background, methods, main_findings, author_conclusion, clinical_implications, basic_mechanism, clinical_basic_translation, limitations, taiwan_relevance, teaching_use, research_use, access_warning",
    )
    .eq("article_id", id)
    .eq("summary_version", 1)
    .maybeSingle<ArticleDetail["summary"]>();

  if (error) {
    throw error;
  }

  return data ?? null;
}

async function getArticleTopics(id: string): Promise<string[]> {
  const supabase = createSupabaseClient();
  const { data, error } = await supabase
    .from("article_topics")
    .select("topics(name_en, name_zh)")
    .eq("article_id", id);

  if (error) {
    throw error;
  }

  return (data ?? [])
    .map((row) => {
      const topic = Array.isArray(row.topics) ? row.topics[0] : row.topics;
      return topic?.name_zh ?? topic?.name_en;
    })
    .filter(Boolean) as string[];
}
