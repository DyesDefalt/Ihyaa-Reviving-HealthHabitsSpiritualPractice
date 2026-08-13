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
- After 5 failed logins from the same IP+email the account is locked for 15 minutes.
  Use a fresh email if you hit a 429 while testing.
- The frontend is an **Expo React Native** app served via Expo Web on port 3000.
