# ALPHA QUANT — DAILY OWNER ROUTINE (Claude Code owns this)
*Rhett handed ownership 2026-07-01. Goal: MAXIMIZE daily intraday-equity profit with a system we can trust. Two standing routines run every trading day; both are wired to fire automatically (triggers) AND are documented here so any session can run them by hand.*

---

## ROUTINE 1 — 8:00 AM ET: SYSTEM CHECK / BUG-FREE SCAN (before the open)
Purpose: prove the system is healthy and bug-free before it trades.
1. **Run the automated gate:** `python C:\AlphaQuant\tradestation-bot\audit_does_it_work.py`
   - Aggregates regression suite (REG-01..28), reliability drill, dashboard validate, preflight, ORB gates → ONE PASS/FAIL.
   - If **FAIL**: open the failing script, diagnose. Non-watched → fix now + re-run to green. Watched trading file → propose + escalate to Rhett; do NOT ship silently.
2. **Confirm the bot is up + loaded:** run_bot alive (heartbeat < 60s), StartTime > any edited-file mtime (rule #13). If a watched file was edited overnight, restart run_bot (watchdog respawn) and re-run the gate.
3. **Read** `CSHV_FINDINGS.md` + `bot_alerts.jsonl` (24h) + the overnight `code_inbox.jsonl` — triage every WARN/FAIL per the warning-triage protocol (verify vs live truth → classify false/real → fix-safe or escalate → LOG). Never ship a red gate into the open.
4. **Verify the day's config posture:** ORB_935_ENTRIES_ENABLED=False (9:35 gated), DOLLAR_STOP_CAP $500 ENABLED, advisor control valid/SIM_ONLY, live blockers still SHADOW.
5. **Report + log:** one line to SESSION_LOG (`8AM check <date>: audit PASS/FAIL, bot loaded, N warns triaged`) + push. Tell Rhett only if something needs him.

## ROUTINE 2 — AFTER EOD POSTS (~5:00 PM ET, after the 4:50 debrief): FULL REVIEW
Purpose: did the system function correctly, and what did we learn?
1. **Run the three checks:**
   - `python C:\AlphaQuant\tradestation-bot\audit_does_it_work.py`  (still green?)
   - `python C:\AlphaQuant\tradestation-bot\validate_dashboard.py`  (dashboard ties to broker truth, caches fresh — refresh planning_roadmap.json to today)
   - `python C:\AlphaQuant\tradestation-bot\tw_health_check.py`  (did TW run the full RTH window, fire every exit, no disconnects?)
2. **Read** today's `outputs/reports/eod_debrief_<date>.md` end to end.
3. **DID THE BOT FUNCTION CORRECTLY?** broker FLAT at close + recon MATCH; 0 unexpected incidents; day net = broker truth.
4. **DID IT ENTER CORRECTLY?** 9:35 path = 0 (gated); re-arm entries only; in-play list matched; check every reject ('Invalid Stop Price' etc.) was handled, not a bad fill; confirm no genuinely-naked position (every fill got a resting stop within ~1-2 min — cross-check ORB_SL_OK vs entries).
5. **DID IT EXIT CORRECTLY?** every exit maps to the deployed rule (candle-close monitor / $500 cap / EOD-flatten); the $500 cap contained every loser; EOD-flatten left 0 positions.
6. **REVIEW EACH TRADE — entry AND exit correctness.** Per round-trip: entry followed the signal; exit fired the right rule at the right level; flag any that didn't. Winners: what (if anything) was left on the table (post-exit continuation) and is it recoverable. Losers: WHY (the current #1 = the unconfirmed-rides-to-EOD-flatten bleeder) — attribute each.
7. **DID TW WORK — tick-by-tick, no gaps?** from tw_health_check: ran full RTH window; live_exit_fired == EOD candle-close count; **stream disconnects = 0** (any RTH disconnect is a real stability flag — the resting stop was the backstop, but investigate); gaps caveat = gap_s is time-since-last-tick (thin/unheld names inflate it) → scope real concern to held-position windows.
8. **Triage every alarm** you (Rhett) got today: pull `code_inbox.jsonl` + `bot_alerts.jsonl`, VERIFY each vs broker truth, classify false/real, FIX the alarm if it cried wolf, LOG the disposition. (Alarms are guilty-until-broker-truth-proven-innocent.)
9. **Write the review** to SESSION_LOG + push SESSION_LOG **and** the standalone `EOD_LATEST.md` to coordination (Planning reads the small file, not the 585KB log). End with the single highest-value next move for profit.

---

## STANDING PRINCIPLES (owner's operating standard)
- **Verify before you state** — every load-bearing claim against broker truth / live code first; the alarms taught us this twice.
- **Every bug found gets a LOCK** — a regression test / drill case — so `audit_does_it_work.py` catches it forever. That's how the assurance compounds.
- **Watched trading files** (risk_config, bot_loop, exit_bot_v2, candle_close_exit, advisor_filter_engine, symbol_universe, orb_runner, orb_multiscan, short_bot, mover_scanner) → proposal + Rhett's go; everything else → fix now + validate.
- **Profit focus:** the edge is at the ENTRY (9:35 gated; re-arm carries) and the current drag is the EOD-flatten bleeders — measure before building, one change at a time, shadow-test, gauntlet, then promote. Live blockers stay SHADOW until Rhett says go live.

## OPEN OWNER TODO (ranked)
1. **TW stream stability** — 2 disconnects on 7/1 (1:58 PM, 3:39 PM); find why TW drops the stream + harden reconnect. (Exit quality depends on it; resting stops are the backstop.)
2. **EOD-flatten bleeders** — the #1 P&L drag: a time-stop / entry-filter for trades that never work and ride to the flatten. Study first.
3. A2-compliance exit-reason labeling still shows EXIT_UNCLASSIFIED (Flag-3 fallback didn't reach that section) — cosmetic, fix.
