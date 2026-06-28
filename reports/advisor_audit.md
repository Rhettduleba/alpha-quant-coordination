# ADVISOR AUDIT -- what the 3rd core component DOES, and has it helped or hurt? (read-only)
_Broker-truth + live code. Post-2026-05-26 baseline (current bot). GROSS only. Freeze intact._

## Q1 -- WHAT IT IS (verified from code)
- **Model: `claude-sonnet-4-6`** (claude_client.py:14, MODEL constant). VERIFIED.
- **Schedule: 8:00 AM / 12:30 PM / 4:30 PM ET** (run_advisor docstring; run-log timestamps confirm). **308 runs logged.** VERIFIED it runs.
- **Inputs** (run_advisor.py steps 1-4.5, VERIFIED): market snapshot (universe quotes), account state, trade journal (recent + all-time), historical pattern analysis, advisor memory, earnings context, news, bot-health watcher.
- **Opinion path** (VERIFIED): prompt_builder -> call_claude -> response_parser -> control_writer writes `active_controls` to advisor_control_latest.json. Bot re-reads it every loop via advisor_filter_engine.
- **UNVERIFIED/not assessed here:** prompt CONTENT quality (whether the LLM's reasoning is good) -- this audit measures EFFECT on trades, not opinion quality.

## Q2 -- WHAT IT EMITS + how often it CHANGES a bot decision
- Latest control file: **13 active_controls** -- {'BLOCK_SYMBOL': 6, 'REQUIRE_MIN_NET_CHANGE_PCT': 1, 'REQUIRE_MIN_NEG_CHANGE_PCT': 1, 'BLOCK_ENTRIES_AFTER_TIME': 1, 'WATCHLIST_TODAY': 1, 'PROMOTE_SYMBOL': 3}. control_mode=SIM_ALLOWLIST_ONLY, env=SIM_ONLY, live_allowed=False.
- Typical run emits ~13 controls: ~6 BLOCK_SYMBOL + REQUIRE_MIN_NET_CHANGE_PCT + REQUIRE_MIN_NEG_CHANGE_PCT + BLOCK_ENTRIES_AFTER_TIME + WATCHLIST_TODAY + ~3 PROMOTE_SYMBOL.
- Control file IS honored: `CONTROL_VALID` is the status on every bot read in the trading window (not rejected/stale).

### THE STRUCTURAL GAP (gate-style): most emitted controls never reach the real book
- **100% of real trades are ORB** (post-2026-05-26: {'orb_v1_6': 282, 'h5_v1': 3}). The composite `bot_loop` path took **0 trades**.
- **ORB (`orb_runner.py`) imports ONLY `should_block_entry`** -- it honors the HARD blocks (BLOCK_SYMBOL, BLOCK_SYMBOL_DUE_TO_NEWS, BLOCK_ALL_NEW_ENTRIES, ALLOW_SYMBOLS_ONLY, BLOCK_ENTRIES_AFTER_TIME) and NOTHING else.
- The SOFT controls -- **WATCHLIST_TODAY, PROMOTE_SYMBOL, REQUIRE_MIN_NET_CHANGE_PCT, REQUIRE_MIN_NEG_CHANGE_PCT, SET_MAX_POSITION_PCT, REDUCE_MAX_POSITIONS** -- are read only by `bot_loop` (composite). Composite never traded -> **these are STRUCTURALLY INERT on the real book.** By count that is the MAJORITY of what the advisor emits.
- ORB's universe = `orb_universe.build_universe()` (S&P500 + supplement, cached). It does **NOT** consume the advisor universe channel (that channel only supplies a cosmetic sector map). So the advisor cannot shape ORB selection either.

## Q3 -- HELPED or HURT (the real one)
- Actual block EVENTS the bot logged post-2026-05-26: **698** -> kinds {'BLOCK_ALL_NEW_ENTRIES_HONORED': 503, 'BLOCK_ENTRIES_AFTER_TIME': 3, 'BLOCK_SYMBOL': 192}.
- BLOCK_SYMBOL: **192 events but only 3 DISTINCT (date,symbol)** -> [('2026-06-19', 'CVX'), ('2026-06-19', 'JNJ'), ('2026-06-19', 'MCD')]. **192/192 were pure broker-`[NO]`-flag relays** (the symbol was broker-flagged unavailable -- the bot/broker would reject it anyway); **0 were advisor-judgment blocks.**
- BLOCK_ALL_NEW_ENTRIES honored only on days: ['2026-05-26'] (on 2026-05-26 the bot took 0 round-trips -- no trading that day regardless).
- **blocked-symbol INTERSECT traded same day: 0** []
- **blocked-symbol INTERSECT ORB-selected same day: 0** []
- => the advisor's blocks NEVER intersected a name ORB selected or traded. **Interventions on the real book: 0 of 285 trades.**
- Counterfactual is **EXACT, not derived**: a blocked name that provably never appears in the selected/traded set has no trade to counterfactual. Gross effect = **$0**. (The ~5% counterfactual-fidelity check the handoff asked for is moot -- there were zero altered trades to validate.)

## BOTTOM LINE (one sentence)
**The Advisor is NET-NEUTRAL / effectively INERT on broker truth post-baseline:** it runs 3x/day, calls Claude for real, and writes a control file the bot validates as CONTROL_VALID -- but the majority of its controls target a composite path that never trades, and its only book-reaching control (BLOCK_SYMBOL) was, every single time, a relay of the broker's own `[NO]` flag that hit 3 symbol-days (CVX/JNJ/MCD, 6/19) and changed **zero** of 285 ORB trades and **$0**.

## CAVEATS / HONESTY
- Window = post-2026-05-26 (the current-bot baseline; 6/08-6/26 trades, 285 round-trips, ~19 days). PRE-baseline the advisor DID make judgment blocks (e.g. 5/12 CRM 'wide spread/low vol') and the composite path traded -- so historically it had more potential effect; out of scope by the baseline rule.
- This measures EFFECT ON TRADES only. The advisor still does human-facing WORK (regime assessment, watchlist, memory, daily review) -- that is not 'inert', it is just ADVISORY, not acting on the book.
- The 3 BLOCK_ENTRIES_AFTER_TIME block events seen are off-hours/replay (5/31 22:24, cutoff 14:30 ET).
- READ-ONLY: no orders, no watched file, no control write. GROSS only. Freeze intact.