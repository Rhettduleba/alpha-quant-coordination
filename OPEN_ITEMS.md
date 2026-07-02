# OPEN ITEMS — living tracker (Claude maintains; Rhett decides the ⭐ items)

_Last updated: 2026-07-02 ~2:20 PM ET. I keep this current and re-surface the ⭐ items so nothing gets dropped._

## ⭐ DECISIONS AWAITING RHETT (need your input — nothing happens until you choose)
_(none open right now)_

## 🔬 IN PROGRESS (I'm investigating; will bring you findings)
- **TW (Tape Watcher) efficiency tuning** — the tick-stream is 92% stream-gaps (up to 46s), defeating tick-precision. Root-cause + tuning plan in flight (workflow wmlsplf16). I'll bring the ranked fixes; deploy carefully since the TW is the live exit owner.

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
