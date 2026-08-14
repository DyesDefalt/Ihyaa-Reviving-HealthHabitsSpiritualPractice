"""Ihyaa curriculum - the public surface the API talks to.

The habit content itself no longer lives here. It moved to backend/data/ as JSON
so that a citation can be verified independently of the habit that cites it, and
so the pool can grow past the 68 hand-written templates that made a year-long plan
repeat every couple of weeks. This module is now a thin adapter over:

    planner.py   - which habit is scheduled on which day
    evidence.py  - the citation and Islamic-source layer, with its shipping gates
    safety.py    - contraindication filtering
    hijri.py     - Hijri-calendar periodization

Content is trilingual (en / id / ar) and nothing here involves haram substances,
riba, or practices outside mainstream Sunni fiqh.
"""
from datetime import date

import evidence
import planner

PILLARS = ["spiritual", "physical", "nutrition", "mental"]

LEVELS = {"beginner": 1, "practicing": 2, "devoted": 3,
          "intermediate": 2, "advanced": 3}

def T(en: str, idn: str, ar: str) -> dict:
    return {"en": en, "id": idn, "ar": ar}


# --------------------------------------------------------------------- phases

PHASE_DEFS: dict[str, list[dict]] = {
    "30_days": [
        {"days": 30,
         "name": T("Foundation", "Fondasi", "التأسيس"),
         "desc": T("Two-minute habits until they stop feeling like effort.",
                   "Kebiasaan dua menit sampai tidak lagi terasa berat.",
                   "عادات من دقيقتين حتى تزول عنها المشقّة.")},
    ],
    "100_days": [
        {"days": 25,
         "name": T("Foundation", "Fondasi", "التأسيس"),
         "desc": T("Small and daily. We are building the floor you will stand on.",
                   "Kecil dan harian. Kita sedang membangun lantai tempat Anda berdiri.",
                   "صغير ويومي؛ نبني الأرض التي ستقف عليها.")},
        {"days": 25,
         "name": T("Depth", "Kedalaman", "العمق"),
         "desc": T("The same habits, but now with understanding — meaning before quantity.",
                   "Kebiasaan yang sama, kini dengan pemahaman — makna sebelum jumlah.",
                   "العادات نفسها لكن بفهم؛ المعنى قبل الكم.")},
        {"days": 25,
         "name": T("Strength", "Kekuatan", "القوّة"),
         "desc": T("Load increases: real training, real fasting, real discipline.",
                   "Beban meningkat: latihan sungguhan, puasa sungguhan, disiplin sungguhan.",
                   "يزيد الحمل: تدريب حقيقي وصيام حقيقي وانتظام حقيقي.")},
        {"days": 25,
         "name": T("Istiqamah", "Istiqamah", "الاستقامة"),
         "desc": T("Nothing new. Just proof that it holds without motivation.",
                   "Tidak ada yang baru. Hanya bukti bahwa ia bertahan tanpa motivasi.",
                   "لا جديد؛ فقط إثبات أنها تثبت بلا حماسة.")},
    ],
    "1_year": [
        {"days": 30, "name": T("Foundation", "Fondasi", "التأسيس"),
         "desc": T("Start absurdly small. Show up, that is all.",
                   "Mulai sangat kecil. Cukup hadir, itu saja.",
                   "ابدأ صغيرًا جدًّا؛ يكفي أن تحضر.")},
        {"days": 30, "name": T("Discipline", "Kedisiplinan", "الالتزام"),
         "desc": T("Fixed times, fixed places. Remove every decision.",
                   "Waktu tetap, tempat tetap. Hilangkan setiap keputusan.",
                   "أوقات ثابتة وأماكن ثابتة؛ أزل كل قرار.")},
        {"days": 30, "name": T("Purity", "Kesucian", "الطهارة"),
         "desc": T("Clean your intake — food, screens, speech, company.",
                   "Bersihkan asupan Anda — makanan, layar, ucapan, pergaulan.",
                   "طهّر ما يدخلك: طعامًا وشاشة وكلامًا وصحبة.")},
        {"days": 30, "name": T("Strength", "Kekuatan", "القوّة"),
         "desc": T("Build a body that can carry long qiyam and long walks.",
                   "Bangun tubuh yang mampu menopang qiyam dan perjalanan panjang.",
                   "ابنِ جسدًا يحمل قيامًا طويلًا ومشيًا طويلًا.")},
        {"days": 30, "name": T("Stillness", "Ketenangan", "السكينة"),
         "desc": T("Learn to sit with silence without reaching for the phone.",
                   "Belajar duduk dalam sunyi tanpa meraih ponsel.",
                   "تعلّم الجلوس مع الصمت دون أن تمتدّ يدك للهاتف.")},
        {"days": 30, "name": T("Generosity", "Kedermawanan", "الكرم"),
         "desc": T("Give until giving becomes reflex rather than decision.",
                   "Memberi sampai memberi menjadi refleks, bukan keputusan.",
                   "أعطِ حتى يصير العطاء طبعًا لا قرارًا.")},
        {"days": 30, "name": T("Knowledge", "Ilmu", "العلم"),
         "desc": T("Twenty minutes a day of something beneficial, every day.",
                   "Dua puluh menit sehari untuk sesuatu yang bermanfaat, setiap hari.",
                   "عشرون دقيقة يوميًا في علم نافع، كل يوم.")},
        {"days": 30, "name": T("Patience", "Kesabaran", "الصبر"),
         "desc": T("The hard middle. This phase is deliberately unglamorous.",
                   "Bagian tengah yang berat. Fase ini memang tidak menarik.",
                   "الوسط الشاقّ؛ هذه المرحلة غير برّاقة بقصد.")},
        {"days": 30, "name": T("Gratitude", "Syukur", "الشكر"),
         "desc": T("Count what you were given before you count what is missing.",
                   "Hitung yang telah diberikan sebelum menghitung yang belum ada.",
                   "عُدّ ما أُعطيت قبل أن تعدّ ما فقدت.")},
        {"days": 30, "name": T("Service", "Pengabdian", "الخدمة"),
         "desc": T("Turn your health outward: be useful to people.",
                   "Arahkan kesehatan Anda ke luar: bermanfaat bagi orang lain.",
                   "وجّه صحّتك للخارج: كن نافعًا للناس.")},
        {"days": 30, "name": T("Depth", "Kedalaman", "العمق"),
         "desc": T("Tahajjud, i'tikaf, long fasts. Only if the base is solid.",
                   "Tahajud, i'tikaf, puasa panjang. Hanya jika fondasinya kuat.",
                   "تهجّد واعتكاف وصيام أطول، بشرط ثبات الأساس.")},
        {"days": 35, "name": T("Istiqamah", "Istiqamah", "الاستقامة"),
         "desc": T("A whole year in. Now it is simply who you are.",
                   "Satu tahun penuh. Sekarang ini memang siapa diri Anda.",
                   "سنة كاملة؛ الآن هذه هي هُويّتك.")},
    ],
}


def phase_of(day: int, challenge_type: str) -> tuple[int, dict, int, int]:
    """Return (1-based phase index, phase def, phase start day, phase end day)."""
    defs = PHASE_DEFS.get(challenge_type) or PHASE_DEFS["30_days"]
    cursor = 0
    for i, ph in enumerate(defs):
        start = cursor + 1
        end = cursor + ph["days"]
        if day <= end or i == len(defs) - 1:
            return i + 1, ph, start, end
        cursor = end
    return 1, defs[0], 1, defs[0]["days"]


def phase_summary(day: int, challenge_type: str, lang: str) -> dict:
    lang = lang if lang in ("en", "id", "ar") else "en"
    defs = PHASE_DEFS.get(challenge_type) or PHASE_DEFS["30_days"]
    index, ph, start, end = phase_of(day, challenge_type)
    return {
        "index": index,
        "total": len(defs),
        "name": ph["name"].get(lang) or ph["name"]["en"],
        "description": ph["desc"].get(lang) or ph["desc"]["en"],
        "start_day": start,
        "end_day": end,
        "day_in_phase": max(1, day - start + 1),
        "phase_days": end - start + 1,
    }


# --------------------------------------------------------------------- helpers

# Prayer-anchored default reminder slots (local clock, 24h). These are only
# fallbacks - prayer.py resolves the real adhan-derived time per user.
ANCHOR_TIMES = {
    "fajr": "05:15", "morning": "07:00", "dhuhr": "12:30", "asr": "15:45",
    "maghrib": "18:20", "isha": "19:45", "night": "21:30", "anytime": "09:30",
}
SLEEP_SHIFT = {"early_bird": -30, "moderate": 0, "night_owl": 45}


def anchor_time(anchor: str, sleep_habit: str) -> str:
    base = ANCHOR_TIMES.get(anchor, "09:30")
    shift = SLEEP_SHIFT.get(sleep_habit, 0)
    if anchor in ("fajr", "night", "isha") and shift:
        hh, mm = (int(x) for x in base.split(":"))
        total = (hh * 60 + mm + shift) % (24 * 60)
        return f"{total // 60:02d}:{total % 60:02d}"
    return base


def tasks_for_day(day: int) -> int:
    return planner.tasks_for_day(day)


# Presentation registry. Keys look like "p_walk#3" - a family plus its progression
# step - so one habit can appear at several difficulties without duplicating text.
TEMPLATES_BY_KEY = planner.presentations_by_key()


def localize(template: dict, lang: str) -> dict:
    """Render one presentation for the UI, with its sourcing resolved.

    Evidence and Islamic sources are looked up by id rather than inlined, and a
    hadith is withheld unless a reviewer has verified it - see evidence.py.
    """
    lang = lang if lang in ("en", "id", "ar") else "en"
    if not template:
        return {}

    def pick(field):
        val = template.get(field)
        return (val.get(lang) or val.get("en")) if isinstance(val, dict) else val

    title = pick("title")
    label = pick("label")
    resolved = evidence.resolve_for_template(template, lang)
    primary_ev = resolved["evidence"][0] if resolved["evidence"] else None
    quran = resolved["quran"][0] if resolved["quran"] else None
    hadith = resolved["hadith"][0] if resolved["hadith"] else None

    return {
        "template_key": template["key"],
        "family_key": template.get("family_key"),
        "pillar": template["pillar"],
        "title": f"{title} - {label}" if label else title,
        "description": pick("desc"),
        # Legacy string fields, kept so existing clients keep working.
        "quran_reference": f"{quran['text']} ({quran['label']})" if quran else None,
        "hadith_reference": f"{hadith['text']} ({hadith['label']})" if hadith else None,
        "science_reference": primary_ev["claim"] if primary_ev else None,
        # Structured sourcing - grade, DOI and caveat are all user-visible now.
        "evidence": resolved["evidence"],
        "quran": resolved["quran"],
        "hadith": resolved["hadith"],
        "evidence_grade": resolved["weakest_grade"],
        "target_steps": template.get("target_steps"),
    }


def pillar_priority(goals: list[str], focus: str = "body") -> list[str]:
    """Body first.

    The previous implementation added a permanent +1 to spiritual with the comment
    "it is the reason this app exists", which put spiritual ahead of body every
    single day and contradicted the product's own positioning. Ordering now comes
    from the user's declared focus.
    """
    order: list[str] = []
    for pillar in planner.pillar_cycle(focus):
        if pillar not in order:
            order.append(pillar)
    return order


def generate_plan(prefs: dict, total_days: int, start: date,
                  challenge_type: str = "30_days") -> list[dict]:
    """Adapter over planner.generate_plan, preserving the stored task shape."""
    sleep_habit = prefs.get("sleep_habit", "moderate")
    rows = planner.generate_plan(
        challenge_type=challenge_type,
        start_date=start,
        focus=prefs.get("focus", "body"),
        fitness_level=prefs.get("fitness_level", "beginner"),
        health_profile=prefs.get("health_profile"),
        seed=prefs.get("plan_seed", "ihyaa"),
    )
    out: list[dict] = []
    for row in rows:
        if row["day_number"] > total_days:
            continue
        out.append({
            "template_key": row["template_key"],
            "pillar": row["pillar"],
            "day_number": row["day_number"],
            "scheduled_date": row["scheduled_date"],
            "scheduled_time": anchor_time(row["anchor"], sleep_habit),
            "anchor": row["anchor"],
            "duration_minutes": row["duration_minutes"],
            "difficulty": row["difficulty"],
            "points_reward": row["points_reward"],
        })
    return out
