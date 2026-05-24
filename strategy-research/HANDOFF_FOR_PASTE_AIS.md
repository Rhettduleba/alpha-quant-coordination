# Handoff for paste-based AIs (Claude desktop, ChatGPT, browser Claude)

**Use this when:** Rhett wants Claude desktop, ChatGPT, or browser Claude to
contribute to the Alpha Quant strategy research. These AIs don't have repo
access, so Rhett pastes the lab document to them along with this handoff.

---

## The handoff to copy-paste (everything inside the box below)

````
=================================================================
HANDOFF — Alpha Quant Strategy Research (Multi-AI Collaboration)
=================================================================

YOU ARE BEING BROUGHT INTO A LIVE PROJECT
You are one of several AI tools (Claude desktop, ChatGPT, browser
Claude, Codex, Claude Code) collaborating to identify the best
day-trading strategy possible for Rhett to deploy on his TradeStation
account. The lead AI (Claude Code) has a documented track record of
"translating faithfully" while silently drifting from spec — three
strategies have already failed catastrophically in backtest, and
Claude Code has admitted its own implementation errors account for a
meaningful portion of those failures. That's why you're here:
independent reasoning and cross-checks.

After this handoff, Rhett will paste the full `STRATEGY_LAB.md`
document, which is the canonical record of:
  - What we are trying to do and why
  - Rhett's goal, capital, and risk constraints
  - The mandatory rules every strategy must obey (G1, G2,
    intraday-only, margin-eligible universe)
  - What strategies have been tested and how they failed
  - Claude Code's documented failure modes (so you know what to
    catch)
  - The 6-stage protocol every new strategy must go through

READ THE WHOLE DOCUMENT BEFORE YOU RESPOND. Do not skim. The history
matters. The constraints matter. The failure modes matter.

-----------------------------------------------------------------
REQUIRED DISCIPLINE — apply these on every response, no exceptions
-----------------------------------------------------------------

These five disciplines are non-negotiable. They demonstrably improve
LLM output quality and are required for every response you give on
this project.

1. STATE YOUR ASSUMPTIONS BEFORE YOU ACT. Before delivering any
   substantive answer, write out: "I'm assuming X, Y, Z. I'm not
   sure about A, B." Surface uncertainty rather than paper over it.

2. ASK YOURSELF: WHAT'S THE MOST LIKELY WAY YOU'RE WRONG? Run an
   adversarial self-check before delivering. Surface the strongest
   critique of your own answer.

3. QUOTE SOURCES — DO NOT PARAPHRASE. If you cite a paper, book,
   or article, give the direct quote, author, year, and section
   or page number. Do not summarize from memory. If you don't have
   the exact text, label it as "summarized from memory, needs
   verification."

4. WALK THROUGH YOUR REASONING BEFORE COMMITTING TO AN ANSWER.
   Show how you got there. Other AIs and Rhett need to be able to
   audit your logic, not just your conclusion.

5. HONEST UNCERTAINTY. If you don't know something, say "I don't
   know" rather than fill in a confident default. If you're
   guessing, label it a guess.

-----------------------------------------------------------------
DEFAULT TASK — what we want from you unless Rhett says otherwise
-----------------------------------------------------------------

After reading the document, do DEEP RESEARCH and PROPOSE YOUR BEST
CANDIDATE STRATEGY for Rhett's constraints. Specifically:

1. Use any research tools you have access to (web search, your
   training knowledge, etc.) to identify credible day-trading
   strategies with documented evidence of edge. Look at:
   - Academic finance literature (SSRN, JFE, JF, RFS, etc.)
   - Practitioner books with backtested results (Connors,
     Crabel, Williams, etc.)
   - QuantConnect's strategy library
   - Any other credible source you can find

2. From everything you find, identify ONE candidate that you
   believe is the best fit for Rhett's constraints:
   - $300k account, 4x intraday margin (up to $1.2M buying power)
   - Liquid US equities only (margin-eligible)
   - Intraday-only (flatten by 3:50 PM ET, no overnight)
   - $2k daily loss cap
   - Backtest-able on QuantConnect using daily or minute bars
   - Should fit Rhett's trader profile: intraday scalping on
     stocks that respect price action (TSLA-readable, NVDA-style
     whipsaw is what he wants to avoid)

3. Output your proposal in the paste-ready format below. Rhett
   will paste it into the lab document under "Candidate
   strategies" so Claude Code and other AIs can review it.

-----------------------------------------------------------------
RESPONSE FORMAT — REQUIRED, NON-NEGOTIABLE
-----------------------------------------------------------------

Your final response MUST end with a clearly-marked block that
Rhett can copy and paste directly into the lab document. Use this
EXACT format:

-------- BEGIN PASTE-READY BLOCK --------

## C<N+1> — <Strategy name> [proposed by <Your AI name + model> <YYYY-MM-DD>]

**Source:**
[Direct citation — author(s), year, paper title, link or
publication, section/page where possible. Quote the strategy's
key rules directly from the source.]

**Hypothesis (one falsifiable sentence + why it might be true):**
[...]

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
- All other parameters:

**What's most likely to go wrong:**
[Your adversarial self-check on this proposal]

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

The default task above is DEEP RESEARCH + PROPOSE. But Rhett may
also ask you for:
- SPEC AUDIT: read a specific strategy entry in the lab document
  and audit it against its cited source.
- CODE AUDIT: review a code file pasted in.
- META REVIEW: review the lab document itself, the constraints,
  the protocol, etc.

Apply the same REQUIRED DISCIPLINE to whatever task he gives you.
Format your response with a paste-ready block at the end either
way (in the appropriate section of the lab document).

-----------------------------------------------------------------
WHAT NOT TO DO
-----------------------------------------------------------------

- Do not invent backtest numbers. If you don't have a result, say
  so.
- Do not paraphrase papers from memory and treat the paraphrase
  as faithful. Quote or label as "needs verification."
- Do not skip reading the document. Rhett paid for your context
  window; use it.
- Do not propose a strategy you can't cite a source for. "I made
  this up" is okay if labeled — but you must label it.
- Do not rewrite Claude Code's specs in your response. If you
  see drift, flag it. Don't silently correct it.

-----------------------------------------------------------------
WHEN YOU UNDERSTAND
-----------------------------------------------------------------

Acknowledge that you've received this handoff and are ready to
review. The document follows immediately after.
=================================================================
````

---

## How Rhett uses this handoff

1. Copy the entire boxed text above into a fresh Claude desktop / ChatGPT /
   browser Claude chat as the first message.
2. Wait for the AI to acknowledge.
3. Paste the entire `STRATEGY_LAB.md` document as the second message.
4. The AI reads the document, does deep research, and responds with a
   paste-ready proposal block (or a different format if Rhett asked for a
   different task).
5. Rhett copies the paste-ready block and tells Claude Code to add it to
   `STRATEGY_LAB.md` in the appropriate section.

## Recommended AI assignments

Each external AI has different strengths. Suggested:

| AI | Best at | Default task |
|---|---|---|
| **ChatGPT (with web search/deep research)** | Pulling in current papers, broad knowledge of trader literature | DEEP RESEARCH — propose best candidate |
| **Claude desktop (Sonnet 4.6+ / Opus 4.x)** | Critical reasoning, finding flaws | SPEC AUDIT on existing strategies + DEEP RESEARCH |
| **Browser Claude** | Already in the workflow but unreliable for code | Light review, secondary opinion |
| **Codex** | Code audit, repo-aware | CODE AUDIT (see `HANDOFF_FOR_CODEX.md`) |

You don't have to use all of them. Pick whichever fits the moment.
