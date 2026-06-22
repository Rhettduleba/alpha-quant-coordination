# DAY-1 FORWARD-TEST READ — findings (Claude Code → Planning)
**Mon 2026-06-22 · read/verify only · re: EOD +$939.93 + the VPS OOM event.** Posture respected: no watched-file / live-path build.

## EXIT-RULE COMPLIANCE (Rhett's question: did the bot follow the exit rules on the losers?)
**YES — provably, from exit_decisions.jsonl (the bot's per-cycle decision log).** 4 losers (ULTA, SNDK, RIOT, BB), all long, all EOD-flatten:
- Every cycle logged `chandelier_hold (unconfirmed)`, **0 exit signals**, and the 1.4×ATR chandelier was **NEVER breached** (closest approach: ULTA +$10.12, SNDK +$164.71, RIOT +$1.99, BB +$0.76 above the chandelier). They never confirmed, so the candle-close exit never armed; the wide chandelier never triggered → correct to hold → EOD-flatten.
- The losses are the **designed cost of the wide chandelier (no tight stop)** — it does not cut slow shallow fades. (The 7 "left-on-table" were winners that exited correctly on candle-close, then continued — the same dial reversed. NOT evidence to loosen; HELD per Planning.)

## V1 — CLEAN-DAY VERDICT: certifier says CLEAN, but that is a **CERTIFIER BUG**; the day is NON-CLEAN
- `clean_day_certifier.certify_day('2026-06-22')` → **CLEAN, consecutive_clean=11** — WRONG.
- ROOT CAUSE: the `no_critical_incident` predicate reads **bot_alerts.jsonl** (0 FAIL today), but the real incident record is **incidents.jsonl (117 FAIL today)** — different files. The certifier never looks at incidents.jsonl, so it missed the whole event.
- The 117: 79× brain_universe_fresh (overnight, pre-Loop-136 fix), 26× scheduled_tasks_present (OOM), 10× broker_order_rejections (the known weekend back-fill), 1× rel_position_recon (transient SNDK), **1× rel_trading_is_thinking @14:11:40 "loop_count FROZEN at 7 >4min".**
- VERDICT (agreeing with Planning): **6/22 is NON-CLEAN** (real infra/monitoring incident). The kill-window clock should NOT have advanced. **The certifier wrongly advanced it → forward-test-integrity bug. FIX NEEDED:** point `no_critical_incident` at incidents.jsonl (or both). Non-watched 1-file fix; recommend doing it (makes the certifier stricter — cannot hurt the forward test). NOT built (read-only posture) — escalating.

## V4 — FREEZE-WINDOW EXIT AUDIT: no exit signal was missed
- The "2:11 freeze" = a brief loop-counter stall under OOM (rel_trading_is_thinking flagged loop_count stuck >4min). It was NOT a bot freeze: exit_decisions.jsonl shows exit_bot_v2 cycling **continuously** 14:05–14:25 — **max gap 76s** (one slow cycle), 54 rows/loser in that window.
- So exit monitoring was never interrupted; combined with the chandelier never being breached, **no candle-close/chandelier exit could have been missed on the 4 losers.** The exit-rule-compliance finding holds through the OOM window.

## V2 — SHADOW DELTAS (V0 gate PASSED 16/16=100%) — **directional only, NON-CLEAN day, NOT a kill input**
- **V9_CHANDELIER_1.4 (the LIVE deployed exit) reconciles to broker truth: +$1,033 / 75%** (≈ +$939.93 actual). Good.
- **`V0_ACTUAL` is MISLABELED** — it is the OLD 0.15×ATR tight-stop baseline (exits ~09:36), net **−$1,048 / 31%**, NOT the actual day. (Reporting-integrity nit: a reader sees "V0_ACTUAL −$1,048" and thinks the day lost money. Recommend renaming V0_ACTUAL → V0_TIGHT_STOP_BASELINE.)
- Today's delta: **new chandelier vs old tight-stop = +$2,082** — i.e. the old 0.15 stop would have stopped out the winners at 09:36 for a −$1,048/31% day; the chandelier held them for +$1,033/75%. Directly on `A-ORB-PHASE1-STOP-001`. **But: N=16, one chop day, NON-CLEAN — directional signal only, NOT a verdict, NOT a kill input.**

## V3 — OVER-DEPLOY: BENIGN (not a cap leak)
- Peak book $312,404 (104% of $300k target) at 10:56 = 5 positions + **12 working (unfilled) stop-entry orders** + MTM. Cumulative **admitted** entry-notional (deploy controller, re-arm) = **$197,318**; the controller governed each admit against the cap. The overshoot is book-drift from counting working orders + MTM, NOT over-admitting/over-filling. Actual deployed capital stayed under target.

## VPS STABILITY — adopting Planning's throttle recommendation + one flag
- AGREED: runtime resource isolation was the gap. The OOM came from accumulated build + agent + diagnostic processes co-located with run_bot on an 8GB box (commit limit ~8.9GB).
- **I will defer heavy build/diagnostic work to post-close during the forward test.**
- **FLAG (honest):** the autonomous alert-triage agent I set up this morning (`alphaquant-alert-triage`, a Claude session every 20 min during RTH on this VPS) is itself non-essential RTH agent activity that adds memory load — a likely contributor. RECOMMEND throttling it during the forward test (e.g., 60-min cadence, or pause it, or run the reasoning off-box). Rhett's call.
- Pagefile/RAM headroom is tight; growing the page file would add commit headroom (system change, Rhett's call).
