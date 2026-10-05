# Ihyaa — Technical Specifications

# Ihyaa — Technical Specifications

Updated 28 Sep 2026: Sekarang match dengan codebase aktual di branch preview-dev (FastAPI + MongoDB + Expo SDK 54). Sebelumnya mengusulkan Supabase/SQLite yang ternyata tidak dipakai. Keputusan: JANGAN migrasi. Backend sudah jalan dan teruji.

## 1\. Architecture Overview
### Current State (Preview-Dev Branch, verified 28 Sep 2026)
**Frontend**: Expo SDK 54 + expo-router + TypeScript. React 19.1, RN 0.81.5. File-based routing di `frontend/app/`. Tabs: Today, Plan, Progress, Store, Profile. Plus: checkin, coach, knowledge, onboarding, sign-in. State: AsyncStorage + expo-secure-store (no Zustand/Redux, direct API calls via `src/api.ts`).

**Backend**: FastAPI + Motor/MongoDB. Single `server.py` (52KB) + modules: `auth.py`, `content.py`, `curriculum.py`, `library.py`, `milestones.py`, `prayer.py`, `health.py`, `db.py`, `models.py`, `templates_advanced.py`, `templates_lifestyle.py`. JWT auth (1-day access, 30-day refresh), bcrypt, email lockout (5 tries, 15 min).

**AI Coach**: Claude Sonnet 4.6 via Emergent Universal Key (`litellm` custom wheel). Multi-turn history in MongoDB. Guardrails: halal + non-medical. **VENDOR LOCKED — needs replacement.**

**Prayer Times**: AlAdhan API v1, monthly MongoDB cache, method=20 (Kemenag) supported + smart default per country. Anchor offsets per prayer. Sleep-habit shift. Offline fallback: fixed clock defaults.

**Design System**: `design_guidelines.json`. Deep pine #1B3B36 + terracotta #B5653E on warm paper #F7F5F0. Fonts: Outfit (Latin), Tajawal (Arabic UI), Amiri (scripture). Light + dark themes. RTL support via I18nManager.

**Test Reports**: `test_reports/iteration_1.json` — verified fixes: email-keyed lockout, refresh token precedence, daily bonus anti-farm, date validation, CORS, store localization, coach prompt formatting.
### Tech Stack (Target — Post Decoupling)

| Layer | Current (preview-dev) | Target | Reasoning |
| ---| ---| ---| --- |
| Framework | Expo SDK 54 + TypeScript ✅ | Same | Already working, EAS ready |
| Navigation | Expo Router v6 ✅ | Same | File-based, type-safe |
| State | AsyncStorage + SecureStore | Add Zustand for complex state | Current works but will need structure as features grow |
| Backend | FastAPI + MongoDB ✅ | Same (decoupled from Emergent) | Working, tested. Don't migrate. |
| Database | MongoDB (Motor async driver) | Same + add Qdrant for vectors | Mongo works. Qdrant free tier for embeddings. |
| Auth | JWT + bcrypt + Emergent Google | JWT + bcrypt + standard Google OAuth | Replace Emergent-managed Google with own OAuth client |
| AI Coach | Claude Sonnet 4.6 (Emergent) ⚠️ | GPT-6 Luna (primary) + DeepSeek V4.1-Flash (fallback) | $0.06-0.20/$0.37-1.20 per 1M tokens. Cheapest current-gen OpenAI. Reliable. Good Bahasa. |
| Personalization | Deterministic plan engine | \+ Jev (decision layer) + bandit scheduler | Jev for intent classification + habit scoring. Thompson Sampling for reminder timing. |
| Prayer Times | AlAdhan API + MongoDB cache ✅ | Same + Kemenag SIHAT (if approved) | Method 20 = Kemenag. Monthly cache works. Add SIHAT as primary source. |
| Push | expo-notifications (local) ✅ | \+ Server-side push (Expo Push API) | Local works. Server push needed for reinstall survival + streak nudges. |
| Content Data | Hardcoded in Python modules | \+ quran-api + hadith-api (vendored SQLite) | Bundle curated content, not runtime API calls. |
| Analytics | None | PostHog (self-hosted) or Amplitude free | Need DAU/retention/funnel data before paid marketing. |
| Crash | None | Sentry | Must-have before Play Store. |
| CI/CD | Emergent preview only | EAS Build + EAS Submit + GitHub Actions | Already has eas.json build profile task in backlog. |

### System Architecture (Target)

```plain
Mobile App (Expo SDK 54 / React Native)
  ├── UI Layer (expo-router, 5 tabs + modals)
  ├── State (AsyncStorage + Zustand)
  ├── API Client (src/api.ts → FastAPI)
  ├── Local Notifications (expo-notifications)
  ├── Design System (design_guidelines.json)
  └── i18n (EN/ID/AR, RTL support)
         │ HTTPS (JWT Bearer)
         ▼
FastAPI Backend (self-hosted, decoupled from Emergent)
  ├── Auth (JWT + bcrypt + Google OAuth)
  ├── Plan Engine (deterministic scheduler, 1% better)
  ├── Prayer Engine (AlAdhan API + MongoDB monthly cache)
  ├── Evidence Engine (DOI + Quran/Hadith citations)
  ├── Safety Layer (contraindication filter)
  ├── Points/Streak Engine
  ├── AI Coach (GPT 6 Luna via provider abstraction)
  ├── Personalization (Jev decision layer + bandit scheduler)
  └── Push Service (Expo Push API, server-scheduled)
         │
    ┌────┴────┐
    ▼         ▼
MongoDB    Qdrant (vectors)
(primary)  (habit/content embeddings)
```

* * *
## 2\. Data Model
### Current MongoDB Collections (from [models.py](http://models.py), verified)
**users** — \_id, email, name, password\_hash, auth\_provider (password|google), picture, role, language (en|ar|id), theme, timezone, onboarding\_completed, is\_pro, pro\_until, points\_balance, lifetime\_points, current\_streak, longest\_streak, last\_checkin\_date, grace\_used\_dates\[\], prefs (embedded Preferences)

**Preferences (embedded in User)** — fitness\_level, health\_goals\[\], dietary\_preferences\[\], sleep\_habit, spiritual\_level, preferred\_challenge (30\_days|100\_days|1\_year), reminders\_enabled, prayer\_method (AlAdhan id), prayer\_school (0=Shafii, 1=Hanafi), location (GeoLocation), age, sex, height\_cm, weight\_kg, conditions\[\], work\_pattern, wake\_time

**challenges** — \_id, user\_id, challenge\_type, status (active|paused|completed|abandoned), start\_date, end\_date, total\_days

**daily\_tasks** — \_id, user\_id, challenge\_id, template\_key, pillar, day\_number, scheduled\_date, scheduled\_time, time\_overridden, anchor, duration\_minutes, difficulty, points\_reward, completed, completed\_at

**milestones** — \_id, user\_id, challenge\_id, kind (weekly|monthly), index, template\_key, start\_date, end\_date, points\_reward, completed, completed\_at

**checkins** — \_id, user\_id, challenge\_id, checkin\_date, mood\_rating (1-5), energy\_rating (1-5), gratitude\_note, reflection\_note, tasks\_completed, tasks\_total, points\_earned — UNIQUE(user\_id, checkin\_date)

**point\_transactions** — \_id, user\_id, amount, type (earned|redeemed), source, description

**coach\_messages** — \_id, user\_id, role (user|assistant), content

**prayer\_months** (cache) — latitude, longitude, method, school, year, month, days{}, cached\_at

**daily\_bonuses** (anti-farm marker) — user\_id, date, bonus\_type
### New Collections Needed (Phase 2+)
**evidence\_records** — habit\_template\_key, evidence\_type (clinical\_doi|quran|hadith|classical\_scholar), doi, journal, publication\_year, study\_type, key\_finding\_id, key\_finding\_en, evidence\_level, is\_retracted, source\_text, translation\_id, translation\_en, reference, grading (sahih|hasan|dhaif), scholar\_name, review\_status, reviewed\_by, reviewed\_at

**contraindications** — habit\_template\_key, condition, severity (info|warning|block), message\_id, message\_en, alternative\_template\_key

**habit\_embeddings** (Qdrant, not MongoDB) — template\_key, vector (384d), metadata {pillar, category, goals\[\], conditions\_safe\[\], time\_of\_day}

**user\_preference\_vectors** (Qdrant) — user\_id, vector, last\_updated

**bandit\_state** — user\_id, arm\_id (reminder\_time|tone|task\_size), alpha, beta, last\_pulled, total\_reward, total\_pulls

**notification\_log** — user\_id, sent\_at, type, arm\_id, opened, action\_taken, habit\_completed\_within\_window
### Key Indexes (MongoDB)

```javascript
db.daily_tasks.createIndex({user_id: 1, scheduled_date: 1, completed: 1});
db.daily_tasks.createIndex({user_id: 1, challenge_id: 1, day_number: 1});
db.checkins.createIndex({user_id: 1, checkin_date: 1}, {unique: true});
db.point_transactions.createIndex({user_id: 1, created_at: -1});
db.coach_messages.createIndex({user_id: 1, created_at: 1});
db.prayer_months.createIndex({latitude: 1, longitude: 1, method: 1, school: 1, year: 1, month: 1}, {unique: true});
db.daily_bonuses.createIndex({user_id: 1, date: 1, bonus_type: 1}, {unique: true});
```

**health\_profiles** — id, user\_id (FK), age, gender, weight\_kg, height\_cm, conditions\[\], allergies\[\], medications\[\], activity\_level, dietary\_restrictions\[\]

**islamic\_profiles** — id, user\_id (FK), prayer\_consistency, quran\_reading\_level, fasting\_experience, preferred\_madhab, prayer\_calc\_method, latitude, longitude, timezone

**habit\_templates** — id, name\_id, name\_en, description\_id, description\_en, category (physical/nutrition/spiritual/mental), subcategory, frequency, target\_days\[\], time\_of\_day, difficulty, estimated\_minutes, is\_active, sort\_order

**evidence\_records** — id, habit\_template\_id (FK), evidence\_type (clinical\_doi/quran/hadith/classical\_scholar), doi, journal, publication\_year, study\_type, sample\_size, key\_finding\_id, key\_finding\_en, evidence\_level (strong/moderate/limited), is\_retracted, source\_text, translation\_id, translation\_en, reference, grading (sahih/hasan/dhaif), scholar\_name, review\_status (pending/approved/rejected), reviewed\_by, reviewed\_at

**contraindications** — id, habit\_template\_id (FK), condition, severity (info/warning/block), message\_id, message\_en, alternative\_habit\_id

**user\_habits** — id, user\_id (FK), habit\_template\_id (FK), custom\_name, is\_active, current\_streak, longest\_streak, total\_completions, reminder\_enabled, reminder\_minutes\_before, started\_at, archived\_at

**habit\_completions** — id, user\_habit\_id (FK), completed\_date, completed\_at, value, notes, mood — UNIQUE(user\_habit\_id, completed\_date)

**meal\_plans** — id, user\_id (FK), plan\_date, meal\_type (sahur/breakfast/lunch/iftar/dinner/snack), food\_name, portion, calories, is\_halal, protein\_g, carbs\_g, fat\_g, fiber\_g, is\_completed — UNIQUE(user\_id, plan\_date, meal\_type)

**water\_logs** — id, user\_id (FK), log\_date, glasses, target\_glasses — UNIQUE(user\_id, log\_date)

**sleep\_logs** — id, user\_id (FK), sleep\_date, bedtime, wake\_time, duration\_minutes, quality (1-5), qailulah\_minutes — UNIQUE(user\_id, sleep\_date)

**prayer\_logs** — id, user\_id (FK), prayer\_date, prayer\_name (fajr/dhuhr/asr/maghrib/isha), status (on\_time/late/missed/qadha), prayed\_at, location — UNIQUE(user\_id, prayer\_date, prayer\_name)

**pahala\_logs** — id, user\_id (FK), log\_date, source\_type, source\_id, pahala\_points, description\_id, description\_en

**fasting\_logs** — id, user\_id (FK), fasting\_date, fasting\_type (ramadan/sunnah\_mon\_thu/arafah/ashura/shawwal/ayyamul\_bidh/other), is\_completed, sahur\_time, iftar\_time — UNIQUE(user\_id, fasting\_date)
### Key Indexes (MongoDB)

```javascript
db.daily_tasks.createIndex({user_id: 1, scheduled_date: 1, completed: 1});
db.daily_tasks.createIndex({user_id: 1, challenge_id: 1, day_number: 1});
db.checkins.createIndex({user_id: 1, checkin_date: 1}, {unique: true});
db.point_transactions.createIndex({user_id: 1, created_at: -1});
db.coach_messages.createIndex({user_id: 1, created_at: 1});
db.prayer_months.createIndex({latitude: 1, longitude: 1, method: 1, school: 1, year: 1, month: 1}, {unique: true});
db.daily_bonuses.createIndex({user_id: 1, date: 1, bonus_type: 1}, {unique: true});
```

* * *
## 3\. Key Algorithms
### 3.1 Habit Scheduling (LRU + Prayer-Aligned)

```plain
1. Filter habits by contraindication (safety layer)
2. Score by LRU (days since last shown)
3. Boost prayer-aligned habits
4. Select top N for today (N = user capacity)
5. Schedule around prayer times
```

Worst case repeat gap: 26 days (365-day window). Target: 60 days. Limited by content volume, not algorithm.
### 3.2 Contraindication Filter
Every habit goes through safety check against user's health conditions:
*   **block**: Habit not shown (e.g., prolonged fasting for CKD patients)
*   **warning**: Habit shown with warning banner (e.g., intense exercise for hypertension)
*   **info**: Habit shown with info note (e.g., caffeine timing for sleep issues)

Tested against: CKD, T1DM, T2DM, pregnancy, anticoagulant, hypertension profiles.
### 3.3 Streak Calculation
Standard streak with target\_days awareness. Only counts days when habit was scheduled. Missed non-scheduled days don't break streak.
### 3.4 Pahala Points
Intentionally simple, non-competitive. No leaderboard. Just personal progress.

| Action | Points |
| ---| --- |
| Prayer on time | 10 |
| Sunnah fasting | 15 |
| Ramadan fasting | 20 |
| Habit completion (easy) | 1 |
| Habit completion (medium) | 2 |
| Habit completion (hard) | 3 |
| Quran reading | 10 |
| Water goal met | 1 |
| Exercise completed | 2 |
| Sleep goal met | 2 |

* * *
## 4\. AI Coach & Personalization (Jev)
### 4.1 AI Coach — "Ustadh Ihyaa"
**Current**: Claude Sonnet 4.6 via Emergent Universal Key (litellm custom wheel). Works but vendor-locked and expensive at scale.

**Target**: Provider abstraction layer (OpenAI-compatible interface) with automatic fallback chain. Any LLM can be swapped via config.

#### Model Selection (Updated 28 Sep 2026)

| Role | Model | Input/1M | Output/1M | Why |
| ---| ---| ---| ---| --- |
| Primary | GPT-6 Luna | $0.06-0.20 | $0.37-1.20 | Cheapest current-gen OpenAI. Reliable infra. Good Bahasa Indonesia. Consistent quality. No peak-hour pricing. |
| Fallback | DeepSeek V4.1-Flash | $0.15-0.30 | $0.60-1.20 | Peak/off-peak (off-peak = 50% off). Outperforms V4-Pro on benchmarks. Vision support. Different infra = failover. |
| Escalation | GPT-6 Luna (Max Effort) | $0.20 | $1.20 | Complex planning, safety-sensitive, structured output requiring high reliability |
| Budget alt | Gemini 3.8 Flash | $0.10 | $0.40 | Cheapest Google option. Strong multilingual. Keep as config option. |

**Why GPT-5.6 Luna over DeepSeek as primary**: OpenAI infrastructure reliability, better Bahasa Indonesia consistency, no peak-hour pricing surprises, simpler billing. DeepSeek V4.1-Flash is excellent as fallback (sometimes even better on benchmarks) and significantly cheaper during off-peak hours.

**Why DeepSeek V4.1-Flash as fallback**: Nearly identical pricing, different infrastructure (failover), occasionally outperforms on reasoning tasks, supports vision (future: food photo analysis), MIT weights available for self-hosting if needed.

#### Fallback Chain

```python
# backend/ai_provider.py
PROVIDERS = [
    {"name": "openai", "model": "gpt-6-luna", "priority": 1},
    {"name": "deepseek", "model": "deepseek-flash", "priority": 2},
    {"name": "google", "model": "gemini-3.8-flash", "priority": 3},
]

async def chat(messages, **kwargs):
    for provider in PROVIDERS:
        try:
            return await call_provider(provider, messages, **kwargs)
        except (RateLimitError, ServiceUnavailable, Timeout):
            continue  # Try next provider
    raise AllProvidersFailed()
```

#### Cost Estimate (100K conversations/month, 2K input + 300 output tokens)

| Scenario | Monthly Cost |
| ---| --- |
| All GPT-5.6 Luna | ~$16-32 |
| 90% Luna + 10% DeepSeek fallback | ~$15-30 |
| 50% Luna (peak) + 50% DeepSeek (off-peak) | ~$12-24 |

Negligible vs Rp49k/month per subscriber revenue. AI is not a cost concern at this scale.

**Guardrails** (server-side, not prompt-only):
*   Two-stage contract: LLM outputs structured JSON → Pydantic validation → business-rule check → execute
*   Intent classification: motivation, habit\_plan, prayer\_time, health\_general, medical\_request, religious\_ruling, other
*   Medical/religious-ruling intents → informational only + referral to professional
*   Never pass raw health records, phone numbers, exact location to LLM
*   Allow-listed action types only (adjust\_habit, suggest\_reminder, log\_completion)
*   Verify habit\_id belongs to authenticated user before any mutation
### 4.2 Jev — Decision/Personalization Layer
**What Jev is**: Typed decision model by TypeSafe AI. You give it context + structured questions, it returns calibrated probabilities (choice/score/noul). NOT a chatbot. NOT a replacement for the LLM coach. 70-500ms latency, ~$0.42/1M input tokens.

**How Ihyaa uses Jev** (complementary to GPT Luna + DeepSeek):

| Use Case | Jev Role | Why Jev (not LLM) |
| ---| ---| --- |
| Intent classification | Classify user message: plan\_adjustment, medical, religious, general | 70ms vs 2s. No hallucination. Calibrated confidence for routing. |
| Habit scoring | Score candidate habits for today based on user profile + history | Batch 20-50 candidates in 1 request. Probabilistic ranking. |
| Safety routing | Flag uncertain/sensitive requests → escalate to stronger model or human | Calibrated probability = reliable fallback trigger. |
| Notification timing | Score candidate reminder times for each user | Fast enough for real-time personalization at scale. |

**Jev does NOT**: generate text, replace the chat coach, store user memory, make Islamic rulings.

**Alternatives to Jev** (if Jev unavailable or pricing changes): Any decision/classification model that supports structured output with calibrated probabilities. Options include: fine-tuned small models (Llama 3.2 3B, Qwen 3.5 7B), or simply using GPT-5.6 Luna with constrained JSON output (slower but same provider). The key requirement is: fast, structured, no hallucination, calibrated confidence.
### 4.3 Bandit-Based Reminder Personalization
Inspired by Duolingo's Recovering Difference Softmax Algorithm (0.5% DAU lift, 2% retention lift).

**Approach**: Contextual Thompson Sampling (simple, effective, no deep learning infra needed).

**Arms** (what we optimize):
*   Reminder time: after\_fajr, morning, lunch, after\_maghrib, evening
*   Tone: encouraging, concise, reflective
*   Task size: 2min, 5min, 15min

**Context**: timezone, prayer window, recent adherence (7d), notification fatigue, day of week, last dismissal.

**Reward**: habit completed within 2-hour window. Negative: notification dismissed, app uninstalled.

**Constraints**: max 2 reminders/day, quiet hours 22:00-04:00, random holdout 5% for unbiased measurement.
### 4.4 Embedding-Based Habit Recommendation
**Model**: `text-embedding-3-small` ($0.02/1M tokens) or self-hosted `multilingual-e5-small` (384d, free).

**Vector Store**: Qdrant Cloud free tier (0.5 vCPU, 1GB RAM, 4GB disk). Sufficient for MVP catalog.

**What gets embedded**: habit descriptions, plan templates, motivation messages, user free-text goals.

**What does NOT get embedded**: raw health events, check-in logs, personal data. Structured fields for those.

**Flow**: User goal text → embed → Qdrant similarity search → top 20 candidates → Jev scores/reranks → top 5 shown.

* * *
## 5\. API Endpoints (FastAPI, current + planned)
### Current (implemented in [server.py](http://server.py))

```plain
POST   /api/auth/register              -- Email + password register
POST   /api/auth/login                 -- JWT login (access + refresh)
POST   /api/auth/refresh               -- Token refresh
POST   /api/auth/logout                -- Invalidate tokens
GET    /api/auth/me                    -- Current user profile
POST   /api/auth/forgot                -- Password reset request
POST   /api/auth/reset                 -- Password reset confirm
POST   /api/auth/google/session        -- Google OAuth (Emergent-managed)
PUT    /api/user/profile               -- Update profile + preferences
PUT    /api/user/location              -- Update location + prayer method
POST   /api/onboarding                 -- Complete onboarding, generate plan
POST   /api/challenge/start            -- Start 30/100/365-day challenge
GET    /api/tasks/today                -- Today's scheduled tasks
PUT    /api/tasks/:id/complete         -- Mark task complete/incomplete
PUT    /api/tasks/:id/time             -- Override scheduled time
GET    /api/plan                       -- Full plan calendar
POST   /api/checkin                    -- Daily mood/energy/gratitude check-in
GET    /api/progress                   -- Stats, streaks, charts
GET    /api/points                     -- Points balance + history
POST   /api/store/redeem               -- Redeem points for Pro
POST   /api/coach                      -- AI coach chat (multi-turn)
GET    /api/coach/history              -- Chat history
GET    /api/knowledge                  -- Knowledge library cards
GET    /api/prayer/times               -- Prayer times for location
GET    /api/prayer/cities              -- City search (Nominatim)
POST   /api/hydration                  -- Log water intake
GET    /api/milestones                 -- Milestone progress
```

### Planned (Phase 2)

```plain
GET    /api/evidence/:templateKey      -- Full evidence card for habit
GET    /api/ramadan/mode               -- Ramadan-specific config + habits
POST   /api/fasting/log                -- Log fasting day
GET    /api/fasting/calendar           -- Hijri fasting calendar
POST   /api/push/register              -- Register Expo push token
GET    /api/food/scan/:barcode         -- Barcode → product info (Open Food Facts)
GET    /api/food/halal/:barcode        -- Halal verification (BPJPH + OFF)
POST   /api/personalize/score          -- Jev habit scoring endpoint
GET    /api/analytics/summary          -- User analytics dashboard
```

* * *
## 6\. External APIs & Open Source
### Content & Data

| API/Library | License | What For | Verdict |
| ---| ---| ---| --- |
| [gadingnst/quran-api](https://github.com/gadingnst/quran-api) | MIT | Quran Arabic + transliteration + ID/EN translation + tafsir Kemenag | ✅ Vendor as SQLite bundle |
| [gadingnst/hadith-api](https://github.com/gadingnst/hadith-api) | MIT | 9 hadith collections with Indonesian translation | ✅ Vendor, but curate grading separately |
| [EQuran.id API](https://equran.id/apidev) | Free | Quran, doa, dzikir, prayer times (517 Indonesian cities) | ✅ Supplementary source |
| [myQuran API v3](https://api.myquran.com/doc) | Free | Indonesian prayer schedules, Quran, calendar | ✅ Fallback for prayer times |
| [AlAdhan API](https://aladhan.com) | Open | Prayer times, Hijri conversion, Qibla (already used) | ✅ Keep as primary, add Kemenag SIHAT if approved |
| [BPJPH Cek Produk Halal](https://bpjph.halal.go.id/cari/sertifikat) | Public | Official halal certification search | ⚠️ No public API. Scrape carefully or seek partnership. |
| [Open Food Facts](https://world.openfoodfacts.org/data) | ODbL | Barcode → nutrition, ingredients, allergens | ✅ Supplementary. Halal status unreliable. |

### Mobile Libraries (Expo/React Native)

| Library | License | What For | Verdict |
| ---| ---| ---| --- |
| [adhan-js](https://github.com/batoulapps/adhan-js) | MIT | Client-side prayer time calculation (offline fallback) | ✅ Add for offline prayer times |
| [@tabby-ai/hijri-converter](https://github.com/tabby-ai/hijri-converter) | MIT | Hijri date conversion (Umm al-Qura) | ✅ Use for fasting calendar + Ramadan detection |
| [react-native-calendars](https://github.com/wix/react-native-calendars) | MIT | Calendar views, marked dates, agenda | ✅ Use for Plan tab calendar |
| [react-native-progress](https://github.com/oblador/react-native-progress) | MIT | Progress rings/bars | ✅ Already using SVG; keep custom or switch |
| [react-native-bottom-sheet](https://github.com/gorhom/react-native-bottom-sheet) | MIT | Bottom sheets for evidence cards, habit detail | ✅ Better UX than modal for evidence |
| [react-native-health-connect](https://github.com/matinzd/react-native-health-connect) | MIT | Android Health Connect (steps, sleep, heart rate) | ✅ Phase 2 wearable integration |

### Reference Only (GPL — DO NOT COPY CODE)
*   [Loop Habit Tracker](https://github.com/iSoron/uhabits) (GPL-3.0, 10K★) — streak scoring, reminder UX reference
*   [Quran Android](https://github.com/quran/quran_android) (GPL-3.0) — architecture reference

* * *
## 7\. Offline & Caching Strategy
**Current**: Prayer times cached monthly in MongoDB (server-side). Frontend has no offline mode yet.

**Target (Phase 2)**:
*   **Prayer times**: Client-side calculation via adhan-js as offline fallback. Server cache remains primary.
*   **Hijri calendar**: Client-side via @tabby-ai/hijri-converter. No API needed.
*   **Content**: Bundle curated Quran/Hadith evidence as SQLite or JSON with app. Update via OTA.
*   **User data**: Today's tasks + recent completions cached in AsyncStorage. Offline completion queued, synced on reconnect.
*   **AI Coach**: Requires network. Show cached conversation history offline.

**Sync rules**: Server wins for profile. Client wins for task completions (with server timestamp reconciliation).
* * *
## 8\. Security & Privacy
### Current (implemented)
*   TLS 1.3 in transit
*   bcrypt password hashing
*   JWT with short-lived access tokens (1 day) + refresh (30 days)
*   Email-keyed brute-force lockout (5 tries → 15 min)
*   CORS explicit origins
*   Input validation via Pydantic
### Needed before production
*   MongoDB authentication + TLS (not just localhost trust)
*   Rate limiting per endpoint (not just login)
*   Health data encryption at rest (MongoDB field-level encryption for conditions\[\])
*   Audit log for admin actions
*   Data export endpoint (GDPR/UU PDP compliance)
*   Account deletion with cascade
### AI Data Privacy
*   Never send health conditions\[\] to LLM unless user explicitly asks health question
*   Anonymize user context before LLM calls (no name, email, exact location)
*   DeepSeek API: DO NOT use for any user data (PRC data residency)
*   Gemini: acceptable for habit coaching. Review Google Cloud DPA.
*   Jev: review TypeSafe AI data processing terms before sending user context
### Known Vulnerability

test\_credentials.md in public repo contains admin/demo passwords. Rotate immediately, remove from git history, or make repo private.

* * *
## 9\. Performance Targets

| Metric | Target |
| ---| --- |
| App launch to interactive | <2 seconds |
| Today screen load | <500ms |
| Habit completion tap | <100ms feedback |
| Offline sync on reconnect | <5 seconds |
| App download size | <50 MB |
| Peak RAM | <150 MB |
| Battery drain | <3% per hour |

* * *
## 10\. Content Volume (Current)

| Category | Template Families | Presentations |
| ---| ---| --- |
| Physical | 68 | ~140 |
| Nutrition | 65 | ~130 |
| Spiritual | 37 | ~80 |
| Mental | 34 | ~70 |
| Total | 76 families | 204 presentations |

*   Evidence: 33 DOI-verified records, all retraction-checked. 1 retracted DOI (PREDIMED 2013) blocklisted.
*   Islamic sources: 31 total. 16 Quran cleared. 15 hadith pending scholar review.
*   Safety layer: HealthProfile + contraindication filtering, tested against CKD/T1DM/pregnancy/anticoagulant.

* * *
## 11\. Build & Deploy
### Current
Preview runs on Emergent platform. `app.json` configured for Expo Web (port 3000). No EAS build profile yet (task exists in backlog).
### Target

```json
{
  "build": {
    "development": { "developmentClient": true, "distribution": "internal" },
    "preview": { "distribution": "internal", "android": { "buildType": "apk" } },
    "production": { "android": { "buildType": "app-bundle" } }
  }
}
```

**Pre-ship checklist**:
- [ ] Decouple from Emergent (replace emergentintegrations + litellm custom wheel)
- [ ] Own Google OAuth client (replace Emergent-managed)
- [ ] Own MongoDB instance (Atlas or self-hosted)
- [ ] EAS build profile configured
- [ ] Sentry DSN configured
- [ ] Play Store internal testing track
- [ ] Privacy policy + terms of service hosted
* * *
## 12\. Testing Strategy
### Current (implemented)
*   Backend test suite: `backend/tests/backend_test.py` (27KB, comprehensive)
*   Test iteration 1: all fixes verified (lockout, token precedence, bonus anti-farm, validation, CORS, localization, coach formatting)
### Needed
*   **Unit**: Plan engine edge cases, prayer anchor resolution, streak with grace days, points calculation
*   **Integration**: Offline-to-online sync, notification scheduling around prayer times, evidence display, Jev scoring flow
*   **E2E (Maestro)**: Onboarding, habit completion, check-in, coach chat, Ramadan mode, store redemption
*   **Safety-critical**: Contraindication blocking (CKD/T1DM/pregnancy/anticoagulant), retraction check, hadith grading labels, AI coach medical/religious refusal
*   **AI eval**: 100-200 prompt Indonesian test set (fluency, cultural fit, refusal quality, schema validity)
* * *
## 13\. Vendor Decoupling Plan (Priority: P0)

The backend CANNOT run outside Emergent in its current state. This blocks EAS builds, Play Store submission, and any independent hosting.

### What to replace

| Emergent Dependency | Replacement | Effort |
| ---| ---| --- |
| `emergentintegrations` package | Direct Google Generative AI SDK (`google-generativeai`) | ~2 hours |
| `litellm` custom wheel | Standard `litellm` from PyPI or direct SDK | ~1 hour |
| Emergent-managed Google Auth | Own Google OAuth 2.0 Client ID/Secret | ~3 hours (Google Console setup + code) |
| Emergent MongoDB | MongoDB Atlas free tier (M0, 512MB) | ~1 hour (connection string swap) |
| Emergent hosting | Railway / Render / [Fly.io](http://Fly.io) free tier | ~2 hours (Dockerfile + deploy) |

**Total estimated effort**: ~1 day of focused work. This is the single highest-leverage task before anything else.