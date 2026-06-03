# 04 Data Pipeline Spec

## 1. Purpose

This document defines the daily and weekly data pipeline. The pipeline runs on Render Python worker.

## 2. Schedule

### Daily

Taiwan time: every day 06:00.  
UTC cron: `0 22 * * *`.

Data window:
1. Start = current Taiwan 06:00 minus 24 hours.
2. End = current Taiwan 06:00.

### Weekly

Taiwan time: Sunday 06:00.  
UTC cron: `0 22 * * SAT`.

Data window:
1. Start = current Sunday Taiwan 06:00 minus 7 days.
2. End = current Sunday Taiwan 06:00.

## 3. Preconditions

Pipeline may run only if:
1. System status is READY.
2. Supabase connection is healthy.
3. Storage bucket exists.
4. Required secrets exist.
5. At least one source enabled.
6. AI provider configured.
7. Publication rules configured.
8. Safety settings enabled.

## 4. Source Collectors

### PubMed / NCBI

Collect:
1. PMID.
2. Title.
3. Abstract.
4. Authors.
5. Journal.
6. Publication date.
7. DOI.
8. Publication type.
9. MeSH / keywords when available.
10. URL.

### Crossref

Collect/enrich:
1. DOI.
2. Publisher.
3. Journal.
4. License metadata.
5. Funding metadata.
6. Relation metadata.
7. Correction/retraction relationships if available.

### Europe PMC

Collect/enrich:
1. PMID.
2. PMCID.
3. DOI.
4. OA full-text availability.
5. Full text URL if legal.
6. Preprint metadata.

### Unpaywall

Detect:
1. is_oa.
2. oa_status.
3. best_oa_location.
4. license.
5. legal PDF / landing page URL.

### RSS / TOC

Sources:
1. NEJM.
2. Lancet.
3. JAMA.
4. BMJ.
5. Annals of Internal Medicine.
6. Nature Medicine.
7. Circulation.
8. Kidney International.
9. JASN.
10. CJASN.
11. AJKD.
12. NDT.

### Preprints

Sources:
1. bioRxiv.
2. medRxiv.

Rules:
1. Always label as preprint.
2. Never treat as peer-reviewed.
3. Useful for early signal and research trends.

### Regulatory / Public Health

Sources:
1. FDA.
2. EMA.
3. WHO.
4. CDC.
5. Taiwan MOHW.
6. Taiwan CDC.
7. NHI.
8. Medical societies.

## 5. Query Keywords

Core nephrology query:
```text
kidney OR renal OR nephrology OR dialysis OR hemodialysis OR peritoneal dialysis OR CKD OR chronic kidney disease OR acute kidney injury OR proteinuria OR electrolyte OR acid-base OR glomerular OR cardiorenal OR vascular calcification
```

Cardiometabolic query:
```text
heart failure OR cardiovascular outcomes OR diabetes OR obesity OR SGLT2 OR GLP-1 OR finerenone OR hypertension OR metabolic syndrome OR fatty liver
```

Geriatrics query:
```text
frailty OR sarcopenia OR dementia OR falls OR polypharmacy OR aging OR long-term care
```

AI medicine query:
```text
artificial intelligence OR machine learning OR large language model OR clinical decision support OR digital health OR remote monitoring OR wearable OR medical AI
```

## 6. Candidate Article Model

Each candidate includes:
1. source_name.
2. source_type.
3. title.
4. abstract.
5. url.
6. DOI.
7. PMID.
8. PMCID.
9. authors.
10. journal.
11. publication_date.
12. collected_at.
13. raw_payload.
14. normalized_key.

## 7. Normalization

DOI:
1. lowercase.
2. trim.
3. remove `https://doi.org/`.
4. remove trailing punctuation.

PMID:
1. numeric string.
2. trim.

Title:
1. lowercase.
2. normalize whitespace.
3. remove punctuation.
4. used for fuzzy matching.

## 8. Deduplication Priority

1. Exact DOI.
2. Exact PMID.
3. Exact PMCID.
4. Same normalized title + first author + year.
5. High title similarity + same journal + close date.
6. RSS item matching PubMed item.

When duplicates are found:
1. Keep one canonical article.
2. Store all source links.
3. Merge metadata.
4. Prefer PubMed abstract.
5. Prefer DOI publisher URL.
6. Preserve OA links.

## 9. Access Status

Allowed values:
1. OPEN_ACCESS.
2. PMC_AVAILABLE.
3. PREPRINT_AVAILABLE.
4. INSTITUTIONAL_ACCESS_NEEDED.
5. ABSTRACT_ONLY.
6. USER_UPLOADED_FULL_TEXT.
7. UNKNOWN.

Rules:
1. Unpaywall OA true → OPEN_ACCESS.
2. PMCID full text → PMC_AVAILABLE.
3. bioRxiv / medRxiv → PREPRINT_AVAILABLE.
4. Publisher-only no OA → INSTITUTIONAL_ACCESS_NEEDED.
5. Abstract only → ABSTRACT_ONLY.
6. User uploaded legal PDF → USER_UPLOADED_FULL_TEXT.

## 10. AI Input Rules

Allowed AI input:
1. Title.
2. Abstract.
3. Metadata.
4. OA full text if legal.
5. Preprint full text if public.
6. User-uploaded legal PDF content.
7. Public regulatory text.

Not allowed:
1. Paywalled full text not legally obtained.
2. Publisher PDF without right.
3. Journal figures unless licensed.
4. Supplementary material unless licensed.

## 11. Daily Selection Logic

Daily output:
1. Must-read 5.
2. Specialty briefs.
3. Deep dive 1.
4. Clinical-basic translation 1.
5. Interesting medicine 1.
6. Trackable topics.

Selection combines:
1. Clinical impact.
2. Evidence strength.
3. Novelty.
4. Specialty relevance.
5. Teaching/research value.
6. Topic weight.
7. Source priority.
8. Access status.
9. Podcast suitability.

## 12. Weekly Selection Logic

Weekly pipeline:
1. Read prior 7 days.
2. Deduplicate.
3. Rerank.
4. Select top 10.
5. Summarize by topic.
6. Identify clinical-basic themes.
7. Identify research questions.
8. Extract teaching materials.
9. Select interesting medicine highlights.
10. Generate conclusion.

## 13. Job Status

Statuses:
1. queued.
2. running.
3. partial_success.
4. succeeded.
5. failed.
6. cancelled.

Each job records:
1. job_type.
2. target_date / target_week.
3. source window.
4. started_at.
5. finished_at.
6. total candidates.
7. total saved.
8. total analyzed.
9. total failed.
10. error_message.
11. triggered_by.
12. retry_of.

## 14. Error Handling

### Source failure

Continue if at least one required source works. Log warning.

### AI failure

Retry. If failed, mark article analysis_failed and continue.

### TTS failure

Store script, mark podcast failed, publish briefing only if allowed by rules.

### Storage failure

Retry upload. Do not depend on Render persistent disk.

## 15. Idempotency

1. Rerunning same date must not duplicate articles.
2. Briefings may be versioned.
3. Podcast may overwrite or version based on policy.
4. Job retries recorded.
5. Unique constraints prevent duplication.

## 16. Acceptance Criteria

1. Daily and weekly schedules work.
2. Candidate articles are collected.
3. Duplicates are merged.
4. Access status is labeled.
5. AI input respects copyright.
6. Job status and errors are recorded.
7. Manual rerun works.
8. Briefing generation can consume pipeline output.
