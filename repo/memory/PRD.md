# Ihyaa — Product Requirements & Build Log

## Original problem statement (13 Aug 2026)
> Build a mobile app: for challenge and guidance and plan like for 30 Days, 100 Days, and a year
> to become more healthy in terms of physicals and mindness. But its for Islamic way. So its
> following the quran, hadits, and other source that credible and have journal and clinically
> proven by doctors and scientist and all of the plan will be 100% halal. So the user will become
> healthy and getting spiritual reward. Plan will be personalize based on user preferences when
> signing up and always adjustable. The plan will booked to the calendar so calendar will be
> alerting the user reminding to do. Since its challenge and most of user will be tired following
> this, we will implementing theory 1% better each days so in early it will be simple short fast
> task for building the habits. Also there are check in daily and rewarding the user poin that can
> exchange with any on the store (but for now they can only exchange with pro plan version).
> Language: English, Arabic and Bahasa Indonesia. Content depth at launch start with 30 Days first.
> Design feel: modern minimalist look with subtle Islamic geometric accents.
> The App name: Ihyaa — Revival.

## Current user instructions — 5 Oct 2026 (override older requirements)
- Health FIRST: food/drinks, practical recipes, halal supplement education, movement, sleep,
  healthy habits, mindfulness/clear thinking; Islamic inspiration complements rather than
  replaces medical evidence. Not just a prayer/reminder app.
- Individual plans should differ materially using user profile/preferences.
- User supplied five documents and requested following them, with **English and Indonesian
  only for now**. Arabic UI language is deactivated; scripture/brand Arabic is not prohibited.
- Latest request: **“Add the ChatGPT AI Models integration to my app.”**
- Approved continuation after proposing Emergent LLM key, personalized EN/ID wellness coaching,
  and separate persistent chat conversations. Uploaded technical spec names **GPT-6 Luna**;
  this exact OpenAI model is configured and has returned verified live responses.
- Requested GitHub continuation on `hermes-update` and `preview-dev`. Only local `main` was
  present. No checkout, commit, push, merge or remote-branch update performed. User must save
  through **Save to GitHub**. Remote state remains unverified.

## Supplied source documents
Unmodified copies are in `/app/memory/specifications/`:
- `product.md` — uploaded Ihyaa PRD.
- `technical.md` — uploaded technical specifications.
- `evidence.md` — content/evidence strategy.
- `monetization.md` — monetization/GTM plan.
- `strategy.html` — blue-ocean strategy document.

The documents mix target requirements and assertions about past implementation, contain
inconsistent model names/pricing, and do not prove features exist or are clinically verified.
Use inspected code and test results for implementation status. EN/ID-only user instruction
overrides old trilingual text. The entire document roadmap is NOT complete in this milestone.

## Architecture
- **Frontend:** Expo SDK 54, React Native, TypeScript, Expo Router; native-first, Expo Web
  preview on supervisor port 3000. Preserve this architecture (no Vite/Supabase migration).
- **Backend:** FastAPI, Motor/MongoDB, supervisor port 8001; all APIs under `/api`.
  Mongo config from `backend/.env` `MONGO_URL` / `DB_NAME` only.
- **API URL:** `process.env.REACT_APP_BACKEND_URL`, injected for Expo with
  `frontend/babel.config.js` and `babel-plugin-transform-inline-environment-variables`.
  The former EXPO_PUBLIC_BACKEND_URL key is retained in env but no longer used by API client.
- **Auth:** existing email/password JWT, bcrypt, refresh, email lockout, managed Google login.
  Secrets remain environment-only. Private test accounts: `memory/test_credentials.md`.
- **Design:** existing Outfit/pine/terracotta/warm-paper system; native controls and testID.
  Desktop preview intentionally uses a centered 460px phone-width layout. Light/dark retained.
  Tajawal UI font loading removed; Amiri preserved for scripture/brand text.
- **AI:** `backend/ai_provider.py` adapter uses the approved emergentintegrations streaming
  interface. `COACH_PROVIDER=openai`, `COACH_MODEL=gpt-6-luna`, `EMERGENT_LLM_KEY` server-only.
  No automatic provider/model fallback and no DeepSeek/Gemini/Jev integration in this batch.

## Previously implemented (some still need end-to-end revalidation)
- Register/login/refresh/logout/me, Google-session exchange, password reset token groundwork.
- 9-step onboarding, goals/preferences, 30-day challenge generation, daily habits/evidence,
  points, check-in, streaks, progress, rewards redeemed for Pro, light/dark profile.
- Plan calendar, local native reminders, .ics export, knowledge library.
- 100-day/year curriculum and milestones, Pro-gating, prayer engine with AlAdhan monthly
  cache, method/school settings, location groundwork, streak grace logic.
- Health calculation foundation in `health.py`, 97 combined templates including lifestyle
  pool, library recipes/supplements/exercises/mind modules and hydration endpoints.
- Previous `LIFESTYLE_TEMPLATES` undefined import is resolved: compile/Ruff checks pass.
- Existing health/profile and recipe library endpoints returned valid JSON in current tests.
  This does not certify health logic, all contraindications or frontend health onboarding.

## Implemented and verified — 5 Oct 2026: ChatGPT + EN/ID milestone
### Real ChatGPT wellness coach
- Replaced the old Claude coach routes with modular `coach.py`, `coach_safety.py`, and
  `ai_provider.py`. Real GPT-6 Luna responses verified via public API and browser, EN and ID.
- `/api/coach/config`: configured provider/model, consent version and message limits, no keys.
- `/api/coach/consent`: explicit versioned accept/revoke, stored with user.
- `/api/coach/sessions` GET/POST; `/api/coach/history?session_id=...`;
  `/api/coach/sessions/{session_id}` DELETE, ownership checks on all session operations.
- `/api/coach/chat` JSON-framed SSE meta/delta/done/error, proxy buffering disabled.
  `/api/coach/chat-sync` compatibility endpoint uses the same stream engine, requires session ID.
- Mongo `coach_sessions`, session-scoped `coach_messages`, TTL-backed `coach_usage`.
  UUID session IDs; startup idempotently migrates old unsessioned conversations.
- Latest 12 messages supply bounded context (not the original earliest-40 history bug).
  Latest 200 messages per conversation display in chronological, deterministic order.
- Only complete successful turns saved. Per-session timed locks, 10 requests/minute per user,
  2,000-character message limit, 100-conversation limit, timeout and sanitized error handling.
- Medical/emergency/religious requests recognized by local deterministic rules get local
  safety referrals, not fabricated AI responses. Prompt adds non-medical/non-fatwa boundaries.
  This is a conservative initial safety layer, NOT Jev or a clinically validated classifier.
- Provider profile context is explicitly allowlisted: safe goals, fitness and sleep pattern,
  selected language. No saved name/email/conditions/metrics/location sent as profile context.
  Basic identifier redaction also applied to chat payloads; free-text redaction is not a
  guarantee of de-identification. User is warned not to include sensitive information.
- No plan mutation/tool execution, no unverified clinical citations or scholar-review claims.
  AI responses are suggestions, not medical advice or religious rulings.
- Frontend: streaming with expo/fetch, saved conversation picker, new/delete confirmation,
  consent/revocation, model label, safety labels, retry/error states, health-first suggestions.
  Supporting modules live under `frontend/src/coach/`.

### English / Indonesian only
- Runtime Lang type, selectors, dictionaries, date/font/layout branches now EN/ID only.
  Old Arabic UI translations archived in a source comment, not included in runtime dictionary.
  Existing backend translation data retained but Arabic is inaccessible via language APIs.
- Registration/profile/onboarding/coach language and localized query validation reject `ar`.
- Startup normalizes historical unsupported user languages to EN; model validator and local
  storage normalizer protect against legacy values. No forced RTL.
- Profile language changes persist immediately (no extra Save), synchronize after login,
  survive reload/sign-out/sign-in. This corrects the previously unverified persistence bug.

### Authenticated reload bug found and fixed
- Test iteration 2 found blank profile content after switching to ID and reloading.
- Root cause: profile initialized prefs from a not-yet-hydrated user and returned null forever.
- Added `SessionGate` for tabs/coach, profile state synchronization, and explicit bootstrap
  loading/error/retry behavior. Auth bootstrap no longer silently renders empty content on
  transient profile-loading failures. Password/token protocols remain unchanged.
- Verified desktop EN→ID reload, mobile reload, re-login language persistence, simulated
  bootstrap outage/retry recovery, and coach deletion after a real Indonesian streamed reply.

## Test evidence
- `/app/test_reports/iteration_2.json`: original testing report, 15/15 targeted backend tests;
  records the then-open frontend reload bug (subsequently resolved, retained for audit trail).
- `/app/backend/tests/test_coach_integration.py`: live model SSE, conversation memory/isolation,
  access controls, consent persistence, safety referrals, private-context allowlist,
  language/input validation, concurrent request lock, rate limit, library/health JSON.
- `/app/test_reports/iteration_2_followup.md`: main-agent post-fix verification results.
- `yarn tsc --noEmit`, Python compileall and Ruff F checks passed after fixes.
- Desktop **1920×800** and mobile **390×844** screenshots: zero horizontal overflow.
- No mocked application integrations. The bootstrap-failure browser check used a temporary
  test-only intercepted 503 response, removed before retrying against the real backend.
- Native iOS/Android streaming/keyboard/reminder behavior not device-tested.

## Prioritized remaining work
### P0 — next product milestone
1. Complete health-profile questionnaire and safety/consent UX, health-first Today/library
   screens, materially contrasting-profile plan tests. Review calorie/fluid/supplement guidance
   for minors, pregnancy, CKD, diabetes, anticoagulants, eating disorders and other risks.
2. Evidence provenance, DOI/retraction validation, explicit source grading and scholar/clinical
   review workflow. No professional review or clinical validation completed by this milestone.
3. Regression-test prayer GPS/manual city/method/Asr, persistence, reminders and .ics anchors;
   advanced track phases/milestones/Pro gating; exact 1 grace day per 7 days edge cases.
4. Address documented credential-publication risk before any public release. Private credential
   inventory updated for test accounts, but remote history/exposure and credential rotation
   were not changed or verified. Do not publish private credential files.

### P1
- Native-device coach streaming, cancellation/retry and long-history pagination.
- Expanded EN/ID safety evaluation corpus and provider-failure tests; current guardrails are
  not a substitute for professional review or an output-validation/retrieval system.
- Confirmed, allowlisted plan-change proposals (two-stage validation) rather than auto-execution.
- Health library citations/contraindications, structured recipes and daily hydration UI.
- Server push and recurring jobs (load scheduled-recurring-tasks skill before implementation).
- App analytics/crash monitoring and native build profiles after integration requirements gathered.
- Extract remaining backend server routes into smaller modules incrementally.

### P2 / larger document roadmap
- Jev decision layer, bandit reminder optimization, embeddings/vector recommendations.
- Reviewed alternate-provider fallback (privacy/data-residency requirements apply).
- Ramadan mode, offline support, family profiles, wearables, opt-in community.
- Subscriptions/payments, trials and pricing implementation; no billing integration added.
- Vendor-decoupling and own OAuth/storage services require separate approved integration work.
- Google Calendar two-way sync remains dependent on separate OAuth credentials.

## Known limitations / next actions
- ChatGPT integration and EN/ID milestone are verified in preview, not the entire document plan.
- App AI remains through the Emergent service as approved; independence/alternate providers are
  not claimed. Model cost estimates from uploaded documents have not been independently verified.
- Coach cannot edit plans or diagnose, certify products halal, or supply verified source evidence.
- Local reminders native-only; Google auth needs a real Google account for manual verification.
- Password-reset email delivery is not configured (existing token/log groundwork only).
- Neither requested GitHub branch has been pushed. User-controlled Save to GitHub is next.
- Suggested enhancement: reviewed, one-tap “add this small habit” proposals with explicit confirmation.