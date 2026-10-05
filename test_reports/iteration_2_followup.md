# Iteration 2 follow-up — 5 Oct 2026

## Resolved findings
The testing agent's HIGH-priority blank-profile reload issue is fixed.
Cause: profile's useState(user?.prefs) mounted before auth finished and stayed undefined.
Changes: SessionGate before tabs/coach, profile synchronization after hydration, explicit
bootstrap loading/error/retry, modal-visible coach errors and busy feedback.

## Verification results
Main-agent Playwright check through current public preview:
- PASS desktop profile language reload EN.
- PASS desktop profile language reload ID.
- PASS no Arabic selector; desktop horizontal overflow [].
- PASS language persisted across sign-out and sign-in.
- PASS mobile profile reload, horizontal overflow [].
- PASS temporary test-only /auth/me 503 -> visible error -> real retry recovers profile.
- PASS real OpenAI Indonesian streamed reply about sleep.
- PASS delete after streamed reply: cancel leaves it intact, confirm returns 200 and closes modal.
- No page errors reported during this check.

Screenshot configs: desktop 1920x800, mobile 390x844.
Artifacts from screenshot tool: ihyaa-language-desktop-fixed.jpg,
ihyaa-language-mobile-fixed.jpg, console_20261005_054127.log.

Compile validation after source fixes: yarn tsc --noEmit PASS; Python compileall PASS;
Ruff F checks PASS. Initial testing agent backend suite: 15/15 PASS.

No application APIs are mocked. The temporary 503 above was test-only failure injection.
Native device runtime and comprehensive medical safety evaluation remain out of scope.