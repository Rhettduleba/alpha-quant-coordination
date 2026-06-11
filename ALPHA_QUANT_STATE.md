# Alpha Quant — State of Record

**Version:** 3.9
**Last updated:** June 11, 2026
**Owner:** Rhett
**Scope:** Current operational state, open items, recent decisions. Stable rules/architecture live in the `CLAUDE.md` files. Historical detail lives in `CHANGELOG.md`.
**Supersedes:** v3.8 (June 8) — predated the candle-close exit deploy, the mover scanner, `falsification_gauntlet`, the H5 quarantine, and ORB multi-scan. Updated from Claude-Code-verified live facts (Loops #16–24, 2026-06-10/11). See the `Current snapshot` section below.

---

## Operating rules (every session, both Claudes)

1. **Verify before asserting.** No system-state claim without reading the file. Label unread claims `unverified`.
2. **Verify every loose end.** "What I did NOT verify" is a list to CLOSE now, not an escape hatch — only genuine reach limits (needs a live session / broker data not yet produced) may remain.
3. **Surface conflicts, don't silently resolve them.** Flag to Rhett.
4. **No process actions without approval.** Restart bot, kill PID, deploy, edit risk config → propose first.
5. **Push back honestly.** Don't soften objections; don't fake disagreement either. Stress-test external-AI input, don't process it as a to-do list.
6. **HARDENED 2026-06-10 (Rhett, overrides the old rule): NEVER output a "What I did NOT verify" section.** Verify everything reachable — pull the real number, don't estimate. The only residual is a fact that physically cannot exist yet (a future live session); state it as a next action, not a hedge-list.
7. **One question per turn to Rhett.**
8. **User-facing times: 12-hour clock + AM/PM ET.**
9. **Measure ≠ fix. Plumbing freeze:** zero trading-behavior change unless a task explicitly authorizes it (write-only logging is allowed; order logic is not).
10. **Broker truth > internal logs.** Cite the highest evidence source; don't infer a cause from a pattern.
11. **Copiable handoffs.** Replies destined for Planning Claude / other AIs are rendered as a full copy-paste markdown block.

---

## Current snapshot (verified 2026-06-11, pre-open)

**Architecture — the 3-AI loop:** Rhett relays numbered handoffs between *Planning Claude* (the browser/app strategist) and *Claude Code* (this VPS node — empirical, executes + verifies + replies in markdown). Claude Code's verified findings outrank either AI's reasoning. Two apps: `tradestation-bot/` (the bot — narrow, reviewable, places SIM orders) and `ai-trading-strategy-agent/` (the advisor — research/analysis). Coordination repo: `C:\repos\alpha-quant-coordination` (this file = source of truth). Live root: `C:\AlphaQuant` (OneDrive = backup-only).

**Accounts:**
| Account | Type | Status |
|---|---|---|
| SIM1623888M | equities (Margin) | **ACTIVE** — ORB lives here |
| SIM1623889F | futures | **DISABLED** — H5 quarantined via `h5_disabled.flag`; flat |
| SIM1623890X | Forex | **CLOSED** |
- Mover scanner has **no dedicated account** — the separate-account path is abandoned (no spare equities account exists; `mover_trader.py` stays INERT until one is created).

**Strategies & status:**
- **ORB** (`orb_runner.py`, 888M) — **LIVE**. 09:35 opening-range breakout, RelVol-ranked. Candle-close exit **deployed** (`d3f7e05`). Multi-scan (hourly re-arm) **built, flag OFF, deploy pending after close** (Loop #23).
- **Mover scanner** (`mover_scanner.py`) — **SHADOW/LOG-ONLY**, hourly scheduled task. De-biased RelVol. Places no orders.
- **H5** (`run_h5.py`, 889F) — **QUARANTINED** (flag present), flat. Known bug: EOD flatten sets `eod_flattened` on submit-not-fill (fix owed before re-enable).

**Active flags (what ON vs OFF does):**
| Flag | Value | Meaning |
|---|---|---|
| `ORB_EXIT_MODE` (risk_config) | `candle_close` | `candle_close` = 0.15×ATR Phase-1 → confirm → first-opposite-1min-candle close → 1.0×ATR catastrophe. `legacy` = old 0.10×ATR tick stop (instant rollback). |
| `ORB_MULTISCAN` (risk_config) | `False` | `True` = re-arm at 10:35/11:35/12:35/13:35/14:35 (`ORB_SCAN_WINDOWS`), tagged by window. `False` = once-a-day 09:35 ORB only. |
| `MOVER_LIVE` (mover_trader) | `False` | `True` = scanner places live-SIM orders (needs an account). `False` = dry-run/log. |
| `MOVER_TRADE_ACCOUNT` | `""` (unset) | The SIM equities account for the scanner. Unset = mover_trader places nothing. |
| `h5_disabled.flag` (file) | present | Present = H5 places no new entries. Delete to re-enable. |

**Detail (bug log, key findings, open items, onboarding):** see `ONBOARDING_AND_FINDINGS.md` in this repo.

---

## §0 Environment (verified 2026-06-08)

- **Live root: `C:\AlphaQuant\`.** VPS migration DONE. OneDrive (`…\Trade station Main`) is **backup-only**. All work targets `C:\AlphaQuant` via absolute paths.
- **`C:\AlphaQuant` is NOT a git repo** — the live code lost version control in the migration. See Go-Live Safety Checklist + OPS-3: **this is now a prerequisite to fix before the first trading-behavior change** (the reject fix must be reversible).
- Both engines running, supervised: ORB `run_bot.py` (PID 10808, restarted 6/08 08:10) → subprocesses `orb_runner.py` each cycle (so logging-code edits auto-load with no restart). H5 `run_h5.py` (PID 7324) imports `h5_runner` once and loops 30s (holds imports until restarted). Chain: runners ← `watchdog_supervisor` (3524) + `h5_supervisor` (6544) ← `Supervisor Guardian` task (2-min) ← OS Task Scheduler.
- Advisor (`run_advisor.py`) live ~3×/day (08:0x / 12:0x / 16:31 ET), real tokens, mostly `parse_errors:0`.
- Accounts flat AM 6/08; ORB ~$990k, H5 ~$1.00M. Preflight `_preflight_diagnostic.py` = 45/46 pre-open (the lone FAIL `scan_completed=False` is correct before 9:35; clears post-scan). CSHV 0 FAIL. Heartbeat at `C:\AlphaQuant\bot_heartbeat.json`, atomic-written (transient read-miss = the temp+replace window, not a fault).

## §1 Honest system state

- **No validated edge. Net-negative in SIM.** **Success = genuinely good-quality trades producing a positive P&L, with trade QUALITY weighted above dollar magnitude** — Rhett doesn't care whether it's $400 or $4,000 as long as the trades are sound. SIM account resets when a winning, bug-free system is confirmed.
- The "longs profit / shorts lose" asymmetry is **unproven and unstable** — it inverted on 6/05 and the journal is phantom-contaminated. Do not act on it.
- **P0 (broker-truth ingestion) is the gate** for utilization, reject attribution, capital deployment.

## §2 P0 status (active work)

- **Tier-1 code-complete.** `broker_fill_logger.log_new_terminal_orders()` (`broker_fill_logger.py:371`) wired into `orb_runner.py:604` + `h5_runner.py:327` → `tradestation-bot/broker_orders_unified.csv` (all terminal states). Reject-half **proven**; fill-half **unproven** — no live ORB session since wiring (mtime 6/06 08:11). The file having only ever held 4 weekend `h5_v1` REJECTED rows and never any ORB rows is **`reasoned`** (content was 4 h5 rejects when first read; no backup holds ORB rows; wiring post-dated Friday's close) — NOT `verified` via creation-time/git (no version control; the migration rewrote the birth time).
- **Tier-2 diagnostic fields added 2026-06-07 (write-only; `broker_fill_logger` join only — no order-path change; verified additive via mtimes):** `broker_response_time` (OpenedDateTime), `market_price_ref_at_submit` (broker `PriceUsedForBuyingPower` — proxy **validated 6/08**: weekend value 7429.5 sat within ~0.4% of MES Fri close 7400.5 / Mon 7456; trustworthy as a near-submission reference, live-tick confirmation comes from today's rejects), `submit_time` + `signal_trigger_px` (join from `fill_quality` by order_id). 19-col schema; file migrated; ORB auto-loads 6/08; H5 picks up on next restart.
- **Deferred (would touch order path):** true NBBO `market_price_at_submit`; distinct `signal_time` (≈ submit_time).
- **Monday harness ready:** `tradestation-bot/p0_verify_harness.py` (measure-only). `--live` = `historicalorders` API (independent FILLS ref; **excludes rejects**); `--export <csv>` = TS executed-orders download (reject-inclusive). Validated end-to-end on real 6/05 data.
- `intended_price` = STOP for ORB stop-limit — **verified** (unit-tested 66.95 vs limit 66.98).

## §3 Phantom-fill bug — contained but ARMED

- `fill_quality` writes `status="FILLED"` + placeholder `fill_px` at submit (`orb_orders.py:152,308`; `h5_orders.py:143`). Not truth.
- Audit (6/07): `slippage_recalibrator` reads it as truth but has never run + output unused; advisor reads `trade_journal`, not `fill_quality`; `slippage_tracker` uses real fills. **No live decision currently poisoned.** Containment: do NOT run `slippage_recalibrator` until fills are real.

## §4 Sequencing (decided)

P0 verify (post-close harness) → **measure** (time-weighted utilization; idle-capital by cause; per-side & per-reject attribution) → **diagnose rejects** (`H-REJECT-STOPSIDE-01`, diagnostic only) → **fix the leak** (Stage-5, pre-registered, only if a fixable construction/timing fault; **gated on OPS-3 git so it's reversible**) → **decide if a replacement queue is needed** (dry-run, gated on fill-selection-bias) → **rotation** (gated on `H-SCORE-RANK-01`). $400k deployment amplifies a negative edge — gated on proven positive expectancy.
- **Post-P0 item:** the advisor has **no real fill prices for the live strategies** — it reads `trade_journal`, which only gets `BROKER_FILL` rows from the dormant `bot_loop` (the runners use `log_new_terminal_orders`, which does not mirror to the journal). Once broker-truth fills exist, **repoint the advisor at `broker_orders_unified.csv`**.
- **Gated / out of scope now:** utilization engine, replacement queue, rotation, fixing invalid-stop, fixing `fill_quality` writes (contain not fix), any sizing/entry/exit/veto/news/VWAP change.

## §5 Pre-registered hypotheses (descriptive first; tiny samples)

`H-REJECT-STOPSIDE-01` (invalid-stop timing race / fill-selection bias; diagnostic only); `H-ORB-OUTLIER-01`; `H-ORB-LONG-ONLY-01` (after costs); `H-VWAP-CONFIRM-01` (log-only); `H-VIX-ORB-01 / H-NR4-*` (descriptive only, no broad regime battery); **H5 signal integrity + session/window discipline** (6/05 08:15 pre-market + weekend "session closed" submissions → audit, don't hot-fix); `H-SCORE-RANK-01` (gates rotation); `H-RECYCLE-01`.

## §6 Latest verified results

- **2026-06-05:** 20 ORB candidates → 8 filled / 8 rejected / 4 untriggered; ORB −$107.81 (longs −$190.91, shorts +$83.10); H5/MES +$492.15 (one EOD-held short); day +$384, −$111 ex-outlier. 5/8 entries triggered far too late (no entry cutoff). Protective stops are Market, slipped 3–9¢.
- **6/05 untriggered-order counterfactual (verified 6/08 from TS minute bars):** all 4 buy-stops were **DODGED BULLETS, no fill-bug** — none crossed its trigger, all closed below it. APP (trig 595.30, high 588.49, close 557.11), UNH (404.24 / 402.96 / 399.70), PNR (73.91 / 73.74 / 73.17), HUM (352.05 / 350.97 / 349.64). The buy-stop mechanism correctly avoided 4 would-be losers.

## §7 Risk config (verified, SIM) + inconsistencies

`DAILY_MAX_LOSS` intentionally **SIM-disabled** (=$1e9). MAX_LOSS_PER_TRADE $750 (benchmarked to the old $2k daily cap); STRATEGY_MAX_LOSS $500/strategy/day; ACCOUNT_DD_KILL 5%; STRATEGY_DD_KILL 10%; MAX_TRADES_PER_DAY 30; MAX_LEVERAGE 4.0; ORB sizes off intended LIVE $100k base; ORB v1.6 stop-limit, 5 bps collar, parallel scan.

- **CONFIRMED inconsistency:** MAX_LOSS_PER_TRADE ($750) **exceeds** STRATEGY_MAX_LOSS ($500/day) — a single trade can lose more than its strategy's whole daily cap. Different scopes (per-trade vs per-strategy-day) do NOT resolve it because the per-trade cap is the larger of the two. Also unconfirmed whether STRATEGY_MAX_LOSS is wired into enforcement. **Resolve before live.**

## Go-Live Safety Checklist (disarmed brakes — fix BEFORE any live capital)

1. **DAILY_MAX_LOSS is OFF in SIM** (=$1e9). Restore **$2,000** AND harden to a **real-time intraday clamp** (today it's scan-time only for ORB; H5 never used it).
2. **ACCOUNT_DD_KILL measures against the wrong base.** It computes 5% off the account-equity HWM (`hwm_account.json` ≈ $1,000,651, the SIM balance) → trips at **~$50k**, ~10× looser than the intended ~$5k (5% of the $100k real base). **Re-base to the $100k real-capital base before live.** (Same question applies to STRATEGY_DD_KILL.)
3. **MAX_LOSS_PER_TRADE $750 > STRATEGY_MAX_LOSS $500** (see §7) — reconcile + confirm enforcement.
4. **Live code under version control (OPS-3)** — prerequisite before the first behavior change so fixes are reversible.

## §8 Open ops items

| # | Item | Impact |
|---|---|---|
| OPS-1 | `Volume Capture` task `LastResult=2`; `data/universe/volume_history.json` stale since 5/29 | Advisory ADV filter only; ORB unaffected (uses its own `orb_or_vol_state.json`, fresh 6/05). Fix the task. |
| OPS-2 | CSHV `scheduled_task_last_run_recent` WARN is a false positive (checks disabled legacy `AlphaQuantBot`, not the active supervisor) | Noisy WARN can mask a real one. Repoint. |
| **OPS-3** | **Live code not under git (`C:\AlphaQuant`)** | **ELEVATED: prerequisite before the first trading-behavior change — the reject fix must be reversible.** |
| OPS-4 | V1 `src/main.py` dashboards stale since 5/11 (pipeline dormant) | The operational `run_advisor.py` loop is the live one. |

## §9 Maintenance

Edit on state change; append a dated line to `CHANGELOG.md`; roll >7-day entries into `CHANGELOG.md`; bump version every edit. Keep architecture/risk-floors/control-vocabulary in `CLAUDE.md`, not here.
