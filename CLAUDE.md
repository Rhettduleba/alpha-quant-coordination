# CLAUDE.md — Alpha Quant workspace

This is the root of the **Alpha Quant** project — two cooperating Python systems for SIM-only equity trading on TradeStation. The canonical, hand-written deep-dive lives in [ALPHA_QUANT_HANDOFF.md](ALPHA_QUANT_HANDOFF.md); read that first if you have time. This file is the shorter operational primer for a Claude session.

## What lives where

```
.
├── tradestation-bot/             # "The Bot" — places SIM orders, enforces risk
├── ai-trading-strategy-agent/    # "The Advisor" — Claude-driven daily analysis + control file
├── Archive/, Sync/, Trades/, Learning/, Marketing/, Launchers/, outputs/
├── ALPHA_QUANT_HANDOFF.md        # full architecture write-up — start here
├── Alpha_Quant_Handoff.docx      # same content as .docx
├── Start_Dashboard.bat           # one-click launcher for the advisor's local dashboard
└── .claude/settings.json         # repo-local Claude Code permissions
```

The two main folders are **separate Python projects** with their own dependencies, logs, and configs. They do not import each other. Their only communication channel is one JSON file on disk (see "The one-way channel" below).

## The architectural rule (do not violate)

> **The agent should know a lot. The bot should do only what has been proven.**

- The **bot** is intentionally narrow, dumb, and reviewable.
- The **advisor** may be smart, opinionated, and constantly learning.
- The advisor never reaches into the bot. It writes one JSON file; the bot reads it with paranoid validation.
- The human owns every gate that changes live behavior, risk limits, or universe.

## SIM-only — non-negotiable

- Account: `SIM1623888M`. The bot's safety stop refuses to start if the account ID doesn't begin with `SIM`.
- The advisor stamps every control file with `environment: "SIM_ONLY"` and `live_allowed: false`.
- Do **not** edit either of those guards, and do not introduce code paths that bypass them.

## The bot — `tradestation-bot/`

- Entry point: [run_bot.py](tradestation-bot/run_bot.py) → per-cycle work in [bot_loop.py](tradestation-bot/bot_loop.py).
- Risk floor: [risk_config.py](tradestation-bot/risk_config.py) — `DAILY_MAX_LOSS = $10,000`.
- Sizing constants in [bot_loop.py](tradestation-bot/bot_loop.py): `MAX_POSITION_PCT = 0.25`, `MAX_OPEN_POSITIONS = 4`, `MAX_TOTAL_EXPOSURE = $100,000`, `MIN_PRICE = $20`, `MIN_NET_CHANGE_PCT = 0.25%`, `MIN_VOLUME = 500,000`, `MAX_SPREAD = $0.25`.
- Sector cap: `MAX_SECTOR_POSITIONS = 2` from [symbol_universe.py](tradestation-bot/symbol_universe.py).
- The advisor filter lives in [advisor_filter_engine.py](tradestation-bot/advisor_filter_engine.py) — the only place the advisor's output is interpreted as behavior.
- Supporting roles: [eod_watchdog.py](tradestation-bot/eod_watchdog.py), [exit_bot_v2.py](tradestation-bot/exit_bot_v2.py), [short_bot.py](tradestation-bot/short_bot.py), [watchdog_supervisor.py](tradestation-bot/watchdog_supervisor.py), [daily_guard.py](tradestation-bot/daily_guard.py), [daily_reconciliation.py](tradestation-bot/daily_reconciliation.py).
- Heartbeat: `bot_heartbeat.json`. Audit trail: `trade_journal.csv` and `advisor_filter_engine.log`.

The bot **must not**: read free text from the advisor, change its own risk config / universe / strategy, touch credentials, or place orders in response to advisor instructions outside the typed schema.

## The advisor — `ai-trading-strategy-agent/`

There are **two pipelines** in this folder. Don't conflate them.

1. **Operational control loop** — [run_advisor.py](ai-trading-strategy-agent/run_advisor.py). Calls Claude (currently `claude-sonnet-4-6`), writes the typed control file the bot obeys. Scheduled ~8:00 AM, ~12:30 PM, ~4:30 PM ET.
2. **V1 advisory research pipeline** — [src/main.py](ai-trading-strategy-agent/src/main.py). Produces daily reports, operator dashboard, weekly review, proposal/experiment artifacts under `outputs/`. Human-review surface; does not feed the bot.

When in doubt about whether a module is part of the active V1 path, consult [V1_SCOPE.md](ai-trading-strategy-agent/V1_SCOPE.md). It explicitly labels these folders as parked / partial / experimental: `src/agents/`, `src/analytics/`, `src/backtesting/`, `src/replay/`, `src/research/`, `src/strategy/`. Do not assume "exists in repo" means "active in workflow."

Common V1 commands (run from `ai-trading-strategy-agent/`):

```powershell
python src/main.py --build-preopen-data
python src/main.py
python src/main.py review-day --date YYYY-MM-DD
python src/main.py review-range --start YYYY-MM-DD --end YYYY-MM-DD
python src/main.py trade-review-ui --host 127.0.0.1 --port 8765
```

If `python src/main.py` fails on OneDrive locking `src/config/models.py`, use the import fallback:
```powershell
python -c "import sys; sys.path.insert(0, 'src'); import main; main.main()"
```

Tests: `pytest` from the advisor repo root. `src/ingest/refresh_test.py` is **manual-only** and intentionally excluded from pytest runs.

## The one-way channel — advisor → bot

The advisor writes two files to `ai-trading-strategy-agent/outputs/advisor_guidance/`:

- `advisor_control_latest.json` — the **typed rulebook the bot actually obeys**. 24-hour TTL.
- `latest_advisor_guidance.json` — human-facing summary; bot reads it only for startup logging.

The bot's [advisor_filter_engine.py](tradestation-bot/advisor_filter_engine.py) re-reads the control file every loop and **rejects** it if: file missing, bad JSON, `environment != "SIM_ONLY"`, `live_allowed != false`, `free_text_control_allowed != false`, or past `expiration_time`. **When rejected, the bot defaults to ALLOW** (no controls) — a missing/stale advisor must never lock the bot out.

The only legal control types are:

`BLOCK_ALL_NEW_ENTRIES`, `BLOCK_SYMBOL`, `ALLOW_SYMBOLS_ONLY`, `BLOCK_ENTRIES_AFTER_TIME`, `REDUCE_MAX_POSITIONS`, `SET_MAX_POSITION_PCT`, `REQUIRE_MIN_NET_CHANGE_PCT`, `REQUIRE_MIN_NEG_CHANGE_PCT`, `BLOCK_SYMBOL_DUE_TO_NEWS`, `PROMOTE_SYMBOL`, `WATCHLIST_TODAY`, `NO_CONTROLS`.

The last three were added 2026-05-26 (Bot AI Phase 2 / Advisor Phase 2):
- `BLOCK_SYMBOL_DUE_TO_NEWS` — blocks a symbol with `headline_summary` + `news_sentiment` (NEG blocks longs, POS blocks shorts).
- `PROMOTE_SYMBOL` — soft scoring nudge: bot composite gets a (0–0.30) bonus for a promoted `(symbol, side, conviction_score)`. Never bypasses hard filters.
- `WATCHLIST_TODAY` — list of up to 20 symbols the advisor prefers; bot adds a 0.05 ranking bonus.

`BLOCK_ALL_NEW_ENTRIES` is now HONORED (reversed from prior `RECOMMENDED_HALT_NOT_HONORED` design as of 2026-05-26). Emergency override: create `tradestation-bot/override_advisor_halt.json` with `{"override": true, "reason": "..."}`.

**Anything outside this list is silently ignored.** Do not extend this vocabulary without a deliberate, reviewed change on both sides of the channel.

## Working rules for Claude in this workspace

> **STANDING RULE #0 — VERIFY BEFORE YOU STATE (permanent, both seats — Planning Claude + Claude Code; added 2026-06-15 Loop 87).** NEVER present a guess or an unverified claim as fact. Verify every load-bearing claim against the real source — live data, the actual code, or broker truth — BEFORE stating it. If it cannot be verified yet, say so explicitly ("unverified" / "needs live capture" / "pending") — never fill the gap with a plausible guess. Check BEFORE acting, not after. Operating standard: **nothing untested reaches Rhett.** This rule overrides convenience, speed, and the urge to sound finished.

1. **Preserve the one-way channel.** Never add a code path that lets the advisor write into bot config, that lets the bot execute free-text advisor instructions, or that loosens the typed-schema gate in [advisor_filter_engine.py](tradestation-bot/advisor_filter_engine.py).
2. **Preserve the SIM-only guards** in both halves of the system.
3. **Strategy changes are advisory-only.** Anything that could change live behavior — entry/exit, sizing, stops, time windows, risk caps, universe — must go through a proposal artifact under `ai-trading-strategy-agent/outputs/proposals/` and stay inactive until a human records explicit approval in `config/manual_approvals.yaml`.
4. **TradeStation tokens are reused, not refreshed per call.** Access tokens last ~20 min; the client refreshes only inside a small buffer (default 60s) before expiry. Persist via `token_cache.json`. Never refresh on every API call or every bot cycle — excessive refreshes can get the API key disabled.
5. **Evidence hierarchy** (highest → lowest): `BROKER_TRUTH` > `BROKER_EXPORT` > `LOCAL_RECONSTRUCTION` > `BOT_LOG_CONTEXT` > `ADVISORY_RESEARCH`. Conclusions must cite the highest available source; anything based only on `LOCAL_RECONSTRUCTION` or `ADVISORY_RESEARCH` must be labeled as such, not presented as broker-confirmed.
6. **Symbol-agnostic logic.** Production reconciliation, analytics, and recommendation code must iterate dynamically over symbols found in the data — no hardcoded `AAPL`/`TSLA`/etc. branches. Watchlists are config data, not code paths.
7. **No secrets in source.** `.env` files only; `token_cache.json` and credential files stay local.
8. **VPS-only as of 2026-05-21.** The whole tree is OneDrive-synced for backup, but only the VPS (`WIN-FIBSSOQKI7K`) should be writing to it. Pre-5/21 machine-suffix artifacts (`*-Home-Office*`, `*-BOOK-*`, etc.) are legacy and safe to delete; new ones appearing during a session are a sync-conflict bug to investigate (CSHV check `onedrive_sync_conflicts` flags them).
9. **Conservative wording.** Don't claim "API connected," "broker truth reconciled," or "production-ready" unless the validation checklist in `ai-trading-strategy-agent/README.md` has actually passed against real data.
10. **OneDrive lock quirk.** On this machine, OneDrive can transiently lock files mid-edit. If a write fails with a permission error and the file isn't actually in use, retry once before assuming a real problem.
11. **Read `CSHV_FINDINGS.md` at session start.** The Continuous System Health Verifier runs every 5 minutes and writes the latest state + suggested fixes per failing check to `CSHV_FINDINGS.md` at the project root. Open it first — any FAIL or WARN there is a higher priority than whatever else you're being asked to do. Each finding includes a suggested fix and the relevant files. Don't re-derive a diagnosis CSHV has already done for you.

## Where the staged ramp stands

The project is in **stages 3–4** of a 6-stage plan:

1. Verify environment ✓
2. Reporting & reconciliation ✓
3. SIM testing with full logs ← **here**
4. AI advisor layer ← actively shipping, not yet trusted enough to graduate
5. Controlled strategy improvements
6. Carefully controlled live trading (only with explicit human approval)

Nothing in this codebase should be edited in a way that quietly advances the system past where the human has approved it to be.

## Reading order for a new session

1. This file.
2. [ALPHA_QUANT_HANDOFF.md](ALPHA_QUANT_HANDOFF.md) — the deep architectural write-up.
3. [ai-trading-strategy-agent/V1_SCOPE.md](ai-trading-strategy-agent/V1_SCOPE.md) — active vs. parked in the advisor repo.
4. [ai-trading-strategy-agent/AGENTS.md](ai-trading-strategy-agent/AGENTS.md) — repo conventions and guardrails for the advisor.
5. `ai-trading-strategy-agent/outputs/advisor_guidance/advisor_control_latest.json` — what the bot will actually obey today.
6. [tradestation-bot/advisor_filter_engine.py](tradestation-bot/advisor_filter_engine.py) — the only interpreter of advisor output.
7. [tradestation-bot/bot_loop.py](tradestation-bot/bot_loop.py) — the single cycle the bot runs.
8. [tradestation-bot/risk_config.py](tradestation-bot/risk_config.py) — the hard floor.
