# PROP-LIVE-BP-AWARE-DEPLOY-2026-06-22  (Phase-3, BEFORE-LIVE — LOG ONLY, NOT BUILT)

**Status:** RECORDED for Phase-3 before-live execution-safety. **NO build, NO live-path change now** (mid-forward-test freeze). Source: Planning handoff 2026-06-22 ~5:35 PM (Rhett: capital cap is $400k; the bot must deploy toward full $400k without TradeStation hard-rejecting orders).

## CORRECTION TO THE RECORD
- The capital cap is **$400k** ($100k × 4 base buying power). **$300k is the CURRENT SIM deploy-target config (75% buffer), NOT the cap.** Intent for live: deploy toward the full $400k.

## THE GAP (before-live)
- `deploy_controller` sizes/admits against **STATIC constants** ($400k base / $300k target). It does NOT read **live available buying power** at order time. (Live equity/BP is currently read only for DD-kill / HWM, never for sizing.)
- **SIM hides it:** SIM raw BP ~$3.8M → never rejects regardless.
- **Live failure mode:** at ~$390k deployed (filled + working-order BP reservations), a new ~$20k admit exceeds available BP → TradeStation **HARD-REJECTS** the order. A static cap cannot see this.

## REQUIRED BEHAVIOR (Phase-3 before-live)
1. Admit/size against **REAL-TIME available buying power** pulled from TS at order time — not a static constant.
2. Account for **working-order BP reservations** (resting entries tie up BP pre-fill) + a slippage cushion, so the bot's ceiling sits just under broker-available BP.
3. Deploy up to the **full $400k** (raise the $300k target) — but ONLY via the live-BP gate above; never as a static $400k constant (that guarantees rejections).
4. On insufficient BP: gracefully **DOWN-SIZE or REFUSE with a reason code** — never submit an order the broker will reject (rejections = API-hygiene + execution-quality damage).

## VERIFICATION (when built, before-live)
- [ ] Simulate $390k deployed + working orders → next admit down-sizes/refuses, no TS reject.
- [ ] Available-BP read is point-in-time at admit (not cached stale) + counts working-order holds.
- [ ] Full-$400k deployment reachable when BP allows (target raise works).
- [ ] Bot BP model vs broker-reported available BP reconciles across a SIM day (no divergence).

## RELATED — already answered (Day-1 read, 2026-06-22)
- "Was the $312k peak a real cap leak or MTM drift?" → **BENIGN (V3 closed).** Cumulative ADMITTED entry-notional was **$197,318** (re-arm; controller governed each admit vs cap); the $312k book = 5 positions + 12 **working (unfilled)** stop-entry orders + MTM. Not a cap leak. BUT it IS live evidence the control drifts past its own target by counting working orders + MTM — the same imprecision against a HARD $400k wall is exactly how a live rejection happens. Reinforces the need for the live-BP gate above.
- Ties into the Phase-3 execution-safety bucket (emergency-exit/cancel-on-disconnect, idempotency, restart-in-SAFE_MODE, daily-loss real-time clamp).

**Watched files when eventually built:** orb_runner.py / orb_multiscan.py / deploy_controller — strategy surface → full proposal + manual_approvals + Rhett approval required at build time. Gated until after the forward test resolves.
