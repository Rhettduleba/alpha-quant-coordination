# Session Handoff — Alpha Quant Research Brain Build

**Date:** May 21, 2026 (Thursday)
**Session scope:** Designed, built, tested, and went live with the Alpha Quant
research brain — a 9-stage research/scoring pipeline that builds a criteria-based
trading universe and feeds it to the bot through a new typed channel.
**Owner:** Rhett. **Built by:** Claude Code (this session).

---

## 1. TL;DR

The bot used to trade a hardcoded 34-symbol list. It now trades a **criteria-based
universe drawn from all ~10,935 NYSE/NASDAQ/AMEX/ARCA symbols**, rebuilt every
pre-market by a new research brain and handed to the bot through a typed,
paranoia-validated channel with a `CORE_UNIVERSE` fallback.

- 9-stage research brain built in `ai-trading-strategy-agent/` (mostly `src/brain/`).
- Live data wired to TradeStation; symbol master + sector map ingested.
- Bot wired to adopt the universe channel (PROP-UNIVERSE-001, Rhett-approved).
- Two scheduled tasks: pre-market research run (7:30 AM ET) + post-close volume
  capture (4:35 PM ET).
- 86 brain tests pass. The brain has run live and published real universes.
- **No profitability evidence yet** — the brain has zero completed trades. See §11.

---

## 2. Decisions Rhett made this session

1. **Open the universe** to all NYSE/NASDAQ, criteria-based (not a hardcoded list).
2. **Open the "one-way valve"** — the advisor may now hand the bot a typed
   candidate universe (previously the advisor could only restrict the bot).
3. **Build inside the existing `ai-trading-strategy-agent/` repo**, not a separate
   project (the parked `src/universe/` scaffolding was reused/extended).
4. **Override the observation-period hold** for this build.
5. **Activate now** — wire the bot immediately (vs. shadow-mode first).
6. **Run the first universe as-is for Friday** — the 150-name, ETF-inclusive
   universe; tuning deferred to post-observation.
7. **Research brain runs pre-market** (corrected from an initial post-close plan).
8. Of the 5 proposed brain improvements: **do #3 + #5 + the measurement loop now**;
   **hold #1, #2, #4** until SIM evidence backs them (see §11).

---

## 3. The research brain — 9 stages

All stages take **injected data providers**, so each is unit-tested offline.
Modules are in `ai-trading-strategy-agent/src/brain/` unless noted.

| Stage | Module | Purpose |
|---|---|---|
| 1 | `src/universe/universe_builder.py` | Criteria-based universe from a whole-exchange symbol master (price $20–600, ADV > 2M, dollar-volume > $25M, spread ≤ 25 bps, exclude halted; cap 150). |
| 2a | `market_context.py` | Top-down regime: risk-on/off, volatility band, sector rotation, macro-day flag. |
| 2b | `intraday_scanner.py` | Ranks the universe by movement quality (gap, RVOL, net change, range) → daily shortlist. |
| 3 | `catalyst_classifier.py` | Classifies the catalyst (news/earnings/analyst/filings) and scores quality. **Currently fed an empty placeholder — see §11.** |
| 4 | `technical_engine.py` | VWAP, opening range, trend, relative strength; scores directional consensus. |
| 5 | `trade_scorecard.py` | 8-factor composite → No-trade / Watch / Good / Strong / A+. |
| 6 | `historical_similarity.py` | "When this setup happened before, what followed?" — bucketed edge lookup. **No history loaded yet — returns neutral.** |
| 7 | `validation_harness.py` | Walk-forward, costs/slippage, kill-weak-ideas, pass/fail. **Has no real data to chew on yet.** |
| 8 | `universe_writer.py` (advisor) + `tradestation-bot/advisor_universe_reader.py` (bot) | The typed advisor→bot universe channel. |
| 9 | `research_brain.py` | Orchestrator — chains stages 1→6→5→8 into one pipeline. |

Configs: `config/universe_builder.yaml` (Stage 1 criteria), `config/research_brain.yaml`
(stages 2+).

---

## 4. Operational wiring

- **`src/universe/symbol_master_ingest.py`** — fetches the public NASDAQ Trader
  symbol directory → `data/universe/symbol_master.csv` (**12,261 symbols**).
- **`src/universe/sector_map_ingest.py`** — fetches the NASDAQ stock screener →
  `data/universe/sector_map.csv` (**6,356 symbols, 12 sectors**). Powers the
  bot's sector-correlation cap on the expanded universe (improvement #3).
- **`src/brain/tradestation_providers.py`** — batched quote provider (~110 API
  calls for the whole exchange, not 12k), rolling average-daily-volume model,
  bars provider.
- **`run_research_brain.py`** — operational runner. Two modes:
  - default = pre-market research run → builds + publishes the universe channel,
    runs the advisory pipeline, writes status + report.
  - `--capture-volume` = post-close volume capture → records full-day volume into
    the rolling ADV history (`data/universe/volume_history.json`).

### The ADV model (important)
Average daily volume is **not** in the TradeStation quote. It is built from a
rolling snapshot: the **post-close capture** records each day's full volume; the
**pre-market run** reads that history to compute ADV. This is why there are two
scheduled runs. ADV accuracy improves as history accumulates.

---

## 5. Bot-side changes (these are LIVE behavior changes)

| File | Change |
|---|---|
| `tradestation-bot/advisor_universe_reader.py` | **NEW** — paranoid reader for `advisor_universe_latest.json`. Validates (SIM_ONLY, live_allowed false, free-text false, not expired). On ANY failure → returns `CORE_UNIVERSE`. Hard-caps at 250 symbols. Also exposes `get_universe_sector_map()`. |
| `tradestation-bot/bot_loop.py` | Scan universe now comes from `get_scan_universe(CORE_UNIVERSE)` instead of the hardcoded list. |
| `tradestation-bot/short_bot.py` | Same change. |
| `tradestation-bot/symbol_universe.py` | `get_sector()` now consults the channel sector map for non-core symbols, so the sector cap works on the expanded universe. `CORE_UNIVERSE` retained as the permanent fallback. |
| `ai-trading-strategy-agent/config/manual_approvals.yaml` | `PROP-UNIVERSE-001` moved to `approved_proposal_ids` (Rhett verbal approval, this session). |

**Safety preserved:** the bot still applies every one of its own hard filters
(price/volume/spread/net-change), risk gates (daily-loss $10k, max 4 positions,
$100k exposure, sector cap), and the restrict-only advisor control filter to
every symbol — regardless of where the universe came from. The channel only
changes *which symbols are scanned*. A broken/stale/missing channel → `CORE_UNIVERSE`.

Proposal: `ai-trading-strategy-agent/outputs/proposals/PROP-UNIVERSE-channel.md`.

---

## 6. Scheduling

Windows Task Scheduler, both run as `SYSTEM`, weekdays:

| Task | Time (ET) | Launcher | Action |
|---|---|---|---|
| `AlphaQuant Research Brain` | 7:30 AM | `C:\AlphaQuant\research_brain.bat` | Build + publish the universe. |
| `AlphaQuant Volume Capture` | 4:35 PM | `C:\AlphaQuant\capture_volume.bat` | Record full-day volume for ADV. |

**Scheduling gotcha (resolved):** Task Scheduler returned `0x80070005` (access
denied) then `0x80070002` (file not found) when launchers lived in the OneDrive
tree / had spaces in their names. Fix: launchers live in **`C:\AlphaQuant\`**
(outside OneDrive, no spaces) and the task action is `cmd /c C:\AlphaQuant\<name>.bat`.
The Volume Capture task was triggered via the scheduler and verified — `Last
Result: 0`. The Research Brain task uses the identical mechanism; **Friday
7:30 AM is its first fully autonomous run — worth a glance at the log.**

---

## 7. Current live state (as of ~8:20 PM ET, May 21)

- `advisor_universe_latest.json` is published — **150 symbols**, sector-enriched
  (106/150 classified; the 44 ETFs are intentionally unclassified → cap-exempt),
  24-hour TTL.
- The bot is wired and will adopt this universe at Friday's open. Friday 7:30 AM
  the scheduled run republishes a fresh universe.
- Brain run status: `outputs/research/research_brain_status.json` → `OK`.
- Latest run: regime RISK_ON, shortlist 30, ~13 actionable (Good-tier) candidates.
- 86/86 research-brain tests pass.

---

## 8. Key output files

| File | What |
|---|---|
| `ai-trading-strategy-agent/outputs/advisor_guidance/advisor_universe_latest.json` | The universe channel the bot reads. |
| `ai-trading-strategy-agent/outputs/research/research_brain_latest.json` | Full machine-readable pipeline result. |
| `ai-trading-strategy-agent/outputs/research/research_brain_report.md` | Human-readable daily report (regime + top candidates). |
| `ai-trading-strategy-agent/outputs/research/research_brain_status.json` | Run status (OK / EMPTY_UNIVERSE / FAILED). |
| `ai-trading-strategy-agent/outputs/logs/research_brain_run.log` | Append-only run log. |
| `tradestation-bot/advisor_universe_reader.log` | Every bot-side universe-channel decision. |
| `data/universe/symbol_master.csv` | 12,261-symbol exchange master. |
| `data/universe/sector_map.csv` | 6,356-symbol sector map. |
| `data/universe/volume_history.json` | Rolling daily-volume history for ADV. |

---

## 9. Tests

12 test files, **86 passing** (run from `ai-trading-strategy-agent/` with
`python -m pytest tests/`):
test_universe_builder, test_market_context, test_intraday_scanner,
test_catalyst_classifier, test_technical_engine, test_trade_scorecard,
test_historical_similarity, test_validation_harness, test_universe_channel,
test_research_brain, test_tradestation_providers, test_sector_map.

**Pre-existing failures (NOT caused by this session):** the full `tests/` run
shows ~10 failures in modules untouched by this work — `test_dashboard_routes`,
`test_ingest`, `test_v1_agent` (a `build_recommendations` signature drift),
`test_bot_health_severity`, `test_live_write_guard`. Left alone; flagged here.

---

## 10. How to operate it

```powershell
# from ai-trading-strategy-agent/  (system Python — the .venv is broken, see §13)
python run_research_brain.py                  # pre-market: build + publish universe
python run_research_brain.py --capture-volume # post-close: record volume for ADV
python -m pytest tests/                       # tests

# refresh the static data occasionally
python -c "import sys;sys.path.insert(0,'src');from universe.symbol_master_ingest import main;main()"
python -c "import sys;sys.path.insert(0,'src');from universe.sector_map_ingest import main;main()"
```

The scheduled tasks run the two modes automatically. To trigger manually:
`schtasks /run /tn "AlphaQuant Research Brain"`.

---

## 11. Open items & next steps

### Approved, next to build
- **The measurement loop** — record the brain's daily per-symbol predictions
  (scorecards) and match them to actual SIM trade outcomes, accumulating the
  dataset the Stage 7 validation harness needs. This is what turns every other
  improvement from "plausible" into "proven." **This was in progress at session
  end — start here.**

### Held — see memory `project_research_brain_deferred_items.md`
- **#1** — wire the scorecard into the channel so the bot *prefers* A+/Strong
  setups. Highest leverage, highest risk: the bot currently consumes only the
  *symbol list* — all the catalyst/technical/scorecard analysis is computed and
  then ignored. The scorecard weights are unvalidated heuristics; wiring the bot
  to trust them could *reduce* profit.
- **#2** — catalyst data (SEC EDGAR filings, TradeStation news, FMP earnings).
  Stage 3 runs on an empty placeholder until this is wired. (No `FMP_API_KEY`
  in either `.env`; FMP earnings needs one.)
- **#4** — historical-edge backfill for Stage 6 (a backtest — overfitting risk).
- **Gate:** #1/#2/#4 are NOT committed profit improvements. Revisit only after
  the measurement loop has produced enough SIM evidence to judge them.

### Known imperfections
- **150-name universe is ETF/cash-heavy** (liquidity-only ranking puts SGOV, a
  cash ETF, at #1; includes leveraged ETFs TQQQ/SOXL/SPXS). Rhett chose to run
  as-is. Tuning (exclude leveraged/cash ETFs, maybe a smaller cap) is a
  post-observation follow-up.
- **Sector labels** come from NASDAQ's screener taxonomy, not clean GICS (e.g.
  TSLA → "Industrials"). The cap works; the buckets aren't textbook.
- **Catalyst & historical-edge stages are inert** until #2 and #4.

---

## 12. Honest caveats & risks (objective assessment)

- **No profitability evidence.** The brain has produced universes but **zero
  completed trades**. Nothing here is proven to improve P&L.
- **The bot's core strategy is net-negative at baseline** — V5 broker truth:
  $-2,282.41 over 22 days, $-3.85 per closed pair. The brain changes *which
  symbols* are traded; it does **not** touch entry timing, exits, or sizing,
  where the actual edge lives. Research layers on an unprofitable core do not
  reliably create profit.
- **The brain's intelligence does not yet reach the bot's decisions** — only its
  symbol list does (improvement #1, held).
- **The research scheduled task's autonomous launch** is verified by equivalence
  (the capture task was triggered via the scheduler successfully; the research
  task uses the identical chain). Friday 7:30 AM is the first true autonomous run.
- **TradeStation providers** were verified against the live API (multiple full
  runs succeeded). The `barcharts` endpoint is exercised only for the ~30
  shortlist symbols and is non-critical to the channel.

---

## 13. Environment notes

- The advisor repo's `.venv` is **broken** — it points at a `C:\Users\rdule\...`
  path from another machine and cannot run on this VPS. **System Python 3.14**
  is used instead.
- Installed into system Python this session: `pytest`, `pyyaml`, `pydantic`,
  `python-dotenv`, `openpyxl`, `certifi`.
- `certifi` was required — system Python had no CA bundle, so HTTPS fetches
  (symbol master, sector map) failed with `CERTIFICATE_VERIFY_FAILED` until
  `certifi` was installed and used for the SSL context.
- Project is **VPS-only** now (hostname `WIN-FIBSSOQKI7K`) — the CLAUDE.md
  multi-machine guidance is historical.

---

## 14. Memory files written this session

In `~/.claude/projects/.../memory/`:
- `feedback_keep_building_autonomously.md`
- `project_vps_only.md`
- `project_research_brain_build.md`
- `project_research_brain_deferred_items.md` (the #1/#2/#4 reminder + gate)

---

## 15. Reading order for the next session

1. This handoff.
2. `ai-trading-strategy-agent/outputs/proposals/PROP-UNIVERSE-channel.md` — the channel design.
3. `ai-trading-strategy-agent/src/brain/research_brain.py` — the orchestrator (entry point to the brain).
4. `ai-trading-strategy-agent/run_research_brain.py` — the operational runner.
5. `tradestation-bot/advisor_universe_reader.py` — the bot-side channel reader.
6. The memory file `project_research_brain_deferred_items.md` — what is held and why.

### Housekeeping not yet done
- `ALPHA_QUANT_STATE.md` and `CHANGELOG.md` in this coordination repo have **not**
  been updated for this session — they should be reconciled against this handoff.
