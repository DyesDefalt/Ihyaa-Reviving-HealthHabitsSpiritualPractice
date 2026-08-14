# Android ship readiness (Phase 2e)

Sourced from Expo's current SDK 54 docs (this project's SDK) via Context7, 2026-08-14. Nothing here was submitted to the Play Console — that step needs your own developer account.

## What's already true about this project

- Expo SDK 54, `compileSdkVersion`/`targetSdkVersion` default to **36** (Android 15) — this already clears Google Play's minimum target API requirement for new app submissions (which moves up roughly once a year; re-check before your actual submission date since store policy, not Expo, sets that floor).
- `app.json` already declares `android.package: "app.ihyaa.mobile"` and an adaptive icon.
- No `eas.json` existed before this session — added at `frontend/eas.json` (see below).

## `frontend/eas.json` — what it configures

| Profile | Purpose | Output |
|---|---|---|
| `build.development` | Dev client for local testing on a device | APK, internal distribution |
| `build.preview` | QA / internal testers, sideloadable | APK, internal distribution, `preview` channel |
| `build.production` | Play Store submission | Android App Bundle (`.aab`), `production` channel, auto-incremented version |
| `submit.production` | Auto-submit to Play Console | Targets the **internal testing track** (up to 100 testers, no review wait) |

## Before you can actually build or submit

1. **Link an EAS project** — `eas init` from `frontend/`, using your own Expo account. This writes a real `extra.eas.projectId` into `app.json`; it can't be generated without your account, so it isn't in this commit.
2. **Play Console setup** (needs your Google Play Developer account, $25 one-time fee):
   - Create the app listing (package name must match `app.ihyaa.mobile` exactly, and can never change once published).
   - Generate a Google Play **service account** with release-manager permission (Play Console → Setup → API access), download its JSON key.
   - Save that key at `frontend/secrets/play-store-service-account.json` — this path is already gitignored (`frontend/.gitignore`), **never commit the real key**.
3. **Store listing assets** (not started): app icon (512x512), feature graphic (1024x500), at least 2 phone screenshots, short/full description, privacy policy URL (required — the app collects health-screening data, so this is not optional), content rating questionnaire, data-safety form (declare what `HealthProfile` fields collect and why).
4. **First build**: `eas build --platform android --profile preview` for a sideloadable QA build; `eas build --platform android --profile production --auto-submit` once ready for the internal testing track.

## Not covered here (deliberately)

- Actual Play Console submission — requires your developer account, which this session has no access to.
- iOS — explicitly sequenced *after* Android ships, per the Android-first decision this session.
- Push notification credentials (FCM) — needed before `expo-notifications` works in a production build; not yet configured.
