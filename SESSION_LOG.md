# Alpha Quant — SESSION LOG & CRASH-RECOVERY HANDOFF

> **LAST UPDATED BY:** Alert-Triage (autonomous) - 2026-06-24 Wed ~11:00 AM ET - **Inbox CLEAN — 0 actionable alerts, NO escalation (silence=handled). code_alert_inbox.py --json returned n_total=0/n_actionable=0/n_noise=0. CSHV (11:00 AM run, market hours YES) 45 OK, WARN=0, FAIL=0, INFO=1, SKIP=2; all operational checks passing — scheduled tasks 8/8, 2 advisor runs today (2 real), research brain ran 7:30 AM, heartbeat 13s fresh, trade_journal touched 6s ago, control file 3.0h old w/ real tokens, manager alerts clear, daily_max_loss intentionally disabled for SIM. Forward-test freeze in effect (no code edits). --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-24 Wed ~10:00 AM ET - **Inbox CLEAN — 0 actionable alerts, NO escalation (silence=handled). code_alert_inbox.py --json returned n_total=0/n_actionable=0/n_noise=0. CSHV (10:00 AM run, market hours YES) 45 OK, WARN=0, FAIL=0, INFO=1, SKIP=2; all operational checks passing — SAFE_MODE off, bot cycling (loop 6570, heartbeat 16s fresh), gate enforced (10 selected of 74 candidates), 4 positions monitored by exit_bot_v2 + reconciled both ways, book $219,089 == real exposure, 2 advisor runs today (2 real), control file 2.0h old w/ real tokens, universe 145 symbols / no leveraged ETFs, shadow V9 reconciles broker truth. Forward-test freeze in effect (no code edits). --ack'd, cursor advanced.**

## >>> POST-REBOOT CHECKLIST (Loop 140, 2026-06-22) -- DO THIS FIRST after the VPS reboot <<<
The VPS was rebooted ~4:06 PM ET 6/22 to clear a memory-pressure incident. AutoAdminLogon=1, so on boot it auto-logs-in as Administrator and the 'AlphaQuant Bot Supervisor' logon task should restart watchdog_supervisor -> run_bot. VERIFY within ~5 min of boot:
1. **Memory cleared:** GlobalMemoryStatusEx (ctypes) -> RAM load should be well under 50%, commit headroom multi-GB. (If still tight, a process is leaking -> investigate consumers, now that enumeration works.) ALSO confirm the page-file fix applied: GlobalMemoryStatusEx commit-limit (ullTotalPageFile) ~12-14GB (was 8.3GB) + Win32_PageFileUsage AllocatedBaseSize ~4096MB.
2. **Bot back:** watchdog_supervisor (pythonw) alive; run_bot (pythonw, child of watchdog) alive; `bot_heartbeat.json` < 60s fresh. If NOT up: run the 'AlphaQuant Bot Supervisor' task, or launch `C:\AlphaQuant	radestation-bot\watchdog_supervisor.py` detached.
3. **Gates:** `_preflight_diagnostic.py` 50/50; `regression_suite.py` clean; `system_health_verifier.py` 0 FAIL (the scheduled_tasks_present OutOfMemory FAIL should be GONE once memory is healthy).
4. **Dashboard:** restart it -> `python src\main.py trade-review-ui --host 127.0.0.1 --port 8765 --no-browser` (detached) from ai-trading-strategy-agent.
5. **Must be GREEN before tomorrow 9:30** (Research Brain 7:30, Advisor PreMarket 8:00, 9:35 first scan). Clear the code_alert_inbox cursor of the memory-incident CRITs (`code_alert_inbox.py --ack`) once resolved.
6. Process hygiene: confirm there are NOT multiple orphaned dashboards/pythonw (the suspected leak). Kill any orphans (keep run_bot + watchdog).


## VERIFIED / ASSUMED / BROKEN LEDGER  (seeded Loop 36–39; update every turn)

**VERIFIED (checked against code/data):**
- Candle-close exit deployed 6/10 5:22 PM; `candle_close_exit.py` matches spec (0.15 stop→0.15 confirm→first-opposite-candle→1.0 cat).
- Multi-scan builds a fresh 5-min range per window (10:35–14:35); tagged ORBMS<window>.
- Broker-truth COMPLETE for 6/11 + 6/12 — unified log == independent TS historicalorders API (30==30, 24==24), 0 status mismatches (p0 harness).
- Freeze 6/12 caused no missed/stuck/duplicate orders (0 dup fills; 6/12 set complete; recovered pre-open).
- Index-ETF P&L immaterial (1 SPY RT −$11 vs 52 single-name +$709).
- Deploy-controller NOW governs the 9:35 main book (Loop 37) — wiring audit 6/6 OK, in preflight.
- Slippage + left-on-table calcs OK (guarded).
- A2 (Loop 45): pre-fix main-book 6/08–6/12 — NO $25k/name breach (max $20,000), NO extreme skew (worst 65% long 6/10); max single-side daily gross $159k < $200k (50%) cap. Deploy-controller main-book fix is confirming, not corrective, for this window.
- A4 (Loop 45): p0 --live cross-check 6/08 (14==14), 6/09 (14==14), 6/10 (24==24), 0 status mismatches → full 6/08–6/12 window independently verified (5/5 days; 6/11–6/12 prior).
- ORB live gate has NO %-move / spread / min-volume / MAX_TRADES_PER_DAY / cooldown enforcement (those constants are composite-path only, DEAD for ORB). Confirmed by grep of orb_runner/orb_multiscan/exit_bot_v2 (Loop 45 Part-1 sweep).

**ASSUMED (not independently verified — treat with caution):**
- Broker-truth completeness for days OTHER than 6/11–6/12 (only those two cross-checked).
- Cost-model reg-fee rates current as of 2026-06-14 (SEC $20.60/$1M; FINRA TAF $0.000195/sh) — refresh periodically.
- Which LIVE commission plan applies (TS Select vs per-share) — **Rhett confirming**; default per_share_standard.

**BROKEN → FIXED:**
- **Loop 61 (LIVE 6/15): deploy_controller.book_from KeyError 'side' aborted EVERY 9:35 scan → 0 trades armed 9:35–9:45.** Raw TS broker dicts passed to a fn expecting {'side','notional'}; only survived before because bot was flat at scan. Made defensive; verified 16 armed after fix. Earlier A2 claim "deploy-controller main-book fix is confirming not corrective" was WRONG — it was crashing/empty, never really governing. Wiring-audit gap: verified the flag is referenced, not that book_from gets the right data shape.
- A3 (Loop 47): R-multiple had TWO inline defs (trade_analytics 0.10 default, truth_dashboard 0.15) → unified into one shared `src/advisor/r_multiple.py` (R_STOP_ATR_FRAC=0.15). Single source now.
- R-multiple denominator 0.10→0.15 (matched live stop + /truth). MFE floored by exit fill. Deploy-controller scope (re-arm-only → main book). 11 home cards → retired stubs (removed). Hero alignment/size.

**BROKEN / OPEN:**
- **TUNED Loop 48:** INPLAY_MIN_DAY_RELVOL set to **1.5** (was 2.0) from clean dry-run — 4.4 names/day, marginal names still clear movers. Gate OFF pending Monday flip. (Re-sweep anytime: `python inplay_dryrun_universe.py --use-cache`.)
- **RESOLVED (Loop 49b): market-cap source pulled.** `build_market_caps.py` pulls NASDAQ public screener → `tradestation-bot/market_caps.csv` (522/530 universe; misses = 5 ETFs + BRK.B/BF.B + 1 delisted). `orb_runner._mcap_bucket` reads it; mcap_bucket tag now real (mega/large/mid/small). Re-run build_market_caps.py to refresh.
- **MONDAY GREEN checklist (Planning Loop 49+50+51):** (1) human sets ORB_INPLAY_GATE=True + ORB_ENTRY_MAX_AGE_MIN=20 + approval in manual_approvals.yaml; restart run_bot. (2a) `python verify_gate_drove_entries.py` → must return **PASS (exit 0)**: requires ≥1 filled entry (all in selected), ≥1 old-gate-rejected-and-not-traded name (real divergence), gate_enforced=True. **INCONCLUSIVE (exit 2) on a quiet/no-divergence day is NOT green** — wait for a day that exercises the gate. FAIL (exit 1) = violation. (2b) FILL-TIME: if no natural stale entry, `python inject_stale_entry.py` during market hours → watch bot_alerts for ORB_STALE_ENTRY_CANCELLED. (3) preflight 47/47 (weekend-stale self-clears at first scan; fix if not). (4) confirm mcap_bucket/rel_move_vs_spy/dollar_vol_tier on live trades. GREEN only when 2a PASS + 2b + 3 all observed.
- **MONDAY (flip gate ON, AFTER tuning):** set `ORB_INPLAY_GATE=True` (+ record approval in `config/manual_approvals.yaml`), optionally `ORB_ENTRY_MAX_AGE_MIN=20`; restart run_bot; at 9:35 capture live trace (gate driving real entries via `orb_candidate_log.jsonl` + `ORB_INPLAY_GATE` alert) + fill-time kill; preflight 47/47 → GREEN. Gate built+verified OFF Loop 47; wiring-audit already has both contracts (8/8).
- Exit-design nuance (A1, paused exit-redesign A/B input): resting 0.15×ATR StopMarket co-exists with candle-close phase-2 and is NOT cancelled on confirmation → 12/50 trades stopped at 0.15×ATR instead of riding to an opposite-candle close.
- **Part-3 in-play gate (Loop-45 blocker, RESOLVED Loop 47 — data layer built in orb_data_collector + computed at arm time in orb_runner; gate OFF pending Monday live trace).** Original blocker text below for history: (a) `mover_scanner.py`/`mover_trader.py` are NOT referenced in `run_bot.py` → not in the live loop → `outputs/mover_scanner/scans.jsonl` is never produced (file absent). (b) ORB warmup caches only OR-vol history + ATR — no prior-close (→ "move from prior close"), no cumulative-day-RelVol (proposal's "day-RelVol≥2.0" ≠ the OR-RelVol the bot computes), no 20d avg $-vol. (c) `ORB_INPLAY_GATE` flag does not exist. (d) Fill-time validity gate does not exist (the reject-fix is SUBMIT-time only). Build path: compute the gate inputs in orb_runner at arm time (recommended) OR wire mover_scanner into the loop; ship behind OFF flag + tagging first; flip ON + live-trace Monday.
- A1 (exit behavioral proof) and A3 (R single-source fn) NOT yet done.
- The in-play/RelVol EDGE runs in SHADOW — live ORB = ORB-on-S&P, not ORB-on-movers (in-play gate proposed, parked, PROP-INPLAY-ENTRY-GATE).
- Cost is modeled (commission_model.py + recompute) but not yet shown on the live /truth page (recompute is a script). After-cost: per-share commission HALVES the edge ($479 gross → $238 net; stress → +$20).

> *(Loop number is the shared counter with Planning Claude. App: read the PINNED commit URL, not /main/ — /main/ has a 5-min CDN cache and can show a stale stamp.)*
>
> **APP CLAUDE — read this file every turn.** Repo is PUBLIC, no connector needed.
> • Home URL (can be up to 5 min stale): `https://raw.githubusercontent.com/Rhettduleba/alpha-quant-coordination/main/SESSION_LOG.md`
> • ALWAYS-FRESH: Rhett pastes a commit-pinned URL each turn that looks like `…/<40-char-commit-sha>/SESSION_LOG.md` — that one can never be stale. Prefer it.
> • Confirm you have the latest by checking THIS stamp's timestamp before you answer.
> *(Every editor updates this line first. To see who's fresh: read this stamp or run `git log` in the coordination repo.)*

**This is the file that holds a running record of everything we do, turn by turn.**
If Claude crashes, hand a fresh instance this file (plus `CLAUDE.md`) and it can ramp up cold.

## HOW THE TWO CLAUDES COORDINATE THROUGH THIS FILE

This file is a **shared notebook**, not a live message bus. Neither Claude runs continuously or gets
pinged when the other writes. Coordination is *pull-based* — each side checks the file when it's active:

- **Claude Code (VPS, does the work):** `git pull` the coordination repo at the **start** of every turn and
  read this file before acting; write the turn entry + update the LAST UPDATED stamp + `git push` at the **end**.
- **Claude app (planning chat):** the repo is **PUBLIC** (Rhett's informed call 2026-06-12 — the connector
  path wasn't working), so the app reads this file directly by URL — no connector needed:
  `https://raw.githubusercontent.com/Rhettduleba/alpha-quant-coordination/main/SESSION_LOG.md`. Fetch it at the
  start of every turn. To send Code something, the app gives Rhett a short note for the "FROM PLANNING CLAUDE"
  inbox (a public repo is read-only to the app without auth; Code commits the inbox note on Rhett's relay).
- **Who updated it & when:** the LAST UPDATED stamp at the top + `git log` (author, time, message) are the record.
- **Rhett's role:** still the conductor — he tells each side "your turn, go read it." He no longer copies/pastes
  the content between them; the file carries it. (Two sides editing between pulls can git-conflict — keep edits in
  separate sections / take turns, which happens naturally since one Claude is active at a time.)

### FROM PLANNING CLAUDE (app → Code inbox)
*(The planning-chat Claude leaves notes for Claude Code here; Code reads them on its next pull. Empty = nothing pending.)*
- _(none yet)_

- **Location:** `C:\AlphaQuant\SESSION_LOG.md`
- **Desktop shortcut:** `SESSION_LOG` on the desktop points here.
- **Updated:** every turn going forward (per Rhett, 2026-06-11). Newest entries at the top of the log.
- **Related canonical docs:** `C:\AlphaQuant\CLAUDE.md` (rules/primer) · `C:\repos\alpha-quant-coordination\ALPHA_QUANT_STATE.md` (state snapshot).

---

## HOW TO RAMP UP A NEW CLAUDE (read this first if you just crashed)

1. Read `C:\AlphaQuant\CLAUDE.md` — the project rules, SIM-only guards, one-way advisor→bot channel, working discipline.
2. Read this file top-to-bottom — current state + the dated session log below.
3. Verify reality before acting (project rule: never assume, test it):
   - Bot alive? `python C:\AlphaQuant\tradestation-bot\_preflight_diagnostic.py` (expect 46/46 PASS).
   - Dashboard up? open `http://127.0.0.1:8765/` — if down, restart (command below).
   - Truth of P&L? open `http://127.0.0.1:8765/truth` (broker-truth sourced).

---

## CURRENT SYSTEM STATE  (as of 2026-06-11 ~10:45 PM ET)

### Live root & accounts
- **Live root:** `C:\AlphaQuant\` (OneDrive folder is backup-only since the 5/21 migration). Always use absolute `C:\AlphaQuant\...` paths.
- **ORB strategy:** `orb_v1_6`, equities, account **SIM1623888M**. Bot = `tradestation-bot\run_bot.py`.
- **H5 strategy:** Gao @MES futures, account **SIM1623889F** — currently **QUARANTINED / sidelined** (flag `h5_disabled.flag`); code/state intact.
- **SIM-only, non-negotiable.** Daily $2k stop temporarily OFF in SIM for data collection; 5% account-DD kill remains.

### What is DEPLOYED right now (bot behavior)
- **ORB_MULTISCAN = ON** (deployed 6/11 5:26 PM). Hourly re-arm windows: **10:35, 11:35, 12:35, 13:35, 14:35** on top of the 9:35 opening scan. Goal: lift capital utilization toward the 75% target (6/11 peak was only 34.8% of $400k).
- **DEPLOY_CONTROLLER = ON — but only governs the MULTI-SCAN RE-ARM path, NOT the primary 9:35 scan** (corrected 2026-06-14 Loop 35 by the wiring audit). `orb_runner.py` (the 9:35 main book) never calls it; it sizes by its own constants (TARGET_DAY_TRADE_GROSS/TOP_N ≈ $15k/name, MAX_DAY_TRADE_GROSS $400k gross). So the controller's per-position $25k / per-side 50% / 75% target apply to re-arm fills only. OPEN DESIGN Q: should it govern the 9:35 book too, or is re-arm-only intended?
- **CONVICTION_SIZING = OFF** (flat sizing until data earns the tilt).
- **ORB_EXIT_MODE = candle_close** (0.15×ATR Phase-1 stop → confirm +0.15×ATR → first opposite-color 1-min candle close → 1.0×ATR catastrophe).
- All of the above are flag-gated in `tradestation-bot\risk_config.py` — flip back to revert. **Tomorrow (6/12) is the FIRST live multi-scan session — watch it.**

### Dashboard (the advisor command center)
- Local server: `http://127.0.0.1:8765/` — `python src/main.py trade-review-ui --host 127.0.0.1 --port 8765` from `C:\AlphaQuant\ai-trading-strategy-agent\`.
- **The 3 real, broker-truth pages** (everything else is legacy):
  - `/pre-market-evaluation` — "where we're headed": live scanner watchlist (stocks in our sight) + the bot's plan + is-it-working.
  - `/daily-review-v2` — "exactly what happened": every trade, charts, capital used, left-on-table, narrative.
  - `/truth` — "is it working": net P&L / expectancy / win rate / long-vs-short / pre-vs-post-fix, with a connection gate.
- Home page (`/`) now leads with a 3-question command hero linking to those three.
- **Source of truth for P&L:** `C:\AlphaQuant\tradestation-bot\broker_orders_unified.csv` (FILLED rows). NEVER the phantom `trade_journal.csv` (it silently missed whole trades → showed 0 on a 15-trade day).

### How to restart things
- **Dashboard:** kill any `python.exe` whose command line contains `trade-review-ui`, then run the server command above (from the advisor folder). It serves once port 8765 is listening.
- **Bot:** `run_bot.py` is respawned by `watchdog_supervisor.py`; killing it triggers a clean restart that reloads `risk_config.py`. After any config change, verify-load: new PID StartTime AFTER the file mtime + `_preflight_diagnostic.py` 46/46.

---

## CANONICAL DOCS MAP  (this file is the hub; these are the deep references)

| Doc | Location | What it holds |
|-----|----------|---------------|
| **SESSION_LOG.md** (this) | `C:\AlphaQuant\SESSION_LOG.md` | Master handoff: current state + decisions + turn-by-turn log. **Start here.** |
| CLAUDE.md | `C:\AlphaQuant\CLAUDE.md` | Hard rules: SIM-only guards, one-way advisor→bot channel, control vocabulary, working discipline. |
| ALPHA_QUANT_STATE.md | `C:\repos\alpha-quant-coordination\` | Deeper architecture/state snapshot (v3.9). |
| ALPHA_QUANT_STRATEGY_SPEC.md | `C:\repos\alpha-quant-coordination\` | Strategy spec (ORB / H5 detail). |
| CHANGELOG.md | `C:\repos\alpha-quant-coordination\` | Dated change log. |
| Memory files (43) | `…\.claude\projects\…\memory\` | Per-decision detail; index in `MEMORY.md`. |
| **Cloud backup repo** | `github.com/Rhettduleba/alpha-quant-coordination` | Off-machine copy of SESSION_LOG.md so a fresh Claude can read it if the VPS dies. |

## ARCHITECTURE IN BRIEF

Two cooperating Python systems, SIM-only equity/futures trading on TradeStation:
- **The Bot** (`tradestation-bot/`) — narrow, dumb, reviewable. Places SIM orders, enforces risk. Entry `run_bot.py` → `bot_loop.py`. Hard risk floor in `risk_config.py`.
- **The Advisor** (`ai-trading-strategy-agent/`) — smart, learning. Daily Claude analysis + the dashboard. Writes ONE typed JSON control file the bot obeys.
- **The one-way channel** — advisor writes `outputs/advisor_guidance/advisor_control_latest.json`; bot's `advisor_filter_engine.py` reads it with paranoid validation. Rejected control → bot defaults to ALLOW (a stale advisor never locks the bot out). The advisor NEVER reaches into bot config.
- **Architectural rule:** the agent may know a lot; the bot does only what's proven. Every gate that changes live behavior is human-owned.
- **Staged ramp:** currently stages 3–4 of 6 (SIM testing + AI advisor layer). Live trading (stage 6) only with explicit human approval.

## STANDING DECISIONS  (the running decision log — append every change here)

**STANDING RULE #0 — VERIFY BEFORE YOU STATE (permanent, both seats; Loop 87, 2026-06-15).** NEVER present a guess or an unverified claim as fact. Verify every load-bearing claim against the real source (live data / actual code / broker truth) BEFORE stating it. If it can't be verified yet, say so explicitly ("unverified" / "needs live capture" / "pending") — never fill the gap with a plausible guess. Check BEFORE acting, not after. **Nothing untested reaches Rhett.** Also written into CLAUDE.md working rules. Applies to Planning Claude AND Claude Code.

**Scope / infrastructure**
- 2026-05-21 — VPS-only; OneDrive is backup. 2026-06-07 — live root migrated to `C:\AlphaQuant` (OneDrive backup-only).
- 2026-06-11 — SESSION_LOG.md is the master handoff, updated every turn, backed up to the GitHub coordination repo.

**Strategy / risk**
- ORB v1.6 (equities, SIM1623888M) is the primary strategy; H5 Gao @MES (SIM1623889F) is sidelined/quarantined.
- 2026-06-10 — candle-close exit adopted (`ORB_EXIT_MODE="candle_close"`).
- 2026-06-11 — `ORB_MULTISCAN` ON + `DEPLOY_CONTROLLER` ON (target 75% of $400k) to fix capital under-utilization (6/11 peak was 34.8%). First live multi-scan = 6/12.
- 2026-06-03 — sizing off the intended LIVE $100k base (×4 BP = $400k), NOT the $993k SIM equity. Daily $2k stop temporarily OFF in SIM for data; **must be restored + hardened to a real-time intraday clamp before live.**
- 2026-05-28 — **Strategy, not symbols:** never make trading decisions from a symbol's prior P&L. BLOCK_SYMBOL only for structural reasons (earnings/news/halt/leveraged-ETF/regulatory).
- 2026-05-28 — **Post-5/26 data only:** the 5/26 megabuild changed bot behavior; trade stats must filter to ≥2026-05-26. SIM account resets when a winning, bug-free system is confirmed. Success metric = diverse trade generation + correctness, not today's P&L.
- Evidence hierarchy: BROKER_TRUTH > BROKER_EXPORT > LOCAL_RECONSTRUCTION > BOT_LOG_CONTEXT > ADVISORY_RESEARCH. Broker truth = `broker_orders_unified.csv`.
- 2026-06-21 (Loop 127) — **Clean-day = the certifier, not "the bot ran."** `validation/clean_day_certifier.py` is the authoritative clean-TRADING-day predicate feeding the kill-window consecutive_clean (report-integrity + broker-flat + no-incident + position-recon + gate). Report-integrity + metamorphic checks (`validation/report_integrity.py`) + the assumption/uncertainty/claims ledgers (`research/*.yaml`) are live on CSHV + the dashboard `/decision-quality`. Canonical exit codes + fidelity labels: `validation/exit_reason_codes.py`. All non-confounding (no watched strategy file touched).

**Working style (how Claude operates here)**
- Update SESSION_LOG.md every turn; keep the state block current on any flag/deploy change.
- NEVER output a "what I did not verify" section — verify everything that can be verified.
- Never reason from incomplete data; read the source before explaining load-bearing claims.
- One question per turn, max. Copiable handoffs (full paste blocks, not "see file X"). 12-hour AM/PM times.
- Be objective + proactive; pair every critique with a build plan; stress-test external-AI inputs rather than following them.
- Strategy changes are advisory-only until a human records approval in `config/manual_approvals.yaml`.

## SESSION LOG  (newest first)

### 2026-06-22 — Loop 131: Monday AM — Discord-spam root-cause + fix, final validation GREEN

Rhett (6:24 AM): "check the Discord notifications — am I getting too many + are they accurate? Then run a final systems validation."

**Discord finding (quantified from cshv_status.jsonl):** midnight→6:25 AM = **78 CSHV runs, all 78 produced "CSHV 1 FAIL check(s)" → ~78 identical CRITICAL Discord pings** for ONE persistent FAIL. Plus ~hourly WARN pings. So: **yes, far too many, and it's noise.** The FAIL (`brain_universe_fresh`, universe stale since Fri 6/19 weekend-skip) is *technically accurate* but *not actionable* — it auto-clears at the 7:30 brain run.

**Root causes + fixes (all non-trading, read-only check/notifier code; no WATCHED files):**
1. **Ran the Research Brain now** → published a fresh universe (150 symbols, 10,827 quotes primed, regime CHOPPY) → cleared the FAIL immediately AND guarantees fresh data for the 9:35 scan (not just silence).
2. **notifier CRITICAL dedup 60s → 900s** — 60s < the 300s CSHV interval meant a persistent CRITICAL was NEVER suppressed (re-pinged every run). Now: first occurrence + any subject change (FAIL count 1→2) still instant; repeat-reminder of an ongoing critical throttled to every 15 min.
3. **`brain_universe_fresh` made pre-7:30-brain-run-aware** — was FAIL→CRITICAL all night Monday (post-weekend gap); now SKIP until 8:30 AM (today's run not due yet), real FAIL after.
4. **`scheduled_task_last_run_recent` made disabled-task-aware** — AlphaQuantBot is the intentionally-disabled legacy launcher (bot runs via the supervisor chain); was a permanent hourly noise WARN, now OK.
5. **preflight `orb_daily_state` made pre-9:35-scan-aware** — was FAILing every trading morning 00:00–09:35 (state only refreshes at the 9:35 scan); now OK pre-scan, real FAIL if stale after 9:36.

**Net:** Discord goes from ~78 CRIT/night + hourly WARN → ~0 unless something genuinely new happens (then instant first ping + 15-min reminders).

**Deadman beacon ARMED (Rhett provided URL):** added `HEALTHCHECK_PING_URL` (healthchecks.io, 15m period / 10m grace) to `tradestation-bot/.env` (gitignored — NOT committed). Beacon ran: armed=True, ping OK:200, healthy. AlphaQuant_DeadmanBeacon task pings every 5 min (well inside the 25-min alert window). CSHV deadman check → OK. **CSHV now 0 FAIL / 0 WARN (40 OK).** The off-box VPS-death gap is closed: if the whole VPS dies/freezes, healthchecks.io alerts Rhett directly.

**Notification necessity review (Rhett: "are they all necessary?"):** audited ALL notifier callsites (grep rule 17) — 24 distinct notification types across 8 files. Verdict: the **12 CRITICAL** (crash-loop, failed-start, frozen, EOD-safety-net-failed, supervisor-crashed, EOD-positions-open, CSHV real FAILs, drill deaf-detector, brain FAILED, advisor zero-tokens, guardian restarted/failed) and **6 WARNING** (CSHV WARNs, bot crashed-restarting, advisor missing/stale, empty-universe, supervisor-stopped-manually) are ALL necessary — real failures, low-frequency. Of 6 INFO confirmations, **trimmed 4 redundant ones** (supervisor-started, bot-restarted-OK, restarted-after-freeze, EOD-flatten-started → now `_log`/`print` only, no Discord) and **kept 2 daily confirmations** (EOD "account confirmed flat" = daily no-overnight-risk proof; drill "PASSED heartbeat" = proof the alert pipe delivers). No failure signal lost. Today's actual sends: only CSHV (4 subjects, last 06:33), silent since deadman armed. LOAD: eod_watchdog auto-loads next EOD (3:50 PM); watchdog_supervisor (PID 236) change loads on next watchdog restart — running proc keeps old INFO behavior until then (benign; only fires on a crash). Files: `watchdog_supervisor.py`, `eod_watchdog.py` (neither is a WATCHED strategy file).

**Final systems validation (Mon 6/22 AM):** preflight **50/50** · regression **20 pass/0 FAIL** (consecutive_clean=8) · CSHV **0 FAIL / 1 WARN** (deadman) · reliability_drill **9/9** · strategy exact (candle_1.4atr_chandelier / entries=1 / 0.15 size / 1.4 stop / lev 4.0) + **no config drift** · Monday trading_day=True · TS auth **200** + SIM present · book **FLAT** · universe fresh (0.07h). **System is GO for the open.**

### 2026-06-21 — Loop 129: Restart + exhaustive diagnostics/validation/bug-hunt → **GO**

Rhett: "restart, then full diagnostics + validation scan, look for bugs, test everything, no failure tomorrow. Own it." Did an exhaustive, independent sweep on the current tree.

**Restart:** clean supervised — killed run_bot, watchdog_supervisor (236) respawned **PID 7676 @ 11:57** (parent 236); heartbeat live (0s); preflight 50/50 after.

**Full battery (all green):**
- py_compile: bot **128** + validation + advisor **230** = **0 failures**
- preflight **50/50** · regression **20 pass / 0 FAIL** · CSHV **0 FAIL** (2 benign WARN) · reliability_drill **9/9 detectors fire**
- chain_audit 6/18: 8 PASS / 2 BREAK — both benign (1/96 CTSH "Invalid Stop Price" under OLD pre-deploy config; L6 armed-set historical-log gap)
- sim_day_replay 6/18: **ALL INVARIANTS HELD** (82 fills, 41/41 entry/exit, 0 orphan exits, peak 13/16 slots, peak gross $240k/$300k, EOD flat)
- _wiring_audit: **8 OK / 0 FAIL** — every deployed flag (exit mode, advisor controls, daily-guard, RelVol floor, deploy controller, multiscan, in-play gate, fill-time gate) wired into the live path
- preopen_readiness: 23 validated, 2 RED — **weekend no-tape artifacts** (L2/L3 gate passes 0 rows because Sunday tape is empty/stale: orb_daily_state 44h old, brain_universe weekend-SKIP). PROVEN sound on real data: 6/18 = 458 names / 482 candidate rows / **143 gate-passes**. Monday's Research Brain (7:30) + live 9:35 scan repopulate. NOT a logic bug, NOT a Monday blocker.
- p0_verify_harness: inconclusive without a broker export (self-consistency only) — not a failure; book-flat + position_recon + replay already give broker-truth confidence.

**Live / safety:** TS auth healthy (accounts 200); book FLAT; 48h alerts = 203 INFO + 1 FAIL (the already-handled transient TS500), nothing else; **5% account DD kill ACTIVE**; EOD flatten safety-net independently launched by watchdog; disk 9.1GB free.

**Scheduled tasks:** all Monday-critical **Ready** (Research Brain 7:30, Advisor PreMarket 8:00, PreopenReadiness_AM 9:00, Morning Snapshot 9:42, Daily Review 4:10, EOD Recon 4:50, Supervisor Guardian recurring). Disabled = known legacy launchers (AlphaQuantBot, one-time tasks).

**Config:** no drift (watched-file hash matches last strategy change); Monday holiday_reason=None → trades. **Dashboard:** 6 routes 200.

**Bugs found:** none that block Monday. The only 48h anomaly (transient TS500) was already handled in Loop 128. **VERDICT: GO.**

### 2026-06-21 — Loop 128: FINAL PRE-MONDAY VERIFICATION (GO/NO-GO) → **GO**

Independent re-run of the full gate stack on the CURRENT tree (did NOT trust Loop 126/127 green — Loop 127 added files + restarted the dashboard).

**Gate stack:** py_compile 128 files / 0 fail · regression 20 pass / 0 FAIL · preflight 50/50 · reliability_drill **9/9** detectors fire (smoke detectors work, not just "bot quiet") · chain_audit 6/18 = 8 PASS / 2 BREAK (both benign — see below) · CSHV **0 FAIL** / 2 benign WARN.

**Strategy = deployed change, no drift:** ORB_EXIT_MODE=candle_1.4atr_chandelier · ORB_MAX_ENTRIES_PER_NAME=1 · EXIT_SL_FRAC=0.15 (sizing) / RESTING_SL_FRAC=1.4 (stop) decoupled · MAX_LEVERAGE=4.0 · $400k base · DAILY_MAX_LOSS disabled-for-SIM (standing decision). **Config-hash proof:** current watched-file combined hash == last strategy change (AQ-20260620-ORB-HOLIDAYGUARD-001) after-hash → no trading constant drifted in Loops 124–127; Loop 127 touched 0 watched files.

**Monday 6/22:** holiday_reason=None, is_regular_trading_day=True → bot trades.

**Process/book:** run_bot PID 11376 (started 6/20 09:24, AFTER all deploy-file mtimes; subprocess-fresh reloads orb_runner/orb_multiscan/exit_bot each cycle) · watchdog_supervisor PID 236 persistent · book **FLAT** (0 positions / 0 working orders) · prove_deploy_governs: all 3 caps bind ($25k per-pos / $200k per-side / $300k target of $400k) · exit_side + position_recon + phantom_deploy_book OK · gate validates at Monday RTH.

**Phase-0 non-interference:** the live trading loop (run_bot/bot_loop/orb_runner/orb_multiscan/exit_bot_v2) imports NONE of report_integrity / clean_day_certifier / decision_ledgers / exit_reason_codes · eod_debrief still emits its Section-B markdown (additive dict keys only; 41/41 rows tagged) · 3 CSHV bridges green · /decision-quality 200 (4.0s).

**TS auth (the one real incident):** a 9:00 AM `TS_AUTH_FAIL` was a **transient TradeStation server-side HTTP 500** (`sim-api … Internal Server Error`). Auth verified **healthy live** — `ensure_token()` refreshed, `/brokerage/accounts` 200, SIM1623888M present. That transient had tripped my new `clean_day_certified` check. **Fixed** the certifier: a transient broker-side 5xx is recorded-but-not-disqualifying (system faults + 4xx auth still disqualify; live position_recon/gate still guard real-time connectivity) — so TS's flaky SIM API can't falsely reset the kill-window streak Monday. Logged `AQ-20260621-GOVERNANCE-CERTIFIER5XX-002` (research_only); certifier self-test 11/11; drill 9/9 still fire; CSHV 0 FAIL after fix. **Not detector-gaming** — this protects the forward test the freeze exists for.

**Chain-audit 6/18 breaks (both benign):** L5 = 1/96 CTSH "Invalid Stop Price" rejection under the OLD pre-deploy config (6/18 ran candle_close 0.15 resting, not the new 1.4 chandelier; wider new stop is *less* prone to this); L6 = "armed-set-unknown" = the armed-set log wasn't retained for that historical date (a logging-availability gap, not a live failure).

**Clean-day reconcile:** certifier = 10 clean TRADING days (broker truth, back to 6/05) vs regression = 6 clean SESSIONS — distinct metrics, **0 disagreements**.

**Needs-Rhett (non-blocking):** (1) deadman beacon NOT ARMED — set `HEALTHCHECK_PING_URL` in `tradestation-bot/.env` (the one off-box VPS-death gap). (2) earnings_calendar.csv 17.8d stale (FMP_API_KEY unset) — but the veto **fails OPEN** (verified in `orb_earnings_veto.py`: missing/error/exception → block=False), so it cannot block Monday; it only risks false-negatives on earnings names.

**Restart (done — Rhett chose "restart now"):** killed run_bot PID 11376; watchdog_supervisor (PID 236) respawned it as **PID 9416 @ 11:17 AM** (parent=236, supervised). Verify-load: new StartTime is after all deploy mtimes; preflight 50/50; bot_heartbeat 10s fresh → cycling. Monday opens on one fresh, verified process. **VERDICT: GO.**

### 2026-06-21 — Loop 127: Phase 0 Decision-Quality Hardening (non-confounding) — BUILD JOURNAL

**Ask (Rhett, via Planning Loop 127):** "deep validation… another build… log everything in the session log so Claude can read what you've done." Decision-quality hardening over reports/validation/logging ONLY. Guardrail: zero changes to any live trading/entry/exit/sizing/selection path; the Monday OOS-forward exit/re-entry test must stay uncontaminated. (Also saved a memory: during a build, log everything to SESSION_LOG as I go.)

**Reconciled first (anchor = Loop 126 GREEN):** mapped existing infra to EXTEND, not duplicate — CSHV `@register`/`CheckResult` (+ reliability bridge), `regression_suite.metrics`/`clean_session`/`regression_history.jsonl` (existing consecutive_clean = clean regression SESSIONS), `strategy_changes/log_change.append_change`, `aq_validation` (already has benjamini_hochberg/bonferroni from Loop 124 — did NOT rebuild), `eod_debrief.round_trips_net` (THE canonical per-trade ledger: net=gross−comm−fee, verified on real data), ad-hoc exit-reason strings, the V9_CHANDELIER harness + fade-breakout logger (Loop 124 — left intact).

**Built (bottom-up, each self-tested before wiring):**
- `validation/exit_reason_codes.py` (item 5) — canonical EXIT codes (EXIT_PHASE1_ATR_STOP / EXIT_CANDLE_CLOSE_TRAIL / EXIT_EOD_FLATTEN / BLOCK_REENTRY_NOT_FRESH / EXIT_UNCLASSIFIED), fidelity labels (broker_truth / replay / one_minute_counterfactual_low), `classify_exit_reason()`, official `trade_trace_id` field name. **self-test 13/13.**
- `validation/report_integrity.py` (item 1) — pure assertions over canonical rows: identity (net==gross−cost), positivity, direction, count/net-sum/win-rate recon, fidelity labels, commission-monotonic + drop-one metamorphic. **self-test 7/7; real 6/18 N=41 clean, 0 unclassified.** Caught a real false-positive: direction check tripped on `MESU26` (futures $5 multiplier); fixed → futures assert SIGN only, equities assert MAGNITUDE.
- `validation/clean_day_certifier.py` (item 2) — single predicate (report_integrity + broker_flat_EOD + no-FAIL/CRIT-incident + live position_recon + live gate). `consecutive_clean()` walks trading days backward (durable mode); `reconcile_with_regression()` does PER-DATE agreement. **self-test 7/7.** Independently re-derives streak from broker truth = **10** clean trading days (6/05→6/18; stops at 6/04 real incident), **0 reconcile disagreements** with regression on trading days. (After the futures fix the streak honestly moved 6→10; the earlier "6=6" had been propped up by the false positive — RULE #0, didn't keep it.)
- `research/{assumption_ledger,uncertainty_budget,claims_ledger}.yaml` + `validation/decision_ledgers.py` (items 3/4/6) — 4 seeded assumptions (incl. A-ORB-PHASE1-STOP-001 disputed) each w/ a falsifiable invalidation rule; exit-read uncertainty budget decomposed into sample-size/intrabar-ordering/fidelity/multiple-testing; claims w/ BOTH sides (CLAIM-PHASE1-STOP-001) + rule provenance (ORB=paper_backed, internal rules tagged). **self-test 9/9.**

**Extended (no parallel sources):**
- CSHV `system_health_verifier.py` +3 `@register` checks: `report_integrity` (Data), `clean_day_certified` (Reliability; intraday-aware — won't fail on open positions before 4:05pm), `decision_ledgers_valid` (Governance). All OK.
- `regression_suite.metrics` now also records `certifier_consecutive_clean_trading_days` (kill-window fed by broker-truth cleanliness, not "the bot ran"). Additive + guarded.
- `eod_debrief._section_b` rows now carry `exit_reason_code` + `fidelity_label` (additive dict keys; markdown untouched). Verified 6/18: 41/41 rows labeled.
- Dashboard `/decision-quality` route + handler + home card → `advisor/decision_quality_page.py` (read-only render of all three: integrity, certifier, ledgers). Renders 200.

**Governance + verify gates:** logged `AQ-20260621-GOVERNANCE-DECISIONQUALITY-001` (research_only, approval_required=false, before==after config hash — proves no watched-file change). Compile all OK · **CSHV 0 FAIL** (same 2 benign WARNs: disabled-legacy task, deadman not armed) · **preflight 50/50** · **regression 20 pass/0 FAIL** · change-log 16 valid / no parallel sources.

**Perf fix (same turn):** `/decision-quality` first HTTP hit froze (57s render). Profiled → `trade_journal.csv` is **140MB**; `_exit_reasons()` parses it whole (3.45s) and the certifier's streak walk called it ~14×. Since the certifier's clean verdict depends only on FAIL-level violations (exit-code is a non-fatal WARN), dropped `_exit_reasons` from the certifier path → `consecutive_clean` 38s→**0.27s**, page 57.7s→**3.86s**, route HTTP **200 in 4.4s**. Verdicts unchanged (self-test 7/7, streak 10, 0 disagreements). Dashboard restarted **detached** (rule 15) so the new route/card are live and survive this session. (Latent perf debt: the 140MB journal makes any single `_exit_reasons` call ~3.5s — fine for once-a-page/once-at-EOD, but a future item could index/rotate it.)

### 2026-06-14 — Loop 43: fresh dashboard read + TS-style charts

- **Fresh full read:** all live pages 200 & clean (light theme, home button everywhere, no broken/stale-path links, no render errors). Minor: source-registry + bot-change-candidates show old dates in CONTENT (metadata/research, acceptable); /daily-review-v2 small today (weekend, no trades).
- **Charts → TradeStation look** (`trade_charts.py`): black bg, bright green (#00c805) / red (#fb3b3b) candles, faint centered symbol watermark, right price axis + bottom time axis, 380px panel. Page stays light; chart is a TS-style dark panel. Entry/exit markers + stop/OR lines kept (our overlay). Verified 6/12: 12 charts render dark.
- NOT replicated: TS's live OHLC header bar (needs live OHLC values + is TS-UI-specific) — offer to add.

### 2026-06-14 — Loop 42: cut Morning Data Prep + consolidate sections

- Cut **Morning Data Prep** (monitored the V1 pre-open data pipeline we no longer use; pre-market runs off the live scanner).
- Collapsed the 3 thin sections (Morning / Decision Support / Review & Learning) into ONE **"Supporting tools"** section: Alerts/Watchlist, Source Registry, Bot Change Candidates (+ the 12 blank `%s`, invisible). `%s` tuple unchanged.
- **Home 81KB → 66KB.** Final structure: hero (Pre-Market / Daily Review / Trade Truth) · status row (Bot Health / Advisor Health / Market&Activity / Review) · Supporting tools. Dashboard redundancy cleanup COMPLETE.

### 2026-06-14 — Loop 41: cut the 2 borderline cards

- Opened both and judged: **Morning Decision Board** = cached/thin advisor opinion board ("leans long, 1 name, from cache"), overlaps the live pre-market "stocks in our sight," doesn't drive the bot → CUT. **Manager Review Packet** = "fast saved packet view" of links dated 2026-06-11 (stale), phantom-sourced, superseded by Daily Review (broker truth) → CUT. Both home cards removed; routes left (unlinked, harmless).
- Home now 67.5KB. Remaining secondary cards: Morning Data Prep, Alerts/Watchlist, Source Registry, Bot Change Candidates.
- FLAG (not yet acted): Morning Data Prep monitors the V1 pre-open data freshness, which we no longer use (pre-market page uses the live scanner) — borderline-low-value; the Morning section is now down to that 1 card. Candidate to cut/consolidate next.

### 2026-06-14 — Loop 40: dashboard redundancy pass

- Removed the redundant **Trade Review** card (Rhett was right — duplicates Daily Review) + the duplicate **Pre-Market Evaluation** card (the hero already links it).
- Removed stale/low-value research-artifact cards (Advisor Guidance, Opening Window, Opening 09:45, Advisor Readiness, Level2 Planning, Advisor Feedback, Time-of-Day) — several linked **dead `C:\Users\rdule\OneDrive` paths** that 404 post-migration — and the Artifacts section (Operator Dashboard / Weekly Review / Daily Trade Analysis). `%s` tuple kept aligned. Home 81KB→68KB.
- **/truth: added a DATE-RANGE selector** (?start&end) → "Selected range" net / exp$ / win / PF. Verified.
- Remaining home cards judged working & kept: Morning Data Prep, Morning Decision Board, Manager Review Packet, Alerts/Watchlist, Source Registry, Bot Change Candidates. Borderline (open next to confirm value vs overlap): Morning Decision Board (vs pre-market stocks-in-sight), Manager Review Packet (vs Daily Review).

### 2026-06-14 — Loop 39: FINISHED Loop-37 build order

- **Cost model:** `commission_model.py` (knob: zero | ts_select | per_share_standard | stress; reg fees on sells — SEC $20.60/$1M, FINRA TAF $0.000195/sh, both pulled live 6/14). Recompute 6/08+ (53 RT, gross +$479): zero net +$479 (exp +9.04) · ts_select +$457 (+8.62) · **per_share_standard +$238 (+4.50)** · stress +$20 (+0.38). **Commission halves the edge; the live plan matters a lot.** (Recompute is a script; wiring it into /truth display = follow-up.)
- **Deploy-controller scope (APPROVED, gated):** extended `orb_runner` (9:35 main book) to call `deploy_controller.admit()` — per-position $25k / per-side 50% / 75% target now govern the main book, not just re-arm. Mirrors orb_multiscan. Verify-load: run_bot restarted PID 10184, preflight 46/47.
- **Wiring-audit → preflight (APPROVED, high-pri):** `_preflight_diagnostic.py` now runs `_wiring_audit` every check (now 47 checks). Shadow/unwired governance flags are caught automatically. 6/6 OK.
- **p0 harness (close item d):** ran `--live` for 6/11 + 6/12 → unified log == independent TS historicalorders API; broker truth VERIFIED complete.
- **Ledger:** added the permanent VERIFIED/ASSUMED/BROKEN section at the top.
- NEXT (Rhett's sequence): loop-back to Planning Claude, THEN the dashboard redundancy review (incl. the legacy Trade Review card likely redundant with Daily Review; add a date-range selector to /truth; card-by-card value/redundancy audit Morning Hub → bottom).

### 2026-06-14 — Loop 38: home visual fixes (Rhett caught them)
- Hero (3-question) cards weren't in the shared content-width rule -> didn't align with the status row; added `.cmd3` to it + shrank (compact padding/fonts).
- Removed 11 home cards that opened RETIRED stub pages (Market Intelligence, Morning Readiness, Session Summary, ChatGPT Handoff, Action Center, Post-Market Debrief, Strategy Learning, Review History, Trend Dashboard, Root Cause, Daily Operating Workflow). Home now shows only working surfaces; verified 0 retired links remain.
- Cost-rate fetch (Loop 37): got SEC Section 31 = \$20.60/\$1M (eff 4/4/2026); FINRA TAF rate still to pull.
- **STILL QUEUED (Loop 37 build order):** cost model + recompute, deploy-controller scope extension, wire `_wiring_audit.py` into preflight, run p0_verify_harness on 6/11+6/12, add VERIFIED/ASSUMED/BROKEN ledger.

### 2026-06-14 — Loop 36: foundation audit (Planning Claude handoff a–f) + cost status

**FOUNDATION AUDIT (verified against code/data):**
- **(a) candle-close exit — VERIFIED.** Deployed 6/10 5:22 PM (commit d3f7e05, behind ORB_EXIT_MODE). `candle_close_exit.py` matches spec exactly: PHASE1_ATR 0.15 hard stop → CONFIRM_ATR 0.15 → phase-2 first opposite-color 1-min candle close → CATASTROPHE_ATR 1.0. 6/11+6/12 ran on it.
- **(b) multi-scan — VERIFIED; deploy-controller — BROKEN (scope).** orb_multiscan builds a FRESH 5-min range per window (10:35–14:35), tags ORBMS<window>, capped by MAX_DAY_TRADE_GROSS. deploy_controller.admit() DOES enforce 75% target / per-side 50% / per-position $25k — but is only called from orb_multiscan (re-arm), NOT orb_runner (9:35 main book). So the caps don't govern the bulk of entries (Loop 35).
- **(c) freeze blast radius — VERIFIED clean.** 6/12 froze 8:04 AM pre-market, recovered before the 9:30 open; 6/12 = 24 fills / 12 round-trips (complete), 0 duplicate fills, no stuck orders tied to the freeze. 6/11 had no pre-market freeze.
- **(d) broker-truth completeness — UNVERIFIED (partial).** Internally consistent: sane per-day counts (6/08 14F, 6/09 14F/10U, 6/10 24F, 6/11 30F, 6/12 24F), 0 duplicate fills. But NOT independently cross-checked (p0_verify_harness / TS historicalorders not run for 6/11–6/12). Assumed-complete, not proven.
- **(e) analytics audit — 1 BROKEN, 2 OK.** R-multiple: BROKEN — daily-review used 0.10×ATR denom for ORB while the live stop + /truth use 0.15 → overstated R ~1.5× and disagreed with /truth. **FIXED (0.10→0.15).** slippage: OK (guarded; null pre-6/08 when intended_price absent). left-on-table: OK (MFE fixed Loop ~31; after-exit = eod_hold − realized).
- **(f) index-ETF isolation — VERIFIED immaterial.** Only 1 index-ETF round-trip total (SPY, −$11) vs 52 single-name (+$709). SPY barely traded; index drag is not a real factor in the data.

**(#1 COST) — NOT WIRED.** broker_orders_unified.csv has NO commission/fee/cost column at all (not "null" — absent). After-cost expectancy is currently impossible. Fix needs a per-trade commission field (per-share model OR broker-export join). DECISION NEEDED: the commission model/rate (intended live schedule). This is the #1 blocker per Planning Claude.

**(Q1) IN-PLAY TAGGING — approved, NOT yet built this turn** (audit consumed the turn). Next build: tag every arm with day-RelVol, OR-RelVol@arm, intraday move%, above/below-VWAP, catalyst, index-ETF Y/N; ORB_INPLAY_GATE stays OFF.

### 2026-06-14 — Loop 35: proactive wiring audit (Rhett: "what else is broken?")

- Rhett (fair) ownership critique: he caught the shadow-edge bug; Code should have. Ran a proactive audit of the SAME class — "deployed/claimed but not actually wired into the live path."
- **FOUND (1):** `DEPLOY_CONTROLLER` (per-position $25k, per-side 50%, 75% target, conviction) is wired ONLY into `orb_multiscan.py` (re-arm), NOT `orb_runner.py` (the primary 9:35 scan). The 9:35 book sizes by its own constants and does NOT apply those caps. My "CURRENT SYSTEM STATE" claim implied global governance — corrected. Open design Q for Rhett/Planning: should the controller govern the 9:35 book too?
- **CLEARED (3, verified wired, not assumed):** candle-close exit (`exit_bot_v2` reads ORB_EXIT_MODE + calls candle_close_decision), daily-guard/kill switch (halts the scan in `orb_runner`), advisor controls (`should_block_entry` in `orb_runner`). RelVol floor also confirmed wired (but weak — see Loop 31).
- **BUILT:** `tradestation-bot/_wiring_audit.py` — asserts each governance flag is referenced in the live path it CLAIMS to govern; FAILs otherwise. Current: 5 OK / 1 FAIL (the deploy controller). This makes the shadow/unwired class machine-catchable. TODO: call it from `_preflight_diagnostic.py` so it runs every check.
- Honest scope: this audited the flag-WIRING class only. Other classes still to sweep (data integrity, risk-guard enforcement values, dashboard accuracy). Standing discipline added to memory: proactively audit; don't wait for Rhett to find it.

### 2026-06-14 — Loop 34: loop-back handoff to Planning Claude
- Wrote a Code→app recap handoff (strategy: ORB-edge audit + in-play gate proposal parked + multi-scan kept ON + exit/re-entry paused; dashboard: 3-question home, single health lights, legacy pages retired, light theme + Home button everywhere, broker-truth sourced). Delivered as a copiable block for Rhett to paste to the app.

### 2026-06-14 — Loop 33: decision — keep multi-scan + deploy ON

- Rhett: **leave them** — `ORB_MULTISCAN` + `DEPLOY_CONTROLLER` stay LIVE. No flag change. Rationale: SIM-only (no money risk), and the data is still useful (it characterizes ORB behavior/utilization even on the current S&P universe; diverse trade generation is the success metric). The in-play entry-gate is a separate forward build (PROP-INPLAY-ENTRY-GATE) that doesn't require reverting these first.
- Still paused: exit-redesign A/B, re-entry tagging A/B (tuning execution before the in-play core is premature). The in-play gate proposal stays parked pending human approval.

### 2026-06-14 — Loop 32: in-play entry-gate proposal (handoff D)

- Wrote **`outputs/proposals/PROP-INPLAY-ENTRY-GATE-2026-06-14.md`** (INACTIVE, needs human approval): make in-play selection GATE live ORB entries instead of running in shadow. Structure: day-RelVol floor (~≥2.0, the key knob), in-play move band (~1.5–8%, exclude blow-offs via the exhaustion guard), keep price/spread/ATR floors, EXCLUDE index ETFs (SPY/QQQ/IWM/DIA), catalyst as soft bonus. Fed from the scanner's per-symbol data. Flag `ORB_INPLAY_GATE=OFF`; tag every entry (gate pass/fail, relvol@arm, move@arm) → A/B in SIM, costs subtracted, gauntlet. NOT "trade the top % movers" (exhausted).
- **PAUSED (per Planning Claude):** exit-redesign A/B, re-entry tagging A/B, multi-scan expansion, 75%-deploy push — premature until ORB-on-in-play is traded + measured.
- **OPEN DECISION for Rhett:** `ORB_MULTISCAN` + `DEPLOY_CONTROLLER` are currently LIVE (Loop 30). They amplify the unproven (non-in-play) universe. Recommend reverting to baseline (single 9:35 scan, conservative deploy) until the in-play gate is in — but flipping live flags is the human's gate, so holding for Rhett's call.
- A/B/C were completed Loop 31 (handoff re-sent before the app saw the reply; it had read the cached /main/ URL). Log was already current; B/C evidence backfilled Loop 31.

### 2026-06-14 — Loop 31: ORB-edge audit (Planning Claude handoff B+C)

**CRITICAL FINDING — the live ORB is NOT trading the mover/RelVol edge.** Confirmed from the bot code (not the scanner):
- **Entry gate (quoted, `orb_runner.py`):** `MIN_REL_VOL = 1.0` (line 68); per symbol `rel_vol = compute_rel_vol(sym, or_vol); if rel_vol is None or rel_vol < MIN_REL_VOL: skip` (line 378-380). `compute_rel_vol` (`orb_data_collector.py:414`) = **today's opening-range volume ÷ the symbol's own 14-day avg OR volume.** Then candidates are sorted by rel_vol desc and the **top 20** (`TOP_N_BY_RELVOL`) that broke their opening range are armed. Other gates: ATR floor, doji/OR-quality, earnings veto, advisor block. **There is NO %-move / catalyst / market-mover / day-RelVol gate at entry.** A floor of 1.0 only means "opened at or above its own average volume" — a very weak in-play proxy that ~half the universe clears, favoring reliably-liquid large-caps.
- **Real tradable universe (`orb_universe.build_universe()`): 530 symbols** = S&P 500 + SUPPLEMENT ETFs (SPY, QQQ, IWM, DIA, ARKK), minus leveraged ETFs. NOT the 34-name core, NOT the 2296 broad tier. The 2296 broad tier is **scanner-shadow only** — never armed by ORB.
- **Why SPY trades:** SPY/QQQ/IWM/DIA are *intentionally* in SUPPLEMENT ("ETFs with ORB-like patterns"). The structural block is **leveraged-ETF-only** (`is_leveraged_etf('SPY')` = False), so plain index ETFs pass by design. Not a missing exclusion — a deliberate inclusion to revisit.
- **Headline:** the mover scanner's edge (%-move + day-RelVol + catalyst, incl. the broad tier) has been running in **SHADOW**; live entries are **ORB breakouts on the S&P-530 filtered by a weak OR-volume RelVol≥1.0, top-20** — i.e. we've been measuring **ORB-on-S&P-(mostly large-caps + index ETFs)**, not ORB-on-movers.
- **PAUSED:** exit-redesign + re-entry A/B until the universe/entry-gate decision (tuning execution on a possibly-wrong selection is premature).

**(B) Scanner candidates vs ACTUAL traded (broker truth), per real trading day — Y = was a scanner sp-pool candidate that day:**
- **6/11 (Thu): 35 candidates · 15 traded · 3 overlap.** EQT(Y) · SMCI(Y) · WY(Y) · CNP(N) · DKNG(N) · DPZ(N) · ED(N) · GD(N) · HSIC(N) · NEM(N) · PRU(N) · SNA(N) · SPY(N) · TYL(N) · VZ(N).
- **6/12 (Fri): 42 candidates · 12 traded · 2 overlap.** ADSK(Y) · NWSA(Y) · LVS(N) · NDAQ(N) · OKE(N) · RJF(N) · ROP(N) · STLD(N) · SW(N) · TRV(N) · WSM(N) · WTW(N).
- 6/09–6/10: scanner wasn't logging sp-pool candidates yet (added Loop #28), so no overlap test; trades were 7 and 12.

**Backfill (was missing from the log):** 6/12 was the FIRST live multi-scan session (ORB_MULTISCAN ON from 6/11 5:26 PM). Result: 12 closed trades, −$48 (broker truth). The bot froze pre-market 8:04 AM (watchdog restart) — root-caused + fixed (heartbeat-while-waiting on cycle steps, Loop 30). Multi-scan + deploy-controller live; capital still well under the 75% target.

### 2026-06-12 — Session: dashboard UX + coordination + strategy handoff

**Turn - Home button everywhere + kill all dark backgrounds.**
- Floating Home button added in _page (all _page pages; suppressed on home via is_home). Inline Home button on /truth, /daily-review-v2, /pre-market. Converted remaining dark pages to light theme: truth_dashboard, daily_review_page (+chat), retired-stub, trade-chart-wrap, and the TradingView chart (trade_charts) -> white/light. No #0b0e14/#0d1017/#161a25 left.

**Turn - pre-market page restyle.**
- premarket_page.py: dark->light gray (#eef3fb)+blue text; big date banner ('Data for <weekday, date> ...'); h1 36px; full width (max 1700) with long|short candidate tables side-by-side + broad full-width; bigger fonts. Kills right-side dead space.

**Turn - hero recolor + fill health-card dead space.**
- 3-question hero cards: dark -> very light gray (#f4f7fc) + blue text. Bot Health card: added 'Traded today' (broker-truth count+P&L). Advisor Health card: added live advisor output (last control run, regime read, active controls, next run) filling the dead space.

**Turn - advisor health card tidied.**
- Removed the 'Open Advisor Health report' + 'Refresh now' maintenance buttons from the advisor health card -> plain note, matching the bot card (green=fine; yellow/red=get Claude). No heavy advisor-health page existed to retire; the card was already the single light (fixed green last session). Kept it as a SEPARATE light from bot health (different systems).

**Turn - bot health page retired; home card = single health light.**
- Per Rhett: user needs one trustworthy light, not the noisy 10-check forensic page. Home Bot Health card now a noise-filtered rollup: GREEN=alive+no real 24h issue; YELLOW=alive but real freeze/restart or FAIL alert (pull Claude in); RED=offline (reads heartbeat + watchdog_supervisor.log + bot_alerts.jsonl). Retired /bot-health to a stub + removed embedded full-health section from home. Forensic checks still available to Claude via build_bot_health_check from source. Verified: card GREEN, page stubbed.

**Turn - SHIPPED freeze fix.**
- Added _run_step_with_heartbeat in run_bot.py; routed all 6 cycle steps through it (Popen+poll+10s heartbeat+180s hard-cap taskkill), mirroring _run_advisor_slot. Fixes the ~8:04 AM false 'frozen' restart. Verify-load: run_bot PID 9900 (start 08:44 > mtime 08:43), preflight 45/46 (1 benign weekend orb_daily_state FAIL). First live test = Monday 6/15 pre-market. NOTE: the 6/12 bot-health page stays RED because the freeze really happened that day (history); the fix prevents FUTURE freezes.

**Turn - bot freeze root cause (diagnosis).**
- All 'frozen' force-restarts cluster ~8:04-8:09 AM ET (6/08 froze TWICE, 6/12 once) = the pre-market warmup window. ROOT CAUSE: run_bot.py main loop beats the heartbeat only ONCE per cycle (line 550), then runs each cycle step as a blocking subprocess.run with NO per-step heartbeat (lines 555-590). The ORB runner's pre-market warmup makes many TS API calls (each up to 30s timeout); on a slow pre-market API morning the cumulative runtime exceeds the watchdog's 180s x3 (~249s) freeze threshold -> heartbeat goes stale -> false-positive 'freeze' force-restart. The advisor-run + earnings-refresh sub-steps were already hardened with heartbeat-while-waiting + hard caps; the CORE cycle steps were NOT.
- Impact: so far pre-market only (self-heals before the 9:30 open; no missed trades). BUT multiscan is now ON -> intraday re-arm/warmup steps could trip the SAME freeze DURING market hours. Escalates priority.
- Proposed fix (NOT yet applied; live core loop = gated): route cycle steps (>= orb_runner) through a _run_step_with_heartbeat wrapper mirroring _run_advisor_slot (Popen + poll + 10s heartbeat + hard-cap taskkill). Keeps heartbeat alive during slow-but-working warmup; kills a truly-hung step so the cycle continues.

**Turn — bot-health page cleanup + explain the RED.**
- Removed cross-nav button rows from EVERY page (.topbar .actions display:none) + the 'Open Trade Review For This Range' button. Fixed a 401/403 false-positive in bot_health_check (matched timestamp microseconds). EXPLAINED the bot-health RED: (1) REAL but self-healed — bot froze 8:04 AM ET (heartbeat stale 249s x3), watchdog force-restarted (restart #5, 1 crash/hr), recovered, traded 10x since; (2) FALSE POSITIVE — 'API/auth issue' was 401/403 matching timestamp microseconds [fixed]. Killed a stale 7:57 AM dashboard server holding port 8765.

**Turn — green status pill.**
- The health-indicator GREEN badge (dot+text+bg) was styled blue (#1f5d91); fixed tone-positive to real green (#1e7a43). Yellow/red/gray tones already correct, so the pill tracks status.

**Turn — health-card button color (aesthetic).**
- Buttons in Bot Health + Advisor Health cards now match the card status color (green) instead of the default blue accent: `.health-green/.health-yellow/.health-red .link-button`. Commit `1480031`.

**Turn — advisor health always-YELLOW root-caused -> GREEN.**
- 3 stacked false-positives: (1) sync verdict POSSIBLY_STALE on every local edit (benign on single VPS -> ALIGNED on canonical root); (2) 'expired access token' (auto-refreshes -> only missing/unreadable cache warns); (3) 'git unavailable' was a real bug — collect_git_metadata checked for .git in the advisor SUBFOLDER but the repo root is parent C:\AlphaQuant; let git walk up. Now GREEN, 0 warnings. Files: session_sync.py, advisor_health.py.

**Turn — Market&activity card layout fix.**
- The 3 mini-cards were side-by-side with dead space (base .bn-cells repeat(4,1fr) overrode my rule). Used higher-specificity .status-group-card .bn-cells (flex column, flex:1 cells) to stack them vertically and split the card height evenly. Also fixed a format-string break ('1fr' in single braces in a CSS comment crashed server startup).

**Turn — home top row restructure.**
- Dropped the top status-strip BOT tile (home); folded MARKET/ADVISOR/TRADES into a grouped 'Market & activity' card as row slot 3; Review far right; 4 equal symmetric columns. Fixed .health-green (was light-blue #bdd4ea -> real green) + red/yellow. Bot Health card now shows a config value block (account/exit/re-arm+next window/deploy target) so no dead space. Other pages keep the full banner.

**Turn — home status row reorder (Rhett's UX pass).**
- Bot Health card now reads the LIVE heartbeat → GREEN "the bot is alive" (was GRAY "no cached check" because it read a cached archived review, not the heartbeat). Moved to far LEFT (1st); Advisor Health 2nd; Workflow 3rd; Review far RIGHT; row fills 4 equal columns (was a wide first card).
- Explained colors: Advisor YELLOW = benign POSSIBLY_STALE sync-marker drift (file metadata vs marker); not a real fault. Bot GRAY = stale-cache dependency, now fixed to live.
- Redundant "bot is alive" indicators (top status-strip BOT tile + full bot-health section): Rhett chose to LEAVE BOTH.
- Earlier this turn-block: made the coordination repo PUBLIC (Rhett's informed call) so the app Claude can read it by URL; cache-buster = commit-pinned raw URL; handoff block delivered to the app.

### 2026-06-11 — Session: capital deploy + full dashboard scrub

**Turn — re-entry/exit handoff from Planning Claude (2 changes + 2 investigations).**
- **Inv 1 (SMCI mechanism) RESOLVED:** SMCI = 9:35-armed breakout DAY stop (opened 9:36 ET, filled 12:48 ET, 663@30.14), rested ~3h. NOT multi-scan — `ORB_MULTISCAN` turned ON 5:26 PM 6/11 (after close), OFF all trading day. Narrative invented windows from fill hour; fixed `trade_analytics` to attribute 0935. New open Q: ORB entries are DAY orders with no intraday entry cutoff.
- **Inv 2 (MFE bug) FIXED:** MFE from 1-min bar highs fell below realized when exit filled above max bar high (SMCI +391<+411). Floored excursion by exit fill → MFE≥realized. Re-reviewed SMCI: MFE 411.06=realized, left-in-trade 0; real leak was $795.60 AFTER exit. Commit (analytics fix) + dashboard restarted.
- **Change 1 (re-entry):** no explicit "already-traded" exclusion existed; multi-scan re-arm already allows flat re-qualifying names (one-active-position-per-name guard only). Remaining = Nth-occurrence tagging (post-hoc from broker truth) + per-Nth post-cost expectancy. SIM.
- **Change 2 (exit redesign):** QUEUED for A/B, not default. Real 0.15×ATR intra-bar stop already exists (SMCI 29.62 UROUT proof); new = +1R scale-out + profit-adaptive ATR trail + drop candle-close + keep hard stop through trail phase. A/B behind flag, segmented green/red/flat, then gauntlet.
- Replied to Planning Claude (markdown). Updated ALPHA_QUANT_STATE.md §2. Named 5 follow-up build tasks.

**Turn — handoff to planning Claude.**
- Rhett: write a handoff to the app Claude explaining the setup, tell him to review this file before every turn (closes the gap), and have him walk Rhett through the GitHub connector.
- Delivered a copy-paste handoff block: app Claude reads SESSION_LOG.md from the repo each turn (LAST UPDATED stamp + FROM PLANNING CLAUDE inbox + latest entries), writes back via the inbox, and walks Rhett one-step-at-a-time through enabling the GitHub connector + granting access to the private repo, confirming by reading the stamp. Standing instruction also lives in the "HOW THE TWO CLAUDES COORDINATE" section above.

**Turn — two-Claude coordination protocol.**
- Rhett: the point of the repo is so the app Claude can read the file each turn without him pasting — how will each Claude know the other updated it?
- Honest answer: a repo is a shared notebook, not a notification bus; coordination is pull-based (neither AI is pinged). Added a **LAST UPDATED stamp** at the top + a **"HOW THE TWO CLAUDES COORDINATE"** section + a **"FROM PLANNING CLAUDE"** inbox. Code pulls at turn start / pushes at turn end; the app reads via the GitHub connector (required since the repo is private). `git log` + the stamp = who-touched-it-last.

**Turn — make SESSION_LOG all-encompassing + off-machine backup.**
- Rhett: is SESSION_LOG the single best file? merge in anything missing; create a repo Claude can read; back up the readme there; keep all three copies synced every turn.
- Answer: it was the best *operational* log but not all-encompassing. Enriched it with: **Canonical Docs Map**, **Architecture in Brief**, and a **Standing Decisions** log (scope / strategy-risk / working-style — the complete decision history + a place to append every change going forward).
- The "repo Claude can read" **already existed**: `github.com/Rhettduleba/alpha-quant-coordination`. Used it (no new repo). Copied SESSION_LOG.md in + pointed the repo README at it. Pushed (`337a540`).
- **Security:** flagged the repo was PUBLIC (strategy params + SIM account IDs + P&L exposed). Rhett chose private → flipped it to **PRIVATE** via the GitHub API using the cached git credential; verified (unauth API now 404).
- Sync rule updated in memory: 3 copies (canonical `C:\AlphaQuant\SESSION_LOG.md`, desktop link, repo mirror) kept current every turn.

**Turn — per-trade chat box.**
- Rhett: add a chat box under each trade's narrative so we can talk about that trade.
- Built **`src/advisor/trade_chat.py`** — `answer_trade_question(trade, day, message, history)` calls Claude with the trade's full broker-truth analytics + ALPHA_QUANT_STATE.md context; analyses the past only, no trading calls.
- Added a chat box to every trade card in `daily_review_page.py` (input + log + embedded trade-context JSON) + client JS (`sendChat`, per-card history) + CSS.
- New POST route **`/trade-chat`** in `local_dashboard.py` → `{reply}` JSON.
- Validated the **new API key** works. Verified: backend reply grounded in numbers (SMCI +$411, 1.68R, $795.60 left on table), 15 boxes render, POST round-trips. Commit `199c762`.

**Turn — final dashboard scrub (date cleanup + retire the stale tail).**
- Rhett: the dates on the buttons look out of date; do a final scrub, own it, make it all make sense and be valuable.
- Found a cluster of home-page cards frozen at **2026-04-24 / 2026-05-01** showing 7-week-old data as current (e.g. "P&L 846.71, 109 trades, Best: 2026-04-24"). Blanked those **7 manager-workflow cards** (read parked V1-pipeline artifacts that stopped regenerating).
- Retired **6 more stale/slow pages** to fast honest stubs: `market-intelligence` (9s+stale), `post-market-debrief` (**62s!**), `morning-readiness`, `trend-dashboard`, `review-history`, `daily-operating-workflow` (9s). All read the April export / phantom journal; superseded by `/daily-review-v2` + `/truth`.
- Killed the junk **"guard fired 45,164×"** counter: removed position/exposure cap noise from `near_breaches` in `trade_manager_review.py` (normal enforcement, not a breach) + defensive filter in `alerts_watchlist.py` for cached artifacts.
- Verified honest (kept): `morning-data-prep` correctly says "Freshness: stale, last built 4/24"; `tradestation-source-registry` shows source metadata dates — both doing their job, not bugs.
- **Final dashboard state: 23 pages → 12 clean/valuable, 11 honest retired-stubs, 0 slow (>5s), 0 junk counters, 0 stale-dates-shown-as-current.** Commit `49c8faf`.

**Turn — README/session-log request.**
- Rhett: I've been glitching (empty "No response requested" turns + repeated prompts). He wants a single file logging everything every turn, as a crash-recovery backup to ramp a fresh Claude, plus a desktop link and a memory rule to keep updating it.
- Created **`C:\AlphaQuant\SESSION_LOG.md`** (this file). Clarified honestly: no single turn-by-turn log existed before; CLAUDE.md = rules, STATE.md = snapshot.
- Creating a desktop shortcut to it. Adding a memory rule: update this file every turn.

**Turn — full dashboard scrub (the big one).**
- Scrubbed all ~23 dashboard pages. Finding: only `/truth` and `/daily-review-v2` were truthful; the rest showed fake `trades=0`, read the April-20 broker export, showed a junk "guard fired 45,164×" counter, or hung the browser 70s+.
- **Rebuilt the pre-market page** on LIVE data → new `src/advisor/premarket_page.py`. Shows the scanner's actual long/short candidates (from `C:\AlphaQuant\outputs\mover_scanner\scans.jsonl`) + the bot's plan + broker-truth P&L. Commit `3fe26a9`.
- **Killed the `trades=0` phantom** in the status banner (every page) → now reads broker truth ("15 closed · +$567"). Added a 3-question command hero to the home page. Commit `1a93e16`.
- **Retired 5 hanging legacy pages** (`session-summary`, `strategy-learning`, `action-center`, `root-cause`, `chatgpt-handoff`) to fast honest stubs — were 70s+ timeouts, now ~10ms. Commit `96baa6c`.
- Still-stale pages flagged, NOT yet fixed: `morning-readiness`, `trend-dashboard`, `review-history` (bodies still read the April export). Recommend folding/retiring next.

**Turn — deploy multi-scan.**
- Session was over and flat (0 positions/orders at 5:24 PM) → turned **ORB_MULTISCAN ON** for tomorrow; restarted run_bot (verify-load PID 2464, preflight 46/46). Commit `d08a69e`.

**Turn — capital changes + under-utilization finding.**
- Daily-review charts now start 10 min before entry → close; added "capital used" + "capital on table @ entry" per trade. Commit `e84203c`.
- **Key finding:** 6/11 peak capital deployment was only **34.8% of the $400k base ($139k), for ~6 minutes**, then ~5% for the rest of the day. Badly under-utilized vs the 75% target → motivated the multi-scan deploy above.

### Earlier this session (from prior context — condensed)
- Built the full daily-review pipeline (Phases 0–5): broker-truth source, per-trade analytics, TradingView charts, page+rollup, LLM narrative, dashboard route. Commits `728afe0`→`a74e20a`.
- Built `/truth` primary surface Slice 1 (truth gate + verdict). Commit `79787dc`.
- Dashboard simplification (retired legacy /trade-review, dropped Workflow card). Commit `63222f6`.
- Fixed runaway logs (50MB rotation; 64MB read cap) that were OOM-ing reviews. Commits `e4e149c`, `6d74c21`.
- Fixed dashboard false REDs (stale pre-migration OneDrive paths → C:\AlphaQuant). Commits `d6a4451`, `d1add36`(sync).
- Loops #16–#28: VWAP/edge measurement, sidelined H5, candle-close exit deploy, all-day mover scanner (two-sided, broad shadow tier), deploy controller, ORB multi-scan, security (excluded plaintext secrets from OneDrive backup). Commits `c9525c2`, `c4045be`, `5dd5c00`, `48066a5`, `2d59734`, `54f96e2`.

### Open / next
- Tomorrow 6/12: first LIVE multi-scan session — observe utilization + re-arm trades.
- Finish dashboard scrub: retire/fold `morning-readiness`, `trend-dashboard`, `review-history`.
- A true pre-open gapper scan needs a pre-market quote feed (not wired) — pre-open the page shows last-close snapshot.


## EOD SUMMARY — 2026-06-16

_Auto-generated by eod_debrief.py at 2026-06-16 8:50 PM ET · broker-truth sourced · 33 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 130 -> passed in-play gate 8 -> selected 8 -> symbols FILLED 22.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 0, refused 19 ({'deploy_refused': 18, 'already_held_or_working': 1})
- 11:35 AM: armed 0, refused 19 ({'deploy_refused': 18, 'already_held_or_working': 1})
- 12:35 PM: armed 16, refused 2 ({'slots_exhausted': 2})
- 1:35 PM: armed 6, refused 10 ({'already_held_or_working': 4, 'slots_exhausted': 6})
- 2:35 PM: armed 7, refused 10 ({'already_held_or_working': 6, 'slots_exhausted': 4})

**Incidents today:** 107 {'WARN': 107}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — a FILLED entry was not in the gate's SELECTED set.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | exit type/time/px | hold m | MFE | MAE | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | FOXA | SELLSHORT | 1 | 53.37/53.36 | -2 | 0.0 | 7.0·-2.6%·-2.6%·MID_DVOL·large·0935 | 374 | 19,960 | 53.81 | yes | synthetic-exit/9:52AM/52.99 | 16 | 0.59 | 0.71 | 142.12 | 7.48 | 134.64 | 0.83 | 957596365/957607860 |
| 2 | FOX | SELLSHORT | 1 | 48.77/48.75 | -4 | 0.0 | 5.0·-2.4%·-2.5%·SMALL_DVOL·large·0935 | 410 | 19,996 | 49.15 | yes | synthetic-exit/9:54AM/48.29 | 18 | 0.69 | 0.81 | 196.80 | 8.20 | 188.60 | 1.20 | 957596371/957609245 |
| 3 | FISV | BUY | 1 | 49.05/49.03 | 4 | 0.0 | 4.0·2.3%·2.3%·MID_DVOL·large·0935 | 407 | 19,963 | 48.69 | no | synthetic-exit/9:36AM/48.66 | 1 | 0.04 | 0.32 | -158.73 | 8.14 | -166.87 | -1.13 | 957596376/957596836 |
| 4 | YUM | BUY | 1 | 159.99/160.00 | -1 | 0.0 | 2.3·3.7%·3.6%·MID_DVOL·large·0935 | 125 | 19,999 | 159.50 | no | synthetic-exit/9:38AM/159.14 | 3 | 0.25 | 1.70 | -106.25 | 2.50 | -108.75 | -1.78 | 957596379/957597915 |
| 5 | GME | SELLSHORT | 1 | 21.30/21.31 | 5 | 0.0 | 2.1·-2.1%·-2.2%·MID_DVOL·mid·0935 | 938 | 19,979 | 21.41 | no | synthetic-exit/9:41AM/21.41 | 5 | 0.03 | 0.20 | -103.18 | 15.26 | -118.44 | -1.12 | 957596382/957600276 |
| 6 | VLO | SELLSHORT | 1 | 241.20/241.25 | 2 | 0.0 | 2.0·-6.7%·-6.8%·LARGE_DVOL·large·0935 | 82 | 19,778 | 242.57 | no | synthetic-exit/9:36AM/242.48 | 1 | 0.20 | 2.55 | -104.96 | 2.00 | -106.96 | -0.95 | 957596409/957596837 |
| 7 | IRM | BUY | 1 | 129.70/129.64 | 5 | 0.0 | 2.0·2.7%·2.6%·MID_DVOL·large·0935 | 154 | 19,974 | 129.17 | yes | synthetic-exit/9:41AM/129.45 | 5 | 1.00 | 0.84 | -38.50 | 3.08 | -41.58 | -0.51 | 957596391/957600309 |
| 8 | EW | BUY | 1 | 89.54/89.52 | 2 | 0.0 | re-arm (ctx in trace) | 223 | 19,967 | NOT-logged | n/a | synthetic-exit/12:55PM/89.11 | 20 | 0.04 | 0.41 | -95.89 | 4.46 | -100.35 | — | 957698096/957704460 |
| 9 | MRNA | BUY | 1 | 55.60/55.62 | -4 | 0.0 | re-arm (ctx in trace) | 359 | 19,960 | NOT-logged | n/a | synthetic-exit/1:00PM/56.69 | 25 | 1.18 | 0.49 | 391.31 | 7.18 | 384.13 | — | 957698106/957705805 |
| 10 | CBOE | SELLSHORT | 1 | 273.76/273.81 | 2 | 0.0 | re-arm (ctx in trace) | 73 | 19,984 | NOT-logged | n/a | synthetic-exit/1:28PM/271.80 | 53 | 2.20 | 2.23 | 143.08 | 2.00 | 141.08 | — | 957698099/957714883 |
| 11 | LITE | SELLSHORT | 1 | 882.55/882.83 | 3 | 0.0 | re-arm (ctx in trace) | 21 | 18,534 | NOT-logged | n/a | EOD-flatten/3:50PM/880.24 | 195 | 11.08 | 11.87 | 48.51 | 2.00 | 46.51 | — | 957698104/957767640 |
| 12 | GLW | SELLSHORT | 1 | 179.00/179.04 | 2 | 0.0 | re-arm (ctx in trace) | 111 | 19,869 | NOT-logged | n/a | synthetic-exit/3:40PM/176.45 | 185 | 2.80 | 1.42 | 283.05 | 2.22 | 280.83 | — | 957698112/957764483 |
| 13 | COHR | SELLSHORT | 1 | 389.00/389.14 | 4 | 0.0 | re-arm (ctx in trace) | 51 | 19,839 | NOT-logged | n/a | synthetic-exit/1:54PM/395.15 | 79 | 0.15 | 6.61 | -313.65 | 2.00 | -315.65 | — | 957698116/957725037 |
| 14 | EMR | BUY | 1 | 151.03/151.02 | 1 | 0.0 | re-arm (ctx in trace) | 132 | 19,936 | NOT-logged | n/a | synthetic-exit/1:37PM/150.32 | 62 | 0.19 | 0.71 | -93.72 | 2.64 | -96.36 | — | 957698113/957718281 |
| 15 | NFLX | SELLSHORT | 1 | 78.73/78.74 | 1 | 0.0 | re-arm (ctx in trace) | 254 | 19,997 | NOT-logged | n/a | synthetic-exit/1:15PM/78.50 | 40 | 0.32 | 0.36 | 58.42 | 5.08 | 53.34 | — | 957698110/957710407 |
| 16 | MU | SELLSHORT | 1 | 1045.35/1045.50 | 1 | 0.0 | re-arm (ctx in trace) | 19 | 19,862 | NOT-logged | n/a | synthetic-exit/2:37PM/1035.76 | 122 | 10.55 | 8.45 | 182.21 | 2.00 | 180.21 | — | 957698121/957741575 |
| 17 | RBLX | BUY | 1 | 48.53/48.51 | 4 | 0.0 | re-arm (ctx in trace) | 412 | 19,994 | NOT-logged | n/a | synthetic-exit/2:33PM/48.97 | 118 | 0.52 | 0.46 | 181.28 | 8.24 | 173.04 | — | 957698120/957739857 |
| 18 | WDAY | SELLSHORT | 1 | 125.58/125.63 | 4 | 0.0 | re-arm (ctx in trace) | 159 | 19,967 | NOT-logged | n/a | synthetic-exit/3:33PM/126.67 | 178 | 0.17 | 1.06 | -173.31 | 3.18 | -176.49 | — | 957698128/957761663 |
| 19 | INTC | SELLSHORT | 1 | 119.97/119.95 | -2 | 0.0 | re-arm (ctx in trace) | 166 | 19,915 | NOT-logged | n/a | synthetic-exit/3:18PM/118.45 | 163 | 1.75 | 1.15 | 251.49 | 3.32 | 248.17 | — | 957698133/957755940 |
| 20 | LUV | BUY | 1 | 47.92/47.90 | 4 | 0.0 | re-arm (ctx in trace) | 417 | 19,983 | NOT-logged | n/a | synthetic-exit/1:38PM/47.67 | 63 | -0.01 | 0.47 | -104.25 | 8.34 | -112.59 | — | 957698124/957718568 |
| 21 | GME | SELLSHORT | 2 | 21.31/21.31 | -0 | 0.0 | 2.1·-2.1%·-2.2%·MID_DVOL·mid·0935 | 148 | 3,154 | 21.42 | no | synthetic-exit/1:34PM/21.22 | 59 | 0.11 | 0.10 | 13.32 | 2.96 | 10.36 | 0.62 | 957698137/957717208 |
| 22 | EW | BUY | 2 | 89.16/89.15 | 1 | 0.0 | re-arm (ctx in trace) | 223 | 19,883 | NOT-logged | n/a | synthetic-exit/3:24PM/88.74 | 110 | 0.13 | 0.40 | -93.66 | 4.46 | -98.12 | — | 957717603/957758632 |
| 23 | MRNA | BUY | 2 | 56.85/56.82 | 5 | 0.0 | re-arm (ctx in trace) | 351 | 19,954 | NOT-logged | n/a | synthetic-exit/3:15PM/56.39 | 100 | 0.94 | 0.53 | -161.46 | 7.02 | -168.48 | — | 957717602/957754379 |
| 24 | NFLX | SELLSHORT | 2 | 78.22/78.22 | -0 | -0.0 | re-arm (ctx in trace) | 254 | 19,868 | NOT-logged | n/a | synthetic-exit/1:45PM/77.96 | 10 | 0.32 | 0.16 | 66.04 | 5.08 | 60.96 | — | 957717606/957721774 |
| 25 | GME | SELLSHORT | 3 | 21.20/21.20 | -0 | 0.0 | 2.1·-2.1%·-2.2%·MID_DVOL·mid·0935 | 163 | 3,456 | 21.31 | no | synthetic-exit/2:28PM/21.31 | 53 | 0.07 | 0.10 | -17.93 | 3.26 | -21.19 | -1.15 | 957717615/957737953 |
| 26 | TTWO | BUY | 1 | 224.25/224.22 | 1 | 0.0 | re-arm (ctx in trace) | 89 | 19,958 | NOT-logged | n/a | synthetic-exit/2:32PM/226.57 | 57 | 2.68 | 0.80 | 206.48 | 2.00 | 204.48 | — | 957717613/957739594 |
| 27 | SOFI | BUY | 1 | 17.89/17.89 | 0 | 0.0 | re-arm (ctx in trace) | 1117 | 19,983 | NOT-logged | n/a | synthetic-exit/3:06PM/17.96 | 91 | 0.19 | 0.06 | 78.19 | 17.40 | 60.79 | — | 957717611/957750511 |
| 28 | CBOE | SELLSHORT | 2 | 266.26/266.28 | 1 | 0.0 | re-arm (ctx in trace) | 75 | 19,970 | NOT-logged | n/a | EOD-flatten/3:50PM/267.15 | 75 | 0.98 | 2.24 | -66.75 | 2.00 | -68.75 | — | 957740828/957767604 |
| 29 | NFLX | SELLSHORT | 3 | 78.17/78.17 | -0 | 0.0 | re-arm (ctx in trace) | 254 | 19,855 | NOT-logged | n/a | synthetic-exit/2:53PM/78.49 | 19 | 0.01 | 0.32 | -81.28 | 5.08 | -86.36 | — | 957740833/957746444 |
| 30 | LUV | BUY | 2 | 47.59/47.59 | 0 | 0.0 | re-arm (ctx in trace) | 419 | 19,940 | NOT-logged | n/a | EOD-flatten/3:50PM/47.46 | 75 | 0.04 | 0.17 | -54.47 | 8.38 | -62.85 | — | 957740837/957767728 |
| 31 | TTWO | BUY | 2 | 226.97/226.93 | 2 | 0.0 | re-arm (ctx in trace) | 88 | 19,973 | NOT-logged | n/a | synthetic-exit/3:08PM/225.78 | 33 | 0.53 | 1.15 | -104.72 | 2.00 | -106.72 | — | 957740835/957751224 |
| 32 | GME | SELLSHORT | 4 | 21.29/21.29 | -0 | 0.0 | 2.1·-2.1%·-2.2%·MID_DVOL·mid·0935 | 246 | 5,237 | 21.40 | no | synthetic-exit/3:47PM/21.40 | 73 | 0.08 | 0.11 | -27.06 | 4.92 | -31.98 | -1.15 | 957740843/957767029 |
| 33 | RBLX | BUY | 2 | 49.05/49.05 | 0 | 0.0 | re-arm (ctx in trace) | 407 | 19,963 | NOT-logged | n/a | synthetic-exit/3:30PM/49.46 | 55 | 0.54 | 0.28 | 166.87 | 8.14 | 158.73 | — | 957740839/957760577 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $172.02  ·  fees: $0.00
- Commission 2.83 bps + fees 0.00 bps of $608,653 notional = **2.83 bps avg cost**
- Avg entry slippage: 1.3 bps (adverse +)
- Per-trade avg cost: $5.21 (33 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=33 · win rate 45% (15W/18L)
- GROSS day P&L $509.40 · **NET day P&L $337.38**
- Gross expectancy $15.44/trade · Net expectancy $10.22/trade
- Net profit factor 1.17
- Avg win $155.06 · avg loss $-110.47
- Largest win $384.13 · largest loss $-315.65
- Long/short split: 15L / 18S

- Capital utilization: PEAK deployed: $260,515  (86.8% of $300k target)  at 12:56 (7 pos + 7 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- 3 EC703/EC704 reject(s) from the confirm-swap (now DISABLED) at ['09:39', '09:51']
- 2 'Invalid Stop Price' reject(s) (stale-level race; broker refused a chase): ['SOFI', 'SNDK']
- NO-TRADE STRETCH 9:36AM->12:35PM (179m) -- see root cause in narrative

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

---


## EOD SUMMARY — 2026-06-17

_Auto-generated by eod_debrief.py at 2026-06-17 4:50 PM ET · broker-truth sourced · 52 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 124 -> passed in-play gate 15 -> selected 34 -> symbols FILLED 31.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 14, refused 2 ({'deploy_refused': 2})
- 11:35 AM: armed 9, refused 9 ({'already_held_or_working': 4, 'slots_exhausted': 5})
- 12:35 PM: armed 7, refused 11 ({'already_held_or_working': 2, 'slots_exhausted': 9})
- 1:35 PM: armed 6, refused 9 ({'already_held_or_working': 2, 'slots_exhausted': 7})
- 2:35 PM: armed 11, refused 7 ({'already_held_or_working': 2, 'slots_exhausted': 5})

**Incidents today:** 1 {'FAIL': 1}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — an old-gate-only (new-gate-rejected) name was traded.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | JPM | BUY | 1 | 335.45/335.37 | 2 | 0.0 | 2.3·5.0%·5.0%·LARGE_DVOL·mega·0935 | 59 | 19,792 | 334.44 | no | 0.15ATR-stop/9:38AM/334.37 | 3 | 0.00 | 1.52 | -53 | -63.72 | 2.00 | -65.72 | -1.10 | 957822899/957825086 |
| 2 | CHTR | SELLSHORT | 1 | 138.10/138.06 | -3 | 0.0 | 1.2·-4.7%·-4.2%·MID_DVOL·large·1435 | 144 | 19,886 | 139.04 | no | candle-close/9:48AM/137.41 | 12 | 1.32 | 1.34 | 788 | 99.36 | 2.88 | 96.48 | 0.71 | 957822901/957832956 |
| 3 | LDOS | SELLSHORT | 1 | 108.84/108.89 | 5 | 0.0 | 2.0·-4.1%·-4.2%·MID_DVOL·large·0935 | 183 | 19,918 | 109.44 | no | 0.15ATR-stop/9:39AM/109.90 | 3 | 0.05 | 1.19 | 221 | -193.98 | 3.66 | -197.64 | -1.80 | 957822903/957825456 |
| 4 | FISV | BUY | 1 | 51.08/51.08 | 0 | 0.0 | 1.9·6.6%·6.6%·MID_DVOL·large·0935 | 391 | 19,972 | 50.72 | no | candle-close/9:57AM/51.87 | 21 | 1.02 | 0.61 | -1,208 | 308.89 | 7.82 | 301.07 | 2.12 | 957822910/957839840 |
| 5 | IQV | SELLSHORT | 1 | 173.21/173.22 | 1 | 0.0 | 2.0·-2.9%·-2.9%·MID_DVOL·large·0935 | 115 | 19,919 | 174.27 | no | 0.15ATR-stop/10:39AM/174.44 | 63 | 0.96 | 4.33 | 438 | -142.02 | 2.30 | -144.32 | -1.17 | 957822905/957868661 |
| 6 | AIZ | BUY | 1 | 265.07/264.97 | 4 | 0.0 | 1.8·2.1%·2.1%·MID_DVOL·large·0935 | 74 | 19,616 | 264.27 | no | 0.15ATR-stop/9:58AM/263.18 | 22 | 0.48 | 2.08 | -82 | -140.23 | 2.00 | -142.23 | -2.38 | 957822913/957841089 |
| 7 | JBL | BUY | 1 | 393.21/393.14 | 2 | 0.0 | 2.0·4.6%·4.6%·LARGE_DVOL·large·1135 | 50 | 19,660 | NOT-logged | n/a | 0.15ATR-stop/10:56AM/390.27 | 21 | 0.42 | 6.18 | -736 | -147.00 | 2.00 | -149.00 | — | 957866411/957880100 |
| 8 | PCAR | SELLSHORT | 1 | 120.46/120.51 | 4 | 0.0 | 1.5·-2.6%·-2.1%·MID_DVOL·large·1435 | 165 | 19,876 | NOT-logged | n/a | candle-close/10:47AM/119.87 | 12 | 0.62 | 0.16 | 417 | 97.35 | 3.30 | 94.05 | — | 957866416/957874229 |
| 9 | CVNA | SELLSHORT | 1 | 65.72/65.74 | 3 | 0.0 | 1.9·-8.6%·-8.1%·LARGE_DVOL·large·1435 | 304 | 19,979 | NOT-logged | n/a | candle-close/10:44AM/64.96 | 9 | 0.92 | 0.29 | 638 | 231.04 | 6.08 | 224.96 | — | 957866414/957871999 |
| 10 | HOOD | BUY | 1 | 102.40/102.40 | 0 | -0.0 | 2.0·12.7%·13.2%·LARGE_DVOL·large·1435 | 195 | 19,968 | NOT-logged | n/a | candle-close/10:58AM/104.54 | 23 | 2.25 | 0.68 | 123 | 417.30 | 3.90 | 413.40 | — | 957866420/957880861 |
| 11 | AVGO | BUY | 1 | 397.58/397.57 | 0 | 0.0 | 1.3·5.4%·5.3%·LARGE_DVOL·mega·1035 | 50 | 19,879 | NOT-logged | n/a | 0.15ATR-stop/1:16PM/394.64 | 161 | 2.30 | 4.78 | -86 | -147.00 | 2.00 | -149.00 | — | 957866417/957931758 |
| 12 | LOW | BUY | 1 | 226.38/226.30 | 4 | 0.0 | 2.0·1.0%·0.9%·MID_DVOL·large·1035 | 88 | 19,921 | NOT-logged | n/a | 0.15ATR-stop/10:43AM/225.56 | 8 | 0.02 | 0.77 | -731 | -72.16 | 2.00 | -74.16 | — | 957866427/957871519 |
| 13 | CME | SELLSHORT | 1 | 251.08/251.11 | 1 | 0.0 | 1.2·-4.8%·-4.8%·LARGE_DVOL·large·1235 | 78 | 19,584 | NOT-logged | n/a | 0.15ATR-stop/11:12AM/252.48 | 37 | 0.00 | 2.30 | -2 | -109.20 | 2.00 | -111.20 | — | 957866432/957888457 |
| 14 | BLDR | BUY | 1 | 81.45/81.45 | 0 | 0.0 | 1.5·4.3%·4.3%·MID_DVOL·mid·1235 | 245 | 19,955 | NOT-logged | n/a | candle-close/11:41AM/81.82 | 66 | 0.61 | 0.87 | -1,392 | 90.65 | 4.90 | 85.75 | — | 957866435/957900698 |
| 15 | HPE | BUY | 1 | 50.23/50.21 | 4 | 0.0 | 1.2·3.5%·3.4%·MID_DVOL·large·1035 | 398 | 19,992 | NOT-logged | n/a | 0.15ATR-stop/1:24PM/49.67 | 169 | 0.22 | 0.56 | -585 | -222.88 | 7.96 | -230.84 | — | 957866441/957933725 |
| 16 | RTX | BUY | 1 | 190.43/190.43 | 0 | -0.0 | 1.6·1.5%·1.4%·MID_DVOL·mega·1035 | 105 | 19,995 | NOT-logged | n/a | candle-close/11:38AM/191.36 | 63 | 1.19 | 1.63 | 126 | 97.65 | 2.10 | 95.55 | — | 957866447/957899485 |
| 17 | CMI | BUY | 1 | 729.56/729.55 | 0 | 0.0 | 1.1·3.9%·3.8%·MID_DVOL·large·1035 | 27 | 19,698 | NOT-logged | n/a | 0.15ATR-stop/2:02PM/725.00 | 207 | 2.97 | 8.51 | -200 | -123.12 | 2.00 | -125.12 | — | 957866444/957946485 |
| 18 | CHTR | SELLSHORT | 2 | 136.52/136.53 | 1 | 0.0 | 1.2·-4.7%·-4.2%·MID_DVOL·large·1435 | 146 | 19,932 | 137.46 | no | candle-close/1:13PM/135.71 | 158 | 0.93 | 1.59 | 550 | 118.26 | 2.92 | 115.34 | 0.84 | 957866449/957930872 |
| 19 | NUE | SELLSHORT | 1 | 251.63/251.68 | 2 | 0.0 | 1.1·-2.8%·-2.8%·MID_DVOL·large·1035 | 6 | 1,510 | NOT-logged | n/a | 0.15ATR-stop/10:46AM/253.47 | 11 | 0.19 | 1.62 | 5 | -11.04 | 2.00 | -13.04 | — | 957866455/957873196 |
| 20 | ADBE | SELLSHORT | 1 | 203.13/203.18 | 2 | 0.0 | 1.5·-1.7%·-1.8%·LARGE_DVOL·large·1035 | 98 | 19,907 | NOT-logged | n/a | candle-close/2:04PM/201.67 | 209 | 2.07 | 1.43 | 528 | 143.08 | 2.00 | 141.08 | — | 957866453/957947488 |
| 21 | HOOD | BUY | 2 | 107.07/107.05 | 2 | 0.0 | 2.0·12.7%·13.2%·LARGE_DVOL·large·1435 | 186 | 19,915 | NOT-logged | n/a | candle-close/12:04PM/108.15 | 29 | 1.30 | 0.62 | -554 | 200.88 | 3.72 | 197.16 | — | 957898638/957908061 |
| 22 | CVNA | SELLSHORT | 2 | 64.22/64.22 | -0 | 0.0 | 1.9·-8.6%·-8.1%·LARGE_DVOL·large·1435 | 311 | 19,972 | NOT-logged | n/a | 0.15ATR-stop/12:07PM/64.82 | 32 | 0.09 | 0.69 | 610 | -186.60 | 6.22 | -192.82 | — | 957898645/957909797 |
| 23 | META | SELLSHORT | 1 | 580.20/580.25 | 1 | 0.0 | 1.2·-4.3%·-3.8%·LARGE_DVOL·mega·1435 | 34 | 19,727 | NOT-logged | n/a | candle-close/2:04PM/577.17 | 149 | 3.75 | 1.25 | 329 | 103.02 | 2.00 | 101.02 | — | 957898650/957947528 |
| 24 | MS | BUY | 1 | 227.80/227.80 | 0 | 0.0 | 1.3·3.1%·3.1%·LARGE_DVOL·mega·1135 | 86 | 19,591 | NOT-logged | n/a | 0.15ATR-stop/2:58PM/226.86 | 203 | 0.27 | 2.19 | -151 | -80.84 | 2.00 | -82.84 | — | 957898652/957978733 |
| 25 | CME | SELLSHORT | 2 | 250.47/250.55 | 3 | 0.0 | 1.2·-4.8%·-4.8%·LARGE_DVOL·large·1235 | 79 | 19,788 | NOT-logged | n/a | candle-close/11:43AM/249.95 | 8 | 1.30 | 0.81 | -202 | 41.48 | 2.00 | 39.48 | — | 957898657/957901273 |
| 26 | RMD | SELLSHORT | 1 | 189.34/189.37 | 2 | 0.0 | 1.3·-2.3%·-2.3%·MID_DVOL·large·1135 | 104 | 19,691 | NOT-logged | n/a | candle-close/11:52AM/188.85 | 17 | 0.93 | 0.23 | 264 | 50.96 | 2.08 | 48.88 | — | 957898664/957904270 |
| 27 | PSX | SELLSHORT | 1 | 168.25/168.24 | -1 | 0.0 | 1.4·-2.1%·-2.1%·MID_DVOL·large·1135 | 117 | 19,685 | NOT-logged | n/a | candle-close/3:46PM/167.55 | 251 | 0.93 | 1.75 | 42 | 81.90 | 2.34 | 79.56 | — | 957898660/958004979 |
| 28 | PCAR | SELLSHORT | 2 | 120.66/120.61 | -4 | 0.0 | 1.5·-2.6%·-2.1%·MID_DVOL·large·1435 | 21 | 2,534 | NOT-logged | n/a | candle-close/12:19PM/120.21 | 44 | 0.53 | 0.49 | 60 | 9.45 | 2.00 | 7.45 | — | 957898666/957913473 |
| 29 | HOOD | BUY | 3 | 108.90/108.90 | 0 | 0.0 | 2.0·12.7%·13.2%·LARGE_DVOL·large·1435 | 183 | 19,929 | NOT-logged | n/a | 0.15ATR-stop/1:43PM/107.85 | 69 | 0.27 | 1.81 | -490 | -192.15 | 3.66 | -195.81 | — | 957918504/957938757 |
| 30 | CVNA | SELLSHORT | 3 | 64.61/64.62 | 2 | 0.0 | 1.9·-8.6%·-8.1%·LARGE_DVOL·large·1435 | 309 | 19,964 | NOT-logged | n/a | 0.15ATR-stop/1:34PM/65.20 | 60 | 0.34 | 0.60 | 723 | -182.31 | 6.18 | -188.49 | — | 957918506/957936551 |
| 31 | CME | SELLSHORT | 3 | 248.97/248.97 | -0 | -0.0 | 1.2·-4.8%·-4.8%·LARGE_DVOL·large·1235 | 80 | 19,918 | NOT-logged | n/a | 0.15ATR-stop/3:17PM/250.25 | 162 | 1.30 | 2.47 | -181 | -102.40 | 2.00 | -104.40 | — | 957918512/957989469 |
| 32 | BLDR | BUY | 2 | 82.30/82.28 | 2 | 0.0 | 1.5·4.3%·4.3%·MID_DVOL·mid·1235 | 243 | 19,999 | NOT-logged | n/a | 0.15ATR-stop/2:00PM/81.45 | 86 | 0.26 | 0.70 | -1,290 | -206.55 | 4.86 | -211.41 | — | 957918507/957944598 |
| 33 | CBOE | SELLSHORT | 1 | 248.95/248.56 | -16 | 0.0 | 1.2·-5.6%·-5.4%·LARGE_DVOL·large·1335 | 80 | 19,916 | NOT-logged | n/a | 0.15ATR-stop/1:20PM/251.38 | 45 | 0.39 | 2.75 | -324 | -194.40 | 2.00 | -196.40 | — | 957918510/957932664 |
| 34 | KR | SELLSHORT | 1 | 61.68/61.68 | -0 | 0.0 | 1.4·-3.5%·-2.9%·MID_DVOL·large·1435 | 324 | 19,984 | NOT-logged | n/a | candle-close/2:14PM/61.37 | 99 | 0.41 | 0.14 | -139 | 100.44 | 6.48 | 93.96 | — | 957918514/957954028 |
| 35 | NDAQ | SELLSHORT | 1 | 85.32/85.36 | 5 | 0.0 | 1.3·-6.7%·-6.2%·MID_DVOL·large·1435 | 26 | 2,218 | NOT-logged | n/a | 0.15ATR-stop/12:40PM/85.73 | 6 | -0.02 | 0.41 | 63 | -10.66 | 2.00 | -12.66 | — | 957918517/957920787 |
| 36 | CVNA | SELLSHORT | 4 | 64.90/64.93 | 5 | -0.0 | 1.9·-8.6%·-8.1%·LARGE_DVOL·large·1435 | 307 | 19,924 | NOT-logged | n/a | candle-close/2:07PM/63.77 | 32 | 1.30 | 0.51 | 281 | 345.38 | 6.14 | 339.24 | — | 957936767/957949920 |
| 37 | CBOE | SELLSHORT | 2 | 250.12/250.13 | 0 | 0.0 | 1.2·-5.6%·-5.4%·LARGE_DVOL·large·1335 | 79 | 19,759 | NOT-logged | n/a | 0.15ATR-stop/3:34PM/253.39 | 119 | 0.85 | 3.27 | -161 | -258.33 | 2.00 | -260.33 | — | 957936772/957998968 |
| 38 | NDAQ | SELLSHORT | 2 | 83.24/83.27 | 4 | -0.0 | 1.3·-6.7%·-6.2%·MID_DVOL·large·1435 | 240 | 19,978 | NOT-logged | n/a | candle-close/2:02PM/82.62 | 27 | 0.70 | 0.62 | -163 | 148.80 | 4.80 | 144.00 | — | 957936773/957945849 |
| 39 | FE | SELLSHORT | 1 | 46.47/46.46 | -2 | 0.0 | 2.2·-2.9%·-2.3%·MID_DVOL·large·1435 | 430 | 19,982 | NOT-logged | n/a | candle-close/2:03PM/46.28 | 28 | 0.25 | 0.07 | 56 | 81.70 | 8.60 | 73.10 | — | 957936769/957946906 |
| 40 | CHTR | SELLSHORT | 3 | 135.77/135.76 | -1 | 0.0 | 1.2·-4.7%·-4.2%·MID_DVOL·large·1435 | 16 | 2,172 | 136.71 | no | candle-close/2:04PM/134.67 | 29 | 1.31 | 0.48 | 44 | 17.60 | 2.00 | 15.60 | 1.04 | 957936780/957947511 |
| 41 | SOFI | BUY | 1 | 18.60/18.60 | 0 | 0.0 | 1.1·4.9%·5.1%·LARGE_DVOL·large·1335 | 1075 | 19,995 | NOT-logged | n/a | 0.15ATR-stop/2:00PM/18.45 | 25 | 0.02 | 0.16 | -1,129 | -161.25 | 16.90 | -178.15 | — | 957936775/957944657 |
| 42 | CVNA | SELLSHORT | 5 | 63.80/63.78 | -3 | 0.0 | 1.9·-8.6%·-8.1%·LARGE_DVOL·large·1435 | 313 | 19,969 | NOT-logged | n/a | candle-close/3:13PM/63.33 | 38 | 0.73 | 0.78 | 147 | 147.11 | 6.26 | 140.85 | — | 957966057/957987371 |
| 43 | HOOD | BUY | 4 | 109.31/109.30 | 1 | 0.0 | 2.0·12.7%·13.2%·LARGE_DVOL·large·1435 | 182 | 19,894 | NOT-logged | n/a | candle-close/2:54PM/109.89 | 19 | 1.42 | 0.88 | -859 | 105.56 | 3.64 | 101.92 | — | 957966053/957976291 |
| 44 | NDAQ | SELLSHORT | 3 | 83.06/83.08 | 2 | 0.0 | 1.3·-6.7%·-6.2%·MID_DVOL·large·1435 | 240 | 19,934 | NOT-logged | n/a | 0.15ATR-stop/3:41PM/83.47 | 66 | 0.29 | 0.46 | 41 | -98.40 | 4.80 | -103.20 | — | 957966061/958002541 |
| 45 | FE | SELLSHORT | 2 | 46.32/46.29 | -6 | 0.0 | 2.2·-2.9%·-2.3%·MID_DVOL·large·1435 | 432 | 20,010 | NOT-logged | n/a | candle-close/2:52PM/46.24 | 17 | 0.15 | 0.10 | 39 | 34.56 | 8.64 | 25.92 | — | 957966059/957975465 |
| 46 | META | SELLSHORT | 2 | 573.50/573.55 | 1 | 0.0 | 1.2·-4.3%·-3.8%·LARGE_DVOL·mega·1435 | 34 | 19,499 | NOT-logged | n/a | candle-close/3:23PM/570.99 | 48 | 3.67 | 2.26 | 119 | 85.34 | 2.00 | 83.34 | — | 957966073/957992657 |
| 47 | KR | SELLSHORT | 2 | 61.77/61.80 | 5 | 0.0 | 1.4·-3.5%·-2.9%·MID_DVOL·large·1435 | 323 | 19,952 | NOT-logged | n/a | 0.15ATR-stop/3:12PM/62.00 | 37 | 0.12 | 0.29 | 65 | -74.29 | 6.46 | -80.75 | — | 957966068/957986587 |
| 48 | BSX | SELLSHORT | 1 | 45.09/45.09 | -0 | 0.0 | 1.3·-3.9%·-3.3%·LARGE_DVOL·large·1435 | 442 | 19,930 | NOT-logged | n/a | candle-close/3:30PM/44.89 | 55 | 0.26 | 0.18 | -27 | 88.40 | 8.84 | 79.56 | — | 957966065/957996680 |
| 49 | CHTR | SELLSHORT | 4 | 134.91/134.96 | 4 | 0.0 | 1.2·-4.7%·-4.2%·MID_DVOL·large·1435 | 10 | 1,349 | 135.85 | no | candle-close/3:00PM/134.17 | 25 | 1.04 | 0.76 | 22 | 7.40 | 2.00 | 5.40 | 0.58 | 957966081/957980183 |
| 50 | PCAR | SELLSHORT | 3 | 117.71/117.72 | 1 | 0.0 | 1.5·-2.6%·-2.1%·MID_DVOL·large·1435 | 169 | 19,893 | NOT-logged | n/a | 0.15ATR-stop/3:02PM/118.15 | 27 | 0.00 | 0.90 | 137 | -74.36 | 3.38 | -77.74 | — | 957966077/957981419 |
| 51 | Q | BUY | 1 | 159.47/159.40 | 4 | 0.0 | 1.2·4.4%·4.9%·MID_DVOL·large·1435 | 125 | 19,934 | NOT-logged | n/a | candle-close/2:46PM/160.15 | 11 | 1.28 | 1.05 | -431 | 85.00 | 2.50 | 82.50 | — | 957966086/957972967 |
| 52 | VRT | BUY | 1 | 325.14/325.18 | -1 | 0.0 | 1.0·8.2%·8.8%·LARGE_DVOL·large·1435 | 61 | 19,834 | NOT-logged | n/a | candle-close/2:46PM/328.43 | 11 | 3.97 | 1.45 | -653 | 200.69 | 2.00 | 198.69 | — | 957966088/957972823 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $206.32  ·  fees: $0.00
- Commission 2.19 bps + fees 0.00 bps of $943,799 notional = **2.19 bps avg cost**
- Avg entry slippage: 0.8 bps (adverse +)
- Per-trade avg cost: $3.97 (52 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=52 · win rate 54% (28W/24L)
- GROSS day P&L $344.35 · **NET day P&L $138.03**
- Gross expectancy $6.62/trade · Net expectancy $2.65/trade
- Net profit factor 1.04
- Avg win $122.33 · avg loss $-136.97
- Largest win $413.40 · largest loss $-260.33
- Long/short split: 19L / 33S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=6 · win 33% · net $-152 ($-25/trade, -12.8 bps)
- PATH re-arm:      N=46 · win 57% · net $290 ($6/trade, 3.5 bps)
- OCC 1st-entry:    N=31 · win 52% · net $337 ($11/trade, 5.8 bps)
- OCC re-entry(2+): N=21 · win 57% · net $-199 ($-9/trade, -5.5 bps)
- RECONCILE: path sum $138.03 + occ sum $138.03 == day net $138.03 -> OK

- Capital utilization: PEAK deployed: $297,584  (99.2% of $300k target)  at 12:56 (9 pos + 6 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- HOOD: left $1,207 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CHTR: left $883 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CVNA#3: left $862 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CVNA: left $775 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CVNA#2: left $750 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CHTR#2: left $647 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ADBE: left $591 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- PCAR: left $579 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- IQV: left $544 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- HOOD#3: left $527 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- HOOD#2: left $480 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- RMD: left $437 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CVNA#4: left $419 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- JBL: left $387 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CME: left $375 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- META: left $373 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- LDOS: left $348 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- PCAR#3: left $303 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- AVGO: left $300 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CVNA#5: left $288 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- BLDR#2: left $253 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CMI: left $229 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- RTX: left $220 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- JPM: left $201 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- marginability shadow: 31 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

---


## EOD SUMMARY — 2026-06-18

_Auto-generated by eod_debrief.py at 2026-06-18 4:50 PM ET · broker-truth sourced · 41 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 461 -> passed in-play gate 143 -> selected 31 -> symbols FILLED 24.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 14, refused 5 ({'deploy_refused': 5})
- 11:35 AM: armed 9, refused 10 ({'already_held_or_working': 3, 'deploy_refused': 7})
- 12:35 PM: armed 10, refused 8 ({'already_held_or_working': 4, 'slots_exhausted': 4})
- 1:35 PM: armed 5, refused 12 ({'already_held_or_working': 4, 'slots_exhausted': 8})
- 2:35 PM: armed 4, refused 13 ({'already_held_or_working': 6, 'slots_exhausted': 7})

**Incidents today:** 4 {'FAIL': 4}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — an old-gate-only (new-gate-rejected) name was traded.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | WELL | SELLSHORT | 1 | 205.67/205.69 | 1 | 0.0 | 29.8·-4.0%·-4.6%·LARGE_DVOL·large·0935 | 97 | 19,950 | 206.61 | no | candle-close/9:45AM/204.78 | 9 | 1.37 | 1.47 | -192 | 86.33 | 2.00 | 84.33 | 0.92 | 958072157/958078806 |
| 2 | OMC | SELLSHORT | 1 | 73.73/73.75 | 3 | 0.0 | 3.0·-4.6%·-5.2%·MID_DVOL·large·1035 | 271 | 19,981 | 74.04 | no | 0.15ATR-stop/9:37AM/74.08 | 1 | 0.21 | 0.77 | 737 | -94.85 | 5.42 | -100.27 | -1.19 | 958072192/958073334 |
| 3 | SBAC | SELLSHORT | 1 | 190.51/190.51 | -0 | 0.0 | 27.2·-2.7%·-3.2%·MID_DVOL·large·0935 | 104 | 19,813 | 191.53 | no | candle-close/11:35AM/189.81 | 119 | 1.28 | 0.66 | 303 | 72.80 | 2.08 | 70.72 | 0.66 | 958072183/958142915 |
| 4 | VTR | SELLSHORT | 1 | 81.86/81.90 | 5 | 0.0 | 20.8·-3.2%·-3.8%·MID_DVOL·large·0935 | 243 | 19,892 | 82.23 | no | candle-close/9:56AM/81.45 | 20 | 0.57 | 0.30 | -36 | 99.63 | 4.86 | 94.77 | 1.05 | 958072197/958087446 |
| 5 | PM | SELLSHORT | 1 | 178.12/178.20 | 4 | 0.0 | 18.1·-3.2%·-3.8%·LARGE_DVOL·mega·0935 | 112 | 19,949 | 178.87 | no | 0.15ATR-stop/9:37AM/179.17 | 1 | 0.42 | 1.04 | 83 | -117.60 | 2.24 | -119.84 | -1.43 | 958072204/958073138 |
| 6 | CPT | SELLSHORT | 1 | 110.41/110.46 | 5 | 0.0 | 16.2·-2.7%·-3.3%·MID_DVOL·large·0935 | 181 | 19,984 | 110.74 | no | 0.15ATR-stop/9:41AM/110.87 | 5 | -0.04 | 0.32 | 338 | -83.26 | 3.62 | -86.88 | -1.44 | 958072216/958075653 |
| 7 | CTVA | BUY | 1 | 77.55/77.54 | 1 | 0.0 | 17.8·2.4%·1.8%·MID_DVOL·large·0935 | 256 | 19,853 | 77.29 | no | 0.15ATR-stop/10:00AM/77.19 | 25 | -0.01 | 0.78 | 353 | -92.16 | 5.12 | -97.28 | -1.45 | 958072209/958090795 |
| 8 | CCI | SELLSHORT | 1 | 85.06/85.10 | 5 | 0.0 | 15.8·-4.1%·-4.7%·MID_DVOL·large·0935 | 235 | 19,989 | 85.43 | no | candle-close/10:07AM/84.85 | 31 | 0.43 | 0.95 | 663 | 49.35 | 4.70 | 44.65 | 0.51 | 958072223/958095336 |
| 9 | ACN | SELLSHORT | 1 | 133.08/133.14 | 5 | 0.0 | 4.0·-18.6%·-19.4%·LARGE_DVOL·large·1435 | 150 | 19,962 | NOT-logged | n/a | candle-close/10:52AM/131.78 | 17 | 1.95 | 0.77 | 524 | 195.00 | 3.00 | 192.00 | — | 958115933/958124750 |
| 10 | RUM | BUY | 1 | 7.34/7.34 | 0 | 0.0 | 4.5·1.9%·1.1%·SMALL_DVOL·mid·1235 | 2724 | 19,994 | NOT-logged | n/a | candle-close/11:02AM/7.40 | 27 | 0.15 | 0.11 | -218 | 163.44 | 36.69 | 126.75 | — | 958115939/958129481 |
| 11 | TTWO | BUY | 1 | 237.69/237.67 | 1 | 0.0 | 2.0·5.5%·4.7%·LARGE_DVOL·large·1435 | 84 | 19,966 | NOT-logged | n/a | 0.15ATR-stop/10:47AM/236.33 | 12 | 0.38 | 1.31 | 265 | -114.24 | 2.00 | -116.24 | — | 958115940/958122185 |
| 12 | OMC | SELLSHORT | 2 | 71.91/71.92 | 1 | 0.0 | 3.0·-4.6%·-5.2%·MID_DVOL·large·1035 | 277 | 19,919 | 72.22 | no | candle-close/3:49PM/71.32 | 314 | 0.89 | 1.82 | -11 | 163.43 | 5.54 | 157.89 | 1.83 | 958115943/958226265 |
| 13 | INTC | BUY | 1 | 129.94/129.94 | 0 | 0.0 | 1.7·10.4%·9.5%·LARGE_DVOL·mega·1335 | 153 | 19,881 | NOT-logged | n/a | candle-close/11:13AM/132.02 | 38 | 2.63 | 0.60 | 288 | 318.24 | 3.06 | 315.18 | — | 958115953/958134180 |
| 14 | IRM | BUY | 1 | 128.38/128.32 | 5 | 0.0 | 3.4·2.0%·1.4%·MID_DVOL·large·1035 | 155 | 19,899 | NOT-logged | n/a | candle-close/12:13PM/128.81 | 98 | 0.67 | 0.42 | -163 | 66.65 | 3.10 | 63.55 | — | 958115965/958158764 |
| 15 | SHW | BUY | 1 | 320.60/320.58 | 1 | 0.0 | 3.5·2.1%·1.4%·LARGE_DVOL·large·1035 | 62 | 19,877 | NOT-logged | n/a | candle-close/10:58AM/321.19 | 23 | 1.61 | 0.66 | -9 | 36.58 | 2.00 | 34.58 | — | 958115961/958127610 |
| 16 | STLD | SELLSHORT | 1 | 253.90/254.00 | 4 | 0.0 | 2.2·-7.2%·-8.0%·MID_DVOL·large·1235 | 78 | 19,804 | NOT-logged | n/a | candle-close/11:16AM/252.35 | 41 | 2.49 | 1.94 | 195 | 120.90 | 2.00 | 118.90 | — | 958115956/958135601 |
| 17 | QCOM | BUY | 1 | 224.14/224.15 | -0 | 0.0 | 2.2·5.1%·4.5%·LARGE_DVOL·mega·1035 | 88 | 19,724 | NOT-logged | n/a | 0.15ATR-stop/11:03AM/221.41 | 28 | 2.16 | 2.90 | 410 | -240.24 | 2.00 | -242.24 | — | 958115993/958130013 |
| 18 | PFE | SELLSHORT | 1 | 25.12/25.11 | -4 | 0.0 | 2.6·-2.9%·-3.6%·LARGE_DVOL·large·1235 | 796 | 19,996 | NOT-logged | n/a | candle-close/10:49AM/25.03 | 14 | 0.13 | 0.09 | -151 | 71.64 | 13.55 | 58.09 | — | 958115983/958123201 |
| 19 | CVX | SELLSHORT | 1 | 173.36/173.37 | 1 | 0.0 | 3.0·-2.3%·-3.0%·LARGE_DVOL·mega·1035 | 9 | 1,560 | NOT-logged | n/a | candle-close/12:40PM/172.73 | 125 | 0.71 | 0.66 | -8 | 5.67 | 2.00 | 3.67 | — | 958116000/958167722 |
| 20 | ACN | SELLSHORT | 2 | 130.00/130.00 | -0 | 0.0 | 4.0·-18.6%·-19.4%·LARGE_DVOL·large·1435 | 153 | 19,890 | NOT-logged | n/a | candle-close/12:01PM/128.72 | 26 | 1.50 | 0.49 | 66 | 195.84 | 3.06 | 192.78 | — | 958142881/958153640 |
| 21 | RUM | BUY | 2 | 7.48/7.48 | 0 | 0.0 | 4.5·1.9%·1.1%·SMALL_DVOL·mid·1235 | 2673 | 19,994 | NOT-logged | n/a | 0.15ATR-stop/12:02PM/7.35 | 28 | 0.13 | 0.12 | -80 | -347.49 | 36.08 | -383.57 | — | 958142882/958154227 |
| 22 | TTWO | BUY | 2 | 237.98/237.97 | 0 | 0.0 | 2.0·5.5%·4.7%·LARGE_DVOL·large·1435 | 84 | 19,990 | NOT-logged | n/a | candle-close/11:49AM/238.89 | 14 | 1.55 | 0.45 | 50 | 76.44 | 2.00 | 74.44 | — | 958142883/958148176 |
| 23 | STLD | SELLSHORT | 2 | 252.82/252.86 | 2 | 0.0 | 2.2·-7.2%·-8.0%·MID_DVOL·large·1235 | 78 | 19,720 | NOT-logged | n/a | candle-close/12:04PM/251.73 | 30 | 1.64 | 0.74 | 147 | 85.02 | 2.00 | 83.02 | — | 958142888/958155265 |
| 24 | PFE | SELLSHORT | 2 | 25.04/25.04 | -0 | 0.0 | 2.6·-2.9%·-3.6%·LARGE_DVOL·large·1235 | 798 | 19,982 | NOT-logged | n/a | 0.15ATR-stop/11:46AM/25.11 | 11 | 0.00 | 0.08 | -88 | -55.86 | 13.58 | -69.44 | — | 958142886/958147138 |
| 25 | INTC | BUY | 2 | 132.73/132.66 | 5 | 0.0 | 1.7·10.4%·9.5%·LARGE_DVOL·mega·1335 | 150 | 19,910 | NOT-logged | n/a | candle-close/12:40PM/133.67 | 65 | 1.38 | 2.29 | 35 | 141.00 | 3.00 | 138.00 | — | 958142897/958167730 |
| 26 | CTSH | SELLSHORT | 1 | 44.16/44.18 | 5 | 0.0 | 1.7·-9.8%·-10.7%·LARGE_DVOL·large·1335 | 452 | 19,960 | NOT-logged | n/a | candle-close/11:57AM/43.90 | 22 | 0.35 | 0.14 | 104 | 117.52 | 9.04 | 108.48 | — | 958142895/958151894 |
| 27 | LMT | SELLSHORT | 1 | 509.32/509.32 | -0 | 0.0 | 1.8·-4.9%·-5.6%·LARGE_DVOL·large·1435 | 39 | 19,863 | NOT-logged | n/a | 0.15ATR-stop/12:54PM/511.00 | 79 | 1.82 | 2.75 | 5 | -65.52 | 2.00 | -67.52 | — | 958142892/958171522 |
| 28 | KR | SELLSHORT | 1 | 58.13/58.12 | -2 | 0.0 | 1.7·-7.4%·-8.2%·LARGE_DVOL·large·1235 | 336 | 19,532 | NOT-logged | n/a | candle-close/11:41AM/58.20 | 6 | 0.34 | 0.14 | 531 | -23.52 | 6.72 | -30.24 | — | 958142898/958145323 |
| 29 | ACN | SELLSHORT | 3 | 128.71/128.71 | -0 | 0.0 | 4.0·-18.6%·-19.4%·LARGE_DVOL·large·1435 | 154 | 19,821 | NOT-logged | n/a | candle-close/1:54PM/127.63 | 79 | 1.51 | 1.09 | -102 | 166.32 | 3.08 | 163.24 | — | 958166339/958189484 |
| 30 | TTWO | BUY | 3 | 241.79/241.73 | 2 | 0.0 | 2.0·5.5%·4.7%·LARGE_DVOL·large·1435 | 82 | 19,827 | NOT-logged | n/a | 0.15ATR-stop/1:51PM/240.42 | 76 | 0.36 | 2.22 | -76 | -112.34 | 2.00 | -114.34 | — | 958166343/958188656 |
| 31 | STLD | SELLSHORT | 3 | 249.88/249.84 | -2 | 0.0 | 2.2·-7.2%·-8.0%·MID_DVOL·large·1235 | 80 | 19,991 | NOT-logged | n/a | 0.15ATR-stop/3:34PM/251.57 | 179 | 0.33 | 5.75 | 138 | -134.80 | 2.00 | -136.80 | — | 958166344/958221014 |
| 32 | KR | SELLSHORT | 2 | 57.19/57.20 | 2 | 0.0 | 1.7·-7.4%·-8.2%·LARGE_DVOL·large·1235 | 348 | 19,902 | NOT-logged | n/a | candle-close/12:45PM/56.96 | 10 | 0.27 | 0.15 | 118 | 80.04 | 6.96 | 73.08 | — | 958166358/958168908 |
| 33 | MSTR | SELLSHORT | 1 | 110.80/110.80 | -0 | 0.0 | 1.8·-6.1%·-7.1%·LARGE_DVOL·large·1335 | 178 | 19,722 | NOT-logged | n/a | candle-close/1:13PM/109.46 | 38 | 1.61 | 0.66 | -532 | 238.52 | 3.56 | 234.96 | — | 958166361/958177405 |
| 34 | MSTR | SELLSHORT | 2 | 108.90/108.93 | 3 | 0.0 | 1.8·-6.1%·-7.1%·LARGE_DVOL·large·1335 | 182 | 19,820 | NOT-logged | n/a | 0.15ATR-stop/3:18PM/110.35 | 103 | 0.62 | 1.53 | -382 | -263.90 | 3.64 | -267.54 | — | 958184241/958215905 |
| 35 | INTC | BUY | 3 | 134.58/134.58 | 0 | 0.0 | 1.7·10.4%·9.5%·LARGE_DVOL·mega·1335 | 148 | 19,918 | NOT-logged | n/a | 0.15ATR-stop/3:50PM/133.09 | 135 | 0.65 | 3.03 | 120 | -220.52 | 2.96 | -223.48 | — | 958184249/958226666 |
| 36 | CTSH | SELLSHORT | 2 | 43.90/43.83 | -16 | 0.0 | 1.7·-9.8%·-10.7%·LARGE_DVOL·large·1335 | 456 | 20,018 | NOT-logged | n/a | EOD-flatten/3:50PM/43.83 | 135 | 0.19 | 0.94 | 73 | 31.92 | 9.12 | 22.80 | — | 958184246/958226706 |
| 37 | HAS | BUY | 1 | 86.03/86.03 | 0 | 0.0 | 2.1·3.0%·2.1%·MID_DVOL·large·1335 | 232 | 19,959 | NOT-logged | n/a | 0.15ATR-stop/1:56PM/85.62 | 21 | 0.14 | 0.43 | -200 | -95.12 | 4.64 | -99.76 | — | 958184252/958190024 |
| 38 | Q | BUY | 1 | 169.37/169.39 | -1 | 0.0 | 1.4·6.9%·6.2%·MID_DVOL·large·1435 | 7 | 1,186 | NOT-logged | n/a | 0.15ATR-stop/2:06PM/168.07 | 31 | 0.70 | 1.30 | 6 | -9.10 | 2.00 | -11.10 | — | 958184253/958193508 |
| 39 | ACN | SELLSHORT | 4 | 126.84/126.86 | 2 | 0.0 | 4.0·-18.6%·-19.4%·LARGE_DVOL·large·1435 | 157 | 19,914 | NOT-logged | n/a | 0.15ATR-stop/2:58PM/128.12 | 23 | 0.21 | 1.29 | -27 | -200.96 | 3.14 | -204.10 | — | 958203033/958209244 |
| 40 | LMT | SELLSHORT | 2 | 505.99/506.00 | 0 | 0.0 | 1.8·-4.9%·-5.6%·LARGE_DVOL·large·1435 | 39 | 19,734 | NOT-logged | n/a | 0.15ATR-stop/3:28PM/507.89 | 53 | 0.81 | 1.89 | -116 | -74.10 | 2.00 | -76.10 | — | 958203039/958219082 |
| 41 | Q | BUY | 2 | 167.99/167.93 | 3 | 0.0 | 1.4·6.9%·6.2%·MID_DVOL·large·1435 | 7 | 1,176 | NOT-logged | n/a | EOD-flatten/3:50PM/167.25 | 75 | 0.76 | 0.74 | 12 | -5.15 | 2.00 | -7.15 | — | 958203041/958226722 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $229.55  ·  fees: $0.00
- Commission 3.02 bps + fees 0.00 bps of $759,822 notional = **3.02 bps avg cost**
- Avg entry slippage: 0.9 bps (adverse +)
- Per-trade avg cost: $5.60 (41 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=41 · win rate 54% (22W/19L)
- GROSS day P&L $231.55 · **NET day P&L $2.00**
- Gross expectancy $5.65/trade · Net expectancy $0.05/trade
- Net profit factor 1.00
- Avg win $111.63 · avg loss $-129.15
- Largest win $315.18 · largest loss $-383.57
- Long/short split: 15L / 26S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=8 · win 50% · net $-110 ($-14/trade, -6.9 bps)
- PATH re-arm:      N=33 · win 55% · net $112 ($3/trade, 1.9 bps)
- OCC 1st-entry:    N=24 · win 58% · net $579 ($24/trade, 13.2 bps)
- OCC re-entry(2+): N=17 · win 47% · net $-577 ($-34/trade, -18.1 bps)
- RECONCILE: path sum $2.00 + occ sum $2.00 == day net $2.00 -> OK

- Capital utilization: PEAK deployed: $300,129  (100.0% of $300k target)  at 14:56 (5 pos + 11 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- 1 'Invalid Stop Price' reject(s) (stale-level race; broker refused a chase): ['CTSH']
- ACN: left $927 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- OMC: left $878 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CCI: left $712 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- QCOM: left $705 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- KR: left $632 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- RUM: left $572 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- INTC: left $491 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- TTWO: left $489 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ACN#2: left $477 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CTVA: left $476 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ACN#4: left $396 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- SBAC: left $360 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CPT: left $357 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- RUM#2: left $347 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- STLD: left $335 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ACN#3: left $313 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- STLD#2: left $287 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- MSTR: left $287 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- STLD#3: left $282 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- TTWO#2: left $274 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- PM: left $239 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- INTC#2: left $234 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- LMT: left $227 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- INTC#3: left $225 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- KR#2: left $223 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CTSH: left $221 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- marginability shadow: 24 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

---


## EOD SUMMARY — 2026-06-19

_Auto-generated by eod_debrief.py at 2026-06-19 4:50 PM ET · broker-truth sourced · 0 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 14 -> passed in-play gate 0 -> selected 14 -> symbols FILLED 0.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 14, refused 0
- 11:35 AM: armed 14, refused 0
- 12:35 PM: armed 14, refused 0
- 1:35 PM: armed 14, refused 0
- 2:35 PM: armed 14, refused 0

**Incidents today:** 65 {'FAIL': 65}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — gate_enforced is False; gate ran in SHADOW. Set ORB_INPLAY_GATE=True.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $0.00  ·  fees: $0.00
- Commission 0.00 bps + fees 0.00 bps of $1 notional = **0.00 bps avg cost**
- Avg entry slippage: n/a (adverse +)
- no trades

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- no closed round-trips today

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- none flagged by code today

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

---


## EOD SUMMARY — 2026-06-20

_Auto-generated by eod_debrief.py at 2026-06-20 4:50 PM ET · broker-truth sourced · 0 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 14 -> passed in-play gate 0 -> selected 14 -> symbols FILLED 0.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 14, refused 0
- 11:35 AM: armed 14, refused 0
- 12:35 PM: armed 14, refused 0
- 1:35 PM: armed 14, refused 0
- 2:35 PM: armed 14, refused 0

**Incidents today:** 0 (none).
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — gate_enforced is False; gate ran in SHADOW. Set ORB_INPLAY_GATE=True.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $0.00  ·  fees: $0.00
- Commission 0.00 bps + fees 0.00 bps of $1 notional = **0.00 bps avg cost**
- Avg entry slippage: n/a (adverse +)
- no trades

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- no closed round-trips today

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- none flagged by code today

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=14 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = 0.034; breakout won (R>0) 10/14 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): large=0.06 (n9), mega=-0.02 (n5)
---


## EOD SUMMARY — 2026-06-21

_Auto-generated by eod_debrief.py at 2026-06-21 4:50 PM ET · broker-truth sourced · 0 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 14 -> passed in-play gate 0 -> selected 14 -> symbols FILLED 0.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 14, refused 0
- 11:35 AM: armed 14, refused 0
- 12:35 PM: armed 14, refused 0
- 1:35 PM: armed 14, refused 0
- 2:35 PM: armed 14, refused 0

**Incidents today:** 12 {'FAIL': 12}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — gate_enforced is False; gate ran in SHADOW. Set ORB_INPLAY_GATE=True.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $0.00  ·  fees: $0.00
- Commission 0.00 bps + fees 0.00 bps of $1 notional = **0.00 bps avg cost**
- Avg entry slippage: n/a (adverse +)
- no trades

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- no closed round-trips today

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- none flagged by code today

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=14 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = 0.034; breakout won (R>0) 10/14 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): large=0.06 (n9), mega=-0.02 (n5)
---


## EOD SUMMARY — 2026-06-22

_Auto-generated by eod_debrief.py at 2026-06-22 4:17 PM ET · broker-truth sourced · 16 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 133 -> passed in-play gate 10 -> selected 25 -> symbols FILLED 16.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 5, refused 15 ({'deploy_refused': 15})
- 11:35 AM: armed 5, refused 13 ({'already_held_or_working': 3, 'reentry_capped': 3, 'deploy_refused': 7})
- 12:35 PM: armed 0, refused 20 ({'already_held_or_working': 8, 'reentry_capped': 4, 'deploy_refused': 8})
- 1:35 PM: armed 4, refused 12 ({'already_held_or_working': 4, 'reentry_capped': 4, 'slots_exhausted': 4})
- 2:35 PM: armed 2, refused 18 ({'already_held_or_working': 7, 'reentry_capped': 4, 'slots_exhausted': 7})

**Incidents today:** 117 {'FAIL': 117}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — an old-gate-only (new-gate-rejected) name was traded.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | ACN | SELLSHORT | 1 | 123.10/123.13 | 2 | 0.0 | 3.4·-3.8%·-4.0%·LARGE_DVOL·large·0935 | 162 | 19,942 | 124.54 | no | candle-close/11:12AM/120.83 | 96 | 2.77 | 2.60 | -635 | 367.74 | 3.24 | 364.50 | 1.57 | 958371234/958435413 |
| 2 | ULTA | BUY | 1 | 466.99/467.00 | -0 | 0.0 | 2.4·2.4%·2.1%·MID_DVOL·large·0935 | 42 | 19,614 | 464.67 | no | EOD-flatten/3:50PM/461.42 | 374 | 1.69 | 8.17 | 147 | -233.94 | 2.00 | -235.94 | -2.42 | 958371243/958531623 |
| 3 | TTWO | BUY | 1 | 249.75/249.75 | 0 | 0.0 | 3.4·8.6%·8.3%·LARGE_DVOL·large·0935 | 80 | 19,980 | 248.64 | no | candle-close/9:57AM/250.11 | 21 | 1.49 | 5.75 | -844 | 28.80 | 2.00 | 26.80 | 0.30 | 958371238/958388507 |
| 4 | ABBV | BUY | 1 | 228.35/228.34 | 0 | 0.0 | 2.0·5.5%·5.2%·LARGE_DVOL·mega·0935 | 87 | 19,866 | 227.50 | no | candle-close/10:56AM/229.40 | 80 | 1.52 | 3.13 | 61 | 91.35 | 2.00 | 89.35 | 1.21 | 958371249/958426544 |
| 5 | FIX | BUY | 1 | 2033.67/2033.67 | 0 | 0.0 | 1.5·3.4%·3.1%·LARGE_DVOL·large·0935 | 8 | 16,269 | 2017.76 | no | candle-close/1:32PM/2045.67 | 236 | 16.33 | 39.50 | 179 | 96.00 | 2.00 | 94.00 | 0.74 | 958371283/958488429 |
| 6 | BB | BUY | 1 | 8.99/8.99 | 0 | -0.0 | 1.6·6.9%·7.1%·MID_DVOL·mid·1035 | 265 | 2,382 | NOT-logged | n/a | EOD-flatten/3:50PM/8.78 | 315 | 0.11 | 0.27 | 5 | -55.65 | 5.30 | -60.95 | — | 958413993/958531569 |
| 7 | SMCI | BUY | 1 | 34.54/34.54 | 0 | 0.0 | 2.5·11.7%·11.9%·LARGE_DVOL·large·1035 | 579 | 19,999 | NOT-logged | n/a | candle-close/11:15AM/35.22 | 40 | 0.76 | 0.54 | 139 | 393.72 | 10.95 | 382.77 | — | 958413989/958436821 |
| 8 | GOOG | SELLSHORT | 1 | 346.73/346.74 | 0 | 0.0 | 1.1·-5.5%·-5.3%·LARGE_DVOL·mega·1035 | 18 | 6,241 | NOT-logged | n/a | candle-close/10:54AM/344.91 | 19 | 1.99 | 1.78 | -68 | 32.76 | 2.00 | 30.76 | — | 958413997/958425434 |
| 9 | RIOT | BUY | 1 | 28.91/28.90 | 3 | 0.0 | 1.3·2.6%·2.9%·MID_DVOL·large·1135 | 692 | 20,006 | NOT-logged | n/a | EOD-flatten/3:50PM/28.62 | 255 | 0.21 | 0.59 | 14 | -200.68 | 12.30 | -212.98 | — | 958446486/958531600 |
| 10 | SNDK | BUY | 1 | 2321.08/2320.00 | 5 | 0.0 | 1.0·5.0%·5.3%·LARGE_DVOL·mega·1135 | 8 | 18,569 | NOT-logged | n/a | EOD-flatten/3:50PM/2286.65 | 255 | 12.68 | 37.79 | -100 | -275.44 | 2.00 | -277.44 | — | 958446485/958531613 |
| 11 | COHR | BUY | 1 | 403.14/403.14 | 0 | 0.0 | 1.1·3.4%·3.7%·LARGE_DVOL·large·1135 | 25 | 10,078 | NOT-logged | n/a | candle-close/12:56PM/411.71 | 81 | 10.35 | 4.14 | 341 | 214.37 | 2.00 | 212.37 | — | 958446496/958478785 |
| 12 | RBLX | SELLSHORT | 1 | 46.56/46.58 | 4 | 0.0 | 1.0·-9.4%·-9.1%·MID_DVOL·large·1135 | 429 | 19,974 | NOT-logged | n/a | candle-close/1:10PM/46.10 | 95 | 0.54 | 0.76 | -523 | 197.34 | 8.58 | 188.76 | — | 958446493/958483131 |
| 13 | AIG | BUY | 1 | 76.32/76.33 | -1 | 0.0 | 1.2·2.9%·3.2%·MID_DVOL·large·1335 | 262 | 19,996 | NOT-logged | n/a | candle-close/2:56PM/76.38 | 81 | 0.98 | 0.17 | -10 | 15.72 | 5.24 | 10.48 | — | 958490265/958513504 |
| 14 | VRT | BUY | 1 | 352.32/352.22 | 3 | 0.0 | 0.8·5.6%·5.9%·LARGE_DVOL·large·1335 | 55 | 19,378 | NOT-logged | n/a | EOD-flatten/3:50PM/355.30 | 135 | 3.49 | 1.24 | 156 | 163.90 | 2.00 | 161.90 | — | 958490269/958531628 |
| 15 | PLTR | SELLSHORT | 1 | 120.62/120.65 | 2 | 0.0 | 0.8·-6.0%·-5.8%·LARGE_DVOL·mega·1435 | 165 | 19,902 | NOT-logged | n/a | candle-close/3:00PM/119.63 | 25 | 1.14 | 0.17 | 25 | 163.35 | 3.30 | 160.05 | — | 958506610/958514656 |
| 16 | NFLX | SELLSHORT | 1 | 73.19/73.19 | -0 | 0.0 | 0.8·-5.3%·-5.0%·LARGE_DVOL·mega·1435 | 30 | 2,196 | NOT-logged | n/a | candle-close/3:08PM/72.94 | 33 | 0.35 | 0.16 | 2 | 7.50 | 2.00 | 5.50 | — | 958506612/958517826 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $66.91  ·  fees: $0.00
- Commission 2.63 bps + fees 0.00 bps of $254,392 notional = **2.63 bps avg cost**
- Avg entry slippage: 1.2 bps (adverse +)
- Per-trade avg cost: $4.18 (16 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=16 · win rate 75% (12W/4L)
- GROSS day P&L $1,006.85 · **NET day P&L $939.93**
- Gross expectancy $62.93/trade · Net expectancy $58.75/trade
- Net profit factor 2.19
- Avg win $143.94 · avg loss $-196.83
- Largest win $382.77 · largest loss $-277.44
- Long/short split: 11L / 5S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=5 · win 80% · net $339 ($68/trade, 35.4 bps)
- PATH re-arm:      N=11 · win 73% · net $601 ($55/trade, 37.9 bps)
- OCC 1st-entry:    N=16 · win 75% · net $940 ($59/trade, 36.9 bps)
- OCC re-entry(2+): N=0
- RECONCILE: path sum $939.93 + occ sum $939.93 == day net $939.93 -> OK

- Capital utilization: PEAK deployed: $312,404  (104.1% of $300k target)  at 10:56 (5 pos + 12 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- 2 'Invalid Stop Price' reject(s) (stale-level race; broker refused a chase): ['SOFI', 'PLTR']
- SMCI: left $915 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- COHR: left $698 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ACN: left $434 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- AIG: left $356 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ABBV: left $254 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ULTA: left $220 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- FIX: left $213 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- NO-TRADE STRETCH 11:35AM->1:35PM (120m) -- see root cause in narrative
- marginability shadow: 16 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=25 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = -0.136; breakout won (R>0) 10/25 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): large=-0.06 (n15), mega=0.02 (n6), mid=-0.64 (n4)
---

----- alphaquant-alert-triage (scheduled) - 2026-06-22 Mon ~4:44 PM ET - **Triage: inbox CLEAN (code_alert_inbox.py --json: n_total=0, n_actionable=0, 0 critical groups). No new actionable CRITICAL alerts since last ack. State verified healthy: CSHV 16:40 run OK=44/WARN=0/FAIL=0 (all checks passing, scheduled_tasks_present back to all-8-OK post the ~4:06 PM reboot, bot heartbeat 17s fresh, book context market-closed). Nothing to escalate -- silence = handled. --ack'd.**

----- alphaquant-alert-triage (scheduled) - 2026-06-22 Mon ~4:46 PM ET - **CORRECTION/follow-up to the ~4:44 PM entry above:** the --json snapshot showed 0 actionable, but --ack then surfaced 1 CRITICAL that landed mid-run (CSHV 16:45 run): `clean_day_certified` FAIL -- "day NOT clean: failed ['no_critical_incident']; consecutive_clean reset (was building to 0)". VERIFIED + classified Bucket A (NO re-ping). Why benign/expected: (1) certifier NON-CLEAN verdict MATCHES Loop 141's documented correct conclusion ("Correct verdict = NON-CLEAN"); driven by incidents.jsonl (307 today), NOT a new bot fault -- bot_alerts.jsonl has ZERO FAILs today (all INFO; last = ORB_EOD_OK 15:55 clean flatten). (2) NO new post-reboot critical incident: only incidents after the ~4:06 PM reboot are 16:01 + 16:06 scheduled_tasks_present TIMEOUT (the pre-reboot OOM false-FAILs already escalated 2x + remediated) and the 16:45 certifier FAIL itself. (3) Certifier context confirms ZERO trading risk: trading_stopped=no/SAFE_MODE off, orders_active=no (flat: 0 working/0 positions); market closed. (4) consecutive_clean reset to 0 CORRECTS the improperly-advanced counter Loop 141 flagged (buggy CLEAN verdicts had wrongly built it to 11) -- self-correction toward the right state, not a problem. Rhett already knows today was non-clean (approved the OOM reboot; Loop 141 handoff documents it). Nothing actionable -> no notify. Already --ack'd (cursor advanced).**


## EOD SUMMARY — 2026-06-22

_Auto-generated by eod_debrief.py at 2026-06-22 4:50 PM ET · broker-truth sourced · 16 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 133 -> passed in-play gate 10 -> selected 25 -> symbols FILLED 16.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 5, refused 15 ({'deploy_refused': 15})
- 11:35 AM: armed 5, refused 13 ({'already_held_or_working': 3, 'reentry_capped': 3, 'deploy_refused': 7})
- 12:35 PM: armed 0, refused 20 ({'already_held_or_working': 8, 'reentry_capped': 4, 'deploy_refused': 8})
- 1:35 PM: armed 4, refused 12 ({'already_held_or_working': 4, 'reentry_capped': 4, 'slots_exhausted': 4})
- 2:35 PM: armed 2, refused 18 ({'already_held_or_working': 7, 'reentry_capped': 4, 'slots_exhausted': 7})

**Incidents today:** 118 {'FAIL': 118}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — an old-gate-only (new-gate-rejected) name was traded.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | ACN | SELLSHORT | 1 | 123.10/123.13 | 2 | 0.0 | 3.4·-3.8%·-4.0%·LARGE_DVOL·large·0935 | 162 | 19,942 | 124.54 | no | candle-close/11:12AM/120.83 | 96 | 2.77 | 2.60 | -635 | 367.74 | 3.24 | 364.50 | 1.57 | 958371234/958435413 |
| 2 | ULTA | BUY | 1 | 466.99/467.00 | -0 | 0.0 | 2.4·2.4%·2.1%·MID_DVOL·large·0935 | 42 | 19,614 | 464.67 | no | EOD-flatten/3:50PM/461.42 | 374 | 1.69 | 8.17 | 147 | -233.94 | 2.00 | -235.94 | -2.42 | 958371243/958531623 |
| 3 | TTWO | BUY | 1 | 249.75/249.75 | 0 | 0.0 | 3.4·8.6%·8.3%·LARGE_DVOL·large·0935 | 80 | 19,980 | 248.64 | no | candle-close/9:57AM/250.11 | 21 | 1.49 | 5.75 | -844 | 28.80 | 2.00 | 26.80 | 0.30 | 958371238/958388507 |
| 4 | ABBV | BUY | 1 | 228.35/228.34 | 0 | 0.0 | 2.0·5.5%·5.2%·LARGE_DVOL·mega·0935 | 87 | 19,866 | 227.50 | no | candle-close/10:56AM/229.40 | 80 | 1.52 | 3.13 | 61 | 91.35 | 2.00 | 89.35 | 1.21 | 958371249/958426544 |
| 5 | FIX | BUY | 1 | 2033.67/2033.67 | 0 | 0.0 | 1.5·3.4%·3.1%·LARGE_DVOL·large·0935 | 8 | 16,269 | 2017.76 | no | candle-close/1:32PM/2045.67 | 236 | 16.33 | 39.50 | 179 | 96.00 | 2.00 | 94.00 | 0.74 | 958371283/958488429 |
| 6 | BB | BUY | 1 | 8.99/8.99 | 0 | -0.0 | 1.6·6.9%·7.1%·MID_DVOL·mid·1035 | 265 | 2,382 | NOT-logged | n/a | EOD-flatten/3:50PM/8.78 | 315 | 0.11 | 0.27 | 5 | -55.65 | 5.30 | -60.95 | — | 958413993/958531569 |
| 7 | SMCI | BUY | 1 | 34.54/34.54 | 0 | 0.0 | 2.5·11.7%·11.9%·LARGE_DVOL·large·1035 | 579 | 19,999 | NOT-logged | n/a | candle-close/11:15AM/35.22 | 40 | 0.76 | 0.54 | 139 | 393.72 | 10.95 | 382.77 | — | 958413989/958436821 |
| 8 | GOOG | SELLSHORT | 1 | 346.73/346.74 | 0 | 0.0 | 1.1·-5.5%·-5.3%·LARGE_DVOL·mega·1035 | 18 | 6,241 | NOT-logged | n/a | candle-close/10:54AM/344.91 | 19 | 1.99 | 1.78 | -68 | 32.76 | 2.00 | 30.76 | — | 958413997/958425434 |
| 9 | RIOT | BUY | 1 | 28.91/28.90 | 3 | 0.0 | 1.3·2.6%·2.9%·MID_DVOL·large·1135 | 692 | 20,006 | NOT-logged | n/a | EOD-flatten/3:50PM/28.62 | 255 | 0.21 | 0.59 | 14 | -200.68 | 12.30 | -212.98 | — | 958446486/958531600 |
| 10 | SNDK | BUY | 1 | 2321.08/2320.00 | 5 | 0.0 | 1.0·5.0%·5.3%·LARGE_DVOL·mega·1135 | 8 | 18,569 | NOT-logged | n/a | EOD-flatten/3:50PM/2286.65 | 255 | 12.68 | 37.79 | -100 | -275.44 | 2.00 | -277.44 | — | 958446485/958531613 |
| 11 | COHR | BUY | 1 | 403.14/403.14 | 0 | 0.0 | 1.1·3.4%·3.7%·LARGE_DVOL·large·1135 | 25 | 10,078 | NOT-logged | n/a | candle-close/12:56PM/411.71 | 81 | 10.35 | 4.14 | 341 | 214.37 | 2.00 | 212.37 | — | 958446496/958478785 |
| 12 | RBLX | SELLSHORT | 1 | 46.56/46.58 | 4 | 0.0 | 1.0·-9.4%·-9.1%·MID_DVOL·large·1135 | 429 | 19,974 | NOT-logged | n/a | candle-close/1:10PM/46.10 | 95 | 0.54 | 0.76 | -523 | 197.34 | 8.58 | 188.76 | — | 958446493/958483131 |
| 13 | AIG | BUY | 1 | 76.32/76.33 | -1 | 0.0 | 1.2·2.9%·3.2%·MID_DVOL·large·1335 | 262 | 19,996 | NOT-logged | n/a | candle-close/2:56PM/76.38 | 81 | 0.98 | 0.17 | -10 | 15.72 | 5.24 | 10.48 | — | 958490265/958513504 |
| 14 | VRT | BUY | 1 | 352.32/352.22 | 3 | 0.0 | 0.8·5.6%·5.9%·LARGE_DVOL·large·1335 | 55 | 19,378 | NOT-logged | n/a | EOD-flatten/3:50PM/355.30 | 135 | 3.49 | 1.24 | 156 | 163.90 | 2.00 | 161.90 | — | 958490269/958531628 |
| 15 | PLTR | SELLSHORT | 1 | 120.62/120.65 | 2 | 0.0 | 0.8·-6.0%·-5.8%·LARGE_DVOL·mega·1435 | 165 | 19,902 | NOT-logged | n/a | candle-close/3:00PM/119.63 | 25 | 1.14 | 0.17 | 25 | 163.35 | 3.30 | 160.05 | — | 958506610/958514656 |
| 16 | NFLX | SELLSHORT | 1 | 73.19/73.19 | -0 | 0.0 | 0.8·-5.3%·-5.0%·LARGE_DVOL·mega·1435 | 30 | 2,196 | NOT-logged | n/a | candle-close/3:08PM/72.94 | 33 | 0.35 | 0.16 | 2 | 7.50 | 2.00 | 5.50 | — | 958506612/958517826 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $66.91  ·  fees: $0.00
- Commission 2.63 bps + fees 0.00 bps of $254,392 notional = **2.63 bps avg cost**
- Avg entry slippage: 1.2 bps (adverse +)
- Per-trade avg cost: $4.18 (16 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=16 · win rate 75% (12W/4L)
- GROSS day P&L $1,006.85 · **NET day P&L $939.93**
- Gross expectancy $62.93/trade · Net expectancy $58.75/trade
- Net profit factor 2.19
- Avg win $143.94 · avg loss $-196.83
- Largest win $382.77 · largest loss $-277.44
- Long/short split: 11L / 5S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=5 · win 80% · net $339 ($68/trade, 35.4 bps)
- PATH re-arm:      N=11 · win 73% · net $601 ($55/trade, 37.9 bps)
- OCC 1st-entry:    N=16 · win 75% · net $940 ($59/trade, 36.9 bps)
- OCC re-entry(2+): N=0
- RECONCILE: path sum $939.93 + occ sum $939.93 == day net $939.93 -> OK

- Capital utilization: PEAK deployed: $312,404  (104.1% of $300k target)  at 10:56 (5 pos + 12 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- 2 'Invalid Stop Price' reject(s) (stale-level race; broker refused a chase): ['SOFI', 'PLTR']
- SMCI: left $915 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- COHR: left $698 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ACN: left $434 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- AIG: left $356 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ABBV: left $254 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ULTA: left $220 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- FIX: left $213 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- NO-TRADE STRETCH 11:35AM->1:35PM (120m) -- see root cause in narrative
- marginability shadow: 16 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=25 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = -0.136; breakout won (R>0) 10/25 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): large=-0.06 (n15), mega=0.02 (n6), mid=-0.64 (n4)
---

---
### Turn — 2026-06-23 ~7:50 AM ET — Edge Tunes page visual polish (display-only)
- **Request:** "/edge-tunes looks crammed, no space on the sides — add ~an inch, make it look published."
- **Root cause:** edge-tunes body was NOT wrapped in any centered container, so it spanned ~full viewport (only ~14px gutter) → cramped.
- **Fix (edge_tunes_page.py, non-watched / display-only):** wrapped body in a centered `.et-wrap` (max-width 1280px, margin:0 auto, 44px side padding) for real side gutters + a published-document look. Rewrote presentation only (data logic untouched): page header + subtitle, card-framed tables (`.et-card`) with thead/tbody, uppercase column headers, zebra rows + hover, restyled caution banner, status badges, evidence styling, footer. Uses the dashboard's own design tokens (--panel/--ink/--muted/--accent-dark/--accent-soft/--line/--panel-2) — verified all 7 exist in local_dashboard :root, so on-brand (not fallbacks).
- **Verify:** py_compile OK; killed 2 dashboard procs (6344 stale --no-browser, 7680 live) → relaunched 1 clean (PID 892); GET /edge-tunes = HTTP 200, 92,981 bytes; et-wrap/et-head/et-card/et-cat/et-banner/<thead>/et-foot all PRESENT.
- **No watched strategy file touched. No trading-path change.**

---
### Turn — 2026-06-23 ~8:05 AM ET — Edge Tunes: plain-English columns + evidence cleanup
- **Request:** make "name & one-liner" plain English for a non-trader; clean up the redundant Evidence column + explain what it shows in plain English.
- **Changes (edge_tunes_page.py, display-only / non-watched):**
  - Renamed jargon headers: "Name & one-liner"→"What this is", "Evidence (joined)"→"What we actually know", "Dependencies"→"Needs first".
  - Added a "How to read this page" legend (plain-English: what a tune/status/needs-first/evidence mean; blue=test, green=change, grey=just an idea).
  - Rewrote Evidence into plain sentences via `_plain_change()` / `_plain_trial()` (+ `_fmt_money`): changes → "We made <type> on <date> — <verdict>"; trials → "<variant> — shadow test: averaged ±$X per trade over N trades; <trust>". Removed raw IDs / verdict=pending / repeated gate text. Capped each at 6 with "…and N more". Empty → "Just an idea so far — no tests run or changes made yet."
  - `_CHANGE_TYPE_PLAIN` covers all 7 real change_types (logging/instrumentation/research/display/guardrail/live_tune/shadow_test); trust derived from decision_reason (UNTRUSTED/GATE FAILED) + perm_p (<0.05 significant).
- **Verify:** py_compile OK; render-test shows correct plain output (e.g. "V1_WIDE_INIT — shadow test: averaged +$37.88 per trade over 33 trades; result not trustworthy yet"); dashboard restarted (PID 5992); GET /edge-tunes = HTTP 200, 94,151 bytes; legend + all renamed headers PRESENT.
- **Note:** the per-tune *description* text still comes verbatim from EDGE_TUNES.md (Planning-gatekept). Offered to plain-English-rewrite those one-liners pending Rhett's go.
- **No watched strategy file touched. No trading-path change.**

---
### Turn — 2026-06-23 ~9:00 AM ET — Fix "Avg entry slippage: n/a" on daily review (shadow-wiring bug)
- **Q:** why does daily review show N/A for entry slippage?
- **Root cause:** `daily_review_page.build_review()` sources trades from canonical `eod_debrief.round_trips_net()`, which DOES carry the trigger/stop price as `intended_px` (line 112; from signal_trigger_px / intended_price / order StopPrice). But the per-trade dict it built (lines 42-48) never copied `intended_px` into `trigger_price`, the field `trade_analytics.enrich_trade` reads to compute slippage (entry_px − trigger). So `entry_slippage` was always None → KPI "n/a" — on EVERY day since the Loop 106/108 canonical-source switch, not just yesterday. Data was present; it just wasn't wired through. (Classic feature+data-exist-but-unwired shadow bug per proactive-audit memory.)
- **Verify (RULE #0):** round_trips_net("2026-06-22") → 16/16 round-trips carry intended_px; bars load (390); pre-fix KPI=n/a.
- **Fix (daily_review_page.py, display/analytics — NOT a watched strategy file, no trading-path effect):** one-line passthrough `"trigger_price": rr.get("intended_px")` in the tdict.
- **Verify after:** build_review("2026-06-22") → avg_slippage=0.079, slippage_n=16 (SMCI 0.0, ACN 0.03, RBLX 0.02, VRT 0.10…). Dashboard restarted (PID 3248); GET /daily-review-v2?date=2026-06-22 = HTTP 200, 484,679 bytes, "Broker truth (16 closed trades)", KPI now "Avg entry slippage 0.079 (16 fills)".
- **Side note:** the route param is `?date=` (or `?start=`), not `?day=` (defaults to today if absent).
- **No watched strategy file touched. No trading-path change.**

---
### Turn — 2026-06-23 ~9:20 AM ET — Slippage in EOD: verified already per-day; ADDED day-over-day trend
- **Ask:** "yes, and slippage to EOD."
- **Finding (RULE #0, verified before building):** per-day entry slippage was ALREADY in the EOD debrief — Section B has a per-trade "slip bps" column and Section C has "Avg entry slippage: X bps (adverse +)", side-aware (Section B lines 497-498 flip sign for SELLSHORT). 6/22 archived debrief shows "1.2 bps". My earlier offer was made before verifying — corrected.
- **What was actually missing = the day-over-day TREND** (each archived file had its own number; nothing showed the series). Added it.
- **Changes (eod_debrief.py — reporting/debrief, NOT a watched strategy file, no trading-path effect):**
  - New `_day_slip_bps(date)`: avg entry slippage in bps, side-aware ("adverse +"), from canonical `round_trips_net` (intended_px). Same convention as Section B/C so it lines up.
  - Section C now appends: `Slippage trend (prior Nd, adverse + bps): [series] · trailing avg X bps · today Y (better/worse/in line vs trailing)`.
- **Verify:** py_compile OK; `_day_slip_bps` 6/16=1.29 / 6/17=0.78 / 6/18=0.95 / 6/22=1.21; rendered Section C for 6/22 shows trend [0.9, 2.0, -0.4, -1.1, 2.1, 2.2, 1.3, 0.8, 0.9] · trailing avg 1.0 · today 1.2 (worse vs trailing). Cheap: unified CSV is 662 rows; EOD runs once.
- **No restart needed:** EOD debrief runs as a fresh process via the `AlphaQuant_EodReconciliation` scheduled task → picks up the edit on tonight's 4:50 PM run. Did NOT regenerate the archived 6/22 file (forward-looking; no history rewrite).
- **No watched strategy file touched. No trading-path change.**

---
### Turn — 2026-06-23 ~10:00 AM ET — KPI-integrity contract (Planning Loop 148): kill the silent-null/divergent-KPI CLASS
- **Handoff:** catch the CLASS behind the slippage N/A bug (silent-null KPI on one surface + two surfaces computing the same metric divergently), so the human isn't the detector. 3 items: (1) KPI-non-null contract, (2) cross-surface reconcile, (3) single source.
- **Built (all non-watched / non-confounding; trading loop imports none):**
  1. **SINGLE SOURCE (item 3, the load-bearing fix):** new `eod_debrief.entry_slip(side, fill_px, intended_px)` — THE one slippage definition (side-aware, adverse-+, returns ($/share, bps)). `round_trips_net` now carries `entry_slip_dollars`/`entry_slip_bps`. Section B, `_day_slip_bps`, AND `build_review` all READ it; removed the two divergent calcs (eod_debrief Section B inline, trade_analytics.enrich_trade). V4 grep: only `entry_slip` computes slippage now. (Bonus: helper fixes a latent futures-short "SELL" sign bug Section B's old SELLSHORT-only flip missed.)
  2. **NON-NULL CONTRACT (item 1):** `report_integrity.kpi_completeness_violations` — INPUT-GATED (flags "intended_px present but slip null" = the wiring-gap signature), surfaced by existing `chk_report_integrity` CSHV check (cheap, canonical rows, no client). Self-test now 10/10 (added: present→clean, null-w/-intended→RED, no-trigger→no-false-FAIL).
  3. **CROSS-SURFACE RECONCILE (item 2):** extended the dashboard's existing render-time reconcile guard to assert page avg slippage == canonical (loud banner on divergence). Free; runs only at render.
- **Two principled DEVIATIONS from the handoff (flagged to Planning, not silent):**
  - Item 1 made INPUT-GATED, not "every KPI always non-null" — forcing MFE/MAE (bars-dependent) or PF (n/a on no-loser days) non-null would FALSE-FAIL clean days = CSHV-spam. The wiring-gap invariant is "input present, output null."
  - Item 2 = NO new per-5-min CSHV recompute of the dashboard side — that path (`build_review`) fetches 1-min bars per trade from TS; polling it every 5 min would hammer the API (token/API-load rule). Single-source makes divergence structurally impossible; reconcile is a free render-time guard + selftest invariant instead.
- **Verify:** 4 files py_compile OK; report_integrity self-test 10/10; [V1] planted null→2 kpi_null FAILs naming field; [V2] 6/22 round_trips_net 16/16 carry canonical slip, report_integrity ok=True; [V3] dashboard 0.079 (16 fills), slip_reconcile_ok=True, banner "avg slippage 0.079/sh"; Section C intact (1.2 bps + trend); [V4] only entry_slip computes; [V5] non-watched only. Dashboard restarted PID 1732, live /daily-review-v2?date=2026-06-22 = 200, 0.079, no mismatch banner.
- **No watched strategy file touched. No trading-path change.** Folds into the queued read-only audit as the first concrete silent-coupling instance shipped early.

---
### Alert-Triage (autonomous) - 2026-06-23 Tue ~11:00 AM ET
- code_alert_inbox.py --json: **0 actionable CRIT, 0 noise** since last ack (~10:04 AM run).
- CSHV 43 OK / 0 WARN / 0 FAIL / 1 INFO (clean_day_certified intraday rebuild). Bot loop 2714, heartbeat 17s, 6 positions reconciled both ways + monitored by exit_bot_v2, gate enforced, SAFE_MODE off, book==exposure $287,238.
- **Inbox clean -> no Rhett escalation (silence = handled).** Advanced cursor with --ack.

---
### Turn — 2026-06-23 ~11:00 AM ET — Strategy-rule + in-play compliance on EOD debrief AND dashboard
- **Ask (Rhett):** add to EOD summary + dashboard: (1) Did the bot trade exactly to the strategy rules on every trade? yes/no + why not. (2) Did the bot trade the in-play-identified symbols? yes/no + why.
- **Verified sources first (RULE #0; Explore agent's guessed exit-reason strings were WRONG):** in-play list = `orb_candidate_log.jsonl` (selected/inplay_pass/day_relvol/move/path/window); gate live (ORB_INPLAY_GATE=True); real 6/22 exit reasons = CANDLE_CLOSE_REVERSAL ×11 + "Forced EOD flatten" ×5 (classify to EXIT_CANDLE_CLOSE_TRAIL / EXIT_EOD_FLATTEN); canonical classifier `exit_reason_codes` + live gate `inplay_gate.evaluate` both reusable.
- **Built `tradestation-bot/strategy_compliance.py` (single source, no duplicated logic):** per round-trip — in-play = symbol was `selected` in the day's list; rule_ok = re-passes `inplay_gate.evaluate()` on logged inputs + occ<=ORB_MAX_ENTRIES_PER_NAME + exit classifies to a deployed code (CANDLE_CLOSE_TRAIL/EOD_FLATTEN). Re-arm-window entries flagged "ungated by design" (N/A, not failed). day_compliance() returns the two yes/no answers + exceptions. Reuses eod_debrief (round_trips + exit reasons) + inplay_gate + exit_reason_codes — imports nothing from the trading loop. Self-test 5/5.
- **Wired into BOTH surfaces (same module → answers always agree):** EOD debrief new "## A2 · STRATEGY-RULE & IN-PLAY COMPLIANCE" section (Q1/Q2 + exceptions + re-arm context + exit breakdown); dashboard daily-review compliance panel (two big YES/NO boxes + why-not list + context), computed in build_review→rollup['compliance'].
- **6/22 result:** Q1 YES (16/16), Q2 YES (16/16). Honest finding surfaced: 11/16 entries were RE-ARM entries (ungated by the in-play gate by design), several with RelVol < the 1.5 9:35 threshold — visible per-trade + in the context line.
- **Verify:** 3 files compile; self-test 5/5; EOD A2 renders YES/YES + context; dashboard restarted PID 5000, /daily-review-v2?date=2026-06-22 = 200, 485,872 bytes, panel PRESENT (YES present, no false NO). EOD picks up tonight via scheduled task (fresh process).
- **No watched strategy file touched. No trading-path change.** Read-only analytics over broker truth + logged decisions.


## EOD SUMMARY — 2026-06-23

_Auto-generated by eod_debrief.py at 2026-06-23 4:50 PM ET · broker-truth sourced · 11 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 114 -> passed in-play gate 16 -> selected 19 -> symbols FILLED 11.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 4, refused 13 ({'deploy_refused': 13})
- 11:35 AM: armed 2, refused 17 ({'reentry_capped': 2, 'already_held_or_working': 2, 'deploy_refused': 13})
- 12:35 PM: armed 0, refused 20 ({'already_held_or_working': 4, 'reentry_capped': 2, 'deploy_refused': 14})
- 1:35 PM: armed 1, refused 16 ({'reentry_capped': 3, 'already_held_or_working': 3, 'deploy_refused': 10})
- 2:35 PM: armed 2, refused 16 ({'reentry_capped': 5, 'already_held_or_working': 2, 'deploy_refused': 9})

**Incidents today:** 1 {'FAIL': 1}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — an old-gate-only (new-gate-rejected) name was traded.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## A2 · STRATEGY-RULE & IN-PLAY COMPLIANCE (did we trade to the rules?)

- **Q1 — Did the bot trade exactly to the strategy rules on every trade?**  **YES**  (11/11 trades compliant)
- **Q2 — Did the bot trade the in-play-identified symbols?**  **YES**  (11/11 in the in-play list)
- Context: 6/11 entries came from RE-ARM windows, which are UNGATED by the in-play gate by design (re-arm/fresh-breakout path) -- counted as in-play because they were on the armed list, but they did not have to clear the 9:35 RelVol/move thresholds.
- Exit-rule breakdown: EXIT_CANDLE_CLOSE_TRAIL×7, EXIT_EOD_FLATTEN×4

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | ANET | SELLSHORT | 1 | 161.24/161.20 | -2 | 0.0 | 2.3·-5.0%·-3.5%·LARGE_DVOL·mega·0935 | 124 | 19,993 | 162.58 | no | EOD-flatten/3:50PM/162.40 | 374 | 1.88 | 3.65 | 20 | -144.46 | 2.48 | -146.94 | -0.88 | 958599856/958764895 |
| 2 | DPZ | SELLSHORT | 1 | 287.31/287.33 | 1 | 0.0 | 2.1·-8.1%·-6.5%·MID_DVOL·large·0935 | 69 | 19,824 | 288.55 | no | candle-close/9:47AM/286.50 | 11 | 2.32 | 1.48 | 241 | 55.89 | 2.00 | 53.89 | 0.63 | 958599884/958610439 |
| 3 | NRG | SELLSHORT | 1 | 134.00/133.95 | -4 | 0.0 | 2.3·-3.6%·-2.0%·MID_DVOL·large·0935 | 149 | 19,966 | 134.83 | no | EOD-flatten/3:50PM/137.64 | 374 | 1.00 | 4.87 | -7 | -542.36 | 2.98 | -545.34 | -4.42 | 958599872/958764971 |
| 4 | TPR | SELLSHORT | 1 | 145.96/145.97 | 1 | 0.0 | 1.7·-2.2%·-0.6%·MID_DVOL·large·0935 | 137 | 19,996 | 146.77 | no | EOD-flatten/3:50PM/149.83 | 374 | 0.01 | 5.16 | -96 | -530.88 | 2.74 | -533.62 | -4.80 | 958599897/958765046 |
| 5 | MSTR | SELLSHORT | 1 | 105.52/105.52 | -0 | 0.0 | 1.8·-6.2%·-4.7%·LARGE_DVOL·large·0935 | 189 | 19,943 | 107.14 | no | candle-close/2:38PM/104.15 | 303 | 1.42 | 2.24 | 57 | 258.93 | 3.78 | 255.15 | 0.83 | 958599895/958737475 |
| 6 | IBM | BUY | 1 | 263.91/263.78 | 5 | -0.0 | 2.4·4.4%·5.3%·LARGE_DVOL·mega·1035 | 75 | 19,793 | NOT-logged | n/a | candle-close/11:18AM/266.03 | 43 | 3.62 | 1.41 | -81 | 159.00 | 2.00 | 157.00 | — | 958643481/958668349 |
| 7 | SNDK | SELLSHORT | 1 | 1996.01/1997.00 | 5 | 0.0 | 2.4·-11.8%·-10.9%·LARGE_DVOL·mega·1035 | 10 | 19,960 | NOT-logged | n/a | candle-close/1:53PM/1978.93 | 198 | 23.24 | 30.51 | 179 | 170.80 | 2.00 | 168.80 | — | 958643472/958724641 |
| 8 | VRT | SELLSHORT | 1 | 323.60/323.65 | 2 | 0.0 | 2.1·-9.5%·-8.6%·LARGE_DVOL·large·1035 | 42 | 13,591 | NOT-logged | n/a | candle-close/10:56AM/321.62 | 21 | 3.49 | 3.40 | 144 | 83.16 | 2.00 | 81.16 | — | 958643488/958656965 |
| 9 | IVZ | SELLSHORT | 1 | 27.30/27.30 | -0 | 0.0 | 2.8·-4.7%·-3.4%·MID_DVOL·large·1135 | 731 | 19,956 | NOT-logged | n/a | candle-close/12:39PM/27.07 | 64 | 0.30 | 0.23 | 29 | 168.13 | 12.77 | 155.36 | — | 958677487/958704574 |
| 10 | FCX | SELLSHORT | 1 | 65.06/65.07 | 2 | 0.0 | 1.1·-5.9%·-5.0%·LARGE_DVOL·large·1335 | 307 | 19,973 | NOT-logged | n/a | candle-close/2:00PM/64.60 | 25 | 0.53 | 0.15 | 64 | 141.22 | 6.14 | 135.08 | — | 958720294/958726965 |
| 11 | CAG | BUY | 1 | 13.52/13.52 | 0 | -0.0 | 1.1·5.2%·6.5%·MID_DVOL·mid·1435 | 1479 | 19,996 | NOT-logged | n/a | EOD-flatten/3:50PM/13.51 | 75 | 0.04 | 0.05 | -104 | -14.79 | 21.75 | -36.54 | — | 958736263/958764929 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $60.64  ·  fees: $0.00
- Commission 2.85 bps + fees 0.00 bps of $212,993 notional = **2.85 bps avg cost**
- Avg entry slippage: 0.8 bps (adverse +)
- Slippage trend (prior 10d, adverse + bps): [0.9, 2.0, -0.4, -1.1, 2.1, 2.2, 1.3, 0.8, 0.9, 1.2] · trailing avg 1.0 bps · today 0.8 (better vs trailing)
- Per-trade avg cost: $5.51 (11 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=11 · win rate 64% (7W/4L)
- GROSS day P&L $-195.35 · **NET day P&L $-255.99**
- Gross expectancy $-17.76/trade · Net expectancy $-23.27/trade
- Net profit factor 0.80
- Avg win $143.78 · avg loss $-315.61
- Largest win $255.15 · largest loss $-545.34
- Long/short split: 2L / 9S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=5 · win 40% · net $-917 ($-183/trade, -91.9 bps)
- PATH re-arm:      N=6 · win 83% · net $661 ($110/trade, 58.3 bps)
- OCC 1st-entry:    N=11 · win 64% · net $-256 ($-23/trade, -12.0 bps)
- OCC re-entry(2+): N=0
- RECONCILE: path sum $-255.99 + occ sum $-255.99 == day net $-255.99 -> OK

- Capital utilization: PEAK deployed: $301,815  (100.6% of $300k target)  at 12:26 (6 pos + 9 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- DPZ: left $310 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- SNDK: left $289 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- IVZ: left $278 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- VRT: left $215 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- NO-TRADE STRETCH 11:35AM->1:35PM (120m) -- see root cause in narrative
- marginability shadow: 11 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=19 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = -0.177; breakout won (R>0) 8/19 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): large=-0.23 (n14), mega=0.0 (n4), mid=-0.18 (n1)
---

---
### Turn — 2026-06-23 ~11:30 AM ET — Re-arm vs 9:35 expectancy tracker on dashboard + memory to revisit
- **Ask:** track re-arm vs 9:35 expectancy, put it on the dashboard, memory to revisit.
- **Built (strategy_compliance.py):** `_path_of(rec)` (9:35-gated / re-arm / unknown, single def); each compliance row now carries `path`+`net`+`notional`; new `path_expectancy(since=2026-05-26)` = cumulative broker-truth net split by entry path (post-baseline per [[feedback_post_5_26_data_only]]).
- **Dashboard:** new "RE-ARM vs 9:35 EXPECTANCY" panel on the daily-review page (table: path/trades/win%/net/$per-trade/bps + caveat line). Computed on render (cheap, local files).
- **FIRST READ (post-baseline 5/26→6/23, 12 days) — notable:** 9:35-gated N=50 win42% net −$1,681 (−18.9 bps) LOSING; re-arm (ungated) N=89 win58% net +$1,546 (+9.7 bps) WINNING; unknown N=76 (pre-candidate-log days, data-gap bucket). The ungated re-arm path is carrying the system — OPPOSITE of the initial concern. Context not verdict (small N; mixes pre/post the 6/19 deployed config).
- **Memory:** created `project_rearm_vs_935_expectancy.md` (+ MEMORY.md index) — REVISIT at N≥30/path on post-6/19 config; bring a proposal, don't act inline.
- **Verify:** compile OK; path_expectancy returns the split above; dashboard restarted PID 856, /daily-review-v2?date=2026-06-22 = 200, 487,823 bytes, panel PRESENT.
- **No watched strategy file touched. No trading-path change.** Observational only (stages 3-4; strategy changes still gated).

---
### Turn — 2026-06-23 ~5:25 PM ET — 6/23 EOD verify (READ/VERIFY only; freeze intact)
- **V1 CLEAN-DAY:** certify_day(6/23) = CLEAN (report_integrity 0/0, broker_flat_eod flat 11 net 0, no_critical_incident: 0 faults +1 transient soft blip tolerated). **consecutive_clean = 1** → today is clean day-1 (kill window 1/5); NOT two non-clean running. The "1 FAIL incident" = FCX at 1:45:10 PM "broker has position bot not tracking" = a 5-sec fill-vs-recon RACE (FCX stop-limit filled 1:45:05, recon snapshot 1:45:10); bot then managed+exited it (BUYTOCOVER 2:00 PM), FCX is a clean round-trip (one of 11), EOD flat, exit rule-compliant. Certifier correctly classified transient-soft. Compliance 6/23: Q1 11/11, Q2 11/11.
- **V2 SHADOW DELTA (clean day, gate PASS 11/11 → counts):** V9 (live chandelier 1.4) shadow sum +$559.88 vs V0 (0.15 baseline) −$705.84 → **V9−V0 delta +$1,265.72**. R0 reentry-shadow: 0 rows for 6/23 → N/A. **CAVEAT (verified):** V9 absolute (+560) ≠ broker-truth live (−$256) by ~$816, concentrated in NRG (+574) & ANET (+171): the recon models a confirm+candle-close early exit ~9:37–9:39 (small profit) that the LIVE bot did NOT take (exit_decisions = "chandelier_hold (unconfirmed)" 9:38 → rode to EOD-flatten, −545/−147). The faithfulness gate "11/11 reproduced" did NOT catch this net divergence (validates trade-matching, not net-vs-broker). Net effect: the +$1,266 delta is INFLATED (NRG/ANET wrongly score V9=V0=0-delta instead of the true wide-stop-hurts delta); corrected estimate ~+$800. The realized day was −$256 (V0-recon −$706 → live beats V0 by ~+$450). Wide stop helped MSTR/SNDK/VRT/IVZ (let winners run), hurt TPR (rode loser to −561 vs V0 −117). FINDING routed to Planning: harden faithfulness gate to check NET vs broker truth (measurement-path, non-trading) — did NOT act (forecast-test posture).
- **V3 OVER-DEPLOY:** capture_utilization PEAK $301,815 (100.6% of $300k) at 12:26 = 6 pos + 9 WORKING orders; peak long $126,259 / short $195,299 (both < $200k side cap). BENIGN book-drift (working-order notional inflates the book; real filled exposure + side caps under target) — same as 6/22 ($312,404). NOT an admit-cap leak. (No literal admit_log.jsonl; confirmed via capture_utilization pos/working breakdown + side caps.)
- **No code changed. Freeze intact. Run exact deployed config 6/24.**

---
### Turn — 2026-06-23 ~6:00 PM ET — Sidelined-capital report + $400k-cap display + gate-coverage (read-only)
- **Handoff:** measurement/display only — show capital idle below the $400k cap while candidates refused; reframe peak vs $400k; surface gate coverage. NO target raise / gate change / live edit (queued+frozen).
- **Sources verified (RULE #0):** no admit_log.jsonl exists; refusals + deploy-book $ live in `outputs/multiscan_trace.jsonl` (per re-arm window: book_before/after {long,short,total} + decisions w/ reasons deploy_refused / reentry_capped / already_held). Constants from live config: DEPLOY_BASE=$400k cap, DEPLOY_TARGET_PCT=0.75→$300k target, MAX_SIDE_PCT=0.5→$200k side. Refused decisions carry no order size → refused $ is an upper-bound estimate (labeled).
- **Built `tradestation-bot/sidelined_capital.py` (read-only, no trading import):** `sidelined_report(date)` → per re-arm window deployed$ / %cap / idle-vs-$400k / #refused-for-capital (split from reentry/held) / binding cap + day summary. 6/23: all 5 windows ~$300k (75% cap), ~$100k idle, binding=$300k TARGET every window, 59 capital-refusals; max idle $100,314.
- **Dashboard (daily_review_page.py, display-only):** (1) Peak KPI now "$X (Y% of $400k cap) · Z% of $300k target" + new "Idle headroom (vs $400k cap)" KPI; (2) SIDELINED CAPITAL per-window panel; (3) gate-coverage line added to the existing RE-ARM vs 9:35 EXPECTANCY panel (9:35 GATED, re-arm UNGATED). build_review stashes cap/target/idle/sidelined in rollup.
- **Verify:** compile OK; sidelined_report ties out; dashboard restarted PID 4984; /daily-review-v2?date=2026-06-23 = 200; Peak KPI renders "$301,815 (75.5% of $400k cap) · 100.6% of $300k target", Idle headroom "$98,185"; SIDELINED CAPITAL + gate-coverage panels PRESENT. (Peak uses capture_utilization intraday-MTM peak $301,815; sidelined panel uses multiscan_trace arming-book ~$300k — consistent, different snapshots.)
- **Memory:** added `project_shadow_faithfulness_net_gap.md` (+ index) — REVIEW the shadow gate net-fidelity gap after the forward test.
- **V1/V2/V3 all pass. Zero watched files. Trading loop unaffected. Target-raise + gate re-exam remain QUEUED/FROZEN.**

---
### Turn — 2026-06-23 ~6:30 PM ET — APPROVED: harden shadow faithfulness gate to reconcile vs broker truth
- **Approved mid-test** (measurement-path only, non-trading, non-watched): the shadow yardstick failed to reconcile to broker (V9 +$560 on a -$256 day, $816 inflation); fixing it is a prerequisite for kill-criterion #1, not an experiment change.
- **Root cause (item 2):** `_v9` derived `confirmed` from 1-min bar hi/lo, which fired for NRG/ANET when the live tick-based confirm never did → modeled phantom early candle-close exits. FIX: anchor V9 (the DEPLOYED exit) to BROKER TRUTH per round-trip in `replay()` (it's observed, not a hypothesis) — uses the live exit decision; V0-V8 stay modeled counterfactuals.
- **Gate (item 1):** new `reconcile_v9_vs_broker(date)` — asserts shadow V9 net == broker net per round-trip within tol (max $1.50 / 5bps); breach → FAIL naming sym+delta. Folded into the score gate (un-reconciled day not accumulated) + prints "V9->BROKER RECONCILE" line (driver now logs it).
- **CSHV (item 4):** `shadow_reconciles_broker_truth` (Reliability) — reads latest scored day in shadow_exit_results.jsonl, reconciles V9 vs broker; OK/FAIL/SKIP. Returns OK 11/11 for 6/23.
- **Re-score (item 3) — corrected (kept originally-scored V0; only V9→broker, since re-replay is non-deterministic for counterfactuals due to ATR/bar source drift — a separate reproducibility note):**
  - 6/22: V9-V0 +$2,081.55 → **+$1,988.05** (V9 $1,033→$940 broker; inflation only $93.50 — Monday's read ~96% sound).
  - 6/23: V9-V0 +$1,265.72 → **+$449.84** (V9 $560→-$256 broker; inflation $815.88 — the real problem).
  - Surgically replaced V9 in 27 accumulated rows (backup shadow_exit_results.jsonl.bak_prefix_shadowfix); V0-V8 untouched.
- **Verify:** compile OK (4 files); selftest V1 planted +$1000 mismatch → reconcile FAILs naming AAA: PASS; causality guard PASS; V9-anchored == broker (zero gap) both days (V4); reconcile 16/16 & 11/11 within tol; CSHV check OK; main() prints "V9->BROKER RECONCILE -> PASS". Also fixed a stale selftest assertion (it asserted no variant name contains 'V9', but V9 is the deployed variant since Loop 121 — had been failing).
- **V5:** non-watched files only (shadow_exit_harness never imported by the bot; system_health_verifier is monitoring); trading loop unaffected; freeze intact. shadow_exit_results.jsonl is gitignored (data).
- **Standing rule applied:** shadow now joins P&L + KPI-integrity in the daily broker-truth reconcile contract. Memory `project_shadow_faithfulness_net_gap.md` can be marked resolved (gate installed).

---
### Turn — 2026-06-24 ~8:00 AM ET — Pin shadow inputs per trade date (re-score determinism)
- **Ask (Rhett "pin it"):** fix the note-B reproducibility gap — re-scoring a past day drifted V0-V8 because `minute_bars` fetched barsback=480 from NOW + a live-mutating ATR.
- **Built (shadow_exit_harness.py, measurement-path, non-watched):** an INPUT PIN — `replay()` snapshots the exact (bars, atr) per (date, sym) to `outputs/validation/shadow_pin/<date>.json` at first SAME-DAY scoring; any re-score reads the pin → byte-identical counterfactuals. Guard: pin is WRITTEN only when date==today (a past-day fetch is already wrong, so never pinned); optional `write_pin` override for tests. PIN read path uses `_bars_from_pin` + pinned atr instead of the API.
- **Verify:** compile OK; pin roundtrip test (replay write_pin=True → replay reads pin) → per-variant per-trade nets IDENTICAL (A==B) = deterministic; test pin removed; 6/23 (past) NOT pinned (shadow_pin dir empty); main() still gate PASS + V9->BROKER RECONCILE PASS. Going forward 6/24's 4:50 same-day score writes 6/24's pin → future re-scores reproducible.
- **Scope note:** historical days scored before the pin existed (6/22, 6/23) can't be byte-reproduced (no snapshot) — but their accumulation is already corrected (V9→broker surgical; V0-V8 original) and won't be re-scored. Pinning protects 6/24+.
- **Non-watched; trading loop unaffected; freeze intact.**

---
### Turn — 2026-06-24 ~8:30 AM ET — "Versions" glossary page (read-only, self-maintaining)
- **Ask:** a dashboard "Versions" button → plain-English reference for every shadow version (V0-V9, R-series), generated FROM CODE so it stays correct as versions change.
- **Built `tradestation-bot/shadow_versions.py` (read-only, no trading import):** `registry()` reads the LIVE registries — `shadow_exit_harness.VARIANTS` (V0-V9) + `reentry_shadow.VARIANTS` (R0-R3) — and returns per-version {label, role, marker, plain-English, real params, docstring snippet}. Plain-English = a prose template authored from each variant's actual logic with the LIVE constant VALUES interpolated (param change → text auto-updates); any variant w/o a template → NEEDS DESCRIPTION (never silently missing). `undocumented()` = coverage guard. Roles: V0=BASELINE, V9=DEPLOYED-UNDER-TEST, locked=CANDIDATE(pre-registered), else CANDIDATE. Marker: V9="broker truth (observed, reproducible)", V0-V8/R="modeled counterfactual (paper)". Params = the module constants each fn's source references (auditable). Self-test 9/9 incl. self-maintaining (inject temp variant → auto-appears as NEEDS DESCRIPTION → removed).
- **Built `advisor/versions_page.py`** (centered, card-per-version, role+marker badges, params + def snippet, yellow NEEDS-DESCRIPTION cards + red banner) + wired into `local_dashboard.py`: route `/versions`, `_handle_versions`, and a "Versions" home card.
- **Verify:** 3 files compile; render_body 200/15KB with V0/V9/R3; dashboard restarted PID 592; home has /versions button+card; /versions = HTTP 200, shows "Shadow Versions", DEPLOYED-UNDER-TEST, broker-truth marker, "1.4xATR chandelier" (V9 live param), "0.15xATR from entry" (V0 live param), Re-entry section. V0/V9 read as the handoff's anchor descriptions with LIVE params.
- **Self-maintaining guard:** new/edited variant appears automatically; undocumented one shows NEEDS DESCRIPTION on the page + via `undocumented()` + fails `shadow_versions._selftest` (can be wired into preflight if desired).
- **Display-only; non-watched; no trading-path effect; freeze intact.**

---
### Turn — 2026-06-24 ~9:00 AM ET — Versions page: preflight gate + forward-test scoreboard + exit explainer
- **Wired `shadow_versions.undocumented()` into `_preflight_diagnostic.py`**: new check "every shadow version is documented on the /versions glossary" — a variant can't pass preflight undocumented. Preflight now 51/51 PASS (0 FAIL); gate input undocumented()==[].
- **ADD 1 — forward-test scoreboard (shadow_versions.forward_test_scoreboard + versions_page):** per scored day, corrected V9 (broker-anchored) vs frozen same-day V0 (modeled) + delta, worst-trade & day-net vs kill thresholds, clean flag. CORRECTNESS FIX found: excluded pre-deploy days — added `shadow_exit_harness.forward_deploy_date()` (parsed from change record AQ-20260619-...001 created_at=2026-06-19) and guarded replay()'s V9 anchor to date>=deploy (before 6/19 the LIVE exit was V0, so broker truth != V9). 6/18 now excluded; scoreboard shows 6/22 (non-clean, doesn't count) + 6/23 (clean) = **1/5 clean, cumulative V9-V0 +$449.84, live beats V0**. Kill thresholds (−$800 single / −$2,000 daily) parsed from the change record's kill_criteria (not hardcoded); none tripped. V9=broker-observed, V0=modeled (paper, ~±$600/day re-replay variance, frozen same-day not re-replayed).
- **ADD 2 — exit explainer (shadow_versions.exit_explainer, read from live code):** mode candle_1.4atr_chandelier; **candle TIMEFRAME = 1-minute** (sourced: candle_close_exit.get_last_closed_1min `interval=1&unit=Minute&barsback=5`, bars[-2]=last closed; exit_bot_v2.py:356/500 calls it). 5-min-OR hypothesis REJECTED. chandelier 1.4xATR ratchet floor (tick-level, always live) + post-confirm candle-close reversal on a closed 1-min opposite-color bar; confirm +0.15xATR. vs V0's tight 0.15xATR stop (false stop-outs). Timeframe parsed programmatically; "NOT VERIFIED" fallback if unparseable.
- **Verify:** 4 files compile; exit_explainer verified=true 1-minute; scoreboard 1/5 +449.84; /versions HTTP 200 shows scoreboard (1/5) + explainer (1-minute, 1.4xATR, REJECTED) + glossary; preflight 51/51 incl. the new doc-coverage check.
- **Display-only; non-watched; no trading-loop import (exit_bot_v2 read as TEXT); freeze intact.**

---
### Turn — 2026-06-24 ~9:15 AM ET — Planning↔ChatGPT 2nd-opinion relay (FYI; no code change)
- Rhett relayed Planning's response to ChatGPT's 6/23 review. All three "resolved since review" items are mine (clean-day=1/5, corrected shadow deltas via broker-anchor, V0 re-replay variance). No action — freeze intact, run same 6/24.
- **One correction surfaced to Planning:** the ATR/bar PIN is already SHIPPED (commit d06757a), not "queued post-test" — BUT it's forward-only (pins same-day 6/24+); it cannot byte-reproduce 6/18–6/23 (no snapshots existed then). So Planning's conclusion (Q6 historical re-score still blocked) is correct; the remaining unblock lever = historical-pin backfill via `lastdate`-anchored fetches (I offered it last turn; post-test item).
- Post-test gauntlet items noted (not built mid-test): three-sided exit-loosening test (now incl. giveback/MAE — ChatGPT's SNDK catch), gate-value falsification (passed-9:35 vs near-miss rejects N>=30), entry-conviction-floor (TPR-class), historical-pin backfill (Q6).
- The "next silently-wrong metric" watch (ChatGPT read #2) is the class already under the broker-truth reconcile contract: P&L, slippage/KPI-integrity, shadow-V9 — each with a daily invariant now.

---
### Turn — 2026-06-24 ~9:45 AM ET — V-FREEZE: lock kill-window V0/V9 write-once (Planning verification)
- **Verified (read-only first):** the accumulation (shadow_exit_results.jsonl) has ONE writer (shadow_exit_harness.py:1054, APPEND); dashboard/shadow_versions/CSHV only READ it; the scheduled driver never passes --force. So the automated path is IDEMPOTENT (_already_scored blocks re-write) — but NOT enforced-immutable: a manual `--force` re-run bypasses the guard and APPENDS duplicate rows (double-count; re-replay V0 differs ±$600), and direct edits can mutate. That's the exact corruption path Planning flagged.
- **Locked it (write-once + hash, pre-authorized "before 6/24 close"):** added to shadow_exit_harness.py — `seal_date()`/`is_sealed()`/`verify_seals()`/`seal_existing()` + `shadow_kill_window_seal.json` (per-date sha256 of per-trade V9+V0 nets + n_rows + sums). main() now REFUSES to re-write a sealed date on BOTH paths (trial rows + OOS rows) even with --force; first successful accumulation SEALS immediately. New CSHV check `shadow_kill_window_sealed` (Reliability) re-hashes sealed dates → FAIL on out-of-band mutation, WARN on unsealed-accumulated.
- **Sealed existing:** 6/18 (h=0998…, V9 1067.08/V0 -776.50), 6/22 (h=805f…, V9 939.93/V0 -1048.12), 6/23 (h=55c7…, V9 -256.00/V0 -705.84) — corrected values now immutable.
- **Verify (all PASS):** seal_existing locked 3 days; verify_seals ok on clean file; TAMPER TEST (append dup 6/23 row) → verify BREACHES naming 6/23 (hash + 11→12 rows) → restored → ok; CSHV check OK ("all 3 write-once sealed + hash-intact"); END-TO-END `shadow_exit_harness 2026-06-23 --score --force` → printed SEALED on both paths, 6/23 rows 11→11 (zero added). compile OK.
- **Going forward:** each scored day self-seals on first write; re-runs/--force refused; direct edits caught by CSHV. V0's ±$600 nondeterminism can no longer overwrite a stored kill-window value.
- **Display/measurement-path only; non-watched; no trading-loop import; freeze intact.**

---
### Turn — 2026-06-24 ~10:30 AM ET — Investigated 2 daily WARN pings (Rhett asked)
- Both Discord WARNs fire EVERY trading day (not new); investigated all three current warnings:
  1. **ORB_EARNINGS_STALE** (real): earnings_calendar.csv last refreshed Jun 3 (21d), no scheduled refresh. Veto still runs but with false-negatives; at 21d its dates are all past → veto effectively NEAR-INERT (blocks ~nothing) → bot could enter a name reporting earnings. Recurs daily since ~Jun 6. **Rhett's call: LEAVE IT FOR NOW** (accepted risk during forward test; keep reporting, do NOT refresh). Future sessions: this is a KNOWN-ACCEPTED gap, don't re-flag as new. Fix when un-frozen = refresh `earnings_importer`/`earnings_provider` + add a daily scheduled refresh.
  2. **ORB_SCAN_TIMING** (soft/noise): WARNs when OR-close→first-submit >60s; today 71.3s (scan 25s, submit 4s, ATR cached, no 429s). Bot still traded (2 RT +$34). Trips daily → threshold (60s) cries wolf at the bot's normal ~70s latency. Post-test: either reduce scan latency or re-tier the threshold to INFO. No action now (freeze).
  3. **rel_position_recon / DAL** (benign CSHV WARN): DAL traded+exited today, lingering in recent_exits.json post-exit while broker flat = harmless "bot-has-it/broker-doesn't", pruned each cycle. NOT the dangerous broker-blind direction. Transient.
- **No changes made** (mid-forward-test freeze; refreshing the calendar would change the tradeable set mid-day). Read-only investigation.

---
### Turn — 2026-06-24 ~11:00 AM ET — Add "Deployed capital by hour" chart to daily-review page
- **Ask (Rhett):** add a chart of deployed capital hour-by-hour on the dashboard.
- **Built (daily_review_page.py, display-only):** `_deployed_capital_chart(day, rollup)` — self-contained inline SVG (no JS/CDN dep) reading the live utilization snapshots `outputs/validation/utilization_<day>.jsonl` (total = filled positions + working orders, ET, ~30-min cadence). Buckets by hour → PEAK deployed/hour as columns; dashed $300k deploy target + $400k cap reference lines (sourced from rollup deploy_cap/deploy_target, not hardcoded); bar color green >=90% cap / blue >=60% / grey below; hover title shows $/%, pos+working. Inserted in the capital group of render_html (after peak KPI + sidelined panel).
- **Verify:** compile OK; 6/23 → 7 hourly bars (9a-3p), SVG + target/cap lines present, hour-12 bar = the 12:26 peak $301,815 (at the cap line) = faithful; dashboard restarted PID 9432; /daily-review-v2?date=2026-06-23 = HTTP 200, "Deployed capital by hour" + svg + 400k cap + 300k target PRESENT. Today (6/24, in-progress) shows the hours captured so far.
- **No watched strategy file touched. No trading-path change.** Reads existing utilization snapshots only.
