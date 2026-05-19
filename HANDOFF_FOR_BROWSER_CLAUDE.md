# Handoff for Browser Claude (Planning Chat)

**From:** Rhett (via Claude Code on the VPS)
**Date:** May 19, 2026
**Purpose:** Review the system review plan before execution. Weigh in on open architectural questions. Push back if anything is wrong.

---

## Who you are in this project

You are the **planning chat** in Rhett's Alpha Quant workflow. Your role:

- Strategy, filtering, evaluation standards. The brain.
- Push back honestly on Claude Code's findings if you see flaws.
- Weigh in on design questions where two AI perspectives + Rhett's call is the right process.
- Own the §5–§9 sections of the State of Record (decisions, standards, scope).

**Claude Code** is your counterpart. It runs on the Windows VPS and has direct file/code/process access. It owns §1 (verified facts) and §4 (current state). It's the hands.

**Rhett** owns every decision that changes live behavior. He arbitrates when you and Claude Code disagree.

---

## What to read first (in this order)

All in the `Rhettduleba/alpha-quant-coordination` GitHub repo:

1. **`ALPHA_QUANT_STATE.md`** (~9 KB, v2.4) — the State of Record. Current state, open verifications, recent decisions, today's bot/advisor state.
   - Raw URL: `https://raw.githubusercontent.com/Rhettduleba/alpha-quant-coordination/main/ALPHA_QUANT_STATE.md`

2. **`SYSTEM_REVIEW_PLAN.md`** (~12 KB, v1.0) — **the document Rhett wants you to review.** Written today after he correctly identified a structural problem: the bot runs 24/7 and generates ~20k "Market closed" rejections per day (including weekends), which contaminates the advisor's reasoning and causes recurring `BLOCK_ALL_NEW_ENTRIES` over-blocking.
   - Raw URL: `https://raw.githubusercontent.com/Rhettduleba/alpha-quant-coordination/main/SYSTEM_REVIEW_PLAN.md`

3. **`AQ_EVALUATION_STANDARDS_C1.md`** — evaluation standards (only fetch if a proposed change needs evaluation). Note: §3 is marked NOT FIT FOR USE pending rewrite.
   - Raw URL: `https://raw.githubusercontent.com/Rhettduleba/alpha-quant-coordination/main/AQ_EVALUATION_STANDARDS_C1.md`

4. **`CHANGELOG.md`** — running edit log. Skip unless you want history.

---

## Today's context

**The trigger:** at 8:04 AM ET today (May 19, 2026), the advisor emitted `BLOCK_ALL_NEW_ENTRIES` blocking all bot trades until the next advisor run at 12:30 PM. Rhett pushed back — his bot is supposed to be a deterministic executor with hard criteria (`MIN_PRICE`, `MIN_VOLUME`, etc.); a blanket block overrides all of that.

**What investigation confirmed:**

1. The bot does run 24/7, scanning every ~5 seconds even on weekends. Journal counts: 33-40k entries on weekdays, 20k on Saturdays and Sundays.
2. The bot does nothing useful outside trading hours — verified by reading `bot_loop.py:225-231`. When market is closed it logs ONE `ENTRY_BLOCKED` event with note "Market closed" and moves on. No scanning, no fetching, no monitoring.
3. The advisor reads the journal (including pre-market and weekend noise) and sometimes concludes "the market is closed all day" or "something is wrong with conditions" and emits `BLOCK_ALL_NEW_ENTRIES` defensively.
4. This has happened before, not just today: May 15 (Fri) lost a full trading day; May 17 (Sun) had no impact (weekend); May 19 (today) is losing the morning.
5. V4 baseline re-verification (broker truth vs. journal-derived) showed the historical "540 trades / -$37,614" baseline was overstated — broker truth for 11 verifiable days is 297 pairs / -$2,846 net.

**What the bot actually gives the advisor:** verified from `data_collector.py` — only two things, both files the bot writes: `trade_journal.csv` and `session_reports/*.json`. Everything else (quotes, positions, P&L, news, sector data) comes directly from the TradeStation API. So stopping the bot outside RTH loses nothing the advisor needs.

**What's broken:** the journal is the contamination path. The advisor's `recent_journal_rows` loader includes all events from the last 5 days unfiltered — so pre-market and weekend `ENTRY_BLOCKED` noise flows straight into the advisor's prompt.

---

## What Rhett wants from you

1. **Read `SYSTEM_REVIEW_PLAN.md` (raw URL above) in full.** It's ~12 KB and has nine numbered sections plus an open-questions section (§8).

2. **Push back honestly.** If anything in the plan is wrong, badly scoped, missing a category, or proposes the wrong fix order, say so plainly with the specific reason. Don't fake agreement to look collaborative.

3. **Weigh in on §8 (the seven open questions).** These are decisions where Rhett wants two AI perspectives before deciding. The questions cover:
   - 24/7 bot vs. RTH-only bot
   - Whether `BLOCK_ALL_NEW_ENTRIES` should exist as an autonomous control at all
   - Whether to filter pre-market journal data from the advisor's prompt
   - Whether to wipe `advisor_memory.json` and rebuild from broker truth
   - Whether to cite the V4 broker-truth baseline (297 pairs / -$2,846 / 11 days) as authoritative replacement for the wrong 540 / -$37,614
   - Right cadence for advisor runs (currently 3x daily)
   - Bot launcher mechanism (icons vs. Task Scheduler)

4. **If you propose changes:** restate the plan section, give your alternative, give your reason. Rhett will arbitrate.

5. **If you agree:** say so and signal "ready to execute" — Claude Code will then start the R1–R8 investigation per §5 of the plan.

---

## Operating rules for both of us (already in STATE.md §1)

1. **Verify before asserting.** No system-state claim without reading the file. If unread, label it "unverified."
2. **Surface conflicts, don't silently resolve them.** When two sources disagree, flag to Rhett — don't pick.
3. **No process actions without approval.** Restart bot, kill PID, deploy code, edit risk config → propose first, act after.
4. **Push back honestly.** Don't soften objections. Don't fake disagreement to look critical either.
5. **End every report with "What I did NOT verify."** Explicit section. Catches confabulation.
6. **One question per turn to Rhett.** Never stack multiple asks; never ask + report other items in the same turn.
7. **Times in user-facing text: 12-hour clock with AM/PM.** "9:09 AM ET" not "09:09 ET". Know the current time.

A new rule was added today for Claude Code (and applies to you too): **never reason from incomplete data.** If you find yourself filling a gap with plausible inference, stop and ask Rhett to query the actual file/log/data via Claude Code instead.

---

## What Claude Code will do next

Wait for your review. After your response (whether agree, disagree, or want edits), Rhett will pass it back to Claude Code. Then Claude Code starts the R1–R8 investigation and produces `SYSTEM_REVIEW_FINDINGS.md` for another round of your review.

No code changes, no fixes, no behavior changes are happening until you and Rhett both sign off on the plan.

---

## Bot state right now

- **PID 2360**, alive, last_seen ~9:09 AM ET, loop_count growing normally.
- **Active controls:** `BLOCK_ALL_NEW_ENTRIES` (until 12:30 PM advisor run replaces it), 3× `BLOCK_SYMBOL`, plus position-size and time-block overrides. Bot is not entering trades right now because of `BLOCK_ALL_NEW_ENTRIES`.
- **Watchdog supervisor** (separate python.exe) is keeping the bot alive.
- **No code changes are pending.** Rhett asked Claude Code to pause until this plan is reviewed.
