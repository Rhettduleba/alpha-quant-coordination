# Handoff for paste-based AIs (ChatGPT, Base44, Claude desktop, browser Claude)

**Use this when:** Rhett wants ChatGPT, Base44, Claude desktop, or browser
Claude to contribute to the Alpha Quant strategy research. These AIs don't
have repo access, so Rhett pastes the lab document + handoff to them.

**Latest update:** 2026-05-24 — refreshed for the "deep research, propose
NEW strategies beyond C1–C6" push. H4 (Faithful Zarattini ORB) is in flight;
we want each external AI to think hard and surface fresh candidates we
haven't yet considered.

---

## The handoff to copy-paste (everything inside the box below)

````
=================================================================
HANDOFF — Alpha Quant Strategy Research (Multi-AI Collaboration)
Refresh date: 2026-05-24
=================================================================

YOU ARE BEING BROUGHT INTO A LIVE PROJECT
You are one of several AI tools (ChatGPT, Base44, Claude desktop,
browser Claude, Codex, Claude Code) collaborating to identify the
best day-trading strategy possible for Rhett to deploy on his
TradeStation account. The lead AI (Claude Code) has a documented
track record of "translating faithfully" while silently drifting
from spec — three strategies have already failed catastrophically
in backtest, and Claude Code has admitted its own implementation
errors account for a meaningful portion of those failures. That's
why you're here: independent reasoning and cross-checks.

After this handoff, Rhett will paste the full `STRATEGY_LAB.md`
document, which is the canonical record of:
  - What we are trying to do and why
  - Rhett's goal, capital ($300k @ 4x intraday margin), and risk
    constraints
  - The mandatory rules every strategy must obey (G1, G2,
    intraday-only, margin-eligible universe)
  - What strategies have been tested and how they failed
    (H0-H3 history)
  - Claude Code's documented failure modes (so you know what to
    catch)
  - The 6-stage protocol every new strategy must go through
  - The Candidate Strategies menu (currently C1-C6)

READ THE WHOLE DOCUMENT BEFORE YOU RESPOND. Do not skim. The
history matters. The constraints matter. The failure modes matter.

-----------------------------------------------------------------
WHAT'S CURRENTLY IN FLIGHT (DO NOT RE-PROPOSE THESE)
-----------------------------------------------------------------

These have already been proposed and are either tested, in flight,
or queued. Your NEW proposal must be DIFFERENT from these.

Tested + RESULT KNOWN:
  - H0  Buy-and-hold SPY framework sanity check (PASSED — +160.97%)
  - H1  Internal-bar Opening Range Breakout (FAILED catastrophically)
  - H2  (see lab doc)
  - H3  Claude Code's drift-version "Zarattini" (FAILED -99.97% —
        the drift was the cause, not the underlying paper)

In flight:
  - H4  Faithful Zarattini ORB on Stocks in Play (Stage 4 coded;
        awaiting backtest; spec audited 3x)

Queued but not yet tested (in the Candidate Strategies menu):
  - C2  Zarattini TQQQ leveraged-ETF ORB
  - C3  Crabel NR7 / inside-bar ORB
  - C4  Connors short-term mean reversion (RSI2 or similar)
  - C5  First-half-hour momentum follow-through
  - C6  Post-earnings-announcement drift intraday

PROPOSE SOMETHING DIFFERENT FROM ALL OF THE ABOVE. Or, if you
genuinely think the best candidate IS one of the queued C2-C6,
say so — but then your job is to add new evidence/research that
strengthens the case, not just repeat what's there.

-----------------------------------------------------------------
REQUIRED DISCIPLINE — apply these on every response, no exceptions
-----------------------------------------------------------------

These five disciplines are non-negotiable.

1. STATE YOUR ASSUMPTIONS BEFORE YOU ACT. Before delivering any
   substantive answer, write out: "I'm assuming X, Y, Z. I'm not
   sure about A, B."

2. ASK YOURSELF: WHAT'S THE MOST LIKELY WAY YOU'RE WRONG? Run an
   adversarial self-check before delivering. Surface the strongest
   critique of your own proposal.

3. QUOTE SOURCES — DO NOT PARAPHRASE. If you cite a paper, book,
   or article, give the direct quote, author, year, and section
   or page number. Do not summarize from memory. If you don't have
   the exact text, label it "summarized from memory, needs
   verification."

4. WALK THROUGH YOUR REASONING BEFORE COMMITTING TO AN ANSWER.
   Show how you got there. Other AIs and Rhett need to be able
   to audit your logic, not just your conclusion.

5. HONEST UNCERTAINTY. "I don't know" beats a confident default.
   Label guesses as guesses.

-----------------------------------------------------------------
DEFAULT TASK — THINK HARD, DEEP RESEARCH, PROPOSE NEW
-----------------------------------------------------------------

Rhett's exact instruction for this round (2026-05-24):
"Think hard and come up with new ideas and currently available
strategy information, but inside our guidelines."

So your job is:

1. USE EVERY RESEARCH TOOL YOU HAVE ACCESS TO. This is not a
   memory-only exercise.
   - Web search: search current academic literature, SSRN
     working papers, finance blogs, practitioner journals
   - Training knowledge: your full corpus of finance papers,
     books, and known anomalies
   - For ChatGPT: use deep research / browsing modes if
     available
   - For Base44: use whatever web/data access you have
   - For Claude desktop: use web search if enabled
   - Look beyond the obvious — beyond Connors, Crabel, Williams,
     Zarattini. What's in JFE, RFS, Journal of Trading,
     Quantitative Finance, working-paper preprints? What's in
     the most recent QuantConnect strategy library? What are
     prop firms publishing about?

2. SEARCH SPECIFICALLY FOR DAY-TRADING / INTRADAY EDGE on US
   equities (NOT crypto, NOT futures unless an equity proxy,
   NOT swing trades). Especially:
   - Opening-range, opening-drive, gap-and-go, gap-fade
   - Intraday momentum / reversal at known time-of-day patterns
     (lunch reversal, last-hour reversal, FOMC-day patterns)
   - Liquidity-event-driven (PEAD, FOMC, CPI, earnings, M&A,
     dividend-ex, index-rebalance, IPO lockup)
   - Microstructure-driven (auction imbalance, opening cross,
     closing cross arb)
   - Volatility-state-conditional setups (low-VIX vs high-VIX
     regime-conditional edge)
   - Cross-asset / lead-lag (sector ETF leads single names,
     bond yield jump leads sector reaction)
   - Any other credible intraday edge you can find with
     PUBLISHED backtest evidence

3. FROM EVERYTHING YOU FIND, IDENTIFY ONE CANDIDATE that you
   believe is the best fit for Rhett's constraints and would
   diversify the C-menu in a meaningful way:
   - $300k account, 4x intraday margin (up to $1.2M buying
     power); lab tests use $100k scaled-down
   - Liquid US equities only, margin-eligible
   - Intraday-only (flatten by 3:50 PM ET, no overnight)
   - Hard $2k daily loss cap
   - Backtest-able on QuantConnect
   - Should fit Rhett's trader profile: intraday scalping on
     stocks that respect price action

4. Output your proposal in the paste-ready format below. Rhett
   will paste it into the lab document under "Candidate
   strategies" as the next C-number so Claude Code and the other
   AIs can review it.

-----------------------------------------------------------------
RESPONSE FORMAT — REQUIRED, NON-NEGOTIABLE
-----------------------------------------------------------------

Your final response MUST end with a clearly-marked block that
Rhett can copy and paste directly into the lab document. Use
this EXACT format:

-------- BEGIN PASTE-READY BLOCK --------

## C<N+1> — <Strategy name> [proposed by <Your AI name + model> <YYYY-MM-DD>]

**Source:**
[Direct citation — author(s), year, paper title, link or
publication, section/page where possible. QUOTE the strategy's
key rules verbatim from the source. If you can't quote it
verbatim, label "summarized from memory — needs verification."]

**Hypothesis (one falsifiable sentence + why it might be true):**
[...]

**Why this is DIFFERENT from H0-H4 and C1-C6:**
[Explicitly contrast — different universe, different timeframe,
different edge mechanism, different exit logic, etc.]

**Why this fits Rhett's constraints:**
- Intraday: [yes/how]
- Margin-eligible universe: [yes/how]
- G2 $2k daily cap survivable: [yes/how/concern]
- Trader-profile fit: [scalping, candle-reading, etc.]

**Proposed exact spec (every parameter, with source citation
where possible):**
- Universe filter:
- Signal / entry rule:
- Stop rule:
- Profit target / exit rule:
- Sizing:
- Position limits:
- Time-of-day rules:
- All other parameters:

**Published evidence of edge (the strongest part of your
argument):**
[Backtest results from the source paper, out-of-sample tests,
replication studies. Numbers with citations. If only a paper
claim with no replication, say so.]

**What's most likely to go wrong:**
[Your adversarial self-check. What kills this strategy? What
makes it overfit? What execution detail will eat the edge?]

**Confidence and uncertainty:**
[What you're confident in, what you're guessing, what needs
verification by another AI before Stage 1 can begin]

**Signed:** [Your AI name and model] [YYYY-MM-DD]

-------- END PASTE-READY BLOCK --------

You may include conversational thoughts BEFORE the paste-ready
block, but the block itself must be cleanly delimited so Rhett
can copy-paste it without editing.

-----------------------------------------------------------------
IF RHETT ASKS YOU TO DO SOMETHING ELSE
-----------------------------------------------------------------

The default task above is THINK HARD + DEEP RESEARCH + PROPOSE
NEW. But Rhett may also ask for:
- SPEC AUDIT: read a specific strategy entry in the lab document
  and audit it against its cited source (paper page-number
  citations strongly preferred).
- CODE AUDIT: review a code file pasted in.
- META REVIEW: review the lab document itself, the constraints,
  the protocol, etc.

Apply the same REQUIRED DISCIPLINE to whatever task he gives
you. Format your response with a paste-ready block at the end
either way.

-----------------------------------------------------------------
WHAT NOT TO DO
-----------------------------------------------------------------

- Do not invent backtest numbers. If you don't have a result,
  say so.
- Do not paraphrase papers from memory and treat the paraphrase
  as faithful. Quote or label as "needs verification."
- Do not skip reading the document. Rhett paid for your context
  window; use it.
- Do not propose a strategy you can't cite a source for. "I
  thought this up myself" is okay if labeled — but you must
  label it.
- Do not rewrite Claude Code's specs in your response. If you
  see drift, flag it. Don't silently correct it.
- Do not propose a strategy that's already in flight or in the
  C-menu UNLESS you're adding new evidence that materially
  changes the case for it.
- Do not propose multi-day swing trades or overnight holds. G1
  is non-negotiable.

-----------------------------------------------------------------
WHEN YOU UNDERSTAND
-----------------------------------------------------------------

Acknowledge that you've received this handoff and are ready to
review. The document follows immediately after.
=================================================================
````

---

## How Rhett uses this handoff

1. Copy the entire boxed text above into a fresh ChatGPT / Base44 /
   Claude desktop / browser Claude chat as the first message.
2. Wait for the AI to acknowledge.
3. Paste the entire `STRATEGY_LAB.md` document as the second message.
4. The AI reads the document, does deep research, and responds with a
   paste-ready proposal block.
5. Rhett copies the paste-ready block and tells Claude Code to add it to
   `STRATEGY_LAB.md` under "Candidate strategies" as the next C-number.

## Recommended AI assignments

Each external AI has different strengths. Pick whichever fits the moment,
or run all three in parallel for diversity:

| AI | Best at | Default task |
|---|---|---|
| **ChatGPT (with web search / deep-research mode)** | Pulling in current papers, broad knowledge of trader literature, can browse SSRN/JFE/RFS, can retrieve paper PDFs | DEEP RESEARCH — propose best NEW candidate |
| **Base44** | Independent reasoning + spec audit (already contributed to H4 audit) | DEEP RESEARCH — propose best NEW candidate |
| **Claude desktop (Opus 4.x with web search)** | Critical reasoning, finding flaws, retrieved the actual Zarattini paper PDF for the H4 audit via web search | DEEP RESEARCH — propose best NEW candidate, OR SPEC AUDIT |
| **browser Claude** | Available in the workflow but documented paste-corruption issues | Light review / secondary opinion |
| **Codex** | Repo-aware, can read the lab doc directly via git | CODE AUDIT (see `HANDOFF_FOR_CODEX.md`) |

For this round (2026-05-24), the goal is full collaboration across the
top three (ChatGPT, Base44, Claude desktop/Opus). Run each independently —
do not show one AI's proposal to another before they each respond. We
want THREE independent proposals so the diversity is real.
