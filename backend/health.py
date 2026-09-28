"""Personal health profile derived from the user's basic info.

Everything here is standard clinical arithmetic (Mifflin-St Jeor, WHO BMI
bands, 30–35 ml/kg hydration, 1.2–1.6 g/kg protein) plus a set of *flags*
that the plan engine uses to boost or exclude habits for this person.
"""

CONDITIONS = ("diabetes", "hypertension", "high_cholesterol", "joint_pain",
              "insomnia", "anxiety", "digestive", "overweight")
WORK_PATTERNS = ("desk", "on_feet", "shift", "home")

ACTIVITY_FACTOR = {"beginner": 1.3, "intermediate": 1.5, "advanced": 1.7}

GOAL_CALORIE_DELTA = {"weight_loss": -400, "build_strength": 200, "more_energy": 0}


def bmi_band(bmi: float | None) -> str | None:
    if bmi is None:
        return None
    if bmi < 18.5:
        return "underweight"
    if bmi < 25:
        return "normal"
    if bmi < 30:
        return "overweight"
    return "obese"


def health_profile(prefs: dict) -> dict:
    age = prefs.get("age")
    sex = prefs.get("sex")
    h = prefs.get("height_cm")
    w = prefs.get("weight_kg")
    goals = set(prefs.get("health_goals") or [])
    conditions = set(prefs.get("conditions") or [])
    level = prefs.get("fitness_level", "beginner")

    bmi = round(w / ((h / 100) ** 2), 1) if h and w else None
    band = bmi_band(bmi)

    bmr = None
    if h and w and age and sex in ("male", "female"):
        bmr = round(10 * w + 6.25 * h - 5 * age + (5 if sex == "male" else -161))
    tdee = round(bmr * ACTIVITY_FACTOR.get(level, 1.3)) if bmr else None
    delta = 0
    for g in goals:
        delta += GOAL_CALORIE_DELTA.get(g, 0)
    if band in ("overweight", "obese") and "weight_loss" not in goals:
        delta -= 200
    if band == "underweight":
        delta = max(delta, 250)
    calorie_target = max(1200, tdee + delta) if tdee else None

    protein_per_kg = 1.6 if ("build_strength" in goals or "weight_loss" in goals) else 1.2
    if age and age >= 60:
        protein_per_kg = max(protein_per_kg, 1.4)
    protein_g = round(w * protein_per_kg) if w else None

    water_ml = round(w * (35 if level != "beginner" else 32) / 50) * 50 if w else 2000
    if "hypertension" in conditions or "diabetes" in conditions:
        water_ml = max(water_ml, 2000)
    water_glasses = max(6, round(water_ml / 250))

    steps = 6000 if level == "beginner" else 8000 if level == "intermediate" else 10000
    if band == "obese" or "joint_pain" in conditions:
        steps = min(steps, 7000)
    sleep_hours = 7.5 if not age or age < 65 else 7.0

    flags: set[str] = set()
    if "diabetes" in conditions:
        flags.update({"no_fasting", "glucose_focus", "low_sugar"})
    if "hypertension" in conditions:
        flags.update({"bp_focus", "low_sodium", "no_hiit"})
    if "high_cholesterol" in conditions:
        flags.update({"lipid_focus"})
    if "joint_pain" in conditions or band == "obese":
        flags.update({"joint_friendly", "no_hiit", "no_jump"})
    if "insomnia" in conditions or "better_sleep" in goals:
        flags.add("sleep_focus")
    if "anxiety" in conditions or "reduce_stress" in goals:
        flags.add("calm_focus")
    if "digestive" in conditions:
        flags.add("gut_focus")
    if band in ("overweight", "obese") or "weight_loss" in goals or "overweight" in conditions:
        flags.add("weight_focus")
    if band == "underweight":
        flags.update({"no_fasting", "gain_focus"})
    if age and age >= 55:
        flags.update({"joint_friendly", "balance_focus"})
    if prefs.get("work_pattern") == "desk":
        flags.add("desk_worker")
    if prefs.get("work_pattern") == "shift":
        flags.update({"sleep_focus", "shift_worker"})
    if sex == "female":
        flags.add("female")
    if "plant_forward" in (prefs.get("dietary_preferences") or []):
        flags.add("plant_forward")

    return {
        "bmi": bmi,
        "bmi_band": band,
        "bmr": bmr,
        "tdee": tdee,
        "calorie_target": calorie_target,
        "protein_g": protein_g,
        "protein_per_kg": protein_per_kg,
        "water_ml": water_ml,
        "water_glasses": water_glasses,
        "step_target": steps,
        "sleep_hours": sleep_hours,
        "flags": sorted(flags),
        "complete": bool(h and w and age and sex),
    }
