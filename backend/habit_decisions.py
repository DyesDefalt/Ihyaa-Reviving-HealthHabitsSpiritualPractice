"""Rank only a conservative subset of existing, unfinished daily habits."""
import asyncio
import hashlib
import json
import logging
from datetime import timedelta
from typing import Literal
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from pymongo import ReturnDocument
from typesafe_sdk import Score

from auth import get_current_user
from coach_safety import CONSENT_VERSION, basic_preferences
from curriculum import LEVELS, TEMPLATES_BY_KEY
from db import get_db
from health import health_profile
from jev import decide, jev_error_code
from models import User, utcnow

router = APIRouter(prefix="/api/decisions", tags=["decisions"])

# Ranking is not a safety assessor. Exclude supplements, fasts, quantified intake,
# intensive workouts, religious prescriptions and templates without a reviewed mapping.
RANKABLE = {
    "p_walk_fajr", "p_stretch", "p_wudu_mobility", "p_walk_mosque", "p_posture", "p_desk_breaks",
    "n_mindful", "n_veg", "n_labels", "n_cook_home",
    "m_read", "m_digital", "m_digital_sunset", "m_niyyah", "m_kindness", "m_learn_skill", "m_single_task",
}
SENSITIVE_PROFILE_POOL = {"m_read", "m_digital", "m_digital_sunset", "m_kindness", "m_learn_skill"}


class HabitScore(BaseModel):
    task_id: str
    score: float | None = Field(default=None, ge=0, le=3, allow_inf_nan=False)
    confidence: float | None = Field(default=None, ge=0, le=1, allow_inf_nan=False)
    probabilities: dict[str, float] = Field(default_factory=dict)


class HabitRanking(BaseModel):
    items: list[HabitScore]
    source: Literal["jev", "rules"]
    ai_ranked: bool
    model: str | None = None
    cached: bool = False
    reason: str | None = None


def candidate_allowed(template: dict, user: User, flags: set[str]) -> bool:
    key = template["key"]
    if key not in RANKABLE or set(template.get("contra", [])) & flags:
        return False
    if template["level"] > LEVELS.get(user.prefs.fitness_level, 1):
        return False
    sensitive = bool(user.prefs.conditions) or (user.prefs.age is not None and user.prefs.age < 18)
    return not sensitive or key in SENSITIVE_PROFILE_POOL


async def candidate_tasks(user: User) -> list[dict]:
    db = get_db()
    challenge = await db.challenges.find_one({"user_id": str(user.id), "status": "active"},
                                             {"_id": 0, "id": {"$toString": "$_id"}}, sort=[("created_at", -1)])
    if not challenge:
        return []
    try:
        day = utcnow().astimezone(ZoneInfo(user.timezone)).date().isoformat()
    except ZoneInfoNotFoundError:
        day = utcnow().date().isoformat()
    rows = await db.daily_tasks.find({"user_id": str(user.id), "challenge_id": challenge["id"],
                                     "scheduled_date": day, "completed": False},
                                    {"_id": 0, "id": {"$toString": "$_id"}, "template_key": 1,
                                     "duration_minutes": 1, "scheduled_time": 1}).sort("scheduled_time", 1).to_list(100)
    flags = set(health_profile(user.prefs.model_dump())["flags"])
    return [row for row in rows if row["template_key"] in TEMPLATES_BY_KEY and
            candidate_allowed(TEMPLATES_BY_KEY[row["template_key"]], user, flags)][:5]


async def score_candidates(rows: list[dict], preferences: dict) -> HabitRanking:
    scored = []
    model = None
    try:
        async with asyncio.timeout(22):
            for row in rows:  # One item per call, serialized through the shared Jev adapter.
                template = TEMPLATES_BY_KEY[row["template_key"]]
                response = await decide({"preferences": preferences, "habit": {
                    "title": template["title"]["en"], "category": template["pillar"],
                    "duration_minutes": row["duration_minutes"],
                }}, {"fit": Score(
                    instructions="Score how well this everyday habit matches these goals and basic preferences as a small next step. Compare relevance and practical effort only. Do not assess medical suitability, safety, diagnosis, or religious validity. No user records are available.",
                    criteria=["low relevance", "some relevance", "good relevance", "strong relevance"],
                )})
                fit = response.scores["fit"]
                probabilities = {str(k): v for k, v in fit.probabilities.items()}
                if set(probabilities) != {"0", "1", "2", "3"} or any(not 0 <= p <= 1 for p in probabilities.values()) or abs(sum(probabilities.values()) - 1) > 0.05:
                    raise ValueError("Invalid fit distribution")
                item = HabitScore(task_id=row["id"], score=fit.score, confidence=fit.confidence, probabilities=probabilities)
                if fit.confidence < 0.5:
                    return standard_order(rows, "low_confidence")
                scored.append(item)
                model = response.model
        return HabitRanking(items=sorted(scored, key=lambda r: -r.score), source="jev", ai_ranked=True, model=model)
    except Exception as exc:
        logging.getLogger(__name__).warning("Jev ranking fallback (%s)", jev_error_code(exc))
        return standard_order(rows, "unavailable")


def standard_order(rows: list[dict], reason: str) -> HabitRanking:
    return HabitRanking(items=[HabitScore(task_id=r["id"]) for r in rows], source="rules", ai_ranked=False, reason=reason)


@router.post("/habits", response_model=HabitRanking)
async def rank_habits(user: User = Depends(get_current_user)):
    if user.coach_consent_version != CONSENT_VERSION:
        raise HTTPException(403, "coach_consent_required")
    rows = await candidate_tasks(user)
    if not rows:
        return standard_order([], "no_candidates")
    preferences = basic_preferences(user, user.language)
    signature = hashlib.sha256(json.dumps({"rows": rows, "preferences": preferences}, sort_keys=True).encode()).hexdigest()
    db = get_db()
    now = utcnow()
    scope = {"user_id": str(user.id)}
    cached = await db.habit_rankings.find_one({**scope, "signature": signature, "expires_at": {"$gt": now}}, {"_id": 0, "result": 1})
    if cached:
        return HabitRanking(**{**cached["result"], "cached": True})
    usage = await db.decision_usage.find_one_and_update(
        {**scope, "minute": now.strftime("%Y-%m-%dT%H:%M")},
        {"$inc": {"count": 1}, "$setOnInsert": {"expires_at": now + timedelta(minutes=2)}},
        upsert=True, projection={"_id": 0, "count": 1}, return_document=ReturnDocument.AFTER)
    if usage["count"] > 4:
        raise HTTPException(429, "decision_rate_limit")
    await db.decision_locks.update_one(scope, {"$setOnInsert": {"busy_until": now}}, upsert=True)
    lock = str(uuid4())
    claimed = await db.decision_locks.update_one({**scope, "busy_until": {"$lte": now}},
                                                {"$set": {"busy_until": now + timedelta(seconds=30), "lock": lock}})
    if not claimed.modified_count:
        raise HTTPException(409, "decision_busy")
    try:
        result = await score_candidates(rows, preferences)
        # Re-read eligibility after awaiting the model; never return stale completed/blocked tasks.
        current = await candidate_tasks(user)
        valid = {r["id"] for r in current}
        result.items = [item for item in result.items if item.task_id in valid]
        if result.ai_ranked:
            await db.habit_rankings.update_one(scope, {"$set": {"signature": signature, "result": result.model_dump(),
                "expires_at": now + timedelta(hours=12), "updated_at": utcnow()}}, upsert=True)
        return result
    finally:
        await asyncio.shield(db.decision_locks.update_one({**scope, "lock": lock}, {"$set": {"busy_until": utcnow()}, "$unset": {"lock": ""}}))