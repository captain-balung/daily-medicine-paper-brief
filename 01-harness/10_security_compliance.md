# 10 Security and Compliance

## 1. Purpose

This document defines platform security, copyright, medical safety, privacy, secret management, RLS, AI disclosure, and incident response.

## 2. Core Principles

1. Do not expose secrets.
2. Do not store unauthorized paid full text.
3. Do not present AI content as clinical decision guidance.
4. Do not collect patient data in MVP.
5. Protect user notes and bookmarks.
6. Audit admin actions.
7. Label preprints.
8. Disclose AI-generated audio.
9. Require legal confirmation for uploaded PDFs.
10. Link paywalled articles to institutional access instead of storing them.

## 3. Secret Management

Do not store in normal tables:
1. OpenAI API key.
2. TTS API key.
3. Supabase service role key.
4. Database URL.
5. Render internal secret.
6. Vercel token.
7. User passwords.
8. Library credentials.

Allowed storage:
1. Render environment variables.
2. Vercel environment variables for server-side values.
3. Supabase Vault if used.
4. Local `.env` excluded from Git.

Frontend may use:
1. NEXT_PUBLIC_SUPABASE_URL.
2. NEXT_PUBLIC_SUPABASE_ANON_KEY.
3. NEXT_PUBLIC_SITE_URL.

Frontend must not use:
1. Service role key.
2. OpenAI API key.
3. TTS API key.
4. Database direct URL.
5. Worker secret.

## 4. Authentication and Roles

MVP:
1. Supabase Auth email.
2. Google OAuth optional.

Roles:
1. admin.
2. physician.
3. resident.
4. nurse.
5. research_assistant.
6. viewer.

Admin:
1. Setup.
2. Pipeline control.
3. Draft review.
4. Publish.
5. Edit content.
6. View logs.

User roles:
1. Read appropriate content.
2. Bookmark.
3. Notes.
4. Role-specific views in future.

## 5. RLS

Enable RLS for:
1. profiles.
2. bookmarks.
3. notes.
4. topic_watchlists.
5. uploaded PDF metadata.
6. draft briefings.
7. admin settings.
8. audit logs.

Rules:
1. Users read/write own bookmarks.
2. Users read/write own notes.
3. Admin can manage drafts.
4. Published content can be public or authenticated depending on mode.
5. Service role used only by backend worker.

## 6. Copyright and Full-Text Policy

Allowed to store:
1. Title.
2. Authors.
3. Journal.
4. Date.
5. DOI.
6. PMID.
7. PMCID.
8. Abstract.
9. Source URL.
10. OA status.
11. AI-generated summary.
12. AI-generated commentary.
13. User notes.
14. Legal OA full text if license permits.
15. User-uploaded PDF if legal.

Not allowed unless licensed:
1. Paid article body.
2. Publisher PDF.
3. Journal figures.
4. Supplementary materials.
5. Long copyrighted excerpts.
6. Institutional credentials.
7. Paywalled downloads.

Paywalled articles:
1. Label INSTITUTIONAL_ACCESS_NEEDED.
2. Show DOI / publisher / PubMed links.
3. Show hospital/library link if configured.
4. Do not store full text.

## 7. User-Uploaded PDFs

Rules:
1. User confirms legal access.
2. Store in private bucket.
3. Access limited to authorized users.
4. Do not redistribute.
5. Do not make public.
6. Log upload.
7. Allow deletion.

## 8. Medical Content Safety

Every article must include:
1. Study type.
2. Evidence level.
3. Access status.
4. Preprint status.
5. Limitations.
6. Source link.
7. Date.
8. Abstract-only or full-text-based status.

Required disclaimers:

Preprint:
```text
本研究為 preprint，尚未經同儕審查，不建議直接改變臨床決策。
```

Abstract-only:
```text
目前僅根據標題、摘要與公開 metadata 進行整理，尚未進行完整全文分析。
```

Paywalled:
```text
本文可能需要透過醫院或學校圖書館機構登入取得全文。平台不儲存未授權付費全文。
```

General:
```text
本平台內容僅供醫學新知整理、教育與研究參考，不作為個別病人之診斷或治療建議。
```

## 9. AI Transparency

Website should disclose:
1. Summaries are AI-assisted.
2. Sources are provided.
3. Human review status may vary by mode.

Podcast disclosure:
```text
本音訊由 AI 根據每日醫學情報早報自動生成。
```

Store metadata:
1. Model used.
2. Prompt version.
3. Output version.
4. Generated time.
5. Human edits.

## 10. Privacy

MVP should not collect patient data.

Allowed:
1. Email.
2. Display name.
3. Role.
4. Bookmarks.
5. Notes.
6. Topic preferences.

Avoid:
1. Patient identifiers.
2. Clinical charts.
3. Protected health information.
4. Hospital confidential data.

Future patient-data use requires separate compliance design.

## 11. Audit Logs

Record:
1. Admin settings changes.
2. Publication events.
3. Manual reruns.
4. AI content edits.
5. Source activation changes.
6. User role changes.
7. PDF uploads.
8. Safety overrides.

## 12. Publication Safety Check

Before publishing:
1. Sources exist.
2. Source URL exists for each article.
3. Evidence labels exist.
4. Limitations exist.
5. Access status exists.
6. Preprint warnings exist.
7. No unauthorized full text stored.
8. AI audio disclosure exists.
9. Medical disclaimer exists.
10. Review completed if required.

## 13. Incident Response

### Secret exposure

1. Revoke secret.
2. Replace env variable.
3. Review logs.
4. Check repository history.
5. Rotate related keys.
6. Document incident.

### Unauthorized full text stored

1. Remove content.
2. Check storage.
3. Review pipeline.
4. Add validation.
5. Log incident.

### Incorrect medical content published

1. Unpublish or correct.
2. Add correction note.
3. Review source and AI output.
4. Improve prompt or validation.
5. Log incident.

## 14. Acceptance Criteria

1. Secrets protected.
2. RLS enabled.
3. Paid full text not stored.
4. Preprints labeled.
5. Disclaimer visible.
6. AI audio disclosure visible.
7. Admin actions logged.
8. Notes private by default.
9. PDFs private.
10. Publication safety check exists.
