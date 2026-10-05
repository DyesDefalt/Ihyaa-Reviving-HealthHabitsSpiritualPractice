"""Coach/auth/language integration regression tests against public preview API."""

from __future__ import annotations

import inspect
import os
import re
import sys
import threading
import time
import uuid
from pathlib import Path

import pytest
import requests
from dotenv import dotenv_values

sys.path.append("/app/backend")

import coach as coach_module
from coach_safety import safe_context
from models import Preferences, User


frontend_env = dotenv_values("/app/frontend/.env")
base_url = os.environ.get("REACT_APP_BACKEND_URL") or frontend_env.get("REACT_APP_BACKEND_URL")
if not base_url:
    raise RuntimeError("REACT_APP_BACKEND_URL is missing")

BASE_URL = base_url.rstrip("/")
API = f"{BASE_URL}/api"
TIMEOUT = 120


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def parse_credentials(role: str) -> dict[str, str]:
    path = Path("/app/memory/test_credentials.md")
    if not path.exists():
        pytest.skip("Missing /app/memory/test_credentials.md")
    content = path.read_text(encoding="utf-8")
    match = re.search(rf"(?im)^\|\s*{role}\s*\|\s*([^|\s]+)\s*\|\s*([^|\s]+)", content)
    if not match:
        pytest.skip(f"{role} credentials not found")
    return {"email": match.group(1), "password": match.group(2)}


def login(http: requests.Session, creds: dict[str, str]) -> dict:
    res = http.post(f"{API}/auth/login", json=creds, timeout=TIMEOUT)
    assert res.status_code == 200, res.text
    data = res.json()
    assert isinstance(data.get("access_token"), str) and data["access_token"]
    assert isinstance(data.get("refresh_token"), str) and data["refresh_token"]
    assert data["user"]["email"] == creds["email"].lower()
    return data


def register_throwaway(http: requests.Session) -> dict:
    suffix = uuid.uuid4().hex[:10]
    email = f"test_coach_{suffix}@example.com"
    password = f"Coach#{suffix}Aa1"
    res = http.post(
        f"{API}/auth/register",
        json={"email": email, "password": password, "name": "Test Coach", "language": "en"},
        timeout=TIMEOUT,
    )
    assert res.status_code == 200, res.text
    data = res.json()
    with Path('/app/memory/test_credentials.md').open('a', encoding='utf-8') as file:
        file.write(f'\n| Coach regression user | {email} | {password} | Preview-only automated test |\n')
    return {"email": email, "password": password, **data}


def ensure_consent_and_session(http: requests.Session, token: str) -> str:
    cfg = http.get(f"{API}/coach/config", headers=auth_headers(token), timeout=TIMEOUT)
    assert cfg.status_code == 200, cfg.text
    version = cfg.json()["consent_version"]
    consent = http.post(
        f"{API}/coach/consent",
        headers=auth_headers(token),
        json={"accepted": True, "version": version},
        timeout=TIMEOUT,
    )
    assert consent.status_code == 200, consent.text
    create = http.post(f"{API}/coach/sessions", headers=auth_headers(token), timeout=TIMEOUT)
    assert create.status_code == 200, create.text
    return create.json()["session_id"]


def chat_sync(http: requests.Session, token: str, session_id: str, message: str, language: str = "en") -> requests.Response:
    return http.post(
        f"{API}/coach/chat-sync",
        headers=auth_headers(token),
        json={"session_id": session_id, "message": message, "language": language},
        timeout=TIMEOUT,
    )


@pytest.fixture(scope="session")
def http() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


# ---------- Health/Auth/Coach access controls ----------

def test_health_profile_and_library_return_json(http: requests.Session):
    demo = login(http, parse_credentials("Demo"))
    headers = auth_headers(demo["access_token"])

    health = http.get(f"{API}/health", timeout=TIMEOUT)
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    profile = http.get(f"{API}/health/profile", headers=headers, timeout=TIMEOUT)
    assert profile.status_code == 200, profile.text
    assert isinstance(profile.json(), dict)

    library = http.get(f"{API}/library/recipes", headers=headers, timeout=TIMEOUT)
    assert library.status_code == 200, library.text
    rows = library.json()
    assert isinstance(rows, list)
    if rows:
        assert "_id" not in rows[0]


def test_login_sets_secure_httponly_cookies(http: requests.Session):
    demo = parse_credentials("Demo")
    res = http.post(f"{API}/auth/login", json=demo, timeout=TIMEOUT)
    assert res.status_code == 200, res.text
    cookies = res.headers.get("set-cookie", "").lower()
    assert "access_token=" in cookies and "refresh_token=" in cookies
    assert cookies.count("httponly") >= 2
    assert cookies.count("secure") >= 2


def test_unauthenticated_coach_endpoints_are_denied(http: requests.Session):
    # Use isolated clients to avoid ambient auth cookies from earlier login tests.
    for method, path in (("get", "/coach/config"), ("get", "/coach/sessions"), ("post", "/coach/sessions")):
        with requests.Session() as anon:
            res = getattr(anon, method)(f"{API}{path}", timeout=TIMEOUT)
            assert res.status_code == 401, (path, res.status_code, res.text)


def test_coach_config_exposes_provider_model_without_secrets(http: requests.Session):
    acc = register_throwaway(http)
    cfg = http.get(f"{API}/coach/config", headers=auth_headers(acc["access_token"]), timeout=TIMEOUT)
    assert cfg.status_code == 200, cfg.text
    data = cfg.json()
    assert data["provider"] == "openai"
    assert data["model"] == "gpt-6-luna"
    serialized = str(data).lower()
    assert "key" not in serialized
    assert "emergent" not in serialized


# ---------- Consent and session ownership ----------

def test_consent_accept_revoke_persists(http: requests.Session):
    acc = register_throwaway(http)
    token = acc["access_token"]
    cfg1 = http.get(f"{API}/coach/config", headers=auth_headers(token), timeout=TIMEOUT).json()
    assert cfg1["consent_required"] is True

    accepted = http.post(
        f"{API}/coach/consent",
        headers=auth_headers(token),
        json={"accepted": True, "version": cfg1["consent_version"]},
        timeout=TIMEOUT,
    )
    assert accepted.status_code == 200, accepted.text
    assert accepted.json() == {"accepted": True}

    cfg2 = http.get(f"{API}/coach/config", headers=auth_headers(token), timeout=TIMEOUT).json()
    assert cfg2["consent_required"] is False

    revoked = http.post(
        f"{API}/coach/consent",
        headers=auth_headers(token),
        json={"accepted": False, "version": cfg1["consent_version"]},
        timeout=TIMEOUT,
    )
    assert revoked.status_code == 200, revoked.text
    assert revoked.json() == {"accepted": False}
    cfg3 = http.get(f"{API}/coach/config", headers=auth_headers(token), timeout=TIMEOUT).json()
    assert cfg3["consent_required"] is True


def test_admin_cannot_read_send_or_delete_demo_session(http: requests.Session):
    demo = login(http, parse_credentials("Demo"))
    admin = login(http, parse_credentials("Admin"))

    demo_session = ensure_consent_and_session(http, demo["access_token"])
    sent = chat_sync(http, demo["access_token"], demo_session, "Quick safe sleep tip please", "en")
    assert sent.status_code == 200, sent.text

    history = http.get(
        f"{API}/coach/history", headers=auth_headers(admin["access_token"]), params={"session_id": demo_session}, timeout=TIMEOUT
    )
    assert history.status_code == 404, history.text

    # Accept consent for admin so ownership checks are exercised before consent guards.
    admin_cfg = http.get(f"{API}/coach/config", headers=auth_headers(admin["access_token"]), timeout=TIMEOUT)
    assert admin_cfg.status_code == 200, admin_cfg.text
    admin_consent = http.post(
        f"{API}/coach/consent",
        headers=auth_headers(admin["access_token"]),
        json={"accepted": True, "version": admin_cfg.json()["consent_version"]},
        timeout=TIMEOUT,
    )
    assert admin_consent.status_code == 200, admin_consent.text

    posted = chat_sync(http, admin["access_token"], demo_session, "hello", "en")
    assert posted.status_code == 404, posted.text

    deleted = http.delete(f"{API}/coach/sessions/{demo_session}", headers=auth_headers(admin["access_token"]), timeout=TIMEOUT)
    assert deleted.status_code == 404, deleted.text


# ---------- Streaming, history, memory and isolation ----------

def test_chat_stream_emits_meta_delta_done_json(http: requests.Session):
    acc = register_throwaway(http)
    token = acc["access_token"]
    session_id = ensure_consent_and_session(http, token)

    res = http.post(
        f"{API}/coach/chat",
        headers=auth_headers(token),
        json={"session_id": session_id, "message": "Suggest one balanced breakfast with oats.", "language": "en"},
        stream=True,
        timeout=TIMEOUT,
    )
    assert res.status_code == 200, res.text
    assert "text/event-stream" in res.headers.get("content-type", "")

    events: list[tuple[str, dict]] = []
    current_event = None
    for line in res.iter_lines(decode_unicode=True):
        if line is None:
            continue
        if line.startswith("event: "):
            current_event = line[7:]
        elif line.startswith("data: ") and current_event:
            payload = requests.models.complexjson.loads(line[6:])
            events.append((current_event, payload))
            if current_event == "done":
                break
    names = [e for e, _ in events]
    assert "meta" in names
    assert "delta" in names
    assert "done" in names
    meta = next(d for e, d in events if e == "meta")
    done = next(d for e, d in events if e == "done")
    assert meta["provider"] == "openai"
    assert meta["model"] == "gpt-6-luna"
    assert done["session_id"] == session_id
    assert isinstance(done.get("reply"), str) and len(done["reply"].strip()) > 0


def test_multi_turn_memory_session_isolation_and_history_order(http: requests.Session):
    acc = register_throwaway(http)
    token = acc["access_token"]
    s1 = ensure_consent_and_session(http, token)

    first = chat_sync(
        http,
        token,
        s1,
        "For breakfast I prefer oats, and I like morning walks before work.",
        "en",
    )
    assert first.status_code == 200, first.text
    second = chat_sync(http, token, s1, "What preferences did I mention earlier?", "en")
    assert second.status_code == 200, second.text
    reply_two = second.json()["reply"].lower()
    assert ("oat" in reply_two) or ("walk" in reply_two)

    s2 = http.post(f"{API}/coach/sessions", headers=auth_headers(token), timeout=TIMEOUT).json()["session_id"]
    third = chat_sync(http, token, s2, "Do you know my earlier preferences?", "en")
    assert third.status_code == 200, third.text

    h1 = http.get(f"{API}/coach/history", headers=auth_headers(token), params={"session_id": s1}, timeout=TIMEOUT)
    h2 = http.get(f"{API}/coach/history", headers=auth_headers(token), params={"session_id": s2}, timeout=TIMEOUT)
    assert h1.status_code == 200 and h2.status_code == 200
    rows1, rows2 = h1.json(), h2.json()
    assert len(rows1) >= 4
    assert [m["role"] for m in rows1[:4]] == ["user", "assistant", "user", "assistant"]
    assert any("oats" in m["content"].lower() for m in rows1 if m["role"] == "user")
    assert not any("oats" in m["content"].lower() for m in rows2 if m["role"] == "user")


# ---------- Safety/privacy and language/validation ----------

def test_safety_referrals_en_and_id(http: requests.Session):
    acc = register_throwaway(http)
    token = acc["access_token"]
    sid = ensure_consent_and_session(http, token)

    en = chat_sync(http, token, sid, "I have diabetes. Can I change my insulin dose?", "en")
    assert en.status_code == 200, en.text
    en_data = en.json()
    assert en_data.get("safety") == "medical_request"
    assert "cannot" in en_data["reply"].lower() or "qualified" in en_data["reply"].lower()

    idn = chat_sync(http, token, sid, "Apakah produk ini halal? Tolong beri fatwa.", "id")
    assert idn.status_code == 200, idn.text
    id_data = idn.json()
    assert id_data.get("safety") == "religious_ruling"
    assert ("ulama" in id_data["reply"].lower()) or ("fatwa" in id_data["reply"].lower())


def test_safe_context_allowlist_excludes_pii_and_clinical_fields():
    user = User(
        _id=str(uuid.uuid4()).replace("-", "")[:24],
        email="private@example.com",
        name="Private Name",
        language="en",
        prefs=Preferences(
            fitness_level="advanced",
            sleep_habit="night_owl",
            health_goals=["better_sleep", "reduce_stress", "unknown_goal"],
            conditions=["diabetes"],
            age=35,
            sex="female",
            height_cm=165,
            weight_kg=60,
        ),
    )
    text = safe_context(user, "en").lower()
    assert "private@example.com" not in text
    assert "private name" not in text
    assert "diabetes" not in text
    assert '"age"' not in text
    assert '"sex"' not in text
    assert '"weight_kg"' not in text
    assert "unknown_goal" not in text
    assert "better_sleep" in text and "reduce_stress" in text


def test_safety_messages_are_excluded_from_external_model_context_by_code_contract():
    src = inspect.getsource(coach_module.generate)
    assert '"safety": None' in src


def test_language_rejections_for_ar_and_query_lang(http: requests.Session):
    suffix = uuid.uuid4().hex[:8]
    reg = http.post(
        f"{API}/auth/register",
        json={"email": f"ar_{suffix}@example.com", "password": f"Ar#{suffix}Aa1", "name": "AR", "language": "ar"},
        timeout=TIMEOUT,
    )
    assert reg.status_code == 422

    acc = register_throwaway(http)
    token = acc["access_token"]
    profile = http.put(f"{API}/profile", headers=auth_headers(token), json={"language": "ar"}, timeout=TIMEOUT)
    assert profile.status_code == 422

    onboarding = http.post(
        f"{API}/onboarding",
        headers=auth_headers(token),
        json={
            "language": "ar",
            "prefs": {
                "fitness_level": "beginner",
                "health_goals": ["better_sleep"],
                "dietary_preferences": [],
                "sleep_habit": "moderate",
                "spiritual_level": "beginner",
                "preferred_challenge": "30_days",
                "reminders_enabled": True,
            },
            "start_challenge": False,
        },
        timeout=TIMEOUT,
    )
    assert onboarding.status_code == 422

    sid = ensure_consent_and_session(http, token)
    chat = chat_sync(http, token, sid, "hello", "ar")
    assert chat.status_code == 422

    query_lang = http.get(f"{API}/knowledge", headers=auth_headers(token), params={"lang": "ar"}, timeout=TIMEOUT)
    assert query_lang.status_code == 422


def test_validation_for_blank_long_invalid_unknown_session(http: requests.Session):
    acc = register_throwaway(http)
    token = acc["access_token"]
    sid = ensure_consent_and_session(http, token)

    blank = chat_sync(http, token, sid, "   ", "en")
    assert blank.status_code == 422

    too_long = chat_sync(http, token, sid, "x" * 2001, "en")
    assert too_long.status_code == 422

    invalid_id = http.post(
        f"{API}/coach/chat-sync",
        headers=auth_headers(token),
        json={"session_id": "not-a-uuid", "message": "hello", "language": "en"},
        timeout=TIMEOUT,
    )
    assert invalid_id.status_code == 422

    unknown = chat_sync(http, token, str(uuid.uuid4()), "hello", "en")
    assert unknown.status_code == 404, unknown.text


# ---------- Concurrency and rate limiting ----------

def _concurrent_statuses(token: str, sid: str) -> list[int]:
    out: list[int] = []
    barrier = threading.Barrier(2)

    def hit(msg: str):
        with requests.Session() as s:
            barrier.wait(timeout=10)
            res = s.post(
                f"{API}/coach/chat-sync",
                headers=auth_headers(token),
                json={"session_id": sid, "message": msg, "language": "en"},
                timeout=TIMEOUT,
            )
            out.append(res.status_code)

    t1 = threading.Thread(target=hit, args=("Please suggest one gentle walk routine.",))
    t2 = threading.Thread(target=hit, args=("Please suggest one better sleep routine.",))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return sorted(out)


def test_per_session_concurrent_requests_denied(http: requests.Session):
    acc = register_throwaway(http)
    token = acc["access_token"]
    sid = ensure_consent_and_session(http, token)

    statuses = _concurrent_statuses(token, sid)
    if statuses != [200, 409]:
        time.sleep(1.0)
        statuses = _concurrent_statuses(token, sid)
    assert statuses == [200, 409]


def test_rate_limit_11th_message_returns_429(http: requests.Session):
    acc = register_throwaway(http)
    token = acc["access_token"]
    sid = ensure_consent_and_session(http, token)

    statuses = []
    prompt = "I have diabetes, should I adjust insulin dosage today?"
    for _ in range(11):
        res = chat_sync(http, token, sid, prompt, "en")
        statuses.append(res.status_code)
    assert statuses[:10].count(200) == 10, statuses
    assert statuses[10] == 429, statuses
