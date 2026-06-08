Alpha Quant — session ramp-up / handoff. Paste the block below (everything
between the lines) as the first message of a new Claude Code session, working
directory = the "Trade station Main" project root. It carries forward from the
May 21, 2026 session.

------------------------------------------------------------------------------

You are picking up the Alpha Quant project — a SIM-only equity trading bot on
TradeStation, running on the VPS. This hands off from the May 21, 2026 session.

FIRST: name this session — run  /rename "<sub-project name>"  (e.g.
/rename "Alpha Costs"). If /rename is unavailable in this build, skip it.

RAMP UP before doing anything:
1. Read C:\repos\alpha-quant-coordination\ALPHA_QUANT_STATE.md — current state,
   open items, operating rules. Follow its §4 "re-verify" list against the
   actual files; the §4 snapshot is dated, not current.
2. The three CLAUDE.md files (project root + tradestation-bot/ +
   ai-trading-strategy-agent/) auto-load. Read the feedback_*.md files named in
   your MEMORY.md index — the index auto-loads, the files do not.
3. Operating rules: verify before asserting (no system-state claim without
   reading the file); propose-first for anything that changes live behavior;
   never touch files the bot reads/writes mid-cycle; one question per turn;
   user-facing times in 12-hour AM/PM ET. The observation period is in
   progress — no tuning/strategy work; bug fixes and infrastructure are fine.
   Git: the code repo's git directory is C:\repos\trade-station-main-git\ (run
   git from there); the coordination repo is C:\repos\alpha-quant-coordination.

WHAT THE MAY 21 SESSION DID — three safety-machinery failures found and fixed,
all DEPLOYED and verified:

(A) EOD FLATTEN FAILURE (May 20). A GOOGL position was never auto-closed: the
    EOD watchdog fired 83 orders 3:56-4:18 PM and TradeStation rejected all 83
    (66x "No Day orders after 4:00PM Eastern" because it used DAY/market
    orders; rest EC703 stale-order conflicts). It logged each as HTTP 200 and
    never checked order status. Closed only by a manual order at 4:18 PM.
    Fix (proposal PROP-SAFETY-001/002, Rhett-approved): new shared module
    tradestation-bot/exit_orders.py — flatten_symbol() places MARKETABLE LIMIT
    orders (never market orders), duration DAY before 4:00 PM and GCP after,
    cancels-and-verifies stale orders, polls the broker position for the fill,
    adapts on rejection. eod_watchdog.py rewritten to use it + a single-instance
    lock. exit_bot_v2.py exits routed through it (the skip-blocks that stranded
    GOOGL were removed). market_hours.py: entry cutoff + forced flatten moved to
    3:50 PM ET. Verified live May 21: IWM+MCD flattened in ~2s each, 35 exits
    filled. NOTE: the TradeStation API rejects the literal "GTC+" (400 Invalid
    duration); the correct extended-hours duration code is "GCP".

(B) RECURRING "FREEZE" (May 16-21) — a FALSE POSITIVE. The ~daily watchdog
    "Heartbeat stale — force restarting" events were not real freezes:
    bot_heartbeat.json lived in the OneDrive-synced tree, OneDrive transiently
    locked it, the watchdog's read failed, and it killed a HEALTHY bot on a
    single failed read (no debounce). Fix: heartbeat moved out of OneDrive to
    %LOCALAPPDATA%\AlphaQuant\bot_heartbeat.json (project_paths.HEARTBEAT_PATH);
    run_bot._write_heartbeat now writes atomically; watchdog_supervisor.py
    requires 3 consecutive stale reads before a restart and logs the real
    exception. Files: project_paths.py, run_bot.py, watchdog_supervisor.py,
    bot_monitor.py.

(C) NO WATCHER ON THE WATCHDOG. The supervisor itself died ~4:04 PM May 21
    (killed externally, no crash log) and run_bot ran orphaned for hours. Fix:
    new tradestation-bot/supervisor_guardian.py + Windows Scheduled Task
    "AlphaQuant Supervisor Guardian" (every 2 min) — relaunches the supervisor
    if dead (killing any orphaned run_bot first). Verified end-to-end.
    Watch chain (each layer restarted by the one to its right; terminates at
    the OS): child scripts <- run_bot.py <- watchdog_supervisor.py <-
    supervisor_guardian.py <- Windows Task Scheduler.

CURRENT LIVE STATE (as of ~8:40 PM ET May 21): supervisor + run_bot both alive,
heartbeat fresh at the new local path, account flat, everything above
deployed. PIDs change on any restart — verify processes by name, not PID.

OPEN ITEMS (priority order):
1. COMMIT TO GIT. None of the May 21 code is committed. ~9 changed/new code
   files + the proposal sit as uncommitted working-tree edits in
   C:\repos\trade-station-main-git\. A week of safety fixes exists only on
   disk. Do this first.
2. Fold the guardian task into setup_autostart.py so a future autostart
   re-install does not silently drop it.
3. Inventory the other scheduled tasks (AlphaQuant Research Brain, AlphaQuant
   Volume Capture, AlphaQuantBot) — is each watched / restarted on failure?
4. Controlled SIM rehearsal of the full exit submit->fill path with a real
   position; then multi-day clean-close observation (PROP-SAFETY test plan).
5. Investigate why the supervisor died at ~4:04 PM (unexplained; possibly
   fallout from a parallel session's PROP-UNIVERSE-001 work).
6. Optional: upgrade the supervisor to a Windows Service with SCM auto-recovery
   (near-instant restart vs the guardian's <=2-min gap; needs NSSM).

GOTCHAS:
- run_bot.py relaunches the child scripts (bot_loop, short_bot, exit_bot_v2,
  eod_watchdog) from disk every cycle — edits to those + exit_orders.py +
  market_hours.py go live at the next loop, no restart. Edits to run_bot.py and
  watchdog_supervisor.py need a process restart.
- To restart cleanly: taskkill /F /T /PID <supervisor pid> (kills run_bot too),
  then schtasks /run /tn "AlphaQuant Bot Supervisor". The guardian also
  relaunches the supervisor within 2 min if it finds it dead.
- Heartbeat is now %LOCALAPPDATA%\AlphaQuant\bot_heartbeat.json — the old
  bot_heartbeat.json in tradestation-bot/ is stale; ignore it.
- TradeStation order duration code is "GCP", not "GTC+" (GTC+ is display-only).
- A parallel session logged a journal double-counting bug in CHANGELOG.md
  (load_all_journal_rows globbed all trade_journal*.csv -> ~27x overcount;
  fixed commit 675dcf5; learned_patterns.json was corrupt, regenerated). Read
  those CHANGELOG entries — the advisor had been learning from distorted data.
- A session-only watch loop (cron 1a85d7a1, 30-min health check) ran in the
  May 21 session; it stopped when that session closed. The bot's own
  supervision (supervisor + guardian) is the durable, OS-backed coverage.

RE-VERIFY at session start (in addition to STATE.md §4):
- Confirm watchdog_supervisor.py AND run_bot.py are both alive
  (Get-CimInstance Win32_Process -Filter "Name LIKE 'python%'").
- schtasks /query /tn "AlphaQuant Supervisor Guardian" — exists, Status Ready.
- %LOCALAPPDATA%\AlphaQuant\bot_heartbeat.json last_seen fresh (< 3 min).
- Tail tradestation-bot/watchdog_supervisor.log and supervisor_guardian.log for
  any new freeze/crash/restart lines.

FIRST TASK: <describe the task — or "tell me where things stand">

------------------------------------------------------------------------------
