#!/usr/bin/env python3
"""Integrity gate for the evidence corpus.

Run before every release:

    python scripts/verify_evidence.py            # offline structural checks
    python scripts/verify_evidence.py --online   # also resolve every DOI

Exits non-zero on any FAIL. The point is that a fabricated citation, a retracted
paper, or an unverified hadith cannot reach a user by accident - the three things
most likely to destroy the credibility this app depends on.

Offline checks (always run):
  * every evidence record has a DOI, and no DOI sits on the retraction blocklist
  * every evidence_id / islamic_source_id referenced by a template exists
  * every hadith is graded sahih or hasan - da'if and ungraded are rejected
  * no placeholder reference numbers
  * every template family resolves to at least one source (evidence or scripture)

Online check (--online): resolves each DOI against doi.org and reports any that
do not resolve. Requires network; skipped by default so CI stays hermetic.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(BACKEND))

import evidence  # noqa: E402
import planner  # noqa: E402

FAILURES: list[str] = []
WARNINGS: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def check_evidence() -> None:
    records = evidence.evidence_by_id()          # raises on retracted / missing DOI
    blocked = evidence.retracted_dois()
    for rid, rec in records.items():
        for field in ("claim", "authors", "year", "journal", "study_type", "grade"):
            if not rec.get(field):
                fail(f"evidence '{rid}' missing required field '{field}'")
        if rec.get("grade") not in ("STRONG", "MODERATE", "WEAK", "CONTESTED"):
            fail(f"evidence '{rid}' has invalid grade {rec.get('grade')!r}")
        claim = rec.get("claim") or {}
        for lang in ("en", "id", "ar"):
            if not claim.get(lang):
                warn(f"evidence '{rid}' claim missing '{lang}' translation")
        if rec.get("grade") in ("WEAK", "CONTESTED") and not rec.get("caveat"):
            fail(f"evidence '{rid}' is {rec['grade']} but carries no caveat")
        if rec.get("supersedes_retracted_doi") and rec["supersedes_retracted_doi"] not in blocked:
            warn(f"evidence '{rid}' supersedes a DOI that is not on the blocklist")
    print(f"  evidence records: {len(records)}")


def check_sources() -> None:
    report = evidence.integrity_report()
    for sid in report["disallowed_grading"]:
        fail(f"islamic source '{sid}' has a grading outside sahih/hasan")
    for sid in report["placeholder_reference"]:
        fail(f"islamic source '{sid}' has a placeholder reference number "
             f"- supply the real one or delete the source")
    if report["pending_review"]:
        warn(f"{len(report['pending_review'])} Islamic source(s) awaiting scholar "
             f"review and therefore WITHHELD from the UI: "
             f"{', '.join(report['pending_review'][:6])}"
             + (" ..." if len(report["pending_review"]) > 6 else ""))
    print(f"  islamic sources: {report['source_count']} "
          f"({report['shippable_sources']} cleared to ship)")


def check_templates() -> None:
    ev_ids = set(evidence.evidence_by_id())
    src_ids = set(evidence.sources_by_id())
    families = planner.load_families()
    for fam in families:
        key = fam.get("key", "<unkeyed>")
        for eid in fam.get("evidence_ids", []):
            if eid not in ev_ids:
                fail(f"family '{key}' references unknown evidence id '{eid}'")
        for sid in fam.get("islamic_source_ids", []):
            if sid not in src_ids:
                fail(f"family '{key}' references unknown islamic source id '{sid}'")
        if not fam.get("evidence_ids") and not fam.get("islamic_source_ids"):
            fail(f"family '{key}' has no sourcing at all")
        if not fam.get("progression"):
            fail(f"family '{key}' has no progression steps")
        for tag in fam.get("contraindications", []):
            if tag not in __import__("safety").TAGS:
                fail(f"family '{key}' uses unknown contraindication tag '{tag}'")
    print(f"  template families: {len(families)} "
          f"-> {len(planner.load_presentations())} presentations")


def check_online() -> None:
    import urllib.error
    import urllib.request

    records = evidence.evidence_by_id()
    print(f"  resolving {len(records)} DOIs ...")
    for rid, rec in sorted(records.items()):
        doi = rec["doi"]
        req = urllib.request.Request(
            f"https://doi.org/{doi}", method="HEAD",
            headers={"User-Agent": "ihyaa-evidence-verifier"},
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                if resp.status >= 400:
                    fail(f"evidence '{rid}' DOI {doi} returned HTTP {resp.status}")
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                warn(f"evidence '{rid}' DOI {doi} resolved but is paywalled ({exc.code})")
            else:
                fail(f"evidence '{rid}' DOI {doi} did not resolve (HTTP {exc.code})")
        except Exception as exc:  # network, DNS, timeout
            warn(f"evidence '{rid}' DOI {doi} could not be checked: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true",
                        help="also resolve every DOI against doi.org")
    args = parser.parse_args()

    print("Ihyaa evidence integrity check")
    try:
        check_evidence()
        check_sources()
        check_templates()
        if args.online:
            check_online()
    except evidence.EvidenceError as exc:
        fail(str(exc))

    if WARNINGS:
        print(f"\n{len(WARNINGS)} warning(s):")
        for msg in WARNINGS:
            print(f"  WARN  {msg}")
    if FAILURES:
        print(f"\n{len(FAILURES)} failure(s):")
        for msg in FAILURES:
            print(f"  FAIL  {msg}")
        return 1
    print("\nAll integrity checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
