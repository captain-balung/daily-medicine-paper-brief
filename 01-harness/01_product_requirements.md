# 01 Product Requirements

## 1. Product Purpose

The platform is a medical research intelligence and knowledge translation system. It collects global medical updates, filters and classifies them, scores their importance, creates Chinese professional summaries, links clinical findings to basic mechanisms, publishes web briefings, and generates medical Podcast audio.

## 2. Users

### Primary users

1. Nephrologist / internist.
2. Medical researcher.
3. Medical teacher.
4. Clinical leader.

Needs:
1. Daily high-quality medical intelligence.
2. Nephrology, dialysis, CKD, cardiorenal-metabolic, geriatrics, internal medicine, and AI medicine focus.
3. Evidence level and clinical implications.
4. Teaching and research reuse.
5. Podcast learning during commute.

### Secondary users

1. Hospital physicians.
2. Residents.
3. Nurses.
4. Research assistants.

Needs:
1. Role-appropriate summaries.
2. Teaching version for residents.
3. Care-point version for nurses.
4. Literature-tracking version for research assistants.

## Core Medical Scope

The MVP focuses on:

1. Nephrology: CKD, AKI, proteinuria, glomerular disease, electrolytes, acid-base disorders, CKD-MBD, anemia, cardiorenal syndrome, renal fibrosis, nephrotoxicity, kidney biomarkers.
2. Dialysis: hemodialysis, peritoneal dialysis, intradialytic hypotension, dialysis adequacy, vascular access, dialysis infection, dialysis nutrition, cognition, home dialysis, remote monitoring.
3. CKD and cardiorenal-metabolic medicine: diabetes, SGLT2 inhibitors, GLP-1 receptor agonists, finerenone, hypertension, obesity, dyslipidemia, heart failure, vascular calcification, frailty.
4. Cardiovascular medicine: heart failure, atrial fibrillation, coronary disease, hypertension, stroke prevention, anticoagulation, cardiovascular outcomes trials.
5. Metabolism: diabetes, obesity, fatty liver, insulin resistance, hyperuricemia, metabolic syndrome, nutrition, muscle metabolism.
6. Geriatrics: frailty, sarcopenia, dementia, falls, polypharmacy, nutrition, functional decline, long-term care, geriatric nephrology.
7. Internal medicine: infection, critical care, sepsis, pulmonary, GI, rheumatology, hematology, guidelines, drug safety.
8. AI medicine and digital health: clinical decision support, digital biomarkers, remote monitoring, LLMs in medicine, imaging AI, wearables, contactless monitoring, workflow AI, AI safety and governance.


## 3. Data Sources

### High-priority clinical journals

1. NEJM.
2. Lancet.
3. JAMA.
4. BMJ.
5. Annals of Internal Medicine.
6. Nature Medicine.
7. Cell.
8. Circulation.

### Nephrology and dialysis journals

1. Kidney International.
2. JASN.
3. CJASN.
4. AJKD.
5. Nephrology Dialysis Transplantation.
6. Peritoneal Dialysis International.
7. Hemodialysis International.

### Basic and translational research

1. Nature.
2. Science.
3. Cell.
4. Nature Biotechnology.
5. Nature Immunology.
6. Cell Metabolism.
7. Nature Medicine.

### Preprints

1. bioRxiv.
2. medRxiv.

Preprints must always be labeled as not peer-reviewed.

### Regulatory and public health sources

1. FDA.
2. EMA.
3. WHO.
4. CDC.
5. Taiwan MOHW.
6. Taiwan CDC.
7. NHI Administration.
8. Relevant medical society announcements.

## 4. Core Product Features

### 4.1 Daily Briefing

Runs every day at 06:00 Taiwan time and covers the prior 24 hours.

Required sections:
1. 今日一句話總結.
2. 今日趨勢總覽.
3. 今日必讀 5 篇.
4. 腎臟與 CKD 快訊.
5. 透析快訊.
6. 心血管快訊.
7. 代謝快訊.
8. 老年醫學快訊.
9. 內科醫學快訊.
10. AI 醫療與數位醫學快訊.
11. 今日深度解析 1 篇.
12. 今日臨床—基礎轉譯.
13. 今日有趣醫學一則.
14. 今日值得追蹤主題.
15. 原始文獻清單.
16. Podcast 播放器與逐字稿.

### 4.2 Daily Podcast

Target length: 15–20 minutes.

Structure:
1. Opening and overview: 1–2 minutes.
2. Top 5 studies: 8–10 minutes.
3. Specialty briefs: 3–4 minutes.
4. Clinical-basic translation: 3–4 minutes.
5. Interesting medicine: 1–2 minutes.
6. Closing: about 30 seconds.

Language:
1. Chinese as primary language.
2. English medical terms retained when useful.

### 4.3 Weekly Briefing

Runs every Sunday morning Taiwan time and covers prior seven days.

Required sections:
1. 本週總結.
2. 本週十大必讀.
3. 分領域整理.
4. 本週臨床—基礎轉譯主題.
5. 本週值得追蹤的研究問題.
6. 本週教學與研究素材.
7. 本週有趣醫學精選.
8. 本週結論.
9. 週報 Podcast.

### 4.4 Knowledge Base

Future features:
1. Bookmarks.
2. Notes.
3. Topic watchlist.
4. Search.
5. Semantic search.
6. Related articles.
7. Teaching/research/journal-club tags.
8. PDF upload and legal full-text analysis.

## 5. Article Output Requirements

Each article must include:
1. Chinese title.
2. Original title.
3. Source.
4. Date.
5. Authors.
6. DOI.
7. PMID.
8. URL.
9. Access status.
10. Preprint status.
11. One-sentence summary.
12. Study type.
13. Topic classification.
14. Evidence level.
15. Importance score.
16. Background.
17. Methods.
18. Main findings.
19. Clinical implications.
20. Basic mechanism.
21. Clinical-basic translation.
22. Limitations.
23. Taiwan clinical relevance.
24. Teaching use.
25. Research use.
26. Podcast suitability.

## 6. Publication Modes

### Personal MVP mode

Can allow auto-publish after setup checks pass.

### Institutional mode

Should use draft → admin review → publish.

## 7. MVP Acceptance Criteria

1. Daily data collection works.
2. AI classification and scoring works.
3. Daily web briefing is generated.
4. Daily Podcast is generated.
5. Weekly briefing is generated.
6. Interesting medicine appears daily.
7. Source links and evidence labels appear.
8. Preprint and access warnings appear.
9. No paid full text is stored without authorization.
10. Admin can see pipeline status.
