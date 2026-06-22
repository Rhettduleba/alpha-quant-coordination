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

## BUCKET B — SAFE-FIXABLE (non-watched, observability)  → ESCALATE WITH A PROPOSED FIX (do NOT auto-edit)
**During the OOS forward test, autonomous code-fixing is DEFERRED (Planning Track B, 2026-06-22).** Even a
"safe" auto-edit carries a real failure mode — e.g. an unattended agent loosening a check to suppress what
it THINKS is noise can BLIND the monitor to a real signal. So a human stays in the loop on every fix.
Class (for recognition): a CSHV/preflight/regression CHECK firing on a benign/expected state (Loop 131/136
false-WARN pattern); a stale display/report; a logging gap; a dead NON-trading helper that is safe to restart.
ACTION NOW: do NOT edit code. ESCALATE it to Rhett (Bucket C format) WITH the specific proposed fix, so a
human applies it (the noise then gets killed at SOURCE, human-in-loop, per A4). Auto-fix re-enables only
AFTER the forward test resolves, via a reviewed whitelist of safe, idempotent, non-trading actions.

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
- DURING THE FORWARD TEST: do NOT autonomously edit/commit ANY code (even non-watched). Escalate fixes
  with a proposal instead (Bucket B). Autonomous auto-fix is deferred (Planning Track B).
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
