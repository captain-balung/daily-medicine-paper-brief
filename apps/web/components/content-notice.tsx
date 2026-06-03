export function ContentNotice({ compact = false }: { compact?: boolean }) {
  return (
    <article className={`panel content-notice ${compact ? "content-notice-compact" : "wide"}`}>
      <h2>Content and source notice</h2>
      <p>
        This site provides AI-generated research briefings, ranking rationale,
        and commentary based on citation metadata and article summaries. It is
        not a reproduction of publisher full text, and it is not medical advice.
      </p>
      {!compact ? (
        <p>
          Article titles, journal names, PMID/DOI identifiers, and source links
          are shown for attribution and verification. Please use the original
          source link for the publisher abstract, full text, and license terms.
        </p>
      ) : null}
    </article>
  );
}
