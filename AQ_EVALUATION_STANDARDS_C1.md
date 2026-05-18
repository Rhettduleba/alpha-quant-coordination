# ALPHA QUANT — EVALUATION STANDARDS (C1)
**Version:** 1.0
**Date:** 2026-05-12 (drafted) · 2026-05-18 (status updated)
**Status:** ⚠ **§3 (STATISTICAL THRESHOLDS) IS NOT FIT FOR USE — pending structural rewrite.** The rest of the document (evidence tiers as a concept, evidence hierarchy, proposal format, rollback discipline, anti-patterns) is usable as guidance. But §3's sample-size and effect-size numbers are statistically incompatible (a +2pp win-rate bar against a 100-trade minimum sample — 2pp is inside the noise band) and must not be used to evaluate any change until rewritten. The §1.4-equivalent baseline (60.6% WR / 1.30 PF / 4,274 trades, held in State of Record §1.4) is also unverified and must be confirmed against the trade journal before any threshold here is trusted. Do NOT evaluate roadmap item #3 against this document until §3 is fixed. See `ALPHA_QUANT_STATE.md` §7 for the full status note.
**Purpose:** Define the standards every proposed change to Alpha Quant must pass before being accepted, kept, or rolled back. This document is the referee — once §3 is sound.

---

## 0. WHY THIS EXISTS

Most trading systems get worse over time because changes get adopted on the basis of "it looked good" or "I had a good feeling about it" or "it worked last week." Every retail trader you've ever read about who blew up did so because they kept changing things without a standard for what "actually helped" means.

This document is the standard. Before any change is implemented, it must specify how it will be evaluated against these rules. After any change is implemented, it must be measured against these rules. If it fails, it gets rolled back. No exceptions, no "give it one more week."

This is not optional rigor. This is the price of getting better instead of worse.

---

## 1. WHAT COUNTS AS A "CHANGE"

A change is any modification to AQ that could plausibly affect performance. This includes:

- Entry logic (filters, scoring weights, signal definitions)
- Exit logic (stop levels, trail distances, breakeven rules)
- Universe (adding/removing symbols, sector caps)
- Risk parameters (daily loss, position size, sector limits)
- Advisor prompt content (new sections, modified standing rules, changed schemas)
- Advisor control types (new types, modified behavior of existing types)
- Volatility regime classifier
- Time-of-day rules

What doesn't count as a change requiring this framework:
- Bug fixes (errors that prevent code from running correctly)
- Operational changes (deployment, scheduling, logging)
- Read-only additions (new metrics displayed, new logs written)
- Refactors that demonstrably don't change behavior

When in doubt, treat it as a change.

---

## 2. MINIMUM EVIDENCE BEFORE A CHANGE IS PROPOSED

A change cannot be proposed for implementation without meeting one of these evidence bars:

### 2.1 Evidence Tier A — Backtest-supported
The change is supported by analysis of the 4,274-trade backtest baseline OR a similarly-sized historical dataset. Requirements:
- Effect size is meaningful (not just statistically detectable — see §3 below)
- Effect is consistent across at least 3 different time periods (no single-window cherry-picking)
- The mechanism is intuitive (we can explain *why* it should work, not just that it correlates)
- Sample size for any sub-condition is ≥ 100 trades, OR the condition is explicitly flagged as exploratory

### 2.2 Evidence Tier B — Live-data-supported
The change is supported by analysis of accumulated live or SIM data from AQ itself. Requirements:
- Minimum 30 trading days of live/SIM data OR 300 trades, whichever is greater
- Effect persists across at least 3 distinct weeks (not just one good week)
- Sub-conditions still require ≥ 100 trades to be actionable

### 2.3 Evidence Tier C — Theory-supported (limited use)
The change is supported by reasoning from established market microstructure or trading theory, not by direct AQ data. Requirements:
- Must cite the specific source / principle (not "everyone knows")
- Must be implemented behind a clear A/B test or flag, not pushed live universally
- Must be re-evaluated at 30-day mark against Tier B standard
- **Cap: no more than 2 Tier C changes active simultaneously.** Theory without data accumulates risk fast.

### 2.4 Insufficient Evidence
Anything that doesn't meet A, B, or C is not actionable. Examples that fail:
- "This worked on one good trading day"
- "I read this on a trading blog"
- "Successful traders do X"
- "It feels like AQ is missing this"
- "Claude said it would help"

If a change can't meet one of the three tiers, the answer is **not** "try it anyway." The answer is "gather more evidence first."

---

## 3. STATISTICAL THRESHOLDS

### 3.1 Sample Size Rules
- **Per condition:** ≥ 100 trades minimum to claim a difference exists
- **For sub-tier breakdowns (e.g., HIGH-tier × 10–11 AM × long):** ≥ 50 trades, and the finding is flagged as preliminary
- **For per-symbol claims:** ≥ 30 trades per symbol, and the finding is flagged as preliminary

These are *minimum* sample sizes for *any* claim. They are not sample sizes for *strong* claims — those require multiples of the above.

### 3.2 Effect Size Rules
A statistically detectable difference is not enough. The effect must be meaningful relative to AQ's baseline.

Baseline: 60.6% WR, 1.30 PF, $35.85 avg P&L per trade.

For a change to qualify as "meaningful improvement":
- **Win rate:** +2 percentage points or more (62.6%+) for the relevant trade subset
- **Profit factor:** +0.10 or more (1.40+) for the relevant trade subset
- **Average P&L:** +$5/trade or more
- **OR drawdown reduction:** -15% or more without harming above three metrics

Smaller differences are likely noise and not worth implementation cost or complexity.

### 3.3 Anti-Overfitting Rules
- **Walk-forward validation required** for any change supported by historical data. Split the dataset into multiple non-overlapping windows; the effect must hold in at least 2/3 of windows.
- **Out-of-sample reservation:** The most recent 20% of data is OFF LIMITS for backtest-driven proposals. It's reserved for final validation only.
- **No parameter optimization on the same data used to validate.** If you tune a threshold on a dataset, you cannot then claim the threshold "works" by testing it on that same dataset.
- **Complexity penalty:** Every new parameter, filter, or rule must justify itself. A change that adds 3 parameters and improves PF by 0.05 is likely overfitting. A change that adds 1 parameter and improves PF by 0.20 is worth examining.

### 3.4 Multiple Comparisons
If you test 20 ideas, one will look "statistically significant" by chance. Rules:
- When testing many candidate changes simultaneously, apply Bonferroni-style correction: require effect size + sample size meeting the standard *multiplied by the number of comparisons*
- Or, simpler: test one focused hypothesis at a time and stop the practice of fishing

---

## 4. POST-IMPLEMENTATION MEASUREMENT

Every change that gets implemented has a defined evaluation window before it's considered "kept" or "rolled back."

### 4.1 Evaluation Window
- **Default:** 30 trading days OR 300 trades, whichever is greater
- **Extended (for low-frequency changes):** Up to 60 trading days if the change only affects a small subset of trades
- **Cannot be shortened** because "it's clearly working" — looks-good early is exactly when overfitting hides

### 4.2 Success Criteria
A change is "kept" if at end of evaluation window, the affected trade subset shows:
- All of: WR, PF, and avg P&L meet or exceed pre-change baseline by at least the §3.2 effect size thresholds
- Drawdown is no worse than pre-change baseline
- No new failure modes appeared (concentrated losses, regime-specific blowups, unexpected behavior)

A change is "rolled back" if any of:
- Any of WR, PF, or avg P&L is worse than pre-change baseline by 50% of the §3.2 threshold (i.e., -1 percentage point WR, -0.05 PF, -$2.50/trade)
- Drawdown is worse than pre-change baseline by 15% or more
- A new failure mode appeared
- The change is producing behavior we don't understand

A change is "extended" (evaluation continues) if:
- Results are mixed (some metrics improved, some flat)
- Sample size hit the minimum but is small enough that another 30 days would clarify
- Extension cannot exceed one additional 30-day window. After that, decide.

### 4.3 Comparison Method
Pre-change baseline must be defined *before* the change goes live. It is:
- The 30 trading days immediately preceding the change, OR
- A matched-condition slice of the 4,274-trade backtest

You do not pick the comparison window after the fact. That's how systems get talked into looking better than they are.

---

## 5. ROLLBACK PROCEDURE

Rollback is not a failure. Rollback is the system working correctly. The cost of a rollback is much lower than the cost of letting a bad change compound.

### 5.1 Triggers
- Evaluation window ends and §4.2 rollback conditions are met
- Mid-window, if performance is catastrophically worse (e.g., -30% PF) — don't wait for the window to end
- Mid-window, if a critical bug is discovered in the change

### 5.2 Process
- Revert the specific code or configuration change
- Document in `outputs/change_log.md` (or equivalent): what was changed, when, evaluation results, why rolled back
- Note in advisor memory if it's something the advisor was using
- Wait minimum 7 trading days before proposing a related change (prevents reactionary tweaking)

### 5.3 What Rollback is NOT
- It is not an admission that the proposer was wrong
- It is not a reason to "try harder" on the same change immediately
- It is not optional once trigger conditions are met

---

## 6. PROPOSAL FORMAT (REQUIRED FOR EVERY CHANGE)

Every proposed change must arrive in this format. If a proposal doesn't have all five sections, it's not ready to be acted on.

```
PROPOSED CHANGE: [one-sentence description]

1. EVIDENCE
   - Tier: A / B / C
   - Sample size: [n trades or n days]
   - Effect size observed: [WR delta, PF delta, avg P&L delta]
   - Walk-forward validation: [pass/fail, with windows]
   - Out-of-sample held: [yes/no]

2. MECHANISM
   - Why should this work? [1-2 paragraphs, no hand-waving]

3. IMPLEMENTATION
   - Files affected: [list]
   - Parameters added: [count + names]
   - Risk: [what could go wrong]

4. EVALUATION PLAN
   - Pre-change baseline window: [dates]
   - Evaluation window: [trades or days]
   - Success thresholds: [specific numbers]
   - Rollback thresholds: [specific numbers]

5. SAFETY
   - Approvals required: [list]
   - SIM-only? [yes/no — should always be yes for now]
   - Reversibility: [easy/medium/hard]
```

---

## 7. ANTI-PATTERNS (THINGS THAT WILL NOT BE ACCEPTED)

These are the moves that will get push-back, every time:

- **"Let's just try it and see"** — without specifying success/failure criteria up front
- **"It worked yesterday"** — single-day results are noise, not evidence
- **"I have a feeling about this"** — feelings are not evidence
- **"The AI said it would help"** — AI claims must be backed by §2 evidence tiers
- **"Let's give it a chance"** — once rollback conditions are hit, the chance is over
- **"We can always roll back if it doesn't work"** — true but irrelevant; the proposal must still meet §6 standards
- **"This is what successful traders do"** — citing unnamed authorities doesn't qualify
- **"Let's add this and also that and also this third thing"** — one change at a time; bundled changes can't be evaluated
- **"The backtest says..." (without walk-forward)** — historical fit without out-of-sample validation is hindsight bias

---

## 8. WHAT THIS DOCUMENT IS NOT

- Not a guarantee AQ will improve. Discipline reduces the chance of getting worse; it doesn't manufacture edge.
- Not a substitute for judgment. These rules are minimums. Sometimes the right answer is "this passes the standards but I still don't like it" — and that's a valid reason to reject.
- Not permanent. This document should be revised when we learn the standards are too loose, too strict, or wrong. But revisions go through their own process — we don't lower the bar in the middle of evaluating something that's failing.

---

## 9. WHAT THE PLANNING CHAT (CLAUDE) COMMITS TO

When evaluating proposals or making recommendations:

- I will not propose changes that fail §2 evidence requirements
- I will push back when Rhett proposes something that fails §2
- I will state my confidence level honestly, including "I don't have enough evidence to recommend this"
- I will surface anti-patterns (§7) when I see them, including my own
- I will not soften feedback to be agreeable
- I will tell Rhett when I think a change he wants is a bad idea
- I will tell Rhett when I think the standards in this document are themselves wrong

---

## 10. APPROVAL

This document is in DRAFT until Rhett reviews and approves. Open questions for review:

1. Are the §3.2 effect size thresholds the right magnitude? (Too aggressive? Too lax?)
2. Are the §4.1 evaluation windows the right length?
3. Are there change types I missed in §1?
4. Is the §2.3 Tier C limit of 2 simultaneous changes the right number?
5. Anything in §7 that you disagree with?

Once approved, this becomes the locked standard and all future Claude Code work for AQ evaluation is built against it.

---

**END C1 DRAFT v1.0**
