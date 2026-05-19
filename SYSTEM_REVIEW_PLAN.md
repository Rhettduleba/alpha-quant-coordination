# Alpha Quant — System Review Plan

**Version:** 1.1
**Date:** May 19, 2026
**Author:** Claude Code (Opus 4.7), running on the VPS
**For review by:** Browser Claude (planning chat)
**Trigger:** Rhett's observation that the bot should not be operating outside trading hours, his correct intuition that something structural is broken, and his request to fix the system before resuming performance work.
**Changes from v1.0:** see §11 changelog at end.

---

## §1 Why this plan exists

On May 19, 2026, today's 8:04 AM advisor run emitted `BLOCK_ALL_NEW_ENTRIES` with reason text "Market is closed — all 3,368 entry attempts were blocked with 'Market closed' reason and zero trades executed today." Rhett pushed back: the bot is supposed to be pure execution, only active during normal market sessions. If pre-market "Market closed" rejections happened every day, the advisor would block every day — yet it doesn't, so something is different about today. He also questioned why we're spending all our time fixing the system instead of evaluating bot and advisor performance.

He's right on both counts.

---

## §2 What the data actually shows

### 2.1 The bot runs 24/7 and logs tens of thousands of "blocked" attempts daily, including weekends

Journal entry counts for the last 8 days (`trade_journal.csv`):

| Date | Day | Total rows | Blocked | Submitted |
|---|---|---:|---:|---:|
| May 11 | Mon | 40,854 | 16,376 | 76 |
| May 12 | Tue | 26,280 | 16,969 | 18 |
| May 13 | Wed | 33,675 | 21,442 | 19 |
| May 14 | Thu | 31,466 | 19,480 | 13 |
| May 15 | Fri | 34,262 | 21,688 | **0** |
| May 16 | **Sat** | 20,548 | 15,411 | 0 |
| May 17 | **Sun** | 20,552 | 15,414 | 0 |
| May 18 | Mon | 33,404 | 21,168 | 34 |

20,000+ rejected entries on Saturday and Sunday confirms: the bot scans continuously regardless of market hours. The blocked attempts come from `bot_loop.py:225-231` which logs `ENTRY_BLOCKED` with note "Market closed" when `is_market_open()` returns False.

### 2.2 `BLOCK_ALL_NEW_ENTRIES` has been emitted multiple times — and the pattern is INCONSISTENT

From `advisor_run_log.jsonl`:

| Date | Day | Action | Effect |
|---|---|---|---|
| May 15 | Fri | `BLOCK_ALL_NEW_ENTRIES` 8:03 AM, kept all day | **0 fills on a real trading day** |
| May 17 | Sun | `BLOCK_ALL_NEW_ENTRIES` 8:03 AM | no impact (weekend) |
| May 19 | Tue (today) | `BLOCK_ALL_NEW_ENTRIES` 8:04 AM | bot blocked from market open until manual unblock at 11:18 AM ET |

But it did NOT fire on May 11, 12, 13, 14, 18 — days with the same large-volume noisy journal preceding them. May 18 in particular had a weekend (May 16-17) inside its 5-day journal lookback window and did NOT emit BLOCK_ALL. May 19 had the same weekend in its window and DID emit BLOCK_ALL.

**Same input → opposite outcome.** Whatever causes BLOCK_ALL emission is not noise-volume alone. See §3.

### 2.3 Verified advisor-run cadence — NOT 12:30 PM as stated in run_advisor.py docstring

The `run_advisor.py:22-25` docstring says the midday slot is 12:30 PM ET. The empirical reality from 8 days of `advisor_run_log.jsonl`:

| Date | Midday run timestamp |
|---|---|
| May 13 | 12:02 PM ET |
| May 14 | 12:01 PM ET |
| May 15 | 12:01 PM ET |
| May 16 | 12:05 PM ET |
| May 17 | 12:02 PM ET |
| May 18 | 12:02 PM ET |

**Actual midday slot: ~12:00–12:05 PM ET.** The docstring is stale. Verified schedule:
- Pre-market: ~8:00 AM ET (range 8:01–8:07)
- Mid-day: ~12:00 PM ET (range 12:01–12:05)
- After close: ~4:30 PM ET (range 4:31–4:33)

### 2.4 The performance baseline cited in prior State of Record was materially wrong

V4 verification (`get_pnl_for_date` over 22 trading days, broker-truth) for the verifiable window only:

| Source | Closed pairs | Net P/L | Avg per pair |
|---|---:|---:|---:|
| Prior SOR baseline (journal-derived) | 540 | $-37,614 | $-69.66 |
| Broker truth (11 verifiable days) | 297 | $-2,846 | $-9.58 |

Cited as broker-truth for those 11 days only; do NOT treat as authoritative replacement until V5 resolves the missing-10-days question.

### 2.5 Recent days the bot didn't trade at all on intended trading days

From V4 + advisor_run_log:

- May 15 (Fri): 0 fills. Advisor emitted `BLOCK_ALL_NEW_ENTRIES`.
- May 19 (Tue, today): 0 fills morning. Advisor emitted `BLOCK_ALL_NEW_ENTRIES` at 8:04 AM. Manually unblocked at 11:18 AM ET; trading active for remainder of day.

---

## §3 Why this matters — leading HYPOTHESIS, not confirmed root cause

The bot was designed as a narrow, deterministic executor with hard criteria. The advisor was designed as a smart, learning layer that could add constraints in the right conditions. The blueprint works as long as the advisor reasons from clean data.

**Leading hypothesis (not yet proven):**

1. Bot runs 24/7 → logs ~20k "Market closed" rejections per day.
2. Advisor's prompt feeds it the journal, including this noise.
3. Advisor reads the noise and reasons defensively.
4. Advisor emits `BLOCK_ALL_NEW_ENTRIES` when something tips its judgment.
5. Bot honors it; zero trading that day.
6. Tomorrow's journal carries forward.

**Why this hypothesis is INCOMPLETE.** The §2.1 data shows comparable noise every day — but BLOCK_ALL only fired on May 15, 17 (no impact, weekend), and 19. May 18 had the same weekend noise (May 16-17) in its 5-day journal window AND DID NOT EMIT BLOCK_ALL. May 19 had the same weekend in its window AND DID EMIT BLOCK_ALL. Same input, opposite outcome.

The contamination theory predicts blocking every day. It doesn't. So contamination cannot be the sole cause. Other plausible factors:

- **(a) LLM judgment variance** — Claude Sonnet has inherent variance; the same prompt can produce different controls.
- **(b) `advisor_memory.json` state** — the advisor's accumulated memory may bias certain runs toward over-blocking.
- **(c) Real data-feed differences** — the gap data was "−100%" on May 19 (data quality issue per the regime_assessment); maybe a similar real anomaly fired May 15.

R3 and R4 below must produce an explicit answer to: **why did BLOCK_ALL fire on May 15 and 19 but not May 11–14 and 18?** Until that's answered, "noise contamination" is one factor at most, not THE cause. The P0 (kill the off-hours noise) stands regardless because the noise is independently bad — but the causal claim is unproven.

---

## §4 Proposed review scope

| # | Area | What we look for |
|---|---|---|
| R1 | **Operating-hours architecture** | How `is_market_open()` is used. The Q1 decision (§8) is bot stays running 24/7 but goes SILENT outside RTH — no scanning, no journal writes when market closed. Verify what changes need to happen in `bot_loop.py` + `short_bot.py` to enforce that, and what current journal writes need suppressing. |
| R2 | **Journal data quality** | What is the actual signal-to-noise ratio in `trade_journal.csv`? Reasons-for-blocking breakdown by event_type and note. Identify which event categories are pure noise vs. which carry real signal. |
| R3 | **Advisor control vocabulary — all 9 control types** | Emission history of EACH control type from `advisor_run_log.jsonl` and the recent control files. Which were emitted, when, for what reason. Identify which are useful vs. which are dangerous when autonomously fired. Includes the open question: why did `BLOCK_ALL_NEW_ENTRIES` fire on May 15 + 19 but not other days? Also covers the currently-active `BLOCK_SYMBOL` × 3 and the position-size overrides — they came from the same advisor judgment now under question. |
| R4 | **Advisor prompt design + memory state** | What does the advisor's prompt actually contain (`ai-trading-strategy-agent/src/advisor/prompt_builder.py`)? Is the journal feed filtered to RTH or raw? **R4b — inspect `advisor_memory.json` directly.** What concrete claims are in it? Are any traceable to the wrong (journal-derived, inflated-loss) baseline? Decide wipe-vs-keep from what's actually in the file. |
| R5 | **Watchdog scheduling** | Per the Q1 decision, the watchdog continues running 24/7 since the bot stays alive. Verify watchdog needs no changes. One Task Scheduler entry at VPS boot (replacing the broken .lnk launchers which are already archived). |
| R6 | **Performance baseline integrity** | The 540 / $-37,614 baseline was journal-derived and wrong. V5 work: implement pagination on `/historicalorders?since=` to pull the missing 10 days of April history. Then publish an authoritative broker-truth baseline. |
| R7 | **Reconciliation reliability** | Already fixed 3 bugs in `daily_reconciliation.py`. Other reporting tools (`performance_summary.py`, `journal_analyzer.py`, etc.) may have similar bugs that mis-state results. Inventory them. |
| R8 | **Cross-checks / sanity monitoring** | Build the RECOMMEND_HALT mechanism (see §8 Q2 reframe): when the advisor wants to halt all trading, it emits a recommendation that surfaces for human confirmation rather than a control the bot silently honors. Implements both the sanity check AND the BLOCK_ALL_NEW_ENTRIES replacement in one mechanism. |

---

## §5 Investigation methodology

For each Rn item, one investigation pass:

1. **Read the canonical file(s)** for that area.
2. **Query supporting data** — journal CSV, log files, control history, broker API.
3. **Identify the actual current behavior** — not the documented or assumed behavior.
4. **Identify the gap** between current behavior and what makes sense.
5. **Propose fix** with effort estimate (small / medium / large) and risk level (safe / behavior-changing / risky).

All findings go into a single `SYSTEM_REVIEW_FINDINGS.md` document in this coordination repo. Browser Claude reviews; Rhett arbitrates; then we sequence fixes.

---

## §6 Fix prioritization framework

| Priority | Criterion |
|---|---|
| **P0** | Stops the bot from operating wrong right now, or removes the contamination loop. Fix before any other change. |
| **P1** | Data integrity — anything that makes downstream analytics or advisor reasoning wrong. |
| **P2** | Removes dangerous autonomous behaviors (the BLOCK_ALL_NEW_ENTRIES class of issue, downgraded to RECOMMEND_HALT). |
| **P3** | Adds sanity checks or cross-validation that catches future regressions. |
| **P4** | Reporting / baseline / cleanup work that doesn't change bot behavior. |

**Likely P0 candidates given the Q1 decision:**
- Gate the `bot_loop.py` and `short_bot.py` cycles on `is_market_open()` — skip all journal writes, all API fetches, all scanning when market is closed. Sleep until next loop iteration.

---

## §7 Deliverable

A `SYSTEM_REVIEW_FINDINGS.md` document with:

- Per-Rn finding: current behavior, gap, root cause (if proven; hypothesis if not), proposed fix, severity (P0–P4), risk (safe/behavior/risky), effort (S/M/L).
- A prioritized execution plan: which fix lands first, what changes for the bot, what the success measurement is.
- Open questions explicitly flagged for Rhett's decision.

Once written, Rhett approves the execution order. Fixes land one at a time, each verified before the next.

**Hard rule for this initiative:** no new features, no performance experiments, no advisor changes beyond what the review surfaces. Plumbing first.

---

## §8 Decisions recorded + remaining open questions

### Q1 (DECIDED by Rhett May 19, 2026): Bot stays 24/7 but goes SILENT outside RTH

Bot keeps running under the watchdog, but `bot_loop.py` short-circuits at the `is_market_open()` check — no scanning, no journal writes, no API fetches outside RTH. Smaller change than process-lifecycle machinery (an if-statement vs. start/stop scheduling), no new failure mode (an RTH-only bot that crashes mid-session has no self-recovery), and the watchdog already keeps the process warm. Matches the project's "narrow, minimal change" philosophy.

This is the implementation mechanism for roadmap item #8 (smart sleep schedule).

### Q2 (REFRAMED by browser Claude + Rhett May 19, 2026): Don't delete BLOCK_ALL_NEW_ENTRIES — downgrade to RECOMMEND_HALT

Original v1.0 plan asked whether to remove `BLOCK_ALL_NEW_ENTRIES` entirely. Browser Claude proposed and Rhett agreed: **downgrade** to a `RECOMMEND_HALT` semantic that surfaces for human confirmation rather than a control the bot silently honors. Preserves the advisor's ability to raise a real alarm (which is what BLOCK_ALL was supposed to be) without giving it unilateral total-halt power. Hard risk floors (`risk_config.py` `DAILY_MAX_LOSS`) and the human `daily_shutdown.json` switch remain — bot is not left exposed.

Implementation merges with R8.

### Q3 (browser Claude lean — confirm during R4): Filter pre-market noise from the advisor's prompt

Defense-in-depth on top of the Q1 P0 (which removes most off-hours journal writes at source). Someone must define what pre-market context is actually useful (gap data: yes; "Market closed" rows: no).

### Q4 (browser Claude lean — investigate in R4b first): Wipe `advisor_memory.json`?

Inspect first, decide after. If the memory contains concrete claims traceable to the wrong baseline, archive + restart fresh. If the memory is mostly stylistic / pattern-recognition without specific wrong claims, keep.

### Q5 (browser Claude lean — agree): Don't promote V4 baseline to "authoritative"

The 297 pairs / $-2,846 / 11 days figure is broker-truth FOR THOSE 11 DAYS, labeled partial. Do not cite as the new authoritative baseline replacing 540 / $-37,614. Promote only after V5 pagination work fills in the missing 10 days.

### Q6 (UNRESOLVED — flagged disagreement with browser Claude): Advisor run cadence

Browser Claude said this is "already closed" with a citation to "STATE §6" that does not exist in the current STATE.md v2.4. The cited reference cannot be verified. Per the operating-rules pushback discipline, Claude Code is leaving this as OPEN until a real source is produced. Working assumption: cadence is 3x daily (~8 AM, ~12 PM, ~4:30 PM ET) per the empirical run log. Whether to change cadence is a downstream question, post-plumbing fixes.

### Q7 (matches Q1 knock-on): One Task Scheduler entry at VPS boot

The broken .lnk launchers were already archived earlier May 19. Since Q1 keeps the bot 24/7-with-silence, no start/stop schedule is needed — just one Task Scheduler entry that starts `watchdog_supervisor.py` at VPS boot. Already in place via current setup; verify no action needed during R5.

---

## §9 Sequence

1. Browser Claude reviews this plan v1.1, agrees or proposes further edits. Rhett arbitrates.
2. Claude Code investigates R1–R8 per §5, produces `SYSTEM_REVIEW_FINDINGS.md`.
3. Browser Claude reviews findings. Rhett approves execution order.
4. Claude Code executes fixes one at a time, each verified before the next.
5. After plumbing solid: resume performance work (V5 pagination + V4 completion, advisor tuning, etc.).

No performance experiments until step 5. No exceptions.

---

## §10 What Claude Code commits to during this initiative

- Verify every claim against actual files / data before asserting it (operating rule 1).
- Surface conflicts between sources rather than picking silently (operating rule 2).
- No process actions without Rhett's explicit approval (operating rule 3).
- Push back honestly — including pushing back on browser Claude if I disagree (operating rule 4).
- End every report with "What I did NOT verify" (operating rule 5).
- One question per turn to Rhett (operating rule 6).
- 12-hour times in user-facing text (operating rule 7).
- Never reason from incomplete data — verify load-bearing claims at the source first (new operating rule, May 19).

---

## §11 Changelog

**v1.1 (May 19, 2026):** Folded in browser-Claude review corrections.

- §3 relabeled "data contamination" from CONFIRMED ROOT CAUSE to LEADING HYPOTHESIS. Added explicit treatment of the May 18 vs. May 19 contradiction (same noise input, opposite outcome). R3 + R4 now required to produce a causal explanation.
- §4 R3 widened to inspect ALL nine control types, not just `BLOCK_ALL_NEW_ENTRIES`. Includes the currently-active `BLOCK_SYMBOL` × 3 and position-size overrides.
- §4 R4 added R4b: read `advisor_memory.json` and inspect for concrete wrong-baseline claims before deciding wipe-vs-keep.
- §2.3 added (verified advisor cadence is ~12:00 PM ET midday, NOT 12:30 PM as `run_advisor.py:22-25` docstring claims). Stale docstring noted; will be fixed during R4 work.
- §8 Q1 recorded as DECIDED (bot 24/7-with-silence per Rhett).
- §8 Q2 reframed as DOWNGRADE not DELETE per browser Claude + Rhett.
- §8 Q5 leaning recorded (do not promote V4 baseline to authoritative).
- §8 Q6 marked UNRESOLVED with explicit flag that browser Claude's cited "STATE §6" reference does not exist in actual STATE.md v2.4.
- §8 Q7 confirmed as one Task Scheduler entry at VPS boot.
- §10 added new operating rule 8 (never reason from incomplete data).
- Reference to today's manual unblock of `BLOCK_ALL_NEW_ENTRIES` added in §2.5.

**v1.0 (May 19, 2026):** Initial draft. See git history for full content.
