import { getSetupChecks } from "@/lib/setup-checks";

export default function SetupPage() {
  const checks = getSetupChecks();
  const ready = checks.every((check) => check.status === "pass");

  return (
    <main className="page">
      <h1 className="page-title">初始設定</h1>
      <p className="lede">
        所有必要檢查通過前，自動化流程維持停用。
      </p>

      <section className="grid">
        <article className="panel">
          <h2>System status</h2>
          <span className={ready ? "badge" : "badge badge-warning"}>
            {ready ? "READY" : "SETUP_REQUIRED"}
          </span>
        </article>

        <article className="panel">
          <h2>Publication mode</h2>
          <p>Auto-publish after setup and safety checks pass.</p>
        </article>

        <article className="panel">
          <h2>MVP sources</h2>
          <p>PubMed, Crossref, Unpaywall.</p>
        </article>

        <article className="panel wide">
          <h2>Readiness checks</h2>
          <ul className="status-list">
            {checks.map((check) => (
              <li className="status-row" key={check.id}>
                <span>{check.label}</span>
                <span
                  className={
                    check.status === "pass" ? "badge" : "badge badge-warning"
                  }
                >
                  {check.status}
                </span>
              </li>
            ))}
          </ul>
        </article>
      </section>
    </main>
  );
}
