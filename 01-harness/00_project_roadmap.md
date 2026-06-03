# 00 Project Roadmap

## 1. Project Goal

建立一套每日自動化醫學研究情報平台，聚焦腎臟、透析、CKD、心血管、代謝、老年醫學、內科醫學、AI 醫療與數位醫學。系統每日台灣時間早上 06:00 收集前 24 小時全球醫學新知，自動完成分類、摘要、重要性評分、臨床—基礎轉譯分析，並發布為網站早報與 15–20 分鐘 Podcast。每週日早上再產生前七天的週報與週報 Podcast。

## 2. Product Vision

這不是一般醫學新聞網站，而是醫學研究情報、臨床新知整理、基礎研究轉譯、教學素材累積、研究題目發想與 Podcast 出版的整合平台。平台最終要成為腎臟科／內科醫師、研究者與教師每日使用的醫學知識中樞。

## 3. Guiding Principles

1. MVP first: 先完成可運作的最小版本，再逐步擴充。
2. Human-first pipeline: 人類設定、帳號、授權、發布規則、資料來源與安全邊界在前；機器自動化在後。
3. Legal source use: 不非法儲存或散布付費全文。
4. Medical safety: 所有醫學內容需標示來源、證據等級、限制與 preprint 狀態。
5. Clear architecture: Vercel 負責網站，Supabase 負責資料，Render 負責長時間 Python worker。
6. Codex-friendly: 所有任務拆成小型、可測試、可審查的 task。

## 4. Technical Stack

- GitHub: code and docs.
- Vercel: Next.js + TypeScript + Tailwind CSS website.
- Supabase: PostgreSQL, Auth, RLS, Storage, pgvector.
- Render: Python worker, daily cron, weekly cron, AI pipeline, Podcast generation.
- AI services: LLM for classification, scoring, summarization, translation, briefing generation; embeddings for semantic search; TTS for MP3.

## 5. Development Phases

### Phase 0 — Specification and Repository Preparation

Deliverables:
1. docs/00_project_roadmap.md
2. docs/01_product_requirements.md
3. docs/02_system_architecture.md
4. docs/03_human_first_pipeline.md
5. docs/04_data_pipeline_spec.md
6. docs/05_database_schema.md
7. docs/06_ai_content_spec.md
8. docs/07_web_ui_spec.md
9. docs/08_api_contracts.md
10. docs/09_deployment_ops.md
11. docs/10_security_compliance.md
12. docs/11_development_tasks.md

Acceptance criteria:
1. Codex can understand the goal, architecture, boundaries, and task order.
2. MVP and future phases are clearly separated.
3. Human-first pipeline is documented before implementation.

### Phase 1 — MVP Foundation

Deliverables:
1. Next.js app skeleton.
2. Supabase schema migrations.
3. Render Python worker skeleton.
4. Initial Setup Dashboard.
5. Basic daily briefing page.
6. Basic article page.
7. Basic podcast player placeholder.

Acceptance criteria:
1. Vercel deployment works.
2. Supabase connection works.
3. Render worker can run a health check.
4. Website redirects admin to setup dashboard if setup is incomplete.

### Phase 2 — Human-First Setup and Safety Gate

Deliverables:
1. System status model.
2. Secrets status checker.
3. Data source activation settings.
4. Topic weights.
5. Publication rules.
6. Medical safety rules.
7. Test pipeline trigger.

Acceptance criteria:
1. Scheduled pipeline cannot publish unless setup status is READY.
2. No secret is shown in the browser.
3. Admin can see pass/fail status for all required setup items.
4. Test pipeline must pass before enabling automation.

### Phase 3 — Daily Data Collection Pipeline

Deliverables:
1. PubMed collector.
2. Crossref collector.
3. Europe PMC collector.
4. Unpaywall OA checker.
5. RSS / TOC collector.
6. bioRxiv / medRxiv collectors.
7. DOI / PMID normalization.
8. Deduplication.
9. Pipeline job logs.

Acceptance criteria:
1. Daily Taiwan 06:00 pipeline collects prior 24 hours.
2. Duplicate DOI / PMID articles are not duplicated.
3. Articles have source, title, abstract, date, DOI/PMID when available.
4. Errors are visible to admin.

### Phase 4 — AI Classification, Scoring, and Summary

Deliverables:
1. Topic classification.
2. Study type classification.
3. Evidence level labeling.
4. Importance scoring.
5. Chinese medical summary.
6. Clinical implication.
7. Basic mechanism.
8. Clinical-basic translation.
9. Limitations and Taiwan relevance.
10. Preprint and access warnings.

Acceptance criteria:
1. Every analyzed article has topic, study type, evidence label, score, and summary.
2. Preprints are clearly labeled.
3. Paywalled articles are not treated as full-text analyzed.

### Phase 5 — Daily Web Briefing

Deliverables:
1. Daily briefing generator.
2. `/daily/YYYY-MM-DD` page.
3. Today must-read 5 articles.
4. Specialty briefs.
5. Deep dive.
6. Interesting medicine item.
7. Source list.

Acceptance criteria:
1. Daily briefing can be generated and displayed.
2. Must-read list contains no more than 5 articles.
3. Every item has source and evidence label.
4. Interesting medicine appears every day.

### Phase 6 — Daily Podcast

Deliverables:
1. Podcast script generator.
2. TTS MP3 generator.
3. Supabase Storage upload.
4. Podcast transcript.
5. Podcast player on daily briefing page.

Acceptance criteria:
1. Daily podcast target length is 15–20 minutes.
2. Chinese is primary language; key English medical terms are retained.
3. Audio is playable.
4. AI-generated audio disclosure appears.

### Phase 7 — Weekly Briefing

Deliverables:
1. Weekly cron.
2. Weekly ranking and synthesis.
3. Weekly top 10.
4. Topic summaries.
5. Clinical-basic translation themes.
6. Teaching and research materials.
7. Weekly interesting medicine highlights.
8. Weekly podcast.

Acceptance criteria:
1. Weekly briefing runs every Sunday morning Taiwan time.
2. Weekly report is synthesized, not merely concatenated.
3. It includes top 10, topic sections, teaching/research materials, and interesting medicine.

### Phase 8 — Knowledge Base and Personalization

Deliverables:
1. Login.
2. Role-based access.
3. Bookmarks.
4. Notes.
5. Topic watchlist.
6. Search.
7. pgvector semantic search.
8. Related articles.
9. Teaching/research/journal-club tags.

Acceptance criteria:
1. Users can save and annotate articles.
2. Search works by keyword and topic.
3. Similar article recommendations do not use unauthorized full text.

### Phase 9 — Admin, Review, and Safety

Deliverables:
1. Admin dashboard.
2. Draft / review / published status.
3. Manual rerun.
4. Edit AI summary.
5. Edit podcast script.
6. Pipeline error dashboard.
7. Audit logs.

Acceptance criteria:
1. Admin can preview and publish.
2. Admin can rerun failed jobs.
3. Admin actions are logged.
4. Institutional mode can require human review.

### Phase 10 — Deployment and Operations

Deliverables:
1. Vercel production.
2. Supabase production.
3. Render daily and weekly cron.
4. Storage buckets.
5. Error alerts.
6. Backup strategy.
7. Manual recovery guide.

Acceptance criteria:
1. Daily and weekly pipelines run reliably.
2. Failures notify admin.
3. Manual rerun works.
4. Secrets are not exposed.

### Phase 11 — Institutional Version

Deliverables:
1. Physician version.
2. Resident teaching version.
3. Nurse education version.
4. Research assistant version.
5. Library access links.
6. Possible SSO.
7. Usage analytics.
8. Journal club module.

Acceptance criteria:
1. Different roles see appropriate content.
2. Institutional access links do not store passwords.
3. Audit and permissions are enforced.

## 6. MVP Definition

MVP must include:

1. Daily 06:00 Taiwan time collection.
2. Core topic focus.
3. Deduplication.
4. Access status labeling.
5. AI classification and scoring.
6. Daily web briefing.
7. Daily 15–20 minute Podcast.
8. Interesting medicine item.
9. Weekly briefing.
10. Supabase storage.
11. Vercel website.
12. Render worker pipeline.
13. Human-first setup gate.
14. No unauthorized paid full-text storage.

## 7. Non-Goals for MVP

MVP does not include:

1. Patient-facing functions.
2. Clinical decision support or diagnosis.
3. Medical device positioning.
4. Automatic paywall bypassing.
5. Full hospital SSO.
6. Native mobile app.
7. Complete coverage of all specialties.
8. Public Apple/Spotify Podcast listing.
