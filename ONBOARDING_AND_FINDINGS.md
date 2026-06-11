# Alpha Quant — Onboarding, Findings & Bug Log

**Last updated:** June 11, 2026 (Loop #24). Companion to `ALPHA_QUANT_STATE.md` (source of truth) and `CHANGELOG.md` (dated history). Read this to ramp fast and to avoid relitigating settled ground.

---

## 1. New-session onboarding (read in this order)

A fresh Planning Claude or Claude Code is productive in minutes by reading:
1. **`ALPHA_QUANT_STATE.md`** → `Current snapshot` section — accounts, strategies, active flags, architecture. The source of truth.
2. **This file** → §3 Key findings (don't relitigate), §4 Bug log (the look-back), §2 Open items.
3. **`CHANGELOG.md`** — only if you need "what changed and when" / a specific commit.
4. **`C:\AlphaQuant\CLAUDE.md`** — stable rules, the one-way advisor→bot channel, SIM-only guards, the control-type vocabulary.
5. For the bot internals: `tradestation-bot/orb_runner.py` (09:35 ORB), `candle_close_exit.py` (the exit), `risk_config.py` (flags + caps).

**The 3-AI loop:** Rhett relays numbered handoffs between Planning Claude (strategist) and Claude Code (this VPS node — executes/verifies/replies in markdown). Claude Code's verified findings outrank either AI's reasoning. Everything is SIM-only.

---

## 2. Open items / next

- **ORB multi-scan** (`c9525c2`, built, flag OFF): flip `ORB_MULTISCAN=True` + restart run_bot **after a close**; then tagged trades accumulate per window.
- **First LIVE candle-close exit fire** — verify at the next open (orders fire on candle closes, catastrophe attaches, rollback works).
- **After ~10 sessions** — run each scan-window's tagged P&L (and the mover-scanner shadow P&L by time-of-day bucket) through `falsification_gauntlet` (honest cumulative `n_trials`); prune dead hours/buckets with evidence.
- **H5 EOD-flatten fix** — verify the *fill*, not just the submit, before setting `eod_flattened`; manage any leftover position on a new day. Required before H5 comes off the sideline.
- **BRO/MMM cancel-noise guard** — skip EOD cancel if the order is already terminal (low priority).
- **Free news feed** (Alpha Vantage / Finnhub) — only IF catalyst tags prove to matter; all current keys (FMP/TS/Tiingo) have dead news.
- **Mover-aware exit (research)** — looser Phase-2 trail for genuine high-RelVol big movers (the SMCI tail); gauntlet-gated, designed off one anecdote — do not deploy on it alone.

---

## 3. Key findings / decisions (settled — don't relitigate)

- **The exit is the leak, not the entries.** 6/10: +$12 captured vs **$5,136 left on the table**, almost all from the old tight stop whipsawing correct calls. Drove the candle-close exit.
- **Long vs short, revised by broker truth.** Earlier reads said shorts are the loss source. 6/10 broker truth revised it: the big short loss (SMCI) was a **CORRECT call killed by the exit**, not a bad entry. The exit fix may rehabilitate the short side. **Do NOT add a short-exhaustion / short-block filter.**
- **Direction is unpredictable; volatility is predictable.** ORB works because it *reacts* to direction (breakout), it doesn't *predict* it.
- **ORB + relative volume** is the one intraday edge that survives rigorous testing (sam-bateman line of evidence). RelVol is the "in play" signal; it's weighted in the mover score and de-biased for time-of-day.
- **Everything gets validated through `falsification_gauntlet`** with an HONEST cumulative `n_trials` (count every variant tried). Non-parametric (sign-flip + bootstrap + Šidák), N≥30 floor, NET-of-cost OOS data only.
- **Execution/costs is the killer for small accounts** — worst in small-cap movers. On 6/10 commission ate **~75% of gross**. Sizing is off the intended LIVE $100k base, not the ~$993k SIM equity, so SIM fill/slippage transfers.
- **No working news feed** on any key we hold (FMP 403, TS 404, Tiingo 403). Catalyst tags are volume/gap only.
- **Rejected:** VWAP-direction entry filter (removed net winners); LLM-as-trader (kept the safety scaffolding only — `mover_trader.py` RiskGate — discarded the free-text-trading idea).

---

## 4. Bug / issues log (the look-back)

| Issue | Symptom | Root cause | Status |
|---|---|---|---|
| Exit-clipping | 6/10 $5,136 left on table; winners strangled, correct calls whipsawed | old 0.10×ATR tick stop fired mid-candle | **FIXED** — candle-close exit `d3f7e05` |
| H5 quarantine timing | 6/10 log shows a 10:00 short despite "disabled" | flag applied 12:53 PM, *after* that day's entry | **RESOLVED** — blocks from next session; flat |
| H5 EOD flatten | sidelined short left open overnight, `eod_flattened=True` | flag set on order **submit, not fill** (no verify) | **OPEN** — fix before re-enable; the stuck position was cleared 6/10 18:05 |
| Backup secrets | `.env` + token caches sitting in OneDrive plaintext | backup `/XF` only excluded `*.pyc` | **FIXED** 6/11 — excluded + purged + verified |
| XOM 6/10 reject | "stop price must be below current market" | stale entry level = scan-latency footprint, NOT hard-to-borrow | **MONITOR** |
| BRO/MMM EOD_CANCEL 400s | HTTP-400 retries at EOD | cancelling orders the broker already expired | **OPEN** (low) — "skip if terminal" guard |
| Scan latency (history) | ORB entries ~9:38 instead of ~9:36 | no HTTP connection pooling | **FIXED** — pooled GET session (186s→~60s) |
| Phantom fills (history) | journal "FILLED" at submit, P&L overstated | journal logs submissions, not broker fills | **CONTAINED** — broker truth is source of record; pre-5/26 data excluded |
| Planning `validation.py` | a DSR-based gauntlet built in the planning chat | never reached the repo | **SUPERSEDED** by `falsification.py` (non-parametric, preferred for fat tails) |

---

## 5. Operating discipline (inherited by every session)

- **Confidence labels** on every claim: `verified` / `reasoned` / `unverified`. Claude Code's empirical findings outrank either AI's reasoning.
- **HARDENED 2026-06-10 (Rhett):** NEVER output a "What I did NOT verify" section. Verify everything reachable — pull the real number, don't estimate. A fact that can't exist yet (future live session) is stated as a next action, not a hedge-list.
- **Broker truth > internal logs.** Cite the highest evidence source.
- **SIM-only phase.** No live capital. Behavior changes deploy behind a default-OFF flag, reversible, after the close when flat, verified (preflight + StartTime > file mtime).
- Every handoff is answered as a **copiable markdown block**.
- **Rhett:** plain English, 12-hour clock + AM/PM ET, honest pushback over agreement, one question per turn.
