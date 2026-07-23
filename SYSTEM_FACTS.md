# SYSTEM_FACTS — live mechanics, machine-generated from the running code/config/broker-truth

> **Generated:** 2026-07-23 16:50:57 Eastern Daylight Time · **coordination-repo HEAD:** `5281fcd` · by `strategy-research/system_facts.py` (read-only).
> Every value below is READ from a real source (the live import for the VALUE; a fresh file scan for the SOURCE file:line). Nothing is hand-typed. A field that can't be derived says `UNVERIFIED`.
> If this contradicts memory, THIS wins — regenerate it (re-run the script) rather than trusting recall.

## STATE
| Fact | Live value | Source |
|---|---|---|
| Live exit mode | candle_1.4atr_chandelier | `tradestation-bot/risk_config.py:60` |
| SAFE_MODE_ENFORCE (gate teeth) | False | `tradestation-bot/risk_config.py:220` |
| consecutive_clean streak | 2 | `validation/clean_day_certifier.py:consecutive_clean()` |
| Posture / freeze + last forward-test | human-maintained record (not a code constant) -- read the CURRENT STATE block | `SESSION_LOG.md (FINDINGS & TEST RESULTS LEDGER + CURRENT STATE)` |

## ENTRY
| Fact | Live value | Source |
|---|---|---|
| Universe size today (published) | 139 | `ai-trading-strategy-agent/outputs/advisor_guidance/advisor_universe_latest.json:universe_size` |
| Universe generated_at | 2026-07-23T07:30:36.223010-04:00 | `advisor_universe_latest.json:generated_at` |
| Universe source | research_brain_v1 | `advisor_universe_latest.json:universe_source` |
| Relative-strength pool size | not in the published artifact -- see research-brain build log | `UNVERIFIED` |
| Re-arm path enabled (ORB_MULTISCAN) | True | `tradestation-bot/risk_config.py:76` |
| Re-arm window times | ['0945', '1035', '1135', '1235', '1335', '1435'] | `tradestation-bot/risk_config.py:85` |
| 9:35 open scan | the once-a-day Zarattini 5-min ORB (orb_runner owns it; NOT a re-arm window) | `tradestation-bot/orb_runner.py:4 (module docstring)` |
| Strategy / breakout trigger | Zarattini 5-min Opening-Range Breakout: long on break of OR high, short on break of OR low | `tradestation-bot/orb_runner.py:459-460 (or_high/or_low) + :4 docstring` |
| Opening-range window | first 5 min (09:30->09:35 ET); scan/arm at 09:35:30 | `tradestation-bot/orb_runner.py:9-12 (timeline)` |
| In-play gate (RelVol/move/$-vol) | False  (OFF) | `tradestation-bot/risk_config.py:291` |
| HTB/halted exclusion | True  (ON) | `tradestation-bot/risk_config.py:335` |
| Earnings veto | live-invoked in 9:35 path; fails OPEN on stale/missing calendar | `tradestation-bot/orb_runner.py:441 (is_earnings_blackout call) + orb_earnings_veto.py` |
| Deploy-controller scope | True -- governs the RE-ARM/multiscan admit ceiling only; 9:35 ORB sizes by its own constants | `tradestation-bot/risk_config.py:270` |
| Deploy base | $400,000 | `tradestation-bot/risk_config.py:269` |
| Deploy target % | 0.95 | `tradestation-bot/risk_config.py:273` |
| Deploy target $ (computed live) | $380,000 | `deploy_controller.deploy_target() = DEPLOY_BASE * DEPLOY_TARGET_PCT` |
| Per-position notional cap | $25,000 | `tradestation-bot/risk_config.py:274` |
| Per-side cap | 0.50 ($200,000/side) | `tradestation-bot/risk_config.py:275` |
| Max open positions (count backstop) | 16 | `tradestation-bot/risk_config.py:92` |

## EXIT
| Fact | Live value | Source |
|---|---|---|
| Resting broker stop distance | min(1.4 x ATR, $500/qty)  (StopMarket; from-entry $-CAP ACTIVE, Loop 187 -- caps single-position loss at $500 from fill, broker-resting/stream-independent) | `tradestation-bot/orb_runner.py:101` |
| Resting stop -- WHEN placed | post-fill monitor on the shared entries_submitted list. 9:35 AND -- since Loop 155 (LIVE Mon 6/29) -- RE-ARM fills both register, so the proven monitor places ONE 1.4xATR resting stop per fill (re-arm coverage 0% -> ~100%). Not atomic with entry; cancel-on-flatten inherited. | `tradestation-bot/orb_runner.py:931-992 + orb_multiscan._register_rearm_resting_stops (Loop 155)` |
| Confirmation threshold | 0.15 x ATR favorable | `tradestation-bot/candle_close_exit.py:24` |
| Chandelier trail multiple | 1.4 x ATR (ratchet-favorable-only floor) | `tradestation-bot/candle_close_exit.py:60` |
| Candle-close trail (post-confirm) | after confirm, exit on first opposite-color 1-min close; live exit = earlier of (chandelier) OR (candle-close) | `tradestation-bot/candle_close_exit.py:63-68 (chandelier_decision docstring)` |
| Catastrophe stop (legacy candle_close mode) | 1.0 x ATR | `tradestation-bot/candle_close_exit.py:25` |
| Unconfirmed time-stop (Loop 220, LIVE 2026-07-01) | 30 min -> flatten if STILL UNCONFIRMED (favorable excursion never crossed +0.15xATR); confirmed positions UNTOUCHED. Fires in exit_bot_v2 for every open position incl. TW-owned (before the lease); reason TIME_EXIT_<N>M_UNCONFIRMED (does not count toward the 2-stops/day breaker). SIM-only, reversible via UNCONFIRMED_TIME_STOP_ENABLED. | `tradestation-bot/risk_config.py:161` |
| EOD forced-flatten time | 15:50 ET (3:50 PM) | `tradestation-bot/market_hours.py:74 + tradestation-bot/market_hours.py:75` |
| Live exit OWNER (Loop 155, LIVE Mon 6/29) | Tape Watcher (tape_watcher --live-exit) fires exits tick-fast via the proven flatten_symbol + holds the exit_ownership lease; exit_bot_v2 DEFERS for TW-owned names. no-double-exit is STRUCTURAL (flatten re-reads live qty -> no-op on flat, no flip). Resting stop = always-on dead-man backstop; lease TTL reclaim (45s) on TW death. | `strategy-research/tape_watcher.py (run_live fire) + tradestation-bot/exit_ownership.py + exit_bot_v2 skip-guard` |
| TW kill-switch (Loop 157) | create tradestation-bot/tw_abort.flag -> TW stands down + releases the lease (exit_bot_v2 resumes; resting stops stay); delete to resume. Read each cycle -- no restart/deploy. | `tradestation-bot/exit_ownership.py:abort_requested` |

## STOP COVERAGE
| Fact | Live value | Source |
|---|---|---|
| ** AS-OF | figures below are HISTORICAL (pre-Loop-155). Re-arm 0% is FIXED Loop 155 (LIVE Mon 6/29); re-arm coverage rises + latency drops from Monday once re-arm stops register + TW owns exits. | `SESSION_LOG.md Loop 155` |
| Entries with a broker resting stop | 498/673 = 74.0% | `strategy-research/stop_coverage_audit.py (re-derived from broker_orders_unified.csv)` |
| 9:35 cohort coverage | 274/278 = 99% | `stop_coverage_audit.py` |
| Re-arm/late cohort coverage | 224/395 = 57% | `stop_coverage_audit.py` |
| Median placement latency | 258s (~4.3 min) | `stop_coverage_audit.py` |
| PRIMARY protection mechanism | software poll (exit_bot_v2 + chandelier)  (mechanisms: {'resting_stop_HIT': 47, 'candle/chandelier': 562, 'eod_flatten': 64}) | `stop_coverage_audit.py exit-mechanism tally` |

## COSTS
| Fact | Live value | Source |
|---|---|---|
| Default commission model | per_share_standard | `ai-trading-strategy-agent/src/advisor/commission_model.py:23` |
| SEC fee per $ of sale proceeds | 2.0600000000000003e-05 | `ai-trading-strategy-agent/src/advisor/commission_model.py:26` |
| TAF_PER_SHARE | 0.000195 | `ai-trading-strategy-agent/src/advisor/commission_model.py:27` |
| REG_FEES_ASOF | 2026-06-14 (SEC eff 2026-04-04; FINRA TAF eff 2026-01-01) | `ai-trading-strategy-agent/src/advisor/commission_model.py:29` |
| Per-share commission schedule (per_share_standard) | $0.01/sh first 500, $0.006/sh after, $1.00 min/order; TS Select = $0 commission | `ai-trading-strategy-agent/src/advisor/commission_model.py:9-10 (docstring)` |

## UNVERIFIED fields (could not be derived from a real source)
ENTRY/Relative-strength pool size
