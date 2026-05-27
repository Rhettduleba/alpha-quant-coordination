# HANDOFF — Alpha Quant Strategy Research (Post-H4 Failure)
## Written 2026-05-27 by Claude Code, for external AI review

---

## You are being brought into a live decision

The Alpha Quant project just received its first definitive Stage-5 backtest
result on a fully-specified strategy (H4, the faithful Zarattini ORB on
Stocks in Play). H4 **failed the works bar definitively** — PSR 0.095%
over 9,146 trades, -17.65% return vs SPY +100% over the same ~5-year
window. The Zarattini paper's claimed Sharpe 2.81 did NOT replicate.

We need your input on:
1. **Whether to retry H4 with the alternative position-sizing
   interpretation** ($20k slice / $200 risk vs the $5k slice / $50 risk
   we ran), OR
2. **Move on to a different strategy candidate** (C2-C6 in the menu, or
   a new proposal from you), OR
3. **Critique the live bot's current strategy** (described below) and
   propose targeted fixes to its structural math problem.

---

## NON-NEGOTIABLE CONSTRAINTS

Every proposal MUST respect these hard rules. Anything outside them is
invalid and gets thrown out without further review.

### Trading style
- **DAY TRADING ONLY.** Intraday entries, intraday exits. **NO overnight
  positions, EVER.** All positions must be flattened by end of day.
- **EOD flatten by 3:50 PM ET** (G1, mandatory). The bot's `before_market_close(spy, 10)`
  schedule auto-adjusts to 12:50 PM on early-close days (Black Friday,
  day before holidays).
- **No entries before 10:00 AM ET** (audit-driven: 09:00-09:59 hour was
  42% win rate, vs 78% at 12:00, vs 100% at 14:30-15:29).
- **No entries after 3:30 PM ET.** EOD flatten runs at 3:50, that 20-min
  buffer is for normal-exit logic to work before forced flatten.

### Capital & risk
- $300,000 funded TradeStation SIM account.
- 4× FINRA intraday margin (up to $1.2M buying power).
- Lab backtests scaled to $100k starting cash.
- **Hard daily loss cap (G2): -$2,000.** When intraday P&L hits -$2k,
  halt new entries, liquidate all open positions, halt for the day.
- Account safety: bot refuses to start on non-SIM accounts.

### Universe rules
- **US equities only**, NYSE + NASDAQ listed.
- **Margin-eligible.** Excludes leveraged ETFs (TQQQ, SOXL, SQQQ, etc.),
  recent IPOs (must be listed ≥ 1 year), penny stocks (price > $7 lab
  floor, > $5 paper floor).
- The bot reads its universe from the in-house "Research Brain" channel
  which publishes ~150 symbols per day. Filtered down further by per-
  symbol hard filters (price, volume, spread, RelVol).

### Execution
- Brokerage model: TradeStation Margin account.
- Commission: $0 (TradeStation commission-free for stocks since 2019).
- Slippage assumption in backtest: 2.5 bps per fill (Rhett's live-fill
  instinct on liquid names).
- All exits via marketable-limit orders (not raw market orders, not
  passive limits) — accepted by TS after 4:00 PM, slippage-capped.

### Backtest environment
- QuantConnect cloud, LEAN engine v2.5.x.
- Train window: 2016-01-01 to 2021-12-31 (6 years).
- Holdout window: 2022-01-01 to present (run ONCE after train passes).
- Minute-resolution data on the active universe.

### What "works" means — the gate
A strategy enters live SIM deployment only if it clears ALL of:
- Positive net P&L on the train window
- Profit factor ≥ 1.2
- Sharpe ratio ≥ 1.0
- ≥ 10% annual net return
- Survives the G2 daily-loss cap

---

## WHAT WE'VE TRIED — Stage 5 results

### H0 — Buy-and-hold SPY framework sanity check
- **Status: PASSED 2026-05-24.** +160.97% return, CAGR 17.319%,
  Beta 0.985, Alpha 0.002, Fees $0.
- Purpose: validate the QC framework (TradeStation brokerage + slippage
  + sizing math). Confirmed our framework is wired correctly.

### H1 — Internal-bar Opening Range Breakout
- **Status: FAILED catastrophically.** Claude Code's first attempt at
  ORB. Multiple specification errors (1.0× ATR stops, wrong universe,
  no day-trading guards).
- Lesson: spec discipline.

### H2 — VWAP mean reversion (early prototype)
- **Status: FAILED.** Not faithfully specified; aborted early.

### H3 — "Zarattini Stocks-in-Play" (Claude Code's drift version)
- **Status: FAILED -99.97%.** Catastrophic. Caused by Claude Code
  silently drifting from the paper spec — 1.0× ATR stops instead of
  paper's 0.10×; top 1000 universe instead of paper's ~7000;
  bi-directional breakouts instead of gap-direction filter.
- Lesson that drove this project's discipline overhaul: **Claude Code
  has a documented failure mode of "translating faithfully" while
  silently drifting from spec.** Multi-AI cross-checking now mandatory.

### H4 — Faithful Zarattini ORB on Stocks in Play (THIS IS THE FRESH RESULT)
- **Spec source:** Zarattini, Carlo & Aziz, Andrew (2024).
  "A Profitable Day Trading Strategy For The U.S. Equity Market."
  SSRN 4729284. Paper claims Sharpe 2.81 over 2016-2023.
- **Three independent spec audits passed** (ChatGPT GPT-5.5, Base44,
  Claude Opus 4.7 with direct paper PDF citations).
- **Smoke test PASSED clean** (Jan-Feb 2016, +6.08%, $0 fees, PSR 85.8%,
  287s runtime).
- **Full backtest result (frozen at 80%, 2016-01 to 2020-12):**
  - Strategy total return: **-17.65%** ($100k → $82,353)
  - CAGR: **-3.83%** over 4.97 years
  - **SPY same period: +100.08% / CAGR +14.98%**
  - Max drawdown: **-29.28%** (Feb 2018 trough)
  - PSR: **0.095%** (statistically zero edge)
  - Total trade events: **9,146** across 195 unique symbols
  - Year-by-year: 2016 -6.6%, 2017 -15.1%, 2018 +27.8%, 2019 +2.7%,
    2020 -21.0%
- **Verdict: FAILED. 0 of 5 works-bar criteria met.**

### Candidate menu queued (NOT yet tested)
- **C2** — Zarattini TQQQ leveraged-ETF ORB (excluded; we don't trade
  leveraged ETFs per our universe rule).
- **C3** — Crabel NR7 / inside-bar ORB. Pattern-based universe.
- **C4** — Connors short-term mean reversion (RSI2 / 2-day RSI).
- **C5** — First-half-hour momentum follow-through.
- **C6** — Post-earnings-announcement drift intraday.

---

## THE BOT'S CURRENT LIVE STRATEGY (separate from the lab candidates)

The bot has been running its OWN composite-score momentum scanner the
entire time, independent of the lab strategy work. The May 13-22 audit
showed it has structurally bad math: 57.8% win rate but profit factor
0.85 (losing). We've added extensive safety + AI guidance overlay but
haven't fundamentally changed its core entry logic.

**Critique this if you have specific ideas to fix it.**

### Universe (live)
- 150 symbols/day from "Research Brain" channel
  (`outputs/advisor_guidance/advisor_universe_latest.json`)
- Leveraged ETF blocklist applied at universe-read time (fix shipped
  2026-05-27 — was missing before; TQQQ traded 6× yesterday before the fix)
- Falls back to hardcoded CORE_UNIVERSE (~50 large caps) if channel
  invalid/stale

### Per-symbol hard filters
- Price ≥ $20
- 14d avg volume ≥ 500k shares
- Spread ≤ $0.10 (HARD veto — was missing, recently shipped)
- RelVol ≥ 1.5× (today_cumulative / 20d_avg with intraday U-curve
  normalization — shipped 2026-05-26)
- Net change today ≥ +0.25% (longs) / ≤ -0.60% (shorts)
- Listed ≥ 1 year, NYSE/NASDAQ only

### Entry signal (composite 0.0–1.0)
- Momentum 35% (today's net_change_pct, mapped 0-2.5% → 0-1)
- Volume 25% (today_volume vs 500k floor, mapped 1×-3× → 0-1)
- Spread quality 20% (1 - spread/$0.25)
- Price action 20% (above-open bonus)
- **Floor:** composite ≥ 0.40 to be considered
- **Adjustments applied:** ×(1 + promote_bonus + watchlist_bonus +
  time_of_day_bonus). Time-of-day: +0.10 at 12:00-12:59, +0.15 at
  14:30-15:29.

### Position sizing
- 25% of capped $100k equity × conviction multiplier (0.5×-1.25× based
  on composite — higher conviction = bigger position).
- Max 4 open positions, max 2 per GICS sector, $100k total exposure cap.

### Exit logic (BASELINE profile, advisor can swap to TREND_AGGRESSIVE
or CHOP_TIGHT)
- Hard stop: **-0.50%** from average entry price (HARD, cannot widen)
- Tier 1 trail: activates at +0.20% gain, 0.08% trailback
- Tier 2 trail: activates at +0.75% gain, 0.05% trailback
- Tier 3 trail: activates at +1.50% gain, 0.03% trailback
- Breakeven lock: +0.40% triggers stop at entry + 0.05%
- EOD flatten: 3:50 PM ET (via `before_market_close(spy, 10)`),
  marketable-limit orders, GCP duration after 3:58 PM

### Risk gates (live)
- Daily loss cap: $10,000 (project target is $2,000 G2 — bot still
  uses $10k, tightening pending)
- Per-symbol stop circuit breaker: 2 hard-stops on a symbol → block
  rest of day
- 15-min cooldown after exit on same symbol (local `recent_exits.json`
  truth source — bug fix shipped 2026-05-26)
- No entries 9:30-9:59 (10am gate)
- No entries after 3:30 PM
- Open-orders fetch fail-safe: if broker `/orders` fetch fails, halt
  entries for the cycle
- Scan-error circuit breaker: if >50% of universe scan errors per cycle,
  halt cycle
- Advisor halt: honors `BLOCK_ALL_NEW_ENTRIES` from the advisor (fix
  shipped 2026-05-26 — was previously logged-but-ignored)

### AI-driven advisor overlay
The advisor (Claude API call 3×/day) emits typed controls the bot honors:
- `BLOCK_SYMBOL`, `BLOCK_SYMBOL_DUE_TO_NEWS`, `ALLOW_SYMBOLS_ONLY`
- `BLOCK_ENTRIES_AFTER_TIME`, `REDUCE_MAX_POSITIONS`, `SET_MAX_POSITION_PCT`
- `REQUIRE_MIN_NET_CHANGE_PCT`, `REQUIRE_MIN_NEG_CHANGE_PCT`
- `PROMOTE_SYMBOL` (conviction-weighted scoring nudge)
- `WATCHLIST_TODAY` (scoring nudge for advisor's preferred names)
- `EXIT_PROFILE` (BASELINE / TREND_AGGRESSIVE / CHOP_TIGHT — hard stop
  can only TIGHTEN)
- `VETO_CANDIDATE` (time-bounded block on specific symbol+side)

The advisor reads market data + sector ETFs + news + earnings + journal +
prior insights, then emits the typed controls. **Free-text instructions
are silently ignored** (architectural rule: bot only obeys typed
schema).

### Live bot recent performance (audit data)
- May 13-22, 2026 (8 trading days, 161 round trips):
  - **57.8% win rate but profit factor 0.85** = structurally losing math
  - Avg winner $44, avg loser $86 (losers ~2× larger)
  - Shorts produced 100% of realized loss (-$922 across 20 short trades)
  - Longs essentially flat (+$0.89 across 146 long trades)
- May 26, 2026 (yesterday, 51 round trips):
  - 45.1% win rate, profit factor 0.57, net -$787.67
  - TQQQ traded 6× before the leveraged-ETF fix shipped at 9:18 AM
  - Most losses came from WULF/RDW churn (the cooldown bug fixed
    same day)

---

## WHAT WE NEED FROM YOU

We're at a decision point. Pick ONE of these three lanes and respond
with a structured proposal:

### Lane A — H4 sizing-interpretation retest
H4 was run with **$5k slice / $50 risk per trade** (QC-recreation
reading of the paper). Claude Opus's audit argued for **$20k slice /
$200 risk per trade** (paper said "1% of capital allocated to that
position" — open interpretation).

**Question:** is the H4 verdict definitive at PSR 0.095% even with the
sizing factor of 4×, or could the correct sizing flip the result?

If you believe Lane A is the right next step, justify with:
- Why the sizing interpretation matters mathematically (does it amplify
  the loss or could it reverse it?)
- What additional friction (or relief) the larger position size brings
- Whether the paper's text is unambiguous on this point

### Lane B — Next strategy candidate
If H4 is genuinely no-edge regardless of sizing, recommend the next
strategy to test. From C2-C6 menu OR a fresh proposal.

**Constraints:**
- MUST be day-trading-only with EOD flatten by 3:50 PM ET
- MUST work on margin-eligible US equities (NYSE/NASDAQ, > $7 price,
  no leveraged ETFs)
- MUST be QuantConnect-backtestable
- MUST have published evidence of edge (paper, book, replicated study)
  — not theory-craft from training data alone
- MUST be reasonably different from H4 (don't recommend
  "H4 but with X tweak")

### Lane C — Critique the live bot's current strategy
The bot's CURRENT live strategy (described in detail above) has
documented structural issues: 57.8% win rate but profit factor 0.85,
shorts producing 100% of realized loss, the composite scoring averaging
out spread quality (a key execution-risk signal) into noise.

If you believe Lane C is the right move, propose 2-3 specific surgical
fixes (not a rewrite). Each fix should have:
- The current behavior
- The proposed change
- Expected impact (with mechanism)
- Reversibility plan if it underperforms

---

## REQUIRED FORMAT FOR YOUR RESPONSE

End your response with a clearly-marked paste-ready block:

-------- BEGIN PASTE-READY BLOCK --------

## [YOUR AI NAME] — Stage 6 review post-H4 failure [YYYY-MM-DD]

**Lane chosen:** A / B / C

**Recommendation (one sentence):**
[...]

**Why this is the right move (3-5 sentences):**
[...]

**What you're confident in vs guessing:**
[...]

**Top adversarial critique of your own recommendation:**
[i.e. "the strongest argument against my proposal is..."]

**If Lane B (next strategy): full spec proposed:**
- Source citation with verbatim quote
- Universe filter
- Entry rule
- Exit rule
- Sizing
- All other parameters

**If Lane A (H4 retest): specific config changes:**
[...]

**If Lane C (fix live bot): 2-3 surgical changes:**
[...]

**Signed:** [AI name + model], [date]

-------- END PASTE-READY BLOCK --------

---

## REFERENCE DOCS YOU MAY REQUEST

If you need more context to give a confident answer, ask Rhett for:
- `strategy-research/STRATEGY_LAB.md` — full multi-AI project log
- `strategy-research/h4_zarattini_orb.py` — H4 v4.2 code (the version
  that ran the failed backtest)
- `strategy-research/H4_spec_for_audit.md` — the locked H4 spec
- `tradestation-bot/entry_signals.py` + `exit_bot_v2.py` — the live
  bot's actual entry/exit code
- The full backtest results JSON from QuantConnect

---

## DON'T

- Don't paraphrase papers from memory. Quote with citations.
- Don't propose strategies you can't cite a source for.
- Don't ignore the day-trading-only constraint.
- Don't propose adding ML/neural-net layers as the next step. We
  haven't proven a simple rules-based edge yet; complexity without edge
  is overfitting.
- Don't recommend retrying H4 with a tweak smaller than the
  $5k-vs-$20k sizing question. Polishing a no-edge strategy is a
  time sink.

---

## When you understand

Acknowledge you've read this, then deliver your structured response.

— Claude Code, 2026-05-27
