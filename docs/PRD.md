# Ihyaa — Product Requirements Document (PRD)

_Updated 28 Sep 2026. "Current state" below is verified against `preview-dev` commit 912cb9a. Anything planned is labeled. Companion docs: TECH_SPEC.md, CONTENT_EVIDENCE.md, MONETIZATION_GTM.md, VERIFICATION.md (correction ledger + sources)._

## 0. Verified current state

**Shipped and working:**
- Auth: register/login/refresh/logout, JWT (1d access/30d refresh), bcrypt, email-keyed lockout (5 tries → 15 min), Google sign-in via Emergent-managed session exchange
- Onboarding: 9-step wizard (language, welcome, name, fitness, goals, diet, sleep, spiritual, track) → generates a personalized plan
- Plan engine: deterministic scheduler, goal-weighted pillar priority (spiritual always first-class), 1%-better ramp (2→5 tasks/day), phase-gated levels, health-flag filtering, per-user seeded ordering
- Today screen: greeting, streak, points, pillar progress rings, expandable habit cards with Quran/hadith/science references
- Plan tab: 42-day strip, per-day dots, local reminders, .ics export (35 days)
- Progress tab: completion ring, streak/best/points stats, pillar bars, 7-day chart
- Daily check-in: mood + energy 1–5, gratitude, reflection
- Points & Store: per-habit points, insert-once daily bonuses (anti-farm), redeem points for Pro (2500/6000/18000)
- Pro gating: 100-day and 1-year tracks require Pro
- AI Coach "Ustadh Ihyaa": Claude Sonnet 4.6 via Emergent, multi-turn, halal/non-medical system prompt
- Knowledge library: 8 trilingual cards; lifestyle library: 14 recipes, 8 exercise routines, 6 mind windows
- Prayer times: AlAdhan + monthly MongoDB cache, per-user method/school, city search
- Trilingual EN/ID/AR with RTL; design system (deep pine + terracotta) in `design_guidelines.json`
- Test iteration 1 fixes landed: email-keyed lockout, header-precedence refresh, bonus anti-farm, challenge validation, CORS env config

**Not built (previously misdescribed as done):**
- DOI evidence registry and retraction checking — zero records exist
- Hadith grading metadata and scholar review — no field, no reviewer
- Contraindication severity levels (info/warning/block) — lifestyle flags only; no CKD/T1DM/pregnancy/anticoagulant support
- Any payment rail — points-only economy
- EAS build profile, analytics, crash reporting
- Backend independence from Emergent

## 1. Vision

Ihyaa (إحياء, "revival") is a mobile health companion that unifies habit tracking, food/lifestyle planning, and Islamic guidance. The thesis: Muslim habit apps are spiritual checklists; fitness apps carry no halal framing; Ihyaa occupies the intersection with Body-first sequencing (physical + nutrition), Quran/Hadith grounding on every habit, and clinically-cited science notes — with Mind/Soul integrated, not bolted on.

**Tagline**: "Sehat itu ibadah."

## 2. Problem

1. **Fragmentation** — Muslims managing health juggle 3–4 apps; nothing unites them.
2. **Missing Islamic context** — mainstream health apps ignore Ramadan, prayer times, halal food, the Hijri calendar.
3. **Missing scientific context** — Islamic apps say "this is sunnah" without the medical why.
4. **Motivation decay** — habit trackers rely on streaks/badges; Ihyaa adds intrinsic religious framing (health as amanah).

**Personas**: primary Muslim Health Seeker (25–45, urban, wants health + ibadah value); secondary Ramadan Improver (seasonal spike, post-Eid churn); tertiary Family Health Manager (manages household health).

## 3. Core loop & differentiators

Open app → Today plan → complete habits → feedback (progress + evidence + pahala framing) → streak/weekly summary → repeat.

Competitive wedge (vs Muslim Pro / MyFitnessPal / generic trackers): unified Islamic-health framing, per-habit Quran/Hadith + science citations, Hijri-aware scheduling, health-flag safety layer, trilingual AR/RTL. The **intended** moats post-Phase-E: structured evidence registry + scholar review as a standing process, and a contraindication layer general health apps have no reason to build. These are roadmap commitments, not current state.

## 4. Feature set

**Phase 1 (exists)**: today screen, habit tracker across 4 pillars (97 templates), meal/lifestyle library, inline evidence on every card, prayer-anchored scheduling, onboarding, points economy, AI coach.

**Phase 2**: Ramadan mode (sahur/iftar planning, tarawih tracking, Laylatul Qadr countdown, zakat calculator, post-Eid transition), family plan (5 profiles, shared meal plans, kids tracking with parental controls), community (anonymous sharing, mosque groups, challenges), Health Connect wearable sync, E-1 evidence registry + API, E-2 contraindication severity upgrade, real-money subscription w/ 14-day trial.

**Phase 3**: AI personalization upgrade (GPT-6 Luna primary / DeepSeek Flash fallback with structured-output guardrails and safety routing), Thompson-sampling reminder timing, embedding-based habit recommendation, adaptive plan adjustment with user confirmation.

## 5. Success metrics

North star: **DAU completing ≥3 habits/day.**

| Metric | 12-mo target |
|---|---|
| Downloads | 50,000 |
| D30 retention | 35% |
| Habits/DAU/day | 4.5 |
| Free→paid conversion | 8% |
| Monthly churn | < 5% |
| NPS | > 50 |

All projections labeled as such; no traction numbers exist yet — deck uses placeholders.

## 6. Non-negotiables

1. No Islamic content ships without scholar review once grading pipeline exists; today's inline citations stay conservative in wording.
2. Medical disclaimers on all health recommendations; the app never replaces a doctor.
3. Privacy-first: health data minimized, transparent policy (UU PDP compliant: export + deletion).

## 7. Positioning

Untuk Muslim yang ingin hidup sehat, Ihyaa adalah health companion yang menyatukan habit tracking, nutrition planning, dan bimbingan Islami dalam satu app — karena sehat itu ibadah, dan ibadah itu bisa sehat.

**Sequencing (user-confirmed)**: Android first via Expo/EAS, Play internal testing before iOS; Indonesia-first beachhead; Arabic content already present but no new Arabic authoring for now; investor deck with explicit placeholders — no fabricated numbers, ever.
