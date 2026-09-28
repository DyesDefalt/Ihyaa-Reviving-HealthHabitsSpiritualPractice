# Ihyaa — Content & Evidence Strategy

_Updated 28 Sep 2026. Previous versions of this document described an evidence pipeline (33 DOI records, 31 Islamic-source registry, contraindication database tested against CKD/T1DM/pregnancy/anticoagulants) that does not exist in the codebase. This version states what exists, what is missing, and the build order to close the gap honestly._

## 1. What actually exists today (measured)

- **97 habit templates**, each carrying trilingual (EN/ID/AR) title, description, Quran reference, hadith reference, and a science note. Science notes are **prose citations** ("PREDIMED re-analysis, NEJM 2018", "Frontiers in Psychology, 2019") — **no DOI strings, no registry, no retraction check** anywhere in the backend.
- **8 knowledge cards**, 14 recipes, 8 exercise routines, 6 mind windows in `library.py` — same inline-citation pattern.
- **Hadith references cite collections** (Sahih Bukhari/Muslim, Sunan an-Nasa'i, Jami` at-Tirmidhi) **without a grading field or review status**. There is no sahih/hasan/dhaif metadata, no reviewer identity, no dates.
- **Safety today = health flags**: `health.py` derives flags from 8 conditions (diabetes, hypertension, high cholesterol, joint pain, insomnia, anxiety, digestive, overweight) + age/sex/work-pattern. `CONTRA_PATCH` excludes 7 templates for specific flags. There is **no CKD, T1DM, pregnancy, or anticoagulant handling**, and no per-condition severity levels (info/warning/block).

What exists is good — coverage is simply not what the old docs claimed. The honest foundation: a working trilingual content engine with verified delivery, and a safety layer at "lifestyle-app" level, not "medical" level.

## 2. The evidence gap — why it matters

The pitch (app + deck) leans on "DOI-verified, scholar-reviewed" as differentiation. None of that machinery exists yet. **No fabricated number should appear in the deck from this doc.** Deck language until Phase E-1 ships: "every habit carries Quran/Hadith grounding plus a clinical science note; a structured DOI registry and scholar review pipeline are under construction."

## 3. Build order (replaces the old "pipeline" description)

### E-0 — Citation audit (cheap, high-leverage)
Go template by template; for each science note, either (a) locate and record the actual DOI behind the prose citation, or (b) downgrade the claim wording to match only what the source supports. Output: spreadsheet now, migration to `evidence_records` collection in E-1.
Known case to handle: olive-oil/PREDIMED claims should cite the **2018 re-analysis**, and the original 2013 paper (retracted+republished) must never be cited as-is.

### E-1 — `evidence_records` collection + API
Schema: template_key, evidence_type (clinical_doi | quran | hadith | classical_scholar), doi, journal, year, study_type, key_finding (en/id), evidence_level (strong/moderate/limited), is_retracted, source_text, translation, reference, grading, review_status, reviewed_by, reviewed_at.
Quarterly re-verification job against Retraction Watch; retraction → OTA content update + push notification to affected users.
Endpoint: `GET /api/evidence/{templateKey}`.

### E-2 — Contraindication upgrade
Current flags → severity levels (`info` / `warning` / `block`) with messages and alternative-template mapping. Priority conditions **in this order**, because each has users waiting:
1. Pregnancy (exercise/nutrition/fasting)
2. T1DM + T2DM (unsupervised fasting blocks — also fix the "sunnah fasting" templates which currently only carry diabetes-derived `no_fasting`)
3. CKD (protein/fluid)
4. Anticoagulant (vitamin-K foods, herbal remedies)
Extend `Preferences.conditions` beyond the current 8 entries and add unit tests asserting block/warn behavior per condition.

### E-3 — Hadith grading + scholar review
- Keep MIT-licensed `hadith-api` (gadingnst) vendored as reference for text/translation only.
- **Never infer grading from collection name.** Own curated grading table keyed by reference.
- Review requirements: reviewer with min. S1 Syariah/Ushuluddin (or equivalent); grading cross-checked against 2 sources; controversial medical claims carry disclaimer.
- **Blocker stands**: no reviewer named, no date set. This is the top risk in every planning doc and it cannot be closed by code. Owner: founder. First action: shortlist 3 candidates this week.

### E-4 — Quran/hadith API vendoring
`gadingnst/quran-api` (MIT) as SQLite bundle for offline Quran text + Kemenag tafsir; AlAdhan stays the prayer-time source (method 20 available for Kemenag alignment; register for Kemenag SIHAT as authoritative backup when approved).

## 4. Grading display (unchanged design)

| Level | Clinical | Islamic | Display |
|---|---|---|---|
| Strong | Meta-analysis, systematic review, large RCT | Quran; Sahih Bukhari/Muslim | Green |
| Moderate | Small RCT, cohort | Sahih (other), Hasan | Yellow |
| Limited | Observational, in-vitro | Dhaif + explicit disclaimer | Orange + disclaimer |
| Expert opinion | Guidelines, consensus | Classical scholar opinion | Blue |

## 5. Content volume roadmap (recalibrated to 97 templates)

| Phase | Target | Priority adds |
|---|---|---|
| Now | 97 templates | — |
| 2 | ~150 templates | Ramadan set (tarawih, qiyam, iftar etiquette), women's health, elderly-friendly, kids (family plan) |
| 3 | ~230 templates | Chronic-disease management, mental-health depth, hajj/umrah prep, Indonesian local wisdom (jamu, evidence-checked) |
| 4 | Community | User-submitted habits through this same review pipeline |

Repeat-gap math (measured): worst gap 30–49 days on 1-year plans, content-limited. Each phase above materially improves rotation depth. Re-measure with the same simulation script after each expansion: `generate_plan()` over 3 seeds, report max inter-occurrence gap per template.

## 6. Quality metrics (honest baselines)

| Metric | Target | Current (measured) |
|---|---|---|
| Templates with ≥1 recorded clinical source (DOI) | 100% | **0%** (prose citations only) |
| Templates with Quran or hadith reference string | 100% | ~100% (spot-checked, not fully audited) |
| Doi registry coverage | 100% | 0 records |
| Scholar review completion (hadith) | 100% | Not started — no reviewer |
| Contraindication severity coverage | 8 conditions + 4 more | 8 lifestyle flags, no block/warn levels |
| 365-day worst repeat gap | 60 days | 30–49 days |
| Retraction check currency | < 90 days | N/A (nothing to check yet) |
