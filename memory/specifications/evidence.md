# Ihyaa — Content & Evidence Strategy

# Ihyaa — Content & Evidence Strategy

Updated 28 Sep 2026: Ditambahkan open source data sources dan API yang bisa digunakan untuk mempercepat content pipeline.

## 0\. Open Source Data Sources
Content pipeline bisa dipercepat dengan data yang sudah ada, daripada menulis semuanya dari nol.
### Quran

| Source | License | Content | Usage |
| ---| ---| ---| --- |
| [gadingnst/quran-api](https://github.com/gadingnst/quran-api) (818★) | MIT | Arabic, transliteration, ID/EN translation, tafsir Kemenag, audio | Vendor as SQLite. Primary Quran source. |
| [EQuran.id API](https://equran.id/apidev) | Free | Quran, doa, dzikir, 6 reciters audio | Supplementary. Cache locally. |
| [Al Quran Cloud](https://alquran.cloud/api) | Open | Quran text, translations, audio (global) | Fallback. Verify translation licensing. |

### Hadith

| Source | License | Content | Usage |
| ---| ---| ---| --- |
| [gadingnst/hadith-api](https://github.com/gadingnst/hadith-api) (396★) | MIT | 9 collections: Bukhari, Muslim, Tirmidhi, Abu Dawud, Nasai, Ibn Majah, Ahmad, Darimi, Malik. Arabic + Indonesian. | Vendor. But grading metadata is unreliable — curate separately. |
| [irsyadulibad/hadits-database](https://github.com/irsyadulibad/hadits-database) (66★) | MIT | SQL database of Indonesian hadith translations | Reference for offline import format. |

Hadith grading (sahih/hasan/dhaif) NOT reliably available in open datasets. Ihyaa must maintain its own curated grading table with scholar review. Never infer "sahih" from collection name alone.

### Prayer Times & Islamic Calendar

| Source | Content | Usage |
| ---| ---| --- |
| [AlAdhan API](https://aladhan.com) (already used) | Prayer times, Hijri conversion, Qibla. Method 20 = Kemenag. | Primary. Monthly MongoDB cache. |
| [Kemenag SIHAT](https://sihat.kemenag.dev/pengembang) | Official Indonesian prayer data | Best authoritative source. Requires registration. |
| [myQuran API v3](https://api.myquran.com/doc) | Indonesian prayer schedules, Quran, calendar | Fallback. Data sourced from Kemenag. |
| [EQuran.id Prayer API](https://equran.id/apidev/shalat) | 517 Indonesian districts, Bimas Islam data | Low-friction fallback. Cache locally. |

### Halal Product Verification

| Source | Content | Usage |
| ---| ---| --- |
| [BPJPH Cek Produk Halal](https://bpjph.halal.go.id/cari/sertifikat) | Official halal certification database | Verification only. No public API. Scrape carefully or partner. |
| [Open Food Facts](https://world.openfoodfacts.org/data) | Barcode → nutrition, ingredients, allergens (crowdsourced) | Supplementary. Halal labels unreliable. ODbL license. |

### Mobile Libraries

| Library | License | What For | Verdict |
| ---| ---| ---| --- |
| [adhan-js](https://github.com/batoulapps/adhan-js) (530★) | MIT | Client-side prayer time calculation (offline) | ✅ Add for offline support |
| [@tabby-ai/hijri-converter](https://github.com/tabby-ai/hijri-converter) | MIT | Hijri date conversion (Umm al-Qura), TypeScript | ✅ Fasting calendar + Ramadan detection |
| [react-native-calendars](https://github.com/wix/react-native-calendars) (10K★) | MIT | Calendar views, marked dates | ✅ Plan tab calendar |
| [react-native-bottom-sheet](https://github.com/gorhom/react-native-bottom-sheet) (9K★) | MIT | Bottom sheets for evidence cards | ✅ Better UX than modal |
| [react-native-health-connect](https://github.com/matinzd/react-native-health-connect) (414★) | MIT | Android Health Connect (steps, sleep) | ✅ Phase 2 wearable integration |

### Reference Only (GPL — DO NOT COPY CODE)
*   [Loop Habit Tracker](https://github.com/iSoron/uhabits) (GPL-3.0, 10K★) — streak scoring reference
*   [Quran Android](https://github.com/quran/quran_android) (GPL-3.0) — architecture reference

* * *
## 1\. Philosophy
Setiap rekomendasi kesehatan di Ihyaa harus lolos **dua lapis verifikasi**:

1. **Clinical evidence**: Penelitian medis modern dengan DOI yang valid, bukan retracted, dan evidence level yang jelas.
2. **Islamic source**: Quran (sahih by definition), Hadits (sahih/hasan only, dhaif dengan disclaimer), atau pendapat ulama klasik yang diakui.

Tidak ada konten yang ship tanpa lolos kedua layer ini. Ini bukan nice-to-have; ini core value proposition.

* * *
## 2\. Evidence Pipeline
### Flow: Research → Verify → Review → Ship

```plain
New habit/recommendation identified
    │
    ▼
Literature search (PubMed, Google Scholar, Cochrane)
    │
    ▼
DOI validation → Check retraction status → Grade evidence level
    │
    ▼
Islamic source search (Quran, Sunnah, classical scholars)
    │
    ▼
Hadith grading verification (sahih/hasan/dhaif via multiple sources)
    │
    ▼
Contraindication mapping (medical safety check)
    │
    ▼
Scholar review (Islamic content only)
    │
    ▼
Content writing (Bahasa Indonesia + English)
    │
    ▼
Ship to production
```

### Evidence Grading System

| Level | Clinical Equivalent | Islamic Equivalent | Display |
| ---| ---| ---| --- |
| Strong | Meta-analysis, systematic review, large RCT | Quran, Sahih Bukhari/Muslim | Green badge |
| Moderate | Small RCT, cohort study, case-control | Sahih (other collections), Hasan | Yellow badge |
| Limited | Observational, in-vitro, animal study | Dhaif (with disclaimer) | Orange badge + disclaimer |
| Expert Opinion | Clinical guidelines, consensus | Classical scholar opinion, ijma' | Blue badge |

* * *
## 3\. Content Categories
### 3.1 Physical (Body)
Habits yang berhubungan dengan aktivitas fisik, exercise, dan gerakan.

**Islamic sources**: Walking to mosque, archery, swimming, horse riding (hadits), physical strength as believer's trait.

**Clinical backing**: WHO physical activity guidelines, exercise physiology research.

**Contraindication examples**: Joint problems, heart conditions, pregnancy modifications.
### 3.2 Nutrition (Makanan & Minuman)
Habits yang berhubungan dengan makan, minum, dan diet.

**Islamic sources**: Kurma, madu, zaitun, habbatussauda, makan 1/3 perut, berhenti sebelum kenyang, tidak berlebihan.

**Clinical backing**: Nutritional epidemiology, dietary intervention studies.

**Contraindication examples**: Diabetes (karbohidrat), CKD (protein), hipertensi (garam), alergi makanan.
### 3.3 Spiritual (Ruh)
Habits yang berhubungan dengan ibadah dan koneksi spiritual.

**Islamic sources**: Sholat, dzikir, baca Quran, doa, sedekah, puasa.

**Clinical backing**: Psychoneuroimmunology, mindfulness research, stress reduction studies.

**Contraindication examples**: OCD/waswas (avoid excessive repetition), severe depression (professional help first).
### 3.4 Mental (Akal)
Habits yang berhubungan dengan kesehatan mental, kognitif, dan emosional.

**Islamic sources**: Tafakkur, muhasabah, sabar, syukur, husnuzhan.

**Clinical backing**: CBT, positive psychology, gratitude research, sleep hygiene.

**Contraindication examples**: Severe mental health conditions (refer to professional), trauma triggers.

* * *
## 4\. Classical Scholar References
### Ibn Sina (Avicenna) — 980-1037 CE
**Primary source**: Al-Qanun fi al-Tibb (The Canon of Medicine)

**Relevant teachings**:
*   Makanan sebagai obat (food as medicine)
*   Keseimbangan (mizaj/temperament)
*   Pentingnya olahraga teratur
*   Hygiene dan cleanliness
*   Sleep hygiene
### Al-Zahrawi (Abulcasis) — 936-1013 CE
**Primary source**: Al-Tasrif (30-volume medical encyclopedia)

**Relevant teachings**:
*   Surgical innovation (menunjukkan pentingnya medical advancement)
*   Nutrition dan diet dalam pengobatan
*   Preventive care
### Ibn Qayyim al-Jawziyya — 1292-1350 CE
**Primary source**: Al-Tibb al-Nabawi (Medicine of the Prophet)

**Relevant teachings**:
*   Thibbun nabawi (prophetic medicine)
*   Holistic health (body, mind, soul)
*   Kurma, madu, zaitun sebagai healing foods
*   Pentingnya tidur yang cukup
*   Olahraga yang disunnahkan
### Ibn Sina on Eating (from Canon of Medicine)
> "Janganlah kamu makan kecuali setelah lapar, dan janganlah kamu berhenti makan kecuali sebelum kenyang." — Prinsip yang sekarang divalidasi oleh penelitian tentang caloric restriction dan mindful eating.
* * *
## 5\. Contraindication Database
### Medical Conditions Mapped

| Condition | Affected Habit Categories | Severity Rules |
| ---| ---| --- |
| Chronic Kidney Disease (CKD) | Nutrition (protein, potassium, fluid), Fasting | BLOCK: prolonged fasting, high-protein diets. WARN: fluid intake targets. |
| Type 1 Diabetes (T1DM) | Nutrition (carb counting), Fasting, Exercise timing | BLOCK: unsupervised fasting. WARN: exercise without glucose monitoring. |
| Type 2 Diabetes (T2DM) | Nutrition (sugar, carb), Fasting, Weight management | WARN: fasting with medication adjustment. INFO: carb timing. |
| Hypertension | Nutrition (sodium), Exercise intensity, Stress | WARN: high-intensity exercise, high-sodium foods. INFO: DASH diet principles. |
| Pregnancy | Exercise, Nutrition, Fasting | BLOCK: prolonged fasting, high-intensity exercise, certain foods. WARN: calorie restriction. |
| Anticoagulant (Warfarin) | Nutrition (vitamin K), Herbal supplements | BLOCK: sudden vitamin K changes. WARN: herbal remedies interaction. |
| Eating Disorder History | All food tracking, Calorie counting | WARN: calorie counting features. INFO: mindful eating alternative. |
| OCD/Waswas | Spiritual habits (repetitive) | WARN: excessive repetition tracking. INFO: qualified scholar guidance. |

* * *
## 6\. Scholar Review Process
### Current Status
*   **16 Quran sources**: Cleared to ship. Quran is sahih by definition.
*   **15 hadith sources**: **PENDING**. Need scholar review before shipping.
### Review Requirements
1. Reviewer harus punya credential Islamic studies (minimum S1 Syariah/Ushuluddin)
2. Reviewer harus verify: grading, translation accuracy, context appropriateness
3. Setiap hadith harus cross-referenced dengan minimal 2 grading sources
4. Kontroversial content (e.g., medical claims from hadith) harus ada disclaimer
### Blocker

TOP RISK: Hadith review blocker has NO OWNER and NO DATE. This is the #1 risk identified in the CEO Advisor review. Fix: name a reviewer, set a target date, track as visible workstream.

* * *
## 7\. Retraction Monitoring
### Process
1. Every DOI is checked against Retraction Watch database before shipping
2. Quarterly re-verification of all shipped DOIs
3. If a DOI is retracted: immediate content flag, push notification to affected users, content update in next OTA
### Known Retractions
*   **PREDIMED 2013** (DOI: 10.1056/NEJMoa1200303): Retracted and republished with corrections. Hard-blocklisted. Original findings about Mediterranean diet were largely maintained but with methodological corrections.

* * *
## 8\. Content Writing Guidelines
### Tone
*   **Bahasa Indonesia**: Warm, encouraging, non-judgmental. Use "yuk" not "kamu harus". Frame everything as opportunity, not obligation.
*   **English**: Same warmth. Avoid clinical jargon. Write like a knowledgeable friend.
### Structure per Habit Card

```plain
[Nama habit]
[1-2 sentence description]
[Time estimate]
[Evidence card — expandable]
  [Clinical: DOI, journal, year, key finding, evidence level]
  [Islamic: Source text, translation, reference, grading]
  [Classical scholar: Name, book, relevant quote]
[Contraindication warning if applicable]
[Complete button]
```

### Language Rules
*   Always Bahasa Indonesia first, English second
*   Arabic text only when necessary (Quran verses, key hadith phrases)
*   No transliteration without translation
*   Use "insya Allah" not "mudah-mudahan" (more universally accepted)

* * *
## 9\. Content Expansion Roadmap
### Phase 1 (Current): 76 template families, 204 presentations
Focus: Core habits across all 4 categories. Foundation set.
### Phase 2: +50 templates (target: 126 families)
Priority additions:
*   Ramadan-specific habits (tarawih, qiyamul lail, iftar etiquette)
*   Women's health (menstruation-friendly exercise, pregnancy nutrition)
*   Elderly-friendly habits (gentle movement, fall prevention)
*   Kids habits (family plan support)
### Phase 3: +100 templates (target: 226 families)
Priority additions:
*   Chronic disease management (diabetes-friendly, heart-healthy)
*   Mental health deep dive (anxiety, depression, grief)
*   Seasonal variations (hajj preparation, umrah health)
*   Indonesian local wisdom (jamu, traditional practices with evidence)
### Phase 4: Community-Generated
*   User-submitted habits (with review pipeline)
*   Ustadz/expert curated collections
*   Local mosque community challenges

* * *
## 10\. Quality Metrics

| Metric | Target | Current |
| ---| ---| --- |
| Evidence coverage (habits with ≥1 clinical + ≥1 Islamic source) | 100% | ~70% |
| Contraindication coverage (habits with safety mapping) | 100% | ~85% |
| Scholar review completion | 100% | ~52% (16/31) |
| Retraction check currency | <90 days | Current |
| 365-day repeat gap | 60 days | 26 days |