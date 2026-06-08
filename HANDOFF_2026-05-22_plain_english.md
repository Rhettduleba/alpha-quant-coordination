# Alpha Quant Research Brain — Plain-English Handoff

**For:** a human picking up this project
**Date:** May 22, 2026

## What this is

Alpha Quant is an automated stock-trading system running in **simulation only**
(no real money). It has two long-standing parts and one new one:

- **The Bot** — the part that actually places trades and enforces risk limits.
  It is deliberately simple and narrow.
- **The Advisor** — a safety layer that can tell the bot to hold back (block
  certain stocks, trade smaller).
- **The Research Brain** (new, built this week) — the part that decides *what
  stocks are worth trading in the first place*.

Before the brain, the bot traded a fixed list of 34 big-name stocks that someone
typed in by hand months ago. The brain replaces that hand-typed list with a list
rebuilt fresh every morning from the whole market.

## How the brain interacts with the rest of the system

Think of it as an assembly line with one hand-off point.

**1. Every weekday around 7:30 AM ET, before the market opens, the brain runs.**
It:
- Looks at every stock listed on the NYSE and NASDAQ — about 11,000 names.
- Narrows them to a tradeable list of ~150 by objective criteria: priced
  $20–$600, heavily traded, tight buy/sell spread, not halted.
- Studies that list — the overall market mood, which stocks are moving and how,
  which sectors are leading, a technical read on each, and a quality score for each.
- Writes the final ~150-stock list into **one file** — the "universe channel."

**2. The bot reads that file.** Every time the bot runs its trading cycle it
picks up the brain's file and scans those ~150 stocks instead of the old 34.
That file is the *only* thing the brain hands the bot — a plain, typed list of
stock symbols.

**3. The bot still makes every real decision itself.** This is the important
part. The brain only changes *which stocks the bot looks at*. The bot then
applies all of its own rules — its entry signals, its loss limits, its position
caps, its sector limits — exactly as before. The brain cannot place a trade,
change a risk limit, or override the bot. It can only put names on the bot's
watch list.

**4. After the close, around 4:35 PM ET, a second small job runs.** It records
the day's trading volume for each stock. The brain needs that to know which
stocks count as "heavily traded" when it builds the next morning's list.

So the daily rhythm is: **7:30 AM the brain builds the list → 9:30 AM–4:00 PM
the bot trades from it → 4:35 PM volume gets recorded for tomorrow.** All of it
runs automatically on a schedule.

## Why a broken brain can't hurt anything

The brain and the bot are deliberately kept at arm's length:

- The hand-off is **one-way and one file**. The brain writes; the bot reads.
  The brain never reaches into the bot's settings or code.
- If the brain's file is **missing, corrupted, stale, or wrong in any way**, the
  bot notices and automatically falls back to its original hand-typed 34-stock
  list. A broken brain just means "trade the old list" — it can never freeze the
  bot or widen its risk.
- The bot keeps **every one of its own safety limits** no matter what list it is
  given: maximum daily loss, maximum number of open positions, maximum position
  size, and so on.
- Everything is **simulation-only**. No real money is involved.

## What is live right now

- The brain is built and scheduled. Two automatic jobs run every weekday
  (about 7:30 AM and about 4:35 PM ET).
- The bot is connected to the brain's universe file.
- The brain has run successfully and produced real ~150-stock lists.
- There is a human-readable daily report, and an alert system (Discord/Telegram)
  that fires if a brain run fails or produces an empty list.

## What is honestly NOT proven, and NOT finished

This part matters — stay skeptical:

- **There is no evidence yet that the brain improves results.** It has changed
  *which* stocks the bot trades, but the bot's underlying trading strategy is
  unchanged — and that strategy has been running at a small net loss
  historically. A bigger or better stock list does not automatically fix an
  unprofitable strategy.
- **The brain scores each stock (A+, Strong, Good, and so on) — but the bot
  ignores those scores.** That is on purpose. We do not trust the scoring until
  there is proof it works; wiring an unproven score into real decisions could
  make things worse.
- **A "measurement loop" is being built.** It records what the brain predicted
  versus what actually happened, day by day, so we can eventually answer "is the
  brain's scoring any good?" Until that has weeks of data, every conclusion is
  provisional.
- The brain cannot yet tell *why* a stock is moving (news, earnings) — that data
  source is not connected yet.
- The first list is liquidity-ranked, so it leans heavily on ETFs (including
  cash-like and leveraged ones). Refining that is a known to-do.

## How to tell it is working

- Read the daily report file `research_brain_report.md` — it shows the day's
  market read and the top candidate stocks in plain terms.
- If a brain run fails or produces an empty list, an alert is sent automatically.
- The two scheduled jobs ("AlphaQuant Research Brain" and "AlphaQuant Volume
  Capture") should show as having run successfully each weekday.

## Who decides what

A human owns every decision that changes real trading behavior. The brain
proposes a stock list; it does not get to expand its own role. Turning on
anything new — such as letting the bot actually act on the brain's scores —
requires explicit human approval, and first, evidence from the measurement loop
that it is worth doing.
