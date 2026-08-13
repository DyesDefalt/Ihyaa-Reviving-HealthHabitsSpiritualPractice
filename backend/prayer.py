"""Real adhan times via the AlAdhan API, cached a whole month at a time.

No API key is required. Every habit anchor (fajr / dhuhr / maghrib / night ...)
is resolved to a wall-clock time derived from that day's actual prayer times,
with a small offset so the habit lands *after* the prayer, not during it.
"""
import os
from datetime import date, datetime, timezone

import httpx

from db import get_db

ALADHAN_BASE = os.environ.get("ALADHAN_BASE", "https://api.aladhan.com/v1")
NOMINATIM = "https://nominatim.openstreetmap.org/search"

PRAYERS = ("Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha")

METHODS = {
    1: "Karachi",
    2: "ISNA",
    3: "Muslim World League",
    4: "Umm al-Qura",
    5: "Egyptian",
    20: "Kemenag Indonesia",
}
SCHOOLS = {0: "shafii", 1: "hanafi"}

# anchor -> (prayer to hang off, minutes after it)
ANCHOR_OFFSETS = {
    "fajr": ("Fajr", 15),
    "morning": ("Sunrise", 45),
    "dhuhr": ("Dhuhr", 20),
    "asr": ("Asr", 20),
    "maghrib": ("Maghrib", 25),
    "isha": ("Isha", 20),
    "night": ("Isha", 90),
    "anytime": ("Sunrise", 180),
}

SLEEP_SHIFT = {"early_bird": -20, "moderate": 0, "night_owl": 40}
SHIFTED_ANCHORS = {"fajr", "night", "isha"}


def _round_coord(v: float) -> float:
    """Nearby GPS readings should share one cache entry."""
    return round(float(v), 2)


def _add_minutes(hhmm: str, minutes: int) -> str:
    hh, mm = (int(x) for x in hhmm.split(":")[:2])
    total = (hh * 60 + mm + minutes) % (24 * 60)
    return f"{total // 60:02d}:{total % 60:02d}"


def resolve_time(anchor: str, timings: dict | None, sleep_habit: str, fallback: str) -> str:
    """Turn an anchor into a clock time using real adhan times when available."""
    if not timings:
        return fallback
    prayer, offset = ANCHOR_OFFSETS.get(anchor, ANCHOR_OFFSETS["anytime"])
    base = timings.get(prayer)
    if not base:
        return fallback
    if anchor in SHIFTED_ANCHORS:
        offset += SLEEP_SHIFT.get(sleep_habit, 0)
    return _add_minutes(base, offset)


async def _fetch_month(lat: float, lng: float, method: int, school: int,
                       year: int, month: int) -> dict[str, dict]:
    url = f"{ALADHAN_BASE}/calendar/{year}/{month}"
    params = {"latitude": lat, "longitude": lng, "method": method, "school": school}
    async with httpx.AsyncClient(timeout=12) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        payload = resp.json()
    if payload.get("code") != 200 or not payload.get("data"):
        raise ValueError("bad AlAdhan payload")

    out: dict[str, dict] = {}
    for day in payload["data"]:
        greg = day.get("date", {}).get("gregorian", {}).get("date")  # DD-MM-YYYY
        if not greg:
            continue
        dd, mm, yyyy = greg.split("-")
        iso = f"{yyyy}-{mm}-{dd}"
        timings = day.get("timings", {})
        out[iso] = {p: (timings.get(p) or "").split(" ")[0] for p in PRAYERS}
    return out


async def month_timings(lat: float, lng: float, method: int, school: int,
                        year: int, month: int) -> dict[str, dict]:
    lat, lng = _round_coord(lat), _round_coord(lng)
    db = get_db()
    key = {"latitude": lat, "longitude": lng, "method": method,
           "school": school, "year": year, "month": month}
    cached = await db.prayer_months.find_one(key, {"_id": 0, "days": 1})
    if cached:
        return cached["days"]
    try:
        days = await _fetch_month(lat, lng, method, school, year, month)
    except Exception:
        return {}
    await db.prayer_months.update_one(
        key, {"$setOnInsert": {**key, "days": days, "cached_at": datetime.now(timezone.utc)}},
        upsert=True)
    return days


async def timings_for_dates(location: dict | None, method: int, school: int,
                            dates: list[str]) -> dict[str, dict]:
    """Prayer times keyed by ISO date; empty dict when the user has no location."""
    if not location or location.get("latitude") is None:
        return {}
    months = {(d[:4], d[5:7]) for d in dates}
    out: dict[str, dict] = {}
    for year, month in sorted(months):
        out.update(await month_timings(location["latitude"], location["longitude"],
                                       method, school, int(year), int(month)))
    return {d: out[d] for d in dates if d in out}


async def timings_for_day(location: dict | None, method: int, school: int,
                          day: str | None = None) -> dict:
    day = day or date.today().isoformat()
    found = await timings_for_dates(location, method, school, [day])
    return found.get(day, {})


async def search_city(query: str) -> list[dict]:
    params = {"q": query, "format": "jsonv2", "addressdetails": 1, "limit": 6}
    headers = {"User-Agent": "Ihyaa/1.0 (islamic health app)"}
    try:
        async with httpx.AsyncClient(timeout=10, headers=headers) as client:
            resp = await client.get(NOMINATIM, params=params)
            resp.raise_for_status()
            rows = resp.json()
    except Exception:
        return []

    out = []
    for row in rows:
        addr = row.get("address", {})
        city = (addr.get("city") or addr.get("town") or addr.get("village")
                or addr.get("state") or row.get("name") or "")
        out.append({
            "label": row.get("display_name", ""),
            "city": city,
            "country": addr.get("country", ""),
            "country_code": (addr.get("country_code") or "").upper(),
            "latitude": float(row["lat"]),
            "longitude": float(row["lon"]),
        })
    return out


# Country -> most commonly accepted calculation method, used as a smart default.
COUNTRY_METHOD = {
    "ID": 20, "MY": 3, "BN": 3, "SG": 3,
    "SA": 4, "AE": 4, "QA": 4, "KW": 4, "BH": 4, "OM": 4, "YE": 4,
    "EG": 5, "SD": 5, "LY": 5, "JO": 5, "SY": 5, "LB": 5, "IQ": 5,
    "PK": 1, "IN": 1, "BD": 1, "AF": 1,
    "US": 2, "CA": 2,
    "TR": 3, "GB": 3, "FR": 3, "DE": 3, "NL": 3, "AU": 3, "ZA": 3, "NG": 3,
}


def default_method(country_code: str | None) -> int:
    return COUNTRY_METHOD.get((country_code or "").upper(), 3)
