# EOD DASHBOARD — UPDATE & VALIDATE (run at each EOD, after the 4:50 PM debrief)
*Standing routine (Rhett directive 2026-06-30). Goal: every surface of the advisor dashboard (127.0.0.1:8765) is up-to-date AND ties to broker truth before the day is closed out. Paste this to Claude Code at EOD, or it runs via the automated step below.*

## ROLE
You are Claude Code on the VPS. The dashboard is **on-demand** (Start_Dashboard.bat → `trade-review-ui`), so "up to date" means: when it's next opened, every page shows TODAY's accurate, broker-truth data. Most pages recompute live; a handful are **cached snapshots** that can silently go stale. Your job: prove the live pages tie to broker truth and refresh any stale cache — then say plainly whether it's clean.

## STEP 1 — RUN THE AUTOMATED VALIDATOR
```
C:\Users\Administrator\AppData\Local\Python\pythoncore-3.14-64\python.exe C:\AlphaQuant\tradestation-bot\validate_dashboard.py
```
It anchors on broker truth (`eod_debrief.round_trips_net` = the canonical day net every live page reads) and checks each cached surface exists + post-dates the last broker write. Read the PASS/WARN/FAIL table. NO-TRADE days auto-pass the cache checks.

## STEP 2 — FIX EACH WARN/FAIL (regenerate the stale cache, then re-run STEP 1)
- **daily_review_v2_narrative / daily_review_html stale or missing** → the 16:10 task didn't run or ran before the close:
  `cd C:\AlphaQuant\ai-trading-strategy-agent && python generate_daily_review.py`  (regenerates the cached LLM narrative + daily_review_latest.html for today)
- **shadow_results missing / no today rows** → the 16:50 shadow score didn't write:
  `cd C:\AlphaQuant\ai-trading-strategy-agent && python run_eod_shadow_score.py`  (or confirm the EodReconciliation task's 3rd action ran — check outputs\daily_review_gen.log / the task LastRunTime)
- **planning_roadmap stale (not today)** → the /planning page is showing an old roadmap. UPDATE `ai-trading-strategy-agent\outputs\planning_roadmap.json`: set `meta.last_updated` = today, refresh `meta.where_we_are` to the real current posture, and reconcile item statuses with what actually shipped (cite SESSION_LOG loops). Don't fabricate progress — mirror the log.
- **advisor_control stale** → the PostClose advisor (4:30) didn't write; re-run `run_advisor.py` or note the failure.

## STEP 3 — SPOT-CHECK LIVE PAGES vs BROKER TRUTH (the numbers, not just freshness)
The validator confirms the *source* reconciles; confirm the headline the human will SEE matches:
- The day's NET P&L on `/truth` and `/daily-review-v2` must equal the validator's `broker_truth_anchor` net (and the EOD debrief's net). If any page shows a different number → that page has a join/scope bug; investigate before declaring clean.
- `/system-validation` should show 0 FAIL rows; `/planning` should show today's date.

## STEP 4 — REPORT + LOG
Write one line to SESSION_LOG: `dashboard EOD validate <date>: VERDICT <PASS/WARN/FAIL>, <net> ties to broker truth, <fixed: …>`. If anything is still WARN/FAIL after STEP 2, say so plainly — never report the dashboard "clean" while a cached surface is stale.

## THE 5 CACHED SURFACES (the only ones that can silently go stale — from the 2026-06-30 dashboard map)
1. `/daily-review-v2` LLM narrative — `outputs/cache/daily_narratives/<day>.json` (16:10 task). **Highest risk: no built-in staleness warning** — this validator IS that warning.
2. `daily_review_latest.html` (16:10 task).
3. `/shadow-results` — `shadow_exit_results.jsonl` (16:50 run_eod_shadow_score.py).
4. `/daily-view` — 9:15 Market-View + 9:40 In-Play LLM snapshots (morning tasks; absent ⇒ "not generated yet").
5. `/trade-review` (legacy) — has its own stale_warning; rebuild with `?refresh=1`.
Everything else (/truth, /autopsy, /what-if-risk, /decision-quality, /system-validation, /system-timeline, /edge-tunes, /planning, /current-strategy) recomputes LIVE from `broker_orders_unified.csv` → `eod_debrief` and is current the moment the page loads — so the only dependency is that the 16:50 EodReconciliation ran (which writes the canonical broker-truth source).
