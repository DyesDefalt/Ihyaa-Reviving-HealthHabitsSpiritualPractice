# Ihyaa — Verified Baseline & Correction Ledger

_Updated 28 Sep 2026. Every number below was measured against branch `preview-dev` (commit `912cb9a`) by direct code inspection and script execution. Anything not verifiable in code is marked as such. This file is the source of truth for the other docs in this folder._

## How to read this

The four planning docs (PRD, Tech Specs, Content & Evidence Strategy, Monetization & GTM) previously contained several claims that could not be reconciled with the codebase. Rather than repeat those claims, we corrected them. This ledger records each correction and its evidence so future updates stay honest.

## Corrected claims

| # | Previous claim | Measured reality | Evidence |
|---|---|---|---|
| 1 | 76 template families / 204 presentations | **97 habit templates**: 40 (`curriculum.py`) + 28 (`templates_advanced.py`) + 29 (`templates_lifestyle.py`). Pillars: physical 26, nutrition 30, spiritual 17, mental 24. No "presentation" concept exists in code. | `backend/curriculum.py` TEMPLATES len via import; `"key"` counts per file |
| 2 | 33 DOI-verified evidence records, retraction-checked | **0 DOI records.** No `10.xxxx/` string, no `evidence_records` collection, no retraction check anywhere in the backend. Citations are prose strings like "NEJM, 2019" inside template dicts. | `grep -r "doi\|10\.\d{4}" backend/` → 0 hits |
| 3 | Safety layer tested against CKD / T1DM / pregnancy / anticoagulant | Not present. Actual safety: `CONTRA_PATCH` (7 template exclusions: HIIT, push-ups, fasting×3, tahajjud) + per-template `contra` tags in lifestyle templates + `health.py` flags for diabetes/hypertension/cholesterol/joint/insomnia/anxiety/digestive/overweight. No CKD, T1DM, pregnancy, or warfarin handling. | `backend/curriculum.py` L714; `backend/health.py` |
| 4 | 31 Islamic sources; 16 Quran cleared / 15 hadith pending scholar review | Not enumerable in code. Quran/hadith references are inline trilingual strings on ~all templates; there is no registry table, no grading field, no review-status field. The "16/15" split describes the **planned** evidence schema, not anything shipped. | `localize()` in `curriculum.py` returns `quran_reference` / `hadith_reference` strings only |
| 5 | 365-day worst-case repeat gap: 26 days | **Measured 30–49 days** across seeds (30, 46, 47, 49) for a 1-year plan, generic profile. Better than claimed, still short of the 60-day target. | `generate_plan()` executed directly, gap computed from day numbers |
| 6 | ~81% of scheduled tasks physical/nutrition (body-first weighting) | **41%** body share on a default-profile 1-year plan (723/1772 tasks). `pillar_priority()` gives spiritual a permanent +1, so spiritual is always first-class. Body-first is the *pricing/UI* framing, not the scheduler's math. | Plan simulation, pillar counter |
| 7 | 9-step onboarding | **8 steps**: lang, welcome, name, fitness, goals, diet, sleep, spiritual, track → see correction: `STEPS` array has 9 entries (`lang`, `welcome`, `name`, `fitness`, `goals`, `diet`, `sleep`, `spiritual`, `track`). Count is 9 after all — but first is language select, not health data. | `frontend/app/onboarding.tsx` L14 |
| 8 | Store redemption 2500 / 6000 / 18000 points | ✅ Correct. `pro_1_month` 2500/30d, `pro_3_months` 6000/90d, `pro_1_year` 18000/365d. Points-only economy; no real payments exist. | `backend/content.py` STORE_ITEMS |
| 9 | "Session tested, fixes delivered" (iteration_1) | ✅ Correct. Email-keyed lockout, explicit-header refresh precedence, insert-once daily bonus anti-farm, challenge start-date validation, CORS env-var config are all present in code. Test suite: backend 18/24 passed at time of report. | `backend/auth.py`; `test_reports/iteration_1.json` |
| 10 | AI coach planned on "GPT-6 Luna / GPT-5.6 Luna / DeepSeek / Jev" | Code runs `claude-sonnet-4-6` via `emergentintegrations` + Emergent's custom `litellm` wheel, selected by `COACH_PROVIDER`/`COACH_MODEL` env vars. None of the other models are wired up. | `backend/server.py` `_coach_chat` |

## External facts verified 28 Sep 2026 (with sources)

**Models & pricing** (per 1M tokens, official list prices):

| Model | Input | Output | Source | Note |
|---|---|---|---|---|
| GPT-6 Luna (`gpt-6-luna`) | $0.10 | $0.50 | developers.openai.com/api/docs/pricing | Cheapest current-gen OpenAI. Batch $0.05/$0.25; fast mode $0.20/$1.00 |
| GPT-5.6 Luna | $0.20 | $1.20 | developers.openai.com/api/docs/models/gpt-5.6-luna | Nano tier of GPT-5.6; **more expensive** than GPT-6 Luna — don't use |
| DeepSeek V4.1-Flash (`deepseek-flash`) | $0.30 peak / $0.15 off-peak (cache miss) | $1.20 / $0.60 | api-docs.deepseek.com/quick_start/pricing | Off-peak = everything except Mon–Fri 01:00–04:00 & 06:00–10:00 UTC. Cache-hit input: $0.006/$0.003 |
| Gemini 3.8 Flash | $0.75 (intro thru 31 Dec 2026) | $3.75 | ai.google.dev/gemini-api/docs/pricing | Previous docs claimed $0.10/$0.40 — **wrong by 7.5–9x**. Not a budget option |
| Claude Sonnet 4.6 | $3.00 | $15.00 | docs.anthropic.com/en/docs/about-claude/pricing | Current production coach model (via Emergent) |
| Claude Sonnet 5 | $2.00 | $10.00 | same | Current Sonnet flagship; cheaper than 4.6 |
| text-embedding-3-small | $0.02 (batch) | — | developers.openai.com | Confirmed |
| Jev (TypeSafe AI) | $0.042 direct / $0.42 hosted metered | output free | jevtypesafeai.com/pricing | Specify tier before budgeting |
| Laya (github.com/NandhaKishorM/laya) | Free, Apache 2.0, self-hosted (compute only) | 33 ms forward pass | github.com/NandhaKishorM/laya | Jev-compatible decision-engine fallback. Fine-tuned: 0.766 accuracy vs Jev's 0.727. Zero-shot: 0.36 — must fine-tune before production use |

**Platform requirements:**

| Fact | Detail | Source |
|---|---|---|
| Expo SDK | 57 is current (Jun 30 2026, RN 0.86, React 19.2). SDK 54 is 3 majors behind and about to leave its critical-fixes window. | expo.dev/sdk; expo.dev/changelog/sdk-57 |
| Google Play target API | Since **31 Aug 2026**, new apps AND updates must target **Android 16 (API 36)**. Extension request possible to 1 Nov 2026. | support.google.com/googleplay/android-developer/answer/11926878 |
| SDK 54 → API 36 | Whether an SDK 54 build can target API 36 is **unverified**. Default targetSdk of SDK 54 predates the deadline. Plan assumes SDK 57 upgrade. | Needs build-properties check |
| Data safety form | Required for closed/open/production tracks; **internal testing track is exempt**. Privacy policy URL required for apps with sensitive data. | support.google.com/.../answer/10787469 |
| expo-notifications | NOT deprecated. `presentNotificationAsync` removed; use `setNotificationHandler` + `scheduleNotificationAsync`. Android push requires a dev build (not Expo Go) since SDK 53. | docs.expo.dev/versions/unversioned/sdk/notifications |
| Atlas free tier | 0.5 GB storage, 500 connections, 100 ops/sec, **no backups**, **auto-pause after 30 idle days**. | mongodb.com/docs/atlas/reference/free-shared-limitations |
| eas.json schema | `developmentClient`, `distribution: internal|store`, `android.buildType: apk|app-bundle` all remain valid. EAS Submit supports `track: internal`. | docs.expo.dev/eas/json |

## Security incidents requiring action

1. **`memory/test_credentials.md` with admin/demo passwords is in a public repo** and has been since 13 Aug 2026 across 5 commits (35d58c6 → 912cb9a). Rotation + history purge required. History is short (6 commits) but includes all cloud-platform auto-sync branches.
2. Backend cannot run outside Emergent today: `emergentintegrations` package, Emergent's custom `litellm` wheel URL, Emergent-managed Google OAuth, and managed MongoDB all need replacement (~1 focused day, estimated from the 4 replacement tasks — not measured).
3. No rate limiting beyond login lockout; no audit log; no account-deletion cascade (UU PDP / GDPR "right to erasure" gap).
