# 06 AI Content Spec

## 1. Purpose

This document defines AI behavior for classification, scoring, summarization, clinical-basic translation, daily briefing, weekly briefing, Podcast scripts, and interesting medicine.

## 2. General Rules

1. Use professional Traditional Chinese.
2. Retain important English medical terms.
3. Do not claim full-text analysis if only abstract is available.
4. Do not store or reproduce paid full text.
5. Preprints must be labeled as not peer-reviewed.
6. Every article must include limitations.
7. Avoid direct clinical treatment instructions.
8. Include source and evidence labels.
9. State uncertainty when data are insufficient.
10. Output structured JSON for pipeline functions.

## 3. Topic Classification

Primary categories:
1. Nephrology.
2. Dialysis.
3. CKD.
4. Cardiovascular Medicine.
5. Metabolism.
6. Geriatrics.
7. Internal Medicine.
8. AI Medicine and Digital Health.
9. Basic and Translational Research.
10. Drug Safety and Guideline Updates.
11. Interesting Medicine.

Output:
```json
{
  "primary_topic": "CKD",
  "secondary_topics": ["Cardiovascular Medicine", "Metabolism"],
  "topic_confidence": 0.87,
  "topic_rationale": "..."
}
```

## 4. Study Type Classification

Allowed study types:
1. Randomized controlled trial.
2. Meta-analysis.
3. Systematic review.
4. Guideline.
5. Cohort study.
6. Case-control study.
7. Cross-sectional study.
8. Case report.
9. Case series.
10. Basic science.
11. Animal study.
12. Cell study.
13. Omics study.
14. AI model study.
15. Preprint clinical study.
16. Preprint basic science.
17. Regulatory alert.
18. Public health announcement.
19. Editorial.
20. News.
21. Commentary.

## 5. Evidence Level

Score 5:
1. Large RCT.
2. Official guideline.
3. High-quality meta-analysis.

Score 4:
1. Good cohort.
2. Multicenter study.
3. Strong real-world evidence.

Score 3:
1. Small clinical study.
2. Registry.
3. Exploratory trial.

Score 2:
1. Case series.
2. Case report.
3. Preprint.

Score 1:
1. Animal.
2. Cell.
3. Hypothesis.
4. Early basic science.

Preprint cannot receive evidence strength 5 unless separately peer-reviewed.

## 6. Importance Scoring

Each score is 1–5.

### Clinical Impact

5 = may change practice or guideline.  
4 = clearly relevant to clinical decisions.  
3 = worth knowing but not practice-changing.  
2 = knowledge mainly.  
1 = low clinical impact.

### Evidence Strength

Use section 5.

### Novelty

5 = new therapy, mechanism, or diagnostic approach.  
4 = important new indication or evidence.  
3 = adds to existing concept.  
2 = small update.  
1 = repetitive.

### Specialty Relevance

5 = directly kidney, dialysis, CKD, or cardiorenal-metabolic.  
4 = highly relevant internal medicine, geriatrics, cardiovascular, metabolic.  
3 = general internal medicine.  
2 = indirect.  
1 = low relevance.

### Teaching and Research Value

5 = excellent for lecture, research idea, or teaching case.  
4 = useful for slides.  
3 = background knowledge.  
2 = occasional reference.  
1 = limited.

### Total Score

22–25: 今日必讀.  
18–21: 值得深入閱讀.  
14–17: 快速瀏覽.  
10–13: 收藏備查.  
<10: 不主動推送.

## 7. Article Summary Template

Each summary must include:
1. 中文標題.
2. 英文原標題.
3. 一句話重點.
4. 研究類型.
5. 證據等級.
6. 主題分類.
7. 背景問題.
8. 研究方法.
9. 主要結果.
10. 作者結論.
11. 臨床意義.
12. 基礎機轉.
13. 臨床—基礎轉譯.
14. 研究限制.
15. 對台灣臨床的啟示.
16. 教學用途.
17. 研究用途.
18. 是否值得追蹤.
19. 警示與限制.

## 8. Clinical-Basic Translation Template

Sections:
1. 臨床問題.
2. 基礎機轉.
3. 研究發現.
4. 臨床可能應用.
5. 目前限制.
6. 後續追蹤.

## 9. Daily Briefing Generation

Daily briefing sections:
1. 今日一句話總結.
2. 今日趨勢總覽.
3. 今日必讀 5 篇.
4. 專科快訊.
5. 今日深度解析.
6. 今日臨床—基礎轉譯.
7. 今日有趣醫學一則.
8. 今日值得追蹤主題.
9. 原始來源清單.

Tone:
1. Professional.
2. Clear.
3. Not sensational.
4. No overclaiming.
5. Suitable for nephrologist / internist.

## 10. Podcast Script Generation

Target length: 15–20 minutes.

Structure:
1. Opening and overview: 1–2 minutes.
2. Top 5 studies: 8–10 minutes.
3. Specialty briefs: 3–4 minutes.
4. Clinical-basic translation: 3–4 minutes.
5. Interesting medicine: 1–2 minutes.
6. Closing: 30 seconds.

Style:
1. Conversational but professional.
2. Chinese primary; English terms retained.
3. Suitable for listening, not just reading.
4. Natural transitions.
5. Avoid too many parentheses or tables.

Disclosure:
```text
本音訊由 AI 根據每日醫學情報早報自動生成，內容供醫學新知整理與教育用途，不作為臨床決策依據。
```

## 11. Weekly Briefing Generation

Weekly briefing must:
1. Not simply concatenate daily briefings.
2. Rerank top articles.
3. Identify major themes.
4. Summarize by topic.
5. Extract teaching materials.
6. Extract research questions.
7. Select weekly interesting medicine highlights.
8. Produce weekly conclusion.

## 12. Interesting Medicine

Allowed:
1. Interesting case report.
2. Medical history.
3. Clinical myth.
4. Serious but funny study.
5. Medical terminology trivia.
6. Animal research with unusual insight.
7. Hospital-work phenomenon with scientific explanation.

Rules:
1. Not vulgar.
2. Do not mock patients.
3. No private patient data.
4. Must retain educational value.
5. Must cite source when based on literature.

## 13. Required Warnings

Preprint:
```text
本研究為 preprint，尚未經同儕審查，不建議直接改變臨床決策。
```

Abstract-only:
```text
目前僅根據標題、摘要與公開 metadata 進行整理，尚未進行完整全文分析。
```

Institutional access:
```text
本文可能需要透過醫院或學校圖書館機構登入取得全文。平台不儲存未授權付費全文。
```

## 14. Quality Checks Before Publishing

1. Source link exists.
2. Evidence label exists.
3. Limitations exist.
4. Access status exists.
5. Preprint warning exists if needed.
6. No unauthorized full text is used.
7. No direct clinical instruction.
8. Podcast disclosure exists.
9. Interesting medicine item exists.
10. All must-read items have scores.

## 15. Acceptance Criteria

1. AI outputs structured summaries.
2. Scores follow rubric.
3. Briefings are readable.
4. Podcast script is listenable.
5. Warnings are correct.
6. Weekly synthesis is not mere concatenation.
7. Output can be stored in Supabase.
