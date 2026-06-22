# CODE ALERT TRIAGE PLAYBOOK
**For the scheduled autonomous Claude Code triage agent (Loop 137, Rhett-approved 2026-06-22).**
Goal: Rhett no longer monitors Discord. Code receives the same alerts (via the mirror) and, on a
schedule, AUTO-HANDLES the noise + first-line-fixes the safe class, and ESCALATES anything with real
risk back to Rhett — pre-diagnosed. The human gate is preserved.

## ON EACH RUN (do exactly this, in order)
1. `git -C C:\repos\alpha-quant-coordination pull` ; read the top of `C:\AlphaQuant\SESSION_LOG.md`
   (stamp) + `C:\AlphaQuant\CSHV_FINDINGS.md`. Know current state before acting.
2. `python C:\AlphaQuant\tradestation-bot\code_alert_inbox.py --json` → the NEW alerts since last ack.
3. For EACH actionable alert, classify into exactly one bucket (below) and act.
4. ALWAYS at the end: append a short dated entry to SESSION_LOG.md (what fired, what you did / escalated),
   sync to the coordination repo, and `code_alert_inbox.py --ack` to advance the cursor.

## BUCKET A — KNOWN-NOISE  → ack, no action
Already-understood benign/expected states (the reader pre-tags many via KNOWN_NOISE). Examples:
- advisor_filter idle with 0 active controls; brain_universe "built today"; transient broker-5xx ignored;
  deadman states already armed; any check we have already confirmed benign in SESSION_LOG.
Action: nothing. They are informational. (If one recurs noisily, consider Bucket B.)

## BUCKET B — AUTO-FIXABLE (non-watched, observability only)  → fix with full discipline, then ack
ONLY this narrow class may be auto-fixed without Rhett:
- A CSHV/preflight/regression CHECK firing on a benign/expected state (a false-WARN/FAIL in a NON-watched
  check file) — refine the check to be context-aware (the Loop 131/136 pattern).
- A stale DISPLAY/dashboard artifact, a read-only report, or a logging gap (non-trading).
- A dead NON-TRADING helper process that is clearly safe to (re)start (e.g., the dashboard, a scheduled
  reporting task) — restart it the same supervised way and verify.
Discipline for any fix: verify the root cause against real data → make the minimal change → test/compile →
`git add` + commit + sync → log to SESSION_LOG. NEVER skip verification.

## BUCKET C — ESCALATE TO RHETT (do NOT touch)  → notify + log + ack
Escalate (notifier.send_notification level CRITICAL, subject "CODE TRIAGE — needs you", body = plain-English
diagnosis + the specific proposed fix) for ANY of:
- Anything touching a WATCHED strategy file (risk_config, bot_loop, exit_bot_v2, candle_close_exit,
  advisor_filter_engine, symbol_universe, orb_runner, orb_multiscan, short_bot) or sizing/universe/stops.
- Positions/orders: naked position, position-recon mismatch that persists >2 cycles, an unprotected
  position, an order-rejection burst that is NOT the known weekend class, daily-loss / drawdown / kill events.
- Auth/token failures that persist (a single transient 5xx is Bucket A); account/broker connectivity down.
- SAFE_MODE engaged/stuck; bot crash-loop; supervisor/guardian down; EOD-flatten failure.
- ANYTHING novel, ambiguous, or that you are not highly confident is benign. **When in doubt, ESCALATE.**

## HARD RULES (never, under any circumstance, autonomously)
- NEVER edit a WATCHED strategy file; NEVER change risk/sizing/universe/stops/time-windows.
- NEVER place, cancel, or modify any order; NEVER touch positions.
- NEVER deploy a strategy change (those need a proposal + manual_approvals + Rhett).
- NEVER restart run_bot / watchdog_supervisor unless there is a clear, verified, safe reason AND it is
  the documented supervised method; prefer to ESCALATE.
- NEVER refresh TS tokens excessively; NEVER touch credentials/.env.
- If a fix is not OBVIOUSLY safe + reversible + non-watched → ESCALATE, do not act.

## ESCALATION FORMAT (what Rhett gets, only when Code can't safely handle it)
One CRITICAL notification: WHAT fired, WHY it matters, Code's diagnosis, the proposed fix, and whether it
needs his approval (watched) or just his go-ahead. Plus a one-line SESSION_LOG entry. Everything Code DID
auto-handle is logged but does NOT ping Rhett (that is the whole point — silence = handled).
