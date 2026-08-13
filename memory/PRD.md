# Ihyaa (إحياء) — Product Requirements & Build Log

## Original problem statement (verbatim, 13 Aug 2026)
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
> The App name: Ihyaa (إحياء) — "Revival".

## User choices captured
| Question | Answer |
|---|---|
| Platform | Native mobile — **Expo / React Native** (previewed via Expo Web on port 3000) |
| Auth | Email + password (JWT) **and** Emergent-managed Google sign-in |
| Calendar | In-app schedule + local push reminders + `.ics` export. Full Google Calendar 2-way sync **deferred** (needs user's Google OAuth Client ID/Secret) |
| Content | Curated fixed 30-day curriculum in DB **and** AI coach chat |
| Points | Redeem for Ihyaa Pro only, no real payments |
| AI model | User asked for "Deepseek Flash" — **not available** via Emergent Universal Key. Using **Claude Sonnet 4.6** (`COACH_MODEL` in `backend/.env`, swappable) |

## Architecture
- **Frontend**: Expo SDK 54 + expo-router (file-based). `/app/frontend/app/*` routes, `/app/frontend/src/*`
  shared code. Runs as a real iOS/Android app via EAS and as Expo Web for browser preview.
  Constrained to a 460px centred column on web so the desktop preview reads as a phone.
- **Backend**: FastAPI + Motor/MongoDB, every route under `/api`. Bearer JWT (1-day access,
  30-day refresh) plus cookies for the web path.
- **Design system**: `/app/design_guidelines.json`. Deep pine `#1B3B36` + terracotta `#B5653E`
  on warm paper `#F7F5F0`; Outfit (Latin) / Tajawal (Arabic UI) / Amiri (scripture); 8-point
  khatam star SVG tessellation at low opacity as the Islamic accent. Light + dark themes.
- **Pillar colours**: body `#B5653E`, food `#D99B29`, mind `#4A6FA5`, soul `#2A9D8F`.

## Core requirements (static)
1. Every habit must carry Quran / hadith grounding **and** a peer-reviewed clinical citation.
2. Nothing contested: no yoga mantras, no music-dependent workouts, no doubtful supplements,
   no fiqh-clashing fasting protocols. 100% halal by construction.
3. "1% better": day 1–3 = 2 tiny tasks, day 4–10 = 3, day 11+ = 4. Duration ramp 0.45× → 1.0×.
4. Trilingual: English, Bahasa Indonesia, Arabic (with RTL text handling).
5. Habits are anchored to prayer times (Fajr/Dhuhr/Asr/Maghrib/Isha/night), shifted by the
   user's sleep habit.
6. Plans are always adjustable — changing preferences re-plans the *future* only.

## What's implemented — 13 Aug 2026 (v1)
- **Auth**: register / login / refresh / logout / me, bcrypt, email-keyed brute-force lockout
  (5 tries → 15 min), password reset tokens, Emergent-managed Google sign-in (web redirect +
  native `openAuthSessionAsync`).
- **Onboarding**: 9-step wizard (language → welcome → name → fitness → goals → diet → sleep →
  spiritual level → track) that generates the personalised plan on finish.
- **Curriculum**: 40 trilingual task templates (10 per pillar) in `backend/curriculum.py`, each
  with title, description, Quran and/or hadith reference and a journal-cited science note.
- **Plan engine**: deterministic `generate_plan()` — goal-weighted pillar priority, level
  gating, 1%-better task count + duration ramp, prayer-anchored reminder times.
- **Today screen**: greeting, streak + points chips, concentric per-pillar progress rings,
  Day X of 30 bar, expandable habit cards with the three evidence blocks, tap-to-complete.
- **Plan tab**: 42-day horizontal strip auto-scrolled to today with per-day completion dots,
  day detail, local push reminders (native only) and `.ics` export (web download / native share).
- **Progress tab**: completion ring, streak / best / points / check-ins stats, pillar bars,
  7-day chart.
- **Daily check-in**: mood + energy 1–5, gratitude + reflection notes, 15 pts, streak logic,
  +100 pts every 7-day streak, one per day (unique index).
- **Points & Rewards**: +10–24 per habit, +50 for a full day (once-per-day marker, un-farmable),
  three Pro items (2 500 / 6 000 / 18 000 pts) redeemed atomically, transaction ledger.
- **Pro gating**: 100-day and 1-year tracks return `402 pro_required` for free users;
  onboarding silently falls back to 30 days.
- **AI Coach** ("Ustadh Ihyaa"): Claude Sonnet 4.6 via Emergent Universal Key, multi-turn
  history in Mongo, user-context injection (streak, level, today's tasks), halal + non-medical
  guardrails in the system prompt, replies in the user's language.
- **Knowledge library**: 8 trilingual cards, pillar filter, expandable evidence.
- **Profile**: language switch, light/dark theme, full preference editing, plan rebuild, sign out.

### Verified fixes from test iteration 1
- Lockout keyed on email (ingress rotates client IPs) — 5 failures now return 429.
- `X-Refresh-Token` header takes precedence over an ambient cookie.
- All-tasks +50 bonus is claimed once per day via a unique `daily_bonuses` marker.
- `start_date` and `scheduled_time` are validated (422 instead of 500).
- Explicit CORS origins + regex, `allow_credentials` on.
- Store catalogue localises from the live i18n language, not the saved profile.
- Coach bubbles render `**bold**`; prompt now forces plain text and <120 words.

## Prioritised backlog
### P0 — next
- **100-Day and 1-Year curricula**: extend `TEMPLATES` (target ~90 templates) so Pro tracks are
  not just longer loops of the 30-day pool. Add phase themes (foundation → depth → mastery).
- **Push notification scheduling on the server** so reminders survive app reinstalls, plus
  Expo push tokens for streak-risk nudges ("your streak ends in 4 hours").
- **Google Calendar 2-way sync** — blocked on the user supplying a Google OAuth Client ID/Secret.

### P1
- Prayer-time API (e.g. Aladhan) keyed to the user's city so anchors use *real* adhan times
  instead of the current fixed clock defaults.
- Streak freeze / "one bad day doesn't reset you" grace mechanic.
- Habit history per template (how many times done, personal best) and a shareable 30-day
  completion certificate.
- Dhikr counter and hydration tracker as first-class in-app tools.
- Arabic layout mirroring via `I18nManager.forceRTL` on native (currently text-direction only).

### P2
- Community / halaqah: private groups, friendly leaderboards, du'a wall.
- Real payments for Pro (Stripe) alongside points redemption.
- Ustadh review workflow so a real scholar can approve every new template before release.
- Apple Health / Google Fit import for steps and sleep.
- EAS build + App Store / Play Store submission pipeline.

## Known limitations
- Local push reminders are native-only; the browser preview shows an explanatory message.
- Prayer anchor times are sensible defaults, not real calculated adhan times yet.
- Google sign-in cannot be exercised in automated tests (needs a real Google account).
