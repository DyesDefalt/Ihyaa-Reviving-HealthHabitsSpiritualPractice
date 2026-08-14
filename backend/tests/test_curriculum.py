"""Tests for the plan engine, the safety gate and the evidence layer.

These encode the problems the redesign exists to fix, so a regression is loud:

  * a year-long plan used to replay the same 17-template pool every ~17 days
  * a 30-day plan could provably never reach advanced content
  * spiritual was force-ranked above body every day, contradicting the positioning
  * nothing stopped a fasting habit being scheduled for a dialysis patient
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import evidence  # noqa: E402
import hijri  # noqa: E402
import planner  # noqa: E402
import safety  # noqa: E402

START = date(2026, 9, 1)


def build(challenge_type="1_year", **kwargs):
    kwargs.setdefault("fitness_level", "advanced")
    kwargs.setdefault("seed", "test-user")
    return planner.generate_plan(challenge_type=challenge_type, start_date=START, **kwargs)


def seasonal_families() -> set[str]:
    """Families confined to a Hijri season - these SHOULD recur inside it."""
    return {
        fam["key"] for fam in planner.load_families()
        if "ordinary" not in fam.get("block_affinity", ["ordinary"])
    }


# --------------------------------------------------------------- repetition

def test_year_plan_does_not_repeat_within_25_days():
    """The headline fix. The old engine scored ~17 days here; this scores ~26.

    25 is the honest floor for the CURRENT pool, not the target. The picker is
    already optimal (least-recently-used), so the only lever left is content
    volume: at ~1.9 draws a day per body pillar, a 60-day floor needs ~115
    presentations per body pillar against the 68/65 that exist today. Raise this
    threshold as tranches land - do not relax it.
    """
    plan = build("1_year")
    seasonal = seasonal_families()
    general = [t for t in plan if t["family_key"] not in seasonal]
    gap = planner.repetition_gap(general)
    assert gap["min_gap_days"] >= 25, (
        f"{gap['worst_key']} repeats after only {gap['min_gap_days']} days"
    )


def test_thirty_day_plan_never_repeats_at_all():
    plan = build("30_days")
    gap = planner.repetition_gap(plan)
    assert gap["min_gap_days"] is None, f"{gap['worst_key']} repeated inside 30 days"
    assert gap["distinct_presentations"] == gap["total_tasks"]


def test_hundred_day_plan_does_not_repeat_within_25_days():
    plan = build("100_days")
    seasonal = seasonal_families()
    general = [t for t in plan if t["family_key"] not in seasonal]
    gap = planner.repetition_gap(general)
    assert gap["min_gap_days"] >= 25


def test_thirty_day_plan_reaches_advanced_content():
    """Previously impossible: min_phase>=2 gated all advanced templates out."""
    plan = build("30_days")
    assert max(t["difficulty"] for t in plan) >= 2


def test_plan_is_deterministic_for_a_seed():
    a = build("100_days", seed="same")
    b = build("100_days", seed="same")
    assert [t["template_key"] for t in a] == [t["template_key"] for t in b]


def test_different_seeds_give_different_plans():
    a = build("100_days", seed="user-a")
    b = build("100_days", seed="user-b")
    assert [t["template_key"] for t in a] != [t["template_key"] for t in b]


# ------------------------------------------------------------ body-first

def test_body_pillars_dominate_under_body_focus():
    plan = build("1_year", focus="body")
    body = [t for t in plan if t["pillar"] in planner.BODY_PILLARS]
    assert len(body) / len(plan) >= 0.60


def test_spiritual_is_not_forced_first_every_day():
    """The old pillar_priority() hard-boosted spiritual above body pillars."""
    plan = build("1_year", focus="body")
    first_of_day = {}
    for task in plan:
        first_of_day.setdefault(task["day_number"], task["pillar"])
    spiritual_first = sum(1 for p in first_of_day.values() if p == "spiritual")
    assert spiritual_first == 0


def test_focus_all_gives_spiritual_real_share():
    plan = build("1_year", focus="all")
    spiritual = [t for t in plan if t["pillar"] == "spiritual"]
    assert len(spiritual) / len(plan) > 0.15


# ---------------------------------------------------------------- safety

def test_dialysis_patient_gets_no_fasting_habits():
    profile = {"conditions": ["t2dm", "dialysis"], "medications": []}
    plan = build("1_year", health_profile=profile)
    keys = {t["template_key"].split("#")[0] for t in plan}
    by_key = {f["key"]: f for f in planner.load_families()}
    for key in keys:
        assert "fasting" not in by_key[key].get("contraindications", []), key


def test_first_trimester_pregnancy_blocks_fasting_and_black_seed():
    profile = {"conditions": [], "medications": [], "pregnancy_trimester": 1}
    blocked = safety.blocked_tags(profile)
    assert "fasting" in blocked
    assert "caloric_restriction" in blocked
    assert "black_seed" in blocked


def test_anticoagulant_blocks_black_seed():
    """Nigella sativa is antiplatelet - the interaction is additive."""
    profile = {"conditions": [], "medications": ["anticoagulant"]}
    plan = build("1_year", health_profile=profile)
    families = {t["family_key"] for t in plan}
    assert "n_blackseed" not in families


def test_type_1_diabetes_is_very_high_risk():
    assert safety.dar_risk_category({"conditions": ["t1dm"]}) == "very_high"


def test_healthy_profile_blocks_nothing():
    assert safety.blocked_tags({"conditions": [], "medications": []}) == set()


def test_gate_notices_explain_withheld_fasting():
    profile = {"conditions": ["t2dm", "ckd_stage_4_5"], "medications": ["insulin"]}
    codes = {n["code"] for n in safety.gate_notices(profile, "en")}
    assert "dar_fasting_gate" in codes


def test_contraindicated_plan_is_still_usable():
    """Filtering must not empty the plan out."""
    profile = {
        "conditions": ["t1dm", "ckd_stage_4_5", "heart_disease", "osteoporosis"],
        "medications": ["insulin", "anticoagulant"],
        "pregnancy_trimester": 2,
    }
    plan = build("100_days", health_profile=profile)
    assert len(plan) > 200
    assert {t["pillar"] for t in plan} >= {"physical", "nutrition"}


# -------------------------------------------------------------- evidence

def test_no_retracted_doi_is_reachable():
    blocked = set(evidence.retracted_dois())
    assert "10.1056/NEJMoa1200303" in blocked, "PREDIMED 2013 must stay blocklisted"
    for rec in evidence.evidence_by_id().values():
        assert rec["doi"] not in blocked


def test_every_evidence_record_has_a_doi():
    for rid, rec in evidence.evidence_by_id().items():
        assert rec.get("doi"), rid


def test_unverified_hadith_is_withheld():
    """Hadith numbers could not be tool-verified, so they must not render."""
    for sid, src in evidence.sources_by_id().items():
        if src["type"] == "hadith" and src["verification_status"] != "verified":
            assert evidence.localize_source(sid, "en") is None, sid


def test_no_weak_grade_hadith_can_ship():
    for src in evidence.sources_by_id().values():
        if src["type"] == "hadith":
            assert src.get("grading") in evidence.ALLOWED_GRADINGS


def test_quran_sources_ship_with_a_label():
    src = evidence.localize_source("is_olive", "en")
    assert src and src["label"].startswith("Qur'an")


def test_every_template_reference_resolves():
    ev_ids = set(evidence.evidence_by_id())
    src_ids = set(evidence.sources_by_id())
    for fam in planner.load_families():
        assert set(fam.get("evidence_ids", [])) <= ev_ids, fam["key"]
        assert set(fam.get("islamic_source_ids", [])) <= src_ids, fam["key"]


def test_weak_evidence_always_carries_a_caveat():
    for rid, rec in evidence.evidence_by_id().items():
        if rec["grade"] in ("WEAK", "CONTESTED"):
            assert rec.get("caveat"), rid


# ---------------------------------------------------------------- hijri

@pytest.mark.parametrize("gregorian,expected_block", [
    (date(2026, 2, 18), "ramadan"),          # 1 Ramadan 1447
    (date(2026, 5, 27), "dhul_hijjah_ten"),  # 10 Dhul Hijjah 1447
])
def test_hijri_blocks_land_on_the_right_season(gregorian, expected_block):
    assert hijri.block_for(gregorian)["id"] == expected_block


def test_seasonal_content_stays_in_its_season():
    """An Ayyam al-Bid fast on the 3rd of the month would simply be wrong."""
    plan = build("1_year")
    seasonal = seasonal_families()
    for task in plan:
        if task["family_key"] in seasonal:
            fam = next(f for f in planner.load_families() if f["key"] == task["family_key"])
            assert task["hijri_block"] in fam["block_affinity"], task


def test_ramadan_surfaces_ramadan_specific_content():
    plan = build("1_year")
    ramadan = {t["family_key"] for t in plan if t["hijri_block"] == "ramadan"}
    assert {"n_suhoor", "n_iftar_composition"} <= ramadan
