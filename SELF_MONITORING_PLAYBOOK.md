# SELF-MONITORING PLAYBOOK — Claude watches the bot (Loop 221, 2026-07-02)

**Trigger to run this:** every trading day at **9:00 AM ET**, then **every 15 minutes** until 4:00 PM ET.
Invoke by pasting: *"Run the SELF_MONITORING_PLAYBOOK check."* (or via `/loop 15m` while the app is open).

## HOW THIS RUNS (Rhett's choice 2026-07-02: "keep the app open")
- **Always-on, every day, app open or not (Windows scheduled tasks — these page Rhett directly):**
  `AlphaQuant PreOpen TradeReadiness` (9:00 AM, `pre_open_trade_readiness.py`) + `AlphaQuant CSHV` (every 5 min,
  runs the hardened `check_alive_but_not_trading` → CRITICAL on alive+open+0-arms). Rhett is paged within 5 min
  of a silent no-trade regardless of whether I'm looping.
- **My active every-15-min watch:** a `/loop` (cron `*/15 9-16 * * 1-5`) that runs THIS playbook while the app is
  open. It is **session-scoped** (dies if the app closes/restarts). **SESSION-START RE-ARM (do this every time I
  start a session during/near a trading day):** check `CronList`; if no `*/15 9-16 * * 1-5` monitoring loop is
  running, RE-CREATE it (CronCreate, recurring) so the active watch resumes. Never assume it survived a restart.
- No headless/unattended autonomy — the active loop only runs with the app open, and Rhett stays in control.

**Why this exists:** On 2026-07-02 the bot sat out an entire open trading day (a bad early-close calendar
entry) and I didn't notice until Rhett did, at noon. My verification stopped at "does my change work / is it
healthy now." It never asked **"will the bot actually TRADE today, and is it trading RIGHT NOW?"** This playbook
makes me ask that, on a clock, and ACT on the answer — the same warnings Rhett gets, acted on.

---

## THE ONE RULE
> I get the same warnings Rhett gets, and I **act** on them — I don't just read them. A warning I saw and
> didn't act on is worse than one I never got. If I can't safely fix it, I escalate to Rhett with the
> diagnosis + the fix, in the same turn.

---

## 9:00 AM — PRE-OPEN "WILL IT TRADE TODAY?" CHECK
Run: `python C:\AlphaQuant\tradestation-bot\pre_open_trade_readiness.py`
- **GO / OK** → the entry path will arm today. Note it, done.
- **CRITICAL `ENTRY_PATH_WILL_NOT_ARM` / `TRADING_DAY_FLAGGED_HOLIDAY` / `CALENDAR_CONTRADICTION`** → the bot is
  configured to sit out an OPEN day. **ACT NOW (before 9:45):** open `market_hours.py` / the failing gate,
  find why the entry path skips, fix if non-watched (calendar data, a flag), or escalate + propose if watched.
  This is the exact 7/2 failure — never let it stand.
- **CRITICAL `RUN_BOT_STALE/NO_HEARTBEAT`** → run_bot is frozen/dead. Check `bot_heartbeat.json` freshness +
  `watchdog_supervisor.log`; if the supervisor didn't restart it, investigate the supervisor.
- **WARN `ENTRIES_HALTED / ADVISOR_BLOCK_ALL`** → intentional halt; confirm it's intended (not a stuck SAFE_MODE).

## EVERY 15 MINUTES, 9:00 AM–4:00 PM ET — INTRADAY HEALTH
1. **Read the warnings Rhett gets** (the same sources):
   - `python C:\AlphaQuant\tradestation-bot\alerts_bridge.py` → last-24h `bot_alerts.jsonl` summary; **any FAIL in the last hour is top priority.**
   - `C:\AlphaQuant\CSHV_FINDINGS.md` → any **FAIL/CRITICAL/WARN** (CSHV runs every 5 min; `check_alive_but_not_trading` now pages CRITICAL if the bot is alive+open+0 arms).
   - `outputs/alerts/code_inbox.jsonl` (via `code_alert_inbox.py --json`) → actionable items routed to me.
2. **The trade-liveness heartbeat** (the 7/2 catch): after 10:45 AM, if it's a regular trading day and market is
   open, confirm **≥1 `ORB_V16_ENTRY_OK` in `bot_alerts.jsonl` today**. Zero = OUTAGE → run `reliability_checks.check_alive_but_not_trading()`; it will name the cause (re-arm path dead / holiday-skip / filter). Fix or escalate.
3. **If I deployed a change in the last 24h**, verify it's BEHAVING in the live path today (not just "loaded") —
   e.g. after the time-stop deploy, confirm `TIME_EXIT` fires only on unconfirmed names; after a window change,
   confirm the new window armed.

## ACTION MATRIX (what "act" means per class)
| Warning | Fix now (non-watched) | Escalate + propose (watched trading path) |
|---|---|---|
| Bad calendar / config data (`market_hours.py`, non-strategy) | ✅ fix + regression-lock | — |
| Detector/monitoring bug (`reliability_checks`, `*_health*`) | ✅ fix + regression-lock | — |
| Entry/exit/sizing/gate LOGIC change (`orb_*`, `exit_bot_v2`, `risk_config`, `bot_loop`) | ❌ never edit mid-session | ✅ surface + PROP + Rhett's go |
| Naked position / stop missing | verify broker truth FIRST; if truly naked, tell Rhett to place a stop (I don't place orders) | — |
| Bot frozen/dead | check supervisor; a single restart is OK, but batch edits + restart ONCE (don't spam the crash alarm) | — |

**Verify before acting** (standing rule): every warning → check it against live/broker truth → classify
(false-alarm / real-unwatched / real-WATCHED / ambiguous) → fix-safe or escalate → **log to SESSION_LOG**.

## CLOSE-OUT each run
- If all clean: one line to SESSION_LOG (`[MONITOR HH:MM] clean — N entries today, CSHV OK, readiness GO`), no Rhett ping (silence = handled).
- If I acted: SESSION_LOG the warning + what I did + the proof it's resolved; ping Rhett only if it's actionable for him or I had to escalate.
