# SYSTEM_FACTS — live mechanics, machine-generated from the running code/config/broker-truth

> **Generated:** 2026-06-28 11:27:37 Eastern Daylight Time · **coordination-repo HEAD:** `68af0d5` · by `strategy-research/system_facts.py` (read-only).
> Every value below is READ from a real source (the live import for the VALUE; a fresh file scan for the SOURCE file:line). Nothing is hand-typed. A field that can't be derived says `UNVERIFIED`.
> If this contradicts memory, THIS wins — regenerate it (re-run the script) rather than trusting recall.

## STATE
| Fact | Live value | Source |
|---|---|---|
| Live exit mode | candle_1.4atr_chandelier | `tradestation-bot/risk_config.py:60` |
| SAFE_MODE_ENFORCE (gate teeth) | False | `tradestation-bot/risk_config.py:188` |
| consecutive_clean streak | 0 | `validation/clean_day_certifier.py:consecutive_clean()` |
| Posture / freeze + last forward-test | human-maintained record (not a code constant) -- read the CURRENT STATE block | `SESSION_LOG.md (FINDINGS & TEST RESULTS LEDGER + CURRENT STATE)` |

## ENTRY
| Fact | Live value | Source |
|---|---|---|
| Universe size today (published) | 145 | `ai-trading-strategy-agent/outputs/advisor_guidance/advisor_universe_latest.json:universe_size` |
| Universe generated_at | 2026-06-26T07:30:28.229842-04:00 | `advisor_universe_latest.json:generated_at` |
| Universe source | research_brain_v1 | `advisor_universe_latest.json:universe_source` |
| Relative-strength pool size | not in the published artifact -- see research-brain build log | `UNVERIFIED` |
| Re-arm path enabled (ORB_MULTISCAN) | True | `tradestation-bot/risk_config.py:76` |
| Re-arm window times | ['1035', '1135', '1235', '1335', '1435'] | `tradestation-bot/risk_config.py:79` |
| 9:35 open scan | the once-a-day Zarattini 5-min ORB (orb_runner owns it; NOT a re-arm window) | `tradestation-bot/orb_runner.py:4 (module docstring)` |
| Strategy / breakout trigger | Zarattini 5-min Opening-Range Breakout: long on break of OR high, short on break of OR low | `tradestation-bot/orb_runner.py:459-460 (or_high/or_low) + :4 docstring` |
| Opening-range window | first 5 min (09:30->09:35 ET); scan/arm at 09:35:30 | `tradestation-bot/orb_runner.py:9-12 (timeline)` |
| In-play gate (RelVol/move/$-vol) | True  (ON) | `tradestation-bot/risk_config.py:259` |
| HTB/halted exclusion | True  (ON) | `tradestation-bot/risk_config.py:289` |
| Earnings veto | live-invoked in 9:35 path; fails OPEN on stale/missing calendar | `tradestation-bot/orb_runner.py:441 (is_earnings_blackout call) + orb_earnings_veto.py` |
| Deploy-controller scope | True -- governs the RE-ARM/multiscan admit ceiling only; 9:35 ORB sizes by its own constants | `tradestation-bot/risk_config.py:238` |
| Deploy base | $400,000 | `tradestation-bot/risk_config.py:237` |
| Deploy target % | 0.95 | `tradestation-bot/risk_config.py:241` |
| Deploy target $ (computed live) | $380,000 | `deploy_controller.deploy_target() = DEPLOY_BASE * DEPLOY_TARGET_PCT` |
| Per-position notional cap | $25,000 | `tradestation-bot/risk_config.py:242` |
| Per-side cap | 0.50 ($200,000/side) | `tradestation-bot/risk_config.py:243` |
| Max open positions (count backstop) | 16 | `tradestation-bot/risk_config.py:86` |

## EXIT
| Fact | Live value | Source |
|---|---|---|
| Resting broker stop distance | 1.4 x ATR  (StopMarket) | `tradestation-bot/orb_runner.py:98` |
| Resting stop -- WHEN placed | post-fill management pass keyed on the 9:35 entries_submitted list (NOT atomic with entry; re-arm fills get none) | `tradestation-bot/orb_runner.py:960-992 (submit_stop_loss_exit)` |
| Confirmation threshold | 0.15 x ATR favorable | `tradestation-bot/candle_close_exit.py:24` |
| Chandelier trail multiple | 1.4 x ATR (ratchet-favorable-only floor) | `tradestation-bot/candle_close_exit.py:60` |
| Candle-close trail (post-confirm) | after confirm, exit on first opposite-color 1-min close; live exit = earlier of (chandelier) OR (candle-close) | `tradestation-bot/candle_close_exit.py:63-68 (chandelier_decision docstring)` |
| Catastrophe stop (legacy candle_close mode) | 1.0 x ATR | `tradestation-bot/candle_close_exit.py:25` |
| EOD forced-flatten time | 15:50 ET (3:50 PM) | `tradestation-bot/market_hours.py:68 + tradestation-bot/market_hours.py:69` |

## STOP COVERAGE
| Fact | Live value | Source |
|---|---|---|
| Entries with a broker resting stop | 107/282 = 37.9% | `strategy-research/stop_coverage_audit.py (re-derived from broker_orders_unified.csv)` |
| 9:35 cohort coverage | 107/111 = 96% | `stop_coverage_audit.py` |
| Re-arm/late cohort coverage | 0/171 = 0% | `stop_coverage_audit.py` |
| Median placement latency | 430s (~7.2 min) | `stop_coverage_audit.py` |
| PRIMARY protection mechanism | software poll (exit_bot_v2 + chandelier)  (mechanisms: {'resting_stop_HIT': 29, 'candle/chandelier': 209, 'eod_flatten': 44}) | `stop_coverage_audit.py exit-mechanism tally` |

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
