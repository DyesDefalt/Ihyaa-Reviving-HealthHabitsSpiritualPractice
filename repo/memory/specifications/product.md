# Ihyaa — Product Requirements Document (PRD)

# Ihyaa — Product Requirements Document

Updated 28 Sep 2026: Sekarang mencerminkan kondisi aktual codebase (branch preview-dev). Bagian "Current State" menunjukkan apa yang sudah ke-build vs yang direncanakan.

## 0\. Current State (Verified 28 Sep 2026)
**Sudah ke-build dan berfungsi** (branch preview-dev, Emergent platform):
*   ✅ Auth: register/login/refresh/logout, JWT, bcrypt, lockout, Google sign-in (Emergent-managed)
*   ✅ Onboarding: 9-step wizard → generates personalized 30-day plan
*   ✅ Plan engine: deterministic scheduler, goal-weighted, 1%-better ramp, prayer-anchored
*   ✅ Today screen: greeting, streak, points, pillar progress rings, expandable habit cards
*   ✅ Plan tab: 42-day strip, per-day dots, local reminders, .ics export
*   ✅ Progress tab: completion ring, streak/best/points stats, pillar bars, 7-day chart
*   ✅ Daily check-in: mood + energy 1-5, gratitude, reflection, streak logic
*   ✅ Points & Store: earn per habit, daily bonus, redeem for Pro (2500/6000/18000 pts)
*   ✅ Pro gating: 100-day & 1-year tracks locked behind Pro
*   ✅ AI Coach "Ustadh Ihyaa": ChatGPT GPT 6 Luna, multi-turn, halal guardrails
*   ✅ Knowledge library: 8 trilingual cards with evidence
*   ✅ Prayer times: AlAdhan API + MongoDB cache, Kemenag method, smart country defaults
*   ✅ Trilingual: EN/ID/AR with RTL support
*   ✅ Design system: design\_guidelines.json (deep pine + terracotta, Outfit/Tajawal/Amiri)
*   ✅ Light + dark themes

**Blocker sebelum production**:
*   ⚠️ Backend vendor-locked ke Emergent (emergentintegrations + litellm custom wheel + managed auth + managed MongoDB)
*   ⚠️ Test credentials exposed di public repo
*   ⚠️ No push notification server (local only)
*   ⚠️ No Sentry/analytics
*   ⚠️ No EAS build profile

**AI Stack (target)**:
*   Primary: GPT-6 Luna ($0.06-0.20/1M input, $0.37-1.20/1M output). Reliable, cheap, good Bahasa Indonesia.
*   Fallback: DeepSeek V4.1-Flash ($0.15-0.30/1M input, $0.60-1.20/1M output). Off-peak 50% discount. Different infra for failover.
*   Decision layer: Jev by TypeSafe AI (70-500ms, structured output, calibrated probabilities). For intent classification, habit scoring, safety routing.
*   Personalization: Thompson Sampling bandit for reminder timing. Embedding pipeline (text-embedding-3-small + Qdrant) for habit recommendation.

* * *
## 1\. Vision
**Ihyaa adalah mobile app yang menggabungkan habit tracking, food & lifestyle planning, dan bimbingan Islami untuk membantu Muslim hidup sehat secara fisik, mental, dan spiritual.**

Bukan sekadar habit tracker. Bukan sekadar prayer reminder. Ihyaa adalah _health companion_ yang membuktikan bahwa gaya hidup sehat berbasis Quran, Hadits, dan ilmuwan Islam (Ibn Sina, Al-Zahrawi, Ibn Qayyim) juga divalidasi oleh penelitian medis modern.
### Tagline
> "Sehat itu ibadah."
### Core Thesis
Muslim habit apps yang ada sekarang hampir semuanya spiritual checklist (sudah sholat? sudah baca Quran?). General fitness apps tidak punya framing halal. Ihyaa duduk di intersection ini: **Body first** (physical + nutrition), backed by **DOI-verified clinical evidence**, dengan **Mind/Soul** sebagai layer yang terintegrasi, bukan terpisah.

* * *
## 2\. Problem Statement
### Masalah yang dipecahkan
1. **Fragmentasi**: Muslim yang mau hidup sehat harus pakai 3-4 app berbeda (fitness tracker, prayer reminder, Quran app, nutrition app). Tidak ada yang menyatukan.
2. **Missing Islamic context**: App kesehatan mainstream tidak mengerti konteks Muslim: puasa Ramadan, waktu sholat, makanan halal, hijri calendar, konsep thibbun nabawi.
3. **Missing scientific context**: App Islami yang ada tidak punya evidence base. Mereka bilang "ini sunnah" tapi tidak bilang KENAPA secara medis itu bermanfaat.
4. **Low retention**: Habit trackers punya retention problem karena tidak punya intrinsic motivation. Ihyaa punya: pahala. Setiap habit sehat = ibadah. Itu motivasi yang lebih kuat dari streak atau badge.
### Target User Persona

| Persona | Deskripsi | Pain Point | Daily Trigger |
| ---| ---| ---| --- |
| Primary: Muslim Health Seeker | 25-45 tahun, urban, middle class, smartphone aktif, aware pentingnya kesehatan tapi bingung mulai dari mana | Terpisah-pisah antara app kesehatan dan app Islam. Mau sehat tapi juga mau dapat nilai ibadah dari usahanya. | Buka app pagi untuk lihat jadwal hari ini, siang untuk log makanan, malam untuk refleksi |
| Secondary: Ramadan Improver | 20-35 tahun, seasonal user yang sangat aktif selama Ramadan, churn setelah Eid | Ramadan adalah reset moment tapi tidak ada tool yang membantu sustain habits setelah Eid | Notifikasi sahur, buka puasa, tarawih tracking |
| Tertiary: Family Health Manager | 30-50 tahun, biasanya ibu yang manage kesehatan keluarga | Kesulitan tracking kesehatan anak + suami + diri sendiri dalam satu tempat | Meal planning, medication reminders, health checklists |

* * *
## 3\. Product Overview
### Core Loop

```plain
Buka app → Lihat "Today" (personalized plan) → Complete habits → 
Dapat feedback (progress + evidence + pahala counter) → 
Lihat streak & weekly summary → Besok repeat
```

### Key Differentiators (vs Competition)

| Fitur | Ihyaa | Muslim Pro | MyFitnessPal | Habitica |
| ---| ---| ---| ---| --- |
| Islamic framing | Core | Core | None | None |
| Health/nutrition tracking | Core | None | Core | Basic |
| Clinical evidence (DOI) | Core | None | Basic | None |
| Hijri calendar integration | Core | Basic | None | None |
| Safety/contraindication layer | Core | None | None | None |
| Scholar-verified content | Core | Partial | None | None |
| Pahala/reward framing | Core | Basic | None | Gamified |

* * *
## 4\. Feature Set
### 4.1 MVP Features (Phase 1)
#### A. Today Screen (Home)
*   Personalized daily plan berdasarkan profil user, waktu sholat, dan health goals
*   Card-based UI: setiap card adalah 1 habit yang bisa di-complete
*   Urutan: Fajr → Morning routine → Meals → Activities → Evening → Isha
*   Pull-down untuk refresh, swipe untuk navigate ke tomorrow/yesterday
#### B. Habit Tracker (Islamic + Health)
*   **Physical habits**: Jalan kaki, stretching, olahraga ringan, tidur cukup
*   **Nutrition habits**: Makan sayur, minum air putih, kurangi gula, makan kurma, madu
*   **Spiritual habits**: Sholat 5 waktu, dzikir pagi/petang, baca Quran, sedekah
*   **Mental habits**: Meditasi/dzikir, journaling, gratitude, digital detox
*   Setiap habit punya: nama, deskripsi, evidence (DOI), Islamic source (Quran/Hadits), contraindication warnings
#### C. Food & Lifestyle Planner
*   Meal planning berdasarkan prinsip thibbun nabawi + modern nutrition
*   Halal food database dengan barcode scanning
*   Intermittent fasting planner (Senin-Kamis sunnah fasting + Ramadan mode)
*   Hydration tracker dengan Islamic framing (air zamzam, sunnah minum)
*   Sleep tracker berdasarkan sunnah (tidur awal, bangun tahajud, qailulah/nap)
#### D. Evidence Layer
*   Setiap habit/rekomendasi punya citation card:
    *   **DOI reference**: Link ke penelitian medis yang relevan
    *   **Islamic source**: Quran verse atau hadits (dengan grading: sahih/hasan/dhaif)
    *   **Classical scholar**: Referensi ke Ibn Sina, Al-Zahrawi, Ibn Qayyim jika relevan
    *   **Contraindication**: Warning untuk kondisi medis tertentu (CKD, diabetes, pregnancy, dll)
#### E. Prayer Time Integration
*   Waktu sholat sebagai anchor untuk daily schedule
*   Habits dijadwalkan around prayer times (bukan sebaliknya)
*   Qibla direction (basic)
*   Adzan notifications
#### F. Basic Onboarding
*   Health profile: usia, gender, kondisi medis, alergi, goals
*   Islamic practice level: seberapa aktif beribadah (untuk personalisasi)
*   Notification preferences
*   Language: Bahasa Indonesia / English
### 4.2 Phase 2 Features
#### G. Ramadan Mode
*   Special UI theme dan habit set untuk Ramadan
*   Sahur/iftar meal planning
*   Tarawih tracking
*   Laylatul Qadr countdown
*   Zakat calculator integration
*   Post-Eid habit transition plan
#### H. Family/Family Plan
*   Multiple profiles dalam satu account
*   Shared meal planning
*   Kids habit tracking (with parental controls)
*   Family challenges
#### I. Community & Social
*   Anonymous progress sharing (opt-in)
*   Local mosque/community groups
*   Group challenges (e.g., "1 juta langkah bersama")
*   Ustadz/expert Q&A
#### J. Wearable Integration
*   Google Fit / Apple Health sync
*   Step counting, heart rate, sleep data
*   Automatic habit completion berdasarkan sensor data
### 4.3 Phase 3 Features
#### K. AI-Powered Personalization (Jev + GPT Luna + DeepSeek)
*   **Jev decision layer**: Intent classification (apa yang user mau?), habit scoring (habit mana yang paling cocok hari ini?), safety routing (kapan escalate ke model yang lebih kuat?)
*   **GPT-6 Luna coach (primary)**: Cheapest current-gen OpenAI ($0.06-0.20/1M input tokens). Reliable, good Bahasa Indonesia, consistent quality. Routine chat dan motivation.
*   **DeepSeek V4.1-Flash (fallback)**: Nearly identical pricing, different infrastructure for failover. Peak/off-peak pricing (off-peak = 50% off). Outperforms V4-Pro on benchmarks.
*   **Automatic fallback chain**: Luna → DeepSeek. No single point of failure.
*   **Bandit-based reminder timing**: Thompson Sampling untuk personalize waktu notifikasi, tone, dan task size. Inspired by Duolingo's notification algorithm.
*   **Embedding-based habit recommendation**: User goal text → vector search → Jev rerank → top 5 suggestions.
*   Adaptive plan adjustment: coach bisa suggest plan changes berdasarkan adherence pattern (dengan user confirmation).
*   Predictive health insights (dengan disclaimer bukan medical advice)
#### L. Marketplace Integration
*   Halal product recommendations
*   Healthy meal delivery partnerships
*   Islamic book/course recommendations

* * *
## 5\. User Experience Flow
### First-Time User Journey

```plain
Install → Splash screen → Language select → Onboarding (5 screens) → 
Health profile setup → Islamic practice level → Goals selection → 
First Today screen → Complete first habit → Celebration animation → 
Prompt notification permission → Done
```

### Daily Active User Journey

```plain
Morning: Notif Fajr → Buka app → Complete morning habits → Sarapan log → 
Siang: Notif Dzuhur → Quick habit check → Log makan siang → 
Sore: Notif Ashar → Activity habit → 
Malam: Notif Maghrib → Log makan malam → Evening habits → 
Notif Isya → Wind down habits → Sleep tracking → 
Weekly: Summary report → Progress review → Adjust goals
```

* * *
## 6\. Success Metrics
### North Star Metric
**Daily Active Users completing ≥3 habits/day**
### Supporting Metrics

| Metric | Target (6 bulan) | Target (12 bulan) |
| ---| ---| --- |
| Downloads | 10,000 | 50,000 |
| D30 Retention | 25% | 35% |
| Daily habits completed per DAU | 3.5 | 4.5 |
| Free → Paid conversion | 5% | 8% |
| Monthly churn | <8% | <5% |
| NPS | 40+ | 50+ |

* * *
## 7\. Constraints & Non-Negotiables

Content Wajib Diverifikasi: Tidak ada konten Islami yang ship tanpa review scholar. Hadits harus sahih/hasan, tidak ada dhaif tanpa disclaimer eksplisit.

Medical Disclaimer: App BUKAN pengganti dokter. Semua health recommendations harus ada disclaimer dan contraindication warnings.

Privacy First: Health data adalah data sensitif. Minimal data collection, on-device processing where possible, transparent privacy policy.

* * *
## 8\. Competitive Positioning
### Positioning Statement
> Untuk Muslim yang ingin hidup sehat, **Ihyaa** adalah health companion yang menggabungkan habit tracking, nutrition planning, dan bimbingan Islami dalam satu app, karena kami percaya sehat itu ibadah dan ibadah itu bisa sehat.
### Key Differentiators
1. **Evidence-backed Islamic health**: Satu-satunya app yang menunjukkan DOI clinical evidence bersama Quran/Hadits reference
2. **Safety-first**: Contraindication layer yang tidak dimiliki kompetitor
3. **Hijri-native**: Calendar dan scheduling yang understands Ramadan, hari sunnah puasa, dll
4. **Indonesia-first**: Bahasa Indonesia, konteks lokal, QRIS integration untuk future payments