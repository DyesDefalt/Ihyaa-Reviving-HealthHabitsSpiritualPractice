import os
from datetime import datetime, timedelta, timezone

import bcrypt
import httpx
import jwt
from bson import ObjectId
from fastapi import HTTPException, Request

from db import get_db
from models import User

JWT_ALGORITHM = "HS256"
ACCESS_TTL = timedelta(days=1)
REFRESH_TTL = timedelta(days=30)
EMERGENT_SESSION_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"

MAX_ATTEMPTS = 5
LOCKOUT = timedelta(minutes=15)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def _secret() -> str:
    return os.environ["JWT_SECRET"]


def create_access_token(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "type": "access",
        "exp": datetime.now(timezone.utc) + ACCESS_TTL,
    }
    return jwt.encode(payload, _secret(), algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + REFRESH_TTL,
    }
    return jwt.encode(payload, _secret(), algorithm=JWT_ALGORITHM)


def set_auth_cookies(response, access_token: str, refresh_token: str) -> None:
    response.set_cookie("access_token", access_token, httponly=True, secure=True,
                        samesite="none", max_age=int(ACCESS_TTL.total_seconds()), path="/")
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True,
                        samesite="none", max_age=int(REFRESH_TTL.total_seconds()), path="/")


def clear_auth_cookies(response) -> None:
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")


def _extract_token(request: Request) -> str | None:
    header = request.headers.get("Authorization", "")
    if header.startswith("Bearer "):
        return header[7:]
    return request.cookies.get("access_token")


async def _user_from_session_token(token: str) -> User | None:
    db = get_db()
    session = await db.user_sessions.find_one({"session_token": token})
    if not session:
        return None
    expires_at = session["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        return None
    doc = await db.users.find_one({"_id": ObjectId(session["user_id"])})
    return User.from_mongo(doc)


async def get_current_user(request: Request) -> User:
    token = _extract_token(request)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, _secret(), algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        doc = await get_db().users.find_one({"_id": ObjectId(payload["sub"])})
        user = User.from_mongo(doc)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        user = await _user_from_session_token(token)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user


async def check_lockout(identifier: str) -> None:
    db = get_db()
    row = await db.login_attempts.find_one({"identifier": identifier})
    if not row:
        return
    if row.get("count", 0) < MAX_ATTEMPTS:
        return
    last = row.get("last_attempt")
    if last and last.tzinfo is None:
        last = last.replace(tzinfo=timezone.utc)
    if last and datetime.now(timezone.utc) - last < LOCKOUT:
        raise HTTPException(status_code=429, detail="Too many failed attempts. Try again in 15 minutes.")
    await db.login_attempts.delete_one({"identifier": identifier})


async def record_failure(identifier: str) -> None:
    await get_db().login_attempts.update_one(
        {"identifier": identifier},
        {"$inc": {"count": 1}, "$set": {"last_attempt": datetime.now(timezone.utc)}},
        upsert=True,
    )


async def clear_failures(identifier: str) -> None:
    await get_db().login_attempts.delete_one({"identifier": identifier})


async def fetch_emergent_session(session_id: str) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(EMERGENT_SESSION_URL, headers={"X-Session-ID": session_id})
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Google session")
    return resp.json()
