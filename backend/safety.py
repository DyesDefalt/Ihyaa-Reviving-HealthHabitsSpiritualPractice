"""Medical safety layer.

Ihyaa prescribes fasting, training and botanicals. Several of those are genuinely
contraindicated for real people, and the app previously collected no health data at
all, so it could not tell. This module is the gate.

Two mechanisms:

  * `contraindications` on a template are matched against the user's health profile.
    A match removes the template from the plan entirely - it is never scheduled and
    never shown.

  * Fasting additionally passes through an IDF-DAR risk stratification. The published
    guideline (Hassanein et al. 2022, doi 10.1016/j.diabres.2021.109185) puts CKD
    stage 4-5, dialysis and diabetic pregnancy in a category advised NOT to fast, and
    a 2024 cohort found 57.9% of high-risk patients who fasted anyway experienced
    hypoglycaemia. This is a gate, not a footnote.

This module is deliberately conservative: when the profile is ambiguous it blocks.
It is decision *support* and does not replace a clinician - `MEDICAL_DISCLAIMER`
must be surfaced wherever these habits appear.
"""
from __future__ import annotations

MEDICAL_DISCLAIMER = {
    "en": "Ihyaa offers general wellbeing guidance, not medical advice. It cannot diagnose or treat. If you are pregnant, managing a health condition, or taking regular medication, speak to your doctor before fasting, changing your diet, or starting new exercise.",
    "id": "Ihyaa memberikan panduan kesehatan umum, bukan nasihat medis. Ini tidak dapat mendiagnosis atau mengobati. Jika Anda hamil, memiliki kondisi kesehatan, atau rutin mengonsumsi obat, konsultasikan dengan dokter sebelum berpuasa, mengubah pola makan, atau memulai olahraga baru.",
    "ar": "يقدّم إحياء إرشادًا عامًا للعافية لا نصيحةً طبية، ولا يُشخّص ولا يعالج. فإن كنتِ حاملًا أو كان لديك مرض أو تتناول دواءً منتظمًا فاستشر طبيبك قبل الصيام أو تغيير الغذاء أو بدء رياضة جديدة.",
}

# Condition ids collected at onboarding.
CONDITIONS = (
    "t1dm", "t2dm", "prediabetes", "hypertension", "heart_disease",
    "ckd_stage_1_2", "ckd_stage_3", "ckd_stage_4_5", "dialysis",
    "asthma", "osteoporosis", "joint_problems", "mobility_impairment",
    "eating_disorder_history", "gastric_ulcer", "migraine", "thyroid",
)

MEDICATIONS = (
    "insulin", "sulfonylurea", "metformin", "anticoagulant", "antihypertensive",
    "diuretic", "corticosteroid", "nsaid", "photosensitising",
)

# Contraindication tags a template may declare.
TAGS = (
    "fasting", "prolonged_fasting", "black_seed", "honey", "vigorous_exercise",
    "high_impact", "prolonged_standing", "breath_holding", "sun_exposure",
    "caloric_restriction", "cold_exposure", "mobility_impairment",
)


def _has(profile: dict, key: str, value: str) -> bool:
    return value in (profile.get(key) or [])


def dar_risk_category(profile: dict) -> str | None:
    """IDF-DAR style stratification. Returns None when diabetes is not present.

    Simplified but deliberately conservative - anything uncertain lands higher.
    """
    conditions = profile.get("conditions") or []
    meds = profile.get("medications") or []
    diabetic = "t1dm" in conditions or "t2dm" in conditions
    if not diabetic:
        return None

    # Very high risk - guideline advises against fasting.
    if "t1dm" in conditions:
        return "very_high"
    if any(c in conditions for c in ("ckd_stage_4_5", "dialysis")):
        return "very_high"
    if profile.get("pregnancy_trimester"):
        return "very_high"
    if profile.get("severe_hypo_last_3_months"):
        return "very_high"

    # High risk - guideline advises against, or requires close supervision.
    if "ckd_stage_3" in conditions or "heart_disease" in conditions:
        return "high"
    if "insulin" in meds:
        return "high"
    if "sulfonylurea" in meds:
        return "moderate"
    return "low"


def blocked_tags(profile: dict | None) -> set[str]:
    """Every contraindication tag this user must not be scheduled."""
    if not profile:
        return set()

    blocked: set[str] = set()
    conditions = profile.get("conditions") or []
    meds = profile.get("medications") or []
    trimester = profile.get("pregnancy_trimester")
    age = profile.get("age")

    # --- Fasting -----------------------------------------------------------
    # Hard blocks straight from the guideline and the pregnancy literature.
    if any(c in conditions for c in ("ckd_stage_4_5", "dialysis")):
        blocked |= {"fasting", "prolonged_fasting", "caloric_restriction"}
    if trimester == 1:
        # First trimester is the sensitive period (Pradella 2024, doi 10.1093/humupd/dmae026).
        blocked |= {"fasting", "prolonged_fasting", "caloric_restriction"}
    if trimester or profile.get("breastfeeding"):
        blocked |= {"prolonged_fasting", "caloric_restriction"}
    if "eating_disorder_history" in conditions:
        blocked |= {"fasting", "prolonged_fasting", "caloric_restriction"}

    risk = dar_risk_category(profile)
    if risk in ("very_high", "high"):
        blocked |= {"fasting", "prolonged_fasting"}
    elif risk == "moderate":
        blocked.add("prolonged_fasting")

    # --- Botanicals --------------------------------------------------------
    # Nigella sativa is antiplatelet and hypoglycaemic - additive with these drugs.
    if "anticoagulant" in meds:
        blocked.add("black_seed")
    if "insulin" in meds or "sulfonylurea" in meds:
        blocked.add("black_seed")
    if trimester:
        blocked.add("black_seed")
    # Honey: infant botulism, and it is still sugar.
    if age is not None and age < 1:
        blocked.add("honey")
    if "t1dm" in conditions or "t2dm" in conditions:
        blocked.add("honey")

    # --- Exercise ----------------------------------------------------------
    if "heart_disease" in conditions:
        blocked.add("vigorous_exercise")
    if "mobility_impairment" in conditions:
        blocked |= {"high_impact", "prolonged_standing", "mobility_impairment"}
    if any(c in conditions for c in ("osteoporosis", "joint_problems")):
        blocked.add("high_impact")
    if trimester in (2, 3):
        blocked |= {"high_impact", "breath_holding"}
    if "asthma" in conditions:
        blocked |= {"breath_holding", "cold_exposure"}
    if age is not None and age >= 65:
        blocked.add("high_impact")

    # --- Other -------------------------------------------------------------
    if "photosensitising" in meds:
        blocked.add("sun_exposure")
    if "gastric_ulcer" in conditions:
        blocked.add("fasting")

    return blocked


def template_allowed(tpl: dict, profile: dict | None) -> bool:
    tags = set(tpl.get("contraindications") or [])
    return not (tags & blocked_tags(profile))


def gate_notices(profile: dict | None, lang: str = "en") -> list[dict]:
    """User-visible explanations for what was withheld and why."""
    if not profile:
        return []
    notices: list[dict] = []
    blocked = blocked_tags(profile)
    risk = dar_risk_category(profile)

    if risk in ("very_high", "high") and "fasting" in blocked:
        notices.append({
            "code": "dar_fasting_gate",
            "severity": "high",
            "title": {
                "en": "Fasting habits are paused for you",
                "id": "Kebiasaan puasa dijeda untuk Anda",
                "ar": "أُوقفت عادات الصيام لك",
            }[lang if lang in ("en", "id", "ar") else "en"],
            "body": {
                "en": "Based on what you shared, international diabetes-and-Ramadan guidance places you in a group advised not to fast without medical supervision. We have removed optional fasting habits from your plan. Please talk to your doctor before fasting.",
                "id": "Berdasarkan yang Anda bagikan, panduan internasional diabetes dan Ramadan menempatkan Anda pada kelompok yang disarankan tidak berpuasa tanpa pengawasan medis. Kami menghapus kebiasaan puasa opsional dari rencana Anda. Silakan bicara dengan dokter Anda sebelum berpuasa.",
                "ar": "بناءً على ما ذكرتَه، تضعك الإرشادات الدولية للسكري ورمضان في فئة يُنصح ألّا تصوم دون إشراف طبي. وقد أزلنا عادات الصيام الاختيارية من خطتك. فراجع طبيبك قبل الصيام.",
            }[lang if lang in ("en", "id", "ar") else "en"],
            "source": "IDF-DAR Practical Guidelines 2021, doi 10.1016/j.diabres.2021.109185",
        })

    if profile.get("pregnancy_trimester"):
        notices.append({
            "code": "pregnancy_gate",
            "severity": "high",
            "title": {
                "en": "Your plan is adjusted for pregnancy",
                "id": "Rencana Anda disesuaikan untuk kehamilan",
                "ar": "عُدّلت خطتك لأجل الحمل",
            }[lang if lang in ("en", "id", "ar") else "en"],
            "body": {
                "en": "Fasting, calorie restriction, black seed and high-impact movement have been removed. Please follow your midwife or doctor's guidance.",
                "id": "Puasa, pembatasan kalori, habbatussauda, dan gerakan berbenturan tinggi telah dihapus. Ikuti panduan bidan atau dokter Anda.",
                "ar": "أُزيل الصيام وتقييد السعرات والحبة السوداء والحركات عالية الارتطام. فاتّبع إرشاد طبيبك أو قابلتك.",
            }[lang if lang in ("en", "id", "ar") else "en"],
            "source": "Pradella et al. 2024, doi 10.1093/humupd/dmae026",
        })

    return notices
