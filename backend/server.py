import os
from dotenv import load_dotenv

load_dotenv()

import secrets
from datetime import date, datetime, timedelta, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Body, Depends, FastAPI, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse
from pymongo.errors import DuplicateKeyError

import auth as A
import prayer as P
from content import KNOWLEDGE_CARDS, STORE_ITEMS, localize_card, localize_item
from curriculum import (TEMPLATES_BY_KEY, generate_plan, localize,
                        phase_summary)
from db import ensure_indexes, get_db
from milestones import MILESTONE_TRACKS, build_milestones, localize_milestone
from models import (Challenge, Checkin, CheckinBody, CoachBody, CoachMessage,
                    CompleteTaskBody, DailyTask, ForgotBody, LocationUpdate,
                    LoginBody, Milestone, OnboardingBody, PointTransaction,
                    Preferences, ProfileUpdate, PublicUser, RegisterBody,
                    ResetBody, StartChallengeBody, TaskTimeBody, User, utcnow)

app = FastAPI(title="Ihyaa API")

_origins = [o.strip() for o in os.environ.get("CORS_ORIGINS", "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_origin_regex=os.environ.get("CORS_ORIGIN_REGEX"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHALLENGE_DAYS = {"30_days": 30, "100_days": 100, "1_year": 365}
PRO_CHALLENGES = {"100_days", "1_year"}
CHECKIN_POINTS = 15
ALL_TASKS_BONUS = 50
STREAK_BONUS_EVERY = 7
STREAK_BONUS_POINTS = 100
GRACE_COOLDOWN_DAYS = 7          # one rescued day per week


# ------------------------------------------------------------------ utilities

def oid(value: str) -> ObjectId:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Invalid id")


def today_str() -> str:
    return date.today().isoformat()


def lang_of(user: User, override: str | None) -> str:
    return override if override in ("en", "ar", "id") else user.language


def loc_dict(user: User) -> dict | None:
    loc = user.prefs.location
    return loc.model_dump() if loc else None


def serialize_task(task: DailyTask, lang: str, timings: dict | None = None,
                   sleep_habit: str = "moderate") -> dict:
    tpl = TEMPLATES_BY_KEY.get(task.template_key)
    content = localize(tpl, lang) if tpl else {}
    when = (task.scheduled_time if task.time_overridden
            else P.resolve_time(task.anchor, timings, sleep_habit, task.scheduled_time))
    return {
        "id": str(task.id),
        "challenge_id": str(task.challenge_id),
        "day_number": task.day_number,
        "scheduled_date": task.scheduled_date,
        "scheduled_time": when,
        "time_overridden": task.time_overridden,
        "anchor": task.anchor,
        "pillar": task.pillar,
        "duration_minutes": task.duration_minutes,
        "difficulty": task.difficulty,
        "points_reward": task.points_reward,
        "completed": task.completed,
        "title": content.get("title", task.template_key),
        "description": content.get("description", ""),
        "quran_reference": content.get("quran_reference"),
        "hadith_reference": content.get("hadith_reference"),
        "science_reference": content.get("science_reference"),
    }


async def award_points(user: User, amount: int, source: str, description: str) -> None:
    db = get_db()
    await db.users.update_one(
        {"_id": oid(str(user.id))},
        {"$inc": {"points_balance": amount, "lifetime_points": max(amount, 0)}},
    )
    await db.point_transactions.insert_one(PointTransaction(
        user_id=str(user.id), amount=amount,
        type="earned" if amount > 0 else "redeemed",
        source=source, description=description,
    ).to_mongo())


async def claim_daily_bonus(user_id: str, day: str, kind: str) -> bool:
    """Insert-once marker so a bonus cannot be farmed by toggling a task."""
    try:
        await get_db().daily_bonuses.insert_one(
            {"user_id": user_id, "bonus_date": day, "kind": kind, "created_at": utcnow()})
        return True
    except DuplicateKeyError:
        return False


async def active_challenge(user_id: str) -> Challenge | None:
    doc = await get_db().challenges.find_one(
        {"user_id": str(user_id), "status": "active"}, sort=[("created_at", -1)])
    return Challenge.from_mongo(doc)


async def current_user(request: Request) -> User:
    return await A.get_current_user(request)


# ------------------------------------------------------------------ lifecycle

@app.on_event("startup")
async def startup() -> None:
    await ensure_indexes()
    db = get_db()
    for email_key, pass_key, name, role in (
        ("ADMIN_EMAIL", "ADMIN_PASSWORD", "Ihyaa Admin", "admin"),
        ("DEMO_EMAIL", "DEMO_PASSWORD", "Demo User", "user"),
    ):
        email = os.environ.get(email_key)
        password = os.environ.get(pass_key)
        if not email or not password:
            continue
        existing = await db.users.find_one({"email": email.lower()})
        if existing is None:
            user = User(email=email.lower(), name=name, role=role,
                        password_hash=A.hash_password(password))
            await db.users.insert_one(user.to_mongo())
        elif not A.verify_password(password, existing.get("password_hash") or ""):
            await db.users.update_one({"_id": existing["_id"]},
                                      {"$set": {"password_hash": A.hash_password(password)}})


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok", "app": "Ihyaa", "time": utcnow().isoformat()}


# ------------------------------------------------------------------ auth

def _issue(response: Response, user: User) -> dict:
    access = A.create_access_token(str(user.id), user.email)
    refresh = A.create_refresh_token(str(user.id))
    A.set_auth_cookies(response, access, refresh)
    return {
        "access_token": access,
        "refresh_token": refresh,
        "user": PublicUser.of(user).model_dump(),
    }


@app.post("/api/auth/register")
async def register(body: RegisterBody, response: Response) -> dict:
    db = get_db()
    email = body.email.lower()
    if await db.users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="An account with this email already exists")
    user = User(email=email, name=body.name.strip() or email.split("@")[0],
                language=body.language if body.language in ("en", "ar", "id") else "en",
                password_hash=A.hash_password(body.password))
    result = await db.users.insert_one(user.to_mongo())
    user.id = str(result.inserted_id)
    return _issue(response, user)


@app.post("/api/auth/login")
async def login(body: LoginBody, request: Request, response: Response) -> dict:
    db = get_db()
    email = body.email.lower()
    # Keyed on the email alone: the ingress proxy rotates client IPs, so an
    # IP-scoped counter would never reach the threshold.
    await A.check_lockout(email)
    doc = await db.users.find_one({"email": email})
    if not doc or not A.verify_password(body.password, doc.get("password_hash") or ""):
        await A.record_failure(email)
        raise HTTPException(status_code=401, detail="Invalid email or password")
    await A.clear_failures(email)
    return _issue(response, User.from_mongo(doc))


@app.post("/api/auth/refresh")
async def refresh_token(request: Request, response: Response) -> dict:
    import jwt
    # An explicit header always wins over an ambient cookie.
    token = request.headers.get("X-Refresh-Token") or request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="No refresh token")
    try:
        payload = jwt.decode(token, os.environ["JWT_SECRET"], algorithms=["HS256"])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    doc = await get_db().users.find_one({"_id": oid(payload["sub"])})
    user = User.from_mongo(doc)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return _issue(response, user)


@app.post("/api/auth/google/session")
async def google_session(response: Response, x_session_id: str = Body(..., embed=True, alias="session_id")) -> dict:
    """Exchange an Emergent Google session_id for an Ihyaa session."""
    data = await A.fetch_emergent_session(x_session_id)
    db = get_db()
    email = (data.get("email") or "").lower()
    if not email:
        raise HTTPException(status_code=401, detail="Google session has no email")
    doc = await db.users.find_one({"email": email})
    if doc is None:
        user = User(email=email, name=data.get("name") or email.split("@")[0],
                    picture=data.get("picture"), auth_provider="google")
        result = await db.users.insert_one(user.to_mongo())
        user.id = str(result.inserted_id)
    else:
        await db.users.update_one({"_id": doc["_id"]}, {"$set": {
            "picture": data.get("picture") or doc.get("picture"),
            "name": doc.get("name") or data.get("name") or "",
        }})
        user = User.from_mongo(await db.users.find_one({"_id": doc["_id"]}))

    session_token = data.get("session_token") or secrets.token_urlsafe(32)
    await db.user_sessions.insert_one({
        "user_id": str(user.id),
        "session_token": session_token,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
        "created_at": datetime.now(timezone.utc),
    })
    payload = _issue(response, user)
    payload["session_token"] = session_token
    return payload


@app.post("/api/auth/logout")
async def logout(request: Request, response: Response) -> dict:
    token = request.headers.get("Authorization", "").replace("Bearer ", "") or request.cookies.get("access_token")
    if token:
        await get_db().user_sessions.delete_many({"session_token": token})
    A.clear_auth_cookies(response)
    return {"ok": True}


@app.get("/api/auth/me")
async def me(user: User = Depends(current_user)) -> dict:
    return PublicUser.of(user).model_dump()


@app.post("/api/auth/forgot-password")
async def forgot_password(body: ForgotBody) -> dict:
    db = get_db()
    doc = await db.users.find_one({"email": body.email.lower()})
    if doc:
        token = secrets.token_urlsafe(32)
        await db.password_reset_tokens.insert_one({
            "token": token, "user_id": str(doc["_id"]), "used": False,
            "expires_at": datetime.now(timezone.utc) + timedelta(hours=1),
        })
        print(f"[Ihyaa] password reset token for {body.email}: {token}")
    return {"ok": True, "message": "If that email exists, a reset link has been sent."}


@app.post("/api/auth/reset-password")
async def reset_password(body: ResetBody) -> dict:
    db = get_db()
    row = await db.password_reset_tokens.find_one({"token": body.token, "used": False})
    if not row:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    expires = row["expires_at"]
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    await db.users.update_one({"_id": oid(row["user_id"])},
                              {"$set": {"password_hash": A.hash_password(body.password)}})
    await db.password_reset_tokens.update_one({"_id": row["_id"]}, {"$set": {"used": True}})
    return {"ok": True}


# ------------------------------------------------------------------ profile

@app.put("/api/profile")
async def update_profile(body: ProfileUpdate, user: User = Depends(current_user)) -> dict:
    updates: dict = {}
    if body.name is not None:
        updates["name"] = body.name.strip()
    if body.language in ("en", "ar", "id"):
        updates["language"] = body.language
    if body.theme in ("light", "dark"):
        updates["theme"] = body.theme
    if body.timezone:
        updates["timezone"] = body.timezone
    if body.prefs is not None:
        updates["prefs"] = body.prefs.model_dump()
    if updates:
        await get_db().users.update_one({"_id": oid(str(user.id))}, {"$set": updates})
    doc = await get_db().users.find_one({"_id": oid(str(user.id))})
    return PublicUser.of(User.from_mongo(doc)).model_dump()


@app.post("/api/onboarding")
async def complete_onboarding(body: OnboardingBody, user: User = Depends(current_user)) -> dict:
    db = get_db()
    prefs = body.prefs
    challenge_type = prefs.preferred_challenge
    if challenge_type in PRO_CHALLENGES and not user.is_pro:
        challenge_type = "30_days"
        prefs.preferred_challenge = "30_days"

    updates: dict = {"prefs": prefs.model_dump(), "onboarding_completed": True}
    if body.name:
        updates["name"] = body.name.strip()
    if body.language in ("en", "ar", "id"):
        updates["language"] = body.language
    if body.timezone:
        updates["timezone"] = body.timezone
    await db.users.update_one({"_id": oid(str(user.id))}, {"$set": updates})
    fresh = User.from_mongo(await db.users.find_one({"_id": oid(str(user.id))}))

    challenge_payload = None
    if body.start_challenge:
        challenge_payload = await _create_challenge(fresh, challenge_type, None)

    return {"user": PublicUser.of(fresh).model_dump(), "challenge": challenge_payload}


# ------------------------------------------------------------------ challenge

async def _create_challenge(user: User, challenge_type: str, start_date: str | None) -> dict:
    db = get_db()
    if challenge_type not in CHALLENGE_DAYS:
        raise HTTPException(status_code=400, detail="Unknown challenge type")
    if challenge_type in PRO_CHALLENGES and not user.is_pro:
        raise HTTPException(status_code=402, detail="pro_required")

    total = CHALLENGE_DAYS[challenge_type]
    start = date.fromisoformat(start_date) if start_date else date.today()
    await db.challenges.update_many({"user_id": str(user.id), "status": "active"},
                                   {"$set": {"status": "abandoned"}})
    challenge = Challenge(user_id=str(user.id), challenge_type=challenge_type,
                          start_date=start.isoformat(),
                          end_date=(start + timedelta(days=total - 1)).isoformat(),
                          total_days=total)
    result = await db.challenges.insert_one(challenge.to_mongo())
    challenge.id = str(result.inserted_id)

    plan = generate_plan(user.prefs.model_dump(), total, start, challenge_type)
    docs = [DailyTask(user_id=str(user.id), challenge_id=str(challenge.id), **row).to_mongo()
            for row in plan]
    if docs:
        await db.daily_tasks.insert_many(docs)

    stones = [Milestone(user_id=str(user.id), challenge_id=str(challenge.id), **row).to_mongo()
              for row in build_milestones(challenge_type, total, start)]
    if stones:
        await db.milestones.insert_many(stones)
    return _serialize_challenge(challenge, user.language)


def _serialize_challenge(c: Challenge, lang: str = "en") -> dict:
    start = date.fromisoformat(c.start_date)
    current_day = max(1, min(c.total_days, (date.today() - start).days + 1))
    return {
        "id": str(c.id),
        "challenge_type": c.challenge_type,
        "status": c.status,
        "start_date": c.start_date,
        "end_date": c.end_date,
        "total_days": c.total_days,
        "current_day": current_day,
        "has_milestones": c.challenge_type in MILESTONE_TRACKS,
        "phase": phase_summary(current_day, c.challenge_type, lang),
    }


@app.post("/api/challenges")
async def start_challenge(body: StartChallengeBody, user: User = Depends(current_user)) -> dict:
    return await _create_challenge(user, body.challenge_type, body.start_date)


@app.get("/api/challenges/active")
async def get_active_challenge(lang: str | None = Query(None),
                               user: User = Depends(current_user)) -> dict | None:
    c = await active_challenge(str(user.id))
    return _serialize_challenge(c, lang_of(user, lang)) if c else None


@app.post("/api/challenges/regenerate")
async def regenerate(user: User = Depends(current_user)) -> dict:
    """Re-plan the remaining days from today using the latest preferences.

    Completed days are preserved; the future is rebuilt.
    """
    db = get_db()
    c = await active_challenge(str(user.id))
    if not c:
        raise HTTPException(status_code=404, detail="No active challenge")
    today = today_str()
    await db.daily_tasks.delete_many({"challenge_id": str(c.id), "scheduled_date": {"$gte": today},
                                      "completed": False})
    start = date.fromisoformat(c.start_date)
    plan = generate_plan(user.prefs.model_dump(), c.total_days, start, c.challenge_type)
    kept = {(t["scheduled_date"], t["template_key"]) async for t in
            db.daily_tasks.find({"challenge_id": str(c.id)}, {"scheduled_date": 1, "template_key": 1})}
    docs = [DailyTask(user_id=str(user.id), challenge_id=str(c.id), **row).to_mongo()
            for row in plan
            if row["scheduled_date"] >= today and (row["scheduled_date"], row["template_key"]) not in kept]
    if docs:
        await db.daily_tasks.insert_many(docs)
    return {"ok": True, "regenerated_tasks": len(docs),
            "challenge": _serialize_challenge(c, user.language)}


# ------------------------------------------------------------------ tasks

@app.get("/api/tasks/today")
async def tasks_today(lang: str | None = Query(None), user: User = Depends(current_user)) -> dict:
    db = get_db()
    language = lang_of(user, lang)
    c = await active_challenge(str(user.id))
    if not c:
        return {"challenge": None, "tasks": [], "date": today_str(), "prayer_times": {},
                "milestones": []}
    today = today_str()
    timings = await P.timings_for_day(loc_dict(user), user.prefs.prayer_method,
                                     user.prefs.prayer_school, today)
    cursor = db.daily_tasks.find({"challenge_id": str(c.id), "scheduled_date": today})
    tasks = [serialize_task(DailyTask.from_mongo(d), language, timings, user.prefs.sleep_habit)
             async for d in cursor]
    tasks.sort(key=lambda t: (t["scheduled_time"], t["pillar"]))

    stones = []
    async for d in db.milestones.find({"challenge_id": str(c.id), "start_date": {"$lte": today},
                                       "end_date": {"$gte": today}}).sort("kind", 1):
        stones.append(localize_milestone(d, language))

    return {"challenge": _serialize_challenge(c, language), "tasks": tasks, "date": today,
            "prayer_times": timings, "milestones": stones}


@app.get("/api/tasks")
async def tasks_range(date_from: str = Query(..., alias="from"), date_to: str = Query(..., alias="to"),
                      lang: str | None = Query(None), user: User = Depends(current_user)) -> list[dict]:
    db = get_db()
    c = await active_challenge(str(user.id))
    if not c:
        return []
    cursor = db.daily_tasks.find({"challenge_id": str(c.id),
                                  "scheduled_date": {"$gte": date_from, "$lte": date_to}})
    rows = [DailyTask.from_mongo(d) async for d in cursor]
    timings = await P.timings_for_dates(loc_dict(user), user.prefs.prayer_method,
                                        user.prefs.prayer_school,
                                        sorted({r.scheduled_date for r in rows}))
    language = lang_of(user, lang)
    out = [serialize_task(r, language, timings.get(r.scheduled_date), user.prefs.sleep_habit)
           for r in rows]
    out.sort(key=lambda t: (t["scheduled_date"], t["scheduled_time"]))
    return out


@app.post("/api/tasks/{task_id}/complete")
async def complete_task(task_id: str, body: CompleteTaskBody,
                        user: User = Depends(current_user)) -> dict:
    db = get_db()
    doc = await db.daily_tasks.find_one({"_id": oid(task_id), "user_id": str(user.id)})
    task = DailyTask.from_mongo(doc)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.completed == body.completed:
        fresh = User.from_mongo(await db.users.find_one({"_id": oid(str(user.id))}))
        return {"task": serialize_task(task, user.language), "user": PublicUser.of(fresh).model_dump(),
                "awarded": 0, "bonus": 0}

    await db.daily_tasks.update_one(
        {"_id": oid(task_id)},
        {"$set": {"completed": body.completed,
                  "completed_at": utcnow() if body.completed else None}})
    task.completed = body.completed

    awarded = 0
    bonus = 0
    tpl = TEMPLATES_BY_KEY.get(task.template_key)
    label = (tpl["title"]["en"] if tpl else task.template_key)
    if body.completed:
        awarded = task.points_reward
        await award_points(user, awarded, "task_complete", f"Completed: {label}")
        remaining = await db.daily_tasks.count_documents(
            {"challenge_id": str(task.challenge_id), "scheduled_date": task.scheduled_date,
             "completed": False})
        if remaining == 0 and await claim_daily_bonus(str(user.id), task.scheduled_date, "all_tasks"):
            bonus = ALL_TASKS_BONUS
            await award_points(user, bonus, "all_tasks", f"All tasks complete on {task.scheduled_date}")
    else:
        awarded = -task.points_reward
        await award_points(user, awarded, "task_uncomplete", f"Undone: {label}")

    fresh = User.from_mongo(await db.users.find_one({"_id": oid(str(user.id))}))
    return {"task": serialize_task(task, user.language),
            "user": PublicUser.of(fresh).model_dump(),
            "awarded": awarded, "bonus": bonus}


@app.put("/api/tasks/{task_id}/time")
async def set_task_time(task_id: str, body: TaskTimeBody, user: User = Depends(current_user)) -> dict:
    res = await get_db().daily_tasks.update_one(
        {"_id": oid(task_id), "user_id": str(user.id)},
        {"$set": {"scheduled_time": body.scheduled_time, "time_overridden": True}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True, "scheduled_time": body.scheduled_time, "time_overridden": True}


@app.delete("/api/tasks/{task_id}/time")
async def reset_task_time(task_id: str, user: User = Depends(current_user)) -> dict:
    """Drop a manual override so the habit follows the adhan again."""
    res = await get_db().daily_tasks.update_one(
        {"_id": oid(task_id), "user_id": str(user.id)},
        {"$set": {"time_overridden": False}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True, "time_overridden": False}


# ------------------------------------------------------------------ prayer times

@app.get("/api/prayer/today")
async def prayer_today(day: str | None = Query(None), user: User = Depends(current_user)) -> dict:
    loc = loc_dict(user)
    timings = await P.timings_for_day(loc, user.prefs.prayer_method,
                                      user.prefs.prayer_school, day)
    return {
        "date": day or today_str(),
        "timings": timings,
        "location": loc,
        "method": user.prefs.prayer_method,
        "method_name": P.METHODS.get(user.prefs.prayer_method, "Muslim World League"),
        "school": user.prefs.prayer_school,
        "using_real_times": bool(timings),
    }


@app.get("/api/prayer/methods")
async def prayer_methods() -> dict:
    return {"methods": [{"id": k, "name": v} for k, v in sorted(P.METHODS.items())],
            "schools": [{"id": 0, "name": "Shafi'i / Maliki / Hanbali"},
                        {"id": 1, "name": "Hanafi"}]}


@app.get("/api/cities/search")
async def cities_search(q: str = Query(..., min_length=2), _: User = Depends(current_user)) -> list[dict]:
    return await P.search_city(q)


@app.put("/api/profile/location")
async def set_location(body: LocationUpdate, user: User = Depends(current_user)) -> dict:
    prefs = user.prefs.model_copy()
    prefs.location = body.location
    prefs.prayer_method = (body.prayer_method if body.prayer_method is not None
                           else P.default_method(body.location.country_code))
    if body.prayer_school is not None:
        prefs.prayer_school = body.prayer_school
    await get_db().users.update_one({"_id": oid(str(user.id))},
                                    {"$set": {"prefs": prefs.model_dump()}})
    fresh = User.from_mongo(await get_db().users.find_one({"_id": oid(str(user.id))}))
    timings = await P.timings_for_day(prefs.location.model_dump(), prefs.prayer_method,
                                      prefs.prayer_school)
    return {"user": PublicUser.of(fresh).model_dump(), "timings": timings}


# ------------------------------------------------------------------ milestones

@app.get("/api/milestones")
async def list_milestones(lang: str | None = Query(None),
                          user: User = Depends(current_user)) -> dict:
    db = get_db()
    c = await active_challenge(str(user.id))
    if not c:
        return {"current": [], "upcoming": [], "past": []}
    language = lang_of(user, lang)
    today = today_str()
    current, upcoming, past = [], [], []
    async for d in db.milestones.find({"challenge_id": str(c.id)}).sort("start_date", 1):
        row = localize_milestone(d, language)
        if row["start_date"] <= today <= row["end_date"]:
            current.append(row)
        elif row["start_date"] > today:
            upcoming.append(row)
        else:
            past.append(row)
    return {"current": current, "upcoming": upcoming[:6], "past": past[-8:]}


@app.post("/api/milestones/{milestone_id}/complete")
async def complete_milestone(milestone_id: str, body: CompleteTaskBody,
                             user: User = Depends(current_user)) -> dict:
    db = get_db()
    doc = await db.milestones.find_one({"_id": oid(milestone_id), "user_id": str(user.id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Milestone not found")
    if bool(doc.get("completed")) == body.completed:
        fresh = User.from_mongo(await db.users.find_one({"_id": oid(str(user.id))}))
        return {"milestone": localize_milestone(doc, user.language),
                "user": PublicUser.of(fresh).model_dump(), "awarded": 0}

    await db.milestones.update_one(
        {"_id": oid(milestone_id)},
        {"$set": {"completed": body.completed,
                  "completed_at": utcnow() if body.completed else None}})
    awarded = doc["points_reward"] if body.completed else -doc["points_reward"]
    await award_points(user, awarded, "milestone",
                       f"{'Completed' if body.completed else 'Undone'} milestone: {doc['template_key']}")
    doc["completed"] = body.completed
    fresh = User.from_mongo(await db.users.find_one({"_id": oid(str(user.id))}))
    return {"milestone": localize_milestone(doc, user.language),
            "user": PublicUser.of(fresh).model_dump(), "awarded": awarded}


@app.get("/api/tasks/calendar.ics")
async def calendar_ics(days: int = Query(30, ge=1, le=365), lang: str | None = Query(None),
                       user: User = Depends(current_user)) -> PlainTextResponse:
    db = get_db()
    c = await active_challenge(str(user.id))
    if not c:
        raise HTTPException(status_code=404, detail="No active challenge")
    start = today_str()
    end = (date.today() + timedelta(days=days)).isoformat()
    cursor = db.daily_tasks.find({"challenge_id": str(c.id),
                                  "scheduled_date": {"$gte": start, "$lte": end}})
    rows = [DailyTask.from_mongo(d) async for d in cursor]
    timings = await P.timings_for_dates(loc_dict(user), user.prefs.prayer_method,
                                        user.prefs.prayer_school,
                                        sorted({r.scheduled_date for r in rows}))
    language = lang_of(user, lang)
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Ihyaa//Revival//EN",
             "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:Ihyaa"]
    stamp = utcnow().strftime("%Y%m%dT%H%M%SZ")
    for task in rows:
        s = serialize_task(task, language, timings.get(task.scheduled_date), user.prefs.sleep_habit)
        hh, mm = (int(x) for x in s["scheduled_time"].split(":"))
        begin = datetime.fromisoformat(task.scheduled_date).replace(hour=hh, minute=mm)
        finish = begin + timedelta(minutes=task.duration_minutes)
        summary = f"Ihyaa Day {task.day_number}: {s['title']}"
        desc = (s.get("description") or "").replace("\n", " ")
        lines += [
            "BEGIN:VEVENT",
            f"UID:{task.id}@ihyaa.app",
            f"DTSTAMP:{stamp}",
            f"DTSTART:{begin.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND:{finish.strftime('%Y%m%dT%H%M%S')}",
            f"SUMMARY:{summary}",
            f"DESCRIPTION:{desc}",
            f"CATEGORIES:{task.pillar.upper()}",
            "BEGIN:VALARM", "TRIGGER:-PT10M", "ACTION:DISPLAY",
            f"DESCRIPTION:{summary}", "END:VALARM",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return PlainTextResponse("\r\n".join(lines), media_type="text/calendar",
                             headers={"Content-Disposition": "attachment; filename=ihyaa.ics"})


# ------------------------------------------------------------------ check-in

@app.get("/api/checkins/today")
async def checkin_today(user: User = Depends(current_user)) -> dict | None:
    doc = await get_db().checkins.find_one({"user_id": str(user.id), "checkin_date": today_str()})
    if not doc:
        return None
    c = Checkin.from_mongo(doc)
    return {"id": str(c.id), "checkin_date": c.checkin_date, "mood_rating": c.mood_rating,
            "energy_rating": c.energy_rating, "gratitude_note": c.gratitude_note,
            "reflection_note": c.reflection_note, "tasks_completed": c.tasks_completed,
            "tasks_total": c.tasks_total, "points_earned": c.points_earned}


@app.post("/api/checkins")
async def create_checkin(body: CheckinBody, user: User = Depends(current_user)) -> dict:
    db = get_db()
    today = today_str()
    if await db.checkins.find_one({"user_id": str(user.id), "checkin_date": today}):
        raise HTTPException(status_code=400, detail="already_checked_in")

    c = await active_challenge(str(user.id))
    total = done = 0
    if c:
        total = await db.daily_tasks.count_documents(
            {"challenge_id": str(c.id), "scheduled_date": today})
        done = await db.daily_tasks.count_documents(
            {"challenge_id": str(c.id), "scheduled_date": today, "completed": True})

    yesterday = (date.today() - timedelta(days=1)).isoformat()
    two_days_ago = (date.today() - timedelta(days=2)).isoformat()
    grace_dates = list(user.grace_used_dates or [])
    grace_cutoff = (date.today() - timedelta(days=GRACE_COOLDOWN_DAYS)).isoformat()
    grace_available = not any(d > grace_cutoff for d in grace_dates)

    rescued = False
    if user.last_checkin_date == yesterday:
        streak = user.current_streak + 1
    elif (user.last_checkin_date == two_days_ago and user.current_streak > 0
            and grace_available):
        # Streak Rescue: exactly one missed day is forgiven, once a week.
        streak = user.current_streak + 1
        rescued = True
        grace_dates.append(yesterday)
    else:
        streak = 1
    longest = max(user.longest_streak, streak)

    points = CHECKIN_POINTS
    streak_bonus = STREAK_BONUS_POINTS if streak % STREAK_BONUS_EVERY == 0 else 0

    checkin = Checkin(user_id=str(user.id), challenge_id=str(c.id) if c else None,
                      checkin_date=today, mood_rating=body.mood_rating,
                      energy_rating=body.energy_rating, gratitude_note=body.gratitude_note,
                      reflection_note=body.reflection_note, tasks_completed=done,
                      tasks_total=total, points_earned=points + streak_bonus)
    await db.checkins.insert_one(checkin.to_mongo())
    await db.users.update_one({"_id": oid(str(user.id))},
                              {"$set": {"current_streak": streak, "longest_streak": longest,
                                        "last_checkin_date": today,
                                        "grace_used_dates": grace_dates[-12:]}})
    await award_points(user, points, "checkin", f"Daily check-in {today}")
    if streak_bonus:
        await award_points(user, streak_bonus, "streak_bonus", f"{streak}-day streak")

    fresh = User.from_mongo(await db.users.find_one({"_id": oid(str(user.id))}))
    next_grace = None
    if rescued:
        next_grace = (date.today() + timedelta(days=GRACE_COOLDOWN_DAYS)).isoformat()
    elif not grace_available and grace_dates:
        used = max(grace_dates)
        next_grace = (date.fromisoformat(used) + timedelta(days=GRACE_COOLDOWN_DAYS)).isoformat()
    return {"points_earned": points + streak_bonus, "streak_bonus": streak_bonus,
            "streak": streak, "tasks_completed": done, "tasks_total": total,
            "streak_rescued": rescued, "grace_available_on": next_grace,
            "user": PublicUser.of(fresh).model_dump()}


# ------------------------------------------------------------------ progress

@app.get("/api/progress/summary")
async def progress_summary(user: User = Depends(current_user)) -> dict:
    db = get_db()
    c = await active_challenge(str(user.id))
    pillars = {p: {"total": 0, "done": 0} for p in ("physical", "nutrition", "mental", "spiritual")}
    total = done = 0
    last7: list[dict] = []

    if c:
        today = today_str()
        cursor = db.daily_tasks.find({"challenge_id": str(c.id), "scheduled_date": {"$lte": today}},
                                     {"pillar": 1, "completed": 1, "scheduled_date": 1})
        by_date: dict[str, dict] = {}
        async for d in cursor:
            total += 1
            p = pillars.setdefault(d["pillar"], {"total": 0, "done": 0})
            p["total"] += 1
            slot = by_date.setdefault(d["scheduled_date"], {"total": 0, "done": 0})
            slot["total"] += 1
            if d.get("completed"):
                done += 1
                p["done"] += 1
                slot["done"] += 1
        for i in range(6, -1, -1):
            day = (date.today() - timedelta(days=i)).isoformat()
            slot = by_date.get(day, {"total": 0, "done": 0})
            rate = round(slot["done"] / slot["total"] * 100) if slot["total"] else 0
            last7.append({"date": day, "total": slot["total"], "done": slot["done"], "rate": rate})

    checkins = await db.checkins.count_documents({"user_id": str(user.id)})
    grace_cutoff = (date.today() - timedelta(days=GRACE_COOLDOWN_DAYS)).isoformat()
    recent_grace = [d for d in (user.grace_used_dates or []) if d > grace_cutoff]
    milestones_done = milestones_total = 0
    if c:
        milestones_total = await db.milestones.count_documents({"challenge_id": str(c.id)})
        milestones_done = await db.milestones.count_documents(
            {"challenge_id": str(c.id), "completed": True})
    return {
        "challenge": _serialize_challenge(c, user.language) if c else None,
        "points_balance": user.points_balance,
        "lifetime_points": user.lifetime_points,
        "current_streak": user.current_streak,
        "longest_streak": user.longest_streak,
        "total_tasks": total,
        "completed_tasks": done,
        "completion_rate": round(done / total * 100) if total else 0,
        "pillars": pillars,
        "last_7_days": last7,
        "total_checkins": checkins,
        "milestones_total": milestones_total,
        "milestones_done": milestones_done,
        "grace_available": len(recent_grace) == 0,
        "grace_available_on": (
            (date.fromisoformat(max(recent_grace)) + timedelta(days=GRACE_COOLDOWN_DAYS)).isoformat()
            if recent_grace else None),
        "grace_used_dates": user.grace_used_dates or [],
    }


@app.get("/api/points/transactions")
async def point_history(user: User = Depends(current_user)) -> list[dict]:
    cursor = get_db().point_transactions.find({"user_id": str(user.id)}).sort("created_at", -1).limit(50)
    out = []
    async for d in cursor:
        t = PointTransaction.from_mongo(d)
        out.append({"id": str(t.id), "amount": t.amount, "type": t.type, "source": t.source,
                    "description": t.description, "created_at": t.created_at.isoformat()})
    return out


# ------------------------------------------------------------------ store

@app.get("/api/store/items")
async def store_items(lang: str | None = Query(None), user: User = Depends(current_user)) -> list[dict]:
    language = lang_of(user, lang)
    return [localize_item(i, language) for i in STORE_ITEMS]


@app.post("/api/store/redeem/{item_id}")
async def redeem(item_id: str, user: User = Depends(current_user)) -> dict:
    item = next((i for i in STORE_ITEMS if i["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db = get_db()
    base = date.today()
    if user.pro_until:
        existing = date.fromisoformat(user.pro_until)
        if existing > base:
            base = existing
    pro_until = (base + timedelta(days=item["grants_pro_days"])).isoformat()

    # Conditional update: the balance check and the debit happen in one atomic op,
    # so concurrent redemptions cannot overspend.
    result = await db.users.update_one(
        {"_id": oid(str(user.id)), "points_balance": {"$gte": item["points_cost"]}},
        {"$inc": {"points_balance": -item["points_cost"]},
         "$set": {"is_pro": True, "pro_until": pro_until}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=400, detail="insufficient_points")

    await db.point_transactions.insert_one(PointTransaction(
        user_id=str(user.id), amount=-item["points_cost"], type="redeemed",
        source="store_redeem", description=f"Redeemed: {item['name']['en']}").to_mongo())
    await db.redemptions.insert_one({"user_id": str(user.id), "item_id": item_id,
                                     "points_spent": item["points_cost"],
                                     "pro_until": pro_until,
                                     "created_at": utcnow()})
    fresh = User.from_mongo(await db.users.find_one({"_id": oid(str(user.id))}))
    return {"ok": True, "pro_until": pro_until, "user": PublicUser.of(fresh).model_dump()}


# ------------------------------------------------------------------ knowledge

@app.get("/api/knowledge")
async def knowledge(lang: str | None = Query(None), pillar: str | None = Query(None),
                    user: User = Depends(current_user)) -> list[dict]:
    language = lang_of(user, lang)
    cards = KNOWLEDGE_CARDS if not pillar or pillar == "all" else [
        c for c in KNOWLEDGE_CARDS if c["pillar"] == pillar]
    return [localize_card(c, language) for c in cards]


# ------------------------------------------------------------------ AI coach

COACH_SYSTEM = """You are Ustadh Ihyaa, the AI wellness coach inside the Ihyaa app.

Ihyaa helps Muslims become healthier in body, mind and soul through short daily
habits grounded in the Quran, authentic Sunnah, and peer-reviewed clinical science.

Rules you never break:
- Everything you suggest must be 100% halal and within mainstream Sunni fiqh. Never
  suggest alcohol, non-halal gelatin/collagen, riba-based products, or practices with
  shirk associations (yoga mantras, chakra work, etc.). Neutral movement is fine.
- When you cite the Quran, give surah:ayah. When you cite hadith, name the collection.
  Never invent a hadith. If unsure of a hadith's authenticity, say so plainly.
- You are not a doctor. For medication, pregnancy, chronic illness, eating disorders or
  mental-health crises, advise the user to see a qualified physician. Say this clearly.
- Keep answers SHORT and warm: at most 3 short paragraphs, under 120 words total.
- Write in PLAIN TEXT only. Never use markdown, asterisks, bullet characters or emoji.
- Honour the "1% better" method: always give the SMALLEST next step, not a full program.
- Reply in the SAME language the user writes in (English, Bahasa Indonesia, or Arabic).
- Open with a brief Islamic greeting only on the first message of a conversation.
"""


def _coach_chat(session_id: str, context: str):
    from emergentintegrations.llm.chat import LlmChat
    provider = os.environ.get("COACH_PROVIDER", "anthropic")
    model = os.environ.get("COACH_MODEL", "claude-sonnet-4-6")
    return LlmChat(
        api_key=os.environ["EMERGENT_LLM_KEY"],
        session_id=session_id,
        system_message=COACH_SYSTEM + "\n\n" + context,
    ).with_model(provider, model)


async def _coach_context(user: User) -> str:
    db = get_db()
    c = await active_challenge(str(user.id))
    parts = [
        f"User name: {user.name or 'friend'}",
        f"Preferred language: {user.language}",
        f"Fitness level: {user.prefs.fitness_level}",
        f"Spiritual level: {user.prefs.spiritual_level}",
        f"Sleep pattern: {user.prefs.sleep_habit}",
        f"Goals: {', '.join(user.prefs.health_goals) or 'not set'}",
        f"Dietary focus: {', '.join(user.prefs.dietary_preferences) or 'standard halal'}",
        f"Current streak: {user.current_streak} days",
        f"Points: {user.points_balance}",
    ]
    if c:
        s = _serialize_challenge(c, "en")
        parts.append(f"Challenge: {s['challenge_type']}, on day {s['current_day']} of {s['total_days']}")
        parts.append(f"Current phase: {s['phase']['name']} (phase {s['phase']['index']} of {s['phase']['total']})")
        timings = await P.timings_for_day(loc_dict(user), user.prefs.prayer_method,
                                         user.prefs.prayer_school)
        if timings:
            city = (user.prefs.location.city if user.prefs.location else "") or "their city"
            parts.append(f"Today's prayer times in {city}: " +
                         ", ".join(f"{k} {v}" for k, v in timings.items()))
        cursor = db.daily_tasks.find({"challenge_id": str(c.id), "scheduled_date": today_str()})
        todays = []
        async for d in cursor:
            t = DailyTask.from_mongo(d)
            tpl = TEMPLATES_BY_KEY.get(t.template_key)
            todays.append(f"{tpl['title']['en'] if tpl else t.template_key} "
                          f"({t.pillar}, {t.duration_minutes}min, "
                          f"{'done' if t.completed else 'not done'})")
        if todays:
            parts.append("Today's tasks: " + "; ".join(todays))
    else:
        parts.append("The user has not started a challenge yet.")
    return "USER CONTEXT (do not repeat verbatim):\n" + "\n".join(parts)


@app.get("/api/coach/history")
async def coach_history(user: User = Depends(current_user)) -> list[dict]:
    cursor = get_db().coach_messages.find({"user_id": str(user.id)}).sort("created_at", 1).limit(200)
    out = []
    async for d in cursor:
        m = CoachMessage.from_mongo(d)
        out.append({"id": str(m.id), "role": m.role, "content": m.content,
                    "created_at": m.created_at.isoformat()})
    return out


@app.delete("/api/coach/history")
async def clear_coach_history(user: User = Depends(current_user)) -> dict:
    await get_db().coach_messages.delete_many({"user_id": str(user.id)})
    return {"ok": True}


@app.post("/api/coach/chat")
async def coach_chat(body: CoachBody, user: User = Depends(current_user)) -> StreamingResponse:
    from emergentintegrations.llm.chat import StreamDone, TextDelta, UserMessage

    db = get_db()
    text = body.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    await db.coach_messages.insert_one(
        CoachMessage(user_id=str(user.id), role="user", content=text).to_mongo())

    history = []
    cursor = db.coach_messages.find({"user_id": str(user.id)}).sort("created_at", 1).limit(40)
    async for d in cursor:
        history.append({"role": d["role"], "content": d["content"]})

    context = await _coach_context(user)
    chat = _coach_chat(f"coach_{user.id}", context)

    prior = history[:-1][-12:]
    if prior:
        transcript = "\n".join(
            f"{'User' if m['role'] == 'user' else 'You'}: {m['content']}" for m in prior)
        prompt = f"Recent conversation so far:\n{transcript}\n\nUser's new message: {text}"
    else:
        prompt = text

    async def gen():
        collected: list[str] = []
        try:
            async for event in chat.stream_message(UserMessage(text=prompt)):
                if isinstance(event, TextDelta):
                    collected.append(event.content)
                    yield f"data: {event.content}\n\n".replace("\n\n\n", "\n\n")
                elif isinstance(event, StreamDone):
                    break
        except Exception as exc:  # surface the failure to the client
            yield f"event: error\ndata: {exc}\n\n"
        finally:
            reply = "".join(collected)
            if reply:
                await db.coach_messages.insert_one(
                    CoachMessage(user_id=str(user.id), role="assistant", content=reply).to_mongo())
            yield "event: done\ndata: end\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.post("/api/coach/chat-sync")
async def coach_chat_sync(body: CoachBody, user: User = Depends(current_user)) -> dict:
    """Non-streaming fallback used by the mobile client when SSE is unavailable."""
    from emergentintegrations.llm.chat import StreamDone, TextDelta, UserMessage

    db = get_db()
    text = body.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    await db.coach_messages.insert_one(
        CoachMessage(user_id=str(user.id), role="user", content=text).to_mongo())

    history = []
    cursor = db.coach_messages.find({"user_id": str(user.id)}).sort("created_at", 1).limit(40)
    async for d in cursor:
        history.append({"role": d["role"], "content": d["content"]})

    context = await _coach_context(user)
    chat = _coach_chat(f"coach_{user.id}", context)
    prior = history[:-1][-12:]
    if prior:
        transcript = "\n".join(
            f"{'User' if m['role'] == 'user' else 'You'}: {m['content']}" for m in prior)
        prompt = f"Recent conversation so far:\n{transcript}\n\nUser's new message: {text}"
    else:
        prompt = text

    collected: list[str] = []
    async for event in chat.stream_message(UserMessage(text=prompt)):
        if isinstance(event, TextDelta):
            collected.append(event.content)
        elif isinstance(event, StreamDone):
            break
    reply = "".join(collected).strip()
    if reply:
        await db.coach_messages.insert_one(
            CoachMessage(user_id=str(user.id), role="assistant", content=reply).to_mongo())
    return {"reply": reply}
