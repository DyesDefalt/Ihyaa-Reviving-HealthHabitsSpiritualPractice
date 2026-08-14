# UI mockups (Phase 2c)

HTML/CSS mockups of 3 key screens, built directly against `design_guidelines.json`'s tokens. Produced as a fallback because the connected Figma seat is View-only (starter tier); these are reference mockups for implementation, not exported Figma frames.

- `01_today.html` / `.png` — daily task list, body-first ordering (physical/nutrition lead), streak, Hijri-aware chip, floating tab bar.
- `02_onboarding_health.html` / `.png` — the health-screening onboarding step (age, conditions, medications) that feeds `HealthProfile`/`safety.py` contraindication filtering. Framed as optional/reassuring, not a medical intake form.
- `03_habit_detail_citation.html` / `.png` — the habit detail card showing the graded clinical evidence (STRONG/MODERATE/WEAK/CONTESTED, effect size, caveat, DOI) and Islamic source, the product's core differentiator.

**Note on `03_habit_detail_citation.html`:** the hadith text/grading shown is illustrative of the UI pattern only. Per `backend/data/islamic_sources.json`, every hadith in the actual dataset is withheld (`pending_scholar_review`) until a named reviewer confirms it — this mockup does not assert that any specific hadith has cleared review.

Open any `.html` file directly in a browser to view/screenshot at other sizes.
