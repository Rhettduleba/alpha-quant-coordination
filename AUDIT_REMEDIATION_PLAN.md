# ALPHA QUANT — AUDIT REMEDIATION PLAN ("make the next audit crystal clean")
Created 2026-06-30 by Claude Code, after the 9-section "does it actually work?" audit (`AUDIT_2026-06-30_DOES-IT-WORK.md`).

## DEFINITION OF DONE ("crystal clean")
Re-running the 9-section audit returns **all PASS**, and it returns all PASS **repeatably and on demand**, because:
1. Every FAIL/PARTIAL/gap below is fixed.
2. The audit itself is a **one-command harness** (no ad-hoc agent fan-out needed to re-run).
3. Each fixed bug has a **regression lock** (a test/drill case) so it can't silently come back.

## GUARDRAILS (unchanged)
- WATCHED trading files (risk_config, bot_loop, exit_bot_v2, candle_close_exit, advisor_filter_engine, symbol_universe, orb_runner, orb_multiscan, short_bot, mover_scanner): NO inline edits — each change is a proposal + Rhett's explicit go, applied then verified.
- Non-watched (monitoring/tests/tools/docs): fix now + validate.
- SIM stays SIM. Most fixes are INERT in SIM (they make the machinery correct for when guards are enabled for live); the two that change SIM trading behavior (sector cap, 4× universe) get extra care + a shadow-first option.

## THE BACKBONE (do FIRST — makes every later fix verifiable)
- **E1 — Repeatable audit harness `audit_does_it_work.py` (non-watched).** One command runs all 9 sections deterministically and prints a PASS/FAIL scorecard + evidence. Reuses regression_suite + reliability_drill + a single broker-truth pull (rate-safe). This is the "crystal clean next time" backbone — after each fix we re-run it.
- **E2 — Regression locks (non-watched).** A test per bug so it can't regress: daily-guard key-contract (B1), sector-cap-enforced-on-ORB (B3), every `*_MUST_SET_BEFORE_LIVE` flag has a consumer (B4/B7), drill case for alive-but-not-trading (B8).
- **E3 — Docs/SYSTEM_FACTS sync (non-watched + 1 watched-doc).** Reconcile CLAUDE.md control vocabulary (B7) + regen SYSTEM_FACTS after each watched change.

## BUG REMEDIATION TABLE (ordered by execution phase)
| ID | Bug | Sev | Watched? | Fix | Makes audit | SIM impact |
|----|-----|-----|----------|-----|-------------|------------|
| **B9** | 3 subprocess calls missing CREATE_NO_WINDOW (operator tools) | LOW | No | add `creationflags=CREATE_NO_WINDOW` at _preflight_diagnostic.py:57, orb_preflight_check.py:200/205/339, setup_autostart.py:33 | §7 lint clean | none |
| **B8** | New alive-but-not-trading detector not drill-tested | LOW | No | add a synthetic WARN case + clean companion to reliability_drill.py | §8 gap closed | none |
| **B1** | Dead daily-loss halt in live ORB path | **HIGH** | **Yes** (orb_runner) | orb_runner.py:364 → `if guard.get("should_trigger_shutdown", False):` | §4 (partial) | none (inert at $1e9) |
| **B4** | Before-live "hard gates" have no code consumer | MED | No (preflight) | add a startup/preflight assertion: a non-SIM account with any `*_MUST_SET_BEFORE_LIVE` flag True + its protection disabled → REFUSE/FAIL | §4 | none in SIM |
| **B6** | DD-kill base mismatch (vs SIM equity, not $400k base) | LOW | config/doc | decide + document/align the 5% kill base | §4 note | none (kill off) |
| **B3** | No sector cap on the live ORB path | MED | **Yes** (orb_runner/orb_multiscan) | wire MAX_SECTOR_POSITIONS into the ORB admit logic | §4/§1 | CHANGES SIM behavior → shadow-first option |
| **B5** | No real-time intraday loss clamp | MED | build + wiring | new monitor that halts/flattens on intraday realized-loss breach (not scan-time only) | §4 | inert in SIM (cap off) |
| **B2** | 4×-marginable universe not implemented | **HIGH** | **Yes** (symbol_universe) | derived 4× universe: criteria + maintained leveraged-ETF list + Special-Margin import; exclude BEFORE ranking | §2 | CHANGES SIM universe → shadow-first option |
| **B7** | CLAUDE.md control vocabulary stale (EXIT_PROFILE/VETO_CANDIDATE) | LOW | doc | document the 2 extra (conservative) control types or gate them | §3 note | none |

## EXECUTION ORDER (one at a time; re-run E1 harness after each)
1. **Phase 0 (now, non-watched, no approval):** B9 → B8 → E1 harness → E2 regression locks → B4 preflight assertion → B6 doc.
2. **Phase 1 (watched, 1-line, highest value):** B1 daily-guard — proposal + diff + Rhett's go → apply → verify with the B1 contract test + re-run §4.
3. **Phase 2 (watched, behavior — shadow-first):** B3 sector cap — proposal; decide enable-in-SIM vs shadow.
4. **Phase 3 (build):** B5 intraday clamp — design + new monitor + wiring proposal.
5. **Phase 4 (watched, biggest):** B2 4× universe — design + proposal; shadow-first.
6. **Phase 5:** B7 doc reconcile + SYSTEM_FACTS/CLAUDE.md sync; final full audit re-run → expect all PASS.

## ACCEPTANCE
After Phase 5: `python audit_does_it_work.py` → 9/9 PASS; §2 + §4 green; regression_suite + reliability_drill include the new locks; SYSTEM_FACTS current. That is "crystal clean," and re-provable any time.
