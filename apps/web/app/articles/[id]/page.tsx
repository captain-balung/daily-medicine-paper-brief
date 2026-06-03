import { notFound } from "next/navigation";
import { getArticleDetail, type ArticleDetail } from "@/lib/articles";
import {
  accessStatusHelp,
  accessStatusLabel,
  recommendationLabel,
} from "@/lib/labels";

export const dynamic = "force-dynamic";

export default async function ArticlePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const article = await getArticleDetail(id);
  if (!article) {
    notFound();
  }

  return (
    <main className="page article-detail">
      <div className="detail-header">
        <div className="card-kicker">
          <span className="badge">{article.article_type ?? "Article"}</span>
          <span className="badge">{accessStatusLabel(article.access_status)}</span>
          {article.score ? (
            <span className="badge">Score {article.score.total_score}</span>
          ) : null}
        </div>
        <h1 className="page-title">{article.title_zh ?? article.title}</h1>
        <p className="original-title">{article.title}</p>
        <div className="metadata">
          <span>{article.journal ?? "Unknown journal"}</span>
          {article.publication_date ? <span>{article.publication_date}</span> : null}
          {article.publisher ? <span>{article.publisher}</span> : null}
          {article.pmid ? <span>PMID {article.pmid}</span> : null}
          {article.doi ? <span>DOI {article.doi}</span> : null}
        </div>
      </div>

      <section className="journal-club-layout">
        <article className="panel journal-main">
          <h2>Journal club snapshot</h2>
          {article.summary ? (
            <>
              <SectionBlock title="Bottom line">
                <p>{article.summary.one_sentence_summary}</p>
              </SectionBlock>
              <SectionBlock title="Why it matters">
                <p>{article.summary.clinical_implications ?? article.score?.scoring_rationale}</p>
              </SectionBlock>
              <SectionBlock title="Study design">
                <p>{article.summary.methods ?? article.summary.background}</p>
              </SectionBlock>
              <SectionBlock title="Key findings">
                <p>{article.summary.main_findings}</p>
              </SectionBlock>
              <SectionBlock title="Limitations">
                <p>{article.summary.limitations}</p>
              </SectionBlock>
            </>
          ) : (
            <p>This article has not been analyzed yet.</p>
          )}
        </article>

        <aside className="journal-sidebar">
          <ScorePanel article={article} />
          <ArticleMetaPanel article={article} />
        </aside>
      </section>

      <section className="grid journal-secondary">
        {article.summary ? (
          <>
            <DetailPanel title="Clinical relevance">
              <p>{article.summary.clinical_implications}</p>
            </DetailPanel>
            <DetailPanel title="Taiwan relevance">
              <p>{article.summary.taiwan_relevance ?? "No Taiwan-specific note available."}</p>
            </DetailPanel>
            <DetailPanel title="Clinical-basic translation">
              <p>
                {article.summary.clinical_basic_translation ??
                  article.summary.basic_mechanism ??
                  "No clinical-basic translation available."}
              </p>
            </DetailPanel>
            <DetailPanel title="Teaching / research use">
              <p>{article.summary.teaching_use}</p>
              <p>{article.summary.research_use}</p>
            </DetailPanel>
          </>
        ) : null}

        {article.abstract ? (
          <DetailPanel title="Abstract" wide>
            <p>{article.abstract}</p>
          </DetailPanel>
        ) : null}
      </section>
    </main>
  );
}

function SectionBlock({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="journal-section">
      <h3>{title}</h3>
      {children}
    </section>
  );
}

function DetailPanel({
  title,
  wide = false,
  children,
}: {
  title: string;
  wide?: boolean;
  children: React.ReactNode;
}) {
  return (
    <article className={`panel ${wide ? "wide" : ""}`}>
      <h2>{title}</h2>
      {children}
    </article>
  );
}

function ScorePanel({ article }: { article: ArticleDetail }) {
  if (!article.score) {
    return (
      <article className="panel">
        <h2>Score</h2>
        <p>No AI score is available yet.</p>
      </article>
    );
  }

  const rows = [
    ["Clinical impact", article.score.clinical_impact],
    ["Evidence strength", article.score.evidence_strength],
    ["Novelty", article.score.novelty],
    ["Specialty relevance", article.score.specialty_relevance],
    ["Teaching/research", article.score.teaching_research_value],
  ];

  return (
    <article className="panel score-panel">
      <h2>Ranking rationale</h2>
      <div className="score-total">
        <strong>{article.score.total_score}</strong>
        <span>{recommendationLabel(article.score.recommendation_level)}</span>
      </div>
      <ul className="status-list">
        {rows.map(([label, value]) => (
          <li className="status-row" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </li>
        ))}
      </ul>
      <p className="rationale-note">{article.score.scoring_rationale}</p>
    </article>
  );
}

function ArticleMetaPanel({ article }: { article: ArticleDetail }) {
  return (
    <article className="panel">
      <h2>Source and access</h2>
      <ul className="status-list">
        <li className="status-row">
          <span>Access</span>
          <strong>{accessStatusLabel(article.access_status)}</strong>
        </li>
        <li className="status-row">
          <span>Open access flag</span>
          <strong>{article.is_open_access ? "Yes" : "No"}</strong>
        </li>
        <li className="status-row">
          <span>PMID</span>
          <strong>{article.pmid ?? "-"}</strong>
        </li>
        <li className="status-row">
          <span>DOI</span>
          <strong>{article.doi ?? "-"}</strong>
        </li>
      </ul>
      <p className="rationale-note">{accessStatusHelp(article.access_status)}</p>
      {article.summary?.access_warning ? (
        <p className="rationale-note">{article.summary.access_warning}</p>
      ) : null}
      {article.url ? (
        <a className="text-link" href={article.url} target="_blank">
          Open source
        </a>
      ) : null}
      {article.topics.length ? (
        <div className="topic-list">
          {article.topics.map((topic) => (
            <span className="badge" key={topic}>
              {topic}
            </span>
          ))}
        </div>
      ) : (
        <span className="badge badge-warning">Unclassified</span>
      )}
    </article>
  );
}
