# HANDOFF — Strategy-research session, 2026-05-28

**Purpose:** Bring a fresh strategy-research session up to date on everything
that happened in the parent session AFTER the H4 80% backtest result was
pasted on 2026-05-27. Includes Stage 6 status, live trading observations
from 5/27, and new backlog items that may inform the next strategy.

**Required reading first** (in order):
1. `C:\repos\alpha-quant-coordination\strategy-research\STRATEGY_LAB.md`
2. `C:\repos\alpha-quant-coordination\strategy-research\HANDOFF_2026-05-27_post_H4_failure.md`
3. This file.

---

## 1. State of the Stage 6 review (post-H4 failure)

H4 v4.2 (Faithful Zarattini ORB) backtested through ~80% of the 6-year
sample before the consolidator lifecycle hung at Dec 2020. Result was
definitive enough to reject:
- -17.65% return
- PSR 0.095% (vs 50% bar)
- 9,146 trades
- 0 of 5 "works bar" criteria met

Three lanes were posed for external AI review (full content in
`HANDOFF_2026-05-27_post_H4_failure.md`):
- **Lane A:** retest H4 with smaller size / different signal weighting
- **Lane B:** propose a new candidate strategy
- **Lane C:** critique the LIVE BOT current strategy (composite scoring)

**Status of the three reviewers:**

| Reviewer | Status | Notes |
|---|---|---|
| GPT-5.5 (ChatGPT) | ✅ DONE | Returned Lane B / C7 — a momentum-rotation strategy. **C7 spec was TRUNCATED mid-signal-construction in the paste.** Full retrieval needed before audit. |
| Base44 | ⏳ PENDING | Waiting for Rhett to paste response |
| Claude desktop | ⏳ PENDING | Waiting for Rhett to paste response |

**Final-auditor protocol (per memory `project_strategy_research_audit_protocol`):**
Claude Code is the final auditor. Once Base44 + Claude desktop respond,
Claude Code synthesizes all three reviews + recommends the next H5
candidate. Until then, no new H5 work proceeds.

---

## 2. Live trading observations — 2026-05-27 (this matters for strategy)

The bot ran all day 5/27 with the full performance-enhancement stack live
(EXIT_PROFILE tiers, conviction sizing, RelVol filter, time-of-day bonus,
per-symbol circuit breaker, etc.). I monitored every event. Patterns worth
feeding into the strategy decision:

### 2a. End-of-monitor running P&L: ~+$1,081 green

Hour-by-hour:
- 10:00–11:00: -$425 (long-side hostile, 5 hard-stops in 6 minutes)
- 11:00–12:00: +$1,140 (winners exploded; RDW +$657 TIER3, LUNR(#2) +$540 TIER3)
- 12:00–1:00: +$760 (IREN re-entries chained; PL re-entries chained)
- 1:00–2:00: -$73 (NKE/PL stopped, RDW continued winning)
- 2:00–3:30: ~+$680 (RDW kept winning, INTU/FUTU added; **METU leveraged ETF bypass lost $242**)

### 2b. The day's headline pattern: same-day re-entries win

After a stop-out, the bot's signal often re-qualifies the same symbol
~5-15 minutes later. The 2-stops-per-day circuit breaker (Task #25,
confirmed firing today as Task #68) caps the damage at exactly 2 attempts.
Results today:

| Symbol | Attempts | Wins | Stops | Day net | Pattern |
|---|---|---|---|---|---|
| RDW | 9 | 7 | 2 | **+$1,264** | Workhorse — kept winning until 2nd stop locked it out at 3:15pm |
| IREN | 6 | 4 | 2 | **+$542** | Same — locked out at 1:10pm after 2nd stop |
| LUNR | 3 | 1 | 2 | -$28 (≈flat) | Locked out at 11:01am |
| HIMS | 2 | 0 | 2 | -$345 | Locked out at 10:46am, 100+ subsequent attempts all blocked |
| PL | 5 | 3 | 2 | +$25 | Locked out at 1:40pm |
| NKE | 4 | 3 | 1 | -$14 | Still tradeable |
| BA | 2 | 1 | 1 | -$138 | |
| FUTU | 3 | 2 | 1 | -$37 (running) | |
| ZS, STM, FRO, VGT (shorts) | 4 | 4 | 0 | +$450 | **Shorts 100% today** |
| RGTI | 2 | 1 | 1 | -$140 | First as long (lost), second as short (won) |
| IWM, RSP, SMCI, AFRM, UBER, TSM, INTU | 1-2 each | mixed | mixed | small | |

**KEY OBSERVATION:** Same-day re-entry attempt #2 was 4-for-5 profitable
(LUNR +$540, IREN +$245, RDW +$657, PL +$62, HIMS −$166). Suggests the
bot's signal has predictive value on the rebound after a fast pullback,
and the circuit-breaker cap at 2 stops is well-calibrated. Tightening to
"1 stop = locked out" would have cost ~$1,300 today.

### 2c. Asymmetry: shorts won 100%, longs ~50%

Shorts today: 4-for-4 trailing-stop winners (ZS +$124, STM +$238, FRO +$48,
VGT +$40) plus RGTI short-after-long-failure +$51. **5-for-5 shorts.**
Longs were ~50/50, with the wins clustered in the chase-rebuy pattern.

If this pattern holds across more days, it argues for:
- Increase short allocation
- Or: ALL trades should be momentum-pullback continuation rather than
  initial breakouts (the way 2nd attempts profitably exploited the dip)

### 2d. RDW is the most productive single symbol today

+$1,264 across 9 trades. Composite stays at 0.892 every cycle (steady),
relvol ranges 3.3–6.8. It's a small-cap space stock (Redwire Corp).
**Strategy implication:** the current scoring loves it. The exits work
because trailing tiers fire ~0.4–2.3% above entry repeatedly.

---

## 3. New live-bot bugs discovered today (relevant to strategy decision)

These got logged as backlog tasks during monitoring. Some are
strategy-relevant because they affect whether observed performance is
trustworthy:

| ID | Item | Strategy impact |
|---|---|---|
| #65 | Conviction sizing × 4 positions blows MAX_TOTAL_EXPOSURE=$100k cap (today's HIMS position was ~$30.4k due to conviction 1.22 × base; 4 of those = $122k > $100k) | Backtest must assume real exposure cap, not theoretical |
| #66 | short_bot.py missing trade attribution string (no conviction_mult/tod_bonus/relvol/spread logged) | Short-side attribution analysis impossible until fixed |
| #67 | Scan failure rate stuck at ~62% across the entire day; SHORT_ENTRY_BLOCKED safety_halt fired 60+ times. Either TS API quote endpoint degraded or universe (~150 symbols) hitting per-cycle rate cap. | **Today's short-side performance is from a tiny fraction of cycles — extrapolating to "shorts work 100%" is fragile** |
| #68 | ✅ VERIFIED: Per-symbol loss circuit breaker fires at 2 stop-outs/day, applies to BOTH longs and shorts on that symbol | Confirms current design intent; tighten only with care |
| #69 | **URGENT:** METU (Direxion Daily META Bull 2X Shares = 2X leveraged ETF) entered live at 3:10pm, hard-stopped at -0.75% = -$242. Today's shipped `leveraged_etf_blocklist.py` has gap coverage — Direxion 2X/3X single-name ETFs (METU, FNGU, FNGD, NVDU, NVDS, etc.) missing. | Confirms the rule "no leveraged ETFs" is still violatable; backtest of any future strategy must assume same rule and exclude these names |

---

## 4. Pattern observations to consider for next strategy (H5)

These are NOT recommendations — they're observations that should inform
the Stage 6 synthesis once Base44 + Claude desktop are in:

1. **Trailing stops materially outperform hard stops on average.** Today's
   trailing-tier exits (T1/T2/T3) won most trades; hard stops took losses.
   The EXIT_PROFILE typed control is doing real work. Any H5 candidate
   should keep the multi-tier trailing logic.

2. **Same-day re-entry is a feature, not a bug.** Either:
   (a) the signal is sticky on names that pulled back, or
   (b) the price reversal IS the edge (mean-reversion in the morning).
   GPT-5.5's C7 was momentum-rotation — if Base44/Claude-desktop both
   propose mean-reversion variants, the live data already weakly supports
   that direction.

3. **Hard stops cluster in the first 6 minutes of position life.**
   HIMS#1 = 2m20s; IREN#1 = 1m5s; LUNR#1 = 2m1s; SMCI = 6m24s; AFRM = 4m51s.
   This argues either:
   (a) widen initial stops to give first 5 min more room, OR
   (b) tighten entries (require a more confirmed bar before entering).

4. **The composite scoring (momentum + volume + spread + price-action)
   correlates with winners.** Composite 0.95+ entries did well; composite
   0.55–0.70 entries (RSP 0.67, PL 0.57, IWM 0.65) all stopped out.
   Argues for raising minimum-composite threshold from current ~0.50 to
   something like 0.80.

5. **Conviction sizing × position cap is broken.** When all 4 positions
   are conviction-1.22 longs, total exposure hits ~$122k vs $100k cap.
   The cap is regularly violated. For any backtest of a new strategy,
   model the REAL exposure or tighten the conviction cap.

---

## 5. Pending work the new session inherits

In priority order:

1. **Wait for Base44 + Claude desktop responses.** Do NOT prematurely
   synthesize Stage 6 with only GPT-5.5 + this session's observations.
   When both arrive, do the 3-way synthesis + final-auditor recommendation.

2. **Retrieve full C7 spec from GPT-5.5.** Paste was truncated mid
   signal-construction formula. Re-prompt GPT-5.5 for the complete spec
   before auditing.

3. **Ship the METU fix (Task #69)** — high priority. Symbols to add to
   `tradestation-bot/leveraged_etf_blocklist.py`:
   - METU (Direxion Daily META Bull 2X)
   - METD (Direxion Daily META Bear 2X)
   - NVDU (Direxion Daily NVDA Bull 2X), NVDS (Bear 2X)
   - NVDL (GraniteShares 2X Long NVDA), NVD (Bear 2X)
   - TSLL (Direxion Daily TSLA Bull 2X), TSLS (Bear 2X)
   - FNGU (MicroSectors FANG+ 3X), FNGD (Bear 3X)
   - AMZU, AMZD, MSFU, MSFD, GGLL, GOOGL leveraged variants
   Full Direxion + MicroSectors + GraniteShares single-name 2X/3X list
   should be added. Hot-reload after.

4. **Tasks #65 (conviction exposure cap) and #66 (short_bot attribution)**
   are pre-existing items from earlier in the parent session, still pending.

5. **Task #67 (scan failure rate ~62%)** — should be diagnosed because
   if persistent, the "shorts 100% today" observation is from a small
   sample size and isn't trustworthy.

---

## 6. Files modified this session — none

I monitored events all day but did NOT push code or doc changes during
the session (this handoff file is the only new artifact). The advisor /
bot ran with the codebase as-shipped on 5/27 morning.

---

## 7. What I owe Rhett going into the next session

Honest acknowledgment: I should have been incrementally appending these
observations to STRATEGY_LAB.md throughout the day instead of leaving
them in chat. This file remedies that. Apologies for the rework.

**Per memory `feedback_copiable_handoffs`:** the full text of this
handoff is reproduced in chat alongside this file write, so Rhett can
copy-paste directly into the new session without opening a file.
