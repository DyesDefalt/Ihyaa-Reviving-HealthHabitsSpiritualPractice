# Ihyaa (إحياء) — Reviving Health, Habits & Spiritual Practice

**Sehat itu ibadah.** — "Health is worship."

Ihyaa is a mobile health companion for Muslims that unifies habit tracking, food & lifestyle planning, and Islamic guidance in one app. Every habit carries Quran/Hadith grounding plus a clinical science note. Prayer times anchor the daily schedule — habits schedule around salah, not the other way around.

## What's built (verified, not vibes)

- **97 habit templates** across 4 pillars — physical (26), nutrition (30), spiritual (17), mental (24) — trilingual EN / ID / AR with full RTL
- Deterministic plan engine: goal-weighted pillar priority, "1% better" ramp (2→5 tasks/day), phase-gated difficulty, health-flag filtering
- Prayer-anchored scheduling via AlAdhan API with whole-month MongoDB caching (per-user method + madhab)
- Auth: JWT + bcrypt, email-keyed brute-force lockout, Google sign-in
- Points economy: earn per habit, daily bonuses (insert-once anti-farm), redeem for Pro (100-day & 1-year tracks)
- AI coach "Ustadh Ihyaa" — halal + non-medical guardrails, multi-turn history
- Knowledge library (8 cards), recipes (14), exercise routines (8), mind windows (6)
- Daily check-ins, streaks, milestones, .ics calendar export, hydration tracking
- Light/dark themes, deep pine + terracotta design system

**Honest gaps** (in active build, see `docs/`): DOI evidence registry and scholar-review pipeline are under construction — citations are inline today. See `docs/VERIFICATION.md` for the full correction ledger separating measured reality from plan.

## Stack

| Layer | Tech |
|---|---|
| Frontend | Expo SDK 54 + expo-router 6 + TypeScript (React 19.1 / RN 0.81.5) |
| Backend | FastAPI + Motor/MongoDB |
| Auth | JWT (1d access / 30d refresh) + bcrypt + lockout; Google OAuth |
| AI coach | Claude Sonnet 4.6 via Emergent today → **GPT-6 Luna** primary + **DeepSeek V4.1-Flash** fallback post-decouple |
| Prayer times | AlAdhan API v1, monthly cache, Kemenag method supported |

## AI model decision

**GPT-6 Luna** (`gpt-6-luna`) primary, **DeepSeek V4.1-Flash** (`deepseek-flash`) fallback. Chosen for cheap + reliable on the most current models:

- GPT-6 Luna: $0.10 / $0.50 per 1M tokens — cheapest current-gen OpenAI, strong Bahasa Indonesia, no peak-hour pricing
- DeepSeek V4.1-Flash: $0.15–0.30 / $0.60–1.20 per 1M, 50% off-peak discount, different infrastructure for genuine failover
- At 10K DAU the coach costs ~$15–30/month total — cents per paying user

## Getting started

Backend (Python 3.11+):

```bash
cd backend
pip install -r requirements.txt
# required env: MONGO_URL, DB_NAME, JWT_SECRET, EMERGENT_LLM_KEY,
#               CORS_ORIGINS, ADMIN_EMAIL/PASSWORD, DEMO_EMAIL/PASSWORD
uvicorn server:app --reload
```

Frontend:

```bash
cd frontend
npm install
# required env: EXPO_PUBLIC_BACKEND_URL=http://localhost:8000
npx expo start
```

Health check: `GET /api/health`.

## Project docs (`docs/`)

- `MASTER_PLAN.md` — one-page plan, phase order, targets
- `PRD.md` — product requirements with verified current-state split
- `TECH_SPEC.md` — architecture, data model, endpoints, security gaps
- `CONTENT_EVIDENCE.md` — evidence pipeline build order (DOI registry → contraindication severity → scholar review)
- `MONETIZATION_GTM.md` — pricing (Rp49k/mo, Rp349k/yr), paywall rules, GTM phases
- `VERIFICATION.md` — correction ledger: every metric measured against the codebase, external facts with sources

## Roadmap (short version)

1. **Security & independence** — rotate credentials, decouple from Emergent (~1 day), Sentry
2. **Ship readiness** — Expo SDK 57 upgrade (settles the Play Store API 36 requirement), EAS profiles, internal testing track
3. **Evidence layer** — citation audit → `evidence_records` registry → contraindication severity (pregnancy, diabetes fasting, CKD, anticoagulant) → hadith scholar review
4. **Monetization** — real-money subscriptions (14-day card-free trial), closed beta with D7 > 30% gate
5. **Growth** — Ramadan mode, mosque partnerships, post-Ramadan retention, family plan

Android first, Indonesia first. iOS after Play Store validation.

## Status

Solo project, active development on the `preview-dev` branch. Planning docs live on `hermes-update` and merge forward. No content ships without source verification; no numbers in docs without measurement.
