# Handoff for Codex (and any repo-aware AI agent)

**Use this when:** Rhett prompts Codex (Cursor, Aider, or another repo-aware
agent) to contribute to Alpha Quant strategy research.

**Latest update:** 2026-05-24 — refreshed for the "deep research, propose
NEW strategies beyond C1–C6" push. H4 is in flight; we want NEW candidates.

---

## Repo and document

- **Repo:** https://github.com/Rhettduleba/alpha-quant-coordination
- **Read first, in full:** `strategy-research/STRATEGY_LAB.md`
- Other strategy code: `strategy-research/` (includes `h4_zarattini_orb.py`
  the current in-flight implementation).

## Required reading

Read `STRATEGY_LAB.md` in full before any work. Including:
- The purpose statement and the 6-stage protocol
- Rhett's goal ($300k @ 4× intraday margin), capital, and risk constraints
- The mandatory rules (G1 3:50 PM flatten, G2 $2k daily cap,
  intraday-only, margin-eligible universe)
- Claude Code's documented failure modes (so you know what to catch)
- Every strategy entry (H0–H4) including the "Constraints applied" table
- Open meta-issues M1–M4
- The Candidate Strategies menu (C1–C6)

Do not skim. The history matters. The constraints matter.

---

## What's currently in flight (don't re-propose)

Tested + RESULT KNOWN:
- H0 buy-and-hold SPY framework sanity (PASSED, +160.97%)
- H1 internal-bar ORB (FAILED catastrophically)
- H2 (see lab doc)
- H3 drift-version Zarattini (FAILED −99.97%, drift was the cause)

In flight:
- H4 faithful Zarattini ORB on Stocks in Play (Stage 4 coded; awaiting
  backtest; spec audited 3×)

Queued in C-menu, not yet tested:
- C2 Zarattini TQQQ leveraged-ETF ORB
- C3 Crabel NR7 / inside-bar ORB
- C4 Connors short-term mean reversion
- C5 first-half-hour momentum follow-through
- C6 post-earnings-announcement drift intraday

Your NEW proposal must be different from all of the above, OR explicitly
strengthen the case for one of the queued candidates with NEW evidence
or refined spec.

---

## REQUIRED DISCIPLINE — apply on every task, no exceptions

1. **State your assumptions before acting.** Write what you're assuming
   and what you might be wrong about.
2. **Ask yourself what's the most likely way you're wrong.** Run an
   adversarial self-check before delivering.
3. **Quote sources — don't paraphrase.** If you cite a paper or book,
   give the direct quote, author, year, page/section. Don't summarize
   from memory.
4. **Walk through your reasoning before committing to action.** Other AIs
   and Rhett must be able to audit your logic, not just your conclusion.
5. **Honest uncertainty.** "I don't know" beats a confident default.
   Label guesses as guesses.

---

## Default task — THINK HARD + DEEP RESEARCH + PROPOSE NEW

Rhett's exact instruction for this round (2026-05-24):
*"Think hard and come up with new ideas and currently available strategy
information, but inside our guidelines."*

So:

1. Use every research tool available to you — web search, your training
   knowledge, the QC strategy library, SSRN, JFE, RFS, finance blogs,
   prop-firm publications, working papers. Don't rely on memory alone.

2. Search specifically for INTRADAY DAY-TRADING edge on US equities. Areas
   worth searching:
   - Opening-range, opening-drive, gap-and-go, gap-fade
   - Intraday momentum / reversal at time-of-day patterns (lunch reversal,
     last-hour reversal, FOMC-day patterns)
   - Liquidity-event-driven (PEAD, FOMC, CPI, earnings, M&A, dividend-ex,
     index-rebalance, IPO lockup)
   - Microstructure (auction imbalance, opening cross, closing cross arb)
   - Volatility-regime-conditional (low-VIX vs high-VIX edge)
   - Cross-asset / lead-lag (sector ETF leads single names, etc.)
   - Anything else credible with PUBLISHED backtest evidence

3. Identify ONE candidate that you believe is the best fit for Rhett's
   constraints AND meaningfully diversifies the C-menu:
   - $300k account, 4× intraday margin (up to $1.2M buying power); lab
     tests use $100k scaled-down
   - Liquid US equities, margin-eligible
   - Intraday-only (flatten by 3:50 PM ET, no overnight)
   - $2k daily loss cap
   - QuantConnect-backtestable

4. **Edit `strategy-research/STRATEGY_LAB.md` directly** to add your
   proposal under "Candidate strategies" as a new C-entry. Use the format
   in the next section.

5. Commit and push with a clear message like
   `Codex: propose candidate C7 — <strategy name>`.

6. Reply to Rhett in chat with a short summary of what you found and what
   you added to the doc.

---

## Format for your candidate proposal (paste this into the lab doc)

```markdown
## C<N+1> — <Strategy name> [proposed by Codex <YYYY-MM-DD>]

**Source:** [Direct citation. Author(s), year, paper/book, link, section
or page. QUOTE key rules verbatim from the source. If you can't quote it,
label "summarized from memory, needs verification."]

**Hypothesis (one falsifiable sentence + why it might be true):**
[...]

**Why this is DIFFERENT from H0-H4 and C1-C6:**
[Different universe / timeframe / edge mechanism / exit logic / etc.]

**Why this fits Rhett's constraints:**
- Intraday: [yes/how]
- Margin-eligible universe: [yes/how]
- G2 $2k daily cap survivable: [yes/how/concern]
- Trader-profile fit: [...]

**Proposed exact spec (every parameter, source-cited where possible):**
[full spec]

**Published evidence of edge:**
[Backtest results from source paper, out-of-sample tests, replications.
Numbers with citations.]

**What's most likely to go wrong:**
[Your adversarial self-check on this proposal]

**Confidence and uncertainty:**
[What you're confident in, what needs verification]

**Signed:** Codex [YYYY-MM-DD]
```

---

## If Rhett asks for something else

Default is THINK HARD + DEEP RESEARCH + PROPOSE NEW. But Rhett may instead
ask for:
- **SPEC AUDIT** — read a specific strategy entry, audit it line-by-line
  against the cited source. Flag every deviation. Flag every uncited
  default. Confirm G1+G2+intraday+margin-eligible are present.
- **CODE AUDIT** — review a code file in the repo (e.g.
  `h4_zarattini_orb.py`). Flag bugs, drift from spec, or missing
  constraints. Verify every line traces to a spec row.
- **META REVIEW** — review the lab document, the protocol, the
  constraints, the framework.

Apply the same REQUIRED DISCIPLINE to whatever task he gives you. Append
your findings to the appropriate section of the lab doc and commit.

---

## Mandatory global rules to keep in mind on every contribution

- **G1:** EOD flatten by 3:50 PM ET. No overnight positions.
- **G2:** Hard $2,000 daily loss cap. Trading stops for the day if hit.
- **Margin-eligible universe only.** No leveraged ETFs, no names that
  TradeStation won't grant 4× intraday margin on. If you can't verify
  margin-eligibility, propose a conservative approximation (NYSE/NASDAQ,
  price ≥ $7 [our lab buffer above paper's $5], ADV ≥ 1M shares, listed
  ≥ 1 year, exclude leveraged ETFs).
- Any strategy proposal that doesn't enforce all four is INVALID.

---

## What not to do

- Don't invent backtest numbers. If you don't have a result, say so.
- Don't paraphrase papers from memory and treat the paraphrase as
  faithful.
- Don't propose strategies without source citations.
- Don't silently fix Claude Code's specs. Flag drift, don't correct it.
- Don't delete prior AI commentary in the doc. Append only.
- Don't propose multi-day swing trades or overnight holds — G1 is
  non-negotiable.

---

## Project context (one paragraph)

Alpha Quant is Rhett Duleba's automated trading research project. The
current sub-project is strategy research in QuantConnect — testing
falsifiable day-trading hypotheses one at a time. Three strategies have
failed catastrophically so far, and Claude Code (the lead AI) owns that
its own implementation errors account for a meaningful share of those
failures. This multi-AI collaboration exists specifically to catch
Claude Code's blind spots before they cost more backtests or real money.
You are part of that collaboration.
