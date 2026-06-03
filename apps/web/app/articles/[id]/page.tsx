import { notFound } from "next/navigation";
import { getArticleDetail } from "@/lib/articles";

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
          <span className="badge">{article.access_status}</span>
          {article.score ? (
            <span className="badge">Score {article.score.total_score}</span>
          ) : null}
        </div>
        <h1 className="page-title">{article.title_zh ?? article.title}</h1>
        <p className="original-title">{article.title}</p>
        <div className="metadata">
          <span>{article.journal ?? "Unknown journal"}</span>
          {article.publisher ? <span>{article.publisher}</span> : null}
          {article.pmid ? <span>PMID {article.pmid}</span> : null}
          {article.doi ? <span>DOI {article.doi}</span> : null}
        </div>
      </div>

      <section className="grid">
        {article.summary ? (
          <>
            <DetailPanel title="One-sentence Summary" wide>
              <p>{article.summary.one_sentence_summary}</p>
            </DetailPanel>

            <ScorePanel article={article} />

            <DetailPanel title="Background">
              <p>{article.summary.background}</p>
            </DetailPanel>
            <DetailPanel title="Methods">
              <p>{article.summary.methods}</p>
            </DetailPanel>
            <DetailPanel title="Main Findings">
              <p>{article.summary.main_findings}</p>
            </DetailPanel>
            <DetailPanel title="Clinical Implications" wide>
              <p>{article.summary.clinical_implications}</p>
            </DetailPanel>
            <DetailPanel title="Clinical-basic Translation" wide>
              <p>{article.summary.clinical_basic_translation}</p>
            </DetailPanel>
            <DetailPanel title="Limitations">
              <p>{article.summary.limitations}</p>
            </DetailPanel>
            <DetailPanel title="Taiwan Relevance">
              <p>{article.summary.taiwan_relevance}</p>
            </DetailPanel>
            <DetailPanel title="Teaching / Research Use">
              <p>{article.summary.teaching_use}</p>
              <p>{article.summary.research_use}</p>
            </DetailPanel>
          </>
        ) : (
          <DetailPanel title="Summary" wide>
            <p>This article has not been analyzed yet.</p>
          </DetailPanel>
        )}

        <DetailPanel title="Topics">
          <div className="card-kicker">
            {article.topics.length ? (
              article.topics.map((topic) => <span className="badge" key={topic}>{topic}</span>)
            ) : (
              <span className="badge badge-warning">Unclassified</span>
            )}
          </div>
        </DetailPanel>

        <DetailPanel title="Source">
          {article.url ? (
            <a className="text-link" href={article.url} target="_blank">
              Open PubMed source
            </a>
          ) : (
            <p>No source URL available.</p>
          )}
          {article.summary?.access_warning ? (
            <p>{article.summary.access_warning}</p>
          ) : null}
        </DetailPanel>

        {article.abstract ? (
          <DetailPanel title="Abstract" wide>
            <p>{article.abstract}</p>
          </DetailPanel>
        ) : null}
      </section>
    </main>
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

function ScorePanel({ article }: { article: Awaited<ReturnType<typeof getArticleDetail>> }) {
  if (!article?.score) {
    return null;
  }

  const rows = [
    ["Clinical impact", article.score.clinical_impact],
    ["Evidence strength", article.score.evidence_strength],
    ["Novelty", article.score.novelty],
    ["Specialty relevance", article.score.specialty_relevance],
    ["Teaching/research", article.score.teaching_research_value],
  ];

  return (
    <article className="panel">
      <h2>Score</h2>
      <ul className="status-list">
        {rows.map(([label, value]) => (
          <li className="status-row" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </li>
        ))}
      </ul>
      <p>{article.score.scoring_rationale}</p>
    </article>
  );
}
