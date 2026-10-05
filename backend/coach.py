"""Authenticated, session-scoped wellness coaching with real OpenAI streaming."""
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Literal
from uuid import NAMESPACE_URL, uuid4, uuid5

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pymongo import ReturnDocument

from ai_provider import model_info, stream_reply
from auth import get_current_user
from coach_safety import CONSENT_VERSION, REPLIES, redact, safe_context, safety_route
from db import get_db
from models import CoachBody, User, utcnow

router = APIRouter(prefix="/api/coach", tags=["coach"])
logger = logging.getLogger(__name__)


class SessionView(BaseModel):
    session_id: str
    title: str
    created_at: datetime
    updated_at: datetime


class MessageView(BaseModel):
    id: str
    session_id: str
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime
    model: str | None = None
    safety: str | None = None


class ConsentBody(BaseModel):
    accepted: bool
    version: str


async def migrate_legacy_chats():
    db = get_db()
    # A deterministic migration ID makes this safe across concurrent startups.
    for uid in await db.coach_messages.distinct("user_id", {"session_id": {"$exists": False}}):
        sid = str(uuid5(NAMESPACE_URL, f"ihyaa-legacy-{uid}"))
        await db.coach_sessions.update_one({"session_id": sid}, {"$setOnInsert": {
            "user_id": str(uid), "session_id": sid, "title": "Earlier conversation",
            "created_at": utcnow(), "updated_at": utcnow(),
        }}, upsert=True)
        await db.coach_messages.update_many(
            {"user_id": uid, "session_id": {"$exists": False}}, {"$set": {"session_id": sid}})


async def owned_session(sid: str, user: User) -> dict:
    doc = await get_db().coach_sessions.find_one(
        {"session_id": sid, "user_id": str(user.id)}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "session_not_found")
    return doc


@router.get("/config")
async def config(user: User = Depends(get_current_user)):
    return {**model_info(), "consent_version": CONSENT_VERSION,
            "consent_required": user.coach_consent_version != CONSENT_VERSION,
            "max_message_length": 2000, "languages": ["en", "id"]}


@router.post("/consent")
async def consent(body: ConsentBody, user: User = Depends(get_current_user)):
    if body.version != CONSENT_VERSION:
        raise HTTPException(409, "consent_version_changed")
    await get_db().users.update_one({"_id": ObjectId(user.id)}, {"$set": {
        "coach_consent_version": CONSENT_VERSION if body.accepted else None}})
    return {"accepted": body.accepted}


@router.get("/sessions", response_model=list[SessionView])
async def sessions(user: User = Depends(get_current_user)):
    return await get_db().coach_sessions.find({"user_id": str(user.id)}, {"_id": 0}).sort(
        "updated_at", -1).limit(100).to_list(100)


@router.post("/sessions", response_model=SessionView)
async def create_session(user: User = Depends(get_current_user)):
    db = get_db()
    if await db.coach_sessions.count_documents({"user_id": str(user.id)}) >= 100:
        raise HTTPException(429, "session_limit")
    doc = {"user_id": str(user.id), "session_id": str(uuid4()),
           "title": "Percakapan baru" if user.language == "id" else "New conversation",
           "created_at": utcnow(), "updated_at": utcnow()}
    result = SessionView(**doc)
    await db.coach_sessions.insert_one(doc)
    return result


@router.get("/history", response_model=list[MessageView])
async def history(session_id: str = Query(...), user: User = Depends(get_current_user)):
    await owned_session(session_id, user)
    rows = await get_db().coach_messages.find(
        {"user_id": str(user.id), "session_id": session_id},
        {"_id": 0, "id": {"$toString": "$_id"}, "session_id": 1, "role": 1,
         "content": 1, "created_at": 1, "model": 1, "safety": 1},
    ).sort([("created_at", -1), ("_id", -1)]).limit(200).to_list(200)
    return list(reversed(rows))


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str, user: User = Depends(get_current_user)):
    await owned_session(session_id, user)
    db = get_db()
    result = await db.coach_sessions.delete_one({
        "session_id": session_id, "user_id": str(user.id),
        "$or": [{"busy_until": {"$exists": False}}, {"busy_until": {"$lt": utcnow()}}],
    })
    if not result.deleted_count:
        raise HTTPException(409, "conversation_busy")
    await db.coach_messages.delete_many({"user_id": str(user.id), "session_id": session_id})
    return {"ok": True}


async def prepare(body: CoachBody, user: User):
    if user.coach_consent_version != CONSENT_VERSION:
        raise HTTPException(403, "coach_consent_required")
    await owned_session(body.session_id, user)
    db = get_db()
    now = utcnow()
    usage = await db.coach_usage.find_one_and_update(
        {"user_id": str(user.id), "minute": now.strftime("%Y-%m-%dT%H:%M")},
        {"$inc": {"count": 1}, "$setOnInsert": {"expires_at": now + timedelta(minutes=2)}},
        upsert=True, return_document=ReturnDocument.AFTER, projection={"_id": 0, "count": 1})
    if usage["count"] > 10:
        raise HTTPException(429, "coach_rate_limit")
    lock = str(uuid4())
    session = await db.coach_sessions.find_one_and_update(
        {"user_id": str(user.id), "session_id": body.session_id,
         "$or": [{"busy_until": {"$exists": False}}, {"busy_until": {"$lt": now}}]},
        {"$set": {"busy_until": now + timedelta(seconds=75), "lock": lock}},
        projection={"_id": 0}, return_document=ReturnDocument.AFTER)
    if not session:
        raise HTTPException(409, "conversation_busy")
    return lock


def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def generate(body: CoachBody, user: User, lock: str):
    db = get_db()
    scope = {"user_id": str(user.id), "session_id": body.session_id}
    language = body.language or user.language
    intent = safety_route(body.message, user)
    reply = ""
    try:
        yield sse("meta", {"session_id": body.session_id, **model_info()})
        async with asyncio.timeout(60):
            if intent:
                reply = REPLIES[intent][language]
                yield sse("delta", {"text": reply})
            else:
                rows = await db.coach_messages.find(
                    {**scope, "safety": None}, {"_id": 0, "role": 1, "content": 1}
                ).sort([("created_at", -1), ("_id", -1)]).limit(12).to_list(12)
                prior = [{"role": d["role"], "content": redact(d["content"], user)} for d in reversed(rows)]
                async for delta in stream_reply(body.session_id, safe_context(user, language), prior, redact(body.message, user)):
                    reply += delta
                    yield sse("delta", {"text": delta})
        if not reply.strip():
            raise RuntimeError("Empty coach response")
        # Only complete turns are saved; failures leave no dangling user message.
        user_id, assistant_id = ObjectId(), ObjectId()
        at = utcnow()
        model = None if intent else model_info()["model"]
        await db.coach_messages.insert_many([
            {"_id": user_id, **scope, "role": "user", "content": body.message,
             "created_at": at, "safety": intent},
            {"_id": assistant_id, **scope, "role": "assistant", "content": reply.strip(),
             "created_at": at + timedelta(microseconds=1), "safety": intent, "model": model},
        ])
        count = await db.coach_messages.count_documents(scope)
        updates = {"updated_at": utcnow()}
        if count == 2:
            # Do not expose sensitive prompt content in the conversation picker.
            updates["title"] = ("Percakapan" if language == "id" else "Conversation") + " · " + at.strftime("%d %b %H:%M")
        await db.coach_sessions.update_one(scope, {"$set": updates})
        yield sse("done", {"session_id": body.session_id, "reply": reply.strip(),
                           "user_message_id": str(user_id), "assistant_message_id": str(assistant_id),
                           "model": model, "safety": intent})
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        # Provider exceptions can contain keys/prompts. Log only the type, not text.
        logger.warning("Coach response failed (%s)", type(exc).__name__)
        yield sse("error", {"code": "coach_unavailable", "retryable": True})
    finally:
        await asyncio.shield(db.coach_sessions.update_one(
            {**scope, "lock": lock}, {"$unset": {"busy_until": "", "lock": ""}}))


@router.post("/chat")
async def chat(body: CoachBody, user: User = Depends(get_current_user)):
    lock = await prepare(body, user)
    return StreamingResponse(generate(body, user, lock), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@router.post("/chat-sync")
async def chat_sync(body: CoachBody, user: User = Depends(get_current_user)):
    """Compatibility route; new mobile/web clients consume /chat incrementally."""
    lock = await prepare(body, user)
    async for chunk in generate(body, user, lock):
        if chunk.startswith("event: error"):
            raise HTTPException(503, "coach_unavailable")
        if chunk.startswith("event: done"):
            result = json.loads(chunk.split("data: ", 1)[1])
    return result