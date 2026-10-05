"""Regression tests for Ihyaa auth, onboarding, curriculum, tasks, check-ins, rewards, content, calendar, and AI coach."""

import os
import re
import asyncio

import time
import uuid
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import pytest
import requests
from dotenv import dotenv_values
import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient


frontend_env = dotenv_values("/app/frontend/.env")
base_url = os.environ.get("REACT_APP_BACKEND_URL") or frontend_env.get("REACT_APP_BACKEND_URL")
if not base_url:
    raise RuntimeError("REACT_APP_BACKEND_URL is missing")
BASE_URL = base_url.rstrip("/")
API = f"{BASE_URL}/api"
TIMEOUT = 60


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def assert_public_user(user: dict, email: str) -> None:
    assert isinstance(user["id"], str) and user["id"]
    assert user["email"] == email.lower()
    assert "password_hash" not in user
    assert "_id" not in user
    assert isinstance(user["points_balance"], int)
    assert isinstance(user["prefs"], dict)


@pytest.fixture(scope="session")
def http():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


@pytest.fixture(scope="session")
def demo_credentials():
    path = Path("/app/memory/test_credentials.md")
    if not path.exists():
        pytest.skip("Missing /app/memory/test_credentials.md")
    content = path.read_text(encoding="utf-8")
    match = re.search(r"(?im)^\|\s*Demo\s*\|\s*([^|\s]+)\s*\|\s*([^|\s]+)", content)
    if not match:
        pytest.skip("Demo credentials not found in test_credentials.md")
    return {"email": match.group(1), "password": match.group(2)}


@pytest.fixture(scope="session")
def registered_account(http):
    suffix = uuid.uuid4().hex[:10]
    email = f"TEST_ihyaa_{suffix}@example.com"
    password = f"Safe#{suffix}Aa1"
    response = http.post(
        f"{API}/auth/register",
        json={"email": email, "password": password, "name": "TEST Ihyaa User", "language": "en"},
        timeout=TIMEOUT,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["access_token"] and data["refresh_token"]
    assert data["user"]["onboarding_completed"] is False
    assert_public_user(data["user"], email)
    return {
        "email": email,
        "password": password,
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "register_response": response,
        "user": data["user"],
    }


@pytest.fixture(scope="session")
def onboarded_account(http, registered_account):
    account = registered_account
    payload = {
        "name": "TEST Onboarded User",
        "language": "en",
        "timezone": "UTC",
        "prefs": {
            "fitness_level": "advanced",
            "health_goals": ["build_strength", "spiritual_growth", "healthy_eating"],
            "dietary_preferences": ["low_sugar", "sunnah_diet"],
            "sleep_habit": "moderate",
            "spiritual_level": "devoted",
            "preferred_challenge": "30_days",
            "reminders_enabled": True,
        },
        "start_challenge": True,
    }
    response = http.post(
        f"{API}/onboarding",
        headers=auth_headers(account["access_token"]),
        json=payload,
        timeout=TIMEOUT,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    account["onboarding_response"] = data
    account["start_date"] = data["challenge"]["start_date"]
    return account


class TestHealthAndAuth:
    """Health, password JWT auth, refresh, cookies, lockout, and CORS."""

    def test_health(self, http):
        response = http.get(f"{API}/health", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["app"] == "Ihyaa"
        assert isinstance(data["time"], str) and "T" in data["time"]

    def test_register_contract_and_secure_cookies(self, registered_account):
        response = registered_account["register_response"]
        cookies = response.headers.get("set-cookie", "").lower()
        assert "access_token=" in cookies and "refresh_token=" in cookies
        assert cookies.count("httponly") >= 2
        assert cookies.count("secure") >= 2
        assert cookies.count("samesite=none") >= 2
        assert registered_account["user"]["onboarding_completed"] is False

    def test_registered_password_is_bcrypt_2b_hash(self, registered_account):
        backend_env = dotenv_values("/app/backend/.env")

        async def load_hash():
            client = AsyncIOMotorClient(backend_env["MONGO_URL"])
            try:
                row = await client[backend_env["DB_NAME"]].users.find_one(
                    {"email": registered_account["email"].lower()}, {"password_hash": 1}
                )
                return row["password_hash"]
            finally:
                client.close()

        password_hash = asyncio.run(load_hash())
        assert password_hash.startswith("$2b$")
        assert bcrypt.checkpw(registered_account["password"].encode(), password_hash.encode())

    def test_demo_login_and_me_same_user(self, http, demo_credentials):
        response = http.post(f"{API}/auth/login", json=demo_credentials, timeout=TIMEOUT)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["access_token"] and data["refresh_token"]
        assert_public_user(data["user"], demo_credentials["email"])
        me = http.get(f"{API}/auth/me", headers=auth_headers(data["access_token"]), timeout=TIMEOUT)
        assert me.status_code == 200, me.text
        assert me.json() == data["user"]

    def test_refresh_header_returns_fresh_valid_access_token(self, registered_account):
        time.sleep(1.1)
        # Isolated client verifies the X-Refresh-Token contract without unrelated cookies.
        response = requests.post(
            f"{API}/auth/refresh",
            headers={"X-Refresh-Token": registered_account["refresh_token"]},
            timeout=TIMEOUT,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["access_token"] and data["refresh_token"]
        assert data["access_token"] != registered_account["access_token"]
        me = requests.get(f"{API}/auth/me", headers=auth_headers(data["access_token"]), timeout=TIMEOUT)
        assert me.status_code == 200
        assert me.json()["email"] == registered_account["email"].lower()
        registered_account["access_token"] = data["access_token"]
        registered_account["refresh_token"] = data["refresh_token"]

    def test_refresh_header_is_not_overridden_by_other_users_cookie(self, http, registered_account, demo_credentials):
        demo = http.post(f"{API}/auth/login", json=demo_credentials, timeout=TIMEOUT)
        assert demo.status_code == 200, demo.text
        response = http.post(
            f"{API}/auth/refresh",
            headers={"X-Refresh-Token": registered_account["refresh_token"]},
            timeout=TIMEOUT,
        )
        assert response.status_code == 200, response.text
        assert response.json()["user"]["email"] == registered_account["email"]

    def test_throwaway_lockout_after_five_failures(self, http):
        suffix = uuid.uuid4().hex[:10]
        email = f"TEST_lockout_{suffix}@example.com"
        password = f"Lock#{suffix}Aa1"
        created = http.post(
            f"{API}/auth/register",
            json={"email": email, "password": password, "name": "TEST Lockout", "language": "en"},
            timeout=TIMEOUT,
        )
        assert created.status_code == 200, created.text
        statuses = []
        for _ in range(5):
            failed = http.post(
                f"{API}/auth/login", json={"email": email, "password": "definitely-wrong"}, timeout=TIMEOUT
            )
            statuses.append(failed.status_code)
            assert failed.status_code == 401, failed.text
            assert failed.json()["detail"] == "Invalid email or password"
        locked = http.post(f"{API}/auth/login", json={"email": email, "password": password}, timeout=TIMEOUT)
        assert locked.status_code == 429, (statuses, locked.text)
        assert "15 minutes" in locked.json()["detail"]

    def test_free_one_year_onboarding_silently_falls_back_to_30_days(self, http):
        suffix = uuid.uuid4().hex[:10]
        email = f"TEST_fallback_{suffix}@example.com"
        password = f"Fallback#{suffix}Aa1"
        created = http.post(
            f"{API}/auth/register",
            json={"email": email, "password": password, "name": "TEST Fallback", "language": "en"},
            timeout=TIMEOUT,
        )
        assert created.status_code == 200, created.text
        token = created.json()["access_token"]
        fallback = http.post(
            f"{API}/onboarding",
            headers=auth_headers(token),
            json={
                "name": "TEST Fallback",
                "language": "en",
                "prefs": {
                    "fitness_level": "beginner",
                    "health_goals": ["better_sleep"],
                    "dietary_preferences": [],
                    "sleep_habit": "moderate",
                    "spiritual_level": "beginner",
                    "preferred_challenge": "1_year",
                    "reminders_enabled": True,
                },
                "start_challenge": True,
            },
            timeout=TIMEOUT,
        )
        assert fallback.status_code == 200, fallback.text
        data = fallback.json()
        assert data["user"]["prefs"]["preferred_challenge"] == "30_days"
        assert data["challenge"]["challenge_type"] == "30_days"
        assert data["challenge"]["total_days"] == 30

    def test_credentialed_cors_uses_explicit_origin(self, http):
        response = http.options(
            f"{API}/auth/login",
            headers={
                "Origin": BASE_URL,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type,authorization",
            },
            timeout=TIMEOUT,
        )
        assert response.status_code in (200, 204), response.text
        assert response.headers.get("access-control-allow-origin") == BASE_URL
        assert response.headers.get("access-control-allow-credentials") == "true"


class TestOnboardingAndCurriculum:
    """Onboarding, challenge gating, plan shape, ramp, and localization."""

    def test_onboarding_starts_day_one_30_day_challenge(self, onboarded_account):
        data = onboarded_account["onboarding_response"]
        assert data["user"]["onboarding_completed"] is True
        assert data["user"]["name"] == "TEST Onboarded User"
        assert data["challenge"]["challenge_type"] == "30_days"
        assert data["challenge"]["total_days"] == 30
        assert data["challenge"]["current_day"] == 1

    def test_free_user_cannot_start_pro_track(self, http, onboarded_account):
        response = http.post(
            f"{API}/challenges",
            headers=auth_headers(onboarded_account["access_token"]),
            json={"challenge_type": "100_days"},
            timeout=TIMEOUT,
        )
        assert response.status_code == 402, response.text
        assert response.json()["detail"] == "pro_required"

    def test_plan_daily_counts_and_one_percent_ramp(self, http, onboarded_account):
        start = date.fromisoformat(onboarded_account["start_date"])
        end = start + timedelta(days=29)
        response = http.get(
            f"{API}/tasks",
            headers=auth_headers(onboarded_account["access_token"]),
            params={"from": start.isoformat(), "to": end.isoformat(), "lang": "en"},
            timeout=TIMEOUT,
        )
        assert response.status_code == 200, response.text
        tasks = response.json()
        by_day = Counter(t["day_number"] for t in tasks)
        assert all(by_day[d] == 2 for d in range(1, 4))
        assert all(by_day[d] == 3 for d in range(4, 11))
        assert all(by_day[d] == 4 for d in range(11, 31))
        # 3*2 + 7*3 + 20*4 = 107. The review request's stated 111 total is arithmetically inconsistent.
        assert len(tasks) == 107
        first = [t for t in tasks if t["day_number"] == 1]
        last = [t for t in tasks if t["day_number"] == 30]
        assert max(t["duration_minutes"] for t in first) < max(t["duration_minutes"] for t in last)
        assert sum(t["duration_minutes"] for t in first) / len(first) < sum(t["duration_minutes"] for t in last) / len(last)

    def test_today_localization_and_evidence_fields(self, http, onboarded_account):
        results = {}
        for lang in ("en", "id", "ar"):
            response = http.get(
                f"{API}/tasks/today",
                headers=auth_headers(onboarded_account["access_token"]),
                params={"lang": lang},
                timeout=TIMEOUT,
            )
            assert response.status_code == 200, response.text
            data = response.json()
            assert data["challenge"]["current_day"] == 1
            assert len(data["tasks"]) == 2
            for task in data["tasks"]:
                assert task["title"] and task["description"]
                assert all(k in task for k in ("quran_reference", "hadith_reference", "science_reference"))
                assert task["science_reference"]
            results[lang] = data["tasks"]
        assert [t["title"] for t in results["en"]] != [t["title"] for t in results["id"]]
        assert [t["description"] for t in results["en"]] != [t["description"] for t in results["ar"]]


class TestTasksCheckinsAndProgress:
    """Task updates, point awards, check-ins, summaries, transactions, and regeneration."""

    def test_task_time_update_persists_and_invalid_time_is_rejected(self, http, onboarded_account):
        today = http.get(
            f"{API}/tasks/today", headers=auth_headers(onboarded_account["access_token"]), timeout=TIMEOUT
        ).json()
        task = today["tasks"][0]
        original = task["scheduled_time"]
        updated = "08:17" if original != "08:17" else "08:18"
        response = http.put(
            f"{API}/tasks/{task['id']}/time",
            headers=auth_headers(onboarded_account["access_token"]),
            json={"scheduled_time": updated},
            timeout=TIMEOUT,
        )
        assert response.status_code == 200, response.text
        assert response.json() == {"ok": True, "scheduled_time": updated}
        later = http.get(
            f"{API}/tasks/today", headers=auth_headers(onboarded_account["access_token"]), timeout=TIMEOUT
        ).json()
        assert next(t for t in later["tasks"] if t["id"] == task["id"])["scheduled_time"] == updated

        invalid = http.put(
            f"{API}/tasks/{task['id']}/time",
            headers=auth_headers(onboarded_account["access_token"]),
            json={"scheduled_time": "not-a-time"},
            timeout=TIMEOUT,
        )
        # Restore state even if validation is missing, so later calendar tests remain valid.
        http.put(
            f"{API}/tasks/{task['id']}/time",
            headers=auth_headers(onboarded_account["access_token"]),
            json={"scheduled_time": original},
            timeout=TIMEOUT,
        )
        assert invalid.status_code == 422, invalid.text

    def test_complete_all_awards_points_bonus_and_uncomplete_subtracts(self, http, onboarded_account):
        headers = auth_headers(onboarded_account["access_token"])
        today = http.get(f"{API}/tasks/today", headers=headers, timeout=TIMEOUT).json()
        tasks = today["tasks"]
        me_before = http.get(f"{API}/auth/me", headers=headers, timeout=TIMEOUT).json()
        expected = me_before["points_balance"]
        final = None
        for index, task in enumerate(tasks):
            response = http.post(
                f"{API}/tasks/{task['id']}/complete",
                headers=headers,
                json={"completed": True},
                timeout=TIMEOUT,
            )
            assert response.status_code == 200, response.text
            final = response.json()
            assert final["awarded"] == task["points_reward"]
            expected += task["points_reward"]
            assert final["bonus"] == (50 if index == len(tasks) - 1 else 0)
        expected += 50
        assert final["user"]["points_balance"] == expected

        last_task = tasks[-1]
        undone = http.post(
            f"{API}/tasks/{last_task['id']}/complete",
            headers=headers,
            json={"completed": False},
            timeout=TIMEOUT,
        )
        assert undone.status_code == 200, undone.text
        data = undone.json()
        assert data["awarded"] == -last_task["points_reward"]
        assert data["bonus"] == 0
        assert data["user"]["points_balance"] == expected - last_task["points_reward"]

        # Restore completion for later tests. A daily completion bonus must not be farmable by toggling.
        repeated = http.post(
            f"{API}/tasks/{last_task['id']}/complete",
            headers=headers,
            json={"completed": True},
            timeout=TIMEOUT,
        )
        assert repeated.status_code == 200, repeated.text
        assert repeated.json()["bonus"] == 0, "All-tasks bonus can be repeatedly farmed by undo/re-complete"

    def test_daily_checkin_awards_and_duplicate_rejected(self, http, onboarded_account):
        headers = auth_headers(onboarded_account["access_token"])
        before = http.get(f"{API}/auth/me", headers=headers, timeout=TIMEOUT).json()
        response = http.post(
            f"{API}/checkins",
            headers=headers,
            json={
                "mood_rating": 4,
                "energy_rating": 5,
                "gratitude_note": "TEST grateful for health",
                "reflection_note": "TEST kept the habits small",
            },
            timeout=TIMEOUT,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["points_earned"] == 15
        assert data["streak_bonus"] == 0
        assert data["streak"] == 1
        assert data["user"]["points_balance"] == before["points_balance"] + 15
        assert data["user"]["current_streak"] == 1

        duplicate = http.post(
            f"{API}/checkins",
            headers=headers,
            json={"mood_rating": 3, "energy_rating": 3, "gratitude_note": "again", "reflection_note": "again"},
            timeout=TIMEOUT,
        )
        assert duplicate.status_code == 400, duplicate.text
        assert duplicate.json()["detail"] == "already_checked_in"

        saved = http.get(f"{API}/checkins/today", headers=headers, timeout=TIMEOUT)
        assert saved.status_code == 200
        checkin = saved.json()
        assert checkin["mood_rating"] == 4
        assert checkin["energy_rating"] == 5
        assert checkin["gratitude_note"] == "TEST grateful for health"
        assert checkin["points_earned"] == 15

    def test_progress_summary_is_coherent(self, http, onboarded_account):
        response = http.get(
            f"{API}/progress/summary", headers=auth_headers(onboarded_account["access_token"]), timeout=TIMEOUT
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["total_tasks"] >= data["completed_tasks"] >= 0
        expected_rate = round(data["completed_tasks"] / data["total_tasks"] * 100) if data["total_tasks"] else 0
        assert data["completion_rate"] == expected_rate
        assert set(data["pillars"]) >= {"physical", "nutrition", "mental", "spiritual"}
        assert sum(p["total"] for p in data["pillars"].values()) == data["total_tasks"]
        assert sum(p["done"] for p in data["pillars"].values()) == data["completed_tasks"]
        assert len(data["last_7_days"]) == 7
        assert data["last_7_days"][-1]["date"] == date.today().isoformat()
        assert data["total_checkins"] == 1

    def test_transactions_include_task_bonus_and_checkin(self, http, onboarded_account):
        response = http.get(
            f"{API}/points/transactions", headers=auth_headers(onboarded_account["access_token"]), timeout=TIMEOUT
        )
        assert response.status_code == 200, response.text
        rows = response.json()
        assert rows and all(isinstance(row["amount"], int) for row in rows)
        sources = Counter(row["source"] for row in rows)
        assert sources["task_complete"] >= 2
        assert sources["all_tasks"] >= 1
        assert sources["task_uncomplete"] >= 1
        assert sources["checkin"] == 1
        assert all("_id" not in row for row in rows)

    def test_regenerate_preserves_completed_today_tasks(self, http, onboarded_account):
        headers = auth_headers(onboarded_account["access_token"])
        before = http.get(f"{API}/tasks/today", headers=headers, timeout=TIMEOUT).json()["tasks"]
        completed_ids = {task["id"] for task in before if task["completed"]}
        assert completed_ids
        profile = http.get(f"{API}/auth/me", headers=headers, timeout=TIMEOUT).json()
        prefs = profile["prefs"]
        prefs["sleep_habit"] = "night_owl"
        prefs["health_goals"] = ["better_sleep", "mental_clarity"]
        updated = http.put(
            f"{API}/profile",
            headers=headers,
            json={"prefs": prefs},
            timeout=TIMEOUT,
        )
        assert updated.status_code == 200, updated.text
        assert updated.json()["prefs"]["sleep_habit"] == "night_owl"
        regenerated = http.post(f"{API}/challenges/regenerate", headers=headers, timeout=TIMEOUT)
        assert regenerated.status_code == 200, regenerated.text
        assert regenerated.json()["ok"] is True
        after = http.get(f"{API}/tasks/today", headers=headers, timeout=TIMEOUT).json()["tasks"]
        after_by_id = {task["id"]: task for task in after}
        assert completed_ids <= set(after_by_id)
        assert all(after_by_id[task_id]["completed"] is True for task_id in completed_ids)


class TestStoreKnowledgeCalendarAndCoach:
    """Rewards catalogue, knowledge library, ICS export, and persisted AI chat."""

    def test_store_catalogue_and_insufficient_redemption(self, http, onboarded_account):
        headers = auth_headers(onboarded_account["access_token"])
        response = http.get(f"{API}/store/items", headers=headers, timeout=TIMEOUT)
        assert response.status_code == 200, response.text
        items = response.json()
        assert [item["id"] for item in items] == ["pro_1_month", "pro_3_months", "pro_1_year"]
        assert [item["points_cost"] for item in items] == [2500, 6000, 18000]
        assert all(item["name"] and item["description"] for item in items)
        redeem = http.post(f"{API}/store/redeem/pro_1_month", headers=headers, timeout=TIMEOUT)
        assert redeem.status_code == 400, redeem.text
        assert redeem.json()["detail"] == "insufficient_points"

    def test_knowledge_cards_and_spiritual_filter(self, http, onboarded_account):
        headers = auth_headers(onboarded_account["access_token"])
        response = http.get(f"{API}/knowledge", headers=headers, timeout=TIMEOUT)
        assert response.status_code == 200, response.text
        cards = response.json()
        assert len(cards) == 8
        assert len({card["id"] for card in cards}) == 8
        for card in cards:
            assert card["title"] and card["content"] and card["scientific_fact"]
            assert all(k in card for k in ("quran_verse", "hadith_text", "scientific_fact"))
        spiritual = http.get(f"{API}/knowledge", headers=headers, params={"pillar": "spiritual"}, timeout=TIMEOUT)
        assert spiritual.status_code == 200
        filtered = spiritual.json()
        assert filtered and all(card["pillar"] == "spiritual" for card in filtered)
        assert len(filtered) < len(cards)

    def test_calendar_ics_is_valid_and_has_alarm(self, http, onboarded_account):
        response = http.get(
            f"{API}/tasks/calendar.ics",
            headers=auth_headers(onboarded_account["access_token"]),
            params={"days": 7, "lang": "en"},
            timeout=TIMEOUT,
        )
        assert response.status_code == 200, response.text
        assert response.headers["content-type"].startswith("text/calendar")
        body = response.text
        assert body.startswith("BEGIN:VCALENDAR")
        assert body.rstrip().endswith("END:VCALENDAR")
        assert "BEGIN:VEVENT" in body and "END:VEVENT" in body
        for field in ("DTSTART:", "DTEND:", "SUMMARY:", "BEGIN:VALARM", "TRIGGER:-PT10M"):
            assert field in body

    def test_ai_coach_indonesian_reply_history_and_clear(self, http, onboarded_account):
        headers = auth_headers(onboarded_account["access_token"])
        cleared = http.delete(f"{API}/coach/history", headers=headers, timeout=TIMEOUT)
        assert cleared.status_code == 200 and cleared.json() == {"ok": True}
        message = "Saya sedang lelah. Apa langkah kecil yang halal untuk kesehatan hari ini?"
        response = http.post(
            f"{API}/coach/chat-sync",
            headers=headers,
            json={"message": message},
            timeout=120,
        )
        assert response.status_code == 200, response.text
        reply = response.json()["reply"]
        assert isinstance(reply, str) and len(reply.strip()) >= 20
        lowered = reply.lower()
        assert any(word in lowered for word in ("anda", "kamu", "langkah", "hari", "allah", "istirahat", "minum"))
        history = http.get(f"{API}/coach/history", headers=headers, timeout=TIMEOUT)
        assert history.status_code == 200
        rows = history.json()
        assert [row["role"] for row in rows] == ["user", "assistant"]
        assert rows[0]["content"] == message
        assert rows[1]["content"] == reply
        deleted = http.delete(f"{API}/coach/history", headers=headers, timeout=TIMEOUT)
        assert deleted.status_code == 200 and deleted.json() == {"ok": True}
        empty = http.get(f"{API}/coach/history", headers=headers, timeout=TIMEOUT)
        assert empty.status_code == 200 and empty.json() == []


class TestInputValidation:
    """Critical malformed-input handling for challenge dates."""

    def test_invalid_challenge_start_date_is_client_error_not_500(self, http, onboarded_account):
        response = http.post(
            f"{API}/challenges",
            headers=auth_headers(onboarded_account["access_token"]),
            json={"challenge_type": "30_days", "start_date": "not-a-date"},
            timeout=TIMEOUT,
        )
        assert response.status_code in (400, 422), response.text
