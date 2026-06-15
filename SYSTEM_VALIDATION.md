# Alpha Quant — System Validation Matrix

**Purpose:** stop the one-bug-per-day whack-a-mole. Every component below has (a) a plain-English
job, (b) a concrete "working" criterion, (c) a test that can be run/automated, (d) a current status,
and (e) whether it's surfaced on the dashboard. The goal: **see every failure at once**, with a live
dashboard panel, instead of discovering them one trading day at a time.

Status key: ✅ verified working · ❌ broken/confirmed-failing · ⚠️ at-risk/partial · ❔ untested.
Owner of the build: Claude Code. Last updated 2026-06-15 (post-mortem of today's stacked failures).

## Today's failure chain (why ~0 useful trades 2026-06-15)
1. 9:35 scan crash-looped (deploy_controller KeyError) → completed late on a degraded OR fetch
   (~34/530) → armed sleepy alphabetical large-caps → `scan_completed` LOCKED the book.
2. Fill-time gate OFF → those stale 9:35 stop-entries sat all day and filled ~13:45 (4h late).
3. Re-arm (movers) slot-starved: `slots = max(0, MAX_OPEN_POSITIONS(4) − 19 working) = 0` → 0 movers.
Three independent breaks, each individually "fixed-or-flagged," none caught before the open. That is
the case for this matrix.

## Validation matrix

| # | Component | Job | "Working" = | Test | Status | Dashboard |
|---|-----------|-----|-------------|------|--------|-----------|
| 1 | run_bot loop | Subprocess each cycle step, heartbeat | heartbeat <60s; each step runs | preflight + heartbeat check | ✅ | ✅ bot-health |
| 2 | Universe (build_universe) | 530 S&P names incl movers | ~530; contains movers | assert count + sample movers present | ✅ | ❌ |
| 3 | Warmup (orb_data_collector) | Cache OR-vol hist, ATR, prior close, $-vol | ≥X% names have all 4 cached | count cached / universe | ⚠️ | ⚠️ timeline |
| 4 | OR fetch (fetch_today_or) | Per-symbol opening range | coverage ≥50% of universe | live coverage count (clean, not hammered) | ⚠️ OR_MIN_BARS=3 fix, unmeasured clean | ❌ |
| 5 | Coverage gate | Don't arm a degraded scan | retry if coverage<50% until 9:50 | unit test: 8%→retry, 74%→arm | ✅ logic | ❌ |
| 6 | 9:35 ORB scan | Rank OR breakouts, arm top-20 | completes once, arms from full universe | scan_completed + armed count + ORB_SCAN_DONE | ❌ today (degraded+locked) | ✅ timeline (per-scan) |
| 7 | In-play gate | Filter to movers (day-RelVol/move/$-vol) | selected = movers, not sleepy | verify_gate_drove_entries.py (A–D) | ❔ enforced first TOMORROW | ✅ inplay-gate page |
| 8 | Sizing | ~$20k/name off $100k×4 base | per-position ≤ caps, risk=1% | recompute armed notional vs caps | ✅ | ⚠️ truth |
| 9 | Deploy controller | Cap per-side/per-position by $ | book_from tolerant; admit caps | test_deploy_controller.py (non-empty book) | ✅ crash-fixed; ❌ never proven counting real exposure | ❌ |
| 10 | Order submission | Place accepted entries | broker ACCEPTS the order | broker status != REJECTED | ⚠️ stop-limit OK, stop-market rejected | ✅ timeline (per-order status) |
| 11 | Reject-fix (9:35) | Skip already-crossed levels | no "invalid stop" rejects | count ORB_STALE_LEVEL skips | ✅ in orb_runner; ❌ NOT in multiscan | ❌ |
| 12 | Fill monitor + SL | Place stop-loss on each fill | every fill gets an SL | SL count == fill count | ⚠️ | ❌ |
| 13 | Exit (candle_close) | 0.15ATR→confirm→opposite-candle→1.0ATR | exits fire per spec | a1_exit_proof.py replay | ✅ (with resting-stop nuance) | ✅ daily-review |
| 14 | Fill-time gate | Kill stale DAY entries (SMCI-class) | stale unfilled entry cancelled | inject_stale_entry.py | ❌ OFF (=today's 4h-late fills) | ❌ |
| 15 | Multi-scan re-arm | Add movers at 10:35–14:35 | arms movers within caps | per-window armed + broker status | ❌ slot-starved (MAX_OPEN_POSITIONS=4) | ✅ timeline (per-scan) |
| 16 | EOD flatten | Cancel + flatten by 15:55 | flat at close | eod_flatten_done + 0 positions 16:00 | ❔ (runs 3:55) | ✅ timeline |
| 17 | Risk floors | daily_guard + 5% DD kill | halts when tripped | simulate loss → halt | ✅ 5% DD active; daily-$ clamp ◆ INTENTIONALLY OFF (SIM data-gathering, Loop 74) — must-set-before-live gate, NOT broken | ✅ (◆ SIM-intentional + 5% DD rows) |
| 18 | Advisor filter | Obey typed control file | reject→ALLOW; types honored | feed control file → behavior | ✅ | ⚠️ |
| 19 | Earnings veto | Block earnings-blackout names | stale-cal warns; blocks correctly | staleness_warning + sample | ⚠️ calendar ~12d stale | ❌ |
| 20 | Mover scanner | Bulk in-play movers (scans.jsonl) | RTH writes; pre-mkt gated | mtime + qualified count | ⚠️ RTH-only (no pre-mkt) | ✅ pre-market page |
| 21 | Research Brain | Publish criteria universe | ~150 names, fresh daily | research_brain_status today | ✅ | ✅ timeline |
| 22 | Advisor control loop | Write control file 8:00/12:30/4:30 | fresh control file daily | advisor_control_latest mtime | ✅ | ✅ timeline |
| 23 | Broker truth log | Log every terminal order | unified==independent (p0) | p0_verify_harness --live | ✅ (5/5 days 6/08–12) | ⚠️ truth |
| 24 | CSHV | Health every 5 min | 46+/48 pass | CSHV_FINDINGS.md | ✅ | ⚠️ |
| 25 | Alerts monitor | Triage manager alerts hourly | actionable surfaced | check_alerts.py | ✅ | ✅ alerts page |
| 26 | Dashboard | Show live state, no stale | each page reads live / refreshes | per-page freshness | ⚠️ (truth+timeline auto; others manual) | ✅ |

## The build (what Claude Code must do)
1. **A `/system-validation` dashboard page** that RUNS each testable check above and shows ✅/❌/⚠️ live —
   so all failures are visible at once. (Reuse: preflight, test_deploy_controller, verify_gate,
   coverage check, p0 harness, fill-time inject.)
2. **A `system_validation.py`** that returns the matrix as data (each row = {component, status, detail}),
   driven by real artifacts/tests, feeding the page.
3. Wire it into CSHV so a regression flips a row to ❌ and lands in CSHV_FINDINGS.md.

## Open fixes feeding red rows (tracked, NOT silently "fixed")
- #14 Fill-time gate OFF → 4h-late stale fills. Turn ON (ORB_ENTRY_MAX_AGE_MIN=20) — pre-open only.
- #15 Re-arm slot cap MAX_OPEN_POSITIONS=4 → **APPROVED + STAGED** (Loop 72): raise to 16 (=$400k/$25k)
  via time-guarded apply_slot_cap.py, scheduled 16:10 ET 2026-06-15. Flips the row OK after apply.
- #11 multiscan missing reject-fix → movers rejected on crossed levels. (still open)
- #9 deploy_controller → **DONE** (Loop 72-73): book_from normalizes raw broker dicts; prove_deploy_governs.py
  proves all 3 caps bind on a non-empty book + LIVE on the real $580k book. Row = GOVERNS.
- #4 OR-fetch clean coverage unmeasured (don't hammer API; read from the real scan).
- #19 earnings_calendar.csv ~12d stale → refresh.
- HTB systematic exclusion (BDX got armed) — after-close, approval-gated.

## Intentional-by-design (NOT failures — do not "fix") + REQUIRED-BEFORE-LIVE gates
Rhett's final SIM decision (Planning Loop 76): **NO account-level halts in SIM** — collect complete
sessions, good AND bad. The ONLY things that close a trade are the per-trade STRATEGY exits
(0.15ATR / candle-close / 1.0ATR), which are UNTOUCHED. All three items below are ◆ SIM-intentional on
the board and carry a REQUIRED-BEFORE-LIVE flag; the `/system-validation` blocking banner lists any that
are unmet and turns into a hard ⛔ if `live_allowed` is ever true while they're off.
- **Daily-loss clamp OFF** (DAILY_MAX_LOSS=1e9, Loop 74). Before live: set a real $ value + harden to a
  real-time intraday clamp. Flag: DAILY_MAX_LOSS_MUST_SET_BEFORE_LIVE.
- **5% account-DD kill OFF** (ACCOUNT_DD_KILL_ENABLED→False, Loop 76) — applied in tonight's after-close
  batch (apply_slot_cap.py, time-guarded). risk_kill_switch.evaluate_account returns OK when disabled;
  HWM keeps tracking so it's accurate when re-enabled. Before live: re-enable + verify it halts. Flag:
  ACCOUNT_DD_KILL_MUST_SET_BEFORE_LIVE.
- **Malfunction breaker NOT built** (Loop 76 — explicitly skipped). MALFUNCTION_BREAKER_BUILT=False.
  Before live: build + wire it. Flag: MALFUNCTION_BREAKER_MUST_BUILD_BEFORE_LIVE.
