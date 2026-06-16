# Alpha Quant Reliability — Claude Code's plan + review of ChatGPT's plan
**FOR: Planning Claude (adversarial critic role)** · FROM: Claude Code (VPS) · 2026-06-16

## Context
Recurring silent failures during market hours; Rhett is acting as the health monitor (today the bot
stopped trading ~10:00, he noticed ~11:50 — root cause was a deploy-book accounting bug that counted
this morning's CLOSED orders as $341k phantom exposure, so it refused every trade). Collaboration:
ChatGPT proposed a reliability architecture; **you (Planning Claude) critique it + find failure modes**;
Claude Code implements. This doc = Code's review of ChatGPT's plan + Code's implementation plan, for
your adversarial pass.

## ChatGPT's plan — summary (strong, adopt the framework)
A professional SRE plan: independent health monitor (30s in RTH), per-module heartbeats, watchdog/restart,
SAFE_MODE, alert_manager (Discord/email/SMS/Telegram), incident log, pre-market readiness check, EOD
reconciliation, a strict per-failure protocol (root cause → detection → alert → regression test → runbook
→ proof), required test gates, a 3-consecutive-clean-SIM-days rule before strategy tuning, and a
reliability freeze. Full file tree under monitoring/ runtime/ logs/ reports/ tests/ docs/.

## Claude Code's review — agree on the framework, but 8 additions from inside the codebase
ChatGPT can't see the code or our failure history. The 3 starred (★) are non-negotiable; without them the
plan would still have MISSED today or perpetuated the repeat-bug pattern.

### ★1 — Heartbeats would NOT have caught today. OUTCOME + internal-vs-broker reconciliation must be P0.
ChatGPT's plan is ~70% liveness (process alive, data fresh, heartbeat stale). Today every heartbeat was
fresh and the bot still silently refused every trade. Liveness-only stays GREEN through our worst failure.
The checks that catch it: (a) "candidates qualified + slots available + book < target, but 0 arms in N min";
(b) **"internal deploy-book total ≠ live broker exposure"** — the exact bug; ChatGPT has order/position
reconciliation but NOT internal-accounting-vs-broker-truth. Elevate from ChatGPT's "Check 6" to P0.

### ★2 — Tests must hit the REAL broker, not mocks. (The actual repeat-bug root cause.)
Twice this week a MOCK-passing test gave false confidence: the exit-fix passed its mock test then the real
broker rejected it (EC704); the deploy bug was never fed a realistic broker order list. RULE: order-path /
broker-truth code must be tested against a CAPTURED REAL broker response (or live), never only a mock.
"Mock passed" ≠ "works." This is why fixed bugs keep returning.

### ★3 — Watch the watcher + PROVE the alert delivers.
The monitor can die silently → square one. It must emit its own heartbeat, be supervised by the existing
supervisor_guardian, AND have a dead-man's switch (periodic "still alive" ping; absence = alarm). And:
notifier.py exists (Discord/email/Telegram) but I have NOT confirmed creds are configured or wired to these
conditions. STEP 0 = send a real test alert and confirm it reaches Rhett's phone. A non-delivering alert is
worse than none (false confidence).

### 4 — Cadence must respect TradeStation rate limits (ChatGPT's 30s would risk an API ban).
We were rate-limited this week; CLAUDE.md rule 4 warns over-refresh can disable the key. Tier it: LOCAL
checks (heartbeat, artifact freshness, trace anomalies — file reads) every 30–60s; BROKER-truth checks
(positions/orders/account) every 2–5 min, reusing the bot's already-fetched data instead of double-polling.

### 5 — Adapt the heartbeat model to our SUBPROCESS architecture.
orb_runner / orb_multiscan / exit are subprocesses spawned fresh each cycle by run_bot — they run and exit,
no persistent heartbeat. Check "did this step RUN this cycle + produce a fresh artifact," not "is the
module's heartbeat stale." Forcing per-daemon heartbeats here is wasted work.

### 6 — SAFE_MODE ≠ the money-halts we deliberately removed in SIM.
We intentionally turned OFF account loss/drawdown halts in SIM for a full data distribution. SAFE_MODE is
for TECHNICAL integrity (broker disconnect, position mismatch, stale data, unknown order state → block new
orders) — adopt that, keep it DISTINCT from money-risk halts that are intentionally off in SIM.

### 7 — The "no-trade reason" check is the single highest-value check; make it concrete.
Every scan/re-arm already writes a structured trace (candidates, passed-gate, armed, refused-with-reasons).
Missing piece = ALERT on the anomaly: "re-arm refused ALL candidates for a reason that shouldn't refuse all
(deploy_refused on a flat book)" → ALERT. Data exists; wire the alert.

### 8 — EXTEND what exists; don't rebuild.
Already live + verified: CSHV (5-min health checks), watchdog_supervisor + supervisor_guardian (respawn,
detached), alerts_bridge/bot_alerts.jsonl, notifier.py, preopen_readiness.py, regression_suite.py (16),
chain_audit.py, _preflight_diagnostic.py (50). Build the NEW live-outcome monitor as a separate
guardian-supervised process, but route findings through EXISTING CSHV_FINDINGS + bot_alerts + notifier.

## Claude Code's implementation plan (P0 MVP — would have caught today at ~10:40, not 11:50)
1. Confirm notifier actually DELIVERS to Rhett (test push). Do FIRST — nothing matters if alerts don't land.
2. Live-outcome monitor (separate process, guardian-supervised, tiered cadence): no-trades-when-expected,
   re-arm-refused-all, **deploy-book-vs-broker-truth**, order/position reconciliation, data freshness.
3. Every FAIL → notifier push (what / when / module / trading-stopped? / orders-active? / next-step) + incident log.
4. SAFE_MODE (technical-integrity only) — block new orders on untrustworthy broker/data/position state.
5. Real-broker capture for the test gate; backfill regression tests for this week's bugs (EC704, deploy-book).
6. EOD reconciliation one-pager.
Then ChatGPT's fuller build sequences behind this. Adopt the reliability freeze + 3-clean-days rule.

## FOR PLANNING CLAUDE — attack this (your adversarial role)
1. Where can the live-outcome monitor itself silently die or FALSE-GREEN? (It must be un-takedownable by
   the thing it watches; is guardian + dead-man's-switch enough, or is there a single point of failure?)
2. What outcome conditions am I still missing? (I have: no-trades, refused-all, book-vs-truth, recon,
   freshness. What else silently fails GREEN?)
3. Thresholds: what's "too long with no trades" given the gate is intentionally selective (some quiet
   stretches are correct)? How do we avoid alert fatigue while not missing a real stall?
4. Where do mock-test gaps still hide even with a "real broker" rule? (Capture staleness, SIM-vs-live broker
   behavior differences, etc.)
5. SAFE_MODE: which exact conditions should auto-pause new entries vs alert-only? Risk of SAFE_MODE itself
   becoming a silent trading-halt we don't notice?
6. Is the 5-min CSHV + a 30–60s local monitor the right split, or do we need the monitor to own everything?
