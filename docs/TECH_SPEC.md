# Ihyaa — Technical Specifications

_Updated 28 Sep 2026. Numbers in this document are measured from `preview-dev` (commit 912cb9a) unless labeled "planned". See `VERIFICATION.md` for the correction ledger and external sources._

## 1. Architecture — verified current state

**Frontend**: Expo SDK 54 + expo-router 6 + TypeScript. React 19.1, RN 0.81.5. File routes in `frontend/app/` — tabs: Today, Plan (calendar), Progress, Store, Profile; plus checkin, coach, knowledge, onboarding, sign-in. State = AsyncStorage + expo-secure-store + in-module tokens; no Zustand/Redux. API client `src/api.ts`: fetch wrapper, Bearer auth, auto single retry after 401 refresh.

**Backend**: FastAPI 0.110 + Motor 3.3 / MongoDB. `server.py` (1,164 lines) + modules: `auth.py` (144), `content.py` (213), `curriculum.py` (1,023), `library.py` (600), `milestones.py` (275), `prayer.py` (170), `health.py` (113), `models.py` (291), `templates_advanced.py` (448), `templates_lifestyle.py` (445). JWT access 1 day / refresh 30 days, bcrypt, email-keyed lockout (5 tries → 15 min), insert-once daily-bonus anti-farm markers, CORS via `CORS_ORIGINS`/`CORS_ORIGIN_REGEX` env.

**AI Coach** ("Ustadh Ihyaa"): `claude-sonnet-4-6` via `emergentintegrations.llm.chat.LlmChat` + Emergent's custom `litellm` wheel. Model/provider swappable through `COACH_PROVIDER`/`COACH_MODEL` env vars. Multi-turn history in MongoDB. System prompt enforces halal + non-medical framing.

**Prayer times**: AlAdhan API v1, whole-month MongoDB cache keyed on (lat, lng, method, school, year, month), method id per-user (default 3), school 0=Shafi'i / 1=Hanafi, Nominatim city search.

**Design system**: `design_guidelines.json` — deep pine `#1B3B36` primary, terracotta `#B5653E` secondary, warm paper `#F7F5F0` background, light+dark themes, pillar colors (physical/nutrition/mental/spiritual), full spacing/radii/shadow/RTL guidelines.

**Trilingual**: every content string via `T(en, id, ar)` — templates, library, knowledge cards, store items. RTL support through I18nManager.

### Content inventory (measured)

| What | Count | Where |
|---|---|---|
| Habit templates | **97** (physical 26, nutrition 30, spiritual 17, mental 24) | curriculum 40 + advanced 28 + lifestyle 29 |
| Knowledge cards | 8 | `content.py` |
| Recipes | 14 | `library.py` |
| Exercise routines | 8 | `library.py` |
| Mind windows | 6 | `library.py` |
| Milestones | weekly/monthly per track | `milestones.py` |

## 2. The one blocker: Emergent decoupling (P0)

Backend cannot run outside the Emergent platform. Replacement plan:

| Dependency | Replacement | Est. effort |
|---|---|---|
| `emergentintegrations` package (LLM + Google auth) | Direct OpenAI/Anthropic SDK + own Google OAuth client | ~2 h |
| `litellm` custom wheel (URL-pinned) | Standard `litellm` from PyPI | ~1 h |
| Emergent Google OAuth (`/api/auth/google/session`) | Own Google OAuth 2.0 client id/secret | ~3 h incl. console |
| Emergent MongoDB | Atlas free tier (0.5 GB; note: no backups, 30-day idle auto-pause) | ~1 h |
| Emergent hosting | Railway / Render / Fly.io | ~2 h incl. Dockerfile |

~1 focused day total. This blocks: EAS builds, Play Store submission, any independent hosting.

## 3. AI model plan (prices verified 28 Sep 2026)

Current: Claude Sonnet 4.6 via Emergent. Target after decoupling — provider abstraction with fallback chain:

| Role | Model | In / out per 1M | Note |
|---|---|---|---|
| Primary coach | **GPT-6 Luna** (`gpt-6-luna`) | $0.10 / $0.50 | **Chosen.** Cheapest current-gen OpenAI, reliable infra, good Bahasa Indonesia. Batch $0.05/$0.25. Prioritizes cheap + reliable on the most current model |
| Fallback | **DeepSeek V4.1-Flash** (`deepseek-flash`) | $0.15–0.30 / $0.60–1.20 | **Chosen.** Off-peak (all hours except Mon–Fri 01:00–04:00, 06:00–10:00 UTC) is 50% off. Different infra = genuine failover |
| Alternative | Claude Sonnet 5 | $2.00 / $10.00 | Only if OpenAI quality dips; cheaper than the current Sonnet 4.6 |
| Rejected | Gemini 3.8 Flash | $0.75 / $3.75 | Not a budget model — earlier $0.10/$0.40 assumption was wrong. Off the plan |
| Rejected | GPT-5.6 Luna | $0.20 / $1.20 | Superseded by GPT-6 Luna at half the price |
| Intent/scoring (Phase 3) | Jev (TypeSafe AI) | $0.042 direct / $0.42 hosted per 1M in, output free | Decision layer only — no text generation |
| Intent/scoring fallback (Phase 3) | **Laya** (`laya`, Apache 2.0, self-hosted) | Free (compute only) | Open-source System-1 decision engine, same request format as Jev (choice/score/noul), 33 ms. Zero-shot accuracy is near chance — **fine-tune on Ihyaa decision sets before routing real traffic** (fine-tuned benchmark 0.766 > Jev's 0.727; zero-shot 0.36). ~4–5 h on free Kaggle T4s |

Cost at 10K DAU × 10 msgs/user/mo ≈ 100K conversations × 2K in + 300 out: **~$15–30/month on GPT-6 Luna**. Negligible vs Rp49k/mo subscription. Embeddings: `text-embedding-3-small` $0.02/1M confirmed.

```python
# ai_provider.py — planned shape
PROVIDERS = [
    {"name": "openai", "model": "gpt-6-luna", "priority": 1},
    {"name": "deepseek", "model": "deepseek-flash", "priority": 2},
]
async def chat(messages, **kw):
    for p in PROVIDERS:
        try:
            return await call(p, messages, **kw)
        except (RateLimitError, ServiceUnavailable, Timeout):
            continue
    raise AllProvidersFailed()
```

## 4. Platform requirements & the API 36 problem

- **Google Play now requires new apps and updates to target Android 16 (API 36)** as of 31 Aug 2026 (extension request possible to 1 Nov 2026). Whether an Expo SDK 54 build can override `targetSdkVersion` to 36 is unverified — assume a **SDK 57 upgrade** is needed.
- Expo SDK 57 (current stable, RN 0.86, React 19.2) is a small release; SDK 54 is 3 majors behind and exits its critical-fixes window at the next SDK release (~Sep/Oct 2026).
- `expo-notifications` is not deprecated; local notifications remain available; Android push requires a development build (not Expo Go) since SDK 53.
- Internal testing track **exempts** the Data safety form; promotion to closed/open/production requires it plus a hosted privacy policy.

**Decision: upgrade to SDK 57 as part of Android ship readiness**, not just API 36 patching — avoids doing it again in 3 months.

### eas.json (to add)

```json
{
  "build": {
    "development": { "developmentClient": true, "distribution": "internal" },
    "preview": { "distribution": "internal", "android": { "buildType": "apk" } },
    "production": { "android": { "buildType": "app-bundle" } }
  }
}
```

EAS Submit supports `"track": "internal"` for the internal-testing track. `releaseChannel` is obsolete; use `channel` if EAS Update is adopted.

## 5. Data model (live collections from models.py)

`users` (embedded `Preferences`: fitness level, goals, diet, sleep, spiritual level, challenge, reminders, prayer method/school, location, age/sex/height/weight, conditions, work pattern, wake time) · `challenges` · `daily_tasks` (template_key, pillar, day_number, scheduled_date/time, anchor, duration, difficulty, points, completed) · `milestones` · `checkins` (UNIQUE user+date) · `point_transactions` · `coach_messages` · `prayer_months` (cache) · `login_attempts` · `daily_bonuses` (UNIQUE user+date+kind) · `hydration` (UNIQUE user+day) · `user_sessions`.

### Collections to add (Phase 2 — evidence & safety build)

`evidence_records` (template_key, type clinical_doi|quran|hadith|scholar, doi, journal, year, finding, level, retracted, source text/translation, grading, review_status/by/at) · `contraindications` (template_key, condition, severity info|warning|block, message, alternative) · push tokens · notification log. These do **not** exist today — see Content & Evidence Strategy for the build plan.

## 6. Plan engine (measured behavior)

- `tasks_for_day`: day 1–3 → 2 tasks, 4–10 → 3, 11–40 → 4, 41+ → 5. 365-day plan = 1,772 tasks.
- `pillar_priority`: goals add weight to pillars (GOAL_PILLAR_WEIGHT), spiritual always +1. Default-profile 1-year plan: 39% spiritual / 20% physical / 20% nutrition / 20% mental → **41% body share**, not 81%.
- Pool rotation: per-pillar pools sorted best-fit-first, round-robin by counter; a new phase jumps to just-unlocked templates. Measured worst repeat gap on 1-year plans: **30–49 days** across seeds (target: 60).
- Phase-gated levels with `level_cap()`; 30-day track uncap at 3.
- Health flags (from `health.py`): diabetes → no_fasting/glucose_focus/low_sugar; hypertension → bp_focus/low_sodium/no_hiit; joint/obese → joint_friendly/no_jump; age ≥ 55 → joint_friendly/balance_focus; desk/shift work flags; plus contraindication exclusion via `contra` tags.

## 7. Endpoints (30 routes verified in server.py)

Auth: register, login, refresh, logout, me, forgot/reset-password, google/session · profile, profile/location, onboarding · challenges, challenges/active, challenges/regenerate · tasks/today, tasks, tasks/{id}/complete, tasks/{id}/time, tasks/calendar.ics · library/{kind}, knowledge, milestones, milestones/{id}/complete · hydration/today, hydration · prayer/today, prayer/methods, cities/search · checkins/today, checkins · progress/summary · points/transactions · store/items, store/redeem/{item_id} · coach/chat, coach/chat-sync, coach/history · health.

Planned (Phase 2): evidence/{templateKey}, ramadan/mode, fasting/log, push/register, personalize/score, analytics/summary.

## 8. Security gaps (before production)

1. **Rotate test credentials + purge git history (public repo, live since 13 Aug).** Shortest path: rotate passwords, `git filter-repo` or fresh orphan branch, force-push.
2. MongoDB auth + TLS (currently localhost-trust).
3. Rate limiting beyond login.
4. Field-level encryption for `conditions[]`.
5. Data-export + account-deletion cascade (UU PDP).
6. Sentry + error boundaries before Play Store.
7. AI guardrails are prompt-level today — add structured-output validation + medical/religious refusal routing when the provider layer is rewritten.

## 9. Performance targets (unchanged, tests pending)

Launch < 2 s · Today < 500 ms · completion tap < 100 ms · app < 50 MB · RAM < 150 MB.
