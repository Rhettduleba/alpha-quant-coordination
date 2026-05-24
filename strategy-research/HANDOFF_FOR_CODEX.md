# Handoff for Codex (and any repo-aware AI agent)

**Use this when:** Rhett prompts Codex (Cursor, Aider, or another repo-aware
agent) to contribute to Alpha Quant strategy research.

---

## Repo and document

- **Repo:** https://github.com/Rhettduleba/alpha-quant-coordination
- **Read first, in full:** `strategy-research/STRATEGY_LAB.md`
- Other strategy code: `strategy-research/` and `quantconnect/`.

## Required reading

Read `STRATEGY_LAB.md` in full before any work. Including:
- The purpose statement and the 6-stage protocol
- Rhett's goal, capital, and risk constraints
- The mandatory rules (G1, G2, intraday-only, margin-eligible universe)
- Claude Code's documented failure modes (so you know what to catch)
- Every strategy entry (H0-H3) including the "Constraints applied" table
- Open meta-issues M1-M4
- The Candidate Strategies menu

Do not skim. The history matters. The constraints matter.

---

## REQUIRED DISCIPLINE — apply on every task, no exceptions

These are non-negotiable for every contribution you make:

1. **State your assumptions before acting.** Before doing the work, write
   what you're assuming and what you might be wrong about.
2. **Ask yourself what's the most likely way you're wrong.** Run an
   adversarial self-check before delivering.
3. **Quote sources — don't paraphrase.** If you cite a paper or book, give
   the direct quote, author, year, page/section. Don't summarize from
   memory.
4. **Walk through your reasoning before committing to action.** Other AIs
   and Rhett must be able to audit your logic, not just your conclusion.
5. **Honest uncertainty.** "I don't know" beats a confident default. Label
   guesses as guesses.

---

## Default task — what Rhett wants from you unless he says otherwise

**Deep research + propose your best candidate strategy** for Rhett's
constraints. Specifically:

1. Use any research tools you have (web search, codebase search, training
   knowledge) to identify credible day-trading strategies with documented
   evidence of edge. Look at academic finance literature (SSRN, JFE),
   practitioner books with backtested results, QuantConnect's strategy
   library, and other credible sources.

2. From everything you find, identify ONE candidate that you believe is
   the best fit for Rhett's constraints:
   - $300k account, 4× intraday margin
   - Liquid US equities (margin-eligible)
   - Intraday-only (flatten by 3:50 PM ET, no overnight)
   - $2k daily loss cap
   - QuantConnect-backtestable

3. **Edit `strategy-research/STRATEGY_LAB.md` directly** to add your
   proposal under "Candidate strategies" as a new entry. Use the format
   in the next section.

4. Commit and push your edit with a clear message like
   `Codex: propose candidate C7 — <strategy name>`.

5. Reply to Rhett in chat with a short summary of what you found and what
   you added to the doc.

---

## Format for your candidate proposal (paste this into the lab doc)

```markdown
## C<N+1> — <Strategy name> [proposed by Codex <YYYY-MM-DD>]

**Source:** [Direct citation. Author(s), year, paper/book, link, section
or page. Quote key rules verbatim from the source.]

**Hypothesis (one falsifiable sentence + why it might be true):**
[...]

**Why this fits Rhett's constraints:**
- Intraday: [yes/how]
- Margin-eligible universe: [yes/how]
- G2 $2k daily cap survivable: [yes/how/concern]
- Trader-profile fit: [...]

**Proposed exact spec (every parameter, source-cited where possible):**
[full spec]

**What's most likely to go wrong:**
[Your adversarial self-check on this proposal]

**Confidence and uncertainty:**
[What you're confident in, what needs verification]

**Signed:** Codex [YYYY-MM-DD]
```

---

## If Rhett asks for something else

Default is deep-research-and-propose. But Rhett may instead ask for:
- **SPEC AUDIT** — read a specific strategy entry, audit it line-by-line
  against the cited source. Flag every deviation. Flag every uncited
  default. Confirm G1+G2+intraday+margin-eligible are present.
- **CODE AUDIT** — review a code file in the repo. Flag bugs, drift from
  spec, or missing constraints.
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
  price ≥ $5, ADV ≥ 1M shares, listed ≥ 1 year, exclude leveraged ETFs).
- Any strategy proposal that doesn't enforce all four is INVALID.

---

## What not to do

- Don't invent backtest numbers. If you don't have a result, say so.
- Don't paraphrase papers from memory and treat the paraphrase as faithful.
- Don't propose strategies without source citations.
- Don't silently fix Claude Code's specs. Flag drift, don't correct it.
- Don't delete prior AI commentary in the doc. Append only.

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
