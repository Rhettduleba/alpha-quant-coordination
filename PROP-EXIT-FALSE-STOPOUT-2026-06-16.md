# PROP-EXIT-FALSE-STOPOUT-2026-06-16 — ORB exit defects (false stop-outs + left-on-table)

**Status:** PROPOSED (advisory-only — NOT active). Requires backtest + human approval in
`config/manual_approvals.yaml` before any flag flips. Strategy change per CLAUDE.md rule 3.
**Source:** Rhett EOD comments 2026-06-16 + Claude Code broker-truth analysis (this file).
**Related:** spawned task `task_1a4d9e35` (exit confirm-swap rebuild) — fold this in.

## Evidence (2026-06-16, broker truth + 1-min bars)

Two distinct exit mechanisms each cost real money today:

### Issue 1 — PHASE-1 0.15×ATR stop is too tight → FALSE STOP-OUTS (before the trade confirms)
The pre-confirmation stop (0.15×ATR) gets hit by normal post-breakout noise before the move can
develop. The thesis then plays out — without us.

| Trade | Entry | Stopped (PHASE1_STOP) | Realized | Then went to | LEFT ON TABLE |
|---|---|---|---|---|---|
| FISV long | 49.05 | 48.66 (**1 minute** after entry) | −$159 | 50.12 by 3:23 PM | **+$594** |
| COHR short | 389.00 | 395.62 (wiggle up, never confirmed) | −$338 | 382.78 by EOD | **+$655** |
| TTWO #2 long | 226.93 | 225.78 (unconfirmed) | −$115 | — | — |

FISV+COHR alone: **−$497 realized that should have been ~+$1,249** (Rhett estimated ~$1,083 — same
order of magnitude; confirmed worse). This is the A1 "12/50 cut short" finding, live.

### Issue 2 — CANDLE_CLOSE_REVERSAL exits on the FIRST opposite candle → LEFT ON TABLE (trend resumes)
Confirmed trades (phase 2) exit on a single opposite-color candle close. Profitable, but the move
keeps going right after.

| Trade | Entry | Exit (candle-close) | Realized | Then went to | LEFT ON TABLE |
|---|---|---|---|---|---|
| MU short | 1045.35 | 1035.91 @ 2:37 PM | +$179 | 1020.00 by EOD | +$302 |
| TTWO #1 long | 224.25 | 226.57 @ 2:32 PM | +$206 | 230.50 by EOD | +$350 |
| CBOE #1 short | 273.76 | 271.80 @ 1:28 PM | +$143 | 264.51 by EOD | +$532 |

(Answers Rhett: MU exited on a single up-candle close in phase 2 while the downtrend resumed; TTWO
left-on-table was UNDER-stated by the in-hold MFE — post-exit it left $350; CBOE left $532, same
candle-close-too-eager pattern. Not a code "bug" — the rule is working as written; the rule is too eager.)

## Root cause
- **Issue 1:** a fixed 0.15×ATR stop applied BEFORE confirmation gives a breakout no room to breathe.
  A normal pullback to/through the breakout level stops the trade at a loss; if it never "confirms"
  (moves 0.15×ATR favorable first) it rides this tight stop the whole time.
- **Issue 2:** the phase-2 exit triggers on ONE opposite candle close. For a trending name a single
  counter-candle is noise, not a reversal.

## Fix candidates (MUST backtest on the ORB research data before enabling — do NOT hand-tune live)
**Issue 1 (false stop-outs):**
1. Widen the pre-confirmation stop (e.g. 0.30–0.50×ATR) — give the breakout room to confirm.
2. Structure stop: place it below the breakout bar's low (long) / above its high (short), not a flat ATR fraction.
3. Time-grace: don't arm the tight stop for the first N minutes (let the opening churn settle).
4. (Interacts with the confirm-swap rebuild — that widens AFTER confirm; this is the BEFORE-confirm gap.)

**Issue 2 (left-on-table):**
1. Require TWO consecutive opposite candle closes (or a close beyond a level), not one.
2. Replace single-candle exit with an ATR trailing stop in phase 2 (ride the trend, exit on a real pullback).
3. Tiered: take partial at +Nx, trail the rest.

## Decision gate
1. Backtest each candidate on the ORB strategy-research dataset (strategy-research/), measure net
   expectancy + win-rate + avg-left-on-table vs the current 0.15×ATR / single-candle baseline.
2. If a candidate improves net expectancy without inflating drawdown, write it up + record approval in
   `config/manual_approvals.yaml`, ship behind an OFF flag, shadow-A/B, then flip.
3. Until then: NO live exit change. Today's exits ran as designed; the design needs evidence-based tuning.

## What is NOT being done (and why)
- No mid-session / un-backtested live exit edit (rule 3 + the EC704 confirm-swap lesson: an untested
  exit change broke live this week). The exit path is money-critical and gets a backtest, not a hunch.
