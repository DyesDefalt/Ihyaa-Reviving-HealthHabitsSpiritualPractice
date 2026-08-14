"""Evidence and Islamic-source layer.

Habit templates never inline a citation. They reference an evidence record and an
Islamic source by id, and this module resolves them - applying two hard gates:

  1. A hadith only renders if a qualified reviewer has marked it `verified` AND its
     grading is sahih or hasan. Everything else is withheld. Hadith reference numbers
     were the one thing three independent research passes could not verify with any
     tool, so the default posture is "do not ship".

  2. An evidence record whose DOI sits on the retraction blocklist raises at load
     time. A retracted citation must never reach a user.

If a source is withheld the card still renders - it simply shows one less block. A
missing hadith is a cosmetic gap; a wrong one is a credibility failure.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

LANGS = ("en", "id", "ar")
ALLOWED_GRADINGS = {"sahih", "hasan"}
SHIPPABLE_STATUS = "verified"


class EvidenceError(RuntimeError):
    """Raised when the evidence corpus itself is invalid - always fatal at boot."""


def _pick(field: dict | None, lang: str) -> str | None:
    """Trilingual field -> one string, falling back to English."""
    if not field:
        return None
    return field.get(lang) or field.get("en")


def _read(name: str) -> dict:
    path = DATA_DIR / name
    if not path.exists():
        raise EvidenceError(f"missing data file: {path}")
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def _evidence_raw() -> dict:
    return _read("evidence.json")


@lru_cache(maxsize=1)
def _sources_raw() -> dict:
    return _read("islamic_sources.json")


@lru_cache(maxsize=1)
def retracted_dois() -> dict[str, dict]:
    """DOI -> blocklist entry. Cited anywhere, this is a fatal error."""
    return {e["doi"]: e for e in _evidence_raw().get("retracted_doi_blocklist", [])}


@lru_cache(maxsize=1)
def evidence_by_id() -> dict[str, dict]:
    records: dict[str, dict] = {}
    blocked = retracted_dois()
    for rec in _evidence_raw().get("evidence", []):
        rid = rec.get("id")
        if not rid:
            raise EvidenceError("evidence record without an id")
        if rid in records:
            raise EvidenceError(f"duplicate evidence id: {rid}")
        doi = rec.get("doi")
        if doi in blocked:
            raise EvidenceError(
                f"evidence '{rid}' cites RETRACTED doi {doi} "
                f"({blocked[doi]['what']}); use '{blocked[doi]['use_instead']}' instead"
            )
        if not doi:
            raise EvidenceError(f"evidence '{rid}' has no DOI - every claim must resolve")
        records[rid] = rec
    return records


@lru_cache(maxsize=1)
def sources_by_id() -> dict[str, dict]:
    sources: dict[str, dict] = {}
    for src in _sources_raw().get("sources", []):
        sid = src.get("id")
        if not sid:
            raise EvidenceError("islamic source without an id")
        if sid in sources:
            raise EvidenceError(f"duplicate islamic source id: {sid}")
        sources[sid] = src
    return sources


def is_shippable(source: dict) -> bool:
    """A hadith needs review AND an acceptable grading. Quran refs are stable."""
    if source.get("verification_status") != SHIPPABLE_STATUS:
        return False
    if source.get("type") == "hadith":
        return source.get("grading") in ALLOWED_GRADINGS
    return True


def localize_evidence(evidence_id: str, lang: str) -> dict | None:
    rec = evidence_by_id().get(evidence_id)
    if not rec:
        return None
    citation = f"{rec['authors']} ({rec['year']}). {rec['journal']}"
    if rec.get("volume_pages"):
        citation += f" {rec['volume_pages']}"
    return {
        "id": rec["id"],
        "claim": _pick(rec.get("claim"), lang),
        "citation": citation,
        "doi": rec["doi"],
        "doi_url": f"https://doi.org/{rec['doi']}",
        "erratum_doi": rec.get("erratum_doi"),
        "study_type": rec.get("study_type"),
        "sample_size": rec.get("sample_size"),
        "effect_size": rec.get("effect_size"),
        "grade": rec.get("grade"),
        "caveat": _pick(rec.get("caveat"), lang),
    }


def localize_source(source_id: str, lang: str) -> dict | None:
    """Returns None when the source is not cleared to ship - by design."""
    src = sources_by_id().get(source_id)
    if not src or not is_shippable(src):
        return None
    out = {
        "id": src["id"],
        "type": src["type"],
        "reference": src["reference"],
        "text": _pick(src.get("text"), lang),
    }
    if src["type"] == "quran":
        out["surah_name"] = src.get("surah_name")
        out["label"] = f"Qur'an {src['reference']}"
    else:
        out["collection"] = src.get("collection")
        out["grading"] = src.get("grading")
        out["grader"] = src.get("grader")
        # The grade is shown to the user, per the 2026-08-13 sourcing decision.
        out["label"] = f"{src.get('collection')} {src['reference']} ({src.get('grading')})"
    return out


def resolve_for_template(tpl: dict, lang: str) -> dict:
    """Attach localized evidence + Islamic sources to a template presentation."""
    evidence = [localize_evidence(eid, lang) for eid in tpl.get("evidence_ids", [])]
    sources = [localize_source(sid, lang) for sid in tpl.get("islamic_source_ids", [])]
    evidence = [e for e in evidence if e]
    sources = [s for s in sources if s]
    return {
        "evidence": evidence,
        "quran": [s for s in sources if s["type"] == "quran"],
        "hadith": [s for s in sources if s["type"] == "hadith"],
        # Surfaced so the UI can badge a card whose strongest support is weak.
        "weakest_grade": _weakest([e.get("grade") for e in evidence]),
    }


_GRADE_ORDER = {"STRONG": 0, "MODERATE": 1, "WEAK": 2, "CONTESTED": 3}


def _weakest(grades: list[str | None]) -> str | None:
    real = [g for g in grades if g in _GRADE_ORDER]
    if not real:
        return None
    return max(real, key=lambda g: _GRADE_ORDER[g])


def integrity_report() -> dict:
    """Used by scripts/verify_evidence.py and by the boot check."""
    ev = evidence_by_id()
    src = sources_by_id()
    pending = [s for s in src.values() if not is_shippable(s)]
    bad_grade = [
        s for s in src.values()
        if s.get("type") == "hadith" and s.get("grading") not in ALLOWED_GRADINGS
    ]
    placeholder = [
        s for s in src.values()
        if str(s.get("reference", "")).strip("0") == "" and s.get("type") == "hadith"
    ]
    return {
        "evidence_count": len(ev),
        "source_count": len(src),
        "shippable_sources": len([s for s in src.values() if is_shippable(s)]),
        "pending_review": sorted(s["id"] for s in pending),
        "disallowed_grading": sorted(s["id"] for s in bad_grade),
        "placeholder_reference": sorted(s["id"] for s in placeholder),
        "grades": {
            g: len([e for e in ev.values() if e.get("grade") == g])
            for g in ("STRONG", "MODERATE", "WEAK", "CONTESTED")
        },
    }
