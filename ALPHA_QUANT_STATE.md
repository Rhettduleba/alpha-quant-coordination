# Alpha Quant — State of Record

**Version:** 2.2
**Last updated:** 2026-05-19
**Owner:** Rhett
**Scope:** Current operational state, open verifications, recent decisions.
Stable rules and architecture live in the repo's `CLAUDE.md` files (auto-loaded by Claude Code).
Historical edits live in `CHANGELOG.md`.

> This file replaces `ALPHA_QUANT_STATE.md` v1.7. Slimmed deliberately — anything stable,
> architectural, or historical was moved out. If something here doesn't change session to
> session, it belongs in `CLAUDE.md` instead. If this file passes ~4 KB, prune.

---

## Operating rules (every session, both Claudes)

1. **Verify before asserting.** No system-state claim without reading the file. If unread, label it "unverified."
2. **Surface conflicts, don't silently resolve them.** When two sources disagree, flag to Rhett — don't pick.
3. **No process actions without approval.** Restart bot, kill PID, deploy code, edit risk config → propose first, act after.
4. **Push back honestly.** Don't soften objections. Don't fake disagreement to look critical either.
5. **End every report with "What I did NOT verify."** Explicit section. Catches confabulation.

---

## §1 Open verifications

| # | Verification | Trigger | Status |
|---|---|---|---|
| V1 | Prompt fix: 8 AM advisor run writes a control file **without** `BLOCK_ENTRIES_AFTER_TIME` | PRE_MARKET 2026-05-19 08:00 ET | PENDING |
| V2 | Freeze fix: PID 2360 survives the 8 AM advisor run with no new "Heartbeat stale" event | Same trigger | PENDING |
| V3 | TradeStation UI shows ~**$-378.70** for 2026-05-18 daily P&L (net broker fills) | Rhett checks TS UI | PENDING |
| V4 | Re-verify the 540-trade historical baseline using broker fills, not journal limit prices (journal was over-stating loss by ~$205 on the one day sampled) | Re-run reconciliation across the 22-day baseline window | PENDING |

V1 + V2 both close on the same observation (today's 8 AM advisor run). If V1 fails while V2 passes, the cause is likely memory-reinforcement (`advisor_memory.json` still nudges toward `BLOCK_ENTRIES_AFTER_TIME` despite the prompt edit). V3 needs Rhett to compare against the TS UI for 2026-05-18. V4 is bigger — re-run reconciliation across the 22-day baseline window once V3 confirms the methodology.

---

## §2 Recent decisions (last 7 days)

- **2026-05-19** — Inventoried TradeStation API endpoints available to our SIM token (probe results recorded in this conversation). Working: `/brokerage/accounts`, `/balances`, `/bodbalances`, `/positions`, `/orders`, `/historicalorders?since=`; `/marketdata/quotes`, `/symbols/{symbol}`, `/barcharts/{symbol}`, `/symbols/{symbol}/news`. NOT available on SIM token: `/executions`, `/fills`, `/activities`, `/transactions` (404), and `/marketdata/options/*` (403). `/historicalorders?since=` is capped at **600 orders per call** regardless of date — pagination required for windows longer than ~11 trading days at current volume.
- **2026-05-19** — Built scope S of the broker-truth library: added `get_pnl_for_date(date_str, account_id=None, client=None)` to `tradestation-bot/daily_reconciliation.py` (above the output helpers section). Returns a dict with `gross_pnl`, `commissions`, `routing_fees`, `net_pnl`, `fill_count`, `closed_pair_count`, `fills`, `closed_pairs`, `source="TRADESTATION_HISTORICAL_ORDERS"`. Smoke-tested against 2026-05-18: returns `net_pnl = $-378.70`, matching the full reconciliation script. Any caller inside the bot repo can now `from daily_reconciliation import get_pnl_for_date`. Cross-repo (advisor → bot) import is NOT enabled by S — would require sys.path manipulation, code copy, or a CSV bridge; covered by future scope M if needed.
- **2026-05-19** — Fixed three pre-existing bugs in `tradestation-bot/daily_reconciliation.py`: (1) was calling `/brokerage/accounts/{id}/orders` (current orders only, returns 0 for past dates) — switched to `/historicalorders?since=YYYY-MM-DD`; (2) `parse_broker_order` read `order["TradeAction"]` which doesn't exist top-level — now derives action from leg's `BuyOrSell` + `OpenOrClose` (Buy/Open → BUY, Sell/Close → SELL, SellShort/Open → SELLSHORT, BuyToCover/Close → BUYTOCOVER); (3) `compute_pnl_from_fills` processed fills in API-returned order (reverse-chrono), losing pair matches — now sorts chronologically; `reconcile` didn't mark fills as consumed, so duplicate journal entries collided on the same fill — now tracks `consumed_order_ids`. Also surfaced commissions ($52.60 for 2026-05-18) as a separate line. **For 2026-05-18: journal P/L was $-584.10, broker fills gross $-326.10, broker fills net of fees $-378.70.** Reconciliation now 34/34 matched, 0 unmatched on either side.
- **2026-05-19** — Rule set for the project: Claude Code executes every read-only / local-analysis / coordination-repo action without asking. Still propose-first for: restart bot, kill PID, deploy bot code, edit risk config / risk floors / control vocabulary, modify advisor control files the bot reads.
- **2026-05-19** — SOR process slimmed. STATE.md v2.0 replaces ALPHA_QUANT_STATE.md v1.7. Single-machine + single-toolchain commitment retires cross-machine concerns. CHANGELOG.md is now the running edit log.
- **2026-05-18** — Prompt-builder edit: removed two `BLOCK_ENTRIES_AFTER_TIME` nudges (formerly lines 61–64 of `ai-trading-strategy-agent/src/advisor/prompt_builder.py`). The control type stays in the vocabulary (line 52); independent reasoning can still emit it. Behavior change first visible at PRE_MARKET 2026-05-19 08:00 ET.
- **2026-05-18 17:35 ET** — Watchdog auto-restarted bot from frozen PID 5468 (pre-fix code, launched 16:07 ET) to PID 2360. PID 2360 is the first instance running the fixed `run_bot.py` (Option B — heartbeat-while-waiting + orphan reaper).

---

## §3 Active proposals

_None tracked yet. Populate from `ai-trading-strategy-agent/outputs/proposals/` when a proposal is awaiting Rhett's approval. Format per row: filename, one-line summary, the blocking question for Rhett._

---

## §4 Current bot / advisor state

- **Bot:** PID **2360**, alive, last_seen `2026-05-19 06:06:38 ET`, loop_count `2632`.
- **Advisor last run:** `2026-05-18 16:33 ET` (PM_AFTER). Control file TTL valid through `2026-05-19 16:33 ET`.
- **Advisor next scheduled:** `2026-05-19 08:00 ET` (PRE_MARKET) — closes both open verifications.
- **Heartbeat-stale events on 2026-05-19:** 0.
- **Active controls in force** (from `advisor_control_latest.json`):
  - `BLOCK_ENTRIES_AFTER_TIME` 11:00 ET *(pre-fix; expected to disappear after the 8 AM run)*
  - `BLOCK_SYMBOL` × 6: MU, BA, META, JNJ, UNH, MSFT
  - `REQUIRE_MIN_NEG_CHANGE_PCT` −1.5%
  - `SET_MAX_POSITION_PCT` 0.15
  - `REDUCE_MAX_POSITIONS` 2

---

## §5 How to maintain this file

- Edit STATE.md when state changes; append one dated line to `CHANGELOG.md`.
- Roll §2 entries older than 7 days into `CHANGELOG.md`.
- Bump the version on every edit (2.0 → 2.1 → 2.2 …).
- Don't grow this file. If it passes ~4 KB, something belongs in `CLAUDE.md` or `CHANGELOG.md` instead.
- Architecture, risk floors, control vocabulary, SIM guards, working rules → all already in the project `CLAUDE.md` files. Do not duplicate here.
- C1 (`AQ_EVALUATION_STANDARDS_C1.md`) is fetched only when evaluating a proposal — not at ramp-up.
