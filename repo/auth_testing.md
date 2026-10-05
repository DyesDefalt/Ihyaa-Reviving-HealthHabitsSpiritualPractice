# Auth preservation checks

Keep the existing JWT, bcrypt, email lockout and Google-session behaviour unchanged.
Read private credentials from memory/test_credentials.md (never expose them in chat).
Use REACT_APP_BACKEND_URL from frontend/.env for all API checks.

1. Verify Mongo users.email unique index, login_attempts.identifier, reset-token TTL.
2. Login with the documented test user; check tokens and /api/auth/me.
3. Bearer and refresh-token paths must remain compatible with the existing app.
4. Registration/profile/onboarding language accepts only en/id; legacy ar users load as en.
5. Coach endpoints require authentication. Another user cannot read, send into, or delete a session.
6. Validate frontend streaming errors and token refresh without exposing raw provider errors.