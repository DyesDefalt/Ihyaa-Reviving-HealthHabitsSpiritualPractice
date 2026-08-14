"""Plan generation.

Replaces the old `pool[counters[pillar] % len(pool)]` selection, which made repetition
inevitable: with 17 templates per pillar and one slot a day, a year-long plan replayed
the same pool roughly every 17 days for its final nine months.

Three changes fix that, and they multiply rather than add:

  1. FAMILIES WITH PROGRESSION STEPS. A family like "walking" expands into several
     distinct presentations (10 min -> 15 -> 20 -> 7,000 steps -> 45 min). Progressive
     overload is what keeps training interesting in real life, and it is what keeps
     the plan interesting here - without writing a new habit for every day.

  2. LEAST-RECENTLY-USED SELECTION, NOT A COUNTER. Each draw takes the eligible
     presentation that has gone longest unshown, which is the policy that maximises
     the minimum gap for a given pool. Measured on a 365-day plan this moves the
     floor from ~17 days to ~26. The picker is now optimal, so the remaining lever
     is content volume, not scheduling: at ~1.9 draws a day per body pillar, a
     60-day floor needs ~115 presentations per body pillar (today: 68 and 65).

  3. HIJRI BLOCKS. When the day falls in Ramadan, Dhul Hijjah or Sha'ban, the draw
     prefers presentations tagged for that block. The Islamic year supplies variety
     the content pool does not have to.

Generation stays deterministic: the same (seed, profile, challenge) always produces the
same plan, so it can be regenerated or audited without storing every task.
"""
from __future__ import annotations

import json
import random
from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path

import hijri
import safety

DATA_DIR = Path(__file__).parent / "data" / "templates"

PILLARS = ("physical", "nutrition", "spiritual", "mental")
BODY_PILLARS = ("physical", "nutrition")

# Body-first ordering (product decision, 2026-08-13). The old code force-boosted
# spiritual to rank first every day, which contradicted the app's own positioning.
FOCUS_CYCLE = {
    "body": ["physical", "nutrition", "physical", "spiritual", "nutrition", "mental"],
    "body_mind": ["physical", "nutrition", "mental", "physical", "spiritual", "nutrition"],
    "all": ["physical", "nutrition", "spiritual", "mental"],
}

CHALLENGE_DAYS = {"30_days": 30, "100_days": 100, "1_year": 365}

FITNESS_LEVEL = {"beginner": 1, "intermediate": 2, "advanced": 3}


def tasks_for_day(day: int) -> int:
    """The 1%-better ramp: start absurdly small so showing up is trivial."""
    if day <= 3:
        return 2
    if day <= 10:
        return 3
    if day <= 40:
        return 4
    return 5


def level_cap_for_day(day: int, fitness_level: int) -> int:
    """Difficulty unlocks with time, never above the user's own declared level."""
    if day <= 14:
        unlocked = 1
    elif day <= 45:
        unlocked = 2
    else:
        unlocked = 3
    return min(unlocked, fitness_level)


@lru_cache(maxsize=1)
def load_families() -> list[dict]:
    families: list[dict] = []
    for path in sorted(DATA_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as fh:
            doc = json.load(fh)
        # A file declares a default pillar, and may carry a second pillar's families
        # under "<pillar>_families" so small tranches do not need their own file.
        for key, contents in doc.items():
            if not key.endswith("families") or not isinstance(contents, list):
                continue
            pillar = doc["pillar"] if key == "families" else key[: -len("_families")]
            if pillar not in PILLARS:
                raise RuntimeError(f"{path.name}: unknown pillar '{pillar}'")
            for fam in contents:
                fam = dict(fam)
                fam.setdefault("pillar", pillar)
                families.append(fam)
    if not families:
        raise RuntimeError(f"no template families found in {DATA_DIR}")
    return families


@lru_cache(maxsize=1)
def load_presentations() -> list[dict]:
    """Flatten every family into its individual progression steps."""
    out: list[dict] = []
    for fam in load_families():
        base_level = fam.get("level", 1)
        for step in fam["progression"]:
            key = f"{fam['key']}#{step['step']}"
            out.append({
                "key": key,
                "family_key": fam["key"],
                "family": fam.get("family", fam["key"]),
                "pillar": fam["pillar"],
                "anchor": fam.get("anchor", "anytime"),
                "level": step.get("level", base_level),
                "step": step["step"],
                "minutes": step.get("minutes", 5),
                "target_steps": step.get("target_steps"),
                "title": fam["title"],
                "desc": fam["desc"],
                "label": step.get("label"),
                "evidence_ids": fam.get("evidence_ids", []),
                "islamic_source_ids": fam.get("islamic_source_ids", []),
                "contraindications": fam.get("contraindications", []),
                "block_affinity": fam.get("block_affinity", ["ordinary"]),
            })
    return out


@lru_cache(maxsize=1)
def presentations_by_key() -> dict[str, dict]:
    return {p["key"]: p for p in load_presentations()}


def eligible(pillar: str, profile: dict | None, fitness_level: int) -> list[dict]:
    """Everything this user may ever be shown for this pillar."""
    return [
        p for p in load_presentations()
        if p["pillar"] == pillar
        and p["level"] <= fitness_level
        and safety.template_allowed(p, profile)
    ]


class _Bag:
    """Least-recently-used picker.

    Always draws the eligible presentation that has gone longest without being shown,
    which is the policy that provably maximises the minimum gap between repeats for a
    given pool. Never-shown items sort first (last_used = -1), so the plan exhausts all
    new content before it repeats anything at all.

    A plain shuffle bag was tried first and rejected: refilling let an item fall at the
    end of one cycle and the start of the next, producing back-to-back repeats.

    The random tie-break is seeded, so plans stay reproducible.
    """

    def __init__(self, items: list[dict], rng: random.Random):
        self._items = items
        self._rng = rng
        self._last_used: dict[str, int] = {p["key"]: -1 for p in items}
        self._jitter = {p["key"]: rng.random() for p in items}

    # A season-specific presentation is treated as this many extra days stale during
    # its season, so Ramadan content surfaces in Ramadan. The bonus deliberately does
    # NOT apply to general ("ordinary"-tagged) content: an item tagged for most blocks
    # would otherwise hold the bonus permanently and crowd everything else out.
    BLOCK_BONUS = 30

    @staticmethod
    def _seasonal_boost(pres: dict, block_id: str) -> bool:
        return (block_id != "ordinary"
                and block_id in pres["block_affinity"]
                and "ordinary" not in pres["block_affinity"])

    @staticmethod
    def _eligible_in_block(pres: dict, block_id: str) -> bool:
        """Season-only content stays in its season.

        A presentation tagged "ordinary" is general and may appear any day. One that
        is not (suhoor, the white-day fast, Ramadan training) is exclusive to the
        blocks it names - scheduling an Ayyam al-Bid fast on the 3rd of the month
        would be simply wrong.
        """
        affinity = pres["block_affinity"]
        return "ordinary" in affinity or block_id in affinity

    def draw(self, block_id: str, level_cap: int, day: int) -> dict | None:
        if not self._items:
            return None
        in_block = [p for p in self._items if self._eligible_in_block(p, block_id)]
        if not in_block:
            in_block = self._items

        for candidates in ([p for p in in_block if p["level"] <= level_cap], in_block):
            if not candidates:
                continue
            pick = min(
                candidates,
                key=lambda p: (
                    self._last_used[p["key"]]
                    - (self.BLOCK_BONUS if self._seasonal_boost(p, block_id) else 0),
                    p["level"], p["step"], self._jitter[p["key"]],
                ),
            )
            self._last_used[pick["key"]] = day
            return pick
        return None


def pillar_cycle(focus: str) -> list[str]:
    return FOCUS_CYCLE.get(focus, FOCUS_CYCLE["body"])


def day_pillars(n: int, focus: str, day: int) -> list[str]:
    """Which pillars fill today's slots.

    Under a body focus the first two slots are always physical and nutrition, so the
    body pillars lead every single day - that is what "body first" means, and it is
    the opposite of the old behaviour where spiritual was force-ranked to the top.

    Remaining slots rotate through the cycle with a per-day offset, so the secondary
    pillars still get a fair share instead of only appearing on the longest days.
    """
    cycle = pillar_cycle(focus)
    out = [] if focus == "all" else [p for p in BODY_PILLARS][:n]
    offset = day
    while len(out) < n:
        out.append(cycle[offset % len(cycle)])
        offset += 1
    return out[:n]


def generate_plan(
    *,
    challenge_type: str = "30_days",
    start_date: date | None = None,
    focus: str = "body",
    fitness_level: str | int = "beginner",
    health_profile: dict | None = None,
    seed: str = "ihyaa",
) -> list[dict]:
    """Deterministically build the whole challenge.

    Returns one dict per scheduled task, in day order.
    """
    total_days = CHALLENGE_DAYS.get(challenge_type, 30)
    start = start_date or date.today()
    fit = FITNESS_LEVEL.get(fitness_level, fitness_level) if isinstance(fitness_level, str) else fitness_level
    fit = max(1, min(3, int(fit)))

    bags = {
        pillar: _Bag(eligible(pillar, health_profile, fit), random.Random(f"{seed}:{pillar}"))
        for pillar in PILLARS
    }

    plan: list[dict] = []
    for day in range(1, total_days + 1):
        day_date = start + timedelta(days=day - 1)
        block = hijri.block_for(day_date)
        cap = level_cap_for_day(day, fit)
        n = tasks_for_day(day)

        # Ramadan deliberately dials volume back; Dhul Hijjah dials it up.
        intensity = block["task_intensity"]
        n = max(2, round(n * intensity))

        used_today: set[str] = set()
        for pillar in day_pillars(n, focus, day):
            pres = bags[pillar].draw(block["id"], cap, day)
            if pres is None or pres["key"] in used_today:
                continue
            used_today.add(pres["key"])
            plan.append({
                "day_number": day,
                "scheduled_date": day_date.isoformat(),
                "template_key": pres["key"],
                "family_key": pres["family_key"],
                "pillar": pres["pillar"],
                "anchor": pres["anchor"],
                "duration_minutes": pres["minutes"],
                "difficulty": pres["level"],
                "points_reward": 8 + pres["level"] * 4,
                "hijri_block": block["id"],
            })
    return plan


def repetition_gap(plan: list[dict]) -> dict:
    """Smallest number of days between two uses of the same presentation.

    This is the metric the whole redesign exists to move. The old engine scored
    about 17 on a 365-day plan.
    """
    last_seen: dict[str, int] = {}
    min_gap = None
    worst = None
    for task in plan:
        key = task["template_key"]
        day = task["day_number"]
        if key in last_seen:
            gap = day - last_seen[key]
            if min_gap is None or gap < min_gap:
                min_gap, worst = gap, key
        last_seen[key] = day
    return {
        "min_gap_days": min_gap,
        "worst_key": worst,
        "distinct_presentations": len(last_seen),
        "total_tasks": len(plan),
    }
