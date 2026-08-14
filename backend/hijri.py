"""Hijri calendar periodization.

This is the app's answer to "a year-long plan gets boring". The Islamic year already
has structure that no habit tracker uses: Ramadan, the six of Shawwal, the first ten
of Dhul Hijjah, Ashura, Sha'ban as a run-up, Ayyam al-Bid every month, and the weekly
Monday/Thursday rhythm. Anchoring content to that calendar means the same walking
habit genuinely reads differently in Ramadan than in an ordinary week - variety comes
from the year itself, not from inventing more tasks.

The conversion below is the standard tabular ("Kuwaiti") arithmetic calendar. It is
deterministic, offline, and accurate to within a day or two of observed dates.

  IMPORTANT: this is for SCHEDULING BLOCKS ONLY. Actual religious observance follows
  local moonsighting or a local authority, and may differ by a day. Never present a
  computed date as the authoritative start of Ramadan, Eid or a fast - `prayer.py`
  already calls AlAdhan for real times and should be the source of truth if a exact
  ruling date is ever surfaced to the user.
"""
from __future__ import annotations

from datetime import date

MONTH_NAMES = {
    1: ("Muharram", "Muharram", "مُحَرَّم"),
    2: ("Safar", "Safar", "صَفَر"),
    3: ("Rabi al-Awwal", "Rabiul Awal", "رَبِيع الأَوَّل"),
    4: ("Rabi al-Thani", "Rabiul Akhir", "رَبِيع الآخِر"),
    5: ("Jumada al-Ula", "Jumadil Awal", "جُمَادَى الأُولَى"),
    6: ("Jumada al-Akhirah", "Jumadil Akhir", "جُمَادَى الآخِرَة"),
    7: ("Rajab", "Rajab", "رَجَب"),
    8: ("Sha'ban", "Sya'ban", "شَعْبَان"),
    9: ("Ramadan", "Ramadan", "رَمَضَان"),
    10: ("Shawwal", "Syawal", "شَوَّال"),
    11: ("Dhul Qa'dah", "Zulkaidah", "ذُو القَعْدَة"),
    12: ("Dhul Hijjah", "Zulhijah", "ذُو الحِجَّة"),
}


def _gregorian_to_jdn(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    return (d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4
            - y2 // 100 + y2 // 400 - 32045)


def to_hijri(g: date) -> tuple[int, int, int]:
    """Gregorian date -> (hijri_year, hijri_month, hijri_day), tabular calendar."""
    jdn = _gregorian_to_jdn(g.year, g.month, g.day)
    l = jdn - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = (((10985 - l) // 5316) * ((50 * l) // 17719)
         + (l // 5670) * ((43 * l) // 15238))
    l = (l - ((30 - j) // 15) * ((17719 * j) // 50)
         - (j // 16) * ((15238 * j) // 43) + 29)
    month = (24 * l) // 709
    day = l - (709 * month) // 24
    year = 30 * n + j - 30
    return year, month, day


# Ordered by precedence - the first match wins.
BLOCKS: list[dict] = [
    {
        "id": "ramadan",
        "name": {"en": "Ramadan", "id": "Ramadan", "ar": "رَمَضَان"},
        "intent": {
            "en": "Fasting changes everything. Training moves close to iftar, food becomes about what breaks the fast well, and sleep is the thing most at risk.",
            "id": "Puasa mengubah segalanya. Latihan bergeser mendekati iftar, makanan berfokus pada berbuka yang baik, dan tidur adalah hal yang paling terancam.",
            "ar": "الصيام يغيّر كل شيء: يقترب التدريب من الإفطار، ويصير الطعام همّه حسن الفطر، ويبقى النوم أكثر ما يُهدَّد.",
        },
        "match": lambda hm, hd: hm == 9,
        "task_intensity": 0.8,
        "notes": "Anaerobic power drops but aerobic capacity and strength hold (ev_ramadan_training). Do NOT frame Ramadan as weight loss - the effect reverts (ev_ramadan_transient).",
    },
    {
        "id": "shawwal_six",
        "name": {"en": "The Six of Shawwal", "id": "Enam Hari Syawal", "ar": "سِتٌّ مِنْ شَوَّال"},
        "intent": {
            "en": "Carrying Ramadan forward instead of losing it. This is the window where the year's gains are kept or dropped.",
            "id": "Membawa Ramadan ke depan alih-alih kehilangannya. Inilah jendela di mana capaian setahun dipertahankan atau dilepaskan.",
            "ar": "استدامة أثر رمضان بدل ضياعه؛ ففي هذه النافذة يُحفَظ مكسب العام أو يُفرَّط فيه.",
        },
        "match": lambda hm, hd: hm == 10 and 2 <= hd <= 12,
        "task_intensity": 0.9,
        "notes": "Directly addresses the 2-5 week post-Ramadan reversion window documented in ev_ramadan_transient.",
    },
    {
        "id": "dhul_hijjah_ten",
        "name": {"en": "The First Ten of Dhul Hijjah", "id": "Sepuluh Hari Pertama Zulhijah", "ar": "العَشْرُ الأُوَل مِنْ ذِي الحِجَّة"},
        "intent": {
            "en": "The most concentrated ten days of the year. Peak block - highest volume, highest intent.",
            "id": "Sepuluh hari paling padat sepanjang tahun. Blok puncak - volume tertinggi, niat tertinggi.",
            "ar": "أكثف عشرة أيام في العام: كتلة الذروة، أعلى حجمٍ وأعلى همّة.",
        },
        "match": lambda hm, hd: hm == 12 and hd <= 10,
        "task_intensity": 1.15,
        "notes": "Peak periodization block.",
    },
    {
        "id": "ashura",
        "name": {"en": "Muharram and Ashura", "id": "Muharram dan Asyura", "ar": "المُحَرَّم وَعَاشُورَاء"},
        "intent": {
            "en": "A new year opening on a fast. A natural reset point for anything that slipped.",
            "id": "Tahun baru yang dibuka dengan puasa. Titik reset alami untuk apa pun yang sempat lepas.",
            "ar": "عامٌ جديد يُفتتح بصيام، ونقطةُ استئنافٍ طبيعية لكل ما تراخى.",
        },
        "match": lambda hm, hd: hm == 1 and 1 <= hd <= 12,
        "task_intensity": 1.0,
        "notes": None,
    },
    {
        "id": "shaban_prep",
        "name": {"en": "Sha'ban - the run-up", "id": "Sya'ban - persiapan", "ar": "شَعْبَان - الاستعداد"},
        "intent": {
            "en": "Build the base now so Ramadan is not a shock. This is a preparation block in the training sense.",
            "id": "Bangun fondasi sekarang agar Ramadan tidak mengejutkan. Ini blok persiapan dalam arti latihan.",
            "ar": "ابنِ الأساس الآن كي لا يكون رمضان مفاجأة؛ فهذه كتلة إعداد بالمعنى التدريبي.",
        },
        "match": lambda hm, hd: hm == 8,
        "task_intensity": 1.05,
        "notes": "Deliberate taper-and-build before the Ramadan load change.",
    },
    {
        "id": "ayyam_bid",
        "name": {"en": "The White Days", "id": "Ayyamul Bidh", "ar": "أَيَّامُ البِيض"},
        "intent": {
            "en": "The monthly three. A small recurring peak that keeps the month from flattening out.",
            "id": "Tiga hari bulanan. Puncak kecil berulang yang menjaga bulan tidak mendatar.",
            "ar": "ثلاثةُ كلِّ شهر: ذروةٌ صغيرة متكرّرة تمنع الشهر من الرتابة.",
        },
        "match": lambda hm, hd: 13 <= hd <= 15,
        "task_intensity": 1.05,
        "notes": None,
    },
    {
        "id": "ordinary",
        "name": {"en": "Steady days", "id": "Hari-hari tetap", "ar": "أَيَّامُ الاستقامة"},
        "intent": {
            "en": "No special season. This is where the habit is actually built - most of the year is ordinary, and that is the point.",
            "id": "Tidak ada musim istimewa. Di sinilah kebiasaan benar-benar dibangun - sebagian besar tahun adalah hari biasa, dan itulah intinya.",
            "ar": "لا موسم خاصّ، وهنا تُبنى العادة حقًّا؛ فأكثر العام أيام عادية، وذلك هو المقصود.",
        },
        "match": lambda hm, hd: True,
        "task_intensity": 1.0,
        "notes": None,
    },
]

BLOCKS_BY_ID = {b["id"]: b for b in BLOCKS}


def block_for(g: date) -> dict:
    """Which periodization block does this Gregorian date fall in?"""
    _, hm, hd = to_hijri(g)
    for block in BLOCKS:
        if block["match"](hm, hd):
            return block
    return BLOCKS_BY_ID["ordinary"]


def describe(g: date, lang: str = "en") -> dict:
    hy, hm, hd = to_hijri(g)
    block = block_for(g)
    names = MONTH_NAMES.get(hm, ("", "", ""))
    idx = {"en": 0, "id": 1, "ar": 2}.get(lang, 0)
    return {
        "hijri_year": hy,
        "hijri_month": hm,
        "hijri_day": hd,
        "hijri_month_name": names[idx],
        "hijri_label": f"{hd} {names[idx]} {hy}",
        "block_id": block["id"],
        "block_name": block["name"].get(lang, block["name"]["en"]),
        "block_intent": block["intent"].get(lang, block["intent"]["en"]),
        "task_intensity": block["task_intensity"],
        "approximate": True,
    }


def is_sunnah_fast_day(g: date) -> bool:
    """Monday, Thursday, or one of the white days."""
    _, _, hd = to_hijri(g)
    return g.weekday() in (0, 3) or 13 <= hd <= 15
