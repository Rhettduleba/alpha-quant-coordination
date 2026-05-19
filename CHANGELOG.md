# Alpha Quant — Changelog

Append-only log of edits to `STATE.md`. Newest first. Format: `**YYYY-MM-DD** — STATE.md vX.Y — one-line summary.`

This file is **not** fetched at ramp-up. Consult only when answering "what changed last week" or rolling §2 entries off STATE.md.

---

- **2026-05-19** — File swap — Renamed `STATE.md` → `ALPHA_QUANT_STATE.md` and the previous v1.7 → `ARCHIVE_ALPHA_QUANT_STATE_v1.7.md`. Browser Claude's existing raw-URL fetch (`.../main/ALPHA_QUANT_STATE.md`) now returns the slim v2.2 content instead of v1.7. v1.7 preserved as archive for history.
- **2026-05-19** — STATE.md v2.2 — Recorded the TradeStation API endpoint inventory (which endpoints work on the SIM token, which don't, and the 600-order cap on `historicalorders?since=`) and the completion of scope S of the broker-truth library (`get_pnl_for_date()` added to `daily_reconciliation.py`, smoke-tested to match `$-378.70` for 2026-05-18). Triggered by Rhett asking which TS data could replace local journal-based reconstruction.
- **2026-05-19** — STATE.md v2.1 — Added §1 V3/V4 (TS UI P&L confirmation + 540-trade baseline re-verify) and §2 entries for the daily_reconciliation.py three-bug fix and the new "just do the work" rule. Trigger: Rhett asked to verify TradeStation P&L matches the bot's, exposing two endpoint/parsing bugs and one matching-algorithm bug; commissions ($52.60/day on 2026-05-18) are now surfaced separately.
- **2026-05-19** — STATE.md v2.0 — Created. Replaces `ALPHA_QUANT_STATE.md` v1.7. Slimmed from ~31 KB to ~3 KB. Dropped: the "Roman" confabulation anecdote, cross-machine sections, role definitions, embedded performance baselines, full §8 operating-rule prose (kept slim 5-rule version), §10 sync protocol (single-machine + single-toolchain commitment retires it). Trigger: Rhett's 2026-05-19 commitment to one machine + Claude Code + browser Claude only, plus observed WebFetch fidelity issues on v1.7 ramp (paraphrase silently, refusal noisily).
