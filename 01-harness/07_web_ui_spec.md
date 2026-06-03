# 07 Web UI Spec

## 1. Purpose

This document defines website pages, user flows, admin flows, display requirements, and UI acceptance criteria. The website is built with Next.js and deployed on Vercel.

## 2. Global UI Principles

1. Professional medical style.
2. Clear information hierarchy.
3. Mobile-friendly.
4. Podcast-accessible.
5. Evidence and access labels visible.
6. Source links always available.
7. Admin and user views separated.
8. Initial setup appears before normal homepage when needed.

## 3. Navigation

Main navigation:
1. 今日早報.
2. 每週週報.
3. 文章資料庫.
4. 主題頻道.
5. Podcast.
6. 我的知識庫.
7. Admin.

Admin is hidden from non-admin users.

## 4. Initial Setup Dashboard

Route:
```text
/admin/setup
```

Sections:
1. System status.
2. Setup checklist.
3. Secrets status.
4. Data source status.
5. Topic weights.
6. Publication rules.
7. Medical safety settings.
8. Test pipeline.
9. Recent errors.

Requirements:
1. No secret values shown.
2. Pass/fail status visible.
3. Automation disabled until READY.
4. Admin can run test pipeline.

## 5. Home Page

Route:
```text
/
```

Sections:
1. Date header.
2. 今日一句話總結.
3. 今日必讀 5 篇.
4. Podcast player.
5. 專科快訊.
6. 今日深度解析.
7. 今日有趣醫學一則.
8. 今日值得追蹤主題.
9. Link to full daily briefing.

If today's briefing is missing:
1. Show last available briefing.
2. Admin sees pipeline status.
3. User sees friendly message.

## 6. Daily Briefing Page

Route:
```text
/daily/YYYY-MM-DD
```

Sections:
1. Title and date.
2. Source window.
3. Podcast player.
4. Transcript link.
5. 今日一句話總結.
6. 今日趨勢總覽.
7. 今日必讀 5 篇.
8. 腎臟與 CKD 快訊.
9. 透析快訊.
10. 心血管快訊.
11. 代謝快訊.
12. 老年醫學快訊.
13. 內科醫學快訊.
14. AI 醫療與數位醫學快訊.
15. 今日深度解析.
16. 今日臨床—基礎轉譯.
17. 今日有趣醫學一則.
18. 今日值得追蹤主題.
19. 原始文獻清單.
20. Disclaimer.

Article card fields:
1. Chinese title.
2. Original title.
3. Journal/source.
4. Date.
5. Study type.
6. Evidence level.
7. Total score.
8. Access status.
9. One-sentence summary.
10. Buttons: read, bookmark, note, source.

## 7. Weekly Briefing Page

Route:
```text
/weekly/YYYY-WW
```

Sections:
1. Week range.
2. Weekly podcast player.
3. 本週總結.
4. 本週十大必讀.
5. 分領域整理.
6. 本週臨床—基礎轉譯主題.
7. 本週值得追蹤研究問題.
8. 本週教學與研究素材.
9. 本週有趣醫學精選.
10. 本週結論.
11. Source list.

## 8. Article Page

Route:
```text
/articles/[id]
```

Sections:
1. Chinese title.
2. Original title.
3. Metadata: journal, date, authors, DOI, PMID, URL, access status, preprint status.
4. One-sentence summary.
5. Study type and evidence level.
6. Score panel.
7. Background.
8. Methods.
9. Main findings.
10. Clinical implications.
11. Basic mechanism.
12. Clinical-basic translation.
13. Limitations.
14. Taiwan relevance.
15. Teaching and research use.
16. Related articles.
17. User notes.
18. Bookmark controls.

## 9. Topic Pages

Routes:
1. /topics/nephrology
2. /topics/dialysis
3. /topics/ckd
4. /topics/cardiovascular
5. /topics/metabolism
6. /topics/geriatrics
7. /topics/internal-medicine
8. /topics/ai-medicine

Content:
1. Topic description.
2. Recent must-read articles.
3. Latest briefings.
4. Watchlist control.
5. Related journal club candidates.

## 10. Podcast Page

Route:
```text
/podcast
```

Sections:
1. Latest daily podcast.
2. Latest weekly podcast.
3. Podcast archive.
4. Audio player.
5. Transcript.
6. AI-generated audio disclosure.

Player:
1. Play/pause.
2. Seek.
3. Duration.
4. Playback speed.
5. Download if allowed.
6. Related briefing link.

## 11. Knowledge Base

Route:
```text
/library
```

Requires login.

Sections:
1. My bookmarks.
2. My notes.
3. Teaching materials.
4. Research ideas.
5. Journal club candidates.
6. Topic watchlist.
7. Saved podcasts.

## 12. Search Page

Route:
```text
/search
```

Features:
1. Keyword search.
2. Topic filter.
3. Date range.
4. Evidence level.
5. Access status.
6. Study type.
7. Score range.
8. Sort by recency, score, relevance.

## 13. Admin Dashboard

Route:
```text
/admin
```

Sections:
1. System status.
2. Latest daily job.
3. Latest weekly job.
4. Drafts awaiting review.
5. Manual rerun controls.
6. Source health.
7. Recent errors.
8. Audit logs link.

## 14. Admin Review Pages

Routes:
1. /admin/review/daily/YYYY-MM-DD
2. /admin/review/weekly/YYYY-WW

Functions:
1. Preview.
2. Edit summaries.
3. Edit podcast script.
4. Regenerate podcast.
5. Approve publish.
6. Reject and rerun.
7. View sources.

## 15. Visual Design

Tone:
1. Professional.
2. Academic.
3. Calm.
4. Trustworthy.

Badges:
1. RCT.
2. Cohort.
3. Guideline.
4. Basic Science.
5. Preprint.
6. Open Access.
7. Institutional Access Needed.
8. Must Read.
9. Teaching.
10. Research Idea.

## 16. Accessibility

1. Semantic HTML.
2. Keyboard-accessible audio player.
3. Transcript for audio.
4. Sufficient contrast.
5. Do not rely only on color.
6. Alt text for images.

## 17. Acceptance Criteria

1. Setup dashboard exists.
2. Daily page displays all sections.
3. Weekly page displays all sections.
4. Article page displays metadata and summary.
5. Podcast player works.
6. Admin can preview drafts.
7. Users can bookmark and note.
8. Mobile layout is readable.
9. Evidence and access badges visible.
10. Source links always available.
