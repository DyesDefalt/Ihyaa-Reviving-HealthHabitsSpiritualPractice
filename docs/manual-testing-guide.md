# Manual testing guide: Android, iOS, Windows PC

Sourced from Expo's current SDK 54 docs (this project's SDK) via Context7, 2026-08-14.

You're always testing **two** things at once: the Expo app in `frontend/`, and a
backend (`backend/` + MongoDB) it talks to over HTTP. Nothing below will work
until step 1 is done, regardless of platform.

Not a mobile-development shop? None of the earlier phases in this project used
Supabase — the `VITE_SUPABASE_URL`/`VITE_SUPABASE_ANON_KEY` in the repo root
`.env` and the `@supabase/supabase-js` entry in the root `package-lock.json`
are leftovers from an earlier scaffold with no `package.json` behind them
anymore; nothing in `frontend/` or `backend/` imports Supabase. Auth here is
bcrypt + JWT against MongoDB (`backend/auth.py`, `backend/db.py`). Worth
deleting that root `.env`/lockfile in a cleanup pass, but out of scope here.

## 1. Get a backend you can reach

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env` (already gitignored — never commit real values here):

```
MONGO_URL=mongodb://localhost:27017      # or an Atlas free-tier connection string
DB_NAME=ihyaa_dev
JWT_SECRET=<any long random string>       # e.g. `python -c "import secrets;print(secrets.token_hex(32))"`
CORS_ORIGINS=http://localhost:8081,http://localhost:19006
ADMIN_EMAIL=you@example.com                # optional: seeds a full-access account on boot
ADMIN_PASSWORD=<pick one, don't reuse it>
DEMO_EMAIL=demo@example.com                # optional: seeds a free-tier account on boot
DEMO_PASSWORD=<pick one>
```

No local Mongo? `docker run -d -p 27017:27017 mongo:7` is the fastest option,
or use a free MongoDB Atlas cluster (allowlist `0.0.0.0/0` for a dev cluster
only, never for anything real).

Start it bound to all interfaces, not just localhost, so a phone/emulator on
the same network can reach it:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

Find the machine's LAN IP — you'll need it for every method below except the
Android emulator and iOS Simulator (which have their own aliases):

- **Windows**: `ipconfig` → IPv4 Address
- **macOS/Linux**: `ifconfig` (or `ip addr`) → look for the `en0`/`wlan0` entry

Then in `frontend/.env`:

```
EXPO_PUBLIC_BACKEND_URL=http://<your-LAN-IP>:8000
```

```bash
cd frontend
npm install
```

## 2. Pick a method

| Method | Platforms it tests | Needs a Mac? | Needs Apple Developer account? | Cost | Best for |
|---|---|---|---|---|---|
| A. Expo Go | Android + iOS, from any dev OS | No | No | Free | Day-to-day dev loop |
| B. Android Emulator | Android, from any dev OS | No | N/A | Free | CI-like Android parity |
| C. iOS Simulator | iOS | **Yes** | No | Free | iOS parity, if you have a Mac |
| D. EAS Build (dev/preview) | Physical device, real native build | No (builds in Expo's cloud) | iOS device installs: yes | Apple: $99/yr | Custom native modules, pre-release QA |

If you're on Windows and don't own a Mac, **Method A on a physical iPhone is
the realistic iOS path** — the Simulator itself is a macOS-only binary, so no
cloud build changes that.

### A. Expo Go — fastest, works from Windows or macOS

1. Install **Expo Go** from the App Store (iOS) or Play Store (Android) on the
   test device.
2. `npx expo start` in `frontend/`.
3. Scan the QR code (Android: Expo Go's built-in scanner; iOS: the Camera app,
   which hands off to Expo Go).
4. Phone and dev machine must be on the **same Wi-Fi**. If it can't connect
   (corporate/guest Wi-Fi, VPN, client isolation), run
   `npx expo start --tunnel` instead — slower, but it proxies over HTTPS
   through Expo's servers and works across networks.

### B. Android Emulator (Windows, macOS, or Linux)

1. Install **Android Studio** → SDK Manager → install a recent SDK Platform
   (API 34+) → Device Manager → create a virtual device (e.g. Pixel 8, API 34).
2. Start the emulator, then from `frontend/`: `npx expo start` and press `a`
   (or `npx expo run:android` for a full native build instead of Expo Go).
3. Networking shortcut: the emulator's special alias `10.0.2.2` always maps to
   your host machine's `localhost`. If the backend runs on the same machine as
   the emulator, you can use `EXPO_PUBLIC_BACKEND_URL=http://10.0.2.2:8000`
   instead of hunting for your LAN IP.

### C. iOS Simulator (macOS only)

Xcode's iOS Simulator does not run on Windows or Linux — this is an Apple OS
constraint, not an Expo one. If you have a Mac:

1. Install Xcode from the App Store, then run it once to accept the license
   and let it install additional components.
2. From `frontend/`: `npx expo start` and press `i` (or `npx expo run:ios`).
3. The Simulator shares your Mac's network stack directly, so
   `EXPO_PUBLIC_BACKEND_URL=http://localhost:8000` works as-is if the backend
   runs on the same Mac — no LAN IP needed.

### D. EAS Build — real native builds, no Mac required to *build*

`frontend/eas.json` already has the profiles for this:

- `development-simulator` — produces an iOS Simulator build (`ios.simulator: true`)
  entirely in Expo's cloud, so you can build it from Windows. You still need a
  **Mac** to actually open and run it, since the Simulator itself is macOS-only.
- `development` / `preview` — installable on a **physical device**. Android
  needs nothing beyond an internal APK. iOS device installs require enrolling
  in the Apple Developer Program ($99/yr); EAS manages the signing
  certificates for you interactively even from a Windows terminal — you don't
  need Xcode.

```bash
cd frontend
eas init                                          # first time only, your own Expo account
eas build --platform android --profile preview    # sideloadable APK
eas build --platform ios --profile preview         # physical iPhone, needs Apple Developer account
eas build --platform ios --profile development-simulator   # .app for macOS Simulator only
```

Install the Android APK by downloading the build URL EAS prints and opening
it on the device. Install the iOS build via **TestFlight** (upload with
`eas submit`) or ad-hoc distribution.

## Minimum OS versions (Expo SDK 54, this project's SDK)

- **iOS**: 15.1+ (`iosDeploymentTarget` in the SDK 54 version table)
- **Android**: 7.0+ / API 24+ (`minSdkVersion`), `compileSdkVersion`/`targetSdkVersion` 36

## Test accounts

The backend seeds accounts from env vars on every boot (`backend/server.py`,
`startup()`):

- `ADMIN_EMAIL` / `ADMIN_PASSWORD` → `role=admin`, `is_pro=True` — full access,
  including the pro-gated 100-day and 1-year challenge tracks.
- `DEMO_EMAIL` / `DEMO_PASSWORD` → `role=user`, `is_pro=False` — the default
  free tier.

Set these in your own `backend/.env` (gitignored) or your host's secrets
manager — never in a committed file. Any account can also just be created
through the app's normal sign-up screen; new registrations default to the
free tier already, no seeding needed.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| "Network request failed" in the app | Wrong `EXPO_PUBLIC_BACKEND_URL` (`localhost` doesn't resolve on a phone/Android emulator — see method-specific IPs above), phone not on the same Wi-Fi, backend bound to `127.0.0.1` instead of `0.0.0.0`, or a firewall blocking port 8000. |
| Backend crashes on startup with a `KeyError` | `MONGO_URL`, `DB_NAME`, or `JWT_SECRET` missing from `backend/.env` — these have no defaults. |
| Mongo connection refused | Mongo isn't running locally, or an Atlas cluster's IP allowlist doesn't include your machine. |
| Stale bundle / weird errors after pulling changes | `npx expo start -c` to clear the Metro cache. |
| Works on Expo Go, fails in a `production` EAS build | Expo Go and dev/preview internal builds are lenient about local HTTP; a `production` build is stricter about cleartext (Android) and App Transport Security (iOS). Point production-profile testing at an HTTPS backend. |
