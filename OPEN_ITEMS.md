# OPEN ITEMS — living tracker (Claude maintains; Rhett decides the ⭐ items)

_Last updated: 2026-07-02 ~2:20 PM ET. I keep this current and re-surface the ⭐ items so nothing gets dropped._

## ⭐ DECISIONS AWAITING RHETT (need your input — nothing happens until you choose)
_(none open right now)_

## 🔬 IN PROGRESS (I'm driving these)
- **Shadow TOURNAMENT (9 exit variants) + /tunes dashboard tab** -- click a tune -> P&L; leader V8pw_wide +$2,024/0-cut in-sample. Entry tunes still need the winner-backtest (some data-blocked). Accumulating OOS daily. [was: multiple exit tunes] -- shadow_tournament.py scores V0/V8/V8p/V10 apples-to-apples, daily EOD accumulation (shadow_tournament_log.jsonl), SHADOW-only. Initial in-sample: V8 fails must-not-cut; **V8p_protected +$1,219/0-cut** and V10 +$804/0-cut are the promising leads. Accumulating OOS; promote only OOS+N>=30+0-cut+net-positive vs V0.
- **TW tuning rollout** (investigation DONE). Root cause: TW reads last-*trade* price only, blind to the mid moving between prints → ~a duplicate of the poller, no real edge (lost 8/9 exits on 7/02). NO safety hole (always covered by poll + time-stop + resting stop). ROLLOUT I'm driving: (a) **after 4pm today** deploy the safe detection fixes (reconnect-reset, honest gap metric, dense tick side-channel = bonus backtester price path) + restart TW per discipline; (b) **tomorrow RTH** shadow-validate the mid-feed fix (fire=False alongside live, diff exit timing); (c) **after tomorrow's close** arm the mid-feed. Never restart the live exit owner during RTH.

## ⭐ DECISIONS AWAITING RHETT
- **PROP-TS-TRANSIENT-LABEL** (WATCHED file orb_runner.py -> needs your go): a transient TS 504 is mislabeled `TS_AUTH_FAIL/FAIL` (should be WARN/transient). Verified benign 7/02 but it false-alarms 'API key failing' on every TS server hiccup. One-line classify fix, alerting-only. `outputs/proposals/PROP-TS-TRANSIENT-LABEL-2026-07-02.md`.
- **PROP-LIVE-QUOTES** (you asked me to draft — DONE, awaiting your approval): switch QUOTES to the live market-data feed, orders stay 100% SIM, hard config split. The real fidelity ceiling for tick-level exits + a true backtester tape. `ai-trading-strategy-agent/outputs/proposals/PROP-LIVE-QUOTES-2026-07-02.md`.
- **Smaller TW calls (I'll bring these with data, not urgent):** should TW own the 30-min time-stop or cede it to exit_bot_v2? · acceptable exit-timing shift from the mid feed (I'll show shadow-diff numbers) · promote tape_watcher.py to the watched-file set since it fires live exits?

## ✅ RESOLVED
- **Early-close half-days** (2026-07-02, Rhett delegated → my call): **SKIP** them (Nov 27, Dec 24 — thin holiday tape, not worth a watched change for ~2 days/yr). Bot already skips via holiday_reason; detector exempts them from the CRITICAL no-trade alarm (7/2 still fully covered). Non-watched; REG 29/0.

## 🔨 QUEUED BUILDS (no decision needed — I'll finish these start-to-finish)
2. **Exit-backtester MVP** (the shadow SIM, Phase 1): `fill_model.py` → `fidelity_gate.py` (must reproduce MU −$1,670 + COHR −$1,975) → run on the clean cohort's dense days. Foundation done (clean_cohort + fill calibration + price-path feed). I take this to completion when we turn back to the sim.
3. **Forward live-shadow** (shadow SIM Phase 2): GATED — build only after the exit-backtester's fill model validates (else it launders SIM-fill optimism forward).

## 🧪 PENDING VALIDATION (live in SIM, but in-sample — not yet "trusted")
4. **30-min unconfirmed time-stop** — LIVE in SIM (Loop 220). In-sample/directional. Keep/promote verdict needs OOS forward data + N≥30 unconfirmed on the re-arm path. Watching daily.
5. **9:45 AM re-arm window** — LIVE (Loop 218); first real day 7/02. Track its expectancy vs the 10:35+ windows; PULL "0945" if it underperforms (~2 weeks / N≥20).

## 🚦 BEFORE-LIVE GATES (not now — required before ANY real-money step)
6. Restore `DAILY_MAX_LOSS` ($2k) + 5% account-DD kill + a real-time intraday loss clamp (all OFF for SIM).
7. Build the **4x-marginable universe** (B2) so we only trade names we can leverage 4x on TS margin.

## 📁 OLDER PARKED DECISIONS (from the 6/27 SESSION_LOG state block — may be partly stale)
Pre-open-gate arming (SAFE_MODE_ENFORCE), OR-distance entry add, earnings-feed refresh, post-test gauntlet → promote-one-lever → fresh 5-clean-day test, and "does a kill day count toward the 5-clean-day bar?" — I can reconcile these against current state and tell you which are still real whenever you want.
