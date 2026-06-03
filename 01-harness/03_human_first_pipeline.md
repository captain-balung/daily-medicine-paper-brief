# 03 Human-First Pipeline

## 1. Principle

Human-First Pipeline means all human-required decisions must occur before machine automation.

Human responsibilities come first:
1. Accounts.
2. Roles.
3. Secrets.
4. Source activation.
5. Topic weights.
6. Publication rules.
7. Medical safety rules.
8. Copyright rules.
9. Test pipeline approval.

Machine responsibilities come after:
1. Data collection.
2. AI classification.
3. AI summary.
4. Podcast generation.
5. Web publication.

## 2. First Screen Requirement

If the system is not ready, the first admin screen must be the Initial Setup Dashboard, not the public homepage.

System states:
1. SETUP_REQUIRED
2. CONFIGURED
3. TESTING
4. READY
5. RUNNING
6. DRAFT_CREATED
7. REVIEW_REQUIRED
8. PUBLISHED
9. FAILED

Only READY or above may run scheduled pipelines.

## 3. Initial Setup Dashboard Sections

### 3.1 System Status

Show:
1. Current status.
2. Required next action.
3. Setup checklist.
4. Last test pipeline result.
5. Last error.

### 3.2 Accounts and Roles

Roles:
1. admin.
2. physician.
3. resident.
4. nurse.
5. research_assistant.
6. viewer.

### 3.3 Secrets Status

Check but never display:
1. SUPABASE_SERVICE_ROLE_KEY.
2. OPENAI_API_KEY.
3. TTS_API_KEY.
4. NCBI_API_KEY.
5. UNPAYWALL_EMAIL.
6. CROSSREF_MAILTO.
7. WORKER_INTERNAL_SECRET.

UI shows only:
1. configured / missing.
2. last checked.
3. connection test status.

### 3.4 Source Activation

Admin chooses enabled sources:
1. PubMed.
2. Crossref.
3. Europe PMC.
4. Unpaywall.
5. RSS / TOC.
6. bioRxiv.
7. medRxiv.
8. FDA / EMA / WHO / CDC.
9. Taiwan MOHW / CDC.

### 3.5 Topic Weights

Default:
1. Nephrology 5.
2. Dialysis 5.
3. CKD 5.
4. Cardiorenal-metabolic 5.
5. Cardiovascular 4.
6. Metabolism 4.
7. Geriatrics 4.
8. Internal medicine 3.
9. AI medicine 4.
10. Basic/translational 3.
11. Drug safety/guidelines 4.
12. Interesting medicine 2.

### 3.6 Publication Rules

Modes:
1. Auto Publish.
2. Draft First.
3. Review Required.
4. Manual Only.

Recommended:
1. Personal MVP: Draft First or Auto Publish.
2. Institutional version: Review Required.
3. Testing: Manual Only.

### 3.7 Medical Safety Settings

Required:
1. Preprint warning.
2. Evidence label.
3. Limitations.
4. Source citation.
5. Medical disclaimer.
6. AI-generated audio disclosure.
7. Paid full-text restriction.
8. Institutional access label.

### 3.8 Test Pipeline

Test steps:
1. Supabase connection.
2. Storage upload.
3. PubMed fetch.
4. Crossref fetch.
5. Unpaywall OA check.
6. AI summary.
7. TTS generation.
8. Draft creation.
9. Frontend display.

## 4. Readiness Checks

System can become READY only if:
1. Supabase connection passes.
2. Storage bucket exists.
3. Required secrets exist.
4. At least one source is enabled.
5. AI provider is configured.
6. TTS provider is configured.
7. Publication mode is selected.
8. Paid full-text policy is confirmed.
9. Preprint warning is enabled.
10. Medical disclaimer is enabled.
11. Test pipeline passes.

## 5. Pipeline Execution Rules

Daily pipeline may run only when:
1. status = READY.
2. daily cron enabled.
3. required secrets exist.
4. active sources exist.
5. publication rules exist.

Weekly pipeline may run only when:
1. status = READY.
2. weekly cron enabled.
3. prior 7 days data exist.
4. weekly settings exist.

## 6. Security Rules

1. Do not store API keys in normal tables.
2. Do not expose secrets in browser.
3. Do not print secrets in logs.
4. Do not run full pipelines from frontend.
5. Admin actions require authentication and admin role.
6. Manual pipeline triggers require authorization.
7. Admin actions must be audit logged.

## 7. Acceptance Criteria

1. Setup dashboard appears before public homepage if incomplete.
2. Secret status is visible without secret values.
3. Setup checks can pass or fail.
4. Pipeline cannot publish when setup is incomplete.
5. Admin can run test pipeline.
6. System becomes READY only after successful checks.
7. Safety settings are enforced before publication.
