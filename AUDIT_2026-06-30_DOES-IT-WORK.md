# ALPHA QUANT — "DOES IT ACTUALLY WORK?" AUDIT RESULT — 2026-06-30
Run by Claude Code (5 parallel investigators for the code/test sections + direct broker-truth verification for §2/5/6/9). Evidence tiers cited. The headline §4 bug was re-verified by hand against the watched file.

## VERDICT
**SIM: sound and trading correctly today. LIVE: NO — blocked on §4 (risk enforcement FAIL) and §2 (4× universe incomplete).**
The audit's own gate ("don't declare it works unless §1,2,4,5,8 all PASS") is NOT met: §2 partial, §4 FAIL. So the honest answer is *"it works in SIM, it is not safe for live yet,"* with a concrete, short fix list.

## SCORECARD
| § | Area | Verdict | Evidence |
|---|---|---|---|
| 1 | Entry pipeline | **PASS** | 15+ filters mapped; all exception paths fail-OPEN; submitted=0 alert registered; 5-day scan record normal except the intentional 6/30 HTB day |
| 2 | Borrow / 4× gate | **PARTIAL** | HTB blocks BOTH sides (orb_runner:711, orb_multiscan:353), per-symbol verified vs blotter (BROKER_TRUTH) — PASS. **4×-marginable universe NOT implemented** (marginability.py shadow-only) — FAIL |
| 3 | Advisor→bot channel | **PASS** | All 9 rejection paths forced → default-to-ALLOW; unknown control types ignored; read-only (one-way valve holds) |
| 4 | Risk enforcement | **FAIL** | Dead daily-loss halt in live ORB path; before-live "hard gates" have no code consumer; no real-time intraday clamp |
| 5 | Exits & stop coverage | **PASS** | BROKER_TRUTH: 5 open / 5 stops / 0 naked = 100%; $500 cap binding to the dollar ($499–$501); EOD-flat pending close |
| 6 | Data / broker truth | **PASS** | Reads broker_orders_unified.csv (not phantom journal); order_action reads Legs[0].BuyOrSell (EC704); 15 RT, +$1,482.94 |
| 7 | Process survivability | **PASS** | All resident procs guardian-supervised + detached; orb_runner/multiscan fresh subprocess each cycle; 3 low-sev CREATE_NO_WINDOW lint |
| 8 | Observability | **PASS** | 5 channels; reliability drill 10/10 (no deaf detectors); every failure class mapped; 1 gap: new detector not drill-tested |
| 9 | Normal day end-to-end | **PASS** | Today: scan→re-arm(17)→stops(100%/$500)→15 RT closed +$1,482.94→5 open covered→EOD pending |

## RANKED BUGS (today's-failure-class first)
1. **[HIGH · LIVE-BLOCKER · WATCHED] Dead daily-loss halt in the live ORB path.** orb_runner.py:364 checks `should_halt`/`halt`; evaluate_daily_guard returns `should_trigger_shutdown` (daily_guard.py:101). Permanently False → the 9:35 daily stop never fires. Masked today by the $1e9 SIM sentinel; would silently fail to halt once a real DAILY_MAX_LOSS is restored for live. **Fix = 1 line:** `if guard.get("should_trigger_shutdown", False):`. WATCHED (orb_runner.py) → proposal + Rhett's go. Re-verified by hand.
2. **[HIGH · LIVE-BLOCKER · WATCHED] 4×-marginable universe not implemented.** HTB blocked, but leveraged-ETF/Special-Margin exclusion is shadow-only; universe can still surface non-4× names. Gated proposal (symbol_universe).
3. **[MED · LIVE-BLOCKER · WATCHED] No sector cap on the live ORB path.** MAX_SECTOR_POSITIONS=2 enforced only in legacy bot_loop/short_bot, NOT orb_runner/orb_multiscan → ORB has no correlation cap (the 6/24 energy-cluster risk). Phase-4 prereq.
4. **[MED · LIVE-BLOCKER · part non-watched] Before-live "hard gates" aren't hard.** The *_MUST_SET_BEFORE_LIVE flags + the 4 disabled protections have NO code consumer that blocks a live launch — only an advisory dashboard. Fix: a startup assertion (non-watched option: add to _preflight_diagnostic.py).
5. **[MED · LIVE-BLOCKER · build] No real-time intraday loss clamp.** Both daily guards are scan/cycle-time only. Documented hardening item; not present.
6. **[LOW] DD-kill base mismatch:** when re-enabled, the 5% kill measures vs real SIM equity (~$993k), not the $400k sizing base.
7. **[LOW · WATCHED doc] CLAUDE.md control vocabulary stale:** advisor handles EXIT_PROFILE + VETO_CANDIDATE (both conservative) not in the documented 12.
8. **[LOW · non-watched] New alive-but-not-trading detector lacks a reliability_drill case** (not smoke-tested). ~15 min.
9. **[LOW · non-watched] 3 subprocess calls missing CREATE_NO_WINDOW** (_preflight_diagnostic.py:57, orb_preflight_check.py:200/205/339, setup_autostart.py:33). Cosmetic.

**Crucial framing:** bugs 1–5 are all LIVE blockers but NONE break SIM today (sentinels mask #1; #2–5 are live-prep). SIM correctness is proven (100% stop coverage, $500 cap binding, broker-reconciled P&L). Live is gated on 1–5.

## FIX ROUTING
- **Non-watched, auto-fix-safe now:** #8 (drill case), #9 (CREATE_NO_WINDOW), #4-preflight-assertion option.
- **Watched → proposal + Rhett's go:** #1 (1-line, most urgent for live), #2, #3, #7 (doc).
- **Build items:** #5 (intraday clamp), #6 (base reconcile).
