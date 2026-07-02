# EOD PER-TRADE TUNE ANALYSIS — added to the EOD process (Rhett, 2026-07-02)

**When:** every trading day at EOD, as part of the debrief. **Run first:** `python C:\AlphaQuant\strategy-research\eod_trade_tune_analysis.py <YYYY-MM-DD>` — it assembles broker-truth per-trade data (net, hold, exit code, MFE/MAE, capture ratio, money-left, entry context). Then reason over EVERY trade with the four questions below and append findings to the running **tune log** (`outputs/reports/tune_log.md`).

## THE ONE HARD RULE (Rhett)
> **An ENTRY tune can NEVER be applied on the strength of a loser alone.** Any entry-rule change proposed to eliminate a loser MUST be backtested against the clean cohort's WINNERS (`clean_cohort.py`, 217 kept trades incl. every real winner) to prove it would NOT have killed a positive trade. If it cuts a winner, it's rejected. Exit tunes go through the exit backtester. **This script surfaces candidates; it never tunes.**

## FOR EVERY TRADE — the four questions

**Q1 — SIGNAL CORRECTNESS (did the bot follow the current strategy?)**
- Entry: did we enter on a real strategy signal? (was it a selected in-play candidate for that window — `entry_ctx.inplay_pass`, RelVol/move/window match). 
- Exit: did we exit on the deployed logic? (`exit_code`: chandelier / candle-close / $500 cap / 30-min time-stop / EOD-flatten).
- **A mismatch is a BUG, not a tune → surface it and FIX it (regression-lock).** Never tune around a bug.

**Q2 — POSITIVE trades: did we leave money on the table?**
- `capture` = realized / MFE; `left_on_table$` = MFE − net. Low capture / large left = we exited early or entered late.
- Ask: could **earlier entry / faster execution** have caught more? could a **smarter exit** have held the runner? (exit backtester tests the exit side on the real price path — no winner-cutting risk since the entry is fixed.)
- Note the $ and the mechanism; accumulate to see if it's systematic (e.g. we always give back the last X%).

**Q3 — NEGATIVE trades (THE BIG ONE): why did we enter, and could a tune have prevented it?**
- Read MFE: **MFE ≤ 0 → the trade NEVER worked = a bad ENTRY** (e.g. MU 6/25, MFE −$43, −$1,670). **MFE > 0 then reversed → held too long = an EXIT problem** (the all-day bleeders).
- For bad ENTRIES: interrogate `entry_ctx` (RelVol, move%, rel-vs-SPY, mcap, extension, time). Is this **NOISE** (a valid setup the market moved against — unavoidable) or a **TUNABLE PATTERN** (a feature that repeats across losers)?
- If tunable: state the exact candidate entry filter that would have stopped THIS trade → **tag it "CANDIDATE ENTRY TUNE — backtest vs clean-cohort winners (must-not-cut) before proposing."** A candidate graduates to a proposal ONLY when it (a) repeats across multiple losers AND (b) survives the winner-backtest.

**Q4 — EXIT: did we exit properly, and can it be better?**
- Was the exit the right deployed one? Given the real price path, would an alternative exit have done better on THIS trade without cutting winners? (exit backtester on the clean cohort).
- We've spent a lot here — stay sharp: log any incremental idea even if small.

## OUTPUT — the running tune log (`outputs/reports/tune_log.md`)
Each EOD append: per-trade one-liners for anything notable + a CANDIDATES section:
- **BUGS** (signal mismatch) → fix now.
- **CANDIDATE ENTRY TUNES** → each tagged "needs winner-backtest"; list the losers it targets + the feature.
- **CANDIDATE EXIT TUNES** → run the exit backtester.
- **MONEY-LEFT patterns** → systematic capture loss on winners.
Over days, a candidate that repeats + survives its gate becomes a `PROP-` artifact for Rhett. Nothing is applied inline.
