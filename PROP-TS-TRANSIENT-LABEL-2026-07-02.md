# PROP-TS-TRANSIENT-LABEL-2026-07-02 — don't label a transient 504 as TS_AUTH_FAIL

**Status:** DRAFT — awaiting Rhett's go (WATCHED file: orb_runner.py). Surfaced by the 15-min monitor on 2026-07-02 14:51:54.

## The problem (verified benign, but the alarm lies)
At 14:51:54 the monitor saw a **FAIL: `TS_AUTH_FAIL — account fetch: 504 Server Error: Gateway Timeout`**. Verified: it was a **single transient TradeStation server-side 504**; the bot recovered immediately (heartbeat cycling loop 3345, still traded — 21 arms/19 round-trips today). No auth problem, no bug on our end.

BUT `TS_AUTH_FAIL` is DEFINED (alerts_bridge.py:29) as **"TS API returned 401/403"** — a real auth failure. `orb_runner.py:254-256` emits it inside a **broad `except Exception`**, so ANY account-fetch error (504/timeout/connection) is mislabeled a FAIL-severity auth failure. Effect: every TS server hiccup pages Rhett as if his **API key is failing** — a false alarm that erodes trust in the alerts (and could mask a real 401/403 in the noise).

## The concrete fix (orb_runner.py:254-256 — WATCHED)
Classify the exception instead of blanket-labeling:
- **401 / 403** (real auth) → keep `log_alert("TS_AUTH_FAIL", "FAIL", ...)`.
- **5xx / 504 / timeout / connection error** (transient) → `log_alert("TS_API_TRANSIENT", "WARN", ...)` — informative, not a FAIL, not "auth".
Detect via the exception's HTTP status (`getattr(e, "response", None).status_code`) or a status substring; default unknown → WARN (fail-soft, don't cry auth).

## Why it's safe
Pure alerting/label change — touches NO trading behavior (entry/exit/sizing/risk). It only changes the severity + name of a log event on an account-fetch error. Add a regression test: a synthesized 504 → WARN/TS_API_TRANSIENT; a 401 → FAIL/TS_AUTH_FAIL.

## Deploy
orb_runner is a fresh subprocess each cycle → loads next cycle, no run_bot restart. But it's WATCHED → needs Rhett's go + a regression lock; deploy is low-risk (alerting only). Also sweep the h5_runner.py:318 `H5_TS_AUTH_FAIL` for the same broad-except pattern.
