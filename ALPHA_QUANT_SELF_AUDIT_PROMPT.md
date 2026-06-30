# ALPHA QUANT — "DOES IT ACTUALLY WORK?" SELF-AUDIT PROMPT
*Written 2026-06-30 after the HTB zero-trades malfunction. Paste this to a fresh Claude Code session to make it prove — with broker truth and live code, not vibes — that Alpha Quant is bug-free and won't malfunction the way it did today.*

---

## YOUR ROLE
You've just been told what Alpha Quant is: a SIM-only ORB equity day-trading bot on TradeStation (account `SIM1623888M`, live root `C:\AlphaQuant`) plus a Claude advisor that writes ONE typed control file. You do NOT trust that it works. Your job is to **try to prove it's broken.** Assume there is a bug until a falsifiable check says otherwise. For every claim, cite the highest evidence available (BROKER_TRUTH > BROKER_EXPORT > LOCAL_RECONSTRUCTION > BOT_LOG_CONTEXT > ADVISORY_RESEARCH). If you can't verify something, mark it **UNKNOWN** — never assume it passes.

## THE FAILURE CLASS YOU ARE HUNTING (today's lesson)
Today the bot traded **zero** all morning because ONE pre-trade filter (Hard-To-Borrow) silently excluded every top-ranked candidate — including 7 LONGS that never needed a borrow. It was then **misdiagnosed** ("TradeStation data is broken") and a **fix over-corrected** (made the bot ignore borrow status entirely and short HTB names). So the bug class is:
1. **A single gate that can silently zero out trading** without anyone being alerted that "the bot is alive but doing nothing."
2. **A diagnosis stated as fact without checking broker truth first.**
3. **A fix that over-corrects** (swings from too-strict to too-loose) instead of being side/context-aware.
4. **A config/constant changed without sweeping every consumer** (validators, health checks, the other entry path).
5. **Something "deployed" that isn't actually wired into the live path** (shadow).
Every section below is designed to catch one of these. Do not just answer "yes"; run the check that would FALSIFY the claim.

---

## SECTION 1 — ENTRY PIPELINE: can any single gate silently kill all trades?
- Enumerate EVERY filter a candidate passes from universe → submitted order (price, volume, net-change, spread, in-play/relvol gate, HTB/halt, sector cap, deploy-controller cap, SAFE_MODE, stale-OR-cross, advisor controls). For EACH: what % of a normal day's candidates does it drop, and **could it drop 100% on a plausible day?**
- Pull today's `orb_candidate_log.jsonl` + `ORB_SCAN_DONE`. For the last 5 trading days, chart `submitted / candidates`. Any day at 0 — was that a legitimate market result or a gate malfunction? Prove which.
- For each gate that is borrow/short-specific, confirm it is **side-aware** (a LONG must never be dropped for a borrow reason). Show the code line.
- Is there an alert that fires when **scan ran but submitted=0 for N consecutive scans during RTH**? If not, that's a hole — today's failure would have been invisible. Specify the fix.

## SECTION 2 — THE 4×-MARGINABLE / BORROW GATE (today's bug area)
- Confirm HTB is now blocked **both sides** in BOTH entry paths (`orb_runner` AND `orb_multiscan`) — show both lines. Confirm `htb_filter.excluded_reason` reports the real flag (not the reverted "advisory" hack).
- Verify against broker truth: query `/marketdata/quotes` for 20 names and confirm `IsHardToBorrow` is per-symbol and matches the platform blotter (don't trust a past claim).
- Is the tradeable universe restricted to **4×-marginable** names? The TS API does NOT expose per-symbol margin — so how is non-4× exclusion sourced (leveraged/inverse ETF list? TS Special Margin list import? price/liquidity criteria)? Is that list present, dated, and actually consulted by the universe builder? If it's a TODO, say so.
- Try to short a known leveraged ETF / special-margin name in a dry-run order-confirm; confirm the universe would never have armed it.

## SECTION 3 — ADVISOR → BOT ONE-WAY CHANNEL
- Force each rejection path in `advisor_filter_engine.py` (missing file, bad JSON, `environment != SIM_ONLY`, `live_allowed != false`, expired) and confirm the bot **defaults to ALLOW** (a dead advisor must never lock the bot out) AND that no free-text/unschema'd control is ever honored.
- Confirm the only control types acted on are the documented vocabulary; anything else is silently ignored. Show the dispatch code.
- Confirm the advisor cannot write bot config, risk, or universe — only the one JSON file.

## SECTION 4 — RISK ENFORCEMENT: are the caps WIRED, not just constants?
- For each: `DAILY_MAX_LOSS`, 5% account-DD kill, `MAX_POSITION_PCT`, `MAX_OPEN_POSITIONS`, `MAX_TOTAL_EXPOSURE`, `MAX_SECTOR_POSITIONS`, `DOLLAR_STOP_CAP ($500)` — find the line that ENFORCES it and a log/test proving it actually triggered (or could). A constant with no consumer is a lie.
- Confirm which guards are currently DISABLED for SIM (`DAILY_MAX_LOSS`, the DD kill) and that there's a written gate requiring their restoration + a real-time intraday clamp BEFORE any live use. For the planned $100k live margin account, confirm sizing is off a $400k (4×) base with a real-time available-buying-power check, not SIM's inflated equity.

## SECTION 5 — EXITS & STOP COVERAGE
- For every fill today, confirm a protective resting stop exists at the broker (UROUT-paired) within N seconds — compute **% coverage** and the max naked window, for both the 9:35 cohort and the re-arm cohort. Today's known gap: re-arm fills historically under-covered.
- Confirm the `$500` per-trade dollar cap places `sl_dist = min(1.4×ATR, $500/qty)` and show a real example from today's orders.
- Confirm EOD flatten actually flattens (daytrade-flat requirement) — broker positions = 0 at close, proven by export.

## SECTION 6 — DATA / BROKER-TRUTH INTEGRITY
- Confirm reconciliation reads broker truth (`broker_orders_unified.csv` / live API), not the phantom journal. Confirm the order-action schema reads `Legs[0].BuyOrSell` (the EC704 gotcha), not top-level.
- Re-derive today's P&L and trade ledger from broker export and reconcile to the bot's numbers. Any mismatch is a bug.

## SECTION 7 — PROCESS SURVIVABILITY & DEPLOY DISCIPLINE
- List every long-lived process (run_bot, watchdog_supervisor, h5 stack, exit owner/TW, dashboards). For each: is it detached (survives a Claude Code restart), and is something watching it (supervisor_guardian) to respawn it? Any process parented to a shell session is a risk.
- Confirm new files using `subprocess` carry `CREATE_NO_WINDOW`. Confirm any edited long-lived process was actually RESTARTED (StartTime > file mtime) and `_preflight_diagnostic.py` re-run to green.
- Confirm `orb_runner`/`orb_multiscan` are fresh subprocesses each cycle (so file edits apply without a run_bot restart) — and that a change to a file imported by the persistent loop is NOT silently stale.

## SECTION 8 — OBSERVABILITY: would we even KNOW it malfunctioned?
- Inventory every alert channel (CSHV, `bot_alerts.jsonl`, reliability_checks, reliability_drill, code_inbox). Does the reliability DRILL still catch each injected fault (no deaf detectors)?
- Specifically: is there a detector for "alive but not trading," "naked position," "gate failing open," "loop frozen during RTH," "scan submitted=0 streak"? Map each failure in Section 1–7 to the alert that would catch it. Gaps = build items.

## SECTION 9 — PROVE A NORMAL DAY (end-to-end)
- Replay or live-observe one full session: universe build → 9:35 scan → fills → stops → re-arm → exits → EOD flat → reconciliation → debrief. Confirm each handoff produced the expected artifact and the numbers tie to broker truth end-to-end.
- State the ONE thing most likely to break tomorrow and the check that would catch it first.

---

## OUTPUT FORMAT
For each section: **PASS / FAIL / UNKNOWN**, the exact command/file/broker query that proves it, the evidence tier, and — for any FAIL/UNKNOWN — the smallest fix and whether it touches a WATCHED trading file (→ proposal + Rhett's go) or is non-watched (→ fix now + validate). End with a ranked list of the real bugs/holes found, today's-failure-class first. Do not declare the system "works" unless Sections 1, 2, 4, 5, and 8 are all PASS with evidence.
