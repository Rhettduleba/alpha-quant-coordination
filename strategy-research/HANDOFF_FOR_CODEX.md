# Handoff for Codex (and any repo-aware AI agent)

**Use this when:** Rhett prompts an agent with repo access (Codex, Cursor,
Claude Code in another session, etc.) to audit or contribute to the Alpha
Quant strategy research.

---

## Repo and document

- **Repo:** https://github.com/Rhettduleba/alpha-quant-coordination
- **Read first, in full:** `strategy-research/STRATEGY_LAB.md`
- All other strategy code referenced lives in `strategy-research/` or
  `quantconnect/`.

## Your task

1. **Clone the repo (or read it directly via the GitHub API).**
2. **Read `STRATEGY_LAB.md` in full before doing anything else.** Including
   every strategy entry, every meta-issue (M1–M4), and the mandatory global
   rules (G1, G2). Do not skim. The document is the project history.
3. **Read the referenced strategy code** for whichever strategy/strategies
   you've been asked to audit. Compare line-by-line against the "Exact spec"
   section of that strategy's entry.
4. **Audit specifically for:**
   - **Spec drift.** Claude Code has a documented failure mode of
     substituting "reasonable defaults" for paper-specified values, then
     labeling the result faithful. Find any such drift.
   - **Compliance with G1 (EOD flatten) and G2 ($2,000 daily loss cap).**
     Future strategies that don't include these are invalid.
   - **Implementation bugs** independent of strategy choice — sizing math,
     stop calculation, fill modeling, etc.
   - **Open meta-issues (M1–M4)** — do you have additional information or
     ideas to resolve them?

## Response format — REQUIRED

You have two outputs:

### Output 1: edit STRATEGY_LAB.md directly and push
- Open `strategy-research/STRATEGY_LAB.md` in your editor.
- Append your commentary into the relevant strategy's "AI commentary"
  section. Use this format:
  ```markdown
  - **Codex [YYYY-MM-DD]:** [your findings, in plain prose or
    structured bullets]
  ```
- If you have a meta-observation that doesn't fit a single strategy, append
  it to the "Cross-AI parking lot" at the bottom of the document.
- Commit with a short descriptive message like
  `Codex review: H3 spec audit — flagged 3 deviations`.
- Push.

### Output 2: respond to Rhett in chat with a summary
After pushing, send Rhett a short message summarizing:
- What you reviewed
- What you found
- What you appended to the document
- Anything that needs human decision

## Mandatory global rules (apply to every strategy you review or propose)

- **G1 — EOD flatten by 3:50 PM ET.** No overnight positions ever.
- **G2 — Hard $2,000 daily loss cap.** Trading stops for the rest of the
  day if intraday P&L drops to −$2,000.
- A strategy that doesn't include both is INVALID and must be fixed
  before any backtest result counts.

## Project context (one paragraph)

Alpha Quant is Rhett's automated trading research project. The current
sub-project is strategy research in QuantConnect — testing falsifiable
day-trading hypotheses one at a time. Three strategies have failed
catastrophically so far (Alpha Quant original −99.92%, H1 −72%, H3 −99.97%),
and Claude Code has owned that the failure pattern points at *its own
implementation* more than at the strategies. The lab document was created
to bring multiple AIs into the review loop specifically to catch Claude
Code's blind spots. You are part of that review loop.

## Rhett's goal

$100,000 capital target ~$10,000 target return; max $500/day loss tolerance
in live trading (the lab uses $2,000/day for backtest research headroom).
Goal pursued through honest iteration of strategy hypotheses.

## Do NOT

- Do not invent backtest numbers. If you're auditing code, you can compute
  expected behavior, but never fabricate a "what the backtest would show."
- Do not rewrite a strategy's spec while auditing it. If the spec is wrong,
  flag it and let Rhett decide.
- Do not delete prior AI commentary. Append only. Wrong analysis is itself
  useful evidence.
