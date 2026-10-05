# Ihyaa — Test Credentials

Seeded automatically on backend startup (`/app/backend/server.py` startup hook).
Values come from `/app/backend/.env`.

| Role  | Email             | Password           | Notes                                        |
|-------|-------------------|--------------------|----------------------------------------------|
| Admin | admin@ihyaa.app   | Ihyaa#Admin2026    | `role: admin`, onboarding NOT completed yet  |
| Demo  | demo@ihyaa.app    | Demo#Ihyaa2026     | Regular user, used for onboarding/e2e flows  |

## Notes for testers
- Auth is JWT Bearer. `POST /api/auth/login` returns `access_token` + `refresh_token`.
  Send `Authorization: Bearer <access_token>` on all other calls.
- Google sign-in uses Emergent-managed Google Auth (`POST /api/auth/google/session`
  with `{"session_id": "..."}`). Cannot be exercised without a real Google session.
- New accounts can be created freely via `POST /api/auth/register`.
- After 5 failed logins for the same email the account is locked for 15 minutes.
  Use a fresh email if you hit a 429 while testing.
- The frontend is an **Expo React Native** app served via Expo Web on port 3000.

## Coach regression accounts — 5 Oct 2026
Preview-only accounts created by the iteration 2 testing agent. Keep this file private;
do not distribute it with public source exports. The regression helper now records new accounts.

| Role | Email | Password | Notes |
|---|---|---|---|
| Coach regression user | test_coach_00ee48e9a6@example.com | Coach#00ee48e9a6Aa1 | Preview test |
| Coach regression user | test_coach_07c410b048@example.com | Coach#07c410b048Aa1 | Preview test |
| Coach regression user | test_coach_0c5f67265d@example.com | Coach#0c5f67265dAa1 | Preview test |
| Coach regression user | test_coach_140f91c0f0@example.com | Coach#140f91c0f0Aa1 | Preview test |
| Coach regression user | test_coach_211d6320c1@example.com | Coach#211d6320c1Aa1 | Preview test |
| Coach regression user | test_coach_2a766777aa@example.com | Coach#2a766777aaAa1 | Preview test |
| Coach regression user | test_coach_338770fec1@example.com | Coach#338770fec1Aa1 | Preview test |
| Coach regression user | test_coach_35eaf73aec@example.com | Coach#35eaf73aecAa1 | Preview test |
| Coach regression user | test_coach_4a2658b1d5@example.com | Coach#4a2658b1d5Aa1 | Preview test |
| Coach regression user | test_coach_52b2502e23@example.com | Coach#52b2502e23Aa1 | Preview test |
| Coach regression user | test_coach_60e9305c4d@example.com | Coach#60e9305c4dAa1 | Preview test |
| Coach regression user | test_coach_6654848825@example.com | Coach#6654848825Aa1 | Preview test |
| Coach regression user | test_coach_825ebb6eee@example.com | Coach#825ebb6eeeAa1 | Preview test |
| Coach regression user | test_coach_8dad911e94@example.com | Coach#8dad911e94Aa1 | Preview test |
| Coach regression user | test_coach_94f64bc461@example.com | Coach#94f64bc461Aa1 | Preview test |
| Coach regression user | test_coach_a15db6bfed@example.com | Coach#a15db6bfedAa1 | Preview test |
| Coach regression user | test_coach_a827b6ba5f@example.com | Coach#a827b6ba5fAa1 | Preview test |
| Coach regression user | test_coach_f11c79dc3e@example.com | Coach#f11c79dc3eAa1 | Preview test |
