# Ihyaa — Master Plan (28 Sep 2026)

One page. Everything else links out. Every number here is code-verified (see `docs/VERIFICATION.md`) or labeled as plan.

## Where we actually are

Working app on `preview-dev`: Expo SDK 54 / FastAPI+Mongo backend, 97 trilingual habit templates, plan engine with measured 30–49-day worst-case repeat gap, prayer-anchored scheduling, points economy, Claude Sonnet 4.6 coach via Emergent, 8 knowledge cards + lifestyle library, iteration-1 security fixes landed.

Not built, despite earlier docs: DOI evidence registry (0 records), hadith grading + scholar review (no reviewer, no date), contraindication severity layer (lifestyle flags only), payment rail, EAS profile, analytics.

Three hard blockers:
1. **Credentials in public repo since 13 Aug** — rotate + purge today.
2. **Emergent lock** — ~1 day to decouple (LLM, OAuth, MongoDB, hosting).
3. **Play Store now requires target API 36** (since 31 Aug 2026) — SDK 57 upgrade solves it cleanly; SDK 54 is 3 majors stale anyway.

## Phase order

**P0 — Security & independence (this week)**
1. Rotate admin/demo passwords, purge `memory/test_credentials.md` from history, consider repo → private.
2. Emergent decoupling: OpenAI SDK + own Google OAuth + Atlas + Railway/Render.
3. Sentry.

**P1 — Ship readiness (weeks 2–3)**
4. SDK 57 upgrade → EAS build profile (`preview` APK internal / `production` AAB) → Play internal testing track (Data safety form exempt on internal track; do it anyway before closed testing).
5. AI provider rewrite: GPT-6 Luna ($0.10/$0.50 per 1M — verified cheapest current-gen) primary, DeepSeek Flash off-peak fallback. Prompt-level guardrails → structured-output validation.

**P2 — Honest evidence layer (weeks 3–5)**
6. E-0 citation audit: every prose citation gets its DOI or gets its wording downgraded.
7. E-1 `evidence_records` collection + `GET /api/evidence/{templateKey}` + quarterly retraction job.
8. E-2 contraindication severity: pregnancy → diabetes fasting blocks → CKD → anticoagulant, in that order.
9. Name the hadith scholar reviewer + date. Non-code blocker. Shortlist 3 this week.

**P3 — Monetization (weeks 4–6)**
10. Play Billing / RevenueCat, Rp49k monthly / Rp349k annual / Rp549k family, 14-day card-free trial.
11. Closed beta 200 users; D7 > 30% gate before any paid spend.

**P4 — Growth (Ramadan-cycle dependent)**
12. Public launch, Ramadan mode, mosque partnerships, post-Ramadan retention (Shawwal tracker, annual lock-in), family plan + wearables.

## Numbers that matter

| Metric | Current (measured) | 12-mo target |
|---|---|---|
| Habit templates | 97 | ~150 (Phase 2 content) |
| DOI evidence records | 0 | 100% coverage of templates |
| Worst 365-day repeat gap | 30–49 days | 60 days |
| Body share of scheduled tasks | 41% | by design, not 81% — fix narrative |
| Scholar-reviewed hadith | 0 | 100% before any hadith ships unreviewed |
| AI cost @10K DAU | ~$15–30/mo (GPT-6 Luna) | cents per paying user |

## Deck rules (phase 2d, unchanged)

Explicit `[ASK]` / `[TRACTION]` / `[TEAM]` placeholders. Zero fabricated numbers. Evidence claims limited to what exists: "every habit carries Quran/Hadith grounding and a clinical science note; structured DOI registry and scholar review pipeline in build." Lead with Hijri-native scheduling + unified Islamic-health framing + Indonesia beachhead; evidence rigor as supporting roadmap, not shipped fact.
