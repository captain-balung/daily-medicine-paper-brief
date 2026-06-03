import type { DailyBriefingItem } from "@/lib/daily-briefings";
import {
  accessStatusHelp,
  accessStatusLabel,
  recommendationLabel,
} from "@/lib/labels";
import Link from "next/link";

export function ArticleCard({ item }: { item: DailyBriefingItem }) {
  const article = item.article;
  if (!article) {
    return null;
  }

  return (
    <article className="panel article-card">
      <div className="card-kicker">
        <span className="badge">{article.article_type ?? "Article"}</span>
        <span className="badge">{accessStatusLabel(article.access_status)}</span>
        {article.score ? (
          <span className="badge">Score {article.score.total_score}</span>
        ) : null}
      </div>
      <h2>
        <Link className="title-link" href={`/articles/${article.id}`}>
          {article.title_zh ?? article.title}
        </Link>
      </h2>
      <p className="original-title">{article.title}</p>
      {item.item_summary ? <p>{item.item_summary}</p> : null}
      {article.score ? (
        <RankingRationale item={item} />
      ) : (
        <p className="rationale-note">{accessStatusHelp(article.access_status)}</p>
      )}
      <div className="metadata">
        <span>{article.journal ?? "Unknown journal"}</span>
        {article.pmid ? <span>PMID {article.pmid}</span> : null}
        {article.doi ? <span>DOI {article.doi}</span> : null}
      </div>
      <div className="link-row">
        {article.url ? (
          <a className="text-link" href={article.url} target="_blank">
            Source
          </a>
        ) : null}
        <Link className="text-link" href={`/articles/${article.id}`}>
          Read analysis
        </Link>
      </div>
    </article>
  );
}

function RankingRationale({ item }: { item: DailyBriefingItem }) {
  const article = item.article;
  const score = article?.score;
  if (!article || !score) {
    return null;
  }

  const strongest = strongestScoreLabel(score);

  return (
    <section className="ranking-rationale" aria-label="Ranking rationale">
      <div className="rationale-title">Why this is ranked</div>
      <ul>
        <li>
          Rank {item.rank ?? "-"} with {score.total_score} points and{" "}
          {recommendationLabel(score.recommendation_level)} recommendation.
        </li>
        <li>Strongest signal: {strongest}.</li>
        <li>{accessStatusHelp(article.access_status)}</li>
      </ul>
      {score.scoring_rationale ? (
        <p className="rationale-note">{score.scoring_rationale}</p>
      ) : null}
    </section>
  );
}

function strongestScoreLabel(score: NonNullable<DailyBriefingItem["article"]>["score"]) {
  if (!score) {
    return "not available";
  }

  const rows = [
    ["clinical impact", score.clinical_impact],
    ["evidence strength", score.evidence_strength],
    ["novelty", score.novelty],
    ["specialty relevance", score.specialty_relevance],
    ["teaching/research value", score.teaching_research_value],
  ] as const;
  const [label, value] = rows.reduce((best, row) =>
    row[1] > best[1] ? row : best,
  );

  return `${label} (${value})`;
}
