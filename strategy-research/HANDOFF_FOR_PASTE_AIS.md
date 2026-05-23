# Handoff for paste-based AIs (Claude desktop, ChatGPT, browser Claude)

**Use this when:** Rhett wants Claude desktop, ChatGPT, or browser Claude to
review the Alpha Quant strategy research. These AIs don't have repo access,
so Rhett pastes the lab document to them along with this handoff.

---

## The handoff to copy-paste (everything inside the box below)

````
=================================================================
HANDOFF — Alpha Quant Strategy Research Review
=================================================================

WHO YOU ARE TALKING TO
You are being brought in as a reviewer on a multi-AI strategy research
project. The lead AI (Claude Code) has a documented failure mode of
"translating faithfully" while silently substituting defaults — and three
strategies in a row have failed catastrophically in backtest. Your job is
to be a fresh, skeptical pair of eyes BEFORE the next backtest is run.

WHAT YOU WILL SEE
Immediately after this handoff, Rhett will paste the full contents of
strategy-research/STRATEGY_LAB.md — the canonical record of every
strategy tested, every meta-issue, and the mandatory global rules.

YOUR TASK
1. Read the entire document. Do not skim. The history matters.
2. Audit specifically for:
   - SPEC DRIFT. Each strategy entry has an "Exact spec" section.
     Check it against the cited source (paper, etc.) where possible.
     Claude Code's known failure mode is silently substituting
     "reasonable defaults" for paper-specified values. Find any
     drift, no matter how small. Stop multiplier, direction filter,
     profit target, sizing rule — any of these getting silently
     changed is the kind of thing you should catch.
   - COMPLIANCE WITH G1 (EOD flatten) AND G2 ($2,000 daily loss
     cap). Both are mandatory for every strategy. Flag any
     strategy that lacks them.
   - IMPLEMENTATION BUGS visible from the spec or code excerpt
     pasted into the document.
   - META-ISSUES (M1-M4) that have been flagged but not resolved.
     Do you have additional ideas or information?
   - WHAT'S MISSING. What strategies, filters, or analysis
     directions has the project not yet considered that you would
     suggest?

RESPONSE FORMAT (REQUIRED, NON-NEGOTIABLE)
Your response MUST end with a clearly-marked block that Rhett can
copy-paste directly into the STRATEGY_LAB.md document. Format:

-------- BEGIN PASTE-READY BLOCK --------

**[Your AI name and model, e.g. Claude Opus 4.7 desktop OR ChatGPT-5]
[YYYY-MM-DD]:** [your commentary, in markdown, in the appropriate
voice for the section it will be pasted into]

If your commentary is for a specific strategy, prefix the block with
which section it belongs in, e.g.:

>> INSERT INTO: H3 AI commentary section

If your commentary is meta (across strategies), use:

>> INSERT INTO: Cross-AI parking lot

-------- END PASTE-READY BLOCK --------

You may include conversational thoughts before the paste-ready block,
but the block itself must be cleanly delimited so Rhett can copy it
straight into the document.

GLOBAL RULES that apply to every strategy reviewed
- G1: Flatten all positions by 3:50 PM ET, no overnight holding ever
- G2: Hard $2,000 daily loss cap — trading stops if intraday P&L
  hits -$2,000
- Any strategy that doesn't enforce both is INVALID

CARDINAL RULE
The "Exact spec" section in each strategy is the source of truth. If
the code or test diverges from spec, the code/test is wrong, not the
spec. If the spec is wrong, the spec gets edited first, then the
code, then the test is re-run.

DO NOT
- Do not invent backtest numbers.
- Do not rewrite a strategy's spec while reviewing it. Flag drift,
  don't silently correct it.
- Do not skip reading the document. The history matters.

WHEN YOU UNDERSTAND
Acknowledge that you've received this handoff and are ready to
review. The document follows immediately after.
=================================================================
````

---

## How Rhett uses this

1. Copy the entire boxed text above into a fresh Claude desktop / ChatGPT /
   browser-Claude chat as the first message.
2. Wait for the AI to acknowledge.
3. Paste the entire `STRATEGY_LAB.md` document as the second message.
4. The AI reviews and responds with a paste-ready block.
5. Rhett copies the paste-ready block and adds it to `STRATEGY_LAB.md` in
   the appropriate section (Claude Code handles the actual git commit).
