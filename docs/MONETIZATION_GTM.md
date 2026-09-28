# Ihyaa — Monetization & Go-To-Market Plan

_Updated 28 Sep 2026. Market data points retained only where the underlying source was previously verified; model costs corrected to official Sept 2026 prices (see VERIFICATION.md). Anything unverifiable is marked._

## 1. Business model

Freemium + subscription. Free tier genuinely useful (Islamic-app users expect core religious content free; aggressive paywalls read as exploitative). Premium unlocks depth. Today the app has a **points-only economy**: Pro is earned (2500/6000/18000 points for 1/3/12 months) and no payment rail exists. Real-money subscription is the Phase M-1 build.

## 2. Pricing (Indonesia-first)

Anchors: Netflix ID Rp54k, Spotify ID Rp55k/mo; ChatGPT Go Rp75k. Ihyaa sits below all three.

| Plan | Price (IDR) | Notes |
|---|---|---|
| Monthly | Rp49.000 | Entry |
| Quarterly | Rp119.000 | Save ~20%; fits Indonesian payday cycles |
| Annual | Rp349.000 | Save 40%; annual plans retain materially better than monthly (industry pattern: 2–2.5x at 12 months — validate on own cohort after launch) |
| Family annual | Rp549.000 | Up to 5 profiles |
| Lifetime | Rp999.000 | Launch promo, cap 1,000 users |

Free tier: 5 active habits/day, today screen, prayer times + notifications, water tracker, 7-day history, basic science notes. **No ads ever** (breaks Islamic UX trust).

Pro: unlimited habits, full evidence cards with DOI links (once E-1 ships), smart meal plans, qailulah sleep tracking, full Ramadan mode, family profiles, unlimited history, weekly reports, offline mode, data export.

## 3. Paywall rules

1. Never on first open — user completes ≥1 habit first.
2. After first evidence-card "aha": "unlock full citation" prompt.
3. Soft prompts on premium features.
4. Day-7 value summary for active users.
5. Ramadan-prep campaign 2 weeks out.

Copy principles: investment in health + ibadah framing; concrete personal numbers ("45 habits this month"); no guilt-tripping, no dark patterns.

**Trial**: 14 days, no card required. Rationale (habit formation > 7-day industry standard) is sound; the specific conversion uplift figures circulating in earlier drafts were not independently verifiable — **do not cite them in the deck**. A/B against 7 days after launch and use own data.

## 4. Revenue projections — planning bands, not forecasts

No download/retention data exists yet; use these as *targets with assumptions stated*, not as predictions:
- Conservative 12-mo: 50K downloads, 2K subscribers, Rp98jt MRR (~$6K) — assumes 8% free→paid, D30 ≥ 30%.
- With Ramadan spike (timing depends on Hijri cycle — first Ramadan in app's life): up to ~2x.
Every investor-facing number in this band must be labeled "projection" with its assumption row. No fabricated traction anywhere.

## 5. GTM phases

**Phase 1 — Soft launch (M1–2)**: 200-user closed beta from Muslim tech Twitter/X,IG, WhatsApp communities; prove core loop; gate: D7 retention > 30% before spending anything.

**Phase 2 — Public launch (M3–4)**: Play Store production, Product Hunt, short-form content ("this Sunnah is backed by science"), micro-influencer outreach (10–100K followers), press kit.

**Phase 3 — Ramadan campaign**: Ramadan mode launch, "30 Days of Ihyaa" challenge, mosque partnerships, zakat integration (donate % of subscription), store featuring submission.

**Phase 4 — Post-Ramadan retention**: Shawwal 6-day fasting tracker, habit transition plans, annual-plan lock-in promo. Cliff risk is high — this phase decides the year.

**Phase 5 — Steady state (M9–12)**: family plan push, Health Connect wearable integration, referral (give 1 mo / get 1 mo), institutional pilots (Islamic schools, companies), localization: Malay → Turkish.

## 6. Channels

Organic first (Rp0): TikTok/IG Reels science-of-sunnah content, X build-in-public, community groups, ASO (habit tracker islami, thibbun nabawi, kesehatan muslim), mosque posters.
Paid only after 1,000 organic downloads prove retention: Google App Campaigns Rp5jt/mo, Meta Rp3jt, TikTok Rp2jt (~Rp10jt/mo total, stop-loss if CPI exceeds targets two weeks running).

## 7. Unit economics (verified model prices)

AI coach cost at scale (GPT-6 Luna $0.10/$0.50 per 1M; fallback DeepSeek $0.15–0.30/$0.60–1.20 off-peak):
- 1K DAU × 10 msg/user/mo ≈ $4–5/mo
- 10K DAU ≈ $15–30/mo
- 50K DAU ≈ $60–120/mo (Luna mostly; DeepSeek off-peak batching for nightly jobs halves it)
Per paying user: cents per month. Real unit-cost risks are hosting, push infra, and (if adopted) Qdrant — not LLM spend. Budget Gemini 3.8 Flash out of any cost plan: real price is $0.75/$3.75 per 1M, not the $0.10/$0.40 previously assumed.

## 8. Risk register (updated)

| Risk | Prob | Impact | Mitigation |
|---|---|---|---|
| Test credentials exposed in public repo | Certain | High | Rotate NOW; purge history (5 commits) |
| Emergent vendor lock | Certain | Blocker | ~1-day decouple task (4 replacements) |
| Google Play API 36 requirement (since Aug 31 2026) | Certain | Blocker | SDK 57 upgrade path; extension request to Nov 1 if needed |
| Scholar review: no owner, no date | High | High | Shortlist 3 reviewers this week — sole non-code blocker |
| Evidence pipeline does not exist for deck claims | Certain | High | E-0 audit + honest deck language until E-1 ships |
| Post-Ramadan cliff | High | Medium | Transition plans, annual lock-in, Shawwal tracker |
| Low free→paid conversion | Medium | High | 14-day trial, A/B paywall timing, bundle value |
| Content controversy (hadith interpretation) | Medium | High | Conservative grading, scholar review, disclaimers |
| AI coach harmful output | Medium | High | Structured output validation, medical/religious refusal routing, human review queue (currently prompt-level only — upgrade with provider rewrite) |
| Medical liability | Low | Very High | Disclaimers, contraindication layer E-2, referral prompts, insurance |

## 9. Immediate actions (priority order)

1. Rotate credentials + purge git history (today)
2. Emergent decoupling (~1 day)
3. Deploy backend (Railway/Render) + Atlas free tier (note: no backups, 30-day idle auto-pause)
4. AI provider rewrite — GPT-6 Luna primary, DeepSeek Flash fallback
5. SDK 57 upgrade + EAS build profile (settles API 36 simultaneously)
6. Sentry + Play Store internal testing track
7. Name hadith reviewer + date
8. E-0 citation audit (feeds deck honestly)
9. RevenueCat or Play Billing integration (real-money subscriptions)
