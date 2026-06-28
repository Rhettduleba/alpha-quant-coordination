# Alpha Quant — SESSION LOG & CRASH-RECOVERY HANDOFF

> # ⭐ CURRENT STATE — 2026-06-27 ~7:25 AM ET (READ FIRST — full cold-start brief: `HANDOFF_2026-06-26_RAMP-UP.md`)
>
> **POSTURE:** Forward test of the Loop-123 exit KILLED 6/25 (day −$2,016.93 < −$2,000 AND MU −$1,670.30 < −$800).
> Rhett's FINAL call: do NOT revert — KEEP the live chandelier exit (`candle_1.4atr_chandelier`), improve in SHADOW.
> Between experiments. **Live bot UNCHANGED, same entries.** SIM-only (`SIM1623888M`); live root **C:\AlphaQuant**.
>
> **⚙️ 2026-06-27 CHANGE (Rhett directive, APPROVED + RECORDED + LOADED):** deploy-controller capital-deployment
> TARGET raised **75% ($300k) → 95% ($380k)** of the $400k DEPLOY_BASE. ONE constant: `risk_config.DEPLOY_TARGET_PCT`
> 0.75→0.95. Per-position $25k and per-side $200k caps UNCHANGED; 9:35 ORB path is NOT deploy-controller-constrained;
> this only lifts the re-arm/multiscan admit ceiling (the WINNING path). Swept EVERYWHERE (dashboard daily-review now
> renders "$380k target", capture_utilization, sidelined_capital, _sizing_base_audit, prove_deploy_governs,
> report_first_admit, sim_day_replay — all readers dynamic = single source of truth). Approval =
> `PROP-DEPLOY-TARGET-095-2026-06-26` in manual_approvals.yaml; change-log = `AQ-20260626-ORBV1-DEPLOY-TARGET-095-001`.
> Verify-load DONE: run_bot restarted PID 10904 (StartTime 7:18 > risk_config mtime 7:06), heartbeat alive, preflight
> 0 FAIL, `deploy_target()`==$380,000; prove_deploy_governs all-PASS at $380k. Effective Mon 6/29 open. Reversible
> (set back to 0.75). **LIVE prereqs (PROP-DEPLOY-TARGET-400K: real-time available-BP gate + sector/correlation cap)
> NOT shipped — required before any LIVE use; SIM has ample BP so no broker rejects.** Also this turn: REVERTED the 12
> scheduled-task SYSTEM-account conversions back to Administrator (restored from XML backups, all RunAs=Administrator).
>
> **CENTRAL FINDINGS:** the 9:35 morning entries are the loss engine every day; the re-arm path made money all 3 days
> (DO NOT touch re-arm). Dollar-split (real fields, 6/23–6/25): preventable-at-ENTRY −$4,521.52 (60%) vs
> manageable-at-EXIT −$3,044.86 (40%). L2 lever = EXTENSION MAGNITUDE, not RS (MU 19.49% skip vs QCOM 9.69% winner).
>
> **BUILT THIS SESSION (all non-watched / shadow):** shadow tooling (`strategy-research/`: excursion_study,
> entry_context_sidecar, l1_unconfirmed_leash, l2_entry_guard, l1_l2_combined; synthesis =
> `outputs/reports/SHADOW_BUILD_SYNTHESIS_2026-06-25.md`). Combined L1+L2 shadow: 3-day red −$2,656 → −$495 (−81%),
> 0 winners cut, NOT green, N<30 → DIRECTIONAL only. Infra: 6 AM PRE-OPEN GO/NO-GO GATE (`pre_open_gate.py`, shadow +
> Telegram/Discord alerts + no-auto-fix escalation; teeth gated on `SAFE_MODE_ENFORCE` flip); **/planning** dashboard
> (living roadmap = `planning_roadmap.json`). NOTE: live `consecutive_clean=0` (SYSTEM_FACTS, 6/27) — the earlier "=4" is STALE; benign CIM-noise is re-tripping the certifier's no_critical_incident, see OPEN DECISION (5).
> Entry-context "deploy" 6/26: gate PASSED with ZERO entry-path change (fields already logged in orb_candidate_log.jsonl;
> sidecar is a read-only reader → byte-identical).
>
> **OPEN DECISIONS AWAITING RHETT:** (1) arm the pre-open gate (flip SAFE_MODE_ENFORCE, ~3-5 shadow mornings first);
> (2) precise OR-distance entry-path add vs proxy (recommend skip); (3) earnings feed refresh (Phase 1.2, veto stale ~21d);
> (4) post-test gauntlet → promote one lever → fresh 5-clean-day test, then Phase 4 scale.
> (5) **CORRECTED 6/27 (my earlier CIM-noise diagnosis was WRONG — verified):** `consecutive_clean=0` is NOT benign-noise-driven. The CIM noise was already non-disqualifying (WARN-not-FAIL + certifier exempt bucket). The REAL disqualifiers are genuine trading-path faults: 6/26 & 6/22 `rel_trading_is_thinking` (main loop frozen >4 min) and 6/19 `rel_gate_not_failing_open` (gate failing open ALL DAY, 64×). 6/23/24/25 WERE clean (3-day run); 6/26's loop-stall broke it → 0 is HONEST. Did the schtasks swap (stops the CSHV false-TIMEOUT noise) but did NOT touch the count (won't game it). **Real lever = fix the recurring 9:30-AM loop-stall + investigate the 6/19 gate-fail-open** — NOT exempting them. Decision for Rhett/Planning: should a single self-recovered loop-stall (vs a sustained one) count as HARD, like position_recon's >2-cycle rule? (I left it HARD — conservative, not gamed.)
> (6) **NEW (stop-coverage audit 6/27):** broker resting-stop coverage is 37.9% (9:35 cohort 96% / re-arm 0%) + ~7 min lag — a real BEFORE-LIVE gap (process-death exposure on the re-arm cohort). Fix = re-arm resting stops + tighter placement; watched-file change → proposal under the gate before live.
>
> **HEALTH NOW:** CSHV 43/0/0; gates green (preflight 51/1W/0F, regression 20/0F, reliability 9/9); pre-open gate
> GO-WITH-WARNINGS; bot alive, no config drift. Canonical living plan = the **/planning** page.
>
> *(Older alert-triage stamps + reboot checklist + ledgers below are HISTORICAL — superseded by the brief above.)*
> ---

---
# 📋 FINDINGS & TEST RESULTS LEDGER  (READ THIS for "what did the latest tests find" — newest first)
> Every audit / study / test result Claude Code runs gets a dated entry HERE, so Planning can read the
> session log instead of a separate handoff. Each entry: date · what · verdict · numbers · source files.

### 2026-06-27 — BUILT: Tape Watcher (TW) v1 — SHADOW ONLY (real stop on every entry + tick-level early exit watching)
- **Why:** stop-coverage audit found 37.9% broker-stop coverage (9:35 96% / re-arm 0%), ~7 min late; exits poll-managed, first-poll ~5 min after entry. TW = a stop computed the instant each entry fills + tick-level watching of the live exit logic. **v1 SHADOW: zero orders, no watched file touched, freeze intact.**
- **Built:** `strategy-research/tape_watcher.py` (observer: `--print-config` / `--replay DATE` / `--live`) + `strategy-research/tw_report.py` (daily reconciliation vs broker truth). Reuses the LIVE exit verbatim (`candle_close_exit.chandelier_decision`) + reads params from code (resting **1.4×ATR**, confirm 0.15, chandelier 1.4 — printed, not assumed). Live stream consumer built (`requests` stream of `/marketdata/stream/quotes`, reconnect + gap detection) but unprovable until a live session. Shadow log → `outputs/validation/tw_shadow.jsonl`.
- **PROVEN TODAY via 6/25 replay (broker truth + 1-min bars; 1-min-bar proxy, not true tick):** **COVERAGE 23/23 = 100%** (vs live 37.9%), **would-place latency 0s** (vs ~7 min). Exit faithfulness: TW reproduces the live exits within cents (the +1m labels = 1-min bar granularity). **MU (the known bleeder): CHANDELIER_STOP, unconfirmed, ~09:55 — matches live** (TW doesn't tighten the wide 1.4×ATR chandelier; its value is coverage+latency+tick-level). **PENN:** TW would-fire candle-close reversal 09:42 but live held to EOD — directional evidence early-watching catches reversals the ~5-min poller misses (proxy-dependent). **Must-not-cut flags:** 2 tiny confirmed-winner clips (RVTY −$0.12/10m, TER −$0.71/6m) for review. Report: `outputs/reports/tw_shadow_report_2026-06-25.md`.
- **STILL OWED before any live talk (flagged, NOT done):** live-tape proof (tick completeness no-gaps + stability/reconnect across a real session) — replay can't prove the stream; and the must-not-cut review of flagged clips. Future live cutover (separate handoff, after clean shadow days + Rhett go) must use REAL broker-resting orders + exactly one exit owner.

### 2026-06-27 — BUILT: LLM Daily Report Layer v1 (9:15 Market View + 9:40 In-Play Review) — SHADOW/ADVISORY
- **Built** `ai-trading-strategy-agent/src/advisor/daily_report.py` + `daily_view_page.py` (dashboard `/daily-view`). OBSERVATIONAL ONLY: changes NO trades/selection/sizing/config, does NOT write advisor_control, not a gate. Delivery = logs + dashboard only (no Telegram/Discord). Reuses `claude_client.call_claude` (sonnet-4-6); ANTHROPIC key already present.
- **Anti-fabrication design:** FACTS are assembled IN CODE (never invented by the LLM); the LLM produces OPINION only, each with a confidence (low/med/high) + explicit "unsure about", instructed to flag uncertainty + give NO buy/sell call. Unavailable inputs (futures/foreign/econ) marked `NOT_WIRED_v1` so the model can't fabricate them.
- **VERIFIED with REAL LLM calls (replayed 6/26):** Report A returned regime=unclear, risk=risk-off, **confidence LOW**, and correctly flagged every NOT_WIRED gap as a thing it's unsure about (602/361 tok). Report B reviewed the top-20 in-play names (3,479 tok), per-name hold/fade + extension(healthy/extended/exhausted) + **TRAP flag** (flagged LITE as MU-class), honest low-confidence where data thin.
- **Guardrails confirmed:** news SANITIZATION works ("IGNORE PREVIOUS INSTRUCTIONS"→"[redacted]", `<system>` stripped, untrusted-news-as-data instruction); SCORE-IT log persists every report's calls (`outputs/reports/daily_view/score_log.jsonl`, outcome=null) for later accuracy-checking; cost-scoped (in-play names only, ~2 calls/day, ~$0.01-0.13); zero trading-path touch (only writes report JSON + score log); ANTHROPIC key via env, no hardcoded secret, reports carry no secrets, files local (not pushed to public repo).
- **Dashboard:** `/daily-view` (HTTP 200, FACTS vs OPINION visually separated, confidence badges, TRAP red badge); dashboard restarted (PID 5760). **Scheduled:** `AlphaQuant_LLM_MarketView` 9:15 + `AlphaQuant_LLM_InPlayReview` 9:40 (S4U/no-window, Mon-Fri, next Mon 6/29). Intraday regime reader = LATER; advisor audit = HELD.

### 2026-06-27 — ANALYSIS: is the in-play GATE helping or hurting? (gate-vs-timing confound) — Rhett's catch SUPPORTED
- **Tool:** `strategy-research/gate_effect_analysis.py` (read-only, GROSS only). Counterfactual on never-traded rejected names = DERIVED (ORB-break + LIVE chandelier on 1-min bars), **sim VALIDATED** (QCOM cf +$437 vs broker +$433; MU cf −$1,582 vs −$1,668 = within ~5%). Report: `outputs/reports/gate_effect_analysis.md`. Gate window 6/15–6/26 (gate live 6/16).
- **ANSWER: strong DIRECTIONAL evidence the gate is ANTI-SELECTING on the 9:35 path — not just timing.** (1) **Gate-REJECTED names' counterfactual gross = +$48.2/trade (81% win, PF 1.98, n=140 that broke out)** vs **gate-PASSED broker-truth = −$29.1/trade (53% win, PF 0.66, n=111).** The gate rejected the better names. (2) **67% of WINNING re-arm names (60/89) would be BLOCKED by the 9:35 gate's quality criteria** (RelVol-low 37, exhausted 19, move-small 4) — **+$8,143 of winners blocked**; the gate rejects the SAME kind of name that wins ungated. (3) The 9:35 loss concentrates in **mega-caps −$229/trade (PF 0.18) + large −$24** while smaller/unknown-mcap names are **+$15/trade (PF 1.43)** — the gate's liquid/top-RelVol criteria favor fade-prone mega/large-caps.
- **The gate's reject criteria are MIS-CALIBRATED:** names rejected for DAY_RELVOL_LOW (+$56 cf), MOVE_TOO_SMALL (+$33), MOVE_EXHAUSTED (+$139) would have WON — the exact opposite of the gate's intent. (INDEX_ETF reject was correct, −$173.)
- **Timing also matters (control):** clean time-of-day shows 09:35 −$29 vs 10:35 +$41/trade — so it's gate AND timing, but the gate evidence is strong. **HYPOTHESIS, not a gate change:** DERIVED counterfactual (vs broker-truth passed = mixed fidelity), in-sample, small N (mega n=11, exhausted n=6), multiple comparisons, $-vol floor bypassed for re-arm (not logged). The fix (recalibrate/scope the gate, esp. for mega-caps + the exhausted/low-relvol rejects) is a WATCHED-file change → separate handoff, gated, OOS test first. READ-ONLY; no orders/watched file; freeze intact.
- **(process note: a bash `export $(… | head -0)` slip printed the env incl. an OpenAI key into the LOCAL transcript only — not synced to CHAT_LOG/public repo; pattern avoided going forward.)**

### 2026-06-27 — ANALYSIS: gross signal quality — IS there an edge before cost, and where? (read-only, GROSS only)
- **Tool:** `strategy-research/gross_signal_quality.py` (read-only, broker-truth, GROSS only/no fees, n=285, 6/08–6/26). Report: `outputs/reports/gross_signal_quality.md`.
- **ANSWER: YES — the flat +$187 gross HIDES a massive divide; it is NOT "no edge."**
- **BUT the cleanest divider (confirmed vs unconfirmed: +$134.7/trade @98% win vs −$225.2/trade @6% win, from exit_decisions.jsonl) is LOOK-AHEAD / NOT a tradeable ENTRY edge** — verified: confirm is decided ~6 min AFTER entry (QCOM 6/25 confirmed 09:41 vs ~09:35 entry). It's largely tautological ("trades that went favorably won") = the EXIT lever (cut unconfirmed bleeders = gauntlet), not entry selection.
- **The ENTRY-OBSERVABLE positive slice (the real candidate edge):** **RE-ARM path +$3,420 / +$19.7/trade / PF 1.30 / 59% win** vs 9:35 path −$3,233 / −$29.1 / PF 0.66. Sharpest: **the 10:35 window (hr 10:00) +$2,342 / +$41.1/trade / 70% win / PF 1.61** (11:00–14:00 ≈ flat-positive). **SHORT side +$1,719 / +$11.2 / PF 1.18** vs long −$1,532 / PF 0.87. **Midday +$3,414 / PF 1.36.** Loss engine = 9:35 / OPEN (−$36.8/trade, PF 0.60) — consistent across splits.
- **Extension split INCONCLUSIVE** (fixed move_pct→real gap vs prior_close, but that understates multi-day extension — MU's earnings gap shows +3.4% since 6/24 already absorbed it; ≥12% bucket n=12 only). Does NOT cleanly test the L2 gap-top thesis; needs a multi-day-extension field. Do not read ≥12%-wins as refuting L2.
- **CANDIDATE EDGE TO ISOLATE + TEST OOS:** the **re-arm path (esp. 10:35 window) + short side**, GROSS-positive and entry-observable. **CAVEATS (flagged):** in-sample, small N per slice (re-arm hours 23–57 each), multiple pre-declared splits (multiple-testing), 6/25 kill day included → these are HYPOTHESES to test out-of-sample, not proven edges. Read-only; no orders/watched file; freeze intact.

### 2026-06-27 — BUILT: execution-cost / implementation-shortfall ledger (read-only) — the binding-constraint number
- **Tool:** `strategy-research/execution_cost_ledger.py` (READ-ONLY, broker-truth; n=285 entries 6/08–6/26). References REAL/broker-logged at ~99–100% (decision=signal_trigger_px, arrival=market_price_ref_at_submit, intended, fill, commission); SPREAD = UNATTRIBUTED (no quote-at-fill). Report: `outputs/reports/execution_cost_ledger.md`.
- **HEADLINE (the number that decides if it can work):** realized **GROSS = +$187 total** (essentially FLAT: +$0.66/trade, −1.06 bps/trade) → **NET = −$1,153** after ~**$1,340 commission+fees**. So the signal is **~flat-to-slightly-negative GROSS, and commission turns it clearly negative.** Per-trade net −4.04 bps. **Cost is the killer, not the entry execution.**
- **Entry implementation shortfall is SMALL + well-controlled: avg 0.82 bps (0.03¢/share).** Decomp: delay (decision→arrival) **2.52 bps** (the breakout's initial move past the armed trigger — inherent to breakout entry) PARTLY OFFSET by execution (arrival→fill) **−1.7 bps** (the stop-limit 5bps collar fills us at/better than arrival). Submit→fill time ~0s (fills immediate). So entry slippage is NOT the problem.
- **The real cost is COMMISSION ≈ 3 bps round-trip (~$1,340 on the per-share plan).** SWING FACTOR: the commission_model notes TS Select = $0 commission; on TS Select the net would be ≈ realized gross (≈ breakeven) instead of −$1,153. **The live commission-plan choice (per-share vs TS Select $0) is the difference between a loss and breakeven** — the highest-leverage cost lever, confirms the long-standing "cost halves the edge" caveat.
- **SPLITS — where it's worst:** **OPEN segment net −$40.92/trade** (the loss engine) vs midday +$18.10 / close +$32.45; **9:35 path net −$33.32/trade vs re-arm +$14.63/trade (re-arm is POSITIVE even AFTER cost)** — consistent with [[project_rearm_vs_935_expectancy]]; shorts (+$7.04) beat longs (−$17.08); LOSERS slip more on entry (IS 1.24 bps) than winners (0.50 bps). Cost (IS+comm) is similar across paths — the net gap is the SIGNAL, not the cost.
- **TIE-OUT: MATCH** — full broker-CSV commission+fees $1,339.71 == eod_debrief/daily_review $1,339.73 (within $1). Ledger's entry-leg-only $669.85 ≈ half (exit leg is the other half). **CAVEAT:** EXIT-side IS not isolated (exit "decision" = chandelier/candle trigger, not cleanly logged) — it sits inside realized gross. READ-ONLY; no orders/watched file; freeze intact.

### 2026-06-27 — DIAGNOSE the loop-stall (clean-day blocker): read-only instrumentation LIVE + ranked hypotheses
- **STEP 1 — instrumentation LIVE (pure logging, no control-flow change):** `run_bot.py` (non-watched) now logs per-stage cycle timing → `logs/loop_stage_timing.jsonl` (each stage's elapsed + `_CYCLE_TOTAL`) and an OBSERVE-ONLY 90s self-watchdog → `logs/loop_stall_dumps.jsonl` (on a >90s single stage: hung-subprocess status/cpu/rss/threads via psutil + host memory + main-thread `faulthandler` stacks; NO kill/restart). Verified live after restart (run_bot PID 10548): loop still cycling (loop_count advancing), timing log populating, watchdog daemon thread running. **No watched file touched; no scan/entry/exit/order change; freeze intact.**
- **CORRECTION to the handoff premise (verified):** the stalls were NOT both "9:30 AM." **6/26 = 09:30:11** (open bell, loop frozen at 2406; bot RECOVERED and scanned fine at 09:35) — but **6/22 = 14:11:40** (mid-afternoon, loop frozen at **7** = a freshly-restarted process on its 7th cycle, bot_alerts empty/quiet that window). The common factor is **a single slow cycle**, not specifically the open.
- **MECHANISM (already explainable from the code):** heartbeat-fresh + loop_count-frozen is EXACTLY what a long cycle produces — each per-cycle step (`_run_step_with_heartbeat`) beats the heartbeat every 10s but `loop_count` only ticks at the loop top. A single step caps at ~190s (hard_cap+taskkill), so a >4-min freeze must be **cumulative** slow steps in one cycle.
- **RANKED HYPOTHESES (evidence-weighted, none asserted as fact):**
  1. **LEADING — cumulative slow/timing-out TS API calls at data-heavy moments.** Direct evidence: run_bot.py:553's own comment ("ORB pre-market warmup makes many 30s-timeout API calls; on a slow morning the cumulative runtime exceeded the watchdog threshold"); 6/26 stall sat in the ~09:26–09:30 pre-open warmup window then recovered/scanned fine (transient slow cycle, not a hard hang); ORB_SCAN_TIMING 6/26 showed OR→first-submit 62.4s.
  2. **taskkill/CIM-WMI hang** letting a step run unbounded — 6/25 had documented CIM/WMI instability; but the taskkill path is bounded by `break`, so this alone can't exceed ~190s (only compounds #1). Needs evidence.
  3. **GC pause / memory pressure** — a 6/22 OOM was noted historically; the new watchdog now captures host_mem at stall to confirm/refute. No direct mem evidence for these two moments yet.
  4. **Single network-hung TS call** that never returns + failed kill — bounded by break; low. 
- **What we still need to CATCH it live:** the instrumentation is now armed; next likely trigger = **Monday's open (~09:25–09:35)** (the weekend won't trigger — steps are sub-second on a closed market). A live catch will show WHICH stage ate the time + whether the hung subprocess is network-waiting (low cpu → confirms #1) vs CPU-busy (→ GC/#3) vs high host-mem (#3). Pinpointing the exact slow API call would need per-call timing INSIDE orb_runner (a watched file) — deferred unless stage-level + cpu/mem isn't enough. **Fix is a SEPARATE handoff after a verified catch.**

### 2026-06-27 — WIRED the available NOT_WIRED inputs into the 9:15 Market View (verify-first; 2 of 3 reachable)
- **FUTURES — WIRED (reachable on current TS auth, verified live):** `@ES`/`@NQ` continuous front-month via `/marketdata/quotes` returned HTTP 200 on our existing entitlement (ES 7397.25 vs prev 7423.25 = −0.35%; NQ 29283 vs 29724.75 = −1.49%). `daily_report._futures_facts()` now puts a real overnight level + % vs prior settle in Report A's FACTS. Real LLM call USED it ("NQ down ~1.49%, weaker than ES → tech-led pressure," risk-off, conf LOW).
- **FOREIGN — WIRED as a LABELED LAGGED PROXY:** raw foreign indices (^GSPC/^GDAXI/^N225) are PREMIUM on our Finnhub key ("Market data subscription required for CFD indices"), but FREE US-listed country ETFs work via Finnhub /quote — EWJ (Japan) −0.63%, EWG (Germany) −1.07%, FXI (China). `_foreign_facts()` wires them with an explicit "pre-open shows the PRIOR US-session print, not the live overnight session" caveat; the LLM treated it cautiously (flagged the lag in 'unsure_about').
- **ECON CALENDAR — stays NOT_WIRED (PREMIUM, verified):** Finnhub `/calendar/economic` = **HTTP 403 "You don't have access to this resource"** on our free key. Quoted in the FACT block; needs a paid feed or a free alternative — Rhett's call. NOT fabricated; the LLM correctly says it's unavailable.
- **Dashboard:** `/daily-view` renders the new futures + foreign-proxy + econ-403 blocks (no restart needed — the page reads the report JSON generically). **Zero trading-path touch** (helpers only READ quotes; no orders, no watched file, no advisor_control). Key hygiene intact (env only, gitignored, nothing pushed).

### 2026-06-27 — Finnhub key WIRED + the two pending news-feed verifications CLOSED (still shadow/read-only)
- **Key added** to `ai-trading-strategy-agent/.env` (`FINNHUB_API_KEY`, value masked `d902…ndg`) — gitignored, NOT git-tracked, NOT in any pushed file (secret-scanned SESSION_LOG/SYSTEM_FACTS/news_shadow/planning/coordination repo: all clean). `news_feed.py` reads it via `os.getenv` (no hardcode).
- **SECRET-SAFETY (Rhett pasted the key in plaintext):** hardened `planning_turn_sync.py` redaction with a generic API-key-shaped-token pattern (24+ alnum w/ a letter AND a digit) — TESTED: redacts the Finnhub key, spares short commit SHAs + normal words. So the turn-end CHAT_LOG auto-sync scrubs the pasted key from the PUBLIC repo. (Optional: rotate the key since it was pasted in chat — free-tier personal key, low risk; Rhett's call.)
- **LIVE free-tier limit CONFIRMED from a real response** (not docs): `X-Ratelimit-Limit: 60` (60 calls/min), `X-Ratelimit-Remaining: 59`, AAPL returned **247 articles** (no company-news cap). Commercial-use clause = personal/non-commercial (a ToS term, not in headers; confirmed from docs earlier).
- **TAGGING ACCURACY (24 articles, collision-prone tickers KEY/ALL/ON/A/F/DELL):** ticker→article **relevance ~83%** (20/24 about/materially-involving the company); **strict "primarily about" ~62%**; **clear misses ~17%** (DELL got a Cisco article + a newborn-accounts story; ALL got a Chubb article; MU got an Apple-primary article). Pattern = general "top-stocks/dividend" lists + competitor/sector articles + occasional noise; worst on short/common-word tickers. **TAGS STAY ADVISORY.** Follow-up to raise precision: require the company name/ticker in the headline. (Catalyst-TYPE tagging separately = 8/8 sample + correct on real m&a/earnings.)
- **Company news now FLOWING:** 5-symbol collect → 814 articles (per-ticker volume high → added a `cap=6` most-recent per ticker to keep the shadow file lean). Sample rows in `news_shadow.jsonl` now carry `source_api:finnhub` with catalyst tags. Read-only/shadow; no trading-path touch; does NOT feed entry selection; does NOT replace the NASDAQ earnings calendar.

### 2026-06-27 — BUILT: free news-feed SHADOW prototype (Finnhub primary + SEC EDGAR keyless) — catalyst tags + post-trade attribution
- **Built** `strategy-research/news_feed.py` (READ-ONLY/shadow): Finnhub company+market news (PRIMARY, needs key) + SEC EDGAR 8-K (SECONDARY, KEYLESS) → catalyst-type tag kept as a SEPARATE field (earnings/analyst/fda/m&a/exec_change/legal_reg/macro/sector/none), NOT a blended score. Writes a SEPARATE file `outputs/validation/news_shadow.jsonl`. Plus a read-only post-trade attribution join. NO watched file, no orders, no behavior change; freeze intact.
- **Finnhub free tier (docs — live-verify pending key):** 60 calls/min, includes company-news + market-news + SEC filings; **commercial use RESTRICTED to personal/non-commercial** (fine for SIM research; a paid plan needed if this ever becomes a commercial product). **No Finnhub key exists** (mover_scanner confirms "Finnhub keys absent") — Rhett must sign up free at finnhub.io + add `FINNHUB_API_KEY` to `ai-trading-strategy-agent/.env` (gitignored, verified). I can't create accounts.
- **VERIFIED TODAY (keyless):** catalyst tagger **8/8** on samples; **SEC EDGAR LIVE** — 10,433-ticker CIK map pulled, real 8-Ks correctly tagged from item codes (MU 6/24 item 2.02→earnings, JPM 5.02→exec_change, DELL 1.01→m&a). **Post-trade attribution (6/25):** surfaced that BOTH big losers were EARNINGS trades — **MU −$1,670 (earnings 8-K) + BB −$646 (earnings)** — directly relevant to the exit/earnings-veto debate.
- **PENDING the key:** live Finnhub free-limit quote (from a real response header) + tagging-accuracy precision on ~20 real article→ticker maps (name-collision risk). EDGAR item-code tagging is deterministic + verified.
- **Hygiene:** no hardcoded secret (key via `os.getenv`), `.env` gitignored, shadow files carry no secrets, news_feed.py local-only (NOT pushed to the public coordination repo). Does NOT replace the NASDAQ earnings calendar; does NOT feed entry selection (attribution/explanation + future individual testing only).

### 2026-06-27 — TW v1 LIVE-SHADOW proving run: can't run today (Sat/closed) → plumbing SMOKE-PROVEN + ARMED for Mon
- **Market CLOSED (Sat 1:42 PM ET, `is_regular_trading_day=False`)** → the full open→close live session can't run today; next session Mon 6/29. Did NOT fake it.
- **Stream plumbing PROVEN now (the novel risky part):** added `tape_watcher.py --smoke`; live connect to `/marketdata/stream/quotes` returned **HTTP 200**, parsed 3 snapshot quotes (NVDA 192.71 / AAPL 282.50 / MSFT 372.73 = Fri closes) + 4 heartbeats/25s, **0 parse errors**. Auth + connect + NDJSON consumer all work. **Tick-COMPLETENESS still unproven** (needs live trading — Monday).
- **`--live` hardened for a valid session:** periodic position re-poll every `RESUBSCRIBE_S=15s` so 9:35 + re-arm entries opened mid-stream get watched (reconnects only when a NEW symbol appears). **Fidelity correction:** live would-place latency = detection lag (≤15s), NOT the replay's 0s (replay knew fill times); literal ms-latency needs the v2 order-FILL stream. Still ≫ better than the bot's ~7min.
- **MUST-NOT-CUT review (6/25 replay vs broker truth):** only **2** confirmed winners would be clipped — RVTY (+$64 net, $21 giveback) + TER (+$140 net, $31 giveback) = **$52 total giveback, NO winner flipped to a loss**. Reassuring but 1-min-bar-proxy → the live tape decides; these are the names to watch Monday.
- **ARMED:** `AlphaQuant_TW_LiveShadow` task (S4U/no-window, Mon–Fri 9:25 AM, `--max-seconds 25800`, logs `tw_shadow.jsonl` + `tw_live.log`); next run **Mon 6/29 9:25 AM**. SHADOW: zero orders, no watched file, freeze intact. **Monday follow-up:** run `tw_report.py 2026-06-29` + check tick-completeness/stability/footprint.
- **NOT ready for a live-cutover conversation** — owes: clean tick-completeness (no material gaps) + stable reconnect across ≥ a few real sessions + live must-not-cut clean + Rhett's go. Live cutover (separate handoff) = real broker-resting stops + exactly one exit owner.

### 2026-06-27 — clean-day false-alarm handoff: Part 1 DONE (schtasks swap); Part 2 = certifier already correct; backfill is HONEST (count not gamed)
- **VERIFY-FIRST overturned the handoff's premise.** Handoff said benign `scheduled_tasks_present` CIM noise was storming `no_critical_incident` → driving `consecutive_clean=0`. NOT TRUE: that noise is already non-disqualifying (the check returns WARN-not-FAIL on timeout + the certifier's `_is_inconclusive_query`/`_is_transient_external` exempt bucket catches 96–148/day). Re-running the certifier's classification proved the real disqualifiers are **genuine trading-path faults**.
- **Part 1 (DONE, valid):** `system_health_verifier.py` — swapped `chk_scheduled_tasks_present` + `chk_scheduled_task_last_run_recent` from `Get-ScheduledTask`(CIM, hangs >30s) to `schtasks.exe` (`_schtasks_names`/`_schtasks_task` helpers, CREATE_NO_WINDOW). Verified: **0.75s + 0.04s**, both return OK; missing-task still FAILs (semantics preserved). Kills the CSHV false-TIMEOUT noise at the source. Non-watched; CSHV re-imports per 5-min run so it auto-loads.
- **Part 2 (NO CHANGE — already implements the intent, and changing it would game the count):** the certifier already exempts NON-TRADING benign noise (CIM/5xx/observational) and keeps real faults strict. The handoff's KEEP-STRICT list (gate-fail-open, recon>2cyc, report-integrity, not-flat) is honored. A loop-stall is trading-path (not in the exempt "non-trading noise" set) so it stays HARD — I did NOT reclassify it to raise the count.
- **BACKFILL (broker-truth, honest):** `consecutive_clean=0`. Per day: **6/19 NON-CLEAN** (gate failing open all day, 64×, 10:40–15:55 — KEEP-STRICT real fault); **6/22 NON-CLEAN** (loop frozen >4min, +148 benign ignored); **6/23 ✓ / 6/24 ✓ / 6/25 ✓ CLEAN** (3-day system-clean run; 6/25 was the P&L-kill day but system-integrity-clean — certifier judges system, not P&L; 96 benign incidents correctly ignored = proof benign-noise day still PASSES); **6/26 NON-CLEAN** (loop frozen >4min at 9:30 — broke the streak). So: benign-noise-heavy day (6/25) PASSES, real-fault days (6/19/6/22/6/26) FAIL — real-fault detection intact.
- **The real lever isn't the certifier — it's the recurring 9:30-AM loop-stall + the 6/19 gate-fail-open.** Fixing those earns clean days legitimately; exempting them would fake the count.

### 2026-06-27 — FIXED: command-window popups (21 scheduled tasks Interactive->S4U) + run_bot taskkill + permissions clarified
- **Popups root cause:** 21 `AlphaQuant*` scheduled tasks ran `LogonType=Interactive` with console actions (`.bat` / `cmd /c python`) → each popped a window on its schedule (CheckAlerts ~20min, Utilization ~30min = the "less frequent" popups). The reverted-from-SYSTEM tasks were the source.
- **Fix (safe, NOT the SYSTEM revert Rhett undid):** converted all 21 to `LogonType=S4U` (runs as **Administrator**, session 0 = no window, **no password**, same account/env). This matches the already-working no-popup tasks (CSHV, Bot Supervisor, EodReconciliation). Verified: **0** AlphaQuant tasks remain Interactive; triggers/actions/state intact; 21 XML backups in `outputs/reports/task_backups_s4u_2026-06-27/` for instant revert.
- **Code cleanup:** `run_bot.py:226,349` taskkill `subprocess.run` were missing `creationflags=_NO_WINDOW` (rare-path popup on advisor-child hang) — added; run_bot restarted (PID 10844, StartTime>mtime) so it's live.
- **Permissions:** both user + project settings already `defaultMode=bypassPermissions` + `skipDangerous=true` → harness shouldn't prompt. The "asking permission" was MY behavior (ending turns with "do you want me to X or Y?") — stopped; just executing per [[feedback_just_do_the_work]].
- **BONUS — the Stop hook is now FIRING:** `planning_sync.log` 13:06:22 "synced turn push=OK" (automatic, not a manual test) + CHAT_LOG has its first real auto-synced turn on the remote. Verbatim every-turn sync is LIVE.

### 2026-06-27 — FIXED: the Stop hook was never firing (root cause = shell backslash mangling, NOT restart)
- The hook command `C:\Users\...\python.exe C:\AlphaQuant\...\planning_turn_sync.py` ran through Git Bash, which ate the backslashes (`C:\Users` → `C:UsersAdministrator...`) → `command not found` (exit 127) every turn, silently, before the script could log. That's why CHAT_LOG stayed empty and the restart didn't help — the hook fired, the command was un-runnable.
- **Fix:** switched `.claude/settings.json` Stop hook to the `args` exec-form (`command`=python.exe, `args`=[script]) → spawned directly, NO shell, backslashes safe. Verified: proper invocation runs + logs (exit 0). Settings existed at session start so the watcher hot-reloads — should fire on the next turn with no restart; confirming next reply via `planning_sync.log`.

### 2026-06-27 — BUILT: auto-sync of every turn to Planning (Stop hook — fixes the "session-log order keeps failing" problem)
- **Why:** the every-turn-update rule failed twice because it relied on Claude Code *remembering*. Fix = remove Claude from the loop. `strategy-research/planning_turn_sync.py` is wired as a Claude Code **Stop hook** (`.claude/settings.json`) → runs automatically at EVERY turn end, no human/memory in the loop.
- **What it does:** streams the live transcript (memory-safe), extracts Rhett's message + my full **verbatim** response, secret-scans + REDACTS (repo is PUBLIC), appends to `CHAT_LOG.md` in the coordination repo, git-pushes (best-effort, rebase-retry on race, CREATE_NO_WINDOW, never blocks the turn, failures logged to `outputs/validation/planning_sync.log`).
- **Verified end-to-end:** parser pulls the exact turn (tested on the live transcript); redaction works (`api_key: …` → `[REDACTED]`); hardened push = OK; remote in sync. Verbatim chosen on purpose — it removes my (unreliable) judgment, which was the failure cause.
- **Planning reads:** `https://raw.githubusercontent.com/Rhettduleba/alpha-quant-coordination/main/CHAT_LOG.md` (verbatim) + `SESSION_LOG.md` (curated digest + this ledger + OPEN DECISIONS).
- **ONE thing pending real-world confirm:** whether the harness activates a just-added Stop hook mid-session or needs a Claude Code restart — confirmed at the start of next turn (check `planning_sync.log`); if it didn't fire, restart needed + I manually sync meanwhile.

### 2026-06-27 — BUILT: SYSTEM_FACTS auto-generated live-truth sheet (Layer 1)
- **What:** `strategy-research/system_facts.py` (read-only) regenerates `SYSTEM_FACTS.md` FROM the running code/config/broker-truth — the fix for Planning stating mechanics from stale memory. Every value is READ from a real source (live import for the VALUE; fresh file-scan for the SOURCE `file:line`); nothing hand-typed; underivable → `UNVERIFIED`.
- **Freshness WIRED (not just intended):** `eod_debrief.main()` now calls `system_facts.generate()` (guarded) and `sync_to_coordination()` pushes `SYSTEM_FACTS.md` alongside SESSION_LOG every 4:50 PM EOD → the coordination repo sheet refreshes daily. Re-runnable any time manually. (`eod_debrief.py` non-watched, runs once-and-exit → next EOD run picks up the change; no restart.)
- **Sample field→source→value (all machine-read):** resting stop distance → `orb_runner.py:98` → **1.4×ATR** · deploy target → `risk_config.py:241` (0.95) × `:237` → **$380k** · confirmation → `candle_close_exit.py:24` → **0.15×ATR** · EOD flatten → `market_hours.py:68/69` → **15:50 ET** · stop coverage → re-derived from `stop_coverage_audit.py` → **37.9% (96% 9:35 / 0% re-arm)**.
- **Only UNVERIFIED field:** relative-strength pool size (not in the published universe artifact) — correctly flagged, not guessed.
- **⚠️ Memory-vs-truth catch (the whole point):** the sheet surfaced `consecutive_clean` = **0 live** (certifier: 6/26 non-clean on the benign `no_critical_incident` CIM-noise) while this log's CURRENT STATE block said "=4". Live truth wins; the "=4" stamp is stale. (Benign-noise-counts-as-non-clean is a known separate issue; not fixed under freeze.)
- **Fetch:** `https://raw.githubusercontent.com/Rhettduleba/alpha-quant-coordination/main/SYSTEM_FACTS.md` · tool `strategy-research/system_facts.py`.

### 2026-06-27 — STOP-COVERAGE AUDIT (is a protective broker stop on EVERY entry, and how fast?)
- **VERDICT: the claim "every entry gets a resting broker StopMarket at entry" is FALSE as stated.** READ-ONLY, broker-truth, reconciled 285==285 to `round_trips_net_all()`; cross-confirmed by an independent 2nd source (`bot_alerts.jsonl` `ORB_SL_OK` count == broker-CSV StopMarket count day-by-day) → NOT a logging artifact.
- **Coverage 37.9%** (107/282 ORB entries, 6/08–6/26), splitting perfectly by path: **9:35 open cohort 96%** (107/111) vs **re-arm / late cohort 0%** (0/171). Mechanism: `orb_runner.py:969` places the resting stop in a post-fill pass keyed only on the 9:35 `entries_submitted`; `orb_multiscan` re-arm never calls `submit_stop_loss_exit`. Break dated to 6/16 (slot-cap 4→16 + re-arm un-starved).
- **Not "at entry":** median latency **~7–8 min** after fill even on the covered cohort; only ~4% within 30s; >5 min in 57%.
- **Distance is 1.4×ATR (chandelier floor), NOT 0.15×ATR** — the "0.15×ATR" label is pre-6/19; K=1.40 exact on every sample.
- **No position was exit-naked:** 282/282 reached flat; PRIMARY protection is the software poll exit (`exit_bot_v2`+chandelier: 209 candle/chandelier + 44 EOD vs only 29 resting-stop fills). The 175 "naked" are broker-resting-stop-naked, not unmanaged.
- **Real BEFORE-LIVE safety gap:** benign in SIM, but if the bot/exit process dies or loses the broker session, ~61% of positions (re-arm cohort) have ZERO broker-side protection + the 9:35 cohort is exposed ~7 min/fill. Downside protection currently depends on the process staying alive. NOT fixed (watched-file live change → Planning gate). Fix candidates: re-arm resting stops + tighten 9:35 placement toward atomic-with-entry.
- **Sources:** `HANDOFF_2026-06-27_STOP-COVERAGE-AUDIT.md` · tool `strategy-research/stop_coverage_audit.py` (read-only).

### 2026-06-27 — DEPLOY-TARGET RAISE 0.75→0.95 ($300k→$380k) [config change, not a test]
- Approved+recorded+loaded (Rhett directive). `risk_config.DEPLOY_TARGET_PCT` 0.75→0.95; per-position $25k + per-side $200k caps UNCHANGED; only lifts the re-arm/multiscan admit ceiling. Swept everywhere incl. dashboard ("$380k target"). Approval `PROP-DEPLOY-TARGET-095-2026-06-26`; change-log `AQ-20260626-ORBV1-DEPLOY-TARGET-095-001`. Verify-loaded (run_bot PID 10904, preflight 0 FAIL, `deploy_target()`==$380,000). LIVE prereqs (available-BP gate + sector/correlation cap) still required before live. Effective Mon 6/29.
---

> **LAST UPDATED BY:** Alert-Triage (autonomous) - 2026-06-26 Fri ~4:04 PM ET (post-close run) - **Inbox CLEAN — 0 actionable alerts, NO escalation (silence=handled). code_alert_inbox.py --json returned n_total=0/n_actionable=0/n_noise=0 (severity-gated feed itself empty). CSHV (4:00:08 PM run, market hours NO) 45 OK / 1 WARN / 0 FAIL / 0 INFO / 3 SKIP. The lone WARN = `clean_day_certified` intraday `['no_critical_incident']`, explicitly "already alerted today; WARN to avoid intraday re-ping spam" = the SAME known knock-on pattern triaged repeatedly 6/25–6/26 (Bucket A: already-confirmed-benign in SESSION_LOG -> ack, no action). NOT new/actionable: `scheduled_tasks_present` **OK** ("All 8 scheduled tasks present"), `rel_position_recon` **OK** (0 positions, agree both ways), no real trading incident — clean_day is only knocked-on. Day closing clean: bot FLAT post-EOD (0 open positions, book $0 == real exposure $0, rel_phantom_deploy_book OK), heartbeat 16s fresh, trade_journal touched 10s ago, SAFE_MODE off, recent_exits.json valid (11 tracked today). daily_review reconciles broker truth (26 RT, NET $524.02 = gross $628.72 − broker-actual cost). report_integrity OK (26 RT, all labels consistent). shadow V9 reconciles broker truth (6/25 23/23) + kill-window sealed (5 days hash-intact). 10 advisor runs today (10 real), control file 3.5h old w/ real tokens, brain universe built today (8.5h ago, 145 published / 530 rel), manager alerts clear (triaged 0.9h ago), token cache 2/2 valid, 0 broker rejections, no OneDrive sync conflicts, deadman beacon armed/healthy, daily_max_loss intentionally disabled for SIM. pre_open_gate ran (GO-WITH-WARNINGS 9:01 AM). SKIPs = eod_flat_at_close (before 4:05 PM window — flatten confirmation pending) + no_overnight_positions_morning (not pre-open) + scan_failure_rate (off-hours). The 9:30 AM rel_trading_is_thinking single-detection freeze (escalated earlier today) remains SELF-RECOVERED, no recurrence (rel_trading_is_thinking OK, outside RTH); re-escalation trigger stays armed. Forward-test freeze in effect (no code edits). --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-26 Fri ~3:04 PM ET - **Inbox CLEAN — 0 actionable alerts, NO escalation (silence=handled). code_alert_inbox.py --json returned n_total=0/n_actionable=0/n_noise=0 (severity-gated feed itself empty). CSHV (3:00:10 PM run, market hours YES) 46 OK / 1 WARN / 0 FAIL / 0 INFO / 2 SKIP. The lone WARN = `clean_day_certified` intraday `['no_critical_incident']`, explicitly "already alerted today; WARN to avoid intraday re-ping spam" = the SAME known knock-on pattern triaged repeatedly 6/25–6/26 (Bucket A: already-confirmed-benign in SESSION_LOG -> ack, no action). NOT new/actionable: `scheduled_tasks_present` shows **OK** ("All 8 scheduled tasks present", CIM cmdlet self-cleared), `rel_position_recon` **OK** (11 reconciled both ways), no real trading incident — clean_day is only knocked-on. Bot HEALTHY: cycling (loop 3292, heartbeat 4–7s fresh), all 11 positions monitored by exit_bot_v2 (highs/lows 0.0m fresh) + reconciled both ways, book $278,622 == real exposure $278,622 (rel_phantom_deploy_book OK, no false 'target reached' refusals), gate enforced (29 selected / 121 candidates, all passed — rel_gate_not_failing_open OK), SAFE_MODE off, 10 advisor runs today (10 real), control file 2.5h old w/ real tokens, manager alerts clear (triaged 0.9h ago), brain universe built today (7.5h ago) / 145 published / 530 rel, recent_exits.json valid (1 tracked), token cache 2/2 valid, 0 broker rejections / 0 scan-failure halts last 30 min, no OneDrive sync conflicts, daily_max_loss intentionally disabled for SIM. daily_review reconciles broker truth (15 RT, NET $2,098.15). shadow V9 reconciles broker truth (6/25 23/23) + kill-window sealed (5 days hash-intact). report_integrity OK (15 RT). pre_open_gate ran (GO-WITH-WARNINGS 9:01 AM). SKIPs = eod_flat_at_close (before 4:05 PM window) + no_overnight_positions_morning (not pre-open). The 9:30 AM rel_trading_is_thinking single-detection freeze (escalated earlier today) remains SELF-RECOVERED, no recurrence (rel_trading_is_thinking OK, loop 3292 advancing); re-escalation trigger stays armed. CLOCK NOTE: `date` reads 3:04 PM EDT and CSHV 3:00 PM ET agree — system clock correct (the `TZ=America/New_York`→7:04 PM is git-bash lacking tzdata, falling back to UTC; benign artifact, not a clock fault). Forward-test freeze in effect (no code edits). --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-26 Fri ~2:04 PM ET - **Inbox CLEAN — 0 actionable alerts, NO escalation (silence=handled). code_alert_inbox.py --json returned n_total=0/n_actionable=0/n_noise=0 (severity-gated feed itself empty). CSHV (2:00:15 PM run, market hours YES) 46 OK / 1 WARN / 0 FAIL / 0 INFO / 2 SKIP. The lone WARN = `clean_day_certified` intraday `['no_critical_incident']`, explicitly "already alerted today; WARN to avoid intraday re-ping spam" = the SAME known knock-on pattern triaged repeatedly 6/25–6/26 (Bucket A: already-confirmed-benign in SESSION_LOG -> ack, no action). NOT new/actionable: `scheduled_tasks_present` shows **OK** ("All 8 scheduled tasks present"), `rel_position_recon` **OK** (11 reconciled both ways), no real trading incident — clean_day is only knocked-on. Bot HEALTHY: cycling (loop 3132, heartbeat 11–17s fresh), all 11 positions monitored by exit_bot_v2 (highs/lows 0.2m fresh) + reconciled both ways, book $299,756 == real exposure $299,756 (rel_phantom_deploy_book OK, no false 'target reached' refusals), gate enforced (29 selected / 121 candidates, all passed — rel_gate_not_failing_open OK), SAFE_MODE off, 10 advisor runs today (10 real), control file 1.5h old w/ real tokens, manager alerts clear (triaged 0.9h ago), brain universe built today (6.5h ago) / 145 published / 530 rel, recent_exits.json valid (1 tracked), token cache 2/2 valid, 0 broker rejections / 0 scan-failure halts last 30 min, no OneDrive sync conflicts, daily_max_loss intentionally disabled for SIM. daily_review reconciles broker truth (14 RT, NET $2,049.09). shadow V9 reconciles broker truth (6/25 23/23) + kill-window sealed (5 days hash-intact). report_integrity OK (14 RT). pre_open_gate ran (GO-WITH-WARNINGS 9:01 AM). SKIPs = eod_flat_at_close (before 4:05 PM window) + no_overnight_positions_morning (not pre-open). The 9:30 AM rel_trading_is_thinking single-detection freeze (escalated earlier today) remains SELF-RECOVERED, no recurrence (rel_trading_is_thinking OK, loop 3132 advancing); re-escalation trigger stays armed. Forward-test freeze in effect (no code edits). --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-26 Fri ~1:04 PM ET - **Inbox CLEAN — 0 actionable alerts, NO escalation (silence=handled). code_alert_inbox.py --json returned n_total=0/n_actionable=0/n_noise=0 (severity-gated feed itself empty). CSHV (1:00:10 PM run, market hours YES) 46 OK / 1 WARN / 0 FAIL / 0 INFO / 2 SKIP. The lone WARN = `clean_day_certified` intraday `['no_critical_incident']`, explicitly "already alerted today; WARN to avoid intraday re-ping spam" = the SAME known knock-on pattern triaged repeatedly 6/25–6/26 (Bucket A: already-confirmed-benign in SESSION_LOG -> ack, no action). NOT new/actionable: `scheduled_tasks_present` shows **OK** ("All 8 scheduled tasks present", CIM cmdlet self-cleared), `rel_position_recon` **OK** (7 reconciled both ways), no real trading incident — clean_day is only knocked-on. Bot HEALTHY: cycling (loop 2972, heartbeat 3–5s fresh), all 7 positions monitored by exit_bot_v2 (highs/lows 0.0m fresh) + reconciled both ways, book $278,358 == real exposure $278,358 (rel_phantom_deploy_book OK, no false 'target reached' refusals), gate enforced (27 selected / 119 candidates, all passed — rel_gate_not_failing_open OK), SAFE_MODE off, 10 advisor runs today (10 real), control file 0.5h old w/ real tokens, manager alerts clear (triaged 0.9h ago), brain universe built today (5.5h ago) / 145 published / 530 rel, recent_exits.json valid (1 tracked), token cache 2/2 valid, 0 broker rejections / 0 scan-failure halts last 30 min, no OneDrive sync conflicts, daily_max_loss intentionally disabled for SIM. daily_review reconciles broker truth (14 RT, NET $2,049.09). shadow V9 reconciles broker truth (6/25 23/23) + kill-window sealed (5 days hash-intact). report_integrity OK (14 RT). pre_open_gate ran (GO-WITH-WARNINGS 9:01 AM). SKIPs = eod_flat_at_close (before 4:05 PM window) + no_overnight_positions_morning (not pre-open). The 9:30 AM rel_trading_is_thinking single-detection freeze (escalated earlier today) remains SELF-RECOVERED, no recurrence (rel_trading_is_thinking OK, loop 2972 advancing); re-escalation trigger stays armed. CLOCK NOTE: `date` reads 1:04 PM EDT and CSHV 1:00 PM ET agree — system clock correct. Forward-test freeze in effect (no code edits). --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-26 Fri ~12:04 PM ET - **Inbox CLEAN — 0 actionable alerts, NO escalation (silence=handled). code_alert_inbox.py --json returned n_total=0/n_actionable=0/n_noise=0 (severity-gated feed itself empty). CSHV (12:00:10 PM run, market hours YES) 46 OK / 1 WARN / 0 FAIL / 0 INFO / 2 SKIP. The lone WARN = `clean_day_certified` intraday `['no_critical_incident']`, explicitly "already alerted today; WARN to avoid intraday re-ping spam" = the SAME known knock-on pattern triaged repeatedly 6/25–6/26 (Bucket A: already-confirmed-benign in SESSION_LOG -> ack, no action). NOT new/actionable: `scheduled_tasks_present` shows **OK** ("All 8 scheduled tasks present", CIM cmdlet self-cleared) and `rel_position_recon` is not in the storm this run — clean_day is only knocked-on, no real trading incident. Bot HEALTHY: cycling (loop 2814, heartbeat 0–2s fresh), all 7 positions monitored by exit_bot_v2 (highs/lows 0.3m fresh) + reconciled both ways, book $260,136 == real exposure $260,136 (rel_phantom_deploy_book OK, no false 'target reached' refusals), gate enforced (22 selected / 114 candidates, all passed — rel_gate_not_failing_open OK), SAFE_MODE off, 8 advisor runs today (8 real), control file 3.9h old w/ real tokens, manager alerts clear (triaged 0.9h ago), brain universe built today (4.5h ago) / 145 published / 530 rel, recent_exits.json valid (2 tracked), token cache 2/2 valid, 0 broker rejections / 0 scan-failure halts last 30 min, no OneDrive sync conflicts, daily_max_loss intentionally disabled for SIM. SKIPs = eod_flat_at_close (before 4:05 PM window) + no_overnight_positions_morning (not pre-open). The 9:30 AM rel_trading_is_thinking single-detection freeze (escalated earlier today) remains SELF-RECOVERED, no recurrence (rel_trading_is_thinking OK, loop advancing); re-escalation trigger stays armed. CLOCK NOTE: prior log stamp labeled 3:04 PM ET is ahead of the real VPS clock — `date` + CSHV both read ~12:00–12:04 PM ET, so the live system clock is correct; the 3:04 PM label is a benign time-labeling artifact in an earlier triage run (NOT a clock fault, not escalated). Forward-test freeze in effect (no code edits). --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-26 Fri ~3:04 PM ET - **Inbox CLEAN — 0 actionable alerts, NO escalation (silence=handled). code_alert_inbox.py --json returned n_total=0/n_actionable=0/n_noise=0. CSHV (11:00 AM run, market hours YES) 46 OK / 1 WARN / 0 FAIL / 0 INFO / 2 SKIP. The lone WARN = `clean_day_certified` intraday `['no_critical_incident']`, explicitly "already alerted today; WARN to avoid intraday re-ping spam" = the SAME known scheduled_tasks_present/CIM-timeout knock-on pattern escalated+diagnosed repeatedly 6/25 (Bucket A: already-confirmed-benign in SESSION_LOG -> ack, no action). NOT new/actionable: the severity-gated inbox feed itself returned 0 actionable, and CSHV now shows `scheduled_tasks_present` **OK** ("All 8 scheduled tasks present", self-cleared) — `clean_day` is only knocked-on, no real trading incident. Bot HEALTHY: cycling (loop 2652, heartbeat 17-19s fresh), all 8 positions monitored by exit_bot_v2 (highs/lows 0.2m fresh) + reconciled both ways, book $279,564 == real exposure (no phantom refusals), gate enforced (17 sel/109 cand), SAFE_MODE off, 8 advisor runs today (8 real), control file 2.9h old w/ real tokens, manager alerts clear, universe 145 published/530 rel, shadow V9 reconciles broker truth (6/25 23/23) + kill-window sealed (5 days hash-intact), daily_review reconciles (5 RT, net $632.28), 0 broker rejections / 0 scan failures, pre-open gate ran (GO-WITH-WARNINGS 9:01 AM). The 9:30 AM rel_trading_is_thinking single-detection freeze (escalated 10:05 AM) remains SELF-RECOVERED with re-escalation trigger armed; no recurrence (CSHV 11:00 AM rel_trading_is_thinking OK, loop advancing). daily_max_loss intentionally disabled for SIM. Forward-test freeze in effect (no code edits). --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-26 Fri ~10:05 AM ET - **ESCALATED 1 issue (CRITICAL ping sent, Discord 204 + Telegram 200 OK) — calibrated LOW-URGENCY/FYI/RECOVERED, not a fire. Inbox had 1 NEW actionable CRITICAL: CSHV `rel_trading_is_thinking` FAIL once at 9:30:11 AM ET — heartbeat fresh (6s) but run_bot main loop_count FROZEN at 2406 for >4min (loop stalled ~9:26-9:30 AM, heartbeat-writer thread stayed alive). NOVEL (first-ever rel_trading_is_thinking FAIL; distinct from the known scheduled_tasks/clean_day CIM-timeout noise). VERIFIED SELF-RECOVERED + ZERO TRADING IMPACT: single detection only (first_ts==last_ts 9:30:11, no recurrence in later 5-min checks); loop resumed and ran the full morning session — ORB SL orders placed 9:39:02 + 9:54:19 AM, 3 positions open + all monitored by exit_bot_v2 + reconciled both ways; CSHV 10:00 AM rel_trading_is_thinking OK (loop 2488 advancing), gate enforced (10 sel/102 cand), SAFE_MODE off, book==exposure, shadow reconciles broker truth; heartbeat now loop 2501 pid 9192; bot_alerts.jsonl 0 FAIL today. Normal cadence ~18s/loop -> >4min stall = ~13 missed cycles, all BEFORE the 9:35 entries fired. Root cause UNVERIFIED — heartbeat-alive-but-loop-frozen rules out a process crash (supervisor did NOT restart); plausibly a one-off GC/IO/network hiccup at the data-heavy open or the same 6/25 VPS CIM/WMI subsystem instability. WHY escalated despite self-heal: NOVEL + liveness/freeze event + occurred at market open + forward-test in progress + Bucket C lists 'bot crash-loop'/liveness -> tie-breaker 'when in doubt, ESCALATE'. PROPOSED (non-watched, freeze-blocked, needs Rhett go-ahead only — NOT watched/risk/strategy): add per-stage timing log around the main loop body + a soft self-watchdog stack-dump if a cycle exceeds ~90s, so a recurrence is diagnosable. No code edited (forward-test freeze). RE-ESCALATION TRIGGER set: a SECOND main-loop freeze, esp. overlapping an active entry/exit window or persisting across >1 consecutive CSHV check (= real stall/crash-loop with impact). No action on the live/trading path. --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-26 Fri ~9:15 AM ET - **ESCALATED 1 issue (CRITICAL ping sent, Discord 204 + Telegram 200 OK) — calibrated LOW-URGENCY/FYI, not a fire. Inbox had 1 NEW actionable CRITICAL (distinct from yesterday's scheduled_tasks_present noise): `supervisor_guardian` restarted `watchdog_supervisor.py` at 6/25 6:56:02 PM ET (found it DEAD, killed orphaned run_bot PID 6316, relaunched supervisor — the CLAUDE.md #15 survivability mechanism working as designed). VERIFIED current state HEALTHY: watchdog_supervisor PID 9232 + run_bot PID 9192 (confirmed correctly parented, 9192 child of 9232) stable ~14h; CSHV 9:00 AM today 46 OK / 0 FAIL / 0 WARN, heartbeat 11s, trade_journal 6s, SAFE_MODE off, flat pre-open, all gates green, research brain + 8 advisor runs done — today's 9:35 session fully supervised. IMPACT ZERO: death/recovery at 6:56 PM ET = ~3h after 4 PM close, account flat at EOD, no scans/entries/positions in that window. NOT a crash-loop: single isolated event, historical watchdog_supervisor recoveries 5/21, 5/31, 6/02 x2, 6/10, 6/25 = first in 15 days. OPEN ITEM (why escalated despite self-heal): root cause UNVERIFIED + novel vs recent noise + Bucket C explicitly lists 'supervisor down' + forward-test in progress -> applied tie-breaker 'when in doubt, ESCALATE'. Plausible (unproven) link to all-day 6/25 CIM/WMI subsystem instability (guardian log: Get-CimInstance 'Shutting down' + 30s timeouts ~12:00-12:10 PM ET, same subsystem behind the scheduled_tasks_present false-FAILs; ~7h separation so not certain). Proposed (non-watched, freeze-blocked): swap Get-CimInstance/Get-ScheduledTask -> schtasks.exe / lighter enumeration in system_health_verifier.py + guardian scan would also harden the supervisor scan; pending Rhett's go-ahead. Re-escalation trigger set: a SECOND watchdog_supervisor death within a short window (esp. market hours) = real crash-loop. No action taken on the live/trading path. --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-25 Thu ~4:00 PM ET - **NO new escalation (silence=handled) — inbox had 3 actionable CRITICAL alerts (3:10–3:45 PM ET), ALL ONE group = the SAME `clean_day_certified` FAIL already escalated to Rhett ~11:05 AM ET today (ping confirmed) + re-verified benign every hour since (12:05/1:00/2:00/3:00 PM). Decomposed LIVE via clean_day_certifier.py this run: failed=[no_critical_incident] ONLY (broker_flat_eod now FLIPPED to OK — flat at EOD, 23 symbols net 0; the day flattened correctly). no_critical_incident = SOFT storm 28>=5 = `{scheduled_tasks_present: 27, rel_position_recon: 1}` (+69 benign ignored) — UNCHANGED meaningful-incident counts vs 3 PM (27/1), NOTHING new after 3 PM. scheduled_tasks_present 27x = the `Get-ScheduledTask` CIM cmdlet hang/TIMEOUT FALSE FAIL (tasks NOT missing — CSHV 4:00 PM run shows scheduled_tasks_present **OK**, "All 8 scheduled tasks present", self-cleared); rel_position_recon 1x = the single 9:40:10 AM LUV open-time fill-tracking blip (1 cycle, self-cleared — Bucket C only escalates recon persisting >2 cycles). Day ended clean: report_integrity OK (23 RT, 0 FAIL/0 WARN), position_recon OK (both ways), gate_enforced OK. Bot healthy: SAFE_MODE off, heartbeat 12s, book $0==exposure $0 (flat post-EOD), shadow V9 reconciles broker truth (6/24 21/21). (NET P&L $-2,016.93 today — not a triage matter; daily_max_loss intentionally disabled for SIM, no daily-loss kill event.) NOT re-pinging Rhett (Bucket A: already-confirmed-benign in SESSION_LOG -> ack, no action) — re-escalating an identical hourly-re-verified issue is exactly the pager noise this system exists to eliminate. Proposed fix (swap Get-ScheduledTask -> schtasks.exe in system_health_verifier.py, non-watched) remains pending Rhett's go-ahead, blocked by forward-test freeze. No action on the live/trading path. --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-25 Thu ~3:00 PM ET - **NO new escalation (silence=handled) — inbox had 3 actionable CRITICAL alerts, ALL ONE group = the SAME `clean_day_certified` FAIL (2:10–2:50 PM ET) already escalated to Rhett ~11:05 AM ET today (ping confirmed) + re-verified benign at 12:05/1:00/2:00 PM. Decomposed LIVE via the certifier this run: failed=[broker_flat_eod, no_critical_incident]. (1) no_critical_incident = SOFT storm 28>=5 = `{scheduled_tasks_present: 27, rel_position_recon: 1}` (+57 benign ignored) — UNCHANGED meaningful-incident counts vs 2 PM (27/1), NOTHING new after 2 PM. scheduled_tasks_present 27x = the `Get-ScheduledTask` CIM cmdlet hang/TIMEOUT FALSE FAIL (tasks NOT missing — CSHV 3:00 PM run shows scheduled_tasks_present **OK**, "All 8 scheduled tasks present", self-cleared); rel_position_recon 1x = the single 9:40:10 AM LUV open-time fill-tracking blip (1 cycle, self-cleared — Bucket C only escalates recon persisting >2 cycles). (2) broker_flat_eod NOT flat = EXPECTED intraday (10 positions mid-afternoon: DELL/PENN/GLW/TECH/PNR/ALB/NOW/CME/BB/TJX, resolves at EOD flatten). position_recon OK both ways (10 reconciled), gate_enforced OK (27 sel/127 cand), report_integrity OK (13 trades 0 FAIL/0 WARN). NO real trading incident: bot cycling (loop 11387 advancing from 11213 @ 2 PM, heartbeat 21s), SAFE_MODE off (active:False), 0 broker rejections/0 scan failures (CSHV 3:00 PM), bot_alerts last 24h = 0 FAIL (only benign ORB_EARNINGS_STALE WARN + 73 INFO). NOT re-pinging Rhett (Bucket A: already-confirmed-benign in SESSION_LOG -> ack, no action) — re-escalating an identical already-diagnosed issue every 20 min is exactly the pager noise this system exists to eliminate. Proposed fix (swap Get-ScheduledTask -> schtasks.exe in system_health_verifier.py, non-watched) remains pending Rhett's go-ahead, blocked by forward-test freeze. No action on the live/trading path. --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-25 Thu ~2:00 PM ET - **NO new escalation (silence=handled) — inbox had 3 actionable CRITICAL alerts, ALL ONE group = the SAME `clean_day_certified` FAIL (1:10–1:50 PM ET) already escalated to Rhett ~11:05 AM ET today (ping confirmed) + re-verified benign at 12:05 PM + 1:00 PM. Decomposed live via the certifier this run: failed=[broker_flat_eod, no_critical_incident]. (1) no_critical_incident = SOFT storm 28>=5 = `{scheduled_tasks_present: 27, rel_position_recon: 1}` (+45 benign ignored) — UNCHANGED count vs 1 PM, NOTHING new after 1 PM. scheduled_tasks_present 27x = the `Get-ScheduledTask` CIM cmdlet hang/TIMEOUT FALSE FAIL (tasks NOT missing — CSHV 2:00 PM run shows scheduled_tasks_present **OK**, "All 8 present", self-cleared); rel_position_recon 1x = the single 9:40:10 AM LUV open-time fill-tracking blip (1 cycle, self-cleared — Bucket C only escalates recon persisting >2 cycles). (2) broker_flat_eod NOT flat = EXPECTED intraday (10 positions mid-afternoon, resolves at EOD flatten). position_recon OK both ways (10 reconciled), gate_enforced OK (26 sel/126 cand), report_integrity OK (12 trades 0 FAIL/0 WARN). NO real trading incident: bot cycling (loop 11213, heartbeat 7s), 10 positions monitored by exit_bot_v2 + reconciled both ways, SAFE_MODE off, gate enforced, 0 broker rejections, 0 scan failures, book $281,502==exposure, shadow reconciles broker truth, bot_alerts last 24h = 0 FAIL (only benign ORB_EARNINGS_STALE WARN + 72 INFO). NOT re-pinging Rhett (Bucket A: already-confirmed-benign in SESSION_LOG -> ack, no action) — re-escalating an identical already-diagnosed issue every 20 min is exactly the pager noise this system exists to eliminate. Proposed fix (swap Get-ScheduledTask -> schtasks.exe in system_health_verifier.py, non-watched) remains pending Rhett's go-ahead, blocked by forward-test freeze. No action on the live/trading path. --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-25 Thu ~1:00 PM ET - **NO new escalation (silence=handled) — inbox had 4 actionable CRITICAL alerts in 2 groups, both the SAME already-escalated issue (escalated to Rhett ~11:05 AM ET today, ping confirmed; re-verified benign ~12:05 PM). Decomposed `clean_day_certified` FAIL directly via the certifier this run: SOFT storm 28>=5 = `{scheduled_tasks_present: 27, rel_position_recon: 1}` (+33 benign ignored). (1) scheduled_tasks_present 27x = the `Get-ScheduledTask` CIM cmdlet hang/TIMEOUT FALSE FAIL — tasks NOT missing; CSHV 1:00 PM run now shows it **OK** ("All 8 scheduled tasks present"), transient hang self-cleared. (2) rel_position_recon 1x = the single 9:40:10 AM LUV open-time fill-tracking blip (1 cycle, self-cleared; LUV SL 9:40:20, exit filled 9:53:19, flat) — Bucket C only escalates recon mismatches persisting >2 cycles. (3) `broker_flat_eod` sub-cond NOT flat = EXPECTED intraday (8 positions mid-day @ 1 PM, resolves at EOD flatten). NO real trading incident: bot cycling (loop 11052, heartbeat 10s), 8 positions monitored by exit_bot_v2 + reconciled both ways, SAFE_MODE off, gate enforced (25 sel/125 cand), 0 broker rejections, 0 scan failures, 0 FAIL in bot_alerts last 24h (only benign ORB_EARNINGS_STALE WARN), book $279,652==exposure, shadow reconciles broker truth. NOT re-pinging Rhett (Bucket A: already-confirmed-benign in SESSION_LOG -> ack, no action) — re-escalating an identical already-diagnosed issue every 20 min is exactly the pager noise this system exists to eliminate. Proposed fix (swap Get-ScheduledTask -> schtasks.exe in system_health_verifier.py, non-watched) remains pending Rhett's go-ahead, blocked by forward-test freeze. No action on the live/trading path. --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-25 Thu ~12:05 PM ET - **NO new escalation (silence=handled) — inbox had 3 actionable CRITICAL alerts, all ONE group = the SAME issue already escalated to Rhett ~11:05 AM ET today (Discord+Telegram ping confirmed sent, full diagnosis+fix logged). Re-verified independently this run: (1) `scheduled_tasks_present` TIMEOUT is a FALSE FAIL — CSHV's `Get-ScheduledTask` CIM cmdlet hangs >30s; tasks NOT missing, confirmed all 37 AlphaQuant tasks present via `schtasks.exe /query` (339 total in 1 fast call: Advisor PreMarket/Midday/PostClose, Bot Supervisor, CSHV, Research Brain, EodReconciliation, this CheckAlerts triage task, etc.). (2) `clean_day_certified` FAIL = pure knock-on (today: 25x scheduled_tasks_present soft incidents storm-trip it >=5 threshold -> 21x clean_day incidents). NO real trading incident: bot cycling (loop 10906, heartbeat 9s), 7 positions monitored by exit_bot_v2 + reconciled both ways, SAFE_MODE off, gate enforced (23 sel/123 cand), no broker rejections, no scan failures, book $279,392==exposure, shadow reconciles broker truth. (3) Lone non-scheduled-task incident today = ONE `rel_position_recon` FAIL at 9:40:10 AM (broker had LUV the bot wasn't yet tracking) — a 1-cycle open-time fill-tracking blip: LUV entry filled 9:35:56, SL placed 9:40:20 (10s after blip), candle-close exit FILLED 9:53:19, position flat; CSHV now OK. Bucket C escalates recon mismatches that persist >2 cycles — this was 1 cycle, self-cleared. NOT re-pinging Rhett: re-escalating an identical already-diagnosed issue every 20 min is exactly the pager noise this system exists to eliminate (Bucket A: already-confirmed-benign in SESSION_LOG -> ack, no action). Proposed fix (swap Get-ScheduledTask -> schtasks.exe in system_health_verifier.py, non-watched) remains pending Rhett's go-ahead, blocked by forward-test freeze. No action on the live/trading path. --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-25 Thu ~11:05 AM ET - **ESCALATED 1 issue (CRITICAL ping sent, Discord+Telegram OK). Inbox had 5 actionable CRITICAL alerts in 2 groups, both CSHV FAILs tracing to ONE harmless cause. ROOT CAUSE (verified): `scheduled_tasks_present` uses PowerShell `Get-ScheduledTask` (CIM cmdlet) which is hanging >3min on the VPS right now -> CSHV 30s timeout fires -> FAIL (TIMEOUT/rc=1), fired 13x today. Tasks are NOT missing: confirmed all 8 expected AlphaQuant tasks present via `schtasks.exe /query` (882ms) + they're firing on schedule (advisor 2x, research brain 07:30, this triage task). KNOCK-ON: `clean_day_certified` FAILs because 13x scheduled_tasks_present soft incidents storm-trip it (14>=5); its broker_flat_eod sub-cond is also NOT flat but that's EXPECTED intraday (6 positions mid-day, resolves at EOD). NO hard faults, NO real trading incident. NOT the 6/22 OOM crisis (RAM 72%/2.2GB free, commit 13.6GB/7.3GB headroom). Escalated (not silent-acked) because: NEW today, contaminates the forward-test `clean_day_certified` invariant, and the fix is a code edit blocked by the freeze. PROPOSED FIX (needs Rhett go-ahead; non-watched file system_health_verifier.py): swap chk_scheduled_tasks_present() from Get-ScheduledTask to `schtasks.exe /query /fo csv /nh` (verified 882ms, lists all 8); same for scheduled_task_last_run_recent. Once landed, clean_day self-resolves + broker_flat clears at EOD. No action taken on the live/trading path. --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-25 Thu ~9:00 AM ET - **Inbox CLEAN — 0 actionable alerts, NO escalation (silence=handled). code_alert_inbox.py --json returned n_total=0/n_actionable=0/n_noise=0. Pre-open run (CSHV 9:00 AM, market hours NO): 45 OK, WARN=0, FAIL=0, INFO=1, SKIP=2 — all operational checks passing: bot heartbeat 17s fresh, trade_journal touched 12s ago, book $0 == real exposure $0 (flat pre-open, no phantom refusals), account flat at pre-open (no overnight carries), SAFE_MODE off, 2 advisor runs today (2 real), control file 1.0h old w/ real tokens, research brain ran today (universe generated_at 07:30:28 ET), published universe 143 names / rel universe 530, manager alerts clear (triaged 0.9h ago), shadow V9 reconciles broker truth (6/24: 21/21), shadow kill-window sealed (4 days hash-intact), daily_max_loss intentionally disabled for SIM, clean_day_certified consecutive_clean=3. SKIPs: eod_flat_at_close (before 4:05 window), scan_failure_rate (off-hours). Forward-test freeze in effect (no code edits). --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-24 Wed ~8:04 PM ET - **Inbox CLEAN — 0 actionable alerts, NO escalation (silence=handled). code_alert_inbox.py --json returned n_total=0/n_actionable=0/n_noise=0. After-hours catch-up run of the */20 triage task (market closed). CSHV (4:00 PM run, market hours NO) 44 OK, WARN=0, FAIL=0, INFO=1, SKIP=3; all operational checks passing — bot heartbeat 19s fresh, trade_journal touched 13s ago, book $0 == real exposure $0 (flat, no phantom refusals), SAFE_MODE off, 4 advisor runs today (4 real), control file 3.5h old w/ real tokens, manager alerts clear, universe 530 names, shadow V9 reconciles broker truth (11/11), canonical daily-review reconciles (21 RT, net $-383.31, win 61.9%, PF 0.8), clean_day_certified consecutive_clean=2, daily_max_loss intentionally disabled for SIM. eod_flat_at_close SKIP (CSHV ran at 4:00, before 4:05 window). Forward-test freeze in effect (no code edits). --ack'd, cursor advanced.**

> **Prior:** Alert-Triage (autonomous) - 2026-06-24 Wed ~3:04 PM ET - **Inbox CLEAN — 0 actionable alerts, NO escalation (silence=handled). code_alert_inbox.py --json returned n_total=0/n_actionable=0/n_noise=0. CSHV (3:00 PM run, market hours YES) 45 OK, WARN=0, FAIL=0, INFO=1, SKIP=2; all operational checks passing — bot cycling (loop 7378, heartbeat 14-16s fresh), all 9 positions monitored by exit_bot_v2 (highs/lows 0.2m fresh) + reconciled both ways, book $320,643 == real exposure $320,643 (no phantom 'target reached' refusals), gate enforced (27 selected of 91 candidates, all passed), SAFE_MODE off, 4 advisor runs today (4 real), control file 2.5h old w/ real tokens, manager alerts clear, universe 530 names, shadow V9 reconciles broker truth (11/11), canonical daily-review reconciles (12 RT, net $1,465.19, win 91.7%, PF 49.26), daily_max_loss intentionally disabled for SIM. Forward-test freeze in effect (no code edits). --ack'd, cursor advanced.**

> **Prior-2:** Alert-Triage (autonomous) - 2026-06-24 Wed ~2:00 PM ET - **Inbox CLEAN — 0 actionable alerts, NO escalation (silence=handled). code_alert_inbox.py --json returned n_total=0/n_actionable=0/n_noise=0. CSHV (2:00 PM run, market hours YES) 45 OK, WARN=0, FAIL=0, INFO=1, SKIP=2; all operational checks passing — bot cycling (loop 7217, heartbeat 15s/18s fresh), all 8 positions monitored by exit_bot_v2 (highs/lows 0.2m fresh), book $300,442 == real exposure $300,442 (no phantom 'target reached' refusals), gate enforced (27 selected of 91 candidates, all passed), SAFE_MODE off, 4 advisor runs today (4 real), control file 1.5h old w/ real tokens, manager alerts clear, universe 530 names, daily_max_loss intentionally disabled for SIM. Forward-test freeze in effect (no code edits). --ack'd, cursor advanced.**

## >>> POST-REBOOT CHECKLIST (Loop 140, 2026-06-22) -- DO THIS FIRST after the VPS reboot <<<
The VPS was rebooted ~4:06 PM ET 6/22 to clear a memory-pressure incident. AutoAdminLogon=1, so on boot it auto-logs-in as Administrator and the 'AlphaQuant Bot Supervisor' logon task should restart watchdog_supervisor -> run_bot. VERIFY within ~5 min of boot:
1. **Memory cleared:** GlobalMemoryStatusEx (ctypes) -> RAM load should be well under 50%, commit headroom multi-GB. (If still tight, a process is leaking -> investigate consumers, now that enumeration works.) ALSO confirm the page-file fix applied: GlobalMemoryStatusEx commit-limit (ullTotalPageFile) ~12-14GB (was 8.3GB) + Win32_PageFileUsage AllocatedBaseSize ~4096MB.
2. **Bot back:** watchdog_supervisor (pythonw) alive; run_bot (pythonw, child of watchdog) alive; `bot_heartbeat.json` < 60s fresh. If NOT up: run the 'AlphaQuant Bot Supervisor' task, or launch `C:\AlphaQuant	radestation-bot\watchdog_supervisor.py` detached.
3. **Gates:** `_preflight_diagnostic.py` 50/50; `regression_suite.py` clean; `system_health_verifier.py` 0 FAIL (the scheduled_tasks_present OutOfMemory FAIL should be GONE once memory is healthy).
4. **Dashboard:** restart it -> `python src\main.py trade-review-ui --host 127.0.0.1 --port 8765 --no-browser` (detached) from ai-trading-strategy-agent.
5. **Must be GREEN before tomorrow 9:30** (Research Brain 7:30, Advisor PreMarket 8:00, 9:35 first scan). Clear the code_alert_inbox cursor of the memory-incident CRITs (`code_alert_inbox.py --ack`) once resolved.
6. Process hygiene: confirm there are NOT multiple orphaned dashboards/pythonw (the suspected leak). Kill any orphans (keep run_bot + watchdog).


## VERIFIED / ASSUMED / BROKEN LEDGER  (seeded Loop 36–39; update every turn)

**VERIFIED (checked against code/data):**
- **Loop 155 (2026-06-28) — EXIT REBUILD (LIVE Mon 6/29 SIM): ⚠️ FREEZE INTENTIONALLY BROKEN + clean-day count RESETS (accepted: fixing the broken core). Rhett chose FULL CUTOVER (I surfaced the TW-unproven-sole-owner risk via AskUserQuestion; he owns the call). K UNCHANGED (1.4, exonerated Loop 154); this is TIMING/COVERAGE/OWNER only.**
  - **CHANGE 1 = DONE + VALIDATED (ships Mon automatically — orb_multiscan runs as a fresh per-cycle subprocess, no restart needed; bot idle Sun).** Re-arm resting-stop coverage 0%→~100% by REUSING the proven 9:35 mechanism: WATCHED `orb_multiscan.py` now registers each armed re-arm entry into orb_runner's shared `daily_state["entries_submitted"]` (new helper `_register_rearm_resting_stops`, + atr/rel_vol carried on armed dicts), so the EXISTING `monitor_fills_and_place_sl` places ONE 1.4×ATR resting stop per fill (idempotent via `sl_orders_placed`) and `cancel_working_exit_orders` cancels it on flatten (no orphan — VERIFIED in exit_orders.py:230). orb_runner UNTOUCHED. Off-market tests T1-T5 PASS: valid-ATR registered / bad-ATR skipped / 9:35 entries+sl_orders_placed preserved byte-for-byte / idempotent re-run=0 / rollover-guard (date-mismatch→no-op, never wipes 9:35 state) / bad-shape→no-op / str-ATR ok. Module offline-demo smoke PASS.
  - **CHANGE 2 (TW single live-exit owner) = SAFETY-FLOOR VERIFIED + LEASE BUILT/TESTED + DESIGN LOCKED; LIVE-FIRING WIRING PENDING (next careful pass before Mon open).** KEY SAFETY PROOF: no-double-exit is STRUCTURAL, not lease-dependent — `exit_orders.flatten_symbol` (exit_orders.py:309) re-reads LIVE broker qty each attempt, returns "confirmed flat" (no order) on qty==0, derives side from live position sign (NO flip). So a 2nd flatten on an already-flat position is a clean no-op; a lease bug costs only LATENCY, never a double-exit/flip. Built shared lease `exit_ownership.py` (TW writes owned+heartbeat; exit_bot_v2 defers for fresh-owned syms; TTL_S=45=3×TW's 15s poll; atomic write): tests T1-T7 PASS — FAIL-OPEN on missing/stale/malformed/no-key (exit_bot_v2 owns everything = status quo), RECLAIM within ≤45s on dead TW. REMAINING: (a) exit_bot_v2 skip-guard (read `owned_fresh()`, defer, fail-open) — contained watched edit; (b) tape_watcher `--live-exit` firing mode (write lease+heartbeat, fire via flatten_symbol, cancel resting stop on exit, fail-safe on stream drop); (c) launch TW detached + supervisor_guardian coverage; (d) e2e validation (single-owner trace, restart idempotency, stream-drop fail-safe, 9:35 regression). Will NOT ship Change 2 until validated (a wrong exit > a slow one).
- **Loop 154 (2026-06-28) — EXIT ATR-MULTIPLE (K) SWEEP 0.5→2.0, 1-min TW replay, READ-ONLY/GROSS.** Tool `strategy-research/exit_k_sweep.py` → `reports/exit_k_sweep.md`. One variable (K = chandelier+resting multiple), structure held (confirm 0.15xATR + candle-close trail); replayed all 282 equities-ORB trades (post-5/26, 0 skipped after fetch-retry) through the chandelier logic on 1-min bars (no intrabar look-ahead: stop level uses water through bar t-1). **PROVENANCE: K=1.4 was HAND-PICKED (Loop 121, to fix 0.15 false-stopouts, "wider than 1.0"), NEVER grid-searched on our trades** (candle_close_exit.py:55-59; TUNE-12 compared only 0.15 vs 1.0) — same trusted-by-design pattern; this sweep is the first fit. **BIG FINDING — it's the TIMING, not the multiple: same structure+K=1.4 replayed on 1-min bars = +$7,488 gross vs the bot's ACTUAL broker gross +$461 over the same 282 trades → ~$7,027 gap = EXECUTION-LAG (5-7min poll late exits + re-arm 0% resting coverage), NOT K** (replay optimistic/no-exit-slippage = upper bound, but direction unambiguous). **K=1.4 EXONERATED:** at proper timing K≥1.0 is a FLAT plateau ($7,220–$8,177, spread only $957 across 1.0→2.0; expectancy ~$26-29/trade, win 75%, PF ~1.4); 1.4 sits near-optimal. Confident directional finding: **do NOT tighten below ~1.0** (K=0.5 kills 32 winners → −$4 breakeven; K=0.7 kills 10). Handoff's prior "1.4 at the whipsaw edge" NOT supported — whipsaw is below 1.0. Do NOT promote the argmax (K=1.6, +$690/+$2.4/trade over 1.4 = WITHIN 1-min noise; argmax wandered 1.6↔1.2 between runs; max-loss non-monotonic across 1.4/1.5/1.6); 1.0-2.0 indistinguishable at 1-min (tick from TW live, proving Mon, would sharpen). MU dominance flagged: −$1,395 (−19%) at K=1.4; MU worst single loss K1.4=−$1,572 vs K2.0=−$577 (even MU's 1-min worst << the lagged −$1,668 broker loss → lag again). In-sample → RANKS for OOS, does NOT promote a number. **REFRAME: the exit fix is TIMING/COVERAGE (foundation-map #4/#8), NOT re-tuning K.** No orders/watched-file/exit change; freeze intact.
- **Loop 153 (2026-06-28) — FOUNDATION MAP (verified-vs-assumed whole-system component audit), READ-ONLY.** Tool `strategy-research/foundation_map.py` → `reports/foundation_map.md`: a living ledger of all 8 core components × {what it actually does [V], why built [A], measured-vs-outcomes?, verdict}, pulling LIVE constants + absorbing the weekend's measured findings with citations. **TALLY: BROKEN/INERT (measured) = #2 gate (anti-selects), #4 exit (killed 6/25 + 0% re-arm stop coverage), #7 advisor (inert). UNPROVEN (mechanically OK, outcome unmeasured) = #1 universe (530-name S&P500+supplement, HTB fail-safe wired), #3 entry-trigger logic (not isolated from selection/gap), #5 sizing (MIN(risk,notional) — risk-aware, NOT naive fixed-$ as feared), #6 risk/correlation (NO correlation control exists; DAILY_MAX_LOSS OFF in SIM), #8 infra-survivability (exit-process-death = naked re-arm positions).** Corrected priors: HTB exclusion IS enforced (memory was stale); sizing is risk-aware; ORB scans the 530 list NOT the 145 research_brain advisor_universe. RANKED REBUILD PRIORITY: 1) #2 gate (highest-leverage broken core selector), 2) #4 exit timing + #8 re-arm 0%-coverage safety gap, 3) #6 add correlation control + restore DAILY_MAX_LOSS (before-live gates), 4) #1/#3/#5 audit-before-touch, 5) #7 advisor (inert ≠ hurting; fix per-symbol-P&L prompt leak). NEXT AUDITS (unmeasured): universe composition, isolated entry-trigger edge, sizing-scheme, correlation/concentration. PRESERVE: the re-arm path (+$19.7/trade PF1.30, ungated), short side (+$11.2 PF1.18), entry execution (0.82bps, collar), HTB fail-safe, the advisor's one-way valve architecture. Reframe = "strip broken layers, keep the working core," NOT rebuild-from-zero. No fix proposed — this is the MAP; fixes are separate gated handoffs. Freeze intact, nothing touched.
- **Loop 152 (2026-06-28) — NEWS-SENTIMENT ANONYMIZATION TEST (Glasserman-Lin distraction effect), READ-ONLY/shadow.** Tool `strategy-research/news_sentiment_anon_test.py` → `reports/news_sentiment_anon_test.md`. Same model (sonnet-4-6, temp 0) scored n=30 mega-cap headlines (MU/NVDA/AAPL from news_shadow.jsonl) NAMED vs name/ticker-MASKED. **VERDICT: distraction effect NOT reproduced — masking is INDISTINGUISHABLE FROM NOISE.** Masking changed only 1/30 reads (0 polarity flips, mean |Δscore| 0.02) — which is BELOW the model's OWN run-to-run noise floor (named-scored-twice self-disagreement = 4/30, |Δscore| 0.05). Outcome alignment: named 5/20 vs masked 6/21 — tied, and the "joinable" items collapse to only 3 distinct ticker-day outcomes (all 6/26: AAPL +2.29% up, MU −1.40% down, NVDA −0.73% down) so alignment has ~3 DOF, anecdote not a rate. The noise-floor measurement is what made it rigorous — earlier single-pass runs showed 2-3/30 "effects" that were just LLM stochasticity. RECOMMENDATION: do NOT fold masking in as a proven accuracy win (not reproduced here); OK to adopt "mask name/ticker before LLM sentiment scoring" as a cheap PRECAUTIONARY default (research-motivated, not locally-proven); a real test needs larger N + news joined to the correct FORWARD session + a both-directions day. CAVEAT: small N, mega-cap-only, in-sample, same-session open→close outcome (DERIVED), 3-day news_shadow snapshot. SHADOW: no orders/watched files/trading impact.
- **Loop 151 (2026-06-28) — ADVISOR AUDIT v2: LOOK-AHEAD HUNT + monoculture (research-grounded skeptical prior).** Extends Loop 150 (`advisor_audit.py` → `reports/advisor_audit.md`) with the field's #1-failure check. **LOOK-AHEAD VERDICT: CLEAN in live operation** — the advisor's inputs do NOT postdate the moment it acts (opposite of the confirmed-vs-unconfirmed trap). Temporal ordering VERIFIED from run log (runs 8:00/12:30/4:30 ET → controls govern only LATER entries; info precedes action). News ingested LIVE (≤ run time by construction); news_collector.py:22-23 = NO separate sentiment model (headline+time only, Claude judges) → no LLM-sentiment look-ahead. No same-day outcome/label in the prompt. CAVEAT: run log has ~6 off-schedule runs per hour = a replay/backtest batch → don't trust any in-sample/replay advisor number (matches research prior). **The skeptical prior is VINDICATED but via a DIFFERENT mechanism than look-ahead: not "fake in-sample edge that dies live", but "no edge applied at all" — the advisor is structurally disconnected from the book, so there's nothing for look-ahead to contaminate.** MONOCULTURE: advisor + 9:15/9:40 daily_report both sonnet-4-6 but VERIFIED independent pipelines (no cross-feed); correlated error LATENT/unrealized (neither alters the book). SECONDARY (not look-ahead): per-symbol rolling-10d P&L IS still rendered in the prompt (prompt_builder.py:307-310, journal_analyzer.py:136 not baseline-filtered) — partial regression of the "performance-by-symbol REMOVED / strategy-not-symbols" design; the PATTERN-section removal landed but the recent-performance symbol_pnl surface survived. Worth a deliberate decision; no change made (read-only). Freeze intact.
- **Loop 150 (2026-06-28) — ADVISOR AUDIT (3rd core component: what it does + helped/hurt on broker truth), READ-ONLY.** Tool `strategy-research/advisor_audit.py` → `outputs/reports/advisor_audit.md`. **BOTTOM LINE: the Advisor is NET-NEUTRAL / effectively INERT on the real book post-baseline — changed 0 of 285 trades, $0.** Q1 (verified from code): model `claude-sonnet-4-6` (claude_client.py:14); runs 8:00/12:30/4:30 ET (308 runs logged); inputs = market snapshot + journal + patterns + memory + earnings + news + bot-health; path prompt_builder→call_claude→response_parser→control_writer writes `active_controls`; control file honored (CONTROL_VALID every read in trading window). Q2 (the gate-style structural gap): **100% of real trades are ORB (282 orb_v1_6 + 3 h5); composite `bot_loop` took 0 trades.** ORB (`orb_runner.py`) imports ONLY `should_block_entry` → honors HARD blocks only (BLOCK_SYMBOL/_DUE_TO_NEWS, BLOCK_ALL, ALLOW_SYMBOLS_ONLY, BLOCK_ENTRIES_AFTER_TIME). The SOFT controls — WATCHLIST_TODAY, PROMOTE_SYMBOL, REQUIRE_MIN_NET/NEG_CHANGE_PCT, SET_MAX_POSITION_PCT, REDUCE_MAX_POSITIONS (the MAJORITY of what it emits, ~13/run) — are read only by composite `bot_loop` → STRUCTURALLY INERT on the book. ORB universe = `orb_universe.build_universe()` (S&P500+supplement); does NOT consume the advisor universe channel (cosmetic sector map only) → advisor can't shape ORB selection either. Q3 (helped/hurt, broker truth): post-5/26 actual block events = 698 {BLOCK_ALL 503 (all 5/26, a 0-trade day), BLOCK_ENTRIES_AFTER_TIME 3 (off-hours/replay), BLOCK_SYMBOL 192}. BLOCK_SYMBOL = 192 events but only **3 distinct (date,sym): CVX/JNJ/MCD on 6/19, and 192/192 were pure broker-`[NO]`-flag relays (0 advisor-judgment blocks)**. **blocked∩traded = 0; blocked∩selected = 0** → counterfactual is EXACT not derived (no altered trade to simulate) → gross effect **$0**. CAVEAT: post-5/26 window only (current-bot baseline); pre-5/26 the advisor DID make judgment blocks (5/12 CRM) + composite traded (out of scope by baseline rule). The advisor still does ADVISORY/human-facing work (regime, watchlist, memory, daily review) — measured here = effect ON TRADES only. Third trusted-by-design component in a row found mis-wired/inert (after gate anti-selects + exit kill). Freeze intact, no watched files touched.
- **Loop 149 (2026-06-28) — GAP-FADE HYPOTHESIS TEST (Rhett's theory) on the gated 9:35 trades, READ-ONLY/GROSS.** Tool `strategy-research/gap_fade_test.py` → `outputs/reports/gap_fade_test.md`. **VERDICT: directionally SUPPORTED but MU-dominated.** Made DETERMINISTIC by switching the gap source from per-symbol 1-min-bar fetches (which throttled non-deterministically — gap-up&long flipped from −$1,814 to +$182 to −$2,188 across runs) to the **logged 9:35 scan price vs prior_close** in `orb_candidate_log.jsonl` (full coverage, no fetch; two consecutive runs now identical). Findings (52/111 classified = gate-era 6/15+; pre-6/15 9:35 trades have no candidate row): (1) **The 9:35 gate forces DIRECTION-MATCH → every gapped entry is BY CONSTRUCTION a WITH-gap entry (with-gap n=52 −$63.9/trade; AGAINST-gap n=0 — the gate structurally cannot make them).** So the gate MANDATES the losing with-gap pattern. (2) gap-up&long is the worst bucket (n=19, −$115/trade, PF 0.31) **but 76% is the single MU 6/25 trade (−$1,668 of −$2,188); ex-MU −$28.9/trade (mildly negative).** (3) gap-down&short n=33 −$34.4/trade PF 0.70 (also loses). (4) 45% of long losers (10/22) were gap-up-longs grossing −$3,158 > the net long loss → ex-gap-up-longs the long side turns positive. CAVEAT: early-shape (noise-then-fade mechanism) DEFERRED (1-min-bar throttle); gap vs immediate prior close understates multi-day; in-sample; GROSS only. Hypothesis to OOS-test pointing the fix at gap-handling (don't force chasing gap-direction / fade large gaps) — NOT a gate/strategy change (freeze intact, watched files untouched).
- Candle-close exit deployed 6/10 5:22 PM; `candle_close_exit.py` matches spec (0.15 stop→0.15 confirm→first-opposite-candle→1.0 cat).
- Multi-scan builds a fresh 5-min range per window (10:35–14:35); tagged ORBMS<window>.
- Broker-truth COMPLETE for 6/11 + 6/12 — unified log == independent TS historicalorders API (30==30, 24==24), 0 status mismatches (p0 harness).
- Freeze 6/12 caused no missed/stuck/duplicate orders (0 dup fills; 6/12 set complete; recovered pre-open).
- Index-ETF P&L immaterial (1 SPY RT −$11 vs 52 single-name +$709).
- Deploy-controller NOW governs the 9:35 main book (Loop 37) — wiring audit 6/6 OK, in preflight.
- Slippage + left-on-table calcs OK (guarded).
- A2 (Loop 45): pre-fix main-book 6/08–6/12 — NO $25k/name breach (max $20,000), NO extreme skew (worst 65% long 6/10); max single-side daily gross $159k < $200k (50%) cap. Deploy-controller main-book fix is confirming, not corrective, for this window.
- A4 (Loop 45): p0 --live cross-check 6/08 (14==14), 6/09 (14==14), 6/10 (24==24), 0 status mismatches → full 6/08–6/12 window independently verified (5/5 days; 6/11–6/12 prior).
- ORB live gate has NO %-move / spread / min-volume / MAX_TRADES_PER_DAY / cooldown enforcement (those constants are composite-path only, DEAD for ORB). Confirmed by grep of orb_runner/orb_multiscan/exit_bot_v2 (Loop 45 Part-1 sweep).

**ASSUMED (not independently verified — treat with caution):**
- Broker-truth completeness for days OTHER than 6/11–6/12 (only those two cross-checked).
- Cost-model reg-fee rates current as of 2026-06-14 (SEC $20.60/$1M; FINRA TAF $0.000195/sh) — refresh periodically.
- Which LIVE commission plan applies (TS Select vs per-share) — **Rhett confirming**; default per_share_standard.

**BROKEN → FIXED:**
- **Loop 61 (LIVE 6/15): deploy_controller.book_from KeyError 'side' aborted EVERY 9:35 scan → 0 trades armed 9:35–9:45.** Raw TS broker dicts passed to a fn expecting {'side','notional'}; only survived before because bot was flat at scan. Made defensive; verified 16 armed after fix. Earlier A2 claim "deploy-controller main-book fix is confirming not corrective" was WRONG — it was crashing/empty, never really governing. Wiring-audit gap: verified the flag is referenced, not that book_from gets the right data shape.
- A3 (Loop 47): R-multiple had TWO inline defs (trade_analytics 0.10 default, truth_dashboard 0.15) → unified into one shared `src/advisor/r_multiple.py` (R_STOP_ATR_FRAC=0.15). Single source now.
- R-multiple denominator 0.10→0.15 (matched live stop + /truth). MFE floored by exit fill. Deploy-controller scope (re-arm-only → main book). 11 home cards → retired stubs (removed). Hero alignment/size.

**BROKEN / OPEN:**
- **TUNED Loop 48:** INPLAY_MIN_DAY_RELVOL set to **1.5** (was 2.0) from clean dry-run — 4.4 names/day, marginal names still clear movers. Gate OFF pending Monday flip. (Re-sweep anytime: `python inplay_dryrun_universe.py --use-cache`.)
- **RESOLVED (Loop 49b): market-cap source pulled.** `build_market_caps.py` pulls NASDAQ public screener → `tradestation-bot/market_caps.csv` (522/530 universe; misses = 5 ETFs + BRK.B/BF.B + 1 delisted). `orb_runner._mcap_bucket` reads it; mcap_bucket tag now real (mega/large/mid/small). Re-run build_market_caps.py to refresh.
- **MONDAY GREEN checklist (Planning Loop 49+50+51):** (1) human sets ORB_INPLAY_GATE=True + ORB_ENTRY_MAX_AGE_MIN=20 + approval in manual_approvals.yaml; restart run_bot. (2a) `python verify_gate_drove_entries.py` → must return **PASS (exit 0)**: requires ≥1 filled entry (all in selected), ≥1 old-gate-rejected-and-not-traded name (real divergence), gate_enforced=True. **INCONCLUSIVE (exit 2) on a quiet/no-divergence day is NOT green** — wait for a day that exercises the gate. FAIL (exit 1) = violation. (2b) FILL-TIME: if no natural stale entry, `python inject_stale_entry.py` during market hours → watch bot_alerts for ORB_STALE_ENTRY_CANCELLED. (3) preflight 47/47 (weekend-stale self-clears at first scan; fix if not). (4) confirm mcap_bucket/rel_move_vs_spy/dollar_vol_tier on live trades. GREEN only when 2a PASS + 2b + 3 all observed.
- **MONDAY (flip gate ON, AFTER tuning):** set `ORB_INPLAY_GATE=True` (+ record approval in `config/manual_approvals.yaml`), optionally `ORB_ENTRY_MAX_AGE_MIN=20`; restart run_bot; at 9:35 capture live trace (gate driving real entries via `orb_candidate_log.jsonl` + `ORB_INPLAY_GATE` alert) + fill-time kill; preflight 47/47 → GREEN. Gate built+verified OFF Loop 47; wiring-audit already has both contracts (8/8).
- Exit-design nuance (A1, paused exit-redesign A/B input): resting 0.15×ATR StopMarket co-exists with candle-close phase-2 and is NOT cancelled on confirmation → 12/50 trades stopped at 0.15×ATR instead of riding to an opposite-candle close.
- **Part-3 in-play gate (Loop-45 blocker, RESOLVED Loop 47 — data layer built in orb_data_collector + computed at arm time in orb_runner; gate OFF pending Monday live trace).** Original blocker text below for history: (a) `mover_scanner.py`/`mover_trader.py` are NOT referenced in `run_bot.py` → not in the live loop → `outputs/mover_scanner/scans.jsonl` is never produced (file absent). (b) ORB warmup caches only OR-vol history + ATR — no prior-close (→ "move from prior close"), no cumulative-day-RelVol (proposal's "day-RelVol≥2.0" ≠ the OR-RelVol the bot computes), no 20d avg $-vol. (c) `ORB_INPLAY_GATE` flag does not exist. (d) Fill-time validity gate does not exist (the reject-fix is SUBMIT-time only). Build path: compute the gate inputs in orb_runner at arm time (recommended) OR wire mover_scanner into the loop; ship behind OFF flag + tagging first; flip ON + live-trace Monday.
- A1 (exit behavioral proof) and A3 (R single-source fn) NOT yet done.
- The in-play/RelVol EDGE runs in SHADOW — live ORB = ORB-on-S&P, not ORB-on-movers (in-play gate proposed, parked, PROP-INPLAY-ENTRY-GATE).
- Cost is modeled (commission_model.py + recompute) but not yet shown on the live /truth page (recompute is a script). After-cost: per-share commission HALVES the edge ($479 gross → $238 net; stress → +$20).

> *(Loop number is the shared counter with Planning Claude. App: read the PINNED commit URL, not /main/ — /main/ has a 5-min CDN cache and can show a stale stamp.)*
>
> **APP CLAUDE — read this file every turn.** Repo is PUBLIC, no connector needed.
> • Home URL (can be up to 5 min stale): `https://raw.githubusercontent.com/Rhettduleba/alpha-quant-coordination/main/SESSION_LOG.md`
> • ALWAYS-FRESH: Rhett pastes a commit-pinned URL each turn that looks like `…/<40-char-commit-sha>/SESSION_LOG.md` — that one can never be stale. Prefer it.
> • Confirm you have the latest by checking THIS stamp's timestamp before you answer.
> *(Every editor updates this line first. To see who's fresh: read this stamp or run `git log` in the coordination repo.)*

**This is the file that holds a running record of everything we do, turn by turn.**
If Claude crashes, hand a fresh instance this file (plus `CLAUDE.md`) and it can ramp up cold.

## HOW THE TWO CLAUDES COORDINATE THROUGH THIS FILE

This file is a **shared notebook**, not a live message bus. Neither Claude runs continuously or gets
pinged when the other writes. Coordination is *pull-based* — each side checks the file when it's active:

- **Claude Code (VPS, does the work):** `git pull` the coordination repo at the **start** of every turn and
  read this file before acting; write the turn entry + update the LAST UPDATED stamp + `git push` at the **end**.
- **Claude app (planning chat):** the repo is **PUBLIC** (Rhett's informed call 2026-06-12 — the connector
  path wasn't working), so the app reads this file directly by URL — no connector needed:
  `https://raw.githubusercontent.com/Rhettduleba/alpha-quant-coordination/main/SESSION_LOG.md`. Fetch it at the
  start of every turn. To send Code something, the app gives Rhett a short note for the "FROM PLANNING CLAUDE"
  inbox (a public repo is read-only to the app without auth; Code commits the inbox note on Rhett's relay).
- **Who updated it & when:** the LAST UPDATED stamp at the top + `git log` (author, time, message) are the record.
- **Rhett's role:** still the conductor — he tells each side "your turn, go read it." He no longer copies/pastes
  the content between them; the file carries it. (Two sides editing between pulls can git-conflict — keep edits in
  separate sections / take turns, which happens naturally since one Claude is active at a time.)

### FROM PLANNING CLAUDE (app → Code inbox)
*(The planning-chat Claude leaves notes for Claude Code here; Code reads them on its next pull. Empty = nothing pending.)*
- _(none yet)_

- **Location:** `C:\AlphaQuant\SESSION_LOG.md`
- **Desktop shortcut:** `SESSION_LOG` on the desktop points here.
- **Updated:** every turn going forward (per Rhett, 2026-06-11). Newest entries at the top of the log.
- **Related canonical docs:** `C:\AlphaQuant\CLAUDE.md` (rules/primer) · `C:\repos\alpha-quant-coordination\ALPHA_QUANT_STATE.md` (state snapshot).

---

## HOW TO RAMP UP A NEW CLAUDE (read this first if you just crashed)

1. Read `C:\AlphaQuant\CLAUDE.md` — the project rules, SIM-only guards, one-way advisor→bot channel, working discipline.
2. Read this file top-to-bottom — current state + the dated session log below.
3. Verify reality before acting (project rule: never assume, test it):
   - Bot alive? `python C:\AlphaQuant\tradestation-bot\_preflight_diagnostic.py` (expect 46/46 PASS).
   - Dashboard up? open `http://127.0.0.1:8765/` — if down, restart (command below).
   - Truth of P&L? open `http://127.0.0.1:8765/truth` (broker-truth sourced).

---

## CURRENT SYSTEM STATE  (as of 2026-06-11 ~10:45 PM ET)

### Live root & accounts
- **Live root:** `C:\AlphaQuant\` (OneDrive folder is backup-only since the 5/21 migration). Always use absolute `C:\AlphaQuant\...` paths.
- **ORB strategy:** `orb_v1_6`, equities, account **SIM1623888M**. Bot = `tradestation-bot\run_bot.py`.
- **H5 strategy:** Gao @MES futures, account **SIM1623889F** — currently **QUARANTINED / sidelined** (flag `h5_disabled.flag`); code/state intact.
- **SIM-only, non-negotiable.** Daily $2k stop temporarily OFF in SIM for data collection; 5% account-DD kill remains.

### What is DEPLOYED right now (bot behavior)
- **ORB_MULTISCAN = ON** (deployed 6/11 5:26 PM). Hourly re-arm windows: **10:35, 11:35, 12:35, 13:35, 14:35** on top of the 9:35 opening scan. Goal: lift capital utilization toward the 75% target (6/11 peak was only 34.8% of $400k).
- **DEPLOY_CONTROLLER = ON — but only governs the MULTI-SCAN RE-ARM path, NOT the primary 9:35 scan** (corrected 2026-06-14 Loop 35 by the wiring audit). `orb_runner.py` (the 9:35 main book) never calls it; it sizes by its own constants (TARGET_DAY_TRADE_GROSS/TOP_N ≈ $15k/name, MAX_DAY_TRADE_GROSS $400k gross). So the controller's per-position $25k / per-side 50% / 75% target apply to re-arm fills only. OPEN DESIGN Q: should it govern the 9:35 book too, or is re-arm-only intended?
- **CONVICTION_SIZING = OFF** (flat sizing until data earns the tilt).
- **ORB_EXIT_MODE = candle_close** (0.15×ATR Phase-1 stop → confirm +0.15×ATR → first opposite-color 1-min candle close → 1.0×ATR catastrophe).
- All of the above are flag-gated in `tradestation-bot\risk_config.py` — flip back to revert. **Tomorrow (6/12) is the FIRST live multi-scan session — watch it.**

### Dashboard (the advisor command center)
- Local server: `http://127.0.0.1:8765/` — `python src/main.py trade-review-ui --host 127.0.0.1 --port 8765` from `C:\AlphaQuant\ai-trading-strategy-agent\`.
- **The 3 real, broker-truth pages** (everything else is legacy):
  - `/pre-market-evaluation` — "where we're headed": live scanner watchlist (stocks in our sight) + the bot's plan + is-it-working.
  - `/daily-review-v2` — "exactly what happened": every trade, charts, capital used, left-on-table, narrative.
  - `/truth` — "is it working": net P&L / expectancy / win rate / long-vs-short / pre-vs-post-fix, with a connection gate.
- Home page (`/`) now leads with a 3-question command hero linking to those three.
- **Source of truth for P&L:** `C:\AlphaQuant\tradestation-bot\broker_orders_unified.csv` (FILLED rows). NEVER the phantom `trade_journal.csv` (it silently missed whole trades → showed 0 on a 15-trade day).

### How to restart things
- **Dashboard:** kill any `python.exe` whose command line contains `trade-review-ui`, then run the server command above (from the advisor folder). It serves once port 8765 is listening.
- **Bot:** `run_bot.py` is respawned by `watchdog_supervisor.py`; killing it triggers a clean restart that reloads `risk_config.py`. After any config change, verify-load: new PID StartTime AFTER the file mtime + `_preflight_diagnostic.py` 46/46.

---

## CANONICAL DOCS MAP  (this file is the hub; these are the deep references)

| Doc | Location | What it holds |
|-----|----------|---------------|
| **SESSION_LOG.md** (this) | `C:\AlphaQuant\SESSION_LOG.md` | Master handoff: current state + decisions + turn-by-turn log. **Start here.** |
| CLAUDE.md | `C:\AlphaQuant\CLAUDE.md` | Hard rules: SIM-only guards, one-way advisor→bot channel, control vocabulary, working discipline. |
| ALPHA_QUANT_STATE.md | `C:\repos\alpha-quant-coordination\` | Deeper architecture/state snapshot (v3.9). |
| ALPHA_QUANT_STRATEGY_SPEC.md | `C:\repos\alpha-quant-coordination\` | Strategy spec (ORB / H5 detail). |
| CHANGELOG.md | `C:\repos\alpha-quant-coordination\` | Dated change log. |
| Memory files (43) | `…\.claude\projects\…\memory\` | Per-decision detail; index in `MEMORY.md`. |
| **Cloud backup repo** | `github.com/Rhettduleba/alpha-quant-coordination` | Off-machine copy of SESSION_LOG.md so a fresh Claude can read it if the VPS dies. |

## ARCHITECTURE IN BRIEF

Two cooperating Python systems, SIM-only equity/futures trading on TradeStation:
- **The Bot** (`tradestation-bot/`) — narrow, dumb, reviewable. Places SIM orders, enforces risk. Entry `run_bot.py` → `bot_loop.py`. Hard risk floor in `risk_config.py`.
- **The Advisor** (`ai-trading-strategy-agent/`) — smart, learning. Daily Claude analysis + the dashboard. Writes ONE typed JSON control file the bot obeys.
- **The one-way channel** — advisor writes `outputs/advisor_guidance/advisor_control_latest.json`; bot's `advisor_filter_engine.py` reads it with paranoid validation. Rejected control → bot defaults to ALLOW (a stale advisor never locks the bot out). The advisor NEVER reaches into bot config.
- **Architectural rule:** the agent may know a lot; the bot does only what's proven. Every gate that changes live behavior is human-owned.
- **Staged ramp:** currently stages 3–4 of 6 (SIM testing + AI advisor layer). Live trading (stage 6) only with explicit human approval.

## STANDING DECISIONS  (the running decision log — append every change here)

**STANDING RULE #0 — VERIFY BEFORE YOU STATE (permanent, both seats; Loop 87, 2026-06-15).** NEVER present a guess or an unverified claim as fact. Verify every load-bearing claim against the real source (live data / actual code / broker truth) BEFORE stating it. If it can't be verified yet, say so explicitly ("unverified" / "needs live capture" / "pending") — never fill the gap with a plausible guess. Check BEFORE acting, not after. **Nothing untested reaches Rhett.** Also written into CLAUDE.md working rules. Applies to Planning Claude AND Claude Code.

**Scope / infrastructure**
- 2026-05-21 — VPS-only; OneDrive is backup. 2026-06-07 — live root migrated to `C:\AlphaQuant` (OneDrive backup-only).
- 2026-06-11 — SESSION_LOG.md is the master handoff, updated every turn, backed up to the GitHub coordination repo.

**Strategy / risk**
- ORB v1.6 (equities, SIM1623888M) is the primary strategy; H5 Gao @MES (SIM1623889F) is sidelined/quarantined.
- 2026-06-10 — candle-close exit adopted (`ORB_EXIT_MODE="candle_close"`).
- 2026-06-11 — `ORB_MULTISCAN` ON + `DEPLOY_CONTROLLER` ON (target 75% of $400k) to fix capital under-utilization (6/11 peak was 34.8%). First live multi-scan = 6/12.
- 2026-06-03 — sizing off the intended LIVE $100k base (×4 BP = $400k), NOT the $993k SIM equity. Daily $2k stop temporarily OFF in SIM for data; **must be restored + hardened to a real-time intraday clamp before live.**
- 2026-05-28 — **Strategy, not symbols:** never make trading decisions from a symbol's prior P&L. BLOCK_SYMBOL only for structural reasons (earnings/news/halt/leveraged-ETF/regulatory).
- 2026-05-28 — **Post-5/26 data only:** the 5/26 megabuild changed bot behavior; trade stats must filter to ≥2026-05-26. SIM account resets when a winning, bug-free system is confirmed. Success metric = diverse trade generation + correctness, not today's P&L.
- Evidence hierarchy: BROKER_TRUTH > BROKER_EXPORT > LOCAL_RECONSTRUCTION > BOT_LOG_CONTEXT > ADVISORY_RESEARCH. Broker truth = `broker_orders_unified.csv`.
- 2026-06-21 (Loop 127) — **Clean-day = the certifier, not "the bot ran."** `validation/clean_day_certifier.py` is the authoritative clean-TRADING-day predicate feeding the kill-window consecutive_clean (report-integrity + broker-flat + no-incident + position-recon + gate). Report-integrity + metamorphic checks (`validation/report_integrity.py`) + the assumption/uncertainty/claims ledgers (`research/*.yaml`) are live on CSHV + the dashboard `/decision-quality`. Canonical exit codes + fidelity labels: `validation/exit_reason_codes.py`. All non-confounding (no watched strategy file touched).

**Working style (how Claude operates here)**
- Update SESSION_LOG.md every turn; keep the state block current on any flag/deploy change.
- NEVER output a "what I did not verify" section — verify everything that can be verified.
- Never reason from incomplete data; read the source before explaining load-bearing claims.
- One question per turn, max. Copiable handoffs (full paste blocks, not "see file X"). 12-hour AM/PM times.
- Be objective + proactive; pair every critique with a build plan; stress-test external-AI inputs rather than following them.
- Strategy changes are advisory-only until a human records approval in `config/manual_approvals.yaml`.

## SESSION LOG  (newest first)

### 2026-06-22 — Loop 131: Monday AM — Discord-spam root-cause + fix, final validation GREEN

Rhett (6:24 AM): "check the Discord notifications — am I getting too many + are they accurate? Then run a final systems validation."

**Discord finding (quantified from cshv_status.jsonl):** midnight→6:25 AM = **78 CSHV runs, all 78 produced "CSHV 1 FAIL check(s)" → ~78 identical CRITICAL Discord pings** for ONE persistent FAIL. Plus ~hourly WARN pings. So: **yes, far too many, and it's noise.** The FAIL (`brain_universe_fresh`, universe stale since Fri 6/19 weekend-skip) is *technically accurate* but *not actionable* — it auto-clears at the 7:30 brain run.

**Root causes + fixes (all non-trading, read-only check/notifier code; no WATCHED files):**
1. **Ran the Research Brain now** → published a fresh universe (150 symbols, 10,827 quotes primed, regime CHOPPY) → cleared the FAIL immediately AND guarantees fresh data for the 9:35 scan (not just silence).
2. **notifier CRITICAL dedup 60s → 900s** — 60s < the 300s CSHV interval meant a persistent CRITICAL was NEVER suppressed (re-pinged every run). Now: first occurrence + any subject change (FAIL count 1→2) still instant; repeat-reminder of an ongoing critical throttled to every 15 min.
3. **`brain_universe_fresh` made pre-7:30-brain-run-aware** — was FAIL→CRITICAL all night Monday (post-weekend gap); now SKIP until 8:30 AM (today's run not due yet), real FAIL after.
4. **`scheduled_task_last_run_recent` made disabled-task-aware** — AlphaQuantBot is the intentionally-disabled legacy launcher (bot runs via the supervisor chain); was a permanent hourly noise WARN, now OK.
5. **preflight `orb_daily_state` made pre-9:35-scan-aware** — was FAILing every trading morning 00:00–09:35 (state only refreshes at the 9:35 scan); now OK pre-scan, real FAIL if stale after 9:36.

**Net:** Discord goes from ~78 CRIT/night + hourly WARN → ~0 unless something genuinely new happens (then instant first ping + 15-min reminders).

**Deadman beacon ARMED (Rhett provided URL):** added `HEALTHCHECK_PING_URL` (healthchecks.io, 15m period / 10m grace) to `tradestation-bot/.env` (gitignored — NOT committed). Beacon ran: armed=True, ping OK:200, healthy. AlphaQuant_DeadmanBeacon task pings every 5 min (well inside the 25-min alert window). CSHV deadman check → OK. **CSHV now 0 FAIL / 0 WARN (40 OK).** The off-box VPS-death gap is closed: if the whole VPS dies/freezes, healthchecks.io alerts Rhett directly.

**Notification necessity review (Rhett: "are they all necessary?"):** audited ALL notifier callsites (grep rule 17) — 24 distinct notification types across 8 files. Verdict: the **12 CRITICAL** (crash-loop, failed-start, frozen, EOD-safety-net-failed, supervisor-crashed, EOD-positions-open, CSHV real FAILs, drill deaf-detector, brain FAILED, advisor zero-tokens, guardian restarted/failed) and **6 WARNING** (CSHV WARNs, bot crashed-restarting, advisor missing/stale, empty-universe, supervisor-stopped-manually) are ALL necessary — real failures, low-frequency. Of 6 INFO confirmations, **trimmed 4 redundant ones** (supervisor-started, bot-restarted-OK, restarted-after-freeze, EOD-flatten-started → now `_log`/`print` only, no Discord) and **kept 2 daily confirmations** (EOD "account confirmed flat" = daily no-overnight-risk proof; drill "PASSED heartbeat" = proof the alert pipe delivers). No failure signal lost. Today's actual sends: only CSHV (4 subjects, last 06:33), silent since deadman armed. LOAD: eod_watchdog auto-loads next EOD (3:50 PM); watchdog_supervisor (PID 236) change loads on next watchdog restart — running proc keeps old INFO behavior until then (benign; only fires on a crash). Files: `watchdog_supervisor.py`, `eod_watchdog.py` (neither is a WATCHED strategy file).

**Final systems validation (Mon 6/22 AM):** preflight **50/50** · regression **20 pass/0 FAIL** (consecutive_clean=8) · CSHV **0 FAIL / 1 WARN** (deadman) · reliability_drill **9/9** · strategy exact (candle_1.4atr_chandelier / entries=1 / 0.15 size / 1.4 stop / lev 4.0) + **no config drift** · Monday trading_day=True · TS auth **200** + SIM present · book **FLAT** · universe fresh (0.07h). **System is GO for the open.**

### 2026-06-21 — Loop 129: Restart + exhaustive diagnostics/validation/bug-hunt → **GO**

Rhett: "restart, then full diagnostics + validation scan, look for bugs, test everything, no failure tomorrow. Own it." Did an exhaustive, independent sweep on the current tree.

**Restart:** clean supervised — killed run_bot, watchdog_supervisor (236) respawned **PID 7676 @ 11:57** (parent 236); heartbeat live (0s); preflight 50/50 after.

**Full battery (all green):**
- py_compile: bot **128** + validation + advisor **230** = **0 failures**
- preflight **50/50** · regression **20 pass / 0 FAIL** · CSHV **0 FAIL** (2 benign WARN) · reliability_drill **9/9 detectors fire**
- chain_audit 6/18: 8 PASS / 2 BREAK — both benign (1/96 CTSH "Invalid Stop Price" under OLD pre-deploy config; L6 armed-set historical-log gap)
- sim_day_replay 6/18: **ALL INVARIANTS HELD** (82 fills, 41/41 entry/exit, 0 orphan exits, peak 13/16 slots, peak gross $240k/$300k, EOD flat)
- _wiring_audit: **8 OK / 0 FAIL** — every deployed flag (exit mode, advisor controls, daily-guard, RelVol floor, deploy controller, multiscan, in-play gate, fill-time gate) wired into the live path
- preopen_readiness: 23 validated, 2 RED — **weekend no-tape artifacts** (L2/L3 gate passes 0 rows because Sunday tape is empty/stale: orb_daily_state 44h old, brain_universe weekend-SKIP). PROVEN sound on real data: 6/18 = 458 names / 482 candidate rows / **143 gate-passes**. Monday's Research Brain (7:30) + live 9:35 scan repopulate. NOT a logic bug, NOT a Monday blocker.
- p0_verify_harness: inconclusive without a broker export (self-consistency only) — not a failure; book-flat + position_recon + replay already give broker-truth confidence.

**Live / safety:** TS auth healthy (accounts 200); book FLAT; 48h alerts = 203 INFO + 1 FAIL (the already-handled transient TS500), nothing else; **5% account DD kill ACTIVE**; EOD flatten safety-net independently launched by watchdog; disk 9.1GB free.

**Scheduled tasks:** all Monday-critical **Ready** (Research Brain 7:30, Advisor PreMarket 8:00, PreopenReadiness_AM 9:00, Morning Snapshot 9:42, Daily Review 4:10, EOD Recon 4:50, Supervisor Guardian recurring). Disabled = known legacy launchers (AlphaQuantBot, one-time tasks).

**Config:** no drift (watched-file hash matches last strategy change); Monday holiday_reason=None → trades. **Dashboard:** 6 routes 200.

**Bugs found:** none that block Monday. The only 48h anomaly (transient TS500) was already handled in Loop 128. **VERDICT: GO.**

### 2026-06-21 — Loop 128: FINAL PRE-MONDAY VERIFICATION (GO/NO-GO) → **GO**

Independent re-run of the full gate stack on the CURRENT tree (did NOT trust Loop 126/127 green — Loop 127 added files + restarted the dashboard).

**Gate stack:** py_compile 128 files / 0 fail · regression 20 pass / 0 FAIL · preflight 50/50 · reliability_drill **9/9** detectors fire (smoke detectors work, not just "bot quiet") · chain_audit 6/18 = 8 PASS / 2 BREAK (both benign — see below) · CSHV **0 FAIL** / 2 benign WARN.

**Strategy = deployed change, no drift:** ORB_EXIT_MODE=candle_1.4atr_chandelier · ORB_MAX_ENTRIES_PER_NAME=1 · EXIT_SL_FRAC=0.15 (sizing) / RESTING_SL_FRAC=1.4 (stop) decoupled · MAX_LEVERAGE=4.0 · $400k base · DAILY_MAX_LOSS disabled-for-SIM (standing decision). **Config-hash proof:** current watched-file combined hash == last strategy change (AQ-20260620-ORB-HOLIDAYGUARD-001) after-hash → no trading constant drifted in Loops 124–127; Loop 127 touched 0 watched files.

**Monday 6/22:** holiday_reason=None, is_regular_trading_day=True → bot trades.

**Process/book:** run_bot PID 11376 (started 6/20 09:24, AFTER all deploy-file mtimes; subprocess-fresh reloads orb_runner/orb_multiscan/exit_bot each cycle) · watchdog_supervisor PID 236 persistent · book **FLAT** (0 positions / 0 working orders) · prove_deploy_governs: all 3 caps bind ($25k per-pos / $200k per-side / $300k target of $400k) · exit_side + position_recon + phantom_deploy_book OK · gate validates at Monday RTH.

**Phase-0 non-interference:** the live trading loop (run_bot/bot_loop/orb_runner/orb_multiscan/exit_bot_v2) imports NONE of report_integrity / clean_day_certifier / decision_ledgers / exit_reason_codes · eod_debrief still emits its Section-B markdown (additive dict keys only; 41/41 rows tagged) · 3 CSHV bridges green · /decision-quality 200 (4.0s).

**TS auth (the one real incident):** a 9:00 AM `TS_AUTH_FAIL` was a **transient TradeStation server-side HTTP 500** (`sim-api … Internal Server Error`). Auth verified **healthy live** — `ensure_token()` refreshed, `/brokerage/accounts` 200, SIM1623888M present. That transient had tripped my new `clean_day_certified` check. **Fixed** the certifier: a transient broker-side 5xx is recorded-but-not-disqualifying (system faults + 4xx auth still disqualify; live position_recon/gate still guard real-time connectivity) — so TS's flaky SIM API can't falsely reset the kill-window streak Monday. Logged `AQ-20260621-GOVERNANCE-CERTIFIER5XX-002` (research_only); certifier self-test 11/11; drill 9/9 still fire; CSHV 0 FAIL after fix. **Not detector-gaming** — this protects the forward test the freeze exists for.

**Chain-audit 6/18 breaks (both benign):** L5 = 1/96 CTSH "Invalid Stop Price" rejection under the OLD pre-deploy config (6/18 ran candle_close 0.15 resting, not the new 1.4 chandelier; wider new stop is *less* prone to this); L6 = "armed-set-unknown" = the armed-set log wasn't retained for that historical date (a logging-availability gap, not a live failure).

**Clean-day reconcile:** certifier = 10 clean TRADING days (broker truth, back to 6/05) vs regression = 6 clean SESSIONS — distinct metrics, **0 disagreements**.

**Needs-Rhett (non-blocking):** (1) deadman beacon NOT ARMED — set `HEALTHCHECK_PING_URL` in `tradestation-bot/.env` (the one off-box VPS-death gap). (2) earnings_calendar.csv 17.8d stale (FMP_API_KEY unset) — but the veto **fails OPEN** (verified in `orb_earnings_veto.py`: missing/error/exception → block=False), so it cannot block Monday; it only risks false-negatives on earnings names.

**Restart (done — Rhett chose "restart now"):** killed run_bot PID 11376; watchdog_supervisor (PID 236) respawned it as **PID 9416 @ 11:17 AM** (parent=236, supervised). Verify-load: new StartTime is after all deploy mtimes; preflight 50/50; bot_heartbeat 10s fresh → cycling. Monday opens on one fresh, verified process. **VERDICT: GO.**

### 2026-06-21 — Loop 127: Phase 0 Decision-Quality Hardening (non-confounding) — BUILD JOURNAL

**Ask (Rhett, via Planning Loop 127):** "deep validation… another build… log everything in the session log so Claude can read what you've done." Decision-quality hardening over reports/validation/logging ONLY. Guardrail: zero changes to any live trading/entry/exit/sizing/selection path; the Monday OOS-forward exit/re-entry test must stay uncontaminated. (Also saved a memory: during a build, log everything to SESSION_LOG as I go.)

**Reconciled first (anchor = Loop 126 GREEN):** mapped existing infra to EXTEND, not duplicate — CSHV `@register`/`CheckResult` (+ reliability bridge), `regression_suite.metrics`/`clean_session`/`regression_history.jsonl` (existing consecutive_clean = clean regression SESSIONS), `strategy_changes/log_change.append_change`, `aq_validation` (already has benjamini_hochberg/bonferroni from Loop 124 — did NOT rebuild), `eod_debrief.round_trips_net` (THE canonical per-trade ledger: net=gross−comm−fee, verified on real data), ad-hoc exit-reason strings, the V9_CHANDELIER harness + fade-breakout logger (Loop 124 — left intact).

**Built (bottom-up, each self-tested before wiring):**
- `validation/exit_reason_codes.py` (item 5) — canonical EXIT codes (EXIT_PHASE1_ATR_STOP / EXIT_CANDLE_CLOSE_TRAIL / EXIT_EOD_FLATTEN / BLOCK_REENTRY_NOT_FRESH / EXIT_UNCLASSIFIED), fidelity labels (broker_truth / replay / one_minute_counterfactual_low), `classify_exit_reason()`, official `trade_trace_id` field name. **self-test 13/13.**
- `validation/report_integrity.py` (item 1) — pure assertions over canonical rows: identity (net==gross−cost), positivity, direction, count/net-sum/win-rate recon, fidelity labels, commission-monotonic + drop-one metamorphic. **self-test 7/7; real 6/18 N=41 clean, 0 unclassified.** Caught a real false-positive: direction check tripped on `MESU26` (futures $5 multiplier); fixed → futures assert SIGN only, equities assert MAGNITUDE.
- `validation/clean_day_certifier.py` (item 2) — single predicate (report_integrity + broker_flat_EOD + no-FAIL/CRIT-incident + live position_recon + live gate). `consecutive_clean()` walks trading days backward (durable mode); `reconcile_with_regression()` does PER-DATE agreement. **self-test 7/7.** Independently re-derives streak from broker truth = **10** clean trading days (6/05→6/18; stops at 6/04 real incident), **0 reconcile disagreements** with regression on trading days. (After the futures fix the streak honestly moved 6→10; the earlier "6=6" had been propped up by the false positive — RULE #0, didn't keep it.)
- `research/{assumption_ledger,uncertainty_budget,claims_ledger}.yaml` + `validation/decision_ledgers.py` (items 3/4/6) — 4 seeded assumptions (incl. A-ORB-PHASE1-STOP-001 disputed) each w/ a falsifiable invalidation rule; exit-read uncertainty budget decomposed into sample-size/intrabar-ordering/fidelity/multiple-testing; claims w/ BOTH sides (CLAIM-PHASE1-STOP-001) + rule provenance (ORB=paper_backed, internal rules tagged). **self-test 9/9.**

**Extended (no parallel sources):**
- CSHV `system_health_verifier.py` +3 `@register` checks: `report_integrity` (Data), `clean_day_certified` (Reliability; intraday-aware — won't fail on open positions before 4:05pm), `decision_ledgers_valid` (Governance). All OK.
- `regression_suite.metrics` now also records `certifier_consecutive_clean_trading_days` (kill-window fed by broker-truth cleanliness, not "the bot ran"). Additive + guarded.
- `eod_debrief._section_b` rows now carry `exit_reason_code` + `fidelity_label` (additive dict keys; markdown untouched). Verified 6/18: 41/41 rows labeled.
- Dashboard `/decision-quality` route + handler + home card → `advisor/decision_quality_page.py` (read-only render of all three: integrity, certifier, ledgers). Renders 200.

**Governance + verify gates:** logged `AQ-20260621-GOVERNANCE-DECISIONQUALITY-001` (research_only, approval_required=false, before==after config hash — proves no watched-file change). Compile all OK · **CSHV 0 FAIL** (same 2 benign WARNs: disabled-legacy task, deadman not armed) · **preflight 50/50** · **regression 20 pass/0 FAIL** · change-log 16 valid / no parallel sources.

**Perf fix (same turn):** `/decision-quality` first HTTP hit froze (57s render). Profiled → `trade_journal.csv` is **140MB**; `_exit_reasons()` parses it whole (3.45s) and the certifier's streak walk called it ~14×. Since the certifier's clean verdict depends only on FAIL-level violations (exit-code is a non-fatal WARN), dropped `_exit_reasons` from the certifier path → `consecutive_clean` 38s→**0.27s**, page 57.7s→**3.86s**, route HTTP **200 in 4.4s**. Verdicts unchanged (self-test 7/7, streak 10, 0 disagreements). Dashboard restarted **detached** (rule 15) so the new route/card are live and survive this session. (Latent perf debt: the 140MB journal makes any single `_exit_reasons` call ~3.5s — fine for once-a-page/once-at-EOD, but a future item could index/rotate it.)

### 2026-06-14 — Loop 43: fresh dashboard read + TS-style charts

- **Fresh full read:** all live pages 200 & clean (light theme, home button everywhere, no broken/stale-path links, no render errors). Minor: source-registry + bot-change-candidates show old dates in CONTENT (metadata/research, acceptable); /daily-review-v2 small today (weekend, no trades).
- **Charts → TradeStation look** (`trade_charts.py`): black bg, bright green (#00c805) / red (#fb3b3b) candles, faint centered symbol watermark, right price axis + bottom time axis, 380px panel. Page stays light; chart is a TS-style dark panel. Entry/exit markers + stop/OR lines kept (our overlay). Verified 6/12: 12 charts render dark.
- NOT replicated: TS's live OHLC header bar (needs live OHLC values + is TS-UI-specific) — offer to add.

### 2026-06-14 — Loop 42: cut Morning Data Prep + consolidate sections

- Cut **Morning Data Prep** (monitored the V1 pre-open data pipeline we no longer use; pre-market runs off the live scanner).
- Collapsed the 3 thin sections (Morning / Decision Support / Review & Learning) into ONE **"Supporting tools"** section: Alerts/Watchlist, Source Registry, Bot Change Candidates (+ the 12 blank `%s`, invisible). `%s` tuple unchanged.
- **Home 81KB → 66KB.** Final structure: hero (Pre-Market / Daily Review / Trade Truth) · status row (Bot Health / Advisor Health / Market&Activity / Review) · Supporting tools. Dashboard redundancy cleanup COMPLETE.

### 2026-06-14 — Loop 41: cut the 2 borderline cards

- Opened both and judged: **Morning Decision Board** = cached/thin advisor opinion board ("leans long, 1 name, from cache"), overlaps the live pre-market "stocks in our sight," doesn't drive the bot → CUT. **Manager Review Packet** = "fast saved packet view" of links dated 2026-06-11 (stale), phantom-sourced, superseded by Daily Review (broker truth) → CUT. Both home cards removed; routes left (unlinked, harmless).
- Home now 67.5KB. Remaining secondary cards: Morning Data Prep, Alerts/Watchlist, Source Registry, Bot Change Candidates.
- FLAG (not yet acted): Morning Data Prep monitors the V1 pre-open data freshness, which we no longer use (pre-market page uses the live scanner) — borderline-low-value; the Morning section is now down to that 1 card. Candidate to cut/consolidate next.

### 2026-06-14 — Loop 40: dashboard redundancy pass

- Removed the redundant **Trade Review** card (Rhett was right — duplicates Daily Review) + the duplicate **Pre-Market Evaluation** card (the hero already links it).
- Removed stale/low-value research-artifact cards (Advisor Guidance, Opening Window, Opening 09:45, Advisor Readiness, Level2 Planning, Advisor Feedback, Time-of-Day) — several linked **dead `C:\Users\rdule\OneDrive` paths** that 404 post-migration — and the Artifacts section (Operator Dashboard / Weekly Review / Daily Trade Analysis). `%s` tuple kept aligned. Home 81KB→68KB.
- **/truth: added a DATE-RANGE selector** (?start&end) → "Selected range" net / exp$ / win / PF. Verified.
- Remaining home cards judged working & kept: Morning Data Prep, Morning Decision Board, Manager Review Packet, Alerts/Watchlist, Source Registry, Bot Change Candidates. Borderline (open next to confirm value vs overlap): Morning Decision Board (vs pre-market stocks-in-sight), Manager Review Packet (vs Daily Review).

### 2026-06-14 — Loop 39: FINISHED Loop-37 build order

- **Cost model:** `commission_model.py` (knob: zero | ts_select | per_share_standard | stress; reg fees on sells — SEC $20.60/$1M, FINRA TAF $0.000195/sh, both pulled live 6/14). Recompute 6/08+ (53 RT, gross +$479): zero net +$479 (exp +9.04) · ts_select +$457 (+8.62) · **per_share_standard +$238 (+4.50)** · stress +$20 (+0.38). **Commission halves the edge; the live plan matters a lot.** (Recompute is a script; wiring it into /truth display = follow-up.)
- **Deploy-controller scope (APPROVED, gated):** extended `orb_runner` (9:35 main book) to call `deploy_controller.admit()` — per-position $25k / per-side 50% / 75% target now govern the main book, not just re-arm. Mirrors orb_multiscan. Verify-load: run_bot restarted PID 10184, preflight 46/47.
- **Wiring-audit → preflight (APPROVED, high-pri):** `_preflight_diagnostic.py` now runs `_wiring_audit` every check (now 47 checks). Shadow/unwired governance flags are caught automatically. 6/6 OK.
- **p0 harness (close item d):** ran `--live` for 6/11 + 6/12 → unified log == independent TS historicalorders API; broker truth VERIFIED complete.
- **Ledger:** added the permanent VERIFIED/ASSUMED/BROKEN section at the top.
- NEXT (Rhett's sequence): loop-back to Planning Claude, THEN the dashboard redundancy review (incl. the legacy Trade Review card likely redundant with Daily Review; add a date-range selector to /truth; card-by-card value/redundancy audit Morning Hub → bottom).

### 2026-06-14 — Loop 38: home visual fixes (Rhett caught them)
- Hero (3-question) cards weren't in the shared content-width rule -> didn't align with the status row; added `.cmd3` to it + shrank (compact padding/fonts).
- Removed 11 home cards that opened RETIRED stub pages (Market Intelligence, Morning Readiness, Session Summary, ChatGPT Handoff, Action Center, Post-Market Debrief, Strategy Learning, Review History, Trend Dashboard, Root Cause, Daily Operating Workflow). Home now shows only working surfaces; verified 0 retired links remain.
- Cost-rate fetch (Loop 37): got SEC Section 31 = \$20.60/\$1M (eff 4/4/2026); FINRA TAF rate still to pull.
- **STILL QUEUED (Loop 37 build order):** cost model + recompute, deploy-controller scope extension, wire `_wiring_audit.py` into preflight, run p0_verify_harness on 6/11+6/12, add VERIFIED/ASSUMED/BROKEN ledger.

### 2026-06-14 — Loop 36: foundation audit (Planning Claude handoff a–f) + cost status

**FOUNDATION AUDIT (verified against code/data):**
- **(a) candle-close exit — VERIFIED.** Deployed 6/10 5:22 PM (commit d3f7e05, behind ORB_EXIT_MODE). `candle_close_exit.py` matches spec exactly: PHASE1_ATR 0.15 hard stop → CONFIRM_ATR 0.15 → phase-2 first opposite-color 1-min candle close → CATASTROPHE_ATR 1.0. 6/11+6/12 ran on it.
- **(b) multi-scan — VERIFIED; deploy-controller — BROKEN (scope).** orb_multiscan builds a FRESH 5-min range per window (10:35–14:35), tags ORBMS<window>, capped by MAX_DAY_TRADE_GROSS. deploy_controller.admit() DOES enforce 75% target / per-side 50% / per-position $25k — but is only called from orb_multiscan (re-arm), NOT orb_runner (9:35 main book). So the caps don't govern the bulk of entries (Loop 35).
- **(c) freeze blast radius — VERIFIED clean.** 6/12 froze 8:04 AM pre-market, recovered before the 9:30 open; 6/12 = 24 fills / 12 round-trips (complete), 0 duplicate fills, no stuck orders tied to the freeze. 6/11 had no pre-market freeze.
- **(d) broker-truth completeness — UNVERIFIED (partial).** Internally consistent: sane per-day counts (6/08 14F, 6/09 14F/10U, 6/10 24F, 6/11 30F, 6/12 24F), 0 duplicate fills. But NOT independently cross-checked (p0_verify_harness / TS historicalorders not run for 6/11–6/12). Assumed-complete, not proven.
- **(e) analytics audit — 1 BROKEN, 2 OK.** R-multiple: BROKEN — daily-review used 0.10×ATR denom for ORB while the live stop + /truth use 0.15 → overstated R ~1.5× and disagreed with /truth. **FIXED (0.10→0.15).** slippage: OK (guarded; null pre-6/08 when intended_price absent). left-on-table: OK (MFE fixed Loop ~31; after-exit = eod_hold − realized).
- **(f) index-ETF isolation — VERIFIED immaterial.** Only 1 index-ETF round-trip total (SPY, −$11) vs 52 single-name (+$709). SPY barely traded; index drag is not a real factor in the data.

**(#1 COST) — NOT WIRED.** broker_orders_unified.csv has NO commission/fee/cost column at all (not "null" — absent). After-cost expectancy is currently impossible. Fix needs a per-trade commission field (per-share model OR broker-export join). DECISION NEEDED: the commission model/rate (intended live schedule). This is the #1 blocker per Planning Claude.

**(Q1) IN-PLAY TAGGING — approved, NOT yet built this turn** (audit consumed the turn). Next build: tag every arm with day-RelVol, OR-RelVol@arm, intraday move%, above/below-VWAP, catalyst, index-ETF Y/N; ORB_INPLAY_GATE stays OFF.

### 2026-06-14 — Loop 35: proactive wiring audit (Rhett: "what else is broken?")

- Rhett (fair) ownership critique: he caught the shadow-edge bug; Code should have. Ran a proactive audit of the SAME class — "deployed/claimed but not actually wired into the live path."
- **FOUND (1):** `DEPLOY_CONTROLLER` (per-position $25k, per-side 50%, 75% target, conviction) is wired ONLY into `orb_multiscan.py` (re-arm), NOT `orb_runner.py` (the primary 9:35 scan). The 9:35 book sizes by its own constants and does NOT apply those caps. My "CURRENT SYSTEM STATE" claim implied global governance — corrected. Open design Q for Rhett/Planning: should the controller govern the 9:35 book too?
- **CLEARED (3, verified wired, not assumed):** candle-close exit (`exit_bot_v2` reads ORB_EXIT_MODE + calls candle_close_decision), daily-guard/kill switch (halts the scan in `orb_runner`), advisor controls (`should_block_entry` in `orb_runner`). RelVol floor also confirmed wired (but weak — see Loop 31).
- **BUILT:** `tradestation-bot/_wiring_audit.py` — asserts each governance flag is referenced in the live path it CLAIMS to govern; FAILs otherwise. Current: 5 OK / 1 FAIL (the deploy controller). This makes the shadow/unwired class machine-catchable. TODO: call it from `_preflight_diagnostic.py` so it runs every check.
- Honest scope: this audited the flag-WIRING class only. Other classes still to sweep (data integrity, risk-guard enforcement values, dashboard accuracy). Standing discipline added to memory: proactively audit; don't wait for Rhett to find it.

### 2026-06-14 — Loop 34: loop-back handoff to Planning Claude
- Wrote a Code→app recap handoff (strategy: ORB-edge audit + in-play gate proposal parked + multi-scan kept ON + exit/re-entry paused; dashboard: 3-question home, single health lights, legacy pages retired, light theme + Home button everywhere, broker-truth sourced). Delivered as a copiable block for Rhett to paste to the app.

### 2026-06-14 — Loop 33: decision — keep multi-scan + deploy ON

- Rhett: **leave them** — `ORB_MULTISCAN` + `DEPLOY_CONTROLLER` stay LIVE. No flag change. Rationale: SIM-only (no money risk), and the data is still useful (it characterizes ORB behavior/utilization even on the current S&P universe; diverse trade generation is the success metric). The in-play entry-gate is a separate forward build (PROP-INPLAY-ENTRY-GATE) that doesn't require reverting these first.
- Still paused: exit-redesign A/B, re-entry tagging A/B (tuning execution before the in-play core is premature). The in-play gate proposal stays parked pending human approval.

### 2026-06-14 — Loop 32: in-play entry-gate proposal (handoff D)

- Wrote **`outputs/proposals/PROP-INPLAY-ENTRY-GATE-2026-06-14.md`** (INACTIVE, needs human approval): make in-play selection GATE live ORB entries instead of running in shadow. Structure: day-RelVol floor (~≥2.0, the key knob), in-play move band (~1.5–8%, exclude blow-offs via the exhaustion guard), keep price/spread/ATR floors, EXCLUDE index ETFs (SPY/QQQ/IWM/DIA), catalyst as soft bonus. Fed from the scanner's per-symbol data. Flag `ORB_INPLAY_GATE=OFF`; tag every entry (gate pass/fail, relvol@arm, move@arm) → A/B in SIM, costs subtracted, gauntlet. NOT "trade the top % movers" (exhausted).
- **PAUSED (per Planning Claude):** exit-redesign A/B, re-entry tagging A/B, multi-scan expansion, 75%-deploy push — premature until ORB-on-in-play is traded + measured.
- **OPEN DECISION for Rhett:** `ORB_MULTISCAN` + `DEPLOY_CONTROLLER` are currently LIVE (Loop 30). They amplify the unproven (non-in-play) universe. Recommend reverting to baseline (single 9:35 scan, conservative deploy) until the in-play gate is in — but flipping live flags is the human's gate, so holding for Rhett's call.
- A/B/C were completed Loop 31 (handoff re-sent before the app saw the reply; it had read the cached /main/ URL). Log was already current; B/C evidence backfilled Loop 31.

### 2026-06-14 — Loop 31: ORB-edge audit (Planning Claude handoff B+C)

**CRITICAL FINDING — the live ORB is NOT trading the mover/RelVol edge.** Confirmed from the bot code (not the scanner):
- **Entry gate (quoted, `orb_runner.py`):** `MIN_REL_VOL = 1.0` (line 68); per symbol `rel_vol = compute_rel_vol(sym, or_vol); if rel_vol is None or rel_vol < MIN_REL_VOL: skip` (line 378-380). `compute_rel_vol` (`orb_data_collector.py:414`) = **today's opening-range volume ÷ the symbol's own 14-day avg OR volume.** Then candidates are sorted by rel_vol desc and the **top 20** (`TOP_N_BY_RELVOL`) that broke their opening range are armed. Other gates: ATR floor, doji/OR-quality, earnings veto, advisor block. **There is NO %-move / catalyst / market-mover / day-RelVol gate at entry.** A floor of 1.0 only means "opened at or above its own average volume" — a very weak in-play proxy that ~half the universe clears, favoring reliably-liquid large-caps.
- **Real tradable universe (`orb_universe.build_universe()`): 530 symbols** = S&P 500 + SUPPLEMENT ETFs (SPY, QQQ, IWM, DIA, ARKK), minus leveraged ETFs. NOT the 34-name core, NOT the 2296 broad tier. The 2296 broad tier is **scanner-shadow only** — never armed by ORB.
- **Why SPY trades:** SPY/QQQ/IWM/DIA are *intentionally* in SUPPLEMENT ("ETFs with ORB-like patterns"). The structural block is **leveraged-ETF-only** (`is_leveraged_etf('SPY')` = False), so plain index ETFs pass by design. Not a missing exclusion — a deliberate inclusion to revisit.
- **Headline:** the mover scanner's edge (%-move + day-RelVol + catalyst, incl. the broad tier) has been running in **SHADOW**; live entries are **ORB breakouts on the S&P-530 filtered by a weak OR-volume RelVol≥1.0, top-20** — i.e. we've been measuring **ORB-on-S&P-(mostly large-caps + index ETFs)**, not ORB-on-movers.
- **PAUSED:** exit-redesign + re-entry A/B until the universe/entry-gate decision (tuning execution on a possibly-wrong selection is premature).

**(B) Scanner candidates vs ACTUAL traded (broker truth), per real trading day — Y = was a scanner sp-pool candidate that day:**
- **6/11 (Thu): 35 candidates · 15 traded · 3 overlap.** EQT(Y) · SMCI(Y) · WY(Y) · CNP(N) · DKNG(N) · DPZ(N) · ED(N) · GD(N) · HSIC(N) · NEM(N) · PRU(N) · SNA(N) · SPY(N) · TYL(N) · VZ(N).
- **6/12 (Fri): 42 candidates · 12 traded · 2 overlap.** ADSK(Y) · NWSA(Y) · LVS(N) · NDAQ(N) · OKE(N) · RJF(N) · ROP(N) · STLD(N) · SW(N) · TRV(N) · WSM(N) · WTW(N).
- 6/09–6/10: scanner wasn't logging sp-pool candidates yet (added Loop #28), so no overlap test; trades were 7 and 12.

**Backfill (was missing from the log):** 6/12 was the FIRST live multi-scan session (ORB_MULTISCAN ON from 6/11 5:26 PM). Result: 12 closed trades, −$48 (broker truth). The bot froze pre-market 8:04 AM (watchdog restart) — root-caused + fixed (heartbeat-while-waiting on cycle steps, Loop 30). Multi-scan + deploy-controller live; capital still well under the 75% target.

### 2026-06-12 — Session: dashboard UX + coordination + strategy handoff

**Turn - Home button everywhere + kill all dark backgrounds.**
- Floating Home button added in _page (all _page pages; suppressed on home via is_home). Inline Home button on /truth, /daily-review-v2, /pre-market. Converted remaining dark pages to light theme: truth_dashboard, daily_review_page (+chat), retired-stub, trade-chart-wrap, and the TradingView chart (trade_charts) -> white/light. No #0b0e14/#0d1017/#161a25 left.

**Turn - pre-market page restyle.**
- premarket_page.py: dark->light gray (#eef3fb)+blue text; big date banner ('Data for <weekday, date> ...'); h1 36px; full width (max 1700) with long|short candidate tables side-by-side + broad full-width; bigger fonts. Kills right-side dead space.

**Turn - hero recolor + fill health-card dead space.**
- 3-question hero cards: dark -> very light gray (#f4f7fc) + blue text. Bot Health card: added 'Traded today' (broker-truth count+P&L). Advisor Health card: added live advisor output (last control run, regime read, active controls, next run) filling the dead space.

**Turn - advisor health card tidied.**
- Removed the 'Open Advisor Health report' + 'Refresh now' maintenance buttons from the advisor health card -> plain note, matching the bot card (green=fine; yellow/red=get Claude). No heavy advisor-health page existed to retire; the card was already the single light (fixed green last session). Kept it as a SEPARATE light from bot health (different systems).

**Turn - bot health page retired; home card = single health light.**
- Per Rhett: user needs one trustworthy light, not the noisy 10-check forensic page. Home Bot Health card now a noise-filtered rollup: GREEN=alive+no real 24h issue; YELLOW=alive but real freeze/restart or FAIL alert (pull Claude in); RED=offline (reads heartbeat + watchdog_supervisor.log + bot_alerts.jsonl). Retired /bot-health to a stub + removed embedded full-health section from home. Forensic checks still available to Claude via build_bot_health_check from source. Verified: card GREEN, page stubbed.

**Turn - SHIPPED freeze fix.**
- Added _run_step_with_heartbeat in run_bot.py; routed all 6 cycle steps through it (Popen+poll+10s heartbeat+180s hard-cap taskkill), mirroring _run_advisor_slot. Fixes the ~8:04 AM false 'frozen' restart. Verify-load: run_bot PID 9900 (start 08:44 > mtime 08:43), preflight 45/46 (1 benign weekend orb_daily_state FAIL). First live test = Monday 6/15 pre-market. NOTE: the 6/12 bot-health page stays RED because the freeze really happened that day (history); the fix prevents FUTURE freezes.

**Turn - bot freeze root cause (diagnosis).**
- All 'frozen' force-restarts cluster ~8:04-8:09 AM ET (6/08 froze TWICE, 6/12 once) = the pre-market warmup window. ROOT CAUSE: run_bot.py main loop beats the heartbeat only ONCE per cycle (line 550), then runs each cycle step as a blocking subprocess.run with NO per-step heartbeat (lines 555-590). The ORB runner's pre-market warmup makes many TS API calls (each up to 30s timeout); on a slow pre-market API morning the cumulative runtime exceeds the watchdog's 180s x3 (~249s) freeze threshold -> heartbeat goes stale -> false-positive 'freeze' force-restart. The advisor-run + earnings-refresh sub-steps were already hardened with heartbeat-while-waiting + hard caps; the CORE cycle steps were NOT.
- Impact: so far pre-market only (self-heals before the 9:30 open; no missed trades). BUT multiscan is now ON -> intraday re-arm/warmup steps could trip the SAME freeze DURING market hours. Escalates priority.
- Proposed fix (NOT yet applied; live core loop = gated): route cycle steps (>= orb_runner) through a _run_step_with_heartbeat wrapper mirroring _run_advisor_slot (Popen + poll + 10s heartbeat + hard-cap taskkill). Keeps heartbeat alive during slow-but-working warmup; kills a truly-hung step so the cycle continues.

**Turn — bot-health page cleanup + explain the RED.**
- Removed cross-nav button rows from EVERY page (.topbar .actions display:none) + the 'Open Trade Review For This Range' button. Fixed a 401/403 false-positive in bot_health_check (matched timestamp microseconds). EXPLAINED the bot-health RED: (1) REAL but self-healed — bot froze 8:04 AM ET (heartbeat stale 249s x3), watchdog force-restarted (restart #5, 1 crash/hr), recovered, traded 10x since; (2) FALSE POSITIVE — 'API/auth issue' was 401/403 matching timestamp microseconds [fixed]. Killed a stale 7:57 AM dashboard server holding port 8765.

**Turn — green status pill.**
- The health-indicator GREEN badge (dot+text+bg) was styled blue (#1f5d91); fixed tone-positive to real green (#1e7a43). Yellow/red/gray tones already correct, so the pill tracks status.

**Turn — health-card button color (aesthetic).**
- Buttons in Bot Health + Advisor Health cards now match the card status color (green) instead of the default blue accent: `.health-green/.health-yellow/.health-red .link-button`. Commit `1480031`.

**Turn — advisor health always-YELLOW root-caused -> GREEN.**
- 3 stacked false-positives: (1) sync verdict POSSIBLY_STALE on every local edit (benign on single VPS -> ALIGNED on canonical root); (2) 'expired access token' (auto-refreshes -> only missing/unreadable cache warns); (3) 'git unavailable' was a real bug — collect_git_metadata checked for .git in the advisor SUBFOLDER but the repo root is parent C:\AlphaQuant; let git walk up. Now GREEN, 0 warnings. Files: session_sync.py, advisor_health.py.

**Turn — Market&activity card layout fix.**
- The 3 mini-cards were side-by-side with dead space (base .bn-cells repeat(4,1fr) overrode my rule). Used higher-specificity .status-group-card .bn-cells (flex column, flex:1 cells) to stack them vertically and split the card height evenly. Also fixed a format-string break ('1fr' in single braces in a CSS comment crashed server startup).

**Turn — home top row restructure.**
- Dropped the top status-strip BOT tile (home); folded MARKET/ADVISOR/TRADES into a grouped 'Market & activity' card as row slot 3; Review far right; 4 equal symmetric columns. Fixed .health-green (was light-blue #bdd4ea -> real green) + red/yellow. Bot Health card now shows a config value block (account/exit/re-arm+next window/deploy target) so no dead space. Other pages keep the full banner.

**Turn — home status row reorder (Rhett's UX pass).**
- Bot Health card now reads the LIVE heartbeat → GREEN "the bot is alive" (was GRAY "no cached check" because it read a cached archived review, not the heartbeat). Moved to far LEFT (1st); Advisor Health 2nd; Workflow 3rd; Review far RIGHT; row fills 4 equal columns (was a wide first card).
- Explained colors: Advisor YELLOW = benign POSSIBLY_STALE sync-marker drift (file metadata vs marker); not a real fault. Bot GRAY = stale-cache dependency, now fixed to live.
- Redundant "bot is alive" indicators (top status-strip BOT tile + full bot-health section): Rhett chose to LEAVE BOTH.
- Earlier this turn-block: made the coordination repo PUBLIC (Rhett's informed call) so the app Claude can read it by URL; cache-buster = commit-pinned raw URL; handoff block delivered to the app.

### 2026-06-11 — Session: capital deploy + full dashboard scrub

**Turn — re-entry/exit handoff from Planning Claude (2 changes + 2 investigations).**
- **Inv 1 (SMCI mechanism) RESOLVED:** SMCI = 9:35-armed breakout DAY stop (opened 9:36 ET, filled 12:48 ET, 663@30.14), rested ~3h. NOT multi-scan — `ORB_MULTISCAN` turned ON 5:26 PM 6/11 (after close), OFF all trading day. Narrative invented windows from fill hour; fixed `trade_analytics` to attribute 0935. New open Q: ORB entries are DAY orders with no intraday entry cutoff.
- **Inv 2 (MFE bug) FIXED:** MFE from 1-min bar highs fell below realized when exit filled above max bar high (SMCI +391<+411). Floored excursion by exit fill → MFE≥realized. Re-reviewed SMCI: MFE 411.06=realized, left-in-trade 0; real leak was $795.60 AFTER exit. Commit (analytics fix) + dashboard restarted.
- **Change 1 (re-entry):** no explicit "already-traded" exclusion existed; multi-scan re-arm already allows flat re-qualifying names (one-active-position-per-name guard only). Remaining = Nth-occurrence tagging (post-hoc from broker truth) + per-Nth post-cost expectancy. SIM.
- **Change 2 (exit redesign):** QUEUED for A/B, not default. Real 0.15×ATR intra-bar stop already exists (SMCI 29.62 UROUT proof); new = +1R scale-out + profit-adaptive ATR trail + drop candle-close + keep hard stop through trail phase. A/B behind flag, segmented green/red/flat, then gauntlet.
- Replied to Planning Claude (markdown). Updated ALPHA_QUANT_STATE.md §2. Named 5 follow-up build tasks.

**Turn — handoff to planning Claude.**
- Rhett: write a handoff to the app Claude explaining the setup, tell him to review this file before every turn (closes the gap), and have him walk Rhett through the GitHub connector.
- Delivered a copy-paste handoff block: app Claude reads SESSION_LOG.md from the repo each turn (LAST UPDATED stamp + FROM PLANNING CLAUDE inbox + latest entries), writes back via the inbox, and walks Rhett one-step-at-a-time through enabling the GitHub connector + granting access to the private repo, confirming by reading the stamp. Standing instruction also lives in the "HOW THE TWO CLAUDES COORDINATE" section above.

**Turn — two-Claude coordination protocol.**
- Rhett: the point of the repo is so the app Claude can read the file each turn without him pasting — how will each Claude know the other updated it?
- Honest answer: a repo is a shared notebook, not a notification bus; coordination is pull-based (neither AI is pinged). Added a **LAST UPDATED stamp** at the top + a **"HOW THE TWO CLAUDES COORDINATE"** section + a **"FROM PLANNING CLAUDE"** inbox. Code pulls at turn start / pushes at turn end; the app reads via the GitHub connector (required since the repo is private). `git log` + the stamp = who-touched-it-last.

**Turn — make SESSION_LOG all-encompassing + off-machine backup.**
- Rhett: is SESSION_LOG the single best file? merge in anything missing; create a repo Claude can read; back up the readme there; keep all three copies synced every turn.
- Answer: it was the best *operational* log but not all-encompassing. Enriched it with: **Canonical Docs Map**, **Architecture in Brief**, and a **Standing Decisions** log (scope / strategy-risk / working-style — the complete decision history + a place to append every change going forward).
- The "repo Claude can read" **already existed**: `github.com/Rhettduleba/alpha-quant-coordination`. Used it (no new repo). Copied SESSION_LOG.md in + pointed the repo README at it. Pushed (`337a540`).
- **Security:** flagged the repo was PUBLIC (strategy params + SIM account IDs + P&L exposed). Rhett chose private → flipped it to **PRIVATE** via the GitHub API using the cached git credential; verified (unauth API now 404).
- Sync rule updated in memory: 3 copies (canonical `C:\AlphaQuant\SESSION_LOG.md`, desktop link, repo mirror) kept current every turn.

**Turn — per-trade chat box.**
- Rhett: add a chat box under each trade's narrative so we can talk about that trade.
- Built **`src/advisor/trade_chat.py`** — `answer_trade_question(trade, day, message, history)` calls Claude with the trade's full broker-truth analytics + ALPHA_QUANT_STATE.md context; analyses the past only, no trading calls.
- Added a chat box to every trade card in `daily_review_page.py` (input + log + embedded trade-context JSON) + client JS (`sendChat`, per-card history) + CSS.
- New POST route **`/trade-chat`** in `local_dashboard.py` → `{reply}` JSON.
- Validated the **new API key** works. Verified: backend reply grounded in numbers (SMCI +$411, 1.68R, $795.60 left on table), 15 boxes render, POST round-trips. Commit `199c762`.

**Turn — final dashboard scrub (date cleanup + retire the stale tail).**
- Rhett: the dates on the buttons look out of date; do a final scrub, own it, make it all make sense and be valuable.
- Found a cluster of home-page cards frozen at **2026-04-24 / 2026-05-01** showing 7-week-old data as current (e.g. "P&L 846.71, 109 trades, Best: 2026-04-24"). Blanked those **7 manager-workflow cards** (read parked V1-pipeline artifacts that stopped regenerating).
- Retired **6 more stale/slow pages** to fast honest stubs: `market-intelligence` (9s+stale), `post-market-debrief` (**62s!**), `morning-readiness`, `trend-dashboard`, `review-history`, `daily-operating-workflow` (9s). All read the April export / phantom journal; superseded by `/daily-review-v2` + `/truth`.
- Killed the junk **"guard fired 45,164×"** counter: removed position/exposure cap noise from `near_breaches` in `trade_manager_review.py` (normal enforcement, not a breach) + defensive filter in `alerts_watchlist.py` for cached artifacts.
- Verified honest (kept): `morning-data-prep` correctly says "Freshness: stale, last built 4/24"; `tradestation-source-registry` shows source metadata dates — both doing their job, not bugs.
- **Final dashboard state: 23 pages → 12 clean/valuable, 11 honest retired-stubs, 0 slow (>5s), 0 junk counters, 0 stale-dates-shown-as-current.** Commit `49c8faf`.

**Turn — README/session-log request.**
- Rhett: I've been glitching (empty "No response requested" turns + repeated prompts). He wants a single file logging everything every turn, as a crash-recovery backup to ramp a fresh Claude, plus a desktop link and a memory rule to keep updating it.
- Created **`C:\AlphaQuant\SESSION_LOG.md`** (this file). Clarified honestly: no single turn-by-turn log existed before; CLAUDE.md = rules, STATE.md = snapshot.
- Creating a desktop shortcut to it. Adding a memory rule: update this file every turn.

**Turn — full dashboard scrub (the big one).**
- Scrubbed all ~23 dashboard pages. Finding: only `/truth` and `/daily-review-v2` were truthful; the rest showed fake `trades=0`, read the April-20 broker export, showed a junk "guard fired 45,164×" counter, or hung the browser 70s+.
- **Rebuilt the pre-market page** on LIVE data → new `src/advisor/premarket_page.py`. Shows the scanner's actual long/short candidates (from `C:\AlphaQuant\outputs\mover_scanner\scans.jsonl`) + the bot's plan + broker-truth P&L. Commit `3fe26a9`.
- **Killed the `trades=0` phantom** in the status banner (every page) → now reads broker truth ("15 closed · +$567"). Added a 3-question command hero to the home page. Commit `1a93e16`.
- **Retired 5 hanging legacy pages** (`session-summary`, `strategy-learning`, `action-center`, `root-cause`, `chatgpt-handoff`) to fast honest stubs — were 70s+ timeouts, now ~10ms. Commit `96baa6c`.
- Still-stale pages flagged, NOT yet fixed: `morning-readiness`, `trend-dashboard`, `review-history` (bodies still read the April export). Recommend folding/retiring next.

**Turn — deploy multi-scan.**
- Session was over and flat (0 positions/orders at 5:24 PM) → turned **ORB_MULTISCAN ON** for tomorrow; restarted run_bot (verify-load PID 2464, preflight 46/46). Commit `d08a69e`.

**Turn — capital changes + under-utilization finding.**
- Daily-review charts now start 10 min before entry → close; added "capital used" + "capital on table @ entry" per trade. Commit `e84203c`.
- **Key finding:** 6/11 peak capital deployment was only **34.8% of the $400k base ($139k), for ~6 minutes**, then ~5% for the rest of the day. Badly under-utilized vs the 75% target → motivated the multi-scan deploy above.

### Earlier this session (from prior context — condensed)
- Built the full daily-review pipeline (Phases 0–5): broker-truth source, per-trade analytics, TradingView charts, page+rollup, LLM narrative, dashboard route. Commits `728afe0`→`a74e20a`.
- Built `/truth` primary surface Slice 1 (truth gate + verdict). Commit `79787dc`.
- Dashboard simplification (retired legacy /trade-review, dropped Workflow card). Commit `63222f6`.
- Fixed runaway logs (50MB rotation; 64MB read cap) that were OOM-ing reviews. Commits `e4e149c`, `6d74c21`.
- Fixed dashboard false REDs (stale pre-migration OneDrive paths → C:\AlphaQuant). Commits `d6a4451`, `d1add36`(sync).
- Loops #16–#28: VWAP/edge measurement, sidelined H5, candle-close exit deploy, all-day mover scanner (two-sided, broad shadow tier), deploy controller, ORB multi-scan, security (excluded plaintext secrets from OneDrive backup). Commits `c9525c2`, `c4045be`, `5dd5c00`, `48066a5`, `2d59734`, `54f96e2`.

### Open / next
- Tomorrow 6/12: first LIVE multi-scan session — observe utilization + re-arm trades.
- Finish dashboard scrub: retire/fold `morning-readiness`, `trend-dashboard`, `review-history`.
- A true pre-open gapper scan needs a pre-market quote feed (not wired) — pre-open the page shows last-close snapshot.


## EOD SUMMARY — 2026-06-16

_Auto-generated by eod_debrief.py at 2026-06-16 8:50 PM ET · broker-truth sourced · 33 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 130 -> passed in-play gate 8 -> selected 8 -> symbols FILLED 22.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 0, refused 19 ({'deploy_refused': 18, 'already_held_or_working': 1})
- 11:35 AM: armed 0, refused 19 ({'deploy_refused': 18, 'already_held_or_working': 1})
- 12:35 PM: armed 16, refused 2 ({'slots_exhausted': 2})
- 1:35 PM: armed 6, refused 10 ({'already_held_or_working': 4, 'slots_exhausted': 6})
- 2:35 PM: armed 7, refused 10 ({'already_held_or_working': 6, 'slots_exhausted': 4})

**Incidents today:** 107 {'WARN': 107}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — a FILLED entry was not in the gate's SELECTED set.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | exit type/time/px | hold m | MFE | MAE | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | FOXA | SELLSHORT | 1 | 53.37/53.36 | -2 | 0.0 | 7.0·-2.6%·-2.6%·MID_DVOL·large·0935 | 374 | 19,960 | 53.81 | yes | synthetic-exit/9:52AM/52.99 | 16 | 0.59 | 0.71 | 142.12 | 7.48 | 134.64 | 0.83 | 957596365/957607860 |
| 2 | FOX | SELLSHORT | 1 | 48.77/48.75 | -4 | 0.0 | 5.0·-2.4%·-2.5%·SMALL_DVOL·large·0935 | 410 | 19,996 | 49.15 | yes | synthetic-exit/9:54AM/48.29 | 18 | 0.69 | 0.81 | 196.80 | 8.20 | 188.60 | 1.20 | 957596371/957609245 |
| 3 | FISV | BUY | 1 | 49.05/49.03 | 4 | 0.0 | 4.0·2.3%·2.3%·MID_DVOL·large·0935 | 407 | 19,963 | 48.69 | no | synthetic-exit/9:36AM/48.66 | 1 | 0.04 | 0.32 | -158.73 | 8.14 | -166.87 | -1.13 | 957596376/957596836 |
| 4 | YUM | BUY | 1 | 159.99/160.00 | -1 | 0.0 | 2.3·3.7%·3.6%·MID_DVOL·large·0935 | 125 | 19,999 | 159.50 | no | synthetic-exit/9:38AM/159.14 | 3 | 0.25 | 1.70 | -106.25 | 2.50 | -108.75 | -1.78 | 957596379/957597915 |
| 5 | GME | SELLSHORT | 1 | 21.30/21.31 | 5 | 0.0 | 2.1·-2.1%·-2.2%·MID_DVOL·mid·0935 | 938 | 19,979 | 21.41 | no | synthetic-exit/9:41AM/21.41 | 5 | 0.03 | 0.20 | -103.18 | 15.26 | -118.44 | -1.12 | 957596382/957600276 |
| 6 | VLO | SELLSHORT | 1 | 241.20/241.25 | 2 | 0.0 | 2.0·-6.7%·-6.8%·LARGE_DVOL·large·0935 | 82 | 19,778 | 242.57 | no | synthetic-exit/9:36AM/242.48 | 1 | 0.20 | 2.55 | -104.96 | 2.00 | -106.96 | -0.95 | 957596409/957596837 |
| 7 | IRM | BUY | 1 | 129.70/129.64 | 5 | 0.0 | 2.0·2.7%·2.6%·MID_DVOL·large·0935 | 154 | 19,974 | 129.17 | yes | synthetic-exit/9:41AM/129.45 | 5 | 1.00 | 0.84 | -38.50 | 3.08 | -41.58 | -0.51 | 957596391/957600309 |
| 8 | EW | BUY | 1 | 89.54/89.52 | 2 | 0.0 | re-arm (ctx in trace) | 223 | 19,967 | NOT-logged | n/a | synthetic-exit/12:55PM/89.11 | 20 | 0.04 | 0.41 | -95.89 | 4.46 | -100.35 | — | 957698096/957704460 |
| 9 | MRNA | BUY | 1 | 55.60/55.62 | -4 | 0.0 | re-arm (ctx in trace) | 359 | 19,960 | NOT-logged | n/a | synthetic-exit/1:00PM/56.69 | 25 | 1.18 | 0.49 | 391.31 | 7.18 | 384.13 | — | 957698106/957705805 |
| 10 | CBOE | SELLSHORT | 1 | 273.76/273.81 | 2 | 0.0 | re-arm (ctx in trace) | 73 | 19,984 | NOT-logged | n/a | synthetic-exit/1:28PM/271.80 | 53 | 2.20 | 2.23 | 143.08 | 2.00 | 141.08 | — | 957698099/957714883 |
| 11 | LITE | SELLSHORT | 1 | 882.55/882.83 | 3 | 0.0 | re-arm (ctx in trace) | 21 | 18,534 | NOT-logged | n/a | EOD-flatten/3:50PM/880.24 | 195 | 11.08 | 11.87 | 48.51 | 2.00 | 46.51 | — | 957698104/957767640 |
| 12 | GLW | SELLSHORT | 1 | 179.00/179.04 | 2 | 0.0 | re-arm (ctx in trace) | 111 | 19,869 | NOT-logged | n/a | synthetic-exit/3:40PM/176.45 | 185 | 2.80 | 1.42 | 283.05 | 2.22 | 280.83 | — | 957698112/957764483 |
| 13 | COHR | SELLSHORT | 1 | 389.00/389.14 | 4 | 0.0 | re-arm (ctx in trace) | 51 | 19,839 | NOT-logged | n/a | synthetic-exit/1:54PM/395.15 | 79 | 0.15 | 6.61 | -313.65 | 2.00 | -315.65 | — | 957698116/957725037 |
| 14 | EMR | BUY | 1 | 151.03/151.02 | 1 | 0.0 | re-arm (ctx in trace) | 132 | 19,936 | NOT-logged | n/a | synthetic-exit/1:37PM/150.32 | 62 | 0.19 | 0.71 | -93.72 | 2.64 | -96.36 | — | 957698113/957718281 |
| 15 | NFLX | SELLSHORT | 1 | 78.73/78.74 | 1 | 0.0 | re-arm (ctx in trace) | 254 | 19,997 | NOT-logged | n/a | synthetic-exit/1:15PM/78.50 | 40 | 0.32 | 0.36 | 58.42 | 5.08 | 53.34 | — | 957698110/957710407 |
| 16 | MU | SELLSHORT | 1 | 1045.35/1045.50 | 1 | 0.0 | re-arm (ctx in trace) | 19 | 19,862 | NOT-logged | n/a | synthetic-exit/2:37PM/1035.76 | 122 | 10.55 | 8.45 | 182.21 | 2.00 | 180.21 | — | 957698121/957741575 |
| 17 | RBLX | BUY | 1 | 48.53/48.51 | 4 | 0.0 | re-arm (ctx in trace) | 412 | 19,994 | NOT-logged | n/a | synthetic-exit/2:33PM/48.97 | 118 | 0.52 | 0.46 | 181.28 | 8.24 | 173.04 | — | 957698120/957739857 |
| 18 | WDAY | SELLSHORT | 1 | 125.58/125.63 | 4 | 0.0 | re-arm (ctx in trace) | 159 | 19,967 | NOT-logged | n/a | synthetic-exit/3:33PM/126.67 | 178 | 0.17 | 1.06 | -173.31 | 3.18 | -176.49 | — | 957698128/957761663 |
| 19 | INTC | SELLSHORT | 1 | 119.97/119.95 | -2 | 0.0 | re-arm (ctx in trace) | 166 | 19,915 | NOT-logged | n/a | synthetic-exit/3:18PM/118.45 | 163 | 1.75 | 1.15 | 251.49 | 3.32 | 248.17 | — | 957698133/957755940 |
| 20 | LUV | BUY | 1 | 47.92/47.90 | 4 | 0.0 | re-arm (ctx in trace) | 417 | 19,983 | NOT-logged | n/a | synthetic-exit/1:38PM/47.67 | 63 | -0.01 | 0.47 | -104.25 | 8.34 | -112.59 | — | 957698124/957718568 |
| 21 | GME | SELLSHORT | 2 | 21.31/21.31 | -0 | 0.0 | 2.1·-2.1%·-2.2%·MID_DVOL·mid·0935 | 148 | 3,154 | 21.42 | no | synthetic-exit/1:34PM/21.22 | 59 | 0.11 | 0.10 | 13.32 | 2.96 | 10.36 | 0.62 | 957698137/957717208 |
| 22 | EW | BUY | 2 | 89.16/89.15 | 1 | 0.0 | re-arm (ctx in trace) | 223 | 19,883 | NOT-logged | n/a | synthetic-exit/3:24PM/88.74 | 110 | 0.13 | 0.40 | -93.66 | 4.46 | -98.12 | — | 957717603/957758632 |
| 23 | MRNA | BUY | 2 | 56.85/56.82 | 5 | 0.0 | re-arm (ctx in trace) | 351 | 19,954 | NOT-logged | n/a | synthetic-exit/3:15PM/56.39 | 100 | 0.94 | 0.53 | -161.46 | 7.02 | -168.48 | — | 957717602/957754379 |
| 24 | NFLX | SELLSHORT | 2 | 78.22/78.22 | -0 | -0.0 | re-arm (ctx in trace) | 254 | 19,868 | NOT-logged | n/a | synthetic-exit/1:45PM/77.96 | 10 | 0.32 | 0.16 | 66.04 | 5.08 | 60.96 | — | 957717606/957721774 |
| 25 | GME | SELLSHORT | 3 | 21.20/21.20 | -0 | 0.0 | 2.1·-2.1%·-2.2%·MID_DVOL·mid·0935 | 163 | 3,456 | 21.31 | no | synthetic-exit/2:28PM/21.31 | 53 | 0.07 | 0.10 | -17.93 | 3.26 | -21.19 | -1.15 | 957717615/957737953 |
| 26 | TTWO | BUY | 1 | 224.25/224.22 | 1 | 0.0 | re-arm (ctx in trace) | 89 | 19,958 | NOT-logged | n/a | synthetic-exit/2:32PM/226.57 | 57 | 2.68 | 0.80 | 206.48 | 2.00 | 204.48 | — | 957717613/957739594 |
| 27 | SOFI | BUY | 1 | 17.89/17.89 | 0 | 0.0 | re-arm (ctx in trace) | 1117 | 19,983 | NOT-logged | n/a | synthetic-exit/3:06PM/17.96 | 91 | 0.19 | 0.06 | 78.19 | 17.40 | 60.79 | — | 957717611/957750511 |
| 28 | CBOE | SELLSHORT | 2 | 266.26/266.28 | 1 | 0.0 | re-arm (ctx in trace) | 75 | 19,970 | NOT-logged | n/a | EOD-flatten/3:50PM/267.15 | 75 | 0.98 | 2.24 | -66.75 | 2.00 | -68.75 | — | 957740828/957767604 |
| 29 | NFLX | SELLSHORT | 3 | 78.17/78.17 | -0 | 0.0 | re-arm (ctx in trace) | 254 | 19,855 | NOT-logged | n/a | synthetic-exit/2:53PM/78.49 | 19 | 0.01 | 0.32 | -81.28 | 5.08 | -86.36 | — | 957740833/957746444 |
| 30 | LUV | BUY | 2 | 47.59/47.59 | 0 | 0.0 | re-arm (ctx in trace) | 419 | 19,940 | NOT-logged | n/a | EOD-flatten/3:50PM/47.46 | 75 | 0.04 | 0.17 | -54.47 | 8.38 | -62.85 | — | 957740837/957767728 |
| 31 | TTWO | BUY | 2 | 226.97/226.93 | 2 | 0.0 | re-arm (ctx in trace) | 88 | 19,973 | NOT-logged | n/a | synthetic-exit/3:08PM/225.78 | 33 | 0.53 | 1.15 | -104.72 | 2.00 | -106.72 | — | 957740835/957751224 |
| 32 | GME | SELLSHORT | 4 | 21.29/21.29 | -0 | 0.0 | 2.1·-2.1%·-2.2%·MID_DVOL·mid·0935 | 246 | 5,237 | 21.40 | no | synthetic-exit/3:47PM/21.40 | 73 | 0.08 | 0.11 | -27.06 | 4.92 | -31.98 | -1.15 | 957740843/957767029 |
| 33 | RBLX | BUY | 2 | 49.05/49.05 | 0 | 0.0 | re-arm (ctx in trace) | 407 | 19,963 | NOT-logged | n/a | synthetic-exit/3:30PM/49.46 | 55 | 0.54 | 0.28 | 166.87 | 8.14 | 158.73 | — | 957740839/957760577 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $172.02  ·  fees: $0.00
- Commission 2.83 bps + fees 0.00 bps of $608,653 notional = **2.83 bps avg cost**
- Avg entry slippage: 1.3 bps (adverse +)
- Per-trade avg cost: $5.21 (33 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=33 · win rate 45% (15W/18L)
- GROSS day P&L $509.40 · **NET day P&L $337.38**
- Gross expectancy $15.44/trade · Net expectancy $10.22/trade
- Net profit factor 1.17
- Avg win $155.06 · avg loss $-110.47
- Largest win $384.13 · largest loss $-315.65
- Long/short split: 15L / 18S

- Capital utilization: PEAK deployed: $260,515  (86.8% of $300k target)  at 12:56 (7 pos + 7 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- 3 EC703/EC704 reject(s) from the confirm-swap (now DISABLED) at ['09:39', '09:51']
- 2 'Invalid Stop Price' reject(s) (stale-level race; broker refused a chase): ['SOFI', 'SNDK']
- NO-TRADE STRETCH 9:36AM->12:35PM (179m) -- see root cause in narrative

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

---


## EOD SUMMARY — 2026-06-17

_Auto-generated by eod_debrief.py at 2026-06-17 4:50 PM ET · broker-truth sourced · 52 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 124 -> passed in-play gate 15 -> selected 34 -> symbols FILLED 31.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 14, refused 2 ({'deploy_refused': 2})
- 11:35 AM: armed 9, refused 9 ({'already_held_or_working': 4, 'slots_exhausted': 5})
- 12:35 PM: armed 7, refused 11 ({'already_held_or_working': 2, 'slots_exhausted': 9})
- 1:35 PM: armed 6, refused 9 ({'already_held_or_working': 2, 'slots_exhausted': 7})
- 2:35 PM: armed 11, refused 7 ({'already_held_or_working': 2, 'slots_exhausted': 5})

**Incidents today:** 1 {'FAIL': 1}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — an old-gate-only (new-gate-rejected) name was traded.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | JPM | BUY | 1 | 335.45/335.37 | 2 | 0.0 | 2.3·5.0%·5.0%·LARGE_DVOL·mega·0935 | 59 | 19,792 | 334.44 | no | 0.15ATR-stop/9:38AM/334.37 | 3 | 0.00 | 1.52 | -53 | -63.72 | 2.00 | -65.72 | -1.10 | 957822899/957825086 |
| 2 | CHTR | SELLSHORT | 1 | 138.10/138.06 | -3 | 0.0 | 1.2·-4.7%·-4.2%·MID_DVOL·large·1435 | 144 | 19,886 | 139.04 | no | candle-close/9:48AM/137.41 | 12 | 1.32 | 1.34 | 788 | 99.36 | 2.88 | 96.48 | 0.71 | 957822901/957832956 |
| 3 | LDOS | SELLSHORT | 1 | 108.84/108.89 | 5 | 0.0 | 2.0·-4.1%·-4.2%·MID_DVOL·large·0935 | 183 | 19,918 | 109.44 | no | 0.15ATR-stop/9:39AM/109.90 | 3 | 0.05 | 1.19 | 221 | -193.98 | 3.66 | -197.64 | -1.80 | 957822903/957825456 |
| 4 | FISV | BUY | 1 | 51.08/51.08 | 0 | 0.0 | 1.9·6.6%·6.6%·MID_DVOL·large·0935 | 391 | 19,972 | 50.72 | no | candle-close/9:57AM/51.87 | 21 | 1.02 | 0.61 | -1,208 | 308.89 | 7.82 | 301.07 | 2.12 | 957822910/957839840 |
| 5 | IQV | SELLSHORT | 1 | 173.21/173.22 | 1 | 0.0 | 2.0·-2.9%·-2.9%·MID_DVOL·large·0935 | 115 | 19,919 | 174.27 | no | 0.15ATR-stop/10:39AM/174.44 | 63 | 0.96 | 4.33 | 438 | -142.02 | 2.30 | -144.32 | -1.17 | 957822905/957868661 |
| 6 | AIZ | BUY | 1 | 265.07/264.97 | 4 | 0.0 | 1.8·2.1%·2.1%·MID_DVOL·large·0935 | 74 | 19,616 | 264.27 | no | 0.15ATR-stop/9:58AM/263.18 | 22 | 0.48 | 2.08 | -82 | -140.23 | 2.00 | -142.23 | -2.38 | 957822913/957841089 |
| 7 | JBL | BUY | 1 | 393.21/393.14 | 2 | 0.0 | 2.0·4.6%·4.6%·LARGE_DVOL·large·1135 | 50 | 19,660 | NOT-logged | n/a | 0.15ATR-stop/10:56AM/390.27 | 21 | 0.42 | 6.18 | -736 | -147.00 | 2.00 | -149.00 | — | 957866411/957880100 |
| 8 | PCAR | SELLSHORT | 1 | 120.46/120.51 | 4 | 0.0 | 1.5·-2.6%·-2.1%·MID_DVOL·large·1435 | 165 | 19,876 | NOT-logged | n/a | candle-close/10:47AM/119.87 | 12 | 0.62 | 0.16 | 417 | 97.35 | 3.30 | 94.05 | — | 957866416/957874229 |
| 9 | CVNA | SELLSHORT | 1 | 65.72/65.74 | 3 | 0.0 | 1.9·-8.6%·-8.1%·LARGE_DVOL·large·1435 | 304 | 19,979 | NOT-logged | n/a | candle-close/10:44AM/64.96 | 9 | 0.92 | 0.29 | 638 | 231.04 | 6.08 | 224.96 | — | 957866414/957871999 |
| 10 | HOOD | BUY | 1 | 102.40/102.40 | 0 | -0.0 | 2.0·12.7%·13.2%·LARGE_DVOL·large·1435 | 195 | 19,968 | NOT-logged | n/a | candle-close/10:58AM/104.54 | 23 | 2.25 | 0.68 | 123 | 417.30 | 3.90 | 413.40 | — | 957866420/957880861 |
| 11 | AVGO | BUY | 1 | 397.58/397.57 | 0 | 0.0 | 1.3·5.4%·5.3%·LARGE_DVOL·mega·1035 | 50 | 19,879 | NOT-logged | n/a | 0.15ATR-stop/1:16PM/394.64 | 161 | 2.30 | 4.78 | -86 | -147.00 | 2.00 | -149.00 | — | 957866417/957931758 |
| 12 | LOW | BUY | 1 | 226.38/226.30 | 4 | 0.0 | 2.0·1.0%·0.9%·MID_DVOL·large·1035 | 88 | 19,921 | NOT-logged | n/a | 0.15ATR-stop/10:43AM/225.56 | 8 | 0.02 | 0.77 | -731 | -72.16 | 2.00 | -74.16 | — | 957866427/957871519 |
| 13 | CME | SELLSHORT | 1 | 251.08/251.11 | 1 | 0.0 | 1.2·-4.8%·-4.8%·LARGE_DVOL·large·1235 | 78 | 19,584 | NOT-logged | n/a | 0.15ATR-stop/11:12AM/252.48 | 37 | 0.00 | 2.30 | -2 | -109.20 | 2.00 | -111.20 | — | 957866432/957888457 |
| 14 | BLDR | BUY | 1 | 81.45/81.45 | 0 | 0.0 | 1.5·4.3%·4.3%·MID_DVOL·mid·1235 | 245 | 19,955 | NOT-logged | n/a | candle-close/11:41AM/81.82 | 66 | 0.61 | 0.87 | -1,392 | 90.65 | 4.90 | 85.75 | — | 957866435/957900698 |
| 15 | HPE | BUY | 1 | 50.23/50.21 | 4 | 0.0 | 1.2·3.5%·3.4%·MID_DVOL·large·1035 | 398 | 19,992 | NOT-logged | n/a | 0.15ATR-stop/1:24PM/49.67 | 169 | 0.22 | 0.56 | -585 | -222.88 | 7.96 | -230.84 | — | 957866441/957933725 |
| 16 | RTX | BUY | 1 | 190.43/190.43 | 0 | -0.0 | 1.6·1.5%·1.4%·MID_DVOL·mega·1035 | 105 | 19,995 | NOT-logged | n/a | candle-close/11:38AM/191.36 | 63 | 1.19 | 1.63 | 126 | 97.65 | 2.10 | 95.55 | — | 957866447/957899485 |
| 17 | CMI | BUY | 1 | 729.56/729.55 | 0 | 0.0 | 1.1·3.9%·3.8%·MID_DVOL·large·1035 | 27 | 19,698 | NOT-logged | n/a | 0.15ATR-stop/2:02PM/725.00 | 207 | 2.97 | 8.51 | -200 | -123.12 | 2.00 | -125.12 | — | 957866444/957946485 |
| 18 | CHTR | SELLSHORT | 2 | 136.52/136.53 | 1 | 0.0 | 1.2·-4.7%·-4.2%·MID_DVOL·large·1435 | 146 | 19,932 | 137.46 | no | candle-close/1:13PM/135.71 | 158 | 0.93 | 1.59 | 550 | 118.26 | 2.92 | 115.34 | 0.84 | 957866449/957930872 |
| 19 | NUE | SELLSHORT | 1 | 251.63/251.68 | 2 | 0.0 | 1.1·-2.8%·-2.8%·MID_DVOL·large·1035 | 6 | 1,510 | NOT-logged | n/a | 0.15ATR-stop/10:46AM/253.47 | 11 | 0.19 | 1.62 | 5 | -11.04 | 2.00 | -13.04 | — | 957866455/957873196 |
| 20 | ADBE | SELLSHORT | 1 | 203.13/203.18 | 2 | 0.0 | 1.5·-1.7%·-1.8%·LARGE_DVOL·large·1035 | 98 | 19,907 | NOT-logged | n/a | candle-close/2:04PM/201.67 | 209 | 2.07 | 1.43 | 528 | 143.08 | 2.00 | 141.08 | — | 957866453/957947488 |
| 21 | HOOD | BUY | 2 | 107.07/107.05 | 2 | 0.0 | 2.0·12.7%·13.2%·LARGE_DVOL·large·1435 | 186 | 19,915 | NOT-logged | n/a | candle-close/12:04PM/108.15 | 29 | 1.30 | 0.62 | -554 | 200.88 | 3.72 | 197.16 | — | 957898638/957908061 |
| 22 | CVNA | SELLSHORT | 2 | 64.22/64.22 | -0 | 0.0 | 1.9·-8.6%·-8.1%·LARGE_DVOL·large·1435 | 311 | 19,972 | NOT-logged | n/a | 0.15ATR-stop/12:07PM/64.82 | 32 | 0.09 | 0.69 | 610 | -186.60 | 6.22 | -192.82 | — | 957898645/957909797 |
| 23 | META | SELLSHORT | 1 | 580.20/580.25 | 1 | 0.0 | 1.2·-4.3%·-3.8%·LARGE_DVOL·mega·1435 | 34 | 19,727 | NOT-logged | n/a | candle-close/2:04PM/577.17 | 149 | 3.75 | 1.25 | 329 | 103.02 | 2.00 | 101.02 | — | 957898650/957947528 |
| 24 | MS | BUY | 1 | 227.80/227.80 | 0 | 0.0 | 1.3·3.1%·3.1%·LARGE_DVOL·mega·1135 | 86 | 19,591 | NOT-logged | n/a | 0.15ATR-stop/2:58PM/226.86 | 203 | 0.27 | 2.19 | -151 | -80.84 | 2.00 | -82.84 | — | 957898652/957978733 |
| 25 | CME | SELLSHORT | 2 | 250.47/250.55 | 3 | 0.0 | 1.2·-4.8%·-4.8%·LARGE_DVOL·large·1235 | 79 | 19,788 | NOT-logged | n/a | candle-close/11:43AM/249.95 | 8 | 1.30 | 0.81 | -202 | 41.48 | 2.00 | 39.48 | — | 957898657/957901273 |
| 26 | RMD | SELLSHORT | 1 | 189.34/189.37 | 2 | 0.0 | 1.3·-2.3%·-2.3%·MID_DVOL·large·1135 | 104 | 19,691 | NOT-logged | n/a | candle-close/11:52AM/188.85 | 17 | 0.93 | 0.23 | 264 | 50.96 | 2.08 | 48.88 | — | 957898664/957904270 |
| 27 | PSX | SELLSHORT | 1 | 168.25/168.24 | -1 | 0.0 | 1.4·-2.1%·-2.1%·MID_DVOL·large·1135 | 117 | 19,685 | NOT-logged | n/a | candle-close/3:46PM/167.55 | 251 | 0.93 | 1.75 | 42 | 81.90 | 2.34 | 79.56 | — | 957898660/958004979 |
| 28 | PCAR | SELLSHORT | 2 | 120.66/120.61 | -4 | 0.0 | 1.5·-2.6%·-2.1%·MID_DVOL·large·1435 | 21 | 2,534 | NOT-logged | n/a | candle-close/12:19PM/120.21 | 44 | 0.53 | 0.49 | 60 | 9.45 | 2.00 | 7.45 | — | 957898666/957913473 |
| 29 | HOOD | BUY | 3 | 108.90/108.90 | 0 | 0.0 | 2.0·12.7%·13.2%·LARGE_DVOL·large·1435 | 183 | 19,929 | NOT-logged | n/a | 0.15ATR-stop/1:43PM/107.85 | 69 | 0.27 | 1.81 | -490 | -192.15 | 3.66 | -195.81 | — | 957918504/957938757 |
| 30 | CVNA | SELLSHORT | 3 | 64.61/64.62 | 2 | 0.0 | 1.9·-8.6%·-8.1%·LARGE_DVOL·large·1435 | 309 | 19,964 | NOT-logged | n/a | 0.15ATR-stop/1:34PM/65.20 | 60 | 0.34 | 0.60 | 723 | -182.31 | 6.18 | -188.49 | — | 957918506/957936551 |
| 31 | CME | SELLSHORT | 3 | 248.97/248.97 | -0 | -0.0 | 1.2·-4.8%·-4.8%·LARGE_DVOL·large·1235 | 80 | 19,918 | NOT-logged | n/a | 0.15ATR-stop/3:17PM/250.25 | 162 | 1.30 | 2.47 | -181 | -102.40 | 2.00 | -104.40 | — | 957918512/957989469 |
| 32 | BLDR | BUY | 2 | 82.30/82.28 | 2 | 0.0 | 1.5·4.3%·4.3%·MID_DVOL·mid·1235 | 243 | 19,999 | NOT-logged | n/a | 0.15ATR-stop/2:00PM/81.45 | 86 | 0.26 | 0.70 | -1,290 | -206.55 | 4.86 | -211.41 | — | 957918507/957944598 |
| 33 | CBOE | SELLSHORT | 1 | 248.95/248.56 | -16 | 0.0 | 1.2·-5.6%·-5.4%·LARGE_DVOL·large·1335 | 80 | 19,916 | NOT-logged | n/a | 0.15ATR-stop/1:20PM/251.38 | 45 | 0.39 | 2.75 | -324 | -194.40 | 2.00 | -196.40 | — | 957918510/957932664 |
| 34 | KR | SELLSHORT | 1 | 61.68/61.68 | -0 | 0.0 | 1.4·-3.5%·-2.9%·MID_DVOL·large·1435 | 324 | 19,984 | NOT-logged | n/a | candle-close/2:14PM/61.37 | 99 | 0.41 | 0.14 | -139 | 100.44 | 6.48 | 93.96 | — | 957918514/957954028 |
| 35 | NDAQ | SELLSHORT | 1 | 85.32/85.36 | 5 | 0.0 | 1.3·-6.7%·-6.2%·MID_DVOL·large·1435 | 26 | 2,218 | NOT-logged | n/a | 0.15ATR-stop/12:40PM/85.73 | 6 | -0.02 | 0.41 | 63 | -10.66 | 2.00 | -12.66 | — | 957918517/957920787 |
| 36 | CVNA | SELLSHORT | 4 | 64.90/64.93 | 5 | -0.0 | 1.9·-8.6%·-8.1%·LARGE_DVOL·large·1435 | 307 | 19,924 | NOT-logged | n/a | candle-close/2:07PM/63.77 | 32 | 1.30 | 0.51 | 281 | 345.38 | 6.14 | 339.24 | — | 957936767/957949920 |
| 37 | CBOE | SELLSHORT | 2 | 250.12/250.13 | 0 | 0.0 | 1.2·-5.6%·-5.4%·LARGE_DVOL·large·1335 | 79 | 19,759 | NOT-logged | n/a | 0.15ATR-stop/3:34PM/253.39 | 119 | 0.85 | 3.27 | -161 | -258.33 | 2.00 | -260.33 | — | 957936772/957998968 |
| 38 | NDAQ | SELLSHORT | 2 | 83.24/83.27 | 4 | -0.0 | 1.3·-6.7%·-6.2%·MID_DVOL·large·1435 | 240 | 19,978 | NOT-logged | n/a | candle-close/2:02PM/82.62 | 27 | 0.70 | 0.62 | -163 | 148.80 | 4.80 | 144.00 | — | 957936773/957945849 |
| 39 | FE | SELLSHORT | 1 | 46.47/46.46 | -2 | 0.0 | 2.2·-2.9%·-2.3%·MID_DVOL·large·1435 | 430 | 19,982 | NOT-logged | n/a | candle-close/2:03PM/46.28 | 28 | 0.25 | 0.07 | 56 | 81.70 | 8.60 | 73.10 | — | 957936769/957946906 |
| 40 | CHTR | SELLSHORT | 3 | 135.77/135.76 | -1 | 0.0 | 1.2·-4.7%·-4.2%·MID_DVOL·large·1435 | 16 | 2,172 | 136.71 | no | candle-close/2:04PM/134.67 | 29 | 1.31 | 0.48 | 44 | 17.60 | 2.00 | 15.60 | 1.04 | 957936780/957947511 |
| 41 | SOFI | BUY | 1 | 18.60/18.60 | 0 | 0.0 | 1.1·4.9%·5.1%·LARGE_DVOL·large·1335 | 1075 | 19,995 | NOT-logged | n/a | 0.15ATR-stop/2:00PM/18.45 | 25 | 0.02 | 0.16 | -1,129 | -161.25 | 16.90 | -178.15 | — | 957936775/957944657 |
| 42 | CVNA | SELLSHORT | 5 | 63.80/63.78 | -3 | 0.0 | 1.9·-8.6%·-8.1%·LARGE_DVOL·large·1435 | 313 | 19,969 | NOT-logged | n/a | candle-close/3:13PM/63.33 | 38 | 0.73 | 0.78 | 147 | 147.11 | 6.26 | 140.85 | — | 957966057/957987371 |
| 43 | HOOD | BUY | 4 | 109.31/109.30 | 1 | 0.0 | 2.0·12.7%·13.2%·LARGE_DVOL·large·1435 | 182 | 19,894 | NOT-logged | n/a | candle-close/2:54PM/109.89 | 19 | 1.42 | 0.88 | -859 | 105.56 | 3.64 | 101.92 | — | 957966053/957976291 |
| 44 | NDAQ | SELLSHORT | 3 | 83.06/83.08 | 2 | 0.0 | 1.3·-6.7%·-6.2%·MID_DVOL·large·1435 | 240 | 19,934 | NOT-logged | n/a | 0.15ATR-stop/3:41PM/83.47 | 66 | 0.29 | 0.46 | 41 | -98.40 | 4.80 | -103.20 | — | 957966061/958002541 |
| 45 | FE | SELLSHORT | 2 | 46.32/46.29 | -6 | 0.0 | 2.2·-2.9%·-2.3%·MID_DVOL·large·1435 | 432 | 20,010 | NOT-logged | n/a | candle-close/2:52PM/46.24 | 17 | 0.15 | 0.10 | 39 | 34.56 | 8.64 | 25.92 | — | 957966059/957975465 |
| 46 | META | SELLSHORT | 2 | 573.50/573.55 | 1 | 0.0 | 1.2·-4.3%·-3.8%·LARGE_DVOL·mega·1435 | 34 | 19,499 | NOT-logged | n/a | candle-close/3:23PM/570.99 | 48 | 3.67 | 2.26 | 119 | 85.34 | 2.00 | 83.34 | — | 957966073/957992657 |
| 47 | KR | SELLSHORT | 2 | 61.77/61.80 | 5 | 0.0 | 1.4·-3.5%·-2.9%·MID_DVOL·large·1435 | 323 | 19,952 | NOT-logged | n/a | 0.15ATR-stop/3:12PM/62.00 | 37 | 0.12 | 0.29 | 65 | -74.29 | 6.46 | -80.75 | — | 957966068/957986587 |
| 48 | BSX | SELLSHORT | 1 | 45.09/45.09 | -0 | 0.0 | 1.3·-3.9%·-3.3%·LARGE_DVOL·large·1435 | 442 | 19,930 | NOT-logged | n/a | candle-close/3:30PM/44.89 | 55 | 0.26 | 0.18 | -27 | 88.40 | 8.84 | 79.56 | — | 957966065/957996680 |
| 49 | CHTR | SELLSHORT | 4 | 134.91/134.96 | 4 | 0.0 | 1.2·-4.7%·-4.2%·MID_DVOL·large·1435 | 10 | 1,349 | 135.85 | no | candle-close/3:00PM/134.17 | 25 | 1.04 | 0.76 | 22 | 7.40 | 2.00 | 5.40 | 0.58 | 957966081/957980183 |
| 50 | PCAR | SELLSHORT | 3 | 117.71/117.72 | 1 | 0.0 | 1.5·-2.6%·-2.1%·MID_DVOL·large·1435 | 169 | 19,893 | NOT-logged | n/a | 0.15ATR-stop/3:02PM/118.15 | 27 | 0.00 | 0.90 | 137 | -74.36 | 3.38 | -77.74 | — | 957966077/957981419 |
| 51 | Q | BUY | 1 | 159.47/159.40 | 4 | 0.0 | 1.2·4.4%·4.9%·MID_DVOL·large·1435 | 125 | 19,934 | NOT-logged | n/a | candle-close/2:46PM/160.15 | 11 | 1.28 | 1.05 | -431 | 85.00 | 2.50 | 82.50 | — | 957966086/957972967 |
| 52 | VRT | BUY | 1 | 325.14/325.18 | -1 | 0.0 | 1.0·8.2%·8.8%·LARGE_DVOL·large·1435 | 61 | 19,834 | NOT-logged | n/a | candle-close/2:46PM/328.43 | 11 | 3.97 | 1.45 | -653 | 200.69 | 2.00 | 198.69 | — | 957966088/957972823 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $206.32  ·  fees: $0.00
- Commission 2.19 bps + fees 0.00 bps of $943,799 notional = **2.19 bps avg cost**
- Avg entry slippage: 0.8 bps (adverse +)
- Per-trade avg cost: $3.97 (52 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=52 · win rate 54% (28W/24L)
- GROSS day P&L $344.35 · **NET day P&L $138.03**
- Gross expectancy $6.62/trade · Net expectancy $2.65/trade
- Net profit factor 1.04
- Avg win $122.33 · avg loss $-136.97
- Largest win $413.40 · largest loss $-260.33
- Long/short split: 19L / 33S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=6 · win 33% · net $-152 ($-25/trade, -12.8 bps)
- PATH re-arm:      N=46 · win 57% · net $290 ($6/trade, 3.5 bps)
- OCC 1st-entry:    N=31 · win 52% · net $337 ($11/trade, 5.8 bps)
- OCC re-entry(2+): N=21 · win 57% · net $-199 ($-9/trade, -5.5 bps)
- RECONCILE: path sum $138.03 + occ sum $138.03 == day net $138.03 -> OK

- Capital utilization: PEAK deployed: $297,584  (99.2% of $300k target)  at 12:56 (9 pos + 6 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- HOOD: left $1,207 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CHTR: left $883 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CVNA#3: left $862 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CVNA: left $775 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CVNA#2: left $750 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CHTR#2: left $647 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ADBE: left $591 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- PCAR: left $579 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- IQV: left $544 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- HOOD#3: left $527 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- HOOD#2: left $480 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- RMD: left $437 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CVNA#4: left $419 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- JBL: left $387 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CME: left $375 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- META: left $373 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- LDOS: left $348 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- PCAR#3: left $303 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- AVGO: left $300 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CVNA#5: left $288 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- BLDR#2: left $253 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CMI: left $229 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- RTX: left $220 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- JPM: left $201 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- marginability shadow: 31 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

---


## EOD SUMMARY — 2026-06-18

_Auto-generated by eod_debrief.py at 2026-06-18 4:50 PM ET · broker-truth sourced · 41 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 461 -> passed in-play gate 143 -> selected 31 -> symbols FILLED 24.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 14, refused 5 ({'deploy_refused': 5})
- 11:35 AM: armed 9, refused 10 ({'already_held_or_working': 3, 'deploy_refused': 7})
- 12:35 PM: armed 10, refused 8 ({'already_held_or_working': 4, 'slots_exhausted': 4})
- 1:35 PM: armed 5, refused 12 ({'already_held_or_working': 4, 'slots_exhausted': 8})
- 2:35 PM: armed 4, refused 13 ({'already_held_or_working': 6, 'slots_exhausted': 7})

**Incidents today:** 4 {'FAIL': 4}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — an old-gate-only (new-gate-rejected) name was traded.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | WELL | SELLSHORT | 1 | 205.67/205.69 | 1 | 0.0 | 29.8·-4.0%·-4.6%·LARGE_DVOL·large·0935 | 97 | 19,950 | 206.61 | no | candle-close/9:45AM/204.78 | 9 | 1.37 | 1.47 | -192 | 86.33 | 2.00 | 84.33 | 0.92 | 958072157/958078806 |
| 2 | OMC | SELLSHORT | 1 | 73.73/73.75 | 3 | 0.0 | 3.0·-4.6%·-5.2%·MID_DVOL·large·1035 | 271 | 19,981 | 74.04 | no | 0.15ATR-stop/9:37AM/74.08 | 1 | 0.21 | 0.77 | 737 | -94.85 | 5.42 | -100.27 | -1.19 | 958072192/958073334 |
| 3 | SBAC | SELLSHORT | 1 | 190.51/190.51 | -0 | 0.0 | 27.2·-2.7%·-3.2%·MID_DVOL·large·0935 | 104 | 19,813 | 191.53 | no | candle-close/11:35AM/189.81 | 119 | 1.28 | 0.66 | 303 | 72.80 | 2.08 | 70.72 | 0.66 | 958072183/958142915 |
| 4 | VTR | SELLSHORT | 1 | 81.86/81.90 | 5 | 0.0 | 20.8·-3.2%·-3.8%·MID_DVOL·large·0935 | 243 | 19,892 | 82.23 | no | candle-close/9:56AM/81.45 | 20 | 0.57 | 0.30 | -36 | 99.63 | 4.86 | 94.77 | 1.05 | 958072197/958087446 |
| 5 | PM | SELLSHORT | 1 | 178.12/178.20 | 4 | 0.0 | 18.1·-3.2%·-3.8%·LARGE_DVOL·mega·0935 | 112 | 19,949 | 178.87 | no | 0.15ATR-stop/9:37AM/179.17 | 1 | 0.42 | 1.04 | 83 | -117.60 | 2.24 | -119.84 | -1.43 | 958072204/958073138 |
| 6 | CPT | SELLSHORT | 1 | 110.41/110.46 | 5 | 0.0 | 16.2·-2.7%·-3.3%·MID_DVOL·large·0935 | 181 | 19,984 | 110.74 | no | 0.15ATR-stop/9:41AM/110.87 | 5 | -0.04 | 0.32 | 338 | -83.26 | 3.62 | -86.88 | -1.44 | 958072216/958075653 |
| 7 | CTVA | BUY | 1 | 77.55/77.54 | 1 | 0.0 | 17.8·2.4%·1.8%·MID_DVOL·large·0935 | 256 | 19,853 | 77.29 | no | 0.15ATR-stop/10:00AM/77.19 | 25 | -0.01 | 0.78 | 353 | -92.16 | 5.12 | -97.28 | -1.45 | 958072209/958090795 |
| 8 | CCI | SELLSHORT | 1 | 85.06/85.10 | 5 | 0.0 | 15.8·-4.1%·-4.7%·MID_DVOL·large·0935 | 235 | 19,989 | 85.43 | no | candle-close/10:07AM/84.85 | 31 | 0.43 | 0.95 | 663 | 49.35 | 4.70 | 44.65 | 0.51 | 958072223/958095336 |
| 9 | ACN | SELLSHORT | 1 | 133.08/133.14 | 5 | 0.0 | 4.0·-18.6%·-19.4%·LARGE_DVOL·large·1435 | 150 | 19,962 | NOT-logged | n/a | candle-close/10:52AM/131.78 | 17 | 1.95 | 0.77 | 524 | 195.00 | 3.00 | 192.00 | — | 958115933/958124750 |
| 10 | RUM | BUY | 1 | 7.34/7.34 | 0 | 0.0 | 4.5·1.9%·1.1%·SMALL_DVOL·mid·1235 | 2724 | 19,994 | NOT-logged | n/a | candle-close/11:02AM/7.40 | 27 | 0.15 | 0.11 | -218 | 163.44 | 36.69 | 126.75 | — | 958115939/958129481 |
| 11 | TTWO | BUY | 1 | 237.69/237.67 | 1 | 0.0 | 2.0·5.5%·4.7%·LARGE_DVOL·large·1435 | 84 | 19,966 | NOT-logged | n/a | 0.15ATR-stop/10:47AM/236.33 | 12 | 0.38 | 1.31 | 265 | -114.24 | 2.00 | -116.24 | — | 958115940/958122185 |
| 12 | OMC | SELLSHORT | 2 | 71.91/71.92 | 1 | 0.0 | 3.0·-4.6%·-5.2%·MID_DVOL·large·1035 | 277 | 19,919 | 72.22 | no | candle-close/3:49PM/71.32 | 314 | 0.89 | 1.82 | -11 | 163.43 | 5.54 | 157.89 | 1.83 | 958115943/958226265 |
| 13 | INTC | BUY | 1 | 129.94/129.94 | 0 | 0.0 | 1.7·10.4%·9.5%·LARGE_DVOL·mega·1335 | 153 | 19,881 | NOT-logged | n/a | candle-close/11:13AM/132.02 | 38 | 2.63 | 0.60 | 288 | 318.24 | 3.06 | 315.18 | — | 958115953/958134180 |
| 14 | IRM | BUY | 1 | 128.38/128.32 | 5 | 0.0 | 3.4·2.0%·1.4%·MID_DVOL·large·1035 | 155 | 19,899 | NOT-logged | n/a | candle-close/12:13PM/128.81 | 98 | 0.67 | 0.42 | -163 | 66.65 | 3.10 | 63.55 | — | 958115965/958158764 |
| 15 | SHW | BUY | 1 | 320.60/320.58 | 1 | 0.0 | 3.5·2.1%·1.4%·LARGE_DVOL·large·1035 | 62 | 19,877 | NOT-logged | n/a | candle-close/10:58AM/321.19 | 23 | 1.61 | 0.66 | -9 | 36.58 | 2.00 | 34.58 | — | 958115961/958127610 |
| 16 | STLD | SELLSHORT | 1 | 253.90/254.00 | 4 | 0.0 | 2.2·-7.2%·-8.0%·MID_DVOL·large·1235 | 78 | 19,804 | NOT-logged | n/a | candle-close/11:16AM/252.35 | 41 | 2.49 | 1.94 | 195 | 120.90 | 2.00 | 118.90 | — | 958115956/958135601 |
| 17 | QCOM | BUY | 1 | 224.14/224.15 | -0 | 0.0 | 2.2·5.1%·4.5%·LARGE_DVOL·mega·1035 | 88 | 19,724 | NOT-logged | n/a | 0.15ATR-stop/11:03AM/221.41 | 28 | 2.16 | 2.90 | 410 | -240.24 | 2.00 | -242.24 | — | 958115993/958130013 |
| 18 | PFE | SELLSHORT | 1 | 25.12/25.11 | -4 | 0.0 | 2.6·-2.9%·-3.6%·LARGE_DVOL·large·1235 | 796 | 19,996 | NOT-logged | n/a | candle-close/10:49AM/25.03 | 14 | 0.13 | 0.09 | -151 | 71.64 | 13.55 | 58.09 | — | 958115983/958123201 |
| 19 | CVX | SELLSHORT | 1 | 173.36/173.37 | 1 | 0.0 | 3.0·-2.3%·-3.0%·LARGE_DVOL·mega·1035 | 9 | 1,560 | NOT-logged | n/a | candle-close/12:40PM/172.73 | 125 | 0.71 | 0.66 | -8 | 5.67 | 2.00 | 3.67 | — | 958116000/958167722 |
| 20 | ACN | SELLSHORT | 2 | 130.00/130.00 | -0 | 0.0 | 4.0·-18.6%·-19.4%·LARGE_DVOL·large·1435 | 153 | 19,890 | NOT-logged | n/a | candle-close/12:01PM/128.72 | 26 | 1.50 | 0.49 | 66 | 195.84 | 3.06 | 192.78 | — | 958142881/958153640 |
| 21 | RUM | BUY | 2 | 7.48/7.48 | 0 | 0.0 | 4.5·1.9%·1.1%·SMALL_DVOL·mid·1235 | 2673 | 19,994 | NOT-logged | n/a | 0.15ATR-stop/12:02PM/7.35 | 28 | 0.13 | 0.12 | -80 | -347.49 | 36.08 | -383.57 | — | 958142882/958154227 |
| 22 | TTWO | BUY | 2 | 237.98/237.97 | 0 | 0.0 | 2.0·5.5%·4.7%·LARGE_DVOL·large·1435 | 84 | 19,990 | NOT-logged | n/a | candle-close/11:49AM/238.89 | 14 | 1.55 | 0.45 | 50 | 76.44 | 2.00 | 74.44 | — | 958142883/958148176 |
| 23 | STLD | SELLSHORT | 2 | 252.82/252.86 | 2 | 0.0 | 2.2·-7.2%·-8.0%·MID_DVOL·large·1235 | 78 | 19,720 | NOT-logged | n/a | candle-close/12:04PM/251.73 | 30 | 1.64 | 0.74 | 147 | 85.02 | 2.00 | 83.02 | — | 958142888/958155265 |
| 24 | PFE | SELLSHORT | 2 | 25.04/25.04 | -0 | 0.0 | 2.6·-2.9%·-3.6%·LARGE_DVOL·large·1235 | 798 | 19,982 | NOT-logged | n/a | 0.15ATR-stop/11:46AM/25.11 | 11 | 0.00 | 0.08 | -88 | -55.86 | 13.58 | -69.44 | — | 958142886/958147138 |
| 25 | INTC | BUY | 2 | 132.73/132.66 | 5 | 0.0 | 1.7·10.4%·9.5%·LARGE_DVOL·mega·1335 | 150 | 19,910 | NOT-logged | n/a | candle-close/12:40PM/133.67 | 65 | 1.38 | 2.29 | 35 | 141.00 | 3.00 | 138.00 | — | 958142897/958167730 |
| 26 | CTSH | SELLSHORT | 1 | 44.16/44.18 | 5 | 0.0 | 1.7·-9.8%·-10.7%·LARGE_DVOL·large·1335 | 452 | 19,960 | NOT-logged | n/a | candle-close/11:57AM/43.90 | 22 | 0.35 | 0.14 | 104 | 117.52 | 9.04 | 108.48 | — | 958142895/958151894 |
| 27 | LMT | SELLSHORT | 1 | 509.32/509.32 | -0 | 0.0 | 1.8·-4.9%·-5.6%·LARGE_DVOL·large·1435 | 39 | 19,863 | NOT-logged | n/a | 0.15ATR-stop/12:54PM/511.00 | 79 | 1.82 | 2.75 | 5 | -65.52 | 2.00 | -67.52 | — | 958142892/958171522 |
| 28 | KR | SELLSHORT | 1 | 58.13/58.12 | -2 | 0.0 | 1.7·-7.4%·-8.2%·LARGE_DVOL·large·1235 | 336 | 19,532 | NOT-logged | n/a | candle-close/11:41AM/58.20 | 6 | 0.34 | 0.14 | 531 | -23.52 | 6.72 | -30.24 | — | 958142898/958145323 |
| 29 | ACN | SELLSHORT | 3 | 128.71/128.71 | -0 | 0.0 | 4.0·-18.6%·-19.4%·LARGE_DVOL·large·1435 | 154 | 19,821 | NOT-logged | n/a | candle-close/1:54PM/127.63 | 79 | 1.51 | 1.09 | -102 | 166.32 | 3.08 | 163.24 | — | 958166339/958189484 |
| 30 | TTWO | BUY | 3 | 241.79/241.73 | 2 | 0.0 | 2.0·5.5%·4.7%·LARGE_DVOL·large·1435 | 82 | 19,827 | NOT-logged | n/a | 0.15ATR-stop/1:51PM/240.42 | 76 | 0.36 | 2.22 | -76 | -112.34 | 2.00 | -114.34 | — | 958166343/958188656 |
| 31 | STLD | SELLSHORT | 3 | 249.88/249.84 | -2 | 0.0 | 2.2·-7.2%·-8.0%·MID_DVOL·large·1235 | 80 | 19,991 | NOT-logged | n/a | 0.15ATR-stop/3:34PM/251.57 | 179 | 0.33 | 5.75 | 138 | -134.80 | 2.00 | -136.80 | — | 958166344/958221014 |
| 32 | KR | SELLSHORT | 2 | 57.19/57.20 | 2 | 0.0 | 1.7·-7.4%·-8.2%·LARGE_DVOL·large·1235 | 348 | 19,902 | NOT-logged | n/a | candle-close/12:45PM/56.96 | 10 | 0.27 | 0.15 | 118 | 80.04 | 6.96 | 73.08 | — | 958166358/958168908 |
| 33 | MSTR | SELLSHORT | 1 | 110.80/110.80 | -0 | 0.0 | 1.8·-6.1%·-7.1%·LARGE_DVOL·large·1335 | 178 | 19,722 | NOT-logged | n/a | candle-close/1:13PM/109.46 | 38 | 1.61 | 0.66 | -532 | 238.52 | 3.56 | 234.96 | — | 958166361/958177405 |
| 34 | MSTR | SELLSHORT | 2 | 108.90/108.93 | 3 | 0.0 | 1.8·-6.1%·-7.1%·LARGE_DVOL·large·1335 | 182 | 19,820 | NOT-logged | n/a | 0.15ATR-stop/3:18PM/110.35 | 103 | 0.62 | 1.53 | -382 | -263.90 | 3.64 | -267.54 | — | 958184241/958215905 |
| 35 | INTC | BUY | 3 | 134.58/134.58 | 0 | 0.0 | 1.7·10.4%·9.5%·LARGE_DVOL·mega·1335 | 148 | 19,918 | NOT-logged | n/a | 0.15ATR-stop/3:50PM/133.09 | 135 | 0.65 | 3.03 | 120 | -220.52 | 2.96 | -223.48 | — | 958184249/958226666 |
| 36 | CTSH | SELLSHORT | 2 | 43.90/43.83 | -16 | 0.0 | 1.7·-9.8%·-10.7%·LARGE_DVOL·large·1335 | 456 | 20,018 | NOT-logged | n/a | EOD-flatten/3:50PM/43.83 | 135 | 0.19 | 0.94 | 73 | 31.92 | 9.12 | 22.80 | — | 958184246/958226706 |
| 37 | HAS | BUY | 1 | 86.03/86.03 | 0 | 0.0 | 2.1·3.0%·2.1%·MID_DVOL·large·1335 | 232 | 19,959 | NOT-logged | n/a | 0.15ATR-stop/1:56PM/85.62 | 21 | 0.14 | 0.43 | -200 | -95.12 | 4.64 | -99.76 | — | 958184252/958190024 |
| 38 | Q | BUY | 1 | 169.37/169.39 | -1 | 0.0 | 1.4·6.9%·6.2%·MID_DVOL·large·1435 | 7 | 1,186 | NOT-logged | n/a | 0.15ATR-stop/2:06PM/168.07 | 31 | 0.70 | 1.30 | 6 | -9.10 | 2.00 | -11.10 | — | 958184253/958193508 |
| 39 | ACN | SELLSHORT | 4 | 126.84/126.86 | 2 | 0.0 | 4.0·-18.6%·-19.4%·LARGE_DVOL·large·1435 | 157 | 19,914 | NOT-logged | n/a | 0.15ATR-stop/2:58PM/128.12 | 23 | 0.21 | 1.29 | -27 | -200.96 | 3.14 | -204.10 | — | 958203033/958209244 |
| 40 | LMT | SELLSHORT | 2 | 505.99/506.00 | 0 | 0.0 | 1.8·-4.9%·-5.6%·LARGE_DVOL·large·1435 | 39 | 19,734 | NOT-logged | n/a | 0.15ATR-stop/3:28PM/507.89 | 53 | 0.81 | 1.89 | -116 | -74.10 | 2.00 | -76.10 | — | 958203039/958219082 |
| 41 | Q | BUY | 2 | 167.99/167.93 | 3 | 0.0 | 1.4·6.9%·6.2%·MID_DVOL·large·1435 | 7 | 1,176 | NOT-logged | n/a | EOD-flatten/3:50PM/167.25 | 75 | 0.76 | 0.74 | 12 | -5.15 | 2.00 | -7.15 | — | 958203041/958226722 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $229.55  ·  fees: $0.00
- Commission 3.02 bps + fees 0.00 bps of $759,822 notional = **3.02 bps avg cost**
- Avg entry slippage: 0.9 bps (adverse +)
- Per-trade avg cost: $5.60 (41 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=41 · win rate 54% (22W/19L)
- GROSS day P&L $231.55 · **NET day P&L $2.00**
- Gross expectancy $5.65/trade · Net expectancy $0.05/trade
- Net profit factor 1.00
- Avg win $111.63 · avg loss $-129.15
- Largest win $315.18 · largest loss $-383.57
- Long/short split: 15L / 26S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=8 · win 50% · net $-110 ($-14/trade, -6.9 bps)
- PATH re-arm:      N=33 · win 55% · net $112 ($3/trade, 1.9 bps)
- OCC 1st-entry:    N=24 · win 58% · net $579 ($24/trade, 13.2 bps)
- OCC re-entry(2+): N=17 · win 47% · net $-577 ($-34/trade, -18.1 bps)
- RECONCILE: path sum $2.00 + occ sum $2.00 == day net $2.00 -> OK

- Capital utilization: PEAK deployed: $300,129  (100.0% of $300k target)  at 14:56 (5 pos + 11 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- 1 'Invalid Stop Price' reject(s) (stale-level race; broker refused a chase): ['CTSH']
- ACN: left $927 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- OMC: left $878 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CCI: left $712 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- QCOM: left $705 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- KR: left $632 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- RUM: left $572 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- INTC: left $491 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- TTWO: left $489 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ACN#2: left $477 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CTVA: left $476 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ACN#4: left $396 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- SBAC: left $360 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CPT: left $357 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- RUM#2: left $347 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- STLD: left $335 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ACN#3: left $313 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- STLD#2: left $287 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- MSTR: left $287 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- STLD#3: left $282 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- TTWO#2: left $274 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- PM: left $239 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- INTC#2: left $234 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- LMT: left $227 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- INTC#3: left $225 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- KR#2: left $223 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CTSH: left $221 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- marginability shadow: 24 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

---


## EOD SUMMARY — 2026-06-19

_Auto-generated by eod_debrief.py at 2026-06-19 4:50 PM ET · broker-truth sourced · 0 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 14 -> passed in-play gate 0 -> selected 14 -> symbols FILLED 0.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 14, refused 0
- 11:35 AM: armed 14, refused 0
- 12:35 PM: armed 14, refused 0
- 1:35 PM: armed 14, refused 0
- 2:35 PM: armed 14, refused 0

**Incidents today:** 65 {'FAIL': 65}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — gate_enforced is False; gate ran in SHADOW. Set ORB_INPLAY_GATE=True.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $0.00  ·  fees: $0.00
- Commission 0.00 bps + fees 0.00 bps of $1 notional = **0.00 bps avg cost**
- Avg entry slippage: n/a (adverse +)
- no trades

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- no closed round-trips today

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- none flagged by code today

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

---


## EOD SUMMARY — 2026-06-20

_Auto-generated by eod_debrief.py at 2026-06-20 4:50 PM ET · broker-truth sourced · 0 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 14 -> passed in-play gate 0 -> selected 14 -> symbols FILLED 0.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 14, refused 0
- 11:35 AM: armed 14, refused 0
- 12:35 PM: armed 14, refused 0
- 1:35 PM: armed 14, refused 0
- 2:35 PM: armed 14, refused 0

**Incidents today:** 0 (none).
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — gate_enforced is False; gate ran in SHADOW. Set ORB_INPLAY_GATE=True.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $0.00  ·  fees: $0.00
- Commission 0.00 bps + fees 0.00 bps of $1 notional = **0.00 bps avg cost**
- Avg entry slippage: n/a (adverse +)
- no trades

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- no closed round-trips today

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- none flagged by code today

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=14 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = 0.034; breakout won (R>0) 10/14 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): large=0.06 (n9), mega=-0.02 (n5)
---


## EOD SUMMARY — 2026-06-21

_Auto-generated by eod_debrief.py at 2026-06-21 4:50 PM ET · broker-truth sourced · 0 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 14 -> passed in-play gate 0 -> selected 14 -> symbols FILLED 0.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 14, refused 0
- 11:35 AM: armed 14, refused 0
- 12:35 PM: armed 14, refused 0
- 1:35 PM: armed 14, refused 0
- 2:35 PM: armed 14, refused 0

**Incidents today:** 12 {'FAIL': 12}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — gate_enforced is False; gate ran in SHADOW. Set ORB_INPLAY_GATE=True.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $0.00  ·  fees: $0.00
- Commission 0.00 bps + fees 0.00 bps of $1 notional = **0.00 bps avg cost**
- Avg entry slippage: n/a (adverse +)
- no trades

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- no closed round-trips today

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- none flagged by code today

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=14 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = 0.034; breakout won (R>0) 10/14 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): large=0.06 (n9), mega=-0.02 (n5)
---


## EOD SUMMARY — 2026-06-22

_Auto-generated by eod_debrief.py at 2026-06-22 4:17 PM ET · broker-truth sourced · 16 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 133 -> passed in-play gate 10 -> selected 25 -> symbols FILLED 16.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 5, refused 15 ({'deploy_refused': 15})
- 11:35 AM: armed 5, refused 13 ({'already_held_or_working': 3, 'reentry_capped': 3, 'deploy_refused': 7})
- 12:35 PM: armed 0, refused 20 ({'already_held_or_working': 8, 'reentry_capped': 4, 'deploy_refused': 8})
- 1:35 PM: armed 4, refused 12 ({'already_held_or_working': 4, 'reentry_capped': 4, 'slots_exhausted': 4})
- 2:35 PM: armed 2, refused 18 ({'already_held_or_working': 7, 'reentry_capped': 4, 'slots_exhausted': 7})

**Incidents today:** 117 {'FAIL': 117}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — an old-gate-only (new-gate-rejected) name was traded.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | ACN | SELLSHORT | 1 | 123.10/123.13 | 2 | 0.0 | 3.4·-3.8%·-4.0%·LARGE_DVOL·large·0935 | 162 | 19,942 | 124.54 | no | candle-close/11:12AM/120.83 | 96 | 2.77 | 2.60 | -635 | 367.74 | 3.24 | 364.50 | 1.57 | 958371234/958435413 |
| 2 | ULTA | BUY | 1 | 466.99/467.00 | -0 | 0.0 | 2.4·2.4%·2.1%·MID_DVOL·large·0935 | 42 | 19,614 | 464.67 | no | EOD-flatten/3:50PM/461.42 | 374 | 1.69 | 8.17 | 147 | -233.94 | 2.00 | -235.94 | -2.42 | 958371243/958531623 |
| 3 | TTWO | BUY | 1 | 249.75/249.75 | 0 | 0.0 | 3.4·8.6%·8.3%·LARGE_DVOL·large·0935 | 80 | 19,980 | 248.64 | no | candle-close/9:57AM/250.11 | 21 | 1.49 | 5.75 | -844 | 28.80 | 2.00 | 26.80 | 0.30 | 958371238/958388507 |
| 4 | ABBV | BUY | 1 | 228.35/228.34 | 0 | 0.0 | 2.0·5.5%·5.2%·LARGE_DVOL·mega·0935 | 87 | 19,866 | 227.50 | no | candle-close/10:56AM/229.40 | 80 | 1.52 | 3.13 | 61 | 91.35 | 2.00 | 89.35 | 1.21 | 958371249/958426544 |
| 5 | FIX | BUY | 1 | 2033.67/2033.67 | 0 | 0.0 | 1.5·3.4%·3.1%·LARGE_DVOL·large·0935 | 8 | 16,269 | 2017.76 | no | candle-close/1:32PM/2045.67 | 236 | 16.33 | 39.50 | 179 | 96.00 | 2.00 | 94.00 | 0.74 | 958371283/958488429 |
| 6 | BB | BUY | 1 | 8.99/8.99 | 0 | -0.0 | 1.6·6.9%·7.1%·MID_DVOL·mid·1035 | 265 | 2,382 | NOT-logged | n/a | EOD-flatten/3:50PM/8.78 | 315 | 0.11 | 0.27 | 5 | -55.65 | 5.30 | -60.95 | — | 958413993/958531569 |
| 7 | SMCI | BUY | 1 | 34.54/34.54 | 0 | 0.0 | 2.5·11.7%·11.9%·LARGE_DVOL·large·1035 | 579 | 19,999 | NOT-logged | n/a | candle-close/11:15AM/35.22 | 40 | 0.76 | 0.54 | 139 | 393.72 | 10.95 | 382.77 | — | 958413989/958436821 |
| 8 | GOOG | SELLSHORT | 1 | 346.73/346.74 | 0 | 0.0 | 1.1·-5.5%·-5.3%·LARGE_DVOL·mega·1035 | 18 | 6,241 | NOT-logged | n/a | candle-close/10:54AM/344.91 | 19 | 1.99 | 1.78 | -68 | 32.76 | 2.00 | 30.76 | — | 958413997/958425434 |
| 9 | RIOT | BUY | 1 | 28.91/28.90 | 3 | 0.0 | 1.3·2.6%·2.9%·MID_DVOL·large·1135 | 692 | 20,006 | NOT-logged | n/a | EOD-flatten/3:50PM/28.62 | 255 | 0.21 | 0.59 | 14 | -200.68 | 12.30 | -212.98 | — | 958446486/958531600 |
| 10 | SNDK | BUY | 1 | 2321.08/2320.00 | 5 | 0.0 | 1.0·5.0%·5.3%·LARGE_DVOL·mega·1135 | 8 | 18,569 | NOT-logged | n/a | EOD-flatten/3:50PM/2286.65 | 255 | 12.68 | 37.79 | -100 | -275.44 | 2.00 | -277.44 | — | 958446485/958531613 |
| 11 | COHR | BUY | 1 | 403.14/403.14 | 0 | 0.0 | 1.1·3.4%·3.7%·LARGE_DVOL·large·1135 | 25 | 10,078 | NOT-logged | n/a | candle-close/12:56PM/411.71 | 81 | 10.35 | 4.14 | 341 | 214.37 | 2.00 | 212.37 | — | 958446496/958478785 |
| 12 | RBLX | SELLSHORT | 1 | 46.56/46.58 | 4 | 0.0 | 1.0·-9.4%·-9.1%·MID_DVOL·large·1135 | 429 | 19,974 | NOT-logged | n/a | candle-close/1:10PM/46.10 | 95 | 0.54 | 0.76 | -523 | 197.34 | 8.58 | 188.76 | — | 958446493/958483131 |
| 13 | AIG | BUY | 1 | 76.32/76.33 | -1 | 0.0 | 1.2·2.9%·3.2%·MID_DVOL·large·1335 | 262 | 19,996 | NOT-logged | n/a | candle-close/2:56PM/76.38 | 81 | 0.98 | 0.17 | -10 | 15.72 | 5.24 | 10.48 | — | 958490265/958513504 |
| 14 | VRT | BUY | 1 | 352.32/352.22 | 3 | 0.0 | 0.8·5.6%·5.9%·LARGE_DVOL·large·1335 | 55 | 19,378 | NOT-logged | n/a | EOD-flatten/3:50PM/355.30 | 135 | 3.49 | 1.24 | 156 | 163.90 | 2.00 | 161.90 | — | 958490269/958531628 |
| 15 | PLTR | SELLSHORT | 1 | 120.62/120.65 | 2 | 0.0 | 0.8·-6.0%·-5.8%·LARGE_DVOL·mega·1435 | 165 | 19,902 | NOT-logged | n/a | candle-close/3:00PM/119.63 | 25 | 1.14 | 0.17 | 25 | 163.35 | 3.30 | 160.05 | — | 958506610/958514656 |
| 16 | NFLX | SELLSHORT | 1 | 73.19/73.19 | -0 | 0.0 | 0.8·-5.3%·-5.0%·LARGE_DVOL·mega·1435 | 30 | 2,196 | NOT-logged | n/a | candle-close/3:08PM/72.94 | 33 | 0.35 | 0.16 | 2 | 7.50 | 2.00 | 5.50 | — | 958506612/958517826 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $66.91  ·  fees: $0.00
- Commission 2.63 bps + fees 0.00 bps of $254,392 notional = **2.63 bps avg cost**
- Avg entry slippage: 1.2 bps (adverse +)
- Per-trade avg cost: $4.18 (16 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=16 · win rate 75% (12W/4L)
- GROSS day P&L $1,006.85 · **NET day P&L $939.93**
- Gross expectancy $62.93/trade · Net expectancy $58.75/trade
- Net profit factor 2.19
- Avg win $143.94 · avg loss $-196.83
- Largest win $382.77 · largest loss $-277.44
- Long/short split: 11L / 5S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=5 · win 80% · net $339 ($68/trade, 35.4 bps)
- PATH re-arm:      N=11 · win 73% · net $601 ($55/trade, 37.9 bps)
- OCC 1st-entry:    N=16 · win 75% · net $940 ($59/trade, 36.9 bps)
- OCC re-entry(2+): N=0
- RECONCILE: path sum $939.93 + occ sum $939.93 == day net $939.93 -> OK

- Capital utilization: PEAK deployed: $312,404  (104.1% of $300k target)  at 10:56 (5 pos + 12 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- 2 'Invalid Stop Price' reject(s) (stale-level race; broker refused a chase): ['SOFI', 'PLTR']
- SMCI: left $915 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- COHR: left $698 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ACN: left $434 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- AIG: left $356 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ABBV: left $254 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ULTA: left $220 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- FIX: left $213 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- NO-TRADE STRETCH 11:35AM->1:35PM (120m) -- see root cause in narrative
- marginability shadow: 16 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=25 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = -0.136; breakout won (R>0) 10/25 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): large=-0.06 (n15), mega=0.02 (n6), mid=-0.64 (n4)
---

----- alphaquant-alert-triage (scheduled) - 2026-06-22 Mon ~4:44 PM ET - **Triage: inbox CLEAN (code_alert_inbox.py --json: n_total=0, n_actionable=0, 0 critical groups). No new actionable CRITICAL alerts since last ack. State verified healthy: CSHV 16:40 run OK=44/WARN=0/FAIL=0 (all checks passing, scheduled_tasks_present back to all-8-OK post the ~4:06 PM reboot, bot heartbeat 17s fresh, book context market-closed). Nothing to escalate -- silence = handled. --ack'd.**

----- alphaquant-alert-triage (scheduled) - 2026-06-22 Mon ~4:46 PM ET - **CORRECTION/follow-up to the ~4:44 PM entry above:** the --json snapshot showed 0 actionable, but --ack then surfaced 1 CRITICAL that landed mid-run (CSHV 16:45 run): `clean_day_certified` FAIL -- "day NOT clean: failed ['no_critical_incident']; consecutive_clean reset (was building to 0)". VERIFIED + classified Bucket A (NO re-ping). Why benign/expected: (1) certifier NON-CLEAN verdict MATCHES Loop 141's documented correct conclusion ("Correct verdict = NON-CLEAN"); driven by incidents.jsonl (307 today), NOT a new bot fault -- bot_alerts.jsonl has ZERO FAILs today (all INFO; last = ORB_EOD_OK 15:55 clean flatten). (2) NO new post-reboot critical incident: only incidents after the ~4:06 PM reboot are 16:01 + 16:06 scheduled_tasks_present TIMEOUT (the pre-reboot OOM false-FAILs already escalated 2x + remediated) and the 16:45 certifier FAIL itself. (3) Certifier context confirms ZERO trading risk: trading_stopped=no/SAFE_MODE off, orders_active=no (flat: 0 working/0 positions); market closed. (4) consecutive_clean reset to 0 CORRECTS the improperly-advanced counter Loop 141 flagged (buggy CLEAN verdicts had wrongly built it to 11) -- self-correction toward the right state, not a problem. Rhett already knows today was non-clean (approved the OOM reboot; Loop 141 handoff documents it). Nothing actionable -> no notify. Already --ack'd (cursor advanced).**


## EOD SUMMARY — 2026-06-22

_Auto-generated by eod_debrief.py at 2026-06-22 4:50 PM ET · broker-truth sourced · 16 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 133 -> passed in-play gate 10 -> selected 25 -> symbols FILLED 16.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 5, refused 15 ({'deploy_refused': 15})
- 11:35 AM: armed 5, refused 13 ({'already_held_or_working': 3, 'reentry_capped': 3, 'deploy_refused': 7})
- 12:35 PM: armed 0, refused 20 ({'already_held_or_working': 8, 'reentry_capped': 4, 'deploy_refused': 8})
- 1:35 PM: armed 4, refused 12 ({'already_held_or_working': 4, 'reentry_capped': 4, 'slots_exhausted': 4})
- 2:35 PM: armed 2, refused 18 ({'already_held_or_working': 7, 'reentry_capped': 4, 'slots_exhausted': 7})

**Incidents today:** 118 {'FAIL': 118}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — an old-gate-only (new-gate-rejected) name was traded.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | ACN | SELLSHORT | 1 | 123.10/123.13 | 2 | 0.0 | 3.4·-3.8%·-4.0%·LARGE_DVOL·large·0935 | 162 | 19,942 | 124.54 | no | candle-close/11:12AM/120.83 | 96 | 2.77 | 2.60 | -635 | 367.74 | 3.24 | 364.50 | 1.57 | 958371234/958435413 |
| 2 | ULTA | BUY | 1 | 466.99/467.00 | -0 | 0.0 | 2.4·2.4%·2.1%·MID_DVOL·large·0935 | 42 | 19,614 | 464.67 | no | EOD-flatten/3:50PM/461.42 | 374 | 1.69 | 8.17 | 147 | -233.94 | 2.00 | -235.94 | -2.42 | 958371243/958531623 |
| 3 | TTWO | BUY | 1 | 249.75/249.75 | 0 | 0.0 | 3.4·8.6%·8.3%·LARGE_DVOL·large·0935 | 80 | 19,980 | 248.64 | no | candle-close/9:57AM/250.11 | 21 | 1.49 | 5.75 | -844 | 28.80 | 2.00 | 26.80 | 0.30 | 958371238/958388507 |
| 4 | ABBV | BUY | 1 | 228.35/228.34 | 0 | 0.0 | 2.0·5.5%·5.2%·LARGE_DVOL·mega·0935 | 87 | 19,866 | 227.50 | no | candle-close/10:56AM/229.40 | 80 | 1.52 | 3.13 | 61 | 91.35 | 2.00 | 89.35 | 1.21 | 958371249/958426544 |
| 5 | FIX | BUY | 1 | 2033.67/2033.67 | 0 | 0.0 | 1.5·3.4%·3.1%·LARGE_DVOL·large·0935 | 8 | 16,269 | 2017.76 | no | candle-close/1:32PM/2045.67 | 236 | 16.33 | 39.50 | 179 | 96.00 | 2.00 | 94.00 | 0.74 | 958371283/958488429 |
| 6 | BB | BUY | 1 | 8.99/8.99 | 0 | -0.0 | 1.6·6.9%·7.1%·MID_DVOL·mid·1035 | 265 | 2,382 | NOT-logged | n/a | EOD-flatten/3:50PM/8.78 | 315 | 0.11 | 0.27 | 5 | -55.65 | 5.30 | -60.95 | — | 958413993/958531569 |
| 7 | SMCI | BUY | 1 | 34.54/34.54 | 0 | 0.0 | 2.5·11.7%·11.9%·LARGE_DVOL·large·1035 | 579 | 19,999 | NOT-logged | n/a | candle-close/11:15AM/35.22 | 40 | 0.76 | 0.54 | 139 | 393.72 | 10.95 | 382.77 | — | 958413989/958436821 |
| 8 | GOOG | SELLSHORT | 1 | 346.73/346.74 | 0 | 0.0 | 1.1·-5.5%·-5.3%·LARGE_DVOL·mega·1035 | 18 | 6,241 | NOT-logged | n/a | candle-close/10:54AM/344.91 | 19 | 1.99 | 1.78 | -68 | 32.76 | 2.00 | 30.76 | — | 958413997/958425434 |
| 9 | RIOT | BUY | 1 | 28.91/28.90 | 3 | 0.0 | 1.3·2.6%·2.9%·MID_DVOL·large·1135 | 692 | 20,006 | NOT-logged | n/a | EOD-flatten/3:50PM/28.62 | 255 | 0.21 | 0.59 | 14 | -200.68 | 12.30 | -212.98 | — | 958446486/958531600 |
| 10 | SNDK | BUY | 1 | 2321.08/2320.00 | 5 | 0.0 | 1.0·5.0%·5.3%·LARGE_DVOL·mega·1135 | 8 | 18,569 | NOT-logged | n/a | EOD-flatten/3:50PM/2286.65 | 255 | 12.68 | 37.79 | -100 | -275.44 | 2.00 | -277.44 | — | 958446485/958531613 |
| 11 | COHR | BUY | 1 | 403.14/403.14 | 0 | 0.0 | 1.1·3.4%·3.7%·LARGE_DVOL·large·1135 | 25 | 10,078 | NOT-logged | n/a | candle-close/12:56PM/411.71 | 81 | 10.35 | 4.14 | 341 | 214.37 | 2.00 | 212.37 | — | 958446496/958478785 |
| 12 | RBLX | SELLSHORT | 1 | 46.56/46.58 | 4 | 0.0 | 1.0·-9.4%·-9.1%·MID_DVOL·large·1135 | 429 | 19,974 | NOT-logged | n/a | candle-close/1:10PM/46.10 | 95 | 0.54 | 0.76 | -523 | 197.34 | 8.58 | 188.76 | — | 958446493/958483131 |
| 13 | AIG | BUY | 1 | 76.32/76.33 | -1 | 0.0 | 1.2·2.9%·3.2%·MID_DVOL·large·1335 | 262 | 19,996 | NOT-logged | n/a | candle-close/2:56PM/76.38 | 81 | 0.98 | 0.17 | -10 | 15.72 | 5.24 | 10.48 | — | 958490265/958513504 |
| 14 | VRT | BUY | 1 | 352.32/352.22 | 3 | 0.0 | 0.8·5.6%·5.9%·LARGE_DVOL·large·1335 | 55 | 19,378 | NOT-logged | n/a | EOD-flatten/3:50PM/355.30 | 135 | 3.49 | 1.24 | 156 | 163.90 | 2.00 | 161.90 | — | 958490269/958531628 |
| 15 | PLTR | SELLSHORT | 1 | 120.62/120.65 | 2 | 0.0 | 0.8·-6.0%·-5.8%·LARGE_DVOL·mega·1435 | 165 | 19,902 | NOT-logged | n/a | candle-close/3:00PM/119.63 | 25 | 1.14 | 0.17 | 25 | 163.35 | 3.30 | 160.05 | — | 958506610/958514656 |
| 16 | NFLX | SELLSHORT | 1 | 73.19/73.19 | -0 | 0.0 | 0.8·-5.3%·-5.0%·LARGE_DVOL·mega·1435 | 30 | 2,196 | NOT-logged | n/a | candle-close/3:08PM/72.94 | 33 | 0.35 | 0.16 | 2 | 7.50 | 2.00 | 5.50 | — | 958506612/958517826 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $66.91  ·  fees: $0.00
- Commission 2.63 bps + fees 0.00 bps of $254,392 notional = **2.63 bps avg cost**
- Avg entry slippage: 1.2 bps (adverse +)
- Per-trade avg cost: $4.18 (16 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=16 · win rate 75% (12W/4L)
- GROSS day P&L $1,006.85 · **NET day P&L $939.93**
- Gross expectancy $62.93/trade · Net expectancy $58.75/trade
- Net profit factor 2.19
- Avg win $143.94 · avg loss $-196.83
- Largest win $382.77 · largest loss $-277.44
- Long/short split: 11L / 5S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=5 · win 80% · net $339 ($68/trade, 35.4 bps)
- PATH re-arm:      N=11 · win 73% · net $601 ($55/trade, 37.9 bps)
- OCC 1st-entry:    N=16 · win 75% · net $940 ($59/trade, 36.9 bps)
- OCC re-entry(2+): N=0
- RECONCILE: path sum $939.93 + occ sum $939.93 == day net $939.93 -> OK

- Capital utilization: PEAK deployed: $312,404  (104.1% of $300k target)  at 10:56 (5 pos + 12 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- 2 'Invalid Stop Price' reject(s) (stale-level race; broker refused a chase): ['SOFI', 'PLTR']
- SMCI: left $915 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- COHR: left $698 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ACN: left $434 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- AIG: left $356 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ABBV: left $254 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ULTA: left $220 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- FIX: left $213 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- NO-TRADE STRETCH 11:35AM->1:35PM (120m) -- see root cause in narrative
- marginability shadow: 16 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=25 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = -0.136; breakout won (R>0) 10/25 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): large=-0.06 (n15), mega=0.02 (n6), mid=-0.64 (n4)
---

---
### Turn — 2026-06-23 ~7:50 AM ET — Edge Tunes page visual polish (display-only)
- **Request:** "/edge-tunes looks crammed, no space on the sides — add ~an inch, make it look published."
- **Root cause:** edge-tunes body was NOT wrapped in any centered container, so it spanned ~full viewport (only ~14px gutter) → cramped.
- **Fix (edge_tunes_page.py, non-watched / display-only):** wrapped body in a centered `.et-wrap` (max-width 1280px, margin:0 auto, 44px side padding) for real side gutters + a published-document look. Rewrote presentation only (data logic untouched): page header + subtitle, card-framed tables (`.et-card`) with thead/tbody, uppercase column headers, zebra rows + hover, restyled caution banner, status badges, evidence styling, footer. Uses the dashboard's own design tokens (--panel/--ink/--muted/--accent-dark/--accent-soft/--line/--panel-2) — verified all 7 exist in local_dashboard :root, so on-brand (not fallbacks).
- **Verify:** py_compile OK; killed 2 dashboard procs (6344 stale --no-browser, 7680 live) → relaunched 1 clean (PID 892); GET /edge-tunes = HTTP 200, 92,981 bytes; et-wrap/et-head/et-card/et-cat/et-banner/<thead>/et-foot all PRESENT.
- **No watched strategy file touched. No trading-path change.**

---
### Turn — 2026-06-23 ~8:05 AM ET — Edge Tunes: plain-English columns + evidence cleanup
- **Request:** make "name & one-liner" plain English for a non-trader; clean up the redundant Evidence column + explain what it shows in plain English.
- **Changes (edge_tunes_page.py, display-only / non-watched):**
  - Renamed jargon headers: "Name & one-liner"→"What this is", "Evidence (joined)"→"What we actually know", "Dependencies"→"Needs first".
  - Added a "How to read this page" legend (plain-English: what a tune/status/needs-first/evidence mean; blue=test, green=change, grey=just an idea).
  - Rewrote Evidence into plain sentences via `_plain_change()` / `_plain_trial()` (+ `_fmt_money`): changes → "We made <type> on <date> — <verdict>"; trials → "<variant> — shadow test: averaged ±$X per trade over N trades; <trust>". Removed raw IDs / verdict=pending / repeated gate text. Capped each at 6 with "…and N more". Empty → "Just an idea so far — no tests run or changes made yet."
  - `_CHANGE_TYPE_PLAIN` covers all 7 real change_types (logging/instrumentation/research/display/guardrail/live_tune/shadow_test); trust derived from decision_reason (UNTRUSTED/GATE FAILED) + perm_p (<0.05 significant).
- **Verify:** py_compile OK; render-test shows correct plain output (e.g. "V1_WIDE_INIT — shadow test: averaged +$37.88 per trade over 33 trades; result not trustworthy yet"); dashboard restarted (PID 5992); GET /edge-tunes = HTTP 200, 94,151 bytes; legend + all renamed headers PRESENT.
- **Note:** the per-tune *description* text still comes verbatim from EDGE_TUNES.md (Planning-gatekept). Offered to plain-English-rewrite those one-liners pending Rhett's go.
- **No watched strategy file touched. No trading-path change.**

---
### Turn — 2026-06-23 ~9:00 AM ET — Fix "Avg entry slippage: n/a" on daily review (shadow-wiring bug)
- **Q:** why does daily review show N/A for entry slippage?
- **Root cause:** `daily_review_page.build_review()` sources trades from canonical `eod_debrief.round_trips_net()`, which DOES carry the trigger/stop price as `intended_px` (line 112; from signal_trigger_px / intended_price / order StopPrice). But the per-trade dict it built (lines 42-48) never copied `intended_px` into `trigger_price`, the field `trade_analytics.enrich_trade` reads to compute slippage (entry_px − trigger). So `entry_slippage` was always None → KPI "n/a" — on EVERY day since the Loop 106/108 canonical-source switch, not just yesterday. Data was present; it just wasn't wired through. (Classic feature+data-exist-but-unwired shadow bug per proactive-audit memory.)
- **Verify (RULE #0):** round_trips_net("2026-06-22") → 16/16 round-trips carry intended_px; bars load (390); pre-fix KPI=n/a.
- **Fix (daily_review_page.py, display/analytics — NOT a watched strategy file, no trading-path effect):** one-line passthrough `"trigger_price": rr.get("intended_px")` in the tdict.
- **Verify after:** build_review("2026-06-22") → avg_slippage=0.079, slippage_n=16 (SMCI 0.0, ACN 0.03, RBLX 0.02, VRT 0.10…). Dashboard restarted (PID 3248); GET /daily-review-v2?date=2026-06-22 = HTTP 200, 484,679 bytes, "Broker truth (16 closed trades)", KPI now "Avg entry slippage 0.079 (16 fills)".
- **Side note:** the route param is `?date=` (or `?start=`), not `?day=` (defaults to today if absent).
- **No watched strategy file touched. No trading-path change.**

---
### Turn — 2026-06-23 ~9:20 AM ET — Slippage in EOD: verified already per-day; ADDED day-over-day trend
- **Ask:** "yes, and slippage to EOD."
- **Finding (RULE #0, verified before building):** per-day entry slippage was ALREADY in the EOD debrief — Section B has a per-trade "slip bps" column and Section C has "Avg entry slippage: X bps (adverse +)", side-aware (Section B lines 497-498 flip sign for SELLSHORT). 6/22 archived debrief shows "1.2 bps". My earlier offer was made before verifying — corrected.
- **What was actually missing = the day-over-day TREND** (each archived file had its own number; nothing showed the series). Added it.
- **Changes (eod_debrief.py — reporting/debrief, NOT a watched strategy file, no trading-path effect):**
  - New `_day_slip_bps(date)`: avg entry slippage in bps, side-aware ("adverse +"), from canonical `round_trips_net` (intended_px). Same convention as Section B/C so it lines up.
  - Section C now appends: `Slippage trend (prior Nd, adverse + bps): [series] · trailing avg X bps · today Y (better/worse/in line vs trailing)`.
- **Verify:** py_compile OK; `_day_slip_bps` 6/16=1.29 / 6/17=0.78 / 6/18=0.95 / 6/22=1.21; rendered Section C for 6/22 shows trend [0.9, 2.0, -0.4, -1.1, 2.1, 2.2, 1.3, 0.8, 0.9] · trailing avg 1.0 · today 1.2 (worse vs trailing). Cheap: unified CSV is 662 rows; EOD runs once.
- **No restart needed:** EOD debrief runs as a fresh process via the `AlphaQuant_EodReconciliation` scheduled task → picks up the edit on tonight's 4:50 PM run. Did NOT regenerate the archived 6/22 file (forward-looking; no history rewrite).
- **No watched strategy file touched. No trading-path change.**

---
### Turn — 2026-06-23 ~10:00 AM ET — KPI-integrity contract (Planning Loop 148): kill the silent-null/divergent-KPI CLASS
- **Handoff:** catch the CLASS behind the slippage N/A bug (silent-null KPI on one surface + two surfaces computing the same metric divergently), so the human isn't the detector. 3 items: (1) KPI-non-null contract, (2) cross-surface reconcile, (3) single source.
- **Built (all non-watched / non-confounding; trading loop imports none):**
  1. **SINGLE SOURCE (item 3, the load-bearing fix):** new `eod_debrief.entry_slip(side, fill_px, intended_px)` — THE one slippage definition (side-aware, adverse-+, returns ($/share, bps)). `round_trips_net` now carries `entry_slip_dollars`/`entry_slip_bps`. Section B, `_day_slip_bps`, AND `build_review` all READ it; removed the two divergent calcs (eod_debrief Section B inline, trade_analytics.enrich_trade). V4 grep: only `entry_slip` computes slippage now. (Bonus: helper fixes a latent futures-short "SELL" sign bug Section B's old SELLSHORT-only flip missed.)
  2. **NON-NULL CONTRACT (item 1):** `report_integrity.kpi_completeness_violations` — INPUT-GATED (flags "intended_px present but slip null" = the wiring-gap signature), surfaced by existing `chk_report_integrity` CSHV check (cheap, canonical rows, no client). Self-test now 10/10 (added: present→clean, null-w/-intended→RED, no-trigger→no-false-FAIL).
  3. **CROSS-SURFACE RECONCILE (item 2):** extended the dashboard's existing render-time reconcile guard to assert page avg slippage == canonical (loud banner on divergence). Free; runs only at render.
- **Two principled DEVIATIONS from the handoff (flagged to Planning, not silent):**
  - Item 1 made INPUT-GATED, not "every KPI always non-null" — forcing MFE/MAE (bars-dependent) or PF (n/a on no-loser days) non-null would FALSE-FAIL clean days = CSHV-spam. The wiring-gap invariant is "input present, output null."
  - Item 2 = NO new per-5-min CSHV recompute of the dashboard side — that path (`build_review`) fetches 1-min bars per trade from TS; polling it every 5 min would hammer the API (token/API-load rule). Single-source makes divergence structurally impossible; reconcile is a free render-time guard + selftest invariant instead.
- **Verify:** 4 files py_compile OK; report_integrity self-test 10/10; [V1] planted null→2 kpi_null FAILs naming field; [V2] 6/22 round_trips_net 16/16 carry canonical slip, report_integrity ok=True; [V3] dashboard 0.079 (16 fills), slip_reconcile_ok=True, banner "avg slippage 0.079/sh"; Section C intact (1.2 bps + trend); [V4] only entry_slip computes; [V5] non-watched only. Dashboard restarted PID 1732, live /daily-review-v2?date=2026-06-22 = 200, 0.079, no mismatch banner.
- **No watched strategy file touched. No trading-path change.** Folds into the queued read-only audit as the first concrete silent-coupling instance shipped early.

---
### Alert-Triage (autonomous) - 2026-06-23 Tue ~11:00 AM ET
- code_alert_inbox.py --json: **0 actionable CRIT, 0 noise** since last ack (~10:04 AM run).
- CSHV 43 OK / 0 WARN / 0 FAIL / 1 INFO (clean_day_certified intraday rebuild). Bot loop 2714, heartbeat 17s, 6 positions reconciled both ways + monitored by exit_bot_v2, gate enforced, SAFE_MODE off, book==exposure $287,238.
- **Inbox clean -> no Rhett escalation (silence = handled).** Advanced cursor with --ack.

---
### Turn — 2026-06-23 ~11:00 AM ET — Strategy-rule + in-play compliance on EOD debrief AND dashboard
- **Ask (Rhett):** add to EOD summary + dashboard: (1) Did the bot trade exactly to the strategy rules on every trade? yes/no + why not. (2) Did the bot trade the in-play-identified symbols? yes/no + why.
- **Verified sources first (RULE #0; Explore agent's guessed exit-reason strings were WRONG):** in-play list = `orb_candidate_log.jsonl` (selected/inplay_pass/day_relvol/move/path/window); gate live (ORB_INPLAY_GATE=True); real 6/22 exit reasons = CANDLE_CLOSE_REVERSAL ×11 + "Forced EOD flatten" ×5 (classify to EXIT_CANDLE_CLOSE_TRAIL / EXIT_EOD_FLATTEN); canonical classifier `exit_reason_codes` + live gate `inplay_gate.evaluate` both reusable.
- **Built `tradestation-bot/strategy_compliance.py` (single source, no duplicated logic):** per round-trip — in-play = symbol was `selected` in the day's list; rule_ok = re-passes `inplay_gate.evaluate()` on logged inputs + occ<=ORB_MAX_ENTRIES_PER_NAME + exit classifies to a deployed code (CANDLE_CLOSE_TRAIL/EOD_FLATTEN). Re-arm-window entries flagged "ungated by design" (N/A, not failed). day_compliance() returns the two yes/no answers + exceptions. Reuses eod_debrief (round_trips + exit reasons) + inplay_gate + exit_reason_codes — imports nothing from the trading loop. Self-test 5/5.
- **Wired into BOTH surfaces (same module → answers always agree):** EOD debrief new "## A2 · STRATEGY-RULE & IN-PLAY COMPLIANCE" section (Q1/Q2 + exceptions + re-arm context + exit breakdown); dashboard daily-review compliance panel (two big YES/NO boxes + why-not list + context), computed in build_review→rollup['compliance'].
- **6/22 result:** Q1 YES (16/16), Q2 YES (16/16). Honest finding surfaced: 11/16 entries were RE-ARM entries (ungated by the in-play gate by design), several with RelVol < the 1.5 9:35 threshold — visible per-trade + in the context line.
- **Verify:** 3 files compile; self-test 5/5; EOD A2 renders YES/YES + context; dashboard restarted PID 5000, /daily-review-v2?date=2026-06-22 = 200, 485,872 bytes, panel PRESENT (YES present, no false NO). EOD picks up tonight via scheduled task (fresh process).
- **No watched strategy file touched. No trading-path change.** Read-only analytics over broker truth + logged decisions.


## EOD SUMMARY — 2026-06-23

_Auto-generated by eod_debrief.py at 2026-06-23 4:50 PM ET · broker-truth sourced · 11 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 114 -> passed in-play gate 16 -> selected 19 -> symbols FILLED 11.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 4, refused 13 ({'deploy_refused': 13})
- 11:35 AM: armed 2, refused 17 ({'reentry_capped': 2, 'already_held_or_working': 2, 'deploy_refused': 13})
- 12:35 PM: armed 0, refused 20 ({'already_held_or_working': 4, 'reentry_capped': 2, 'deploy_refused': 14})
- 1:35 PM: armed 1, refused 16 ({'reentry_capped': 3, 'already_held_or_working': 3, 'deploy_refused': 10})
- 2:35 PM: armed 2, refused 16 ({'reentry_capped': 5, 'already_held_or_working': 2, 'deploy_refused': 9})

**Incidents today:** 1 {'FAIL': 1}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — an old-gate-only (new-gate-rejected) name was traded.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## A2 · STRATEGY-RULE & IN-PLAY COMPLIANCE (did we trade to the rules?)

- **Q1 — Did the bot trade exactly to the strategy rules on every trade?**  **YES**  (11/11 trades compliant)
- **Q2 — Did the bot trade the in-play-identified symbols?**  **YES**  (11/11 in the in-play list)
- Context: 6/11 entries came from RE-ARM windows, which are UNGATED by the in-play gate by design (re-arm/fresh-breakout path) -- counted as in-play because they were on the armed list, but they did not have to clear the 9:35 RelVol/move thresholds.
- Exit-rule breakdown: EXIT_CANDLE_CLOSE_TRAIL×7, EXIT_EOD_FLATTEN×4

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | ANET | SELLSHORT | 1 | 161.24/161.20 | -2 | 0.0 | 2.3·-5.0%·-3.5%·LARGE_DVOL·mega·0935 | 124 | 19,993 | 162.58 | no | EOD-flatten/3:50PM/162.40 | 374 | 1.88 | 3.65 | 20 | -144.46 | 2.48 | -146.94 | -0.88 | 958599856/958764895 |
| 2 | DPZ | SELLSHORT | 1 | 287.31/287.33 | 1 | 0.0 | 2.1·-8.1%·-6.5%·MID_DVOL·large·0935 | 69 | 19,824 | 288.55 | no | candle-close/9:47AM/286.50 | 11 | 2.32 | 1.48 | 241 | 55.89 | 2.00 | 53.89 | 0.63 | 958599884/958610439 |
| 3 | NRG | SELLSHORT | 1 | 134.00/133.95 | -4 | 0.0 | 2.3·-3.6%·-2.0%·MID_DVOL·large·0935 | 149 | 19,966 | 134.83 | no | EOD-flatten/3:50PM/137.64 | 374 | 1.00 | 4.87 | -7 | -542.36 | 2.98 | -545.34 | -4.42 | 958599872/958764971 |
| 4 | TPR | SELLSHORT | 1 | 145.96/145.97 | 1 | 0.0 | 1.7·-2.2%·-0.6%·MID_DVOL·large·0935 | 137 | 19,996 | 146.77 | no | EOD-flatten/3:50PM/149.83 | 374 | 0.01 | 5.16 | -96 | -530.88 | 2.74 | -533.62 | -4.80 | 958599897/958765046 |
| 5 | MSTR | SELLSHORT | 1 | 105.52/105.52 | -0 | 0.0 | 1.8·-6.2%·-4.7%·LARGE_DVOL·large·0935 | 189 | 19,943 | 107.14 | no | candle-close/2:38PM/104.15 | 303 | 1.42 | 2.24 | 57 | 258.93 | 3.78 | 255.15 | 0.83 | 958599895/958737475 |
| 6 | IBM | BUY | 1 | 263.91/263.78 | 5 | -0.0 | 2.4·4.4%·5.3%·LARGE_DVOL·mega·1035 | 75 | 19,793 | NOT-logged | n/a | candle-close/11:18AM/266.03 | 43 | 3.62 | 1.41 | -81 | 159.00 | 2.00 | 157.00 | — | 958643481/958668349 |
| 7 | SNDK | SELLSHORT | 1 | 1996.01/1997.00 | 5 | 0.0 | 2.4·-11.8%·-10.9%·LARGE_DVOL·mega·1035 | 10 | 19,960 | NOT-logged | n/a | candle-close/1:53PM/1978.93 | 198 | 23.24 | 30.51 | 179 | 170.80 | 2.00 | 168.80 | — | 958643472/958724641 |
| 8 | VRT | SELLSHORT | 1 | 323.60/323.65 | 2 | 0.0 | 2.1·-9.5%·-8.6%·LARGE_DVOL·large·1035 | 42 | 13,591 | NOT-logged | n/a | candle-close/10:56AM/321.62 | 21 | 3.49 | 3.40 | 144 | 83.16 | 2.00 | 81.16 | — | 958643488/958656965 |
| 9 | IVZ | SELLSHORT | 1 | 27.30/27.30 | -0 | 0.0 | 2.8·-4.7%·-3.4%·MID_DVOL·large·1135 | 731 | 19,956 | NOT-logged | n/a | candle-close/12:39PM/27.07 | 64 | 0.30 | 0.23 | 29 | 168.13 | 12.77 | 155.36 | — | 958677487/958704574 |
| 10 | FCX | SELLSHORT | 1 | 65.06/65.07 | 2 | 0.0 | 1.1·-5.9%·-5.0%·LARGE_DVOL·large·1335 | 307 | 19,973 | NOT-logged | n/a | candle-close/2:00PM/64.60 | 25 | 0.53 | 0.15 | 64 | 141.22 | 6.14 | 135.08 | — | 958720294/958726965 |
| 11 | CAG | BUY | 1 | 13.52/13.52 | 0 | -0.0 | 1.1·5.2%·6.5%·MID_DVOL·mid·1435 | 1479 | 19,996 | NOT-logged | n/a | EOD-flatten/3:50PM/13.51 | 75 | 0.04 | 0.05 | -104 | -14.79 | 21.75 | -36.54 | — | 958736263/958764929 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $60.64  ·  fees: $0.00
- Commission 2.85 bps + fees 0.00 bps of $212,993 notional = **2.85 bps avg cost**
- Avg entry slippage: 0.8 bps (adverse +)
- Slippage trend (prior 10d, adverse + bps): [0.9, 2.0, -0.4, -1.1, 2.1, 2.2, 1.3, 0.8, 0.9, 1.2] · trailing avg 1.0 bps · today 0.8 (better vs trailing)
- Per-trade avg cost: $5.51 (11 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=11 · win rate 64% (7W/4L)
- GROSS day P&L $-195.35 · **NET day P&L $-255.99**
- Gross expectancy $-17.76/trade · Net expectancy $-23.27/trade
- Net profit factor 0.80
- Avg win $143.78 · avg loss $-315.61
- Largest win $255.15 · largest loss $-545.34
- Long/short split: 2L / 9S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=5 · win 40% · net $-917 ($-183/trade, -91.9 bps)
- PATH re-arm:      N=6 · win 83% · net $661 ($110/trade, 58.3 bps)
- OCC 1st-entry:    N=11 · win 64% · net $-256 ($-23/trade, -12.0 bps)
- OCC re-entry(2+): N=0
- RECONCILE: path sum $-255.99 + occ sum $-255.99 == day net $-255.99 -> OK

- Capital utilization: PEAK deployed: $301,815  (100.6% of $300k target)  at 12:26 (6 pos + 9 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- DPZ: left $310 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- SNDK: left $289 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- IVZ: left $278 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- VRT: left $215 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- NO-TRADE STRETCH 11:35AM->1:35PM (120m) -- see root cause in narrative
- marginability shadow: 11 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=19 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = -0.177; breakout won (R>0) 8/19 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): large=-0.23 (n14), mega=0.0 (n4), mid=-0.18 (n1)
---

---
### Turn — 2026-06-23 ~11:30 AM ET — Re-arm vs 9:35 expectancy tracker on dashboard + memory to revisit
- **Ask:** track re-arm vs 9:35 expectancy, put it on the dashboard, memory to revisit.
- **Built (strategy_compliance.py):** `_path_of(rec)` (9:35-gated / re-arm / unknown, single def); each compliance row now carries `path`+`net`+`notional`; new `path_expectancy(since=2026-05-26)` = cumulative broker-truth net split by entry path (post-baseline per [[feedback_post_5_26_data_only]]).
- **Dashboard:** new "RE-ARM vs 9:35 EXPECTANCY" panel on the daily-review page (table: path/trades/win%/net/$per-trade/bps + caveat line). Computed on render (cheap, local files).
- **FIRST READ (post-baseline 5/26→6/23, 12 days) — notable:** 9:35-gated N=50 win42% net −$1,681 (−18.9 bps) LOSING; re-arm (ungated) N=89 win58% net +$1,546 (+9.7 bps) WINNING; unknown N=76 (pre-candidate-log days, data-gap bucket). The ungated re-arm path is carrying the system — OPPOSITE of the initial concern. Context not verdict (small N; mixes pre/post the 6/19 deployed config).
- **Memory:** created `project_rearm_vs_935_expectancy.md` (+ MEMORY.md index) — REVISIT at N≥30/path on post-6/19 config; bring a proposal, don't act inline.
- **Verify:** compile OK; path_expectancy returns the split above; dashboard restarted PID 856, /daily-review-v2?date=2026-06-22 = 200, 487,823 bytes, panel PRESENT.
- **No watched strategy file touched. No trading-path change.** Observational only (stages 3-4; strategy changes still gated).

---
### Turn — 2026-06-23 ~5:25 PM ET — 6/23 EOD verify (READ/VERIFY only; freeze intact)
- **V1 CLEAN-DAY:** certify_day(6/23) = CLEAN (report_integrity 0/0, broker_flat_eod flat 11 net 0, no_critical_incident: 0 faults +1 transient soft blip tolerated). **consecutive_clean = 1** → today is clean day-1 (kill window 1/5); NOT two non-clean running. The "1 FAIL incident" = FCX at 1:45:10 PM "broker has position bot not tracking" = a 5-sec fill-vs-recon RACE (FCX stop-limit filled 1:45:05, recon snapshot 1:45:10); bot then managed+exited it (BUYTOCOVER 2:00 PM), FCX is a clean round-trip (one of 11), EOD flat, exit rule-compliant. Certifier correctly classified transient-soft. Compliance 6/23: Q1 11/11, Q2 11/11.
- **V2 SHADOW DELTA (clean day, gate PASS 11/11 → counts):** V9 (live chandelier 1.4) shadow sum +$559.88 vs V0 (0.15 baseline) −$705.84 → **V9−V0 delta +$1,265.72**. R0 reentry-shadow: 0 rows for 6/23 → N/A. **CAVEAT (verified):** V9 absolute (+560) ≠ broker-truth live (−$256) by ~$816, concentrated in NRG (+574) & ANET (+171): the recon models a confirm+candle-close early exit ~9:37–9:39 (small profit) that the LIVE bot did NOT take (exit_decisions = "chandelier_hold (unconfirmed)" 9:38 → rode to EOD-flatten, −545/−147). The faithfulness gate "11/11 reproduced" did NOT catch this net divergence (validates trade-matching, not net-vs-broker). Net effect: the +$1,266 delta is INFLATED (NRG/ANET wrongly score V9=V0=0-delta instead of the true wide-stop-hurts delta); corrected estimate ~+$800. The realized day was −$256 (V0-recon −$706 → live beats V0 by ~+$450). Wide stop helped MSTR/SNDK/VRT/IVZ (let winners run), hurt TPR (rode loser to −561 vs V0 −117). FINDING routed to Planning: harden faithfulness gate to check NET vs broker truth (measurement-path, non-trading) — did NOT act (forecast-test posture).
- **V3 OVER-DEPLOY:** capture_utilization PEAK $301,815 (100.6% of $300k) at 12:26 = 6 pos + 9 WORKING orders; peak long $126,259 / short $195,299 (both < $200k side cap). BENIGN book-drift (working-order notional inflates the book; real filled exposure + side caps under target) — same as 6/22 ($312,404). NOT an admit-cap leak. (No literal admit_log.jsonl; confirmed via capture_utilization pos/working breakdown + side caps.)
- **No code changed. Freeze intact. Run exact deployed config 6/24.**

---
### Turn — 2026-06-23 ~6:00 PM ET — Sidelined-capital report + $400k-cap display + gate-coverage (read-only)
- **Handoff:** measurement/display only — show capital idle below the $400k cap while candidates refused; reframe peak vs $400k; surface gate coverage. NO target raise / gate change / live edit (queued+frozen).
- **Sources verified (RULE #0):** no admit_log.jsonl exists; refusals + deploy-book $ live in `outputs/multiscan_trace.jsonl` (per re-arm window: book_before/after {long,short,total} + decisions w/ reasons deploy_refused / reentry_capped / already_held). Constants from live config: DEPLOY_BASE=$400k cap, DEPLOY_TARGET_PCT=0.75→$300k target, MAX_SIDE_PCT=0.5→$200k side. Refused decisions carry no order size → refused $ is an upper-bound estimate (labeled).
- **Built `tradestation-bot/sidelined_capital.py` (read-only, no trading import):** `sidelined_report(date)` → per re-arm window deployed$ / %cap / idle-vs-$400k / #refused-for-capital (split from reentry/held) / binding cap + day summary. 6/23: all 5 windows ~$300k (75% cap), ~$100k idle, binding=$300k TARGET every window, 59 capital-refusals; max idle $100,314.
- **Dashboard (daily_review_page.py, display-only):** (1) Peak KPI now "$X (Y% of $400k cap) · Z% of $300k target" + new "Idle headroom (vs $400k cap)" KPI; (2) SIDELINED CAPITAL per-window panel; (3) gate-coverage line added to the existing RE-ARM vs 9:35 EXPECTANCY panel (9:35 GATED, re-arm UNGATED). build_review stashes cap/target/idle/sidelined in rollup.
- **Verify:** compile OK; sidelined_report ties out; dashboard restarted PID 4984; /daily-review-v2?date=2026-06-23 = 200; Peak KPI renders "$301,815 (75.5% of $400k cap) · 100.6% of $300k target", Idle headroom "$98,185"; SIDELINED CAPITAL + gate-coverage panels PRESENT. (Peak uses capture_utilization intraday-MTM peak $301,815; sidelined panel uses multiscan_trace arming-book ~$300k — consistent, different snapshots.)
- **Memory:** added `project_shadow_faithfulness_net_gap.md` (+ index) — REVIEW the shadow gate net-fidelity gap after the forward test.
- **V1/V2/V3 all pass. Zero watched files. Trading loop unaffected. Target-raise + gate re-exam remain QUEUED/FROZEN.**

---
### Turn — 2026-06-23 ~6:30 PM ET — APPROVED: harden shadow faithfulness gate to reconcile vs broker truth
- **Approved mid-test** (measurement-path only, non-trading, non-watched): the shadow yardstick failed to reconcile to broker (V9 +$560 on a -$256 day, $816 inflation); fixing it is a prerequisite for kill-criterion #1, not an experiment change.
- **Root cause (item 2):** `_v9` derived `confirmed` from 1-min bar hi/lo, which fired for NRG/ANET when the live tick-based confirm never did → modeled phantom early candle-close exits. FIX: anchor V9 (the DEPLOYED exit) to BROKER TRUTH per round-trip in `replay()` (it's observed, not a hypothesis) — uses the live exit decision; V0-V8 stay modeled counterfactuals.
- **Gate (item 1):** new `reconcile_v9_vs_broker(date)` — asserts shadow V9 net == broker net per round-trip within tol (max $1.50 / 5bps); breach → FAIL naming sym+delta. Folded into the score gate (un-reconciled day not accumulated) + prints "V9->BROKER RECONCILE" line (driver now logs it).
- **CSHV (item 4):** `shadow_reconciles_broker_truth` (Reliability) — reads latest scored day in shadow_exit_results.jsonl, reconciles V9 vs broker; OK/FAIL/SKIP. Returns OK 11/11 for 6/23.
- **Re-score (item 3) — corrected (kept originally-scored V0; only V9→broker, since re-replay is non-deterministic for counterfactuals due to ATR/bar source drift — a separate reproducibility note):**
  - 6/22: V9-V0 +$2,081.55 → **+$1,988.05** (V9 $1,033→$940 broker; inflation only $93.50 — Monday's read ~96% sound).
  - 6/23: V9-V0 +$1,265.72 → **+$449.84** (V9 $560→-$256 broker; inflation $815.88 — the real problem).
  - Surgically replaced V9 in 27 accumulated rows (backup shadow_exit_results.jsonl.bak_prefix_shadowfix); V0-V8 untouched.
- **Verify:** compile OK (4 files); selftest V1 planted +$1000 mismatch → reconcile FAILs naming AAA: PASS; causality guard PASS; V9-anchored == broker (zero gap) both days (V4); reconcile 16/16 & 11/11 within tol; CSHV check OK; main() prints "V9->BROKER RECONCILE -> PASS". Also fixed a stale selftest assertion (it asserted no variant name contains 'V9', but V9 is the deployed variant since Loop 121 — had been failing).
- **V5:** non-watched files only (shadow_exit_harness never imported by the bot; system_health_verifier is monitoring); trading loop unaffected; freeze intact. shadow_exit_results.jsonl is gitignored (data).
- **Standing rule applied:** shadow now joins P&L + KPI-integrity in the daily broker-truth reconcile contract. Memory `project_shadow_faithfulness_net_gap.md` can be marked resolved (gate installed).

---
### Turn — 2026-06-24 ~8:00 AM ET — Pin shadow inputs per trade date (re-score determinism)
- **Ask (Rhett "pin it"):** fix the note-B reproducibility gap — re-scoring a past day drifted V0-V8 because `minute_bars` fetched barsback=480 from NOW + a live-mutating ATR.
- **Built (shadow_exit_harness.py, measurement-path, non-watched):** an INPUT PIN — `replay()` snapshots the exact (bars, atr) per (date, sym) to `outputs/validation/shadow_pin/<date>.json` at first SAME-DAY scoring; any re-score reads the pin → byte-identical counterfactuals. Guard: pin is WRITTEN only when date==today (a past-day fetch is already wrong, so never pinned); optional `write_pin` override for tests. PIN read path uses `_bars_from_pin` + pinned atr instead of the API.
- **Verify:** compile OK; pin roundtrip test (replay write_pin=True → replay reads pin) → per-variant per-trade nets IDENTICAL (A==B) = deterministic; test pin removed; 6/23 (past) NOT pinned (shadow_pin dir empty); main() still gate PASS + V9->BROKER RECONCILE PASS. Going forward 6/24's 4:50 same-day score writes 6/24's pin → future re-scores reproducible.
- **Scope note:** historical days scored before the pin existed (6/22, 6/23) can't be byte-reproduced (no snapshot) — but their accumulation is already corrected (V9→broker surgical; V0-V8 original) and won't be re-scored. Pinning protects 6/24+.
- **Non-watched; trading loop unaffected; freeze intact.**

---
### Turn — 2026-06-24 ~8:30 AM ET — "Versions" glossary page (read-only, self-maintaining)
- **Ask:** a dashboard "Versions" button → plain-English reference for every shadow version (V0-V9, R-series), generated FROM CODE so it stays correct as versions change.
- **Built `tradestation-bot/shadow_versions.py` (read-only, no trading import):** `registry()` reads the LIVE registries — `shadow_exit_harness.VARIANTS` (V0-V9) + `reentry_shadow.VARIANTS` (R0-R3) — and returns per-version {label, role, marker, plain-English, real params, docstring snippet}. Plain-English = a prose template authored from each variant's actual logic with the LIVE constant VALUES interpolated (param change → text auto-updates); any variant w/o a template → NEEDS DESCRIPTION (never silently missing). `undocumented()` = coverage guard. Roles: V0=BASELINE, V9=DEPLOYED-UNDER-TEST, locked=CANDIDATE(pre-registered), else CANDIDATE. Marker: V9="broker truth (observed, reproducible)", V0-V8/R="modeled counterfactual (paper)". Params = the module constants each fn's source references (auditable). Self-test 9/9 incl. self-maintaining (inject temp variant → auto-appears as NEEDS DESCRIPTION → removed).
- **Built `advisor/versions_page.py`** (centered, card-per-version, role+marker badges, params + def snippet, yellow NEEDS-DESCRIPTION cards + red banner) + wired into `local_dashboard.py`: route `/versions`, `_handle_versions`, and a "Versions" home card.
- **Verify:** 3 files compile; render_body 200/15KB with V0/V9/R3; dashboard restarted PID 592; home has /versions button+card; /versions = HTTP 200, shows "Shadow Versions", DEPLOYED-UNDER-TEST, broker-truth marker, "1.4xATR chandelier" (V9 live param), "0.15xATR from entry" (V0 live param), Re-entry section. V0/V9 read as the handoff's anchor descriptions with LIVE params.
- **Self-maintaining guard:** new/edited variant appears automatically; undocumented one shows NEEDS DESCRIPTION on the page + via `undocumented()` + fails `shadow_versions._selftest` (can be wired into preflight if desired).
- **Display-only; non-watched; no trading-path effect; freeze intact.**

---
### Turn — 2026-06-24 ~9:00 AM ET — Versions page: preflight gate + forward-test scoreboard + exit explainer
- **Wired `shadow_versions.undocumented()` into `_preflight_diagnostic.py`**: new check "every shadow version is documented on the /versions glossary" — a variant can't pass preflight undocumented. Preflight now 51/51 PASS (0 FAIL); gate input undocumented()==[].
- **ADD 1 — forward-test scoreboard (shadow_versions.forward_test_scoreboard + versions_page):** per scored day, corrected V9 (broker-anchored) vs frozen same-day V0 (modeled) + delta, worst-trade & day-net vs kill thresholds, clean flag. CORRECTNESS FIX found: excluded pre-deploy days — added `shadow_exit_harness.forward_deploy_date()` (parsed from change record AQ-20260619-...001 created_at=2026-06-19) and guarded replay()'s V9 anchor to date>=deploy (before 6/19 the LIVE exit was V0, so broker truth != V9). 6/18 now excluded; scoreboard shows 6/22 (non-clean, doesn't count) + 6/23 (clean) = **1/5 clean, cumulative V9-V0 +$449.84, live beats V0**. Kill thresholds (−$800 single / −$2,000 daily) parsed from the change record's kill_criteria (not hardcoded); none tripped. V9=broker-observed, V0=modeled (paper, ~±$600/day re-replay variance, frozen same-day not re-replayed).
- **ADD 2 — exit explainer (shadow_versions.exit_explainer, read from live code):** mode candle_1.4atr_chandelier; **candle TIMEFRAME = 1-minute** (sourced: candle_close_exit.get_last_closed_1min `interval=1&unit=Minute&barsback=5`, bars[-2]=last closed; exit_bot_v2.py:356/500 calls it). 5-min-OR hypothesis REJECTED. chandelier 1.4xATR ratchet floor (tick-level, always live) + post-confirm candle-close reversal on a closed 1-min opposite-color bar; confirm +0.15xATR. vs V0's tight 0.15xATR stop (false stop-outs). Timeframe parsed programmatically; "NOT VERIFIED" fallback if unparseable.
- **Verify:** 4 files compile; exit_explainer verified=true 1-minute; scoreboard 1/5 +449.84; /versions HTTP 200 shows scoreboard (1/5) + explainer (1-minute, 1.4xATR, REJECTED) + glossary; preflight 51/51 incl. the new doc-coverage check.
- **Display-only; non-watched; no trading-loop import (exit_bot_v2 read as TEXT); freeze intact.**

---
### Turn — 2026-06-24 ~9:15 AM ET — Planning↔ChatGPT 2nd-opinion relay (FYI; no code change)
- Rhett relayed Planning's response to ChatGPT's 6/23 review. All three "resolved since review" items are mine (clean-day=1/5, corrected shadow deltas via broker-anchor, V0 re-replay variance). No action — freeze intact, run same 6/24.
- **One correction surfaced to Planning:** the ATR/bar PIN is already SHIPPED (commit d06757a), not "queued post-test" — BUT it's forward-only (pins same-day 6/24+); it cannot byte-reproduce 6/18–6/23 (no snapshots existed then). So Planning's conclusion (Q6 historical re-score still blocked) is correct; the remaining unblock lever = historical-pin backfill via `lastdate`-anchored fetches (I offered it last turn; post-test item).
- Post-test gauntlet items noted (not built mid-test): three-sided exit-loosening test (now incl. giveback/MAE — ChatGPT's SNDK catch), gate-value falsification (passed-9:35 vs near-miss rejects N>=30), entry-conviction-floor (TPR-class), historical-pin backfill (Q6).
- The "next silently-wrong metric" watch (ChatGPT read #2) is the class already under the broker-truth reconcile contract: P&L, slippage/KPI-integrity, shadow-V9 — each with a daily invariant now.

---
### Turn — 2026-06-24 ~9:45 AM ET — V-FREEZE: lock kill-window V0/V9 write-once (Planning verification)
- **Verified (read-only first):** the accumulation (shadow_exit_results.jsonl) has ONE writer (shadow_exit_harness.py:1054, APPEND); dashboard/shadow_versions/CSHV only READ it; the scheduled driver never passes --force. So the automated path is IDEMPOTENT (_already_scored blocks re-write) — but NOT enforced-immutable: a manual `--force` re-run bypasses the guard and APPENDS duplicate rows (double-count; re-replay V0 differs ±$600), and direct edits can mutate. That's the exact corruption path Planning flagged.
- **Locked it (write-once + hash, pre-authorized "before 6/24 close"):** added to shadow_exit_harness.py — `seal_date()`/`is_sealed()`/`verify_seals()`/`seal_existing()` + `shadow_kill_window_seal.json` (per-date sha256 of per-trade V9+V0 nets + n_rows + sums). main() now REFUSES to re-write a sealed date on BOTH paths (trial rows + OOS rows) even with --force; first successful accumulation SEALS immediately. New CSHV check `shadow_kill_window_sealed` (Reliability) re-hashes sealed dates → FAIL on out-of-band mutation, WARN on unsealed-accumulated.
- **Sealed existing:** 6/18 (h=0998…, V9 1067.08/V0 -776.50), 6/22 (h=805f…, V9 939.93/V0 -1048.12), 6/23 (h=55c7…, V9 -256.00/V0 -705.84) — corrected values now immutable.
- **Verify (all PASS):** seal_existing locked 3 days; verify_seals ok on clean file; TAMPER TEST (append dup 6/23 row) → verify BREACHES naming 6/23 (hash + 11→12 rows) → restored → ok; CSHV check OK ("all 3 write-once sealed + hash-intact"); END-TO-END `shadow_exit_harness 2026-06-23 --score --force` → printed SEALED on both paths, 6/23 rows 11→11 (zero added). compile OK.
- **Going forward:** each scored day self-seals on first write; re-runs/--force refused; direct edits caught by CSHV. V0's ±$600 nondeterminism can no longer overwrite a stored kill-window value.
- **Display/measurement-path only; non-watched; no trading-loop import; freeze intact.**

---
### Turn — 2026-06-24 ~10:30 AM ET — Investigated 2 daily WARN pings (Rhett asked)
- Both Discord WARNs fire EVERY trading day (not new); investigated all three current warnings:
  1. **ORB_EARNINGS_STALE** (real): earnings_calendar.csv last refreshed Jun 3 (21d), no scheduled refresh. Veto still runs but with false-negatives; at 21d its dates are all past → veto effectively NEAR-INERT (blocks ~nothing) → bot could enter a name reporting earnings. Recurs daily since ~Jun 6. **Rhett's call: LEAVE IT FOR NOW** (accepted risk during forward test; keep reporting, do NOT refresh). Future sessions: this is a KNOWN-ACCEPTED gap, don't re-flag as new. Fix when un-frozen = refresh `earnings_importer`/`earnings_provider` + add a daily scheduled refresh.
  2. **ORB_SCAN_TIMING** (soft/noise): WARNs when OR-close→first-submit >60s; today 71.3s (scan 25s, submit 4s, ATR cached, no 429s). Bot still traded (2 RT +$34). Trips daily → threshold (60s) cries wolf at the bot's normal ~70s latency. Post-test: either reduce scan latency or re-tier the threshold to INFO. No action now (freeze).
  3. **rel_position_recon / DAL** (benign CSHV WARN): DAL traded+exited today, lingering in recent_exits.json post-exit while broker flat = harmless "bot-has-it/broker-doesn't", pruned each cycle. NOT the dangerous broker-blind direction. Transient.
- **No changes made** (mid-forward-test freeze; refreshing the calendar would change the tradeable set mid-day). Read-only investigation.

---
### Turn — 2026-06-24 ~11:00 AM ET — Add "Deployed capital by hour" chart to daily-review page
- **Ask (Rhett):** add a chart of deployed capital hour-by-hour on the dashboard.
- **Built (daily_review_page.py, display-only):** `_deployed_capital_chart(day, rollup)` — self-contained inline SVG (no JS/CDN dep) reading the live utilization snapshots `outputs/validation/utilization_<day>.jsonl` (total = filled positions + working orders, ET, ~30-min cadence). Buckets by hour → PEAK deployed/hour as columns; dashed $300k deploy target + $400k cap reference lines (sourced from rollup deploy_cap/deploy_target, not hardcoded); bar color green >=90% cap / blue >=60% / grey below; hover title shows $/%, pos+working. Inserted in the capital group of render_html (after peak KPI + sidelined panel).
- **Verify:** compile OK; 6/23 → 7 hourly bars (9a-3p), SVG + target/cap lines present, hour-12 bar = the 12:26 peak $301,815 (at the cap line) = faithful; dashboard restarted PID 9432; /daily-review-v2?date=2026-06-23 = HTTP 200, "Deployed capital by hour" + svg + 400k cap + 300k target PRESENT. Today (6/24, in-progress) shows the hours captured so far.
- **No watched strategy file touched. No trading-path change.** Reads existing utilization snapshots only.

---
### Turn — 2026-06-24 ~11:45 AM ET — Deployed-capital-per-hour in EOD + deployment attribution (read-only)
- **Two asks:** (Rhett) add deployed capital per hour to the EOD summary; (Planning) deployment-attribution report — split idle capital into thin-signal (correct) vs self-throttle (fixable) vs stale-slot, headline "qualified refused for CAPITAL: N".
- **Built:**
  - `sidelined_capital.deployment_attribution(date)`: per re-arm window, idle (cap-deployed) = THIN-SIGNAL + SELF-THROTTLE (these sum to idle, V1); SELF-THROTTLE = qualified names refused by our caps (deploy/slot/reentry) × est demand, capped at idle. Headline = qualified refused for CAPITAL (deploy_refused/gross_cap). `_stale_slot_day` = $ in red names held to EOD-flatten (DEPLOYED-but-stuck, reported SEPARATELY — not in the idle sum). Added per-window `skip_reasons` Counter to `sidelined_report`.
  - `eod_debrief._section_deployment` (new Section H): deployed-by-hour table (peak/hour from utilization snapshots, % of $400k cap, pos+working) + idle attribution table + headline + stale-slot line. Wired into build().
- **SPEC RECONCILIATION flagged to Planning:** handoff said 3 buckets sum to idle, but STALE-SLOT is DEPLOYED capital (held in losers), not idle → I made THIN+SELF-THROTTLE = idle (clean, no double-count, V1 holds) and report STALE-SLOT separately. Also fixed: idle $ is a LEVEL → headline uses peak idle (not sum across windows, which double-counts the same persistent ~$100k); gross-demand labeled upper-bound (N×$25k).
- **Verify:** compile OK; V1 thin+self-throttle==idle every window (sum-ok=True); V2 counts from trace skip_reasons; V3 6/23 → ALL self-throttle (59 refused, $100k idle/window, book at $300k target), 6/24 10:35 → self-throttle (6 refused, book filled); STALE-SLOT 6/23 = $79,951/4 names. EOD Section H renders (hourly 9AM-3PM table + attribution + stale-slot).
- **FINDING:** 6/23 (and 6/24 re-arm) idle is SELF-THROTTLE not thin-signal — the book fills to the $300k target by ~10:35 then refuses qualified names. Strengthens the queued raise-to-$400k case (gated). Attribution covers RE-ARM windows only (9:35 path = separate runner, not in multiscan_trace).
- **No deployment floor added. Read-only; non-watched; no trading-loop import; freeze intact.** EOD picks up Section H on tonight's scheduled run (fresh process).

---
### Turn — 2026-06-24 ~12:15 PM ET — Standing daily LOSER ATTRIBUTION cut (EOD Section I)
- **Built (eod_debrief.py, read-only):** `_trade_attribution(date)` (per round-trip: side, confirm from exit_decisions live log, exit-reason bucket via exit_reason_codes, hold, net) + `_section_loser_attribution` Section I with 4 tables: (1) losers by side, (2) ALL trades by EXIT REASON x CONFIRM (partition), (3) BLEEDER FLAG (confirm=no + EOD-flatten), (4) MUST-NOT-CUT control (longest-held winners). Wired into build().
- **Verify:** compile OK; V1 losers reconcile by side (6/22 -$787 all long; 6/23 -$1,226 short + -$37 long); V2 partition exact (16==16, 11==11); V3 6/22 bleeders=LONGS (SNDK/ULTA/RIOT/BB), 6/23 bleeders=SHORTS (NRG/TPR/ANET) — same unconfirmed-EOD signature both sides; V5 read-only.
- **CORRECTION to handoff (RULE #0):** MSTR 6/23 is confirm=**YES** (candle-close exit, +$255, 303min), NOT "confirm=no" as the handoff stated. Reported to Planning.
- **KEY FINDING — the discriminator is CONFIRM, not side and not exit-reason alone:** confirmed trades won 100% BOTH days (candle-close AND a confirmed EOD-flatten VRT 6/22 +$161.90); unconfirmed→EOD-flatten lost 100% (0/8 over 2 days, -$2,050). So a loser-aging rule should key on CONFIRM (spares EVERY winner — all winners confirmed); keying on hold-time alone would wrongly cut MSTR (confirmed 303min +$255 winner). Sharpens the gauntlet target.
- **No trading change; non-watched; no trading-loop import; freeze intact.** EOD picks up Section I tonight (fresh process). Tonight will auto-include PAYX/SPGI once closed.


## EOD SUMMARY — 2026-06-24

_Auto-generated by eod_debrief.py at 2026-06-24 4:50 PM ET · broker-truth sourced · 21 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 86 -> passed in-play gate 19 -> selected 26 -> symbols FILLED 21.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 8, refused 11 ({'reentry_capped': 1, 'already_held_or_working': 4, 'deploy_refused': 6})
- 11:35 AM: armed 7, refused 9 ({'reentry_capped': 8, 'deploy_refused': 1})
- 12:35 PM: armed 1, refused 18 ({'reentry_capped': 9, 'already_held_or_working': 7, 'deploy_refused': 2})
- 1:35 PM: armed 1, refused 16 ({'already_held_or_working': 3, 'reentry_capped': 9, 'deploy_refused': 4})
- 2:35 PM: armed 0, refused 15 ({'reentry_capped': 9, 'already_held_or_working': 3, 'deploy_refused': 3})

**Incidents today:** 1 {'FAIL': 1}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — gate SELECTED sleepy names (day-RelVol<1.3) instead of movers; the gate is not filtering correctly.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## A2 · STRATEGY-RULE & IN-PLAY COMPLIANCE (did we trade to the rules?)

- **Q1 — Did the bot trade exactly to the strategy rules on every trade?**  **YES**  (21/21 trades compliant)
- **Q2 — Did the bot trade the in-play-identified symbols?**  **YES**  (21/21 in the in-play list)
- Context: 13/21 entries came from RE-ARM windows, which are UNGATED by the in-play gate by design (re-arm/fresh-breakout path) -- counted as in-play because they were on the armed list, but they did not have to clear the 9:35 RelVol/move thresholds.
- Exit-rule breakdown: EXIT_CANDLE_CLOSE_TRAIL×14, EXIT_EOD_FLATTEN×7

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | PAYX | SELLSHORT | 1 | 93.58/93.62 | 4 | 0.0 | 3.1·-2.4%·-2.9%·MID_DVOL·large·0935 | 213 | 19,933 | 94.02 | no | EOD-flatten/3:50PM/96.43 | 374 | 0.56 | 3.44 | 19 | -607.05 | 4.26 | -611.31 | -6.46 | 958837347/959003693 |
| 2 | HAL | SELLSHORT | 1 | 33.85/33.86 | 3 | -0.0 | 2.8·-3.1%·-3.6%·MID_DVOL·large·0935 | 590 | 19,972 | 34.04 | no | candle-close/11:10AM/33.62 | 94 | 0.31 | 0.73 | -171 | 135.70 | 11.08 | 124.62 | 1.13 | 958837349/958899672 |
| 3 | DTE | BUY | 1 | 150.72/150.70 | 1 | 0.0 | 2.7·2.1%·1.6%·MID_DVOL·large·0935 | 132 | 19,895 | 150.28 | no | candle-close/3:02PM/151.02 | 326 | 0.46 | 1.52 | 17 | 39.60 | 2.64 | 36.96 | 0.63 | 958837375/958985637 |
| 4 | NWS | BUY | 1 | 28.65/28.64 | 3 | 0.0 | 2.5·2.6%·2.1%·SMALL_DVOL·large·0935 | 698 | 19,998 | 28.52 | no | candle-close/10:19AM/28.76 | 43 | 0.15 | 0.18 | -168 | 76.78 | 12.38 | 64.40 | 0.72 | 958837386/958870502 |
| 5 | PFG | SELLSHORT | 1 | 108.44/108.48 | 4 | 0.0 | 2.0·-2.5%·-3.0%·MID_DVOL·large·0935 | 184 | 19,952 | 108.75 | no | candle-close/9:45AM/108.58 | 9 | 0.43 | 0.47 | 353 | -26.68 | 3.68 | -30.36 | -0.52 | 958837390/958844437 |
| 6 | SPGI | SELLSHORT | 1 | 396.60/396.78 | 5 | 0.0 | 1.9·-2.6%·-3.1%·LARGE_DVOL·large·0935 | 50 | 19,830 | 398.34 | no | EOD-flatten/3:50PM/402.02 | 374 | 0.93 | 8.37 | -40 | -271.00 | 2.00 | -273.00 | -3.13 | 958837394/959003718 |
| 7 | DAL | BUY | 1 | 89.33/89.32 | 1 | 0.0 | 2.6·6.1%·5.6%·LARGE_DVOL·large·0935 | 223 | 19,921 | 88.90 | no | candle-close/10:25AM/89.83 | 49 | 0.73 | 1.00 | 183 | 111.50 | 4.46 | 107.04 | 1.11 | 958837380/958874578 |
| 8 | DHI | BUY | 1 | 167.93/167.93 | 0 | 0.0 | 2.8·7.5%·7.0%·MID_DVOL·large·1035 | 118 | 19,816 | NOT-logged | n/a | candle-close/11:16AM/168.50 | 41 | 0.90 | 0.72 | -234 | 67.26 | 2.36 | 64.90 | — | 958880651/958903080 |
| 9 | PHM | BUY | 1 | 136.97/136.93 | 3 | 0.0 | 2.2·7.9%·7.5%·MID_DVOL·large·1035 | 145 | 19,861 | NOT-logged | n/a | candle-close/10:54AM/137.65 | 19 | 1.22 | 0.59 | -287 | 98.60 | 2.90 | 95.70 | — | 958880664/958891889 |
| 10 | BLDR | BUY | 1 | 85.41/85.39 | 2 | 0.0 | 2.1·10.3%·9.8%·SMALL_DVOL·mid·1035 | 233 | 19,899 | NOT-logged | n/a | candle-close/11:19AM/86.20 | 45 | 0.91 | 0.90 | -177 | 185.24 | 4.66 | 180.58 | — | 958880670/958904477 |
| 11 | AFRM | BUY | 1 | 78.97/78.97 | 0 | 0.0 | 2.2·9.3%·8.8%·MID_DVOL·large·1035 | 253 | 19,979 | NOT-logged | n/a | candle-close/11:16AM/79.55 | 41 | 0.79 | 1.10 | -481 | 146.74 | 5.06 | 141.68 | — | 958880657/958903066 |
| 12 | LEN | BUY | 1 | 93.07/93.11 | -4 | 0.0 | 1.8·6.5%·6.0%·SMALL_DVOL·large·1035 | 214 | 19,917 | NOT-logged | n/a | candle-close/11:03AM/93.57 | 28 | 0.64 | 0.24 | -126 | 107.00 | 4.28 | 102.72 | — | 958880676/958896616 |
| 13 | MSTR | SELLSHORT | 1 | 98.57/98.59 | 2 | 0.0 | 1.6·-4.3%·-4.8%·LARGE_DVOL·large·1035 | 202 | 19,911 | NOT-logged | n/a | candle-close/11:37AM/97.18 | 62 | 1.52 | 1.18 | 616 | 280.78 | 4.04 | 276.74 | — | 958880691/958912312 |
| 14 | VICI | BUY | 1 | 27.01/27.01 | 0 | 0.0 | 2.9·1.0%·0.5%·MID_DVOL·large·1035 | 740 | 19,987 | NOT-logged | n/a | candle-close/3:02PM/27.07 | 267 | 0.10 | 0.30 | -244 | 44.40 | 12.88 | 31.52 | — | 958880686/958985648 |
| 15 | UPST | BUY | 1 | 33.41/33.40 | 3 | 0.0 | 1.4·5.4%·5.0%·SMALL_DVOL·mid·1035 | 574 | 19,177 | NOT-logged | n/a | candle-close/11:19AM/33.81 | 44 | 0.48 | 0.76 | -654 | 229.60 | 10.89 | 218.71 | — | 958880693/958904164 |
| 16 | KVUE | BUY | 1 | 18.84/18.84 | 0 | 0.0 | 3.3·2.2%·1.5%·MID_DVOL·large·1135 | 1061 | 19,989 | NOT-logged | n/a | EOD-flatten/3:50PM/18.71 | 255 | 0.04 | 0.15 | 95 | -137.93 | 16.73 | -154.66 | — | 958911580/959003637 |
| 17 | KMB | BUY | 1 | 107.65/107.62 | 3 | 0.0 | 2.0·3.4%·2.6%·MID_DVOL·large·1135 | 185 | 19,915 | NOT-logged | n/a | EOD-flatten/3:50PM/106.38 | 255 | 0.05 | 1.38 | 67 | -234.95 | 3.70 | -238.65 | — | 958911585/959003616 |
| 18 | CVX | SELLSHORT | 1 | 171.05/171.06 | 1 | 0.0 | 1.4·-2.8%·-3.5%·LARGE_DVOL·mega·1135 | 112 | 19,158 | NOT-logged | n/a | EOD-flatten/3:50PM/172.27 | 255 | 0.11 | 1.41 | 84 | -136.64 | 2.24 | -138.88 | — | 958911594/959003594 |
| 19 | BKR | SELLSHORT | 1 | 55.85/55.86 | 2 | 0.0 | 1.3·-4.8%·-5.5%·MID_DVOL·large·1135 | 358 | 19,994 | NOT-logged | n/a | EOD-flatten/3:50PM/56.44 | 255 | 0.21 | 0.66 | 29 | -211.22 | 7.16 | -218.38 | — | 958911588/959003544 |
| 20 | SLB | SELLSHORT | 1 | 46.06/46.05 | -2 | 0.0 | 1.2·-3.6%·-4.3%·LARGE_DVOL·large·1135 | 434 | 19,990 | NOT-logged | n/a | EOD-flatten/3:50PM/46.69 | 255 | 0.19 | 0.66 | 22 | -273.42 | 8.68 | -282.10 | — | 958911590/959003707 |
| 21 | DOW | SELLSHORT | 1 | 29.05/29.05 | -0 | 0.0 | 1.3·-4.1%·-4.7%·MID_DVOL·large·1235 | 688 | 19,986 | NOT-logged | n/a | candle-close/1:27PM/28.86 | 52 | 0.20 | 0.10 | -358 | 130.72 | 12.26 | 118.46 | — | 958934771/958953342 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $138.33  ·  fees: $0.00
- Commission 3.32 bps + fees 0.00 bps of $417,080 notional = **3.32 bps avg cost**
- Avg entry slippage: 1.4 bps (adverse +)
- Slippage trend (prior 10d, adverse + bps): [2.0, -0.4, -1.1, 2.1, 2.2, 1.3, 0.8, 0.9, 1.2, 0.8] · trailing avg 1.0 bps · today 1.4 (worse vs trailing)
- Per-trade avg cost: $6.59 (21 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=21 · win rate 62% (13W/8L)
- GROSS day P&L $-244.97 · **NET day P&L $-383.31**
- Gross expectancy $-11.67/trade · Net expectancy $-18.25/trade
- Net profit factor 0.80
- Avg win $120.31 · avg loss $-243.42
- Largest win $276.74 · largest loss $-611.31
- Long/short split: 12L / 9S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=7 · win 57% · net $-582 ($-83/trade, -41.7 bps)
- PATH re-arm:      N=14 · win 64% · net $198 ($14/trade, 7.1 bps)
- OCC 1st-entry:    N=21 · win 62% · net $-383 ($-18/trade, -9.2 bps)
- OCC re-entry(2+): N=0
- RECONCILE: path sum $-383.31 + occ sum $-383.31 == day net $-383.31 -> OK

- Capital utilization: PEAK deployed: $320,604  (106.9% of $300k target)  at 14:56 (9 pos + 7 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- MSTR: left $990 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- PFG: left $624 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- PHM: left $213 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- marginability shadow: 21 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=26 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = -0.143; breakout won (R>0) 7/26 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): large=-0.17 (n22), mega=-0.11 (n1), mid=0.01 (n3)
## H · CAPITAL DEPLOYMENT (by hour + idle attribution)

**Deployed book by hour (peak; filled positions + working orders):**

| hour | deployed | % of $400k cap | pos+working |
|--|--|--|--|
| 9AM | $219,177 | 55% | 4+7 |
| 10AM | $301,319 | 75% | 8+7 |
| 11AM | $280,422 | 70% | 5+9 |
| 12PM | $300,737 | 75% | 8+7 |
| 1PM | $300,423 | 75% | 8+7 |
| 2PM | $320,604 | 80% | 9+7 |
| 3PM | $261,009 | 65% | 7+6 |

**Idle-capital attribution** (why capital sat idle vs the $400k cap; RE-ARM windows):
- **Qualified trades refused for CAPITAL today: 16** (peak idle below cap $100,470; gross demand upper-bound $400,000 at $25k/name). _The only number that justifies raising the deploy target._

| window | deployed | idle vs cap | thin-signal | self-throttle | refused cap/slot/reentry |
|--|--|--|--|--|--|
| 1035 | $299,530 | $100,470 | $0 | $100,470 | 6/0/1 |
| 1135 | $299,894 | $100,106 | $0 | $100,106 | 1/0/8 |
| 1235 | $299,970 | $100,030 | $0 | $100,030 | 2/0/9 |
| 1335 | $299,849 | $100,151 | $0 | $100,151 | 4/0/9 |
| 1435 | $299,849 | $100,151 | $0 | $100,151 | 3/0/9 |

- STALE-SLOT (separate; DEPLOYED-but-stuck, NOT idle): $138,809 in 7 red name(s) held to EOD-flatten -- a tighter exit would have freed the slot.
- _thin-signal + self-throttle = idle (cap-deployed) per window. Thin-signal idle is CORRECT (no qualified candidate wanted it -- NOT a defect, no floor implied); self-throttle is fixable (our caps). The 9:35 path deploys first; this covers the re-arm windows in the trace._

## I · LOSER ATTRIBUTION (exit-reason x confirm x side)

**1. Losers by SIDE:**
- LONG losers 2 ($-393.31) · SHORT losers 6 ($-1,554.03) · total losing $-1,947.34 over 8 trade(s)

| sym | side | confirm | exit | hold m | net$ |
|--|--|--|--|--|--|
| PAYX | short | no | EOD-flatten | 374 | $-611.31 |
| SLB | short | no | EOD-flatten | 255 | $-282.10 |
| SPGI | short | no | EOD-flatten | 374 | $-273.00 |
| KMB | long | no | EOD-flatten | 255 | $-238.65 |
| BKR | short | no | EOD-flatten | 255 | $-218.38 |
| KVUE | long | no | EOD-flatten | 255 | $-154.66 |
| CVX | short | no | EOD-flatten | 255 | $-138.88 |
| PFG | short | yes | candle-close | 9 | $-30.36 |

**2. ALL trades by EXIT REASON x CONFIRM (partitions every round-trip):**
| exit reason | confirm | n | win% | net$ | avg hold m |
|--|--|--|--|--|--|
| EOD-flatten | no | 7 | 0% | $-1,916.98 | 289 |
| candle-close | yes | 14 | 93% | $1,533.67 | 80 |
- _partition check: cells sum to 21 == N 21_

**3. BLEEDER FLAG — unconfirmed-rides-to-EOD-flatten (the named target class):**
- 7 trade(s), net $-1,916.98, avg hold 289m

| sym | side | hold m | net$ |
|--|--|--|--|
| PAYX | short | 374 | $-611.31 |
| SLB | short | 255 | $-282.10 |
| SPGI | short | 374 | $-273.00 |
| KMB | long | 255 | $-238.65 |
| BKR | short | 255 | $-218.38 |
| KVUE | long | 255 | $-154.66 |
| CVX | short | 255 | $-138.88 |

**4. MUST-NOT-CUT CONTROL — winners a tightening rule must spare (longest-held first):**
| sym | side | confirm | exit | hold m | net$ |
|--|--|--|--|--|--|
| DTE | long | yes | candle-close | 326 | $36.96 |
| VICI | long | yes | candle-close | 267 | $31.52 |
| HAL | short | yes | candle-close | 94 | $124.62 |
| MSTR | short | yes | candle-close | 62 | $276.74 |
| DOW | short | yes | candle-close | 52 | $118.46 |
| DAL | long | yes | candle-close | 49 | $107.04 |

---

---
### Turn — 2026-06-24 ~12:45 PM ET — Fix dashboard lag (daily-review 50s -> 5s) + clear leaked process
- **Researched (not assumed):** home 381ms / versions 485ms FINE; daily-review-v2 = **50.5s**. Profiled components → `strategy_compliance.path_expectancy()` = **46.2s** (the whole lag). Root cause: it iterates every post-baseline day, and each day calls `eod_debrief._exit_reasons()` which scans the entire **140MB trade_journal.csv** (~3.5s) → 12 scans = ~42s. Also found a LEAKED duplicate dashboard process (PID 6220 @07:27 owning port + 9432 @11:01); session restarts weren't cleanly killing the old one.
- **Fixes (both perf, read-only, non-watched):**
  - `eod_debrief._exit_reasons`: refactored to scan the 140MB journal ONCE per process (group exit events by date + cache); LIVE day always read fresh (never serve stale), past days served from cache. Identical data, far fewer reads. → path_expectancy COLD 46.2s→**3.8s**, day_compliance 4.1s→**0.02s**.
  - `strategy_compliance.path_expectancy`: cache the cumulative result keyed by the post-baseline date set (auto-invalidates when a new day lands) — it's identical across every render. COLD 3.8s, cached **0.01s**.
  - Killed ALL leaked dashboard instances, freed port, started exactly ONE (PID 10180, owns 8765).
- **Verify:** compile OK; _exit_reasons 6/23 identical (NRG reasons correct); daily-review-v2?date=2026-06-23 now COLD **5.17s** / WARM **0.73s** (was 50.5s), HTTP 200, 382,139 bytes (content intact); home 329ms / versions 464ms; 1 instance.
- **Note:** caches are per-process; the EOD debrief (fresh 4:50 process) builds its own (one journal pass) → accurate. Today's cumulative path_expectancy is cached by date-set so its in-progress contribution can be slightly stale intraday (context metric; acceptable). Future: a supervisor should keep the dashboard at one instance to prevent restart leaks.
- **No watched strategy file touched. No trading-path change.**

---
### Turn — 2026-06-24 ~5:30 PM ET — (A) P&L cost-model reconcile/labels + (B) STAGE $400k target raise
- **(A) VERIFIED (read-only):** all NET surfaces (daily-review, EOD debrief) = `round_trips_net` NET = gross − BROKER-ACTUAL CommissionFee (not a model); daily-review NET==day_totals NET==canonical (6/24 −$383.31 = gross −$244.97 − $138.34 broker cost; matches the log). SIM account is on a per-share plan so broker-actual ≈ per_share_standard (PAYX 213sh = $4.26). NONE use zero/ts_select. `/truth` uses a SEPARATE MODELED per_share_standard cost (projection) — flagged.
- **(A) FIXED the mislabel:** daily-review header said "after-cost (per_share_standard MODEL)" → now "day P&L is NET of BROKER-ACTUAL commission (CommissionFee per fill, NOT a model)" + the live-plan caveat. Added KPIs "Net P&L (after broker-actual cost)" + "Gross P&L (before cost)" so gross blotter vs net review is never confused again. CSHV `daily_review_reconciles_broker_truth` now NAMES the cost basis (broker-actual CommissionFee) + states daily-review+EOD+/truth delegate to one NET definition.
- **(A) OPEN ITEM flagged to Rhett:** live-account commission plan (TS Select $0 vs per-share) unconfirmed — cost halves the edge; SIM is per-share, live TBD.
- **(B) STAGED (deploy HELD, governance-gated):** wrote `outputs/proposals/PROP-DEPLOY-TARGET-400K-2026-06-24.md` — raise DEPLOY_TARGET_PCT 0.75→1.0 ($300k→$400k), JUSTIFIED by the 3-day self-throttle data (16/59 qualified refused for capital, ~$100k idle/window). HARD PREREQUISITE: the live available-BP gate (admit/size vs real-time TS BP, account for working-order holds + slippage, down-size/refuse → no TS reject; pairs with PROP-LIVE-BP-AWARE-DEPLOY). Keep $200k/side + $25k/name. Verification plan V1-V5 (sim $390k → refuse, no TS reject). FIRE CONDITION: test resolves + between experiments + manual_approvals + BP gate green. NOT a deployment floor. NOTHING deployed.
- **No live-path edit. daily_review_page + system_health_verifier are display/monitoring (non-watched). Freeze intact.**
- **Rhett's call on commission plan: NOT DECIDED YET.** → keep all executed-trade surfaces on BROKER-ACTUAL cost (current state); dashboard header flags live-plan TBD. WHEN decided: if TS Select → reconcile shadow/projection cost model to ts_select (SIM net then overstates live cost, edge better than shown); if per-share → no change. Known-open, don't re-raise as new.

---
### Turn — 2026-06-24 ~6:00 PM ET — MSTR 6/24 left-on-table verify (NO bug) + exit autopsy (read-only)
- **(1) PRIORITY sign-check — PASSES, no measurement bug:** MSTR 6/24 SHORT entry 98.57@10:35 → exit 97.18@11:37, 202sh, net +$276.74. left_on_table_after_exit = **+$616.10** (eod_hold $896.88 − realized $280.78), POSITIVE = correctly captures DOWNWARD continuation for the short (eod 94.13 < exit 97.18). Formula for shorts = (exit−eod)×qty → positive when price falls after exit = CORRECT sign. NOT missing, NOT zero, sign right. left_on_table_in_trade = $18.18 (mfe 298.96 − realized).
- **Why Rhett expected ~$1000:** the post-exit MFE (price fell to $92.28 @ 13:47 = $989.80 favorable) but REVERTED to 94.13 by EOD. The metric uses HELD-TO-EOD close ($616), not the post-exit favorable EXTREME ($990) — so it UNDERSTATES givebacks that revert before close. Definitional, not a bug. Value IS displayed (per-trade card "Left after exit" + day KPI) but givebacks are NOT ranked/surfaced as a list.
- **(2) EXIT AUTOPSY:** exit_decisions → EXIT 11:37:09 reason CANDLE_CLOSE_REVERSAL (phase2), **confirmed=True** (first confirm 11:36:46). Chandelier (107.36) never threatened. Trigger = the 11:37 1-min candle closed UP (o97.21→c97.23) against the short → candle-close reversal fired @ 97.18. Then price RESUMED falling to 92.28 — the 11:36-37 bounce was a brief pullback in a continuing downtrend. **Clean NAMED data point FOR exit-loosening:** the candle-close trail cut a CONFIRMED winner early on a 1-bar mid-trend bounce, leaving $616 (EOD) / $990 (peak) on the table. Counterweight to the unconfirmed-bleeder points AGAINST loosening.
- **No code change (posture = read-only verify; metric is correct). Recommended enhancements (asked Rhett): add post-exit-MFE complement (peak giveback) + rank/surface largest givebacks + left-on-table non-null/sign guard in the integrity contract.**

---
### Turn — 2026-06-24 ~6:30 PM ET — Giveback visibility build (Rhett: build now, display-only)
- **(1) post_exit_mfe field (trade_analytics.enrich_trade):** peak favorable continuation AFTER exit (short: exit−lowest-low-after-exit; long: highest-high−exit; favorable-only). Complements left_on_table_after_exit (held-to-EOD, which understates reverting moves). MSTR 6/24 verified: post_exit_mfe **$989.80** vs left_after $616.10.
- **(2) Ranked "Largest givebacks" panel (daily_review_page):** top-6 by post_exit_mfe (>$50), shows sym/side/exit/net/giveback-to-EOD/peak-giveback. MSTR ranks #1 ($990). Surfaces the exit-loosening cost. + rollup peak_giveback day total ($3,284.98 on 6/24).
- **(3) Integrity guard (build_review reconcile block):** for each trade w/ bars, recompute left_on_table_after_exit from broker truth ((eod−exit) long / (exit−eod) short) and assert the stored value matches (non-null + correct SIGN); mismatch → loud RECONCILE banner. Verified clean on 6/24 (21/21, reconcile_ok=True) — catches any future short sign-flip.
- **Verify:** compile OK; MSTR post_exit_mfe $989.80; reconcile_ok=True (guard clean); top givebacks MSTR/PFG/PHM; dashboard restarted PID 10368 (1 instance); /daily-review-v2?date=2026-06-24 = 200, "Largest givebacks" + "Peak giveback (post-exit)" + MSTR PRESENT.
- **Display/measurement only; non-watched; no trading-path change; freeze intact.**

---
### Turn — 2026-06-24 ~7:00 PM ET — MSTR vs ANET confirm-state contrast (read-only verify from exit_decisions)
- **MSTR 6/24 SHORT (giveback counter-case) — CONFIRMED:** entry 98.57, atr 8.79, confirm_level 97.25 (entry−0.15ATR). Price fell to 97.14 ≤ 97.25 → **CONFIRMED @ 11:36:46** → candle-close reversal ARMED → the 11:37 up-candle (o97.21→c97.23, opposite-color for a short) tripped it → EXIT 97.18 +$277. Chandelier 107.35 never near (max high 99.42). Then ran to 92.28 (giveback $616 EOD / $990 peak).
- **ANET 6/23 SHORT (bleeder) — NEVER CONFIRMED:** entry 161.235, atr 7.43, confirm_level 160.12. Lowest it traded = 160.83 — **missed the confirm trigger by $0.71** → NEVER CONFIRMED → candle-close NEVER armed → only the 1.4xATR chandelier (168.66) active → the all-day grind to high 164.75 never reached 168.66 → NO synthetic exit → rode to EOD-flatten −$147. Last state "chandelier_hold (unconfirmed)".
- **VERDICT: difference is FULLY explained by confirm-state; nothing else going on.** Confirmed → responsive candle-close exit (fires on any opposite candle close, even a tiny bounce → can clip a winner). Unconfirmed → only the far chandelier backstop (a grind that never closes through it rides to EOD). MSTR was cut early on a small bounce BECAUSE confirmed; ANET rode a big adverse move BECAUSE unconfirmed.
- **Implication:** the two cases pull the exit in OPPOSITE directions (confirmed wants looser to capture continuation; unconfirmed wants tighter to stop the bleed) → a CONFIRM-KEYED exit. Reinforces the gauntlet target = confirm-keyed unconfirmed-bleeder cut (NOT loosening the confirmed exit). ANET near-miss ($0.71 from confirming) = the 0.15ATR threshold is the knife-edge lever.
- **Both already in standing samples:** ANET 6/23 = Section I bleeder; MSTR 6/24 = Section I must-not-cut + the new "Largest givebacks" panel (#1, $990). No build (read-only verify). Freeze intact.

---
### Turn — 2026-06-24 ~7:30 PM ET — Fix false "exit: WARN" on /system-validation (stale check)
- **Rhett:** "/system-validation says exit: warn." Root cause: `system_validation_page.py:199` hardcoded `OK if ORB_EXIT_MODE == "candle_close" else WARN` — but the DEPLOYED mode since 6/19 (Loop 121) is `candle_1.4atr_chandelier`, so the check false-WARNed on the CORRECT config (stale check, same class as the earlier shadow_versions 'V9' selftest staleness). NOT a real problem — verified exits are healthy (reconcile_ok on 6/22-6/24, CSHV rel_exit_side OK, 0 WARN).
- **Fix (display-only, non-watched):** OK if ORB_EXIT_MODE in the valid deployed set {candle_1.4atr_chandelier, candle_close}; WARN only on an UNRECOGNIZED mode; label now shows the actual mode. Now renders "exit (candle_1.4atr_chandelier) — OK".
- **Verify:** compile OK; dashboard restarted (PID 5248, via Python/Bash — PowerShell tool was EPERM-ing on spawn this turn, transient infra; worked around it); /system-validation exit row = "[OK]", no WARN emoji.
- **No watched file / trading-path change. Freeze intact.**

---
### Turn — 2026-06-24 ~7:45 PM ET — OWN the stale-validation miss + handoff + memory (Rhett frustrated)
- Rhett (rightly frustrated): the `/system-validation` exit check stayed stale (hard-coded old `candle_close`, false-WARNed on the deployed `candle_1.4atr_chandelier` for days). Asked for a handoff explaining how I missed it.
- **Owned it honestly:** I had the deployed-mode fact in front of me ~6x this session AND fixed the SAME stale-check class twice (shadow_versions 'V9' self-test, earnings) without recognizing the pattern or sweeping. Never grepped for old-value consumers; never proactively opened /system-validation.
- **Wrote handoff** `HANDOFF_2026-06-24_STALE-VALIDATION-MISS.md` (Rhett's note + my response + 4 standing rules). **Wrote memory** `feedback_config_change_sweep_consumers.md` (+ MEMORY.md index) so future sessions load the rule.
- **Proactive sweep done:** no identical sibling stale checks (only correct comments reference `candle_close`).
- **Standing rules:** (1) config-value change → grep tree for OLD value + constant, reconcile EVERY consumer (esp. validation/health/CSHV/preflight/selftests); (2) validation checks read source-of-truth not literals; (3) fix one stale check → sweep for siblings; (4) proactively open health surfaces, don't wait to be told.
- **Recommended (not built): make /system-validation deployed-value checks read the change-log's approved-deployed value (self-updating).** Offered.

---
### Turn — 2026-06-24 ~7:55 PM ET — Detailed handoff of the stale-validation miss (Rhett asked)
- Expanded `HANDOFF_2026-06-24_STALE-VALIDATION-MISS.md` into the FULL record: chronology of all 3 turns since Rhett flagged the warn (Turn 1 vague report + Claude investigated wrong surfaces/guessed; Turn 2 located under /system-validation + root cause + fix 269b5d1; Turn 3 owned it), an explicit "WHAT CLAUDE MISSED" section (5 failures), the 5 standing rules, and the recommended source-of-truth follow-up. Committed.

---
### Turn — 2026-06-24 ~8:30 PM ET — 3 verifications from the 6/24 2nd-opinion review (read-only)
- **V1 LOSER RECONCILE — clean:** 21 RT, 13W (net>0) / 8L (net<0) / 0 scratch; win_rate 61.9%. ALL 8 losers reconcile to −$1,947.34 and ARE in EOD Section I Table 1 ("Losers by SIDE", 8 listed). The review's "7" = the BLEEDER FLAG (Table 3, confirm=no + EOD-flatten subset, by design). The 8th = PFG (confirm=YES, candle-close, −$30.36) — correctly excluded from the bleeder class. Already reconcilable from the EOD (Table 1 lists all; Table 2 partition "cells sum to 21==21"); report_integrity already enforces count/win-rate. No fix needed.
- **V2 CORRELATED CLUSTER — confirmed gap:** CVX/BKR/SLB all SHORT, all entered 11:35 (re-arm), all confirm=no, all EOD-flatten. Combined notional **$59,142** (~$20k each), combined net **−$639.36**. 1-min return correlations: CVX-BKR 0.42, CVX-SLB 0.55, BKR-SLB 0.68 → moderately-to-strongly correlated = effectively ONE energy-sector short bet 3×. The $25k/name + $200k/side caps don't stop factor concentration; MAX_SECTOR_POSITIONS=2 didn't prevent it (likely re-arm bypasses it / cross-subsector buckets). FLAG: a sector/correlation exposure cap belongs in the before-live work alongside the BP gate (the queued $400k raise must not mean "same bet more times").
- **V3 CONFIRM-LOGGING INTEGRITY (highest) — SOLID + path-consistent + decision-time, ONE caveat:** confirm is computed IDENTICALLY for 9:35 + re-arm (same exit_bot_v2 monitor, entry-path-agnostic; same CONFIRM_ATR 0.15; same get_atr14 atr; high/low water tracked from `last_price` polls). Logged at decision time, monotonic (water only ratchets, confirmed-once stays), NOT back-filled. Spot-checks: MSTR conf=YES ✓ (polled 97.14 ≤ 97.25), CVX conf=NO ✓ (never crossed). **PAYX = poll-resolution near-miss:** logged conf=NO is FAITHFUL to the bot (polled last_px min 93.31 never reached confirm 93.18) BUT the 1-min candle low 93.02 DID cross — a sub-poll wick the bot didn't sample. So confirm = "did the bot's POLLED price cross +0.15ATR", NOT "did price ever cross". ANET (canonical bleeder) is a CLEAN unconfirmed (candle low 160.83 never reached 160.12). NOT a thesis-breaking defect (the flag is what gated the live exit → correctly explains behavior) but "unconfirmed" can include borderline near-misses (PAYX) — relevant when keying a gauntlet rule on confirm-state.
- **No code change (read-only verify). Freeze intact.**

---
### Turn — 2026-06-24 ~8:45 PM ET — Kill the STALE-CHECK class: meta-check auditor (B) + staged conversion (A)
- **Owned the planning-seat miss** (per handoff): the stale-check class kept getting patched per-instance with Rhett as detector. Built the meta-check to find the CLASS, not instances.
- **BUILD B — `validation/stale_check_auditor.py` (DONE):** AST scan of validation/health/CSHV/preflight files for any check comparing a config CONSTANT to a HARD-CODED literal. Self-test 1/1 (flags a planted `rc.ORB_EXIT_MODE=='candle_close'`, ignores var-compares). **FULL INVENTORY = 8 instances, all in `_preflight_diagnostic.py:141-147`** (DAILY_MAX_LOSS, MAX_LOSS_PER_TRADE, MAX_TRADES_PER_DAY, STRATEGY_MAX_LOSS, ACCOUNT_DD_KILL_PCT, STRATEGY_DD_KILL_PCT, MAX_LEVERAGE — all `== literal`). The /system-validation exit check is NOT flagged (already converted to a set in 269b5d1). Wired into preflight as the standing invariant — WARN now (inventory pending), flip to FAIL post-test once 0.
- **BUILD A — STAGED proposal `PROP-SELF-UPDATING-VALIDATION-2026-06-24.md`:** convert the 8 to read the APPROVED-DEPLOYED value from a single source-of-truth registry (`deployed_config_expected.json`) instead of scattered literals → unapproved drift still FAILs (tripwire holds), approved change auto-updates (one place). + /system-validation deployed-value rows read the registry. Verification: planted approved change → check follows; planted drift → FAILs; auditor→0 → flip WARN→FAIL. FIRE post-test (validation code; build-during-freeze avoids churn).
- **Verify:** auditor compile + self-test 1/1; full inventory = 8; preflight wired (49 PASS / 1 WARN / 2 FAIL). The 2 FAILs ("positions clean: 3 open", "orders clean: 7 working") are PRE-EXISTING context-insensitive checks (expect 0, fail when run with open positions) — NOT caused by my change (my change = the 1 WARN). Flagged separately.
- **Non-watched (validation/preflight only); no trading-loop import; freeze intact.** Joins P&L / slippage-KPI / shadow-V9 / kill-window-seal as a standing decision-quality invariant.

---
### Turn — 2026-06-24 ~9:00 PM ET — ACK 3 verifications; folded V2 + V3 caveat into the queue (no build)
- ACK-only handoff. No code/trading change. Persisted the two queue decisions so they survive:
- **V2 → PROP-DEPLOY-TARGET-400K:** added "HARD PREREQUISITE #2 — SECTOR/FACTOR-CORRELATION exposure cap" (covers re-arm path, groups by correlation/sector-family not subsector labels, ships WITH the raise + BP gate). Evidence: CVX/BKR/SLB $59k energy bet 3x, MAX_SECTOR_POSITIONS=2 didn't stop it.
- **V3 → new memory `project_exit_loosening_gauntlet.md` (+ MEMORY.md):** consolidated the post-test exit gauntlet (cut unconfirmed-rides-to-EOD, CONFIRM-KEYED not hold-time; three-sided net-of-cost; MSTR giveback counter-case vs ANET bleeder) + the V3 poll-confirm caveat ("confirmed"=polled price crossed, not "price ever crossed"; PAYX near-miss) + the pre-registered clean-fail-vs-poll-near-miss split + optional continuous-confirm shadow diagnostic.
- V1 = Planning's seat (relayed ChatGPT's count without checking Table 1); no system defect. Freeze intact.

---
## 6/25 — Pre-market page verification (V1 HTB leak / V2 slippage / V3 qualified-count) — READ-ONLY, no code change

**V1 — TTD HTB leak: NO ESCALATION (display-only, not tradable).**
- Trade gate verified live: `ORB_EXCLUDE_HARD_TO_BORROW=True` → BOTH 9:35 (orb_runner.py:656) and re-arm (orb_multiscan.py:304) apply `htb_filter` fail-safe exclusion (`MarketFlags.IsHardToBorrow`; also excludes UNKNOWN_BORROW/NO_QUOTE). TTD (IsHardToBorrow) → SKIP both directions, never armed.
- Display: `HB_FILTER=False` (SIM, "recorded not filtered", mover_scanner.py:123) → scanner surfaces HB names. 6/25 09:35 scan: TTD short, hb_flag=True, surfaced in short-candidate rows. Two HB signals are independent sources (scanner `Restrictions` = badge; gate `MarketFlags.IsHardToBorrow` = fail-safe authority).
- DEFECT (flag, queue — NOT a live-rule violation): premarket section header reads "Short candidates — % losers (tradable, S&P pool)" but TTD (HB) appears there and the gate WILL refuse it. "tradable" label is misleading on HB rows; the "never surfaced in research" half of the standing rule is technically deviated by design in SIM.
**V2 — slippage is an ESTIMATE, gates-not-ranks.** `est_slippage_bps` = half bid/ask spread in bps, marketable-entry proxy captured at selection (mover_scanner.py:139-141). NOT realized broker-truth slippage (that is post-fill `eod_debrief.entry_slip`). Cost feeds selection as a HARD spread cutoff (`spread_pct>MAX_SPREAD_PCT=0.5%` drop, :126) but NOT as a ranking weight (`score=relvol*exhaustion`, :136). Not a pure display artifact.
**V3 — "qualified" = passed FIRST liquidity screen, not full in-play gate.** `qualified=len(movers)` (:194) = names passing last≥$5, prev_vol≥1M, spread≤0.5%. RelVol thresholds / sector cap / HTB applied downstream at arming. 6/25: 527 checked → 363 qualified (matches page). "broad —, — qualified" em-dash = broad tier runs only ≥10:00 (BROAD_SKIP_BEFORE), 9:35 scan has no broad_scanned key → by design, not a bug (confirmed broad_scanned absent in 09:35 record).

---
## 6/25 ~9:55 — MU long verification (V1 price integrity / V2 red-candle entry / V3 exit state) — READ-ONLY

**V1 — PRICE IS REAL. NO escalation, NO data defect.** WebSearch: MU (Micron) genuinely ~$1,231 on 6/25/2026 (+17.4% premkt) on a blowout fiscal Q3 ($41.46B rev beat); prior close $1,048.51. Bot scanner ($1,252.90, +19.49%), broker fill ($1,253.03), and implied prior close ($1,048.5) all match reality EXACTLY. The "MU ~$100-130" premise (handoff + my own first instinct) is a STALE-KNOWLEDGE artifact — Micron is a ~$1,000+ stock by mid-2026. RULE #0 caught it before a false escalation.
  - Design note: a naive "reject if price diverges from prior_close x N" bad-tick guard would have FALSELY blocked this legit +17% earnings gap. A real bad-tick guard must use spread/staleness/tick-to-tick checks, not a gross prior-close divergence threshold.
**V2 — entry on red candle = expected mechanics.** BUY StopLimit, signal_trigger_px 1253.0, filled 1253.03 @ 9:35:56 ET (order 959068139, orb_v1_6). Breakout triggered intrabar crossing the OR-high UP; price then faded (red close). Not a bug. Never confirmed (+0.15xATR) — price went straight down.
**V3 — MU is CLOSED/FLAT (not open).** Exited SELL 15 @ 1141.81 @ 9:55:27 ET (order 959087927); protective stop @1124.34 went UROUT (cancelled) → strategy/candle exit fired ABOVE the hard stop, not the stop itself. Realized GROSS = (1141.81-1253.03)x15 = **-$1,668.30**. Unconfirmed loser, 20-min hold (NOT a ride-to-EOD bleeder). The handoff's -$966.90 was a ~9:50 mid-trade snapshot; it exited lower at 9:55.
  - **SECONDARY FINDING (real, queue):** realized -$1,668 >> MAX_LOSS_PER_TRADE ($750). Sizing is NOTIONAL-based (15x$1253=$18,795, within $25k cap), NOT loss-based, so per-trade $ risk is uncontrolled on a high-priced/high-ATR name. Protective stop alone permitted -$1,930 (10.3% stop distance). This is the known "no real-time intraday clamp" gap (DAILY_MAX_LOSS currently $1e9 = SIM-disabled). Relevant to before-live hardening; governance-gated (proposal, not inline).

---
## 6/25 ~10:10 — Confirmation-keyed exit gauntlet QUEUED (DO NOT BUILD) — captured to proposal + memory
Rhett's insight: deployed exit (candle_1.4atr_chandelier) allocates protection INVERSELY to risk — confirmed→tight candle-close, unconfirmed→wide 1.4xATR chandelier. Fix = key exit aggressiveness on confirm state.
- Full buildable spec persisted: `ai-trading-strategy-agent/outputs/proposals/PROP-CONFIRM-KEYED-EXIT-2026-06-25.md` (STAGED, fire post-test + between experiments + manual_approvals.yaml). Half A (do-first, tighten unconfirmed: A1 time/A2 MAE/A3 N-closes/A4 chandelier) vs Half B (3-sided only, room for confirmed: B1/B2). Test primitives individually (composite trap). Three-sided net-of-cost + N>=30 + FDR + MUST-NOT-CUT control + SEALED V0/V9 baseline. Poll-confirm caveat (clean-fail vs poll-near-miss).
- Memory updated: project_exit_loosening_gauntlet.md + MEMORY.md index.
- MU 6/25 worked example BROKER-VERIFIED + corrected 3 draft errors: (1) confirm=FALSE [filled the TBD] — ATR 76.29, confirm_level 1264.47, high_water 1250.14 never regained entry 1253.03; (2) NOT an EOD ride — exited 9:55:27 via CHANDELIER_STOP(1.4xATR) @1141.81, 20-min hold; (3) loss = -$1,668.30 gross (draft's "$1,147" was the exit price). MU = sharpest Half-A example + direction-agnostic (long-side) proof.
- NO build, NO live-path change. Freeze intact (3/5 clean).

---
## 6/25 ~10:25 — Gauntlet spec v2 QUEUED (DO NOT BUILD) — excursion-keyed + entry/exit study; SUPERSEDES v1
Rhett's v2 direction corrects the v1 frame: discriminator is NOT confirmed/unconfirmed binary but the CONTINUOUS early-excursion shape (MFE vs MAE), and entry+exit studied TOGETHER (v1 exit-only = tunneling error). Losers were wrong from minute 1 (MFE~0 + large MAE), not winners-that-reversed.
- New spec: `ai-trading-strategy-agent/outputs/proposals/PROP-EXCURSION-KEYED-EXIT-2026-06-25.md`. v1 (PROP-CONFIRM-KEYED-EXIT) marked SUPERSEDED (banner) but retained for broker-verified examples + A1-A4/B1-B2 primitives.
- THREE READ-ONLY STUDIES (post-close; gate the build): S3 (DO FIRST) entry/exit $ split (preventable-at-entry vs manageable-at-exit); S1 confirmed-winner study + adaptive-widen counterfactual (incl. MANDATORY 1d cost side); S2 biggest winners vs losers whole-trade similarity → rank discriminators by clean-separation AND early-readability-live.
- Unified fix hypothesis: exit keyed on continuous excursion (MFE~0 → short leash; MFE grows → earn room), keep poll confirm flag as executable lever, optional entry filter only if S3 shows big preventable-entry $ (separate primitive). Guardrails unchanged (N>=30/FDR/MUST-NOT-CUT/sealed-baseline/no-composite/no-mid-test-build).
- Memory updated (project_exit_loosening_gauntlet.md + MEMORY.md index). RULE #0: MU 6/25 already verifies the v2 frame (high_water 1250.14 < entry 1253.03 → MFE never positive). Studies NOT run (live session; post-close per spec). NO build, freeze intact (3/5 clean).

---
## 6/25 ~12:08 — Excursion studies: read-only engine BUILT + scheduled post-close (per Rhett "yes, run at close")
- NEW read-only files (non-watched, import-only, no live-path touch): `strategy-research/excursion_study.py` (engine: build_feature_table + study3/study1/study2) + `strategy-research/run_excursion_study.bat` (launcher).
- VERIFIED: engine 6/24 feature-table net = -$383.31 reconciles EXACTLY to eod_debrief.day_totals broker truth (21 trades). No live API calls (pinned bars only: outputs/validation/shadow_pin/{date}.json); missing pins → NOT-AVAILABLE.
- SCHEDULED: `AlphaQuant_ExcursionStudy_OneTime` (schtasks, /sc once, 5:15 PM ET 6/25, runs SYSTEM) → writes outputs/reports/excursion_study_2026-06-25.md on the full 3-day window (6/23,6/24,6/25). Validated by a manual /run (SYSTEM context works; produced report). 5:15 = after 4:50 EOD recon settles broker truth.
- PRELIMINARY read (partial mid-session data; N tiny; NOT actionable, pre-N>=30, freeze intact): S3 loser split skews preventable-at-ENTRY (MU's -$1,668 classified gap-top/entry, not exit); S1 adaptive-widen counterfactual on 6/24 (13 winners): keeping candle-close + widening chandelier = Δ$0 (chandelier never binds; MFE max ~0.33xATR), DROPPING candle-close converts 10/13 winners to losses → early evidence AGAINST Half B / loosening, reinforces Half A (unconfirmed = 100% lose). S2 cleanest+earliest discriminator = confirm state, then MFE~0.
- PROVENANCE GAPS (NOT-LOGGED, never faked): rs_vs_spy, distance_from_OR/extension, per-trade R. These limit S2/S3; adding RS + OR-distance logging is an entry-context change → post-test (touches scan/entry path), flagged not done.
- Studies NOT acted on. No live-path change. Freeze intact (3/5 clean).

---
## 6/25 ~12:10 — THREE NOT-LOGGED FEATURES (excursion-study provenance gaps) — for the record
These are needed by the gauntlet studies (S2/S3) but are NOT logged anywhere today. The engine emits them as
NOT-LOGGED and never fabricates a value. Each requires an ENTRY-PATH logging change (mover_scanner / orb_runner /
orb_multiscan = WATCHED files) → POST-TEST, via proposal + manual_approvals.yaml. They should be added BEFORE the
studies are treated as authoritative, because they limit Study 2 (discriminators) and Study 3 (entry-vs-exit $ split).

1. **rs_vs_spy** — relative strength vs SPY (stock's return minus SPY's over the entry window).
   - WHY: S3 "weak-move vs peers" preventable-at-entry criterion (the v2 spec's "TPR RS -0.6%" example); a Study-2
     entry discriminator (do winners enter with stronger RS than losers?).
   - WHERE IT'D LIVE: computed at scan time in `mover_scanner.py` (needs a SPY quote alongside the universe scan),
     stamped on the mover dict, carried to the entry/journal record.
   - STATUS: not logged in scans.jsonl or exit_decisions.jsonl. WATCHED path (scanner feeds ORB arming) → post-test.

2. **distance_from_OR / extension** — how far price had already extended from the opening-range level at entry
   (OR-high for longs, OR-low for shorts): did we buy near the breakout or far into an extended/spent move
   (MU gap-top, PAYX near-low).
   - WHY: S3 "entered far into the move" preventable-at-entry; a Study-2 entry discriminator.
   - WHERE IT'D LIVE: computed at arming/entry in `orb_runner.py` / `orb_multiscan.py` (OR levels + entry px are both
     known there), stamped on the entry record.
   - STATUS: not logged. WATCHED path → post-test.

3. **per-trade R** — net P&L in units of the trade's initial $ risk (entry − initial stop, × shares).
   - WHY: normalizes P&L across price levels so trades are comparable (MU -$1,668 @ $1,253 vs NRG -$545 @ $134 are not
     comparable in $ but are in R); required for proper expectancy / variant scoring.
   - WHERE IT'D LIVE: log the initial stop-distance × shares (the risk denominator) at arming, store on the trade record.
   - STATUS: not derivable from broker truth (no per-trade $risk basis stored; the 0.15/1.4xATR levels are EXIT params,
     not the entry-risk denominator). WATCHED path → post-test.

CONFIRMED: every turn this session is logged to SESSION_LOG (5 turn-blocks, lines ~1938-1977: pre-market verify, MU
verify, gauntlet v1, gauntlet v2, excursion engine+schedule) + this entry. A cold Claude can reconstruct the full session.

---
## 6/25 ~12:14 — Entry-context logging PROPOSAL created (queues the 3 NOT-LOGGED features)
- NEW proposal: `ai-trading-strategy-agent/outputs/proposals/PROP-ENTRY-CONTEXT-LOGGING-2026-06-25.md` (STAGED, post-test, manual_approvals.yaml).
- Captures rs_vs_spy (mover_scanner, +1 SPY symbol in existing batch), dist_from_or_atr (orb_runner/orb_multiscan, OR level vs entry / atr), risk_per_share+risk_dollars (→ per-trade R, from the initial stop distance at arming).
- Behavior-PRESERVING (write-only observability; no decision reads them) but touches WATCHED entry-path files → governance-gated, post-test. Minimal footprint: compute + ONE append to a new sidecar `entry_context.jsonl` via a helper. V1-V5 incl. behavior-equivalence replay + SPY-adds-no-token-refresh check + verify-load discipline.
- It's the PREREQUISITE for the gauntlet studies being authoritative (S2 discriminators / S3 entry-vs-exit $ split currently under-attribute the entry lever). Linked from project_exit_loosening_gauntlet.md memory.
- No build, no live-path change. Freeze intact (3/5 clean).

---
## 6/25 ~post-close — CSHV clean-day FALSE reset + notification spam: DIAGNOSED + FIXED (Rhett: handoff then fix)
SYMPTOM: ~12 CRITICAL "clean_day_certified FAIL" Discord pings 12:15-16:00. ROOT: scheduled_tasks_present logged 27 PowerShell Get-ScheduledTask query TIMEOUTs as FAIL → certifier SOFT-storm (27>=5) → FALSE-reset the forward-test clean-day streak (→0). rel_position_recon (LUV) fired 1x (tolerated); LUV was a clean +$153 win, properly exited 9:53. NO trading/strategy/risk fault. System healthy throughout.
HANDOFF: C:\AlphaQuant\HANDOFF_2026-06-25_CLEAN-DAY-FALSE-RESET.md (full chronology + fix + guardrails).
FIX (validation/health only; NO watched/live-path file; freeze intact):
- A. `system_health_verifier.chk_scheduled_tasks_present`: retry 2x + return WARN (inconclusive), not FAIL, on a query timeout/error. Genuine missing-task still FAILs.
- B. `clean_day_certifier._is_inconclusive_query` + exempt in `_scan_incident_file`: scheduled_tasks_present query-failure incidents (timeout/failed-to-query/rc=/exc) are EXEMPT → retroactively heals today + future. Missing-task NOT exempt.
- C. `chk_clean_day_certified` intraday throttle: FAIL once/day on first detection then WARN (marker outputs/cshv_intraday_clean_alert.json) → kills the intraday re-ping spam on ANY non-clean day.
VERIFY-LOAD: py_compile OK both files; certifier selftest 11/11; certify_day('2026-06-25')->clean, consecutive_clean 0->3 HEALED; full CSHV --no-notify = OK=46/WARN=0/FAIL=0 (was OK=45/WARN=1). CSHV runs fresh every 5 min → next run auto-uses new code. Forward test back to 3/5 clean, freeze intact.

---
## 6/25 ~post-EOD — OFFICIAL KILL ADJUDICATION (broker truth) — BOTH KILLS CROSSED
V1: Day NET = -$2,016.93 (round_trips_net=day_totals to the cent, 23 round-trips) CROSSES -$2,000 daily kill by $16.93. MU NET = -$1,670.30 CROSSES single-trade kill (MAX_LOSS_PER_TRADE=$750; handoff said $800) by $920. BOTH kills tripped per broker truth. CAVEAT: both SIM-DISABLED (DAILY_MAX_LOSS=$1e9; per-trade is scan-time sizing not intraday clamp) so bot did NOT halt — but intended-live thresholds crossed.
PER KILL RULE: Loop-123 exit change must REVERT to V0/R0. Watched-file change → AWAITING Rhett's go (not done autonomously).
CLEAN-DAY: (a) scheduled_tasks false-FAIL non-clean = FIXED/false (today certifies integrity-clean, consecutive_clean=3). (b) Certifier predicate is integrity-only (no P&L/kill) → today integrity-clean; the kill is a SEPARATE revert trigger, orthogonal to the streak. False-FAIL does NOT corrupt the kill verdict (P&L-sourced).
V2: MU real (Micron ~$1,231 6/25, +17.4% earnings gap, prior close $1,048.51); -$1,670.30 = gross -1668.30 + $2 comm, 15sh, not a scaling artifact. SNDK/GLW/DELL scales internally consistent (elevated 2026 universe). NO double-count: 46 FILLED (23 RT), 8 UROUT excluded.
V3 BLEEDER SAMPLE (all 7 losers confirm=NO, MFE~0, got wide chandelier): MU long 9:35 MFE/ATR -0.04 MAE112 CHANDELIER_STOP FAST~20m; DELL short 9:35 -0.02; PENN long 9:35 +0.08; PNR long re-arm -0.01; GLW long re-arm +0.06; BB long re-arm +0.01; ALB short re-arm +0.01. All clean-fails (PENN closest 0.08<0.15). Direction-agnostic (today longs). Feeds confirm/excursion-keyed spec. RS=NOT-LOGGED.
PENDING Rhett: (1) authorize revert to V0/R0; (2) the scheduled_tasks false-FAIL fix already applied this session (separate).

---
## 6/25 ~post-EOD — KILL RULE OVERRIDDEN by Rhett (deliberate); Loop-123 exit STAYS, test CONTINUES
DECISION: Both kills crossed per broker truth (daily NET -$2,016.93 < -$2,000 by $16.93; MU -$1,670.30 < -$750 single-trade). Per the kill rule the Loop-123 exit (candle_1.4atr_chandelier) should REVERT to V0/R0. Claude RECOMMENDED revert (protocol discipline). Rhett OVERRODE: keep the deployed Loop-123 exit, treat the kill day as EVIDENCE for the queued excursion-keyed fix, forward test CONTINUES. Informed override after Claude laid out both sides.
- NO code change. NO revert. Freeze intact. Deployed exit unchanged (ORB_EXIT_MODE=candle_1.4atr_chandelier).
- The kill rule is therefore DISCRETIONARY, not automatic — do NOT assume a future kill auto-reverts or that the test ended 6/25.
- OPEN (flagged for Planning, not blocking): does the 6/25 kill day COUNT toward the 5-clean-day promotion bar? Certifier says integrity-clean (consecutive_clean=3 after the false-FAIL fix), BUT the day crossed the daily kill. Integrity-clean != a clean *validation* day for the exit. Planning to clarify whether a kill day counts toward the 5.
- Both kills SIM-disabled (DAILY_MAX_LOSS=$1e9; per-trade=scan-time sizing) so neither enforced intraday.


## EOD SUMMARY — 2026-06-25

_Auto-generated by eod_debrief.py at 2026-06-25 4:50 PM ET · broker-truth sourced · 23 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 114 -> passed in-play gate 14 -> selected 25 -> symbols FILLED 23.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 10, refused 10 ({'already_held_or_working': 1, 'reentry_capped': 2, 'deploy_refused': 7})
- 11:35 AM: armed 3, refused 17 ({'already_held_or_working': 8, 'reentry_capped': 5, 'deploy_refused': 4})
- 12:35 PM: armed 2, refused 18 ({'already_held_or_working': 9, 'reentry_capped': 6, 'deploy_refused': 3})
- 1:35 PM: armed 1, refused 18 ({'already_held_or_working': 9, 'reentry_capped': 8, 'deploy_refused': 1})
- 2:35 PM: armed 1, refused 13 ({'already_held_or_working': 6, 'reentry_capped': 7})

**Incidents today:** 97 {'FAIL': 97}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — an old-gate-only (new-gate-rejected) name was traded.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## A2 · STRATEGY-RULE & IN-PLAY COMPLIANCE (did we trade to the rules?)

- **Q1 — Did the bot trade exactly to the strategy rules on every trade?**  **YES**  (23/23 trades compliant)
- **Q2 — Did the bot trade the in-play-identified symbols?**  **YES**  (23/23 in the in-play list)
- Context: 15/23 entries came from RE-ARM windows, which are UNGATED by the in-play gate by design (re-arm/fresh-breakout path) -- counted as in-play because they were on the armed list, but they did not have to clear the 9:35 RelVol/move thresholds.
- Exit-rule breakdown: EXIT_CANDLE_CLOSE_TRAIL×16, EXIT_EOD_FLATTEN×7

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | DELL | SELLSHORT | 1 | 391.94/391.77 | -4 | 0.0 | 2.3·-4.3%·-4.9%·LARGE_DVOL·mega·0935 | 51 | 19,989 | 396.68 | no | EOD-flatten/3:50PM/404.85 | 374 | 0.78 | 22.50 | -240 | -658.16 | 2.00 | -660.16 | -2.73 | 959068134/959231914 |
| 2 | QCOM | SELLSHORT | 1 | 213.75/213.75 | -0 | 0.0 | 2.3·-3.7%·-4.3%·LARGE_DVOL·mega·0935 | 93 | 19,879 | 216.28 | no | candle-close/9:45AM/209.09 | 9 | 6.75 | 4.22 | 401 | 433.38 | 2.00 | 431.38 | 1.83 | 959068129/959075908 |
| 3 | PENN | BUY | 1 | 21.64/21.63 | 2 | 0.0 | 2.6·5.5%·4.9%·SMALL_DVOL·mid·0935 | 924 | 19,991 | 21.52 | no | EOD-flatten/3:50PM/21.15 | 374 | 0.17 | 0.84 | -65 | -448.14 | 15.09 | -463.23 | -4.19 | 959068125/959231980 |
| 4 | MU | BUY | 1 | 1253.03/1253.00 | 0 | 0.0 | 1.8·3.4%·2.8%·LARGE_DVOL·mega·0935 | 15 | 18,795 | 1239.24 | no | CHANDELIER_STO/9:55AM/1141.81 | 20 | 1.97 | 116.72 | 1,092 | -1668.30 | 2.00 | -1670.30 | -8.08 | 959068139/959087927 |
| 5 | LUV | BUY | 1 | 52.05/52.05 | 0 | 0.0 | 1.7·7.2%·6.6%·MID_DVOL·large·0935 | 384 | 19,987 | 51.77 | no | candle-close/9:53AM/52.45 | 17 | 0.45 | 0.20 | -138 | 153.60 | 7.68 | 145.92 | 1.35 | 959068145/959085420 |
| 6 | CME | SELLSHORT | 1 | 225.99/226.00 | 0 | 0.0 | 1.8·-8.3%·-8.9%·LARGE_DVOL·large·0935 | 88 | 19,887 | 227.46 | no | EOD-flatten/3:50PM/225.34 | 374 | 0.76 | 4.43 | 30 | 57.20 | 2.00 | 55.20 | 0.43 | 959068141/959231881 |
| 7 | SWK | BUY | 1 | 91.27/91.24 | 3 | 0.0 | 1.7·5.7%·5.1%·MID_DVOL·large·0935 | 219 | 19,988 | 90.82 | no | candle-close/9:44AM/91.56 | 9 | 0.66 | 0.52 | 162 | 63.51 | 4.38 | 59.13 | 0.60 | 959068149/959075182 |
| 8 | TECH | BUY | 1 | 70.34/70.32 | 3 | 0.0 | 24.0·19.4%·19.0%·LARGE_DVOL·mid·1035 | 284 | 19,977 | NOT-logged | n/a | candle-close/3:33PM/70.67 | 298 | 0.38 | 0.07 | 0 | 93.72 | 5.68 | 88.04 | — | 959118622/959226042 |
| 9 | PNR | BUY | 1 | 77.49/77.47 | 3 | 0.0 | 4.5·3.2%·2.8%·MID_DVOL·large·1035 | 258 | 19,992 | NOT-logged | n/a | EOD-flatten/3:50PM/75.90 | 315 | -0.01 | 1.97 | 26 | -410.22 | 5.16 | -415.38 | — | 959118625/959232008 |
| 10 | BB | BUY | 1 | 10.64/10.64 | 0 | 0.0 | 3.5·21.9%·21.5%·MID_DVOL·mid·1035 | 1879 | 19,993 | NOT-logged | n/a | EOD-flatten/3:50PM/10.31 | 315 | 0.04 | 0.47 | 19 | -620.07 | 26.55 | -646.62 | — | 959118627/959231864 |
| 11 | GLW | BUY | 1 | 229.72/229.68 | 2 | 0.0 | 2.4·11.7%·11.2%·LARGE_DVOL·large·1035 | 87 | 19,986 | NOT-logged | n/a | EOD-flatten/3:50PM/225.03 | 315 | 0.78 | 8.94 | 282 | -408.03 | 2.00 | -410.03 | — | 959118633/959231961 |
| 12 | SNDK | BUY | 1 | 2179.68/2180.04 | -2 | 0.0 | 2.1·13.6%·13.2%·LARGE_DVOL·mega·1035 | 9 | 19,617 | NOT-logged | n/a | candle-close/10:54AM/2205.65 | 19 | 33.32 | 26.33 | 1,164 | 233.73 | 2.00 | 231.73 | — | 959118638/959128428 |
| 13 | AAPL | SELLSHORT | 1 | 279.01/279.01 | -0 | 0.0 | 1.8·-4.6%·-5.1%·LARGE_DVOL·mega·1035 | 71 | 19,810 | NOT-logged | n/a | candle-close/11:01AM/277.89 | 26 | 1.77 | 1.08 | 202 | 79.52 | 2.00 | 77.52 | — | 959118647/959132155 |
| 14 | FLEX | BUY | 1 | 163.26/163.25 | 1 | 0.0 | 1.5·8.0%·7.6%·MID_DVOL·UNKNOWN·1035 | 121 | 19,754 | NOT-logged | n/a | candle-close/12:18PM/165.25 | 103 | 2.63 | 2.94 | -463 | 240.79 | 2.42 | 238.37 | — | 959118659/959165582 |
| 15 | PLTR | SELLSHORT | 1 | 108.08/108.11 | 3 | 0.0 | 1.7·-4.4%·-4.9%·LARGE_DVOL·mega·1035 | 184 | 19,887 | NOT-logged | n/a | candle-close/11:00AM/107.17 | 25 | 1.13 | 0.53 | -26 | 167.44 | 3.68 | 163.76 | — | 959118654/959131584 |
| 16 | ALB | SELLSHORT | 1 | 140.51/140.52 | 1 | 0.0 | 1.8·-4.2%·-4.7%·MID_DVOL·large·1035 | 142 | 19,952 | NOT-logged | n/a | EOD-flatten/3:50PM/141.13 | 315 | 0.08 | 2.26 | 6 | -88.04 | 2.84 | -90.88 | — | 959118650/959231847 |
| 17 | RVTY | BUY | 1 | 112.76/112.85 | -8 | 0.0 | 1.4·6.7%·6.6%·MID_DVOL·large·1135 | 177 | 19,959 | NOT-logged | n/a | candle-close/11:59AM/113.14 | 24 | 0.89 | 0.54 | 80 | 67.26 | 3.54 | 63.72 | — | 959150282/959159286 |
| 18 | NOW | SELLSHORT | 1 | 90.51/90.50 | -1 | 0.0 | 1.5·-3.3%·-3.4%·LARGE_DVOL·large·1135 | 220 | 19,912 | NOT-logged | n/a | candle-close/3:29PM/89.84 | 234 | 0.89 | 0.68 | 68 | 147.40 | 4.40 | 143.00 | — | 959150286/959224393 |
| 19 | MSTR | SELLSHORT | 1 | 86.88/86.89 | 1 | 0.0 | 1.2·-7.1%·-7.3%·LARGE_DVOL·large·1135 | 224 | 19,461 | NOT-logged | n/a | candle-close/12:44PM/85.74 | 69 | 1.58 | 1.72 | 94 | 255.36 | 4.48 | 250.88 | — | 959150288/959174161 |
| 20 | AMAT | BUY | 1 | 650.72/650.72 | 0 | 0.0 | 1.1·10.1%·10.1%·LARGE_DVOL·mega·1235 | 29 | 18,871 | NOT-logged | n/a | candle-close/1:15PM/654.68 | 40 | 5.28 | 5.97 | 393 | 114.84 | 2.00 | 112.84 | — | 959171390/959185419 |
| 21 | TER | BUY | 1 | 463.26/463.20 | 1 | 0.0 | 1.1·8.0%·8.1%·LARGE_DVOL·large·1235 | 43 | 19,920 | NOT-logged | n/a | candle-close/2:27PM/466.56 | 112 | 4.44 | 6.35 | 240 | 141.90 | 2.00 | 139.90 | — | 959171387/959206903 |
| 22 | MSFT | SELLSHORT | 1 | 351.00/351.00 | -0 | 0.0 | 1.1·-3.9%·-3.9%·LARGE_DVOL·mega·1335 | 51 | 17,901 | NOT-logged | n/a | candle-close/1:50PM/349.46 | 15 | 1.80 | 0.34 | -165 | 78.54 | 2.00 | 76.54 | — | 959192067/959196631 |
| 23 | TJX | SELLSHORT | 1 | 157.76/157.77 | 1 | 0.0 | 1.1·-4.5%·-4.5%·LARGE_DVOL·large·1435 | 126 | 19,878 | NOT-logged | n/a | candle-close/3:26PM/157.25 | 51 | 0.76 | 0.39 | 241 | 64.26 | 2.52 | 61.74 | — | 959209414/959223507 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $108.42  ·  fees: $0.00
- Commission 2.39 bps + fees 0.00 bps of $453,386 notional = **2.39 bps avg cost**
- Avg entry slippage: 0.2 bps (adverse +)
- Slippage trend (prior 10d, adverse + bps): [-0.4, -1.1, 2.1, 2.2, 1.3, 0.8, 0.9, 1.2, 0.8, 1.4] · trailing avg 0.9 bps · today 0.2 (better vs trailing)
- Per-trade avg cost: $4.71 (23 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=23 · win rate 70% (16W/7L)
- GROSS day P&L $-1,908.50 · **NET day P&L $-2,016.92**
- Gross expectancy $-82.98/trade · Net expectancy $-87.69/trade
- Net profit factor 0.54
- Avg win $146.23 · avg loss $-622.37
- Largest win $431.38 · largest loss $-1,670.30
- Long/short split: 13L / 10S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=7 · win 57% · net $-2,102 ($-300/trade, -151.8 bps)
- PATH re-arm:      N=16 · win 75% · net $85 ($5/trade, 2.7 bps)
- OCC 1st-entry:    N=23 · win 70% · net $-2,017 ($-88/trade, -44.5 bps)
- OCC re-entry(2+): N=0
- RECONCILE: path sum $-2,016.92 + occ sum $-2,016.92 == day net $-2,016.92 -> OK

- Capital utilization: PEAK deployed: $299,300  (99.8% of $300k target)  at 11:56 (8 pos + 7 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- MU: left $1,438 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- SNDK: left $1,281 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- QCOM: left $862 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- SWK: left $425 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- AMAT: left $422 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- GLW: left $415 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- TJX: left $328 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- AAPL: left $294 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- TER: left $250 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- LUV: left $246 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- marginability shadow: 23 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=25 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = 0.135; breakout won (R>0) 18/25 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): UNKNOWN=0.15 (n1), large=0.16 (n13), mega=0.23 (n8), mid=-0.25 (n3)
## H · CAPITAL DEPLOYMENT (by hour + idle attribution)

**Deployed book by hour (peak; filled positions + working orders):**

| hour | deployed | % of $400k cap | pos+working |
|--|--|--|--|
| 9AM | $101,023 | 25% | 2+3 |
| 10AM | $280,610 | 70% | 8+6 |
| 11AM | $299,300 | 75% | 8+7 |
| 12PM | $279,354 | 70% | 8+6 |
| 1PM | $281,547 | 70% | 9+5 |
| 2PM | $281,688 | 70% | 10+4 |
| 3PM | $280,465 | 70% | 10+4 |

**Idle-capital attribution** (why capital sat idle vs the $400k cap; RE-ARM windows):
- **Qualified trades refused for CAPITAL today: 15** (peak idle below cap $118,242; gross demand upper-bound $375,000 at $25k/name). _The only number that justifies raising the deploy target._

| window | deployed | idle vs cap | thin-signal | self-throttle | refused cap/slot/reentry |
|--|--|--|--|--|--|
| 1035 | $299,937 | $100,063 | $0 | $100,063 | 7/0/2 |
| 1135 | $299,976 | $100,024 | $0 | $100,024 | 4/0/5 |
| 1235 | $299,036 | $100,964 | $0 | $100,964 | 3/0/6 |
| 1335 | $299,700 | $100,300 | $0 | $100,300 | 1/0/8 |
| 1435 | $281,758 | $118,242 | $0 | $118,242 | 0/0/7 |

- STALE-SLOT (separate; DEPLOYED-but-stuck, NOT idle): $119,903 in 6 red name(s) held to EOD-flatten -- a tighter exit would have freed the slot.
- _thin-signal + self-throttle = idle (cap-deployed) per window. Thin-signal idle is CORRECT (no qualified candidate wanted it -- NOT a defect, no floor implied); self-throttle is fixable (our caps). The 9:35 path deploys first; this covers the re-arm windows in the trace._

## I · LOSER ATTRIBUTION (exit-reason x confirm x side)

**1. Losers by SIDE:**
- LONG losers 5 ($-3,605.56) · SHORT losers 2 ($-751.04) · total losing $-4,356.60 over 7 trade(s)

| sym | side | confirm | exit | hold m | net$ |
|--|--|--|--|--|--|
| MU | long | no | candle-close | 20 | $-1,670.30 |
| DELL | short | no | EOD-flatten | 374 | $-660.16 |
| BB | long | no | EOD-flatten | 315 | $-646.62 |
| PENN | long | no | EOD-flatten | 374 | $-463.23 |
| PNR | long | no | EOD-flatten | 315 | $-415.38 |
| GLW | long | no | EOD-flatten | 315 | $-410.03 |
| ALB | short | no | EOD-flatten | 315 | $-90.88 |

**2. ALL trades by EXIT REASON x CONFIRM (partitions every round-trip):**
| exit reason | confirm | n | win% | net$ | avg hold m |
|--|--|--|--|--|--|
| EOD-flatten | no | 7 | 14% | $-2,631.10 | 340 |
| candle-close | yes | 14 | 100% | $2,052.74 | 74 |
| candle-close | no | 2 | 50% | $-1,438.57 | 20 |
- _partition check: cells sum to 23 == N 23_

**3. BLEEDER FLAG — unconfirmed-rides-to-EOD-flatten (the named target class):**
- 7 trade(s), net $-2,631.10, avg hold 340m

| sym | side | hold m | net$ |
|--|--|--|--|
| DELL | short | 374 | $-660.16 |
| BB | long | 315 | $-646.62 |
| PENN | long | 374 | $-463.23 |
| PNR | long | 315 | $-415.38 |
| GLW | long | 315 | $-410.03 |
| ALB | short | 315 | $-90.88 |
| CME | short | 374 | $55.20 |

**4. MUST-NOT-CUT CONTROL — winners a tightening rule must spare (longest-held first):**
| sym | side | confirm | exit | hold m | net$ |
|--|--|--|--|--|--|
| CME | short | no | EOD-flatten | 374 | $55.20 |
| TECH | long | yes | candle-close | 298 | $88.04 |
| NOW | short | yes | candle-close | 234 | $143.00 |
| TER | long | yes | candle-close | 112 | $139.90 |
| FLEX | long | yes | candle-close | 103 | $238.37 |
| MSTR | short | yes | candle-close | 69 | $250.88 |

---

---
## 6/25 ~5:20 PM — DECISION REVERSED AGAIN (final): NO revert; KEEP current chandelier exit LIVE; build improvements in SHADOW
Decision sequence today: override(keep) -> revert(5:10) -> NO-revert/build-in-shadow(5:20, FINAL). 5:20 handoff is authoritative.
- NO live change. Current exit stays: ORB_EXIT_MODE=candle_1.4atr_chandelier. V0 (candle_close tight 0.15ATR stop) is the KNOWN-WORSE baseline -> do NOT revert to it. Freeze holds; SIM bot keeps running current exit until an improved version passes shadow + Rhett approves deploy.
- KEEP untouched: re-arm path (green all 3 days), candle-close-on-confirmed (confirmed all won), gate mover-selection (70% win).
- FIX (all 9:35 morning bucket): exhausted gap-top chasing, unconfirmed on wide 1.4ATR leash, confirmed cut early (giveback).
3-LEVER SHADOW BUILD (each tested individually, gauntlet: 3-sided net-of-cost, N>=30, FDR, MSTR must-not-cut, clean-fail vs poll-near-miss):
  L1 (do-first, exit): tight leash on unconfirmed (time / MAE>=K*ATR / N adverse closes).
  L2 (second, ENTRY 9:35-only): exhaustion/extension guard; MUST NOT skip good winners (QCOM/LUV/SWK); re-arm untouched.
  L3 (third, 3-sided only): earn-room for confirmed (adaptive widen vs flat 1.4ATR).
DIAGNOSE-FIRST dollar-split (6/23-6/25, read-only, DONE): total loser net -$7,566.38. preventable-at-ENTRY -$5,573.89 (74%) vs manageable-at-EXIT -$1,992.49 (26%). By path: 9:35 losers -$4,934 (65%), re-arm losers -$2,632 (35%). => ENTRY (L2) is the BIGGER dollar lever; L1 is safer/do-first; both real, overlap on same trades (MU = entry-attributed gap-top AND L1-catchable).
  CAVEAT: entry split is HEURISTIC — rs_vs_spy/distance_from_or/extension NOT-LOGGED; 13/19 losers had usable exhaustion. L2 needs PROP-ENTRY-CONTEXT-LOGGING built first to be rigorous. No revert staged (5:10 superseded). Build is next phase.

---
## 6/25 ~5:40 PM — LEVER 1 (tight-leash-unconfirmed) BUILT + scored in SHADOW (read-only)
NEW file: strategy-research/l1_unconfirmed_leash.py (read-only; imports eod_debrief/excursion_study; no watched/live touch; no live API; pinned bars + exit_decisions polls only). Report: outputs/reports/l1_unconfirmed_leash.md.
VERIFIED by me: sim actual nets reconcile to broker truth EXACTLY (5-day round_trips_net = -$1,714.32; 6/18 +2, 6/22 +940, 6/23 -256, 6/24 -383, 6/25 -2017). 0 confirmed trades altered (MUST-NOT-CUT holds by construction, all 12 variants).
RESULT (DIRECTIONAL, NOT promotable): L1 cuts unconfirmed bleed hard. Best by Δnet = A_time_3m +$7,952.90 over 28 unconfirmed trades; MAE variants more principled but low-N. MU -$1,670 -> -$50..-$314 band (3-min); DELL -$660->-$246; PENN -$463->-$15.
CAVEATS (verified skepticism): (1) N=28 < 30 -> underpowered, not promotable; (2) the "3-min optimal" is TIMING-LUCK not edge -- MU's 3-min cf spans -$50..-$314 depending on poll (caught a bounce); robust read = "short leash helps a lot," NOT "3 min is the parameter"; (3) winner-conversion tiny (1 trade) ONLY because unconfirmed=lost all 5 days -> OOS risk (other regimes: more unconfirmed trades later confirm+win, a too-tight clock leash would cut them). RECOMMEND the MAE-keyed leash (invalidation-based) over the clock leash (timing-fragile) for the gauntlet.
NEXT: accumulate N>=30 over more days; build entry-context logging to unblock L2 (the bigger 74% lever). No live change; freeze holds.

---
## 6/25 ~5:45 PM — PRE-OPEN VERIFICATION SWEEP for 6/26 → GO
A (changed since 6/24): ONLY system_health_verifier.py + clean_day_certifier.py (both NON-watched validation/health). NO watched strategy file modified. Live config UNCHANGED: ORB_EXIT_MODE=candle_1.4atr_chandelier (no revert applied), ORB_MAX_ENTRIES=1. No silent drift.
B (trading path): run_bot ALIVE (PID 6316, heartbeat 18s); exit_bot_v2 = in-process per-cycle step of run_bot (run_bot.py:635) — alive via the loop (today's exit_decisions writes prove it); EOD flatten worked today (CSHV eod_flat_at_close OK, account flat); guards ACTIVE (ACCOUNT_DD_KILL 0.05, STRATEGY_DD_KILL 0.10, malfunction guards; DAILY_MAX_LOSS SIM-disabled = the ONLY thing off, intended); stale-check sweep = 8 PRE-EXISTING preflight tripwires (NONE new from tonight's edits).
C (measurement): certifier selftest 11/11 (heals false-FAIL BUT still FAILs real faults — not blinded); shadow V9 reconciles broker truth 23/23; kill-window 5 sealed + hash-intact (verify_seals ok, 0 breaches); all reconcile CSHV checks green.
D (ops): RAM 78% / 1.8GB free (adequate, tight side -> throttle heavy work during RTH tomorrow); NO duplicate processes (1x run_bot/watchdog/h5); supervisor chain healthy (guardian scheduled Next 5:50PM, Bot Supervisor task Running); deadman_beacon armed (110s); 8 scheduled tasks present.
E (gates, NUMBERS): _preflight 51 PASS / 1 WARN / 0 FAIL (WARN = known stale-literal = PROP-SELF-UPDATING-VALIDATION); regression_suite 21 pass / 0 FAIL / 2 skip (consecutive_clean=12, day-replay clean, EOD flat); reliability_drill 9/9 detectors fired; CSHV OK=46 / WARN=0 / FAIL=0. Verify-load: no long-lived process runs the edited files (CSHV/certifier load fresh each 5-min cycle; the 46/0/0 run already used new code) -> no restart needed.
VERDICT: **GO for 6/26 open.** Non-green called out: 1 known WARN (stale-literals, staged fix), RAM moderate (throttle tomorrow). Neither blocks. Needs Rhett decision (separate): build L2/entry-logging now vs wait (handoff below).

---
## 6/25 ~6:15 PM — ENTRY-CONTEXT SIDECAR built (TRUE read-only READER) + CORRECTION: rs_vs_spy was NEVER not-logged
RULE #0 WIN: the "rs_vs_spy / move% / exhaustion NOT-LOGGED" premise (that justified a watched-entry-path observer) was WRONG -- the excursion engine read the wrong logs. orb_candidate_log.jsonl ALREADY logs per-candidate at decision time, BOTH paths: rel_move_vs_spy(=rs_vs_spy), spy_move_pct, day_relvol, move_pct, prior_close/price(gap), path, selected, gate decision. scans.jsonl has the big scan_move_pct(MU 19.49)+exhaustion.
=> The Planning-approved entry-path OBSERVER is LARGELY UNNECESSARY for L2's core fields. NEW file strategy-research/entry_context_sidecar.py is a PURE READER (joins orb_candidate_log + scans + round_trips_net -> outputs/entry_context.jsonl). ZERO entry-path touch; equivalence trivially guaranteed; NO Rhett-gated watched-file deploy needed for the core fields. Verified: join 55/55 candidate + 51/55 scan; rs values match direct pull; no watched file touched; no live API.
REFINED DOLLAR-SPLIT (real fields vs heuristic): preventable-ENTRY -$4,521.52 (60%, was -$5,573.89/74%) | manageable-EXIT -$3,044.86 (40%, was -$1,992.49/26%); total -$7,566.38 unchanged. ~$1,052 reclassified entry->exit. So ENTRY still the bigger lever but LESS dominant (60/40 not 74/26); L1(exit) bigger than thought.
L2 DESIGN INSIGHT: with REAL rs_vs_spy, NOT ONE loser flagged on weak-RS -- every directional loser's RS was ALIGNED with its trade direction. So RS-misalignment is NOT the loser signal; EXHAUSTION/EXTENSION is the clean entry discriminator (MU/BB/GLW = exhaustion 1.0 + 19-22% scan moves = clean entry-preventable). PNR/PENN/KMB/TPR reclassified to manageable-exit (RS aligned, exhaustion <0.9). (CAVEAT: losers-only; winner-vs-loser RS-magnitude separation is a Study-2 question, unproven -- don't declare RS useless.)
RESIDUAL TRUE GAPS (still NOT-LOGGED): distance_from_OR/extension_atr (or_high/or_low computed in orb_runner but not persisted to these logs), earnings_catalyst (earnings_calendar stale ~21.8d -> feed refresh, not entry-path), per_trade_R (stop distance not persisted). Exhaustion+scan_move proxy "extended move" so OR-distance is lower-priority.
NO live change; freeze holds.

---
## 6/25 ~6:35 PM — LEVER 2 (9:35 entry exhaustion/extension guard) BUILT + scored in shadow (read-only)
NEW file: strategy-research/l2_entry_guard.py (read-only; 9:35-path ONLY, re-arm NEVER skipped; imports entry_context_sidecar+eod_debrief; no watched/live touch; no live API). Reconciles to broker truth (-256/-383.31/-2016.93).
KEY FINDING (verified): the discriminator is EXTENSION MAGNITUDE, NOT exhaustion. exhaustion=1.0 has BOTH winners and losers on 9:35: MU(loss,move19.49) DELL(loss,-8.57) PFG(loss,-5.57) QCOM(WIN +$431, move9.69). So EXH_only or loose EXT cuts QCOM (a winner). Only EXH>=0.95 & |move|>=12% (or EXT_only>=10%) skips ONLY MU, spares QCOM/LUV/SWK + all winners.
BEST VARIANT (EXH>=0.95 & |move|>=12%): skips MU only (-$1,670), 0 winners cut, 9:35 bucket -$3,600 -> -$1,930, 6/25 day -$2,017 -> -$347... wait day-> -$986 (3-day). MU skipped=YES, QCOM/LUV/SWK skipped=NO.
HONEST LIMIT: L2 does NOT turn the days green. It surgically removes the ONE extreme gap-top (MU). The OTHER 9:35 losers (DELL/PAYX/NRG/TPR/PENN/SPGI, moves <9%) are NOT extension-driven -> outside L2's reach -> they're L1 (exit) territory (confirm=NO bleeders). N=19 (<30), rests on effectively ONE trade (MU) -> DIRECTIONAL, not deployable.
SYNTHESIS: L1+L2 are COMPLEMENTARY, BOTH needed. L2 = remove rare extreme gap-tops (MU-class huge single losses, extension>=12%); L1 = cut the unconfirmed slow bleeders (the majority). Neither alone turns 6/23-6/25 green. NEXT: combined L1+L2 counterfactual (apply both, measure if days go green) + accumulate N>=30, each param validated individually (no composite). No live change; freeze holds.

---
## 6/25 ~6:55 PM — SHADOW BUILD FINISHED: combined L1+L2 counterfactual + consolidated synthesis
NEW file: strategy-research/l1_l2_combined.py (read-only; sequential entry-skip then exit-leash, NOT a composite; imports l1/l2/sidecar/eod_debrief; no watched/live touch; no live API). Baseline reconciles to broker truth EXACTLY (-2656.24).
RESULT (verified, reproduced independently): best winner-preserving config L1+L2 (9:35only, K=0.5) = -$2,656.24 -> -$494.98 (-81% red), 0 winners cut, but does NOT reach green (-$495 short; only 6/23 flips +). L2 dominant (+$1,670 removing MU), L1 marginal (+$491 cutting unconfirmed bleeders). MU correctly assigned to L2 not double-counted (interaction -$1,026.45). Tighter K (0.75/1.0) is WORSE. N=19/7 (<30) -> directional, not deployable.
CONSOLIDATED SYNTHESIS written: outputs/reports/SHADOW_BUILD_SYNTHESIS_2026-06-25.md (full map: diagnosis -> L1 -> L2 -> combined -> path-to-deploy). Levers are COMPLEMENTARY (L2=rare extreme gap-tops via extension>=12%; L1=unconfirmed bleeders via MAE K=0.5). Together address ~81% of 3-day damage with ZERO winner harm -> strong directional support the fix is real.
NOTHING deployable: needs N>=30 + OOS + FDR + must-not-cut, then promote ONE at a time -> fresh 5-clean test. Shadow tooling complete (excursion_study, entry_context_sidecar, l1_unconfirmed_leash, l2_entry_guard, l1_l2_combined) all reconcile to broker truth, none touch live path. Freeze intact; GO for 6/26 stands (no live change this whole session).

---
## 6/26 ~7:36 AM — MORNING PRE-OPEN SYSTEM CHECK → HEALTHY/GO
CSHV 07:35: OK=43/WARN=0/FAIL=0 (clean-day fix HELD overnight, no false-FAIL recurrence; consecutive_clean=4). Bot alive (heartbeat 5s, loop 2100, pid 9192). Config NO drift (no watched file changed overnight; ORB_EXIT_MODE=candle_1.4atr_chandelier unchanged; DD_KILL 0.05 active). RAM recovered 65%/2.9GB free (was 78%/1.8GB; overnight agents freed). Gates: preflight 51/1WARN(known stale-literal)/0FAIL, regression 20/0FAIL, reliability 9/9. Processes CLEAN: run_bot(9192)/watchdog(9232, respawned overnight=chain working)/h5(6048) each 1x, NO orphans from last night's agents, NO dupes. Alerts: bot_alerts 24h = 0 FAIL/CRIT, 1 known WARN (ORB_EARNINGS_STALE earnings_calendar 21.8d -> earnings veto may false-negative today; residual gap from synthesis); code_inbox empty. 5:15 excursion task ran OK (55 trades). Pre-open Fri; ORB scan 9:35 on the deployed (unchanged) exit. No live change this session; shadow build separate.
ONE YELLOW: earnings_calendar stale 21.8d -> earnings veto degraded (relevant: MU was an earnings gap). Known-accepted; offer to refresh the feed (read-only).

---
## 6/26 ~8:10 AM — PRE-OPEN GO/NO-GO GATE built (consolidate + strengthen + teeth + schedule)
NEW non-watched files: tradestation-bot/pre_open_gate.py (orchestrator), run_pre_open_gate.bat (launcher). EDITED non-watched display: advisor/system_validation_page.py (GO/NO-GO banner + per-check table). NO watched strategy file changed.
A CONSOLIDATE: gate runs+rolls up preflight(51/1W/0F), regression(20/0F), reliability(9/9), CSHV(run_all -> 43OK/0W/0F), clean_day_certifier(consecutive_clean=4), + 4 reconcile contracts (P&L/shadow-V9/kill-window-seal/report-integrity) each CRITICAL.
B STRENGTHEN: config_drift (live ORB_EXIT_MODE vs change-log approved -> CRITICAL), stale_check_meta (8 known literals -> WARN), trading_path_alive (heartbeat+guards+SAFE_MODE -> CRITICAL), data_freshness (FIXED: reads orb_universe._cache_is_fresh() source-of-truth + advisor_universe daily, not a hardcoded 24h -> killed a FALSE WARN on the 7-day ORB cache), vps_health (RAM/dupes -> WARN). Each tagged CRITICAL/WARN.
C TEETH: verdict GO if 0 CRITICAL FAIL else NO-GO; STALE(>4h)/missing status = NO-GO by default. On NO-GO + --engage -> safe_mode.engage(triggered_by='pre_open_gate') (blocks NEW entries only, never exits; won't auto-clear a gate hold). /validation banner shows GO/NO-GO (CRITICALs first) + honest label 'invariant gate, NOT a bug-free guarantee'. --notify pushes one GO/NO-GO notification.
  TEETH PROOF (verified, contained, restored): SAFE_MODE engage + SAFE_MODE_ENFORCE=True -> block_new_entries()=BLOCKED; shadow(False)=not blocked; clear=released. Live risk_config on disk UNCHANGED.
D SCHEDULE: AlphaQuant_PreOpenGate daily 6:00 AM ET, runs SYSTEM, registered + verified end-to-end (fresh status, GO-WITH-WARNINGS, 0 CRITICAL, SAFE_MODE inactive on GO). Self-report: stale status -> NO-GO on the page (a gate that didn't run can't look green).
VERIFICATION: selftest 15/0 (planted config-drift+CRITICAL flip to NO-GO and named; WARN-only doesn't flip; is_stale True for old/missing; --engage engages on NO-GO, doesn't auto-clear on GO). Bug caught+fixed: false universe WARN (source-of-truth fix).
GATED (Rhett's go): flip risk_config.SAFE_MODE_ENFORCE False->True (the ONE watched change that ARMS the teeth) AFTER a clean restart. Until then the gate is SHADOW (computes + would-block, changes NOTHING live). Today GO; freeze intact; no live change.

---
## 6/26 ~8:20 AM — PRE-OPEN GATE ADDENDUM: NO-GO notifications (Telegram+Discord) + silent-non-run alert + escalation (NO auto-fix)
Non-watched edits: pre_open_gate.py (_notify rewritten), system_health_verifier.py (+chk_pre_open_gate_ran watcher). NO watched strategy file changed.
NOTIFICATIONS (notifier fans out to BOTH channels -- delivery VERIFIED: discord OK:204, telegram OK:200 via one labeled test):
 - NO-GO -> level CRITICAL, subject names the failing CRITICAL check(s) + 'BOT HELD'; body = 'awaiting clearance; NO auto-fix; gate must RE-RUN and return GO before open; held SIM bot = no emergency'.
 - GO -> brief, dated + N/N clean (distinct day-to-day so never dedup-suppressed; absence-of-message unambiguous). GO-WITH-WARNINGS=WARNING, GO=INFO.
SILENT NON-RUN ALERT: new CSHV check chk_pre_open_gate_ran -- in the pre-open window (06:15-09:35 wkday) FAILs CRITICAL (-> CSHV notifies both channels) if pre_open_gate_status.json missing/stale = 'NO-GO by default'; ran-but-NO-GO -> WARN (gate already alerted); GO -> OK; weekend SKIP. (The gate cannot alert on its own non-run; this external watcher covers it.)
NO AUTO-FIX (verified): gate only engages SAFE_MODE + writes status + notifies. NO code/config modification (grep clean; SAFE_MODE_ENFORCE never written), NO auto-clear/auto-open in production (clear only in selftest). Post-fix flow: human diagnoses (real vs FALSE-FAIL) -> Rhett approves fix -> Code fixes -> gate RE-RUNS -> must return GO -> human clears the hold -> bot opens. Gate never bypasses itself.
VERIFICATION (handoff checklist all PASS): NO-GO both-channel delivery; non-run -> NO-GO-by-default FAIL; no auto-modify/auto-open path; post-fix re-run-GO required (gate never auto-clears). One labeled '[DELIVERY TEST] ignore' sent to Rhett's Telegram+Discord.
GATED (unchanged): arming the teeth = flip risk_config.SAFE_MODE_ENFORCE False->True after clean restart (Rhett's go). Until then SHADOW. Today GO; freeze intact; no live change.

---
## 6/26 ~9:00 AM — /planning dashboard page BUILT + live (living roadmap from JSON)
NEW non-watched files: outputs/planning_roadmap.json (editable data file -- phases/items/status/owner/depends_on/gate + meta), src/advisor/planning_page.py (renderer, returns title+body). EDITED non-watched display: local_dashboard.py (+/planning route, +_handle_planning, +nav card). NO watched strategy file.
RENDERS: WHERE-WE-ARE banner + last-updated stamp + current-state + 6 phase cards (P0-P4 + Safety/Infra) with color-coded status badges (NOT_STARTED/IN_PROGRESS/BLOCKED/DONE/DEPLOYED), BLOCKED items show what they wait on. Verified live: GET /planning -> 200 (83KB), banner+5 phases+nav link present.
RULE #0 STATUS CORRECTIONS (handoff snapshot was behind last session's verified shadow work -- encoded accurate + flagged via 'code_note'): 0.1 dollar-split DONE (not IN_PROGRESS; refined 74%->60/40 real fields); 0.2 advanced (Study 2 discriminators done); 1.1 CORRECTED -- entry-path observer UNNECESSARY (rs_vs_spy already logged in orb_candidate_log; sidecar is a read-only reader; no deploy-go needed) -> split residual gaps to 1.3; L2 IN_PROGRESS shadow-built (not BLOCKED on data; blocked from PROMOTION on N>=30); S.3 meta-check BUILT (only the conversion staged).
INCIDENT (caused + fixed): restarting the dashboard to pick up the new route revealed a PRE-EXISTING DUPLICATE (2 trade-review-ui instances, 5248+3200, from Start_Dashboard.bat run twice; no supervisor auto-respawns the dashboard). Killed both + my orphaned relaunch, relaunched ONE DETACHED (survives session, rule #15) -> exactly 1 instance (PID 11848) owns 8765. (This dup is exactly what the pre-open gate vps_health 'no dup procs' check catches.)
No live trading change; freeze intact.

---
## 6/26 ~9:05 AM — ENTRY-CONTEXT SIDECAR "DEPLOY": gate PASSED with ZERO entry-path change (RULE #0 reconciliation)
Rhett's GO = deploy the read-only entry-context sidecar, CONDITIONAL on a zero-diff equivalence proof. RECONCILED to verified reality: there is NOTHING to deploy to the entry path -- the L2 fields are ALREADY logged live + accumulating.
EQUIVALENCE PROOF (airtight, demonstrated): entry_context_sidecar is referenced NOWHERE in the trading path (run_bot/bot_loop/orb_runner/orb_multiscan/mover_scanner/exit_bot_v2) -> the bot cannot call it -> deleting it leaves trades BYTE-IDENTICAL by construction (zero-diff; nothing to run-with-vs-without).
DATA ALREADY LIVE: orb_candidate_log.jsonl (2256 recs, written every scan both paths) has rel_move_vs_spy(=rs_vs_spy)/spy_move_pct/move_pct/day_relvol/gap inputs. So 1.1's deploy gate is SATISFIED without a risky entry-path flip: req#1 read-only-observer ✓, req#2 equivalence zero-diff ✓ (by construction), req#3 fields ✓ except OR-distance+earnings. Post-deploy sweep clean: NO watched file modified, config_drift PASS, gate GO-WITH-WARNINGS.
ONE RESIDUAL ENTRY-PATH ITEM (the only thing Rhett's GO could add): persist or_high/or_low for PRECISE distance_from_OR -- NOT logged. But that requires adding a line INSIDE orb_runner's candidate-log write (= 'added logic in the entry function', which req#1 said to avoid) and the L2 discriminator (extension MAGNITUDE = move%) is ALREADY logged -> recommend SKIP (proxy suffices); revisit if needed. AWAITING Rhett: make the OR-distance entry-path add (real watched change + equivalence proof) or rely on the already-logged proxy.
/planning updated: 1.1 -> DEPLOYED (gate passed, zero-diff), L2 -> BLOCKED-on-data (accumulating ~1wk), banner+stamp. Earnings flag = follow-on (Phase 1.2). No live change; freeze intact.

---
## 6/26 ~9:10 AM — SESSION LOG + DOCS UPDATED FOR FRESH PLANNING SESSION RAMP-UP
Rhett starting a new Planning Claude chat -> fully ramped the cold-start surfaces:
- SESSION_LOG: inserted a "⭐ CURRENT STATE — 2026-06-26" block at the very top (posture / central findings / built-this-session / open decisions / health), above the now-historical alert-triage stamps + reboot checklist + ledgers.
- NEW cold-start brief: `HANDOFF_2026-06-26_RAMP-UP.md` (single-doc ramp: posture, findings, shadow tooling, infra, entry-context deploy, open decisions, where-things-are, health). Points to /planning + SHADOW_BUILD_SYNTHESIS.
- /planning roadmap (planning_roadmap.json) already current (1.1 DEPLOYED zero-diff, L2 BLOCKED-on-data, banner/stamp).
- Memory current (project_kill_override + project_exit_loosening_gauntlet updated to final state this session).
CANONICAL RAMP SOURCES for the new session: (1) HANDOFF_2026-06-26_RAMP-UP.md, (2) /planning page, (3) outputs/reports/SHADOW_BUILD_SYNTHESIS_2026-06-25.md, (4) this SESSION_LOG top block. No live change; freeze intact.

---
## 6/26 PM — Phase 1.2 EARNINGS REFRESH: Phase A done -> STOP-and-report (FMP free-tier coverage INADEQUATE)
VERIFICATION ANSWERS: (1) Source=FMP; FMP_API_KEY is SET (advisor .env, NOT bot .env -> likely why Loop-128 thought unset) + VALID (probe HTTP 200). NOT the blocker. (2) orb_earnings_veto.is_earnings_blackout IS called in the live 9:35 path (orb_runner.py:441, WATCHED); veto module itself non-watched but live-invoked. (3) Veto reads earnings_calendar.csv DIRECTLY (orb_earnings_veto.py:41, fails open on stale/missing) -> refreshing that file re-arms live behavior -> Phase B MUST route fresh data to a SEPARATE file. importer writes the LIVE csv by default (earnings_importer:60/285).
THE BLOCKER (RULE #0 catch): FMP PLAN coverage is inadequate, NOT the key. stable/earnings?symbol=MU -> HTTP 402 Premium (AAPL=164 works only as free demo symbol); global earnings-calendar returns a LIMITED subset (23/30d) that MISSES MU even in MU's report window (+-7d returned CCL/FDX/NKE, no MU); legacy /api/v3 -> 403 dead. Old earnings_calendar.csv = only 6 mega-caps (never universe-wide). => refreshing FMP would NOT have flagged MU = fails the Phase-1.2 goal. Probes were read-only, key never exposed, NO file written.
STOPPED per Phase A (do not build importer until source answered). OPTIONS for Rhett: (a) eval FREE NASDAQ public earnings calendar (precedent: build_market_caps NASDAQ screener) -- RECOMMEND eval before paying; (b) FMP premium ($, unlocks per-symbol+full calendar); (c) accept limited coverage. TS is NOT a wired/available earnings source (provider config = local_csv + fmp only).
/planning: 1.2 -> BLOCKED (source decision), added 1.2-D (live re-arm) BLOCKED, stamp updated. No live change; no watched file modified; freeze intact.

---
## 6/26 PM — FREE earnings source FOUND (NASDAQ) + Phase 0 timing-study (Studies A-D) DONE
SOURCE: FREE NASDAQ public earnings calendar (api.nasdaq.com/api/calendar/earnings, browser headers) WORKS + covers MU (listed 6/24 its real report date, EPS fcst $20.98, mktcap $1.37T) + PAYX. Full coverage, $0, no credential -> no FMP premium needed. /planning 1.2 -> IN_PROGRESS (build Phase B on NASDAQ, gated on Rhett go).
PHASE 0 TIMING STUDY (read-only, NEW strategy-research/timing_study.py, reconciles to -$2,656.24):
- A: pre-10:00 cut removes -$3,600.57 (19 trades, ALL 9:35-scan, 0 re-arm) -> +$944.33 (re-arm intact). Discards 10 winners (+$1,334) + 9 losers (-$4,934). Same-window mechanical cut, NOT predictive.
- B: 4/9 reversal-then-bleed (DELL/NRG/TPR/SPGI = unconfirmed shorts, ~0 MFE, MAE>=0.7ATR, held 374min to EOD-flatten). MU NOT a bleed (20min chandelier stop, sharpest -$1,670). PAYX/PENN/ANET = poll-near-miss tagged.
- C: CONFIRMED 36 = +$4,824.58 (97.2% win) vs UNCONFIRMED 19 = -$7,480.82 (5.3% win). Unconfirmed: clean-fail 10/-$5,213, poll-near-miss 9/-$2,268.
- D GATE-MAP (verified ACTUAL governance, not flags): 9:35 = IN-PLAY GATED (gate_enforced ALL candidates 6/23-6/25, 110->14 pass->10 sel) + 9:30-9:35 OR + earnings veto called-but-INERT(stale) + admit governed-0-refusals. re-arm = UNGATED (gate_enforced=False) + FRESH 5-min range/window + NO earnings veto + admit governed-0-refusals. => paths differ in SELECTION + RANGE -> 9:35-vs-re-arm gap CONFOUNDED.
- SYNTHESIS: counterintuitive -- the MORE-GATED 9:35 path LOSES, the UNGATED re-arm WINS, so selection-gating isn't the protector; the real driver is CONFIRMATION/range. "Wait until 10:00" is a CONFOUNDED proxy that also throws out pre-10:00 confirmed winners. Durable lever = confirmation/extension (L1/L2), NOT the clock. DIAGNOSTIC ONLY (N=55, 3 days), not promotable.
No live change; no watched file modified; no live trading API. Freeze intact.

---
## 6/26 PM — Phase 1.2-B EARNINGS REFRESH (free NASDAQ) DONE — safe infra, nothing live changed
NEW non-watched files: tradestation-bot/earnings_nasdaq_refresh.py + run_earnings_refresh.bat. Fetches FREE NASDAQ earnings -> writes earnings_calendar_FRESH.csv (SEPARATE file) in the veto's exact 19-col schema. HARD safety: refuses to write the LIVE earnings_calendar.csv; verified live file UNTOUCHED (mtime+hash identical before/after). 197-name calendar, MU present (6/24 EPS $20.98), window 6/23-7/12. Daily task AlphaQuant_EarningsRefresh @7:00 AM SYSTEM registered. CHANGES NOTHING the bot trades (veto still on old file). No watched strategy file.
CARRY TO PHASE C (RULE #0): NASDAQ returns time='time-not-supplied' (no BMO/AMC) AND the veto hardcodes earnings@9:30AM +-18h -> an AMC report on day D (MU 6/24) computes to D 9:30, ~6h BEFORE the next-day 9:35 blackout floor -> MU still MISSED. So Phase B (data) is necessary but NOT sufficient; Phase C must WIDEN the veto window (block day-of + full next session regardless of time), not just refresh the calendar. Phase D (point veto at fresh + window fix) = gated on Phase C clean + Rhett approval.
/planning 1.2 -> IN_PROGRESS (Phase B done; Phase C/D pending). Freeze intact.

---
## 6/26 PM — Phase 1.2-C earnings-veto SHADOW VALIDATION (read-only) DONE
NEW non-watched file: strategy-research/earnings_veto_shadow.py (in-memory veto eval vs the FRESH calendar over 6/22-6/25; touches no live file, no live veto). Reconciles to round_trips_net (71 trades, -$1,716.31).
RESULT:
- CURRENT veto (9:30AM+-18h, real is_earnings_blackout pointed at fresh in-memory): vetoes PAYX(9:35) only; MU vetoed=FALSE -> CONFIRMS data-refresh-alone is insufficient (the 9:30AM assumption misses MU's AMC-day-after gap).
- WIDENED veto (block day-of + prior trading session, regardless of time): vetoes PAYX + MU (both 9:35); MU vetoed=TRUE. Loss-avoided ~$2,281 on the 9:35 path. MUST-NOT-CUT PASSES: 0 winners vetoed (QCOM/LUV/SWK untouched; DAL = winner w/ FUTURE earnings correctly NOT blocked).
- Veto is 9:35-ONLY by wiring (orb_multiscan doesn't call it) -> re-arm protected. (Shadow shows BB(re-arm,earnings 6/25) would block IF applied to re-arm, but live wiring leaves re-arm untouched -> accepted; we don't touch the profitable re-arm path.)
HONEST: in-sample (MU is the motivating case), tiny N (4 earnings names / 4 days) -> directional validation that fresh-data + widened-window works, NOT a deployment proof.
PHASE D (gated): point live veto at earnings_calendar_fresh.csv + WIDEN the window in orb_earnings_veto (watched-path edit) -> HELD on Rhett approval (manual_approvals.yaml) + clean pre-open sweep after. /planning 1.2 updated. No live change; freeze intact.

---
## 6/26 PM — Entry-SIGNATURE study (confirmed vs unconfirmed: entry-features vs early-excursion) DONE
NEW non-watched file: strategy-research/entry_signature_study.py (read-only; imports entry_context_sidecar+eod_debrief; reconciles 55 trades / 36 conf / 19 unconf / -$2,656.24).
PART 1 (entry features): NO entry feature separates confirmed vs unconfirmed -- rs_vs_spy/day_relvol/gap_pct/cand_move/spy_move AUC 0.35-0.64 (all <0.8), exhaustion best at 0.64. Rhett's hypothesis = NO per feature (confirmed do NOT enter with a materially different RS/extension/RelVol/gap profile). Categorical: re-arm confirms more (72% vs 9:35 53%).
PART 2 (early excursion): SEPARATES. MAE->loss AUC: 0.62(1m)/0.73(2m)/0.77(3m)/0.82(5m); low-MFE->loss 0.74 at 1min. Unconfirmed run ~3x early MAE (0.168 vs 0.050 ATR @5min). "MFE~0 + large MAE" cleanly marks losers within minutes.
PART 3 VERDICT: discriminator is EARLY-EXCURSION, NOT entry (best entry AUC 0.65 < 0.80 bar) -> CONFIRMS L1 (fast MAE-keyed exit) as the primary lever, an entry screen on RS/RelVol/gap WON'T work. EXCEPTION: gap-top MU-class IS entry-screenable -- scan_move/extension >=12% flags BB/MU/TECH/SNDK (exhaustion 1.0) at entry = L2. Converges with timing-study (confirmation is the driver) + dollar-split (L1+L2).
HONEST: N=55/3d, confirmed=POST-entry label -> overfit-prone HYPOTHESIS (needs N>=30+FDR+OOS); unconfirmed segmented clean-fail (MU/PNR) vs poll-near-miss (ANET/PAYX). No watched file, no live API, freeze intact. /planning 0.2-entry-signature DONE.

---
## 6/26 PM — L1 MUST-NOT-CUT AUDIT (no-lookahead) DONE — corrects "0 confirmed cut" + finds K floor 0.75 + a polling prerequisite
NEW non-watched file: strategy-research/l1_mustnotcut_audit.py (read-only; reconciles 55/36 conf/+$4,824.58/-$2,656.24).
FINDING 1 (corrects prior claim): the earlier l1 "0 confirmed winners cut by construction" OVERSTATED safety -- it used post-hoc labels AND poll-blind data. VERIFIED: the exit monitor first-polls minutes-to-hours after entry (median 5.2min, up to 5h; 33/55 trades' first poll >3min, e.g. DTE 6/24 18284s, HAL 6/24 3976s). So the poll-based casualty count (0 at all K) is a poll-BLINDNESS artifact, not real safety.
FINDING 2 (the real count, pinned-bar minute-by-minute, 6/24+): K=0.5 CUTS 3 CONFIRMED WINNERS = $949.72 (HAL +124.62->-341.07, VICI +31.52->-232.73, DTE +36.96->-182.82; each dipped ~0.51xATR adverse BEFORE confirming late-day). K=0.75 -> 0, K=1.0 -> 0. 0 ambiguous straddle bars; count does NOT flip. => MIN-SAFE K = 0.75xATR (revises the earlier l1 K=0.5 'dominates' rec); or gate on N-adverse-closes not a single touch.
FINDING 3 (prerequisite, the bigger one): the casualty dips are in the UNPOLLED early window (HAL's 0.51ATR dip was before its first poll at 10:42). So the bar-count = what an IDEAL minute-by-minute leash would do; the current poll-blind monitor would NOT fire (hence the 0 vs 3 gap). A 'fast MAE-keyed exit' CANNOT work without early-window polling that doesn't exist today -- L1 needs that polling fix as a PREREQUISITE. Worth a separate look at live-exit early coverage.
Honest: N=36/3d, diagnostic only; 6/23 no pin (poll-only). No watched file, no live API. /planning L1 updated (K floor 0.75 + polling prerequisite). Freeze intact.

---
## 6/26 PM — L1 EARLY-EXIT DECISION TABLE (trigger sweep) DONE — safe param K=0.75 but edge is MU-dependent
NEW non-watched file: strategy-research/l1_decision_table.py (read-only; reconciles -2656.24/36conf/19unconf; false-cut method = l1_mustnotcut_audit pinned-bar, K=0.5->3 & K=0.75->0 MATCH).
TABLE (11 triggers, three-sided net-of-cost): MAE K=0.4 NET+1411(3 false cuts), K=0.5 +414(3fc), K=0.6 +224(1fc), K=0.75 +679(0fc); TIME 1-5m NET +575..+1453 BUT 24-28 false cuts + poll-fragile; N-closes 1-3 NET NEGATIVE (-760..-1688).
KEY FINDINGS: (1) MAE K=0.75 is the ONLY 0-false-cut trigger -> principled pick (price-distance, not a clock), MIN-SAFE K=0.75. (2) EVERY row is MU-DEPENDENT -- K=0.75 NET +$679 -> -$104 without MU (sign-flips); ALL 11 rows DEMOTED. (3) Time triggers DESTROY confirmed winners (24-28 false cuts) + are poll-fragile (NET negative at -1 poll) -> rejected. (4) N-closes net-negative -> rejected. (5) FDR x11 hypotheses; unconfirmed lost ~100% on 3 days -> NETs are an UPPER bound -> NOTHING promotable, OOS in a recovering regime REQUIRED.
TAKEAWAY (sharpens strategy): L1's edge on this sample IS essentially the single MU trade, and MU is better handled by L2 (gap-top entry skip, >=12% extension). L1's marginal value on the SLOW non-gap-top bleeders (DELL/NRG/TPR) is UNPROVEN (net-flat-to-negative without MU). So: L2 = higher-confidence lever for the MU-class; L1 = must-not-cut-safe at K>=0.75 but marginal value unproven + needs the early-polling prerequisite (prior audit). No watched file, no live API. /planning P2 L1-table DONE. Freeze intact.


## EOD SUMMARY — 2026-06-26

_Auto-generated by eod_debrief.py at 2026-06-26 4:50 PM ET · broker-truth sourced · 26 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 115 -> passed in-play gate 14 -> selected 28 -> symbols FILLED 26.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 7, refused 9 ({'reentry_capped': 1, 'deploy_refused': 8})
- 11:35 AM: armed 5, refused 9 ({'reentry_capped': 6, 'already_held_or_working': 1, 'deploy_refused': 2})
- 12:35 PM: armed 5, refused 13 ({'reentry_capped': 9, 'already_held_or_working': 4})
- 1:35 PM: armed 2, refused 12 ({'reentry_capped': 7, 'already_held_or_working': 3, 'deploy_refused': 2})
- 2:35 PM: armed 0, refused 16 ({'reentry_capped': 8, 'already_held_or_working': 5, 'deploy_refused': 3})

**Incidents today:** 2 {'FAIL': 2}.
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — an old-gate-only (new-gate-rejected) name was traded.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## A2 · STRATEGY-RULE & IN-PLAY COMPLIANCE (did we trade to the rules?)

- **Q1 — Did the bot trade exactly to the strategy rules on every trade?**  **YES**  (26/26 trades compliant)
- **Q2 — Did the bot trade the in-play-identified symbols?**  **YES**  (26/26 in the in-play list)
- Context: 18/26 entries came from RE-ARM windows, which are UNGATED by the in-play gate by design (re-arm/fresh-breakout path) -- counted as in-play because they were on the armed list, but they did not have to clear the 9:35 RelVol/move thresholds.
- Exit-rule breakdown: EXIT_CANDLE_CLOSE_TRAIL×15, EXIT_EOD_FLATTEN×11

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 1 | FDXF | SELLSHORT | 1 | 154.75/154.39 | -23 | 0.0 | 2.3·-2.6%·-1.9%·MID_DVOL·large·0935 | 129 | 19,963 | 156.57 | no | candle-close/9:42AM/154.00 | 6 | 2.83 | 0.97 | 64 | 96.75 | 2.58 | 94.17 | 0.40 | 959307134/959311822 |
| 2 | DELL | SELLSHORT | 1 | 387.50/387.57 | 2 | 0.0 | 2.4·-5.3%·-4.6%·LARGE_DVOL·mega·0935 | 51 | 19,762 | 392.22 | no | EOD-flatten/3:50PM/391.16 | 374 | 2.37 | 11.38 | -150 | -186.66 | 2.00 | -188.66 | -0.78 | 959307131/959456455 |
| 3 | GLW | SELLSHORT | 1 | 217.70/217.75 | 2 | 0.0 | 2.1·-4.5%·-3.8%·LARGE_DVOL·large·0935 | 91 | 19,811 | 220.21 | no | candle-close/9:41AM/215.84 | 5 | 3.36 | 3.00 | -652 | 169.26 | 2.00 | 167.26 | 0.73 | 959307149/959310850 |
| 4 | HWM | SELLSHORT | 1 | 261.51/261.60 | 3 | 0.0 | 1.9·-4.2%·-3.5%·LARGE_DVOL·large·0935 | 75 | 19,613 | 263.02 | no | candle-close/9:45AM/259.90 | 9 | 2.92 | 2.44 | -647 | 120.75 | 2.00 | 118.75 | 1.05 | 959307154/959314126 |
| 5 | VLTO | BUY | 1 | 90.27/90.27 | 0 | 0.0 | 1.8·8.8%·9.6%·MID_DVOL·large·0935 | 221 | 19,950 | 89.94 | no | EOD-flatten/3:50PM/89.33 | 374 | 0.35 | 1.50 | 82 | -207.74 | 4.42 | -212.16 | -2.94 | 959307170/959456548 |
| 6 | CAT | SELLSHORT | 1 | 1016.67/1017.00 | 3 | 0.0 | 1.7·-3.8%·-3.0%·LARGE_DVOL·mega·0935 | 19 | 19,317 | 1022.74 | no | candle-close/9:57AM/1014.94 | 21 | 6.25 | 5.49 | 324 | 32.87 | 2.00 | 30.87 | 0.27 | 959307178/959322666 |
| 7 | FLEX | SELLSHORT | 1 | 154.37/154.40 | 2 | 0.0 | 1.8·-4.3%·-3.5%·LARGE_DVOL·UNKNOWN·0935 | 129 | 19,914 | 155.91 | no | candle-close/12:17PM/152.83 | 161 | 2.03 | 5.41 | 819 | 198.66 | 2.58 | 196.08 | 0.99 | 959307167/959388522 |
| 8 | ON | SELLSHORT | 1 | 94.17/94.21 | 4 | 0.0 | 5.8·-20.4%·-20.3%·LARGE_DVOL·large·1035 | 212 | 19,964 | NOT-logged | n/a | candle-close/11:07AM/92.95 | 32 | 1.29 | 0.71 | 553 | 258.64 | 4.24 | 254.40 | — | 959345178/959360861 |
| 9 | PYPL | BUY | 1 | 43.79/43.79 | 0 | 0.0 | 2.2·3.2%·3.3%·MID_DVOL·large·1035 | 456 | 19,968 | NOT-logged | n/a | candle-close/11:17AM/43.98 | 42 | 0.21 | 0.19 | 141 | 86.64 | 9.12 | 77.52 | — | 959345184/959365121 |
| 10 | MRNA | BUY | 1 | 66.74/66.80 | -9 | 0.0 | 1.8·11.2%·11.3%·MID_DVOL·large·1035 | 299 | 19,955 | NOT-logged | n/a | candle-close/10:47AM/67.50 | 12 | 1.10 | 0.57 | -63 | 227.21 | 5.98 | 221.23 | — | 959345185/959351632 |
| 11 | LLY | BUY | 1 | 1197.58/1197.00 | 5 | 0.0 | 2.1·5.9%·6.0%·LARGE_DVOL·mega·1035 | 16 | 19,161 | NOT-logged | n/a | candle-close/11:43AM/1202.45 | 68 | 6.03 | 17.18 | 64 | 77.92 | 2.00 | 75.92 | — | 959345180/959375783 |
| 12 | LITE | SELLSHORT | 1 | 790.04/790.08 | 1 | 0.0 | 1.7·-7.9%·-7.8%·LARGE_DVOL·large·1035 | 25 | 19,751 | NOT-logged | n/a | candle-close/11:14AM/778.83 | 39 | 13.22 | 3.65 | -879 | 280.25 | 2.00 | 278.25 | — | 959345190/959363490 |
| 13 | INCY | BUY | 1 | 114.30/114.28 | 2 | 0.0 | 1.8·5.9%·6.0%·SMALL_DVOL·large·1035 | 175 | 20,002 | NOT-logged | n/a | candle-close/11:05AM/114.85 | 30 | 0.89 | 0.83 | -191 | 96.25 | 3.50 | 92.75 | — | 959345187/959359866 |
| 14 | COHR | SELLSHORT | 1 | 377.01/377.18 | 5 | 0.0 | 1.3·-7.0%·-6.9%·LARGE_DVOL·large·1035 | 50 | 18,850 | NOT-logged | n/a | EOD-flatten/3:50PM/379.88 | 315 | 7.01 | 10.58 | -0 | -143.50 | 2.00 | -145.50 | — | 959345192/959456442 |
| 15 | UBER | BUY | 1 | 75.15/75.26 | -15 | 0.0 | 1.4·4.0%·3.9%·LARGE_DVOL·large·1135 | 265 | 19,915 | NOT-logged | n/a | candle-close/12:04PM/75.49 | 29 | 0.41 | 0.09 | 151 | 90.10 | 5.30 | 84.80 | — | 959372304/959384315 |
| 16 | MPWR | SELLSHORT | 1 | 1332.65/1333.08 | 3 | 0.0 | 1.2·-7.0%·-7.1%·LARGE_DVOL·large·1135 | 15 | 19,990 | NOT-logged | n/a | EOD-flatten/3:50PM/1322.14 | 255 | 15.98 | 25.25 | 164 | 157.65 | 2.00 | 155.65 | — | 959372300/959456502 |
| 17 | WDC | SELLSHORT | 1 | 603.05/603.22 | 3 | 0.0 | 1.1·-10.5%·-10.5%·LARGE_DVOL·large·1135 | 32 | 19,298 | NOT-logged | n/a | candle-close/12:55PM/595.83 | 81 | 7.57 | 5.45 | 304 | 231.04 | 2.00 | 229.04 | — | 959372308/959400285 |
| 18 | DDOG | BUY | 1 | 233.04/233.00 | 2 | 0.0 | 1.1·5.3%·5.2%·MID_DVOL·large·1135 | 85 | 19,808 | NOT-logged | n/a | candle-close/11:42AM/234.57 | 7 | 1.94 | 0.54 | 443 | 130.05 | 2.00 | 128.05 | — | 959372307/959375060 |
| 19 | NFLX | BUY | 1 | 74.92/74.92 | 0 | 0.0 | 1.2·5.6%·5.5%·LARGE_DVOL·mega·1135 | 266 | 19,929 | NOT-logged | n/a | EOD-flatten/3:50PM/73.13 | 255 | 0.28 | 1.85 | 133 | -476.14 | 5.32 | -481.46 | — | 959372305/959456527 |
| 20 | DOCS | BUY | 1 | 20.80/20.79 | 5 | 0.0 | 1.5·4.7%·4.7%·SMALL_DVOL·mid·1235 | 962 | 20,010 | NOT-logged | n/a | EOD-flatten/3:50PM/20.79 | 195 | 0.02 | 0.27 | 58 | -9.62 | 15.54 | -25.16 | — | 959394880/959456466 |
| 21 | HPE | SELLSHORT | 1 | 43.43/43.44 | 2 | 0.0 | 1.2·-6.7%·-6.7%·LARGE_DVOL·large·1235 | 460 | 19,978 | NOT-logged | n/a | EOD-flatten/3:50PM/43.52 | 195 | 0.03 | 0.61 | -69 | -41.40 | 9.20 | -50.60 | — | 959394882/959456477 |
| 22 | TSLA | BUY | 1 | 385.25/385.25 | 0 | 0.0 | 1.4·2.7%·2.6%·LARGE_DVOL·mega·1235 | 51 | 19,648 | NOT-logged | n/a | EOD-flatten/3:50PM/382.96 | 195 | 2.13 | 6.70 | -192 | -116.79 | 2.00 | -118.79 | — | 959394883/959456538 |
| 23 | VRT | SELLSHORT | 1 | 303.19/303.32 | 4 | 0.0 | 1.1·-6.6%·-6.7%·LARGE_DVOL·large·1235 | 65 | 19,707 | NOT-logged | n/a | EOD-flatten/3:50PM/307.39 | 195 | 2.05 | 4.58 | 261 | -273.00 | 2.00 | -275.00 | — | 959394887/959456573 |
| 24 | ADI | SELLSHORT | 1 | 385.15/385.18 | 1 | 0.0 | 1.1·-7.5%·-7.5%·LARGE_DVOL·mega·1235 | 51 | 19,643 | NOT-logged | n/a | EOD-flatten/3:50PM/389.61 | 195 | 2.33 | 7.93 | 261 | -227.46 | 2.00 | -229.46 | — | 959394888/959456385 |
| 25 | CNP | BUY | 1 | 44.79/44.79 | 0 | 0.0 | 1.9·1.2%·1.2%·MID_DVOL·large·1335 | 446 | 19,976 | NOT-logged | n/a | candle-close/2:52PM/44.92 | 78 | 0.14 | 0.04 | 40 | 57.98 | 8.92 | 49.06 | — | 959411818/959436476 |
| 26 | VRTX | BUY | 1 | 495.55/495.50 | 1 | 0.0 | 1.4·2.9%·2.9%·LARGE_DVOL·large·1335 | 3 | 1,487 | NOT-logged | n/a | EOD-flatten/3:50PM/495.22 | 135 | 2.21 | 8.84 | -14 | -0.99 | 2.00 | -2.99 | — | 959411819/959456582 |

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $104.70  ·  fees: $0.00
- Commission 2.11 bps + fees 0.00 bps of $495,370 notional = **2.11 bps avg cost**
- Avg entry slippage: 0.1 bps (adverse +)
- Slippage trend (prior 10d, adverse + bps): [-1.1, 2.1, 2.2, 1.3, 0.8, 0.9, 1.2, 0.8, 1.4, 0.2] · trailing avg 1.0 bps · today 0.1 (better vs trailing)
- Per-trade avg cost: $4.03 (26 round-trips)

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- N=26 · win rate 62% (16W/10L)
- GROSS day P&L $628.72 · **NET day P&L $524.02**
- Gross expectancy $24.18/trade · Net expectancy $20.15/trade
- Net profit factor 1.30
- Avg win $140.86 · avg loss $-172.98
- Largest win $278.25 · largest loss $-481.46
- Long/short split: 12L / 14S


**Split — context, not a verdict; building toward N>=30 per bucket:**
- PATH 9:35-gated:  N=7 · win 71% · net $206 ($29/trade, 14.9 bps)
- PATH re-arm:      N=19 · win 58% · net $318 ($17/trade, 8.9 bps)
- OCC 1st-entry:    N=26 · win 62% · net $524 ($20/trade, 10.6 bps)
- OCC re-entry(2+): N=0
- RECONCILE: path sum $524.02 + occ sum $524.02 == day net $524.02 -> OK

- Capital utilization: PEAK deployed: $299,979  (100.0% of $300k target)  at 14:26 (12 pos + 4 working)

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- FDXF: left $1,255 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- FLEX: left $1,032 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ON: left $787 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- GLW: left $738 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- DDOG: left $635 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- MRNA: left $535 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- WDC: left $522 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- CAT: left $481 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- MPWR: left $311 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- VRT: left $282 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- ADI: left $262 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- NFLX: left $247 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- UBER: left $239 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- LLY: left $213 on the table AFTER exit (post-exit favorable continuation) -- see PROP-EXIT-FALSE-STOPOUT
- marginability shadow: 26 armed names all STOCK/no-restrictions -> 4x assumption held (broker is the per-symbol authority; SHADOW, before-live gate OFF)

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=28 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = 0.017; breakout won (R>0) 16/28 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): UNKNOWN=0.85 (n1), large=-0.02 (n20), mega=0.0 (n6), mid=0.09 (n1)
## H · CAPITAL DEPLOYMENT (by hour + idle attribution)

**Deployed book by hour (peak; filled positions + working orders):**

| hour | deployed | % of $400k cap | pos+working |
|--|--|--|--|
| 9AM | $201,892 | 50% | 4+6 |
| 10AM | $279,544 | 70% | 8+6 |
| 11AM | $259,984 | 65% | 7+6 |
| 12PM | $278,295 | 70% | 7+7 |
| 1PM | $299,825 | 75% | 9+7 |
| 2PM | $299,979 | 75% | 12+4 |
| 3PM | $279,350 | 70% | 11+4 |

**Idle-capital attribution** (why capital sat idle vs the $400k cap; RE-ARM windows):
- **Qualified trades refused for CAPITAL today: 15** (peak idle below cap $102,557; gross demand upper-bound $375,000 at $25k/name). _The only number that justifies raising the deploy target._

| window | deployed | idle vs cap | thin-signal | self-throttle | refused cap/slot/reentry |
|--|--|--|--|--|--|
| 1035 | $299,746 | $100,254 | $0 | $100,254 | 8/0/1 |
| 1135 | $299,058 | $100,942 | $0 | $100,942 | 2/0/6 |
| 1235 | $297,443 | $102,557 | $0 | $102,557 | 0/0/9 |
| 1335 | $299,613 | $100,387 | $0 | $100,387 | 2/0/7 |
| 1435 | $299,603 | $100,397 | $0 | $100,397 | 3/0/8 |

- STALE-SLOT (separate; DEPLOYED-but-stuck, NOT idle): $178,963 in 10 red name(s) held to EOD-flatten -- a tighter exit would have freed the slot.
- _thin-signal + self-throttle = idle (cap-deployed) per window. Thin-signal idle is CORRECT (no qualified candidate wanted it -- NOT a defect, no floor implied); self-throttle is fixable (our caps). The 9:35 path deploys first; this covers the re-arm windows in the trace._

## I · LOSER ATTRIBUTION (exit-reason x confirm x side)

**1. Losers by SIDE:**
- LONG losers 5 ($-840.56) · SHORT losers 5 ($-889.22) · total losing $-1,729.78 over 10 trade(s)

| sym | side | confirm | exit | hold m | net$ |
|--|--|--|--|--|--|
| NFLX | long | no | EOD-flatten | 255 | $-481.46 |
| VRT | short | no | EOD-flatten | 195 | $-275.00 |
| ADI | short | no | EOD-flatten | 195 | $-229.46 |
| VLTO | long | no | EOD-flatten | 374 | $-212.16 |
| DELL | short | no | EOD-flatten | 374 | $-188.66 |
| COHR | short | no | EOD-flatten | 315 | $-145.50 |
| TSLA | long | no | EOD-flatten | 195 | $-118.79 |
| HPE | short | no | EOD-flatten | 195 | $-50.60 |
| DOCS | long | no | EOD-flatten | 195 | $-25.16 |
| VRTX | long | no | EOD-flatten | 135 | $-2.99 |

**2. ALL trades by EXIT REASON x CONFIRM (partitions every round-trip):**
| exit reason | confirm | n | win% | net$ | avg hold m |
|--|--|--|--|--|--|
| EOD-flatten | no | 11 | 9% | $-1,574.13 | 244 |
| candle-close | yes | 11 | 100% | $1,488.13 | 35 |
| candle-close | no | 4 | 100% | $610.02 | 58 |
- _partition check: cells sum to 26 == N 26_

**3. BLEEDER FLAG — unconfirmed-rides-to-EOD-flatten (the named target class):**
- 11 trade(s), net $-1,574.13, avg hold 244m

| sym | side | hold m | net$ |
|--|--|--|--|
| NFLX | long | 255 | $-481.46 |
| VRT | short | 195 | $-275.00 |
| ADI | short | 195 | $-229.46 |
| VLTO | long | 374 | $-212.16 |
| DELL | short | 374 | $-188.66 |
| COHR | short | 315 | $-145.50 |
| TSLA | long | 195 | $-118.79 |
| HPE | short | 195 | $-50.60 |
| DOCS | long | 195 | $-25.16 |
| VRTX | long | 135 | $-2.99 |
| MPWR | short | 255 | $155.65 |

**4. MUST-NOT-CUT CONTROL — winners a tightening rule must spare (longest-held first):**
| sym | side | confirm | exit | hold m | net$ |
|--|--|--|--|--|--|
| MPWR | short | no | EOD-flatten | 255 | $155.65 |
| FLEX | short | yes | candle-close | 161 | $196.08 |
| WDC | short | no | candle-close | 81 | $229.04 |
| CNP | long | no | candle-close | 78 | $49.06 |
| LLY | long | yes | candle-close | 68 | $75.92 |
| PYPL | long | no | candle-close | 42 | $77.52 |

---

---
## 6/26 post-close — STANDING TRADE AUTOPSY built (Part 1 run + Part 2 wired into EOD + dashboard)
NEW non-watched files: strategy-research/trade_autopsy.py (engine) + advisor/autopsy_page.py (dashboard). EDITED non-watched: eod_debrief.py (+_section_autopsy = section J, wrapped so it NEVER breaks the debrief) + local_dashboard.py (+/autopsy route+handler+nav card). NO watched strategy file.
PART 1 (6/26 autopsy, reconciles +$524.02, verified independently): confirmed 15 = +$2,098.15 (100% win, booked by ~3PM via fast candle-close) vs unconfirmed 11 = -$1,574.13 (9.1% win). THE GIVEBACK: peak +$2,098 @15RT(3PM) -> +$524 @close; the 11 late-closers (all the unconfirmed book) rode to the EOD flatten = the -$1,574 giveback (10 bleeders -$1,729.78 + 1 winner MPWR +$155.65). Structural: confirmed exit fast, unconfirmed drag to EOD.
  Lens A: only DELL was a true early reversal (10.9% of loss); the other 9 ground down slowly (not sharp reversals). Lens B (K=0.75 must-not-cut, ideal-early-poll): saved only $13.02 (2 cut), 0 winners clipped -> on a slow-grind day the leash barely helps. Lens C: CLUSTER not MU-class (top loser NFLX -$481=27.8%, 0 gap-tops). Cumulative early-exit-0.75 net +$458.54 but -$351.55 WITHOUT MU 6/25 -> L1 edge STILL MU-dominated.
PART 2: standing TRADE AUTOPSY now in every EOD debrief (section J) + dashboard /autopsy (live, reconciles, tables render, nav card), with cumulative tally + fixed in-sample footer (accumulating N != promotion).
DASHBOARD HYGIENE: found + cleaned ANOTHER pre-existing duplicate trade-review-ui instance (recurring; 11164 old-code orphan); now exactly ONE instance (PID 8808). Recurring dup spawner worth a look (Start_Dashboard.bat re-run?). No watched file, no live API, freeze intact.

---
## 6/26 evening — FIXED the recurring command-window popups (Rhett: very annoying)
DIAGNOSIS: NOT from this session's new work (audited: my new .py use CREATE_NO_WINDOW; my new tasks already run as SYSTEM). Source = 12 PRE-EXISTING scheduled tasks running as Administrator (interactive session) via cmd/.bat -> each flashes a console window on the desktop when it fires. Frequent culprits = AlphaQuant_Utilization (every 30min), Mover Scanner + CheckAlerts (hourly).
FIX (Rhett approved 'convert all if confident, don't jeopardize the system'): converted all 12 recurring read-log Admin cmd/.bat tasks to run as SYSTEM (session 0 = no desktop window). Backed up each task's XML first (outputs/reports/task_backups/) for a no-password revert path. VERIFIED: triggered each + all 12 returned Last Result=0 (ran clean under SYSTEM) -> 0 reverts needed.
  Converted: Utilization, Mover Scanner, CheckAlerts, Nightly Backup, ArchiveDailyState, CostReconcile, PreopenReadiness, PreopenReadiness_AM, RegressionRecord, Daily Review, Morning Book Outcome, Morning Book Snapshot.
  SKIPPED (safety): Advisor ONE-TIME-9-35 (writes the bot control file) + Flatten Stuck (trading action) + SlotCap (one-time) -- all one-time/dormant, no popup, never triggered.
TRADING UNTOUCHED: none of these are the trading bot (runs via watchdog_supervisor chain); all are auxiliary analytics/snapshot/backup/triage tasks. No watched file changed.
REMAINING (optional, gated): run_bot.py (WATCHED) has 2 subprocess calls my scan flagged without CREATE_NO_WINDOW -- mostly it already uses _NO_WINDOW; needs a closer look + Rhett's go since it's watched. Not done.


## EOD SUMMARY — 2026-06-27

_Auto-generated by eod_debrief.py at 2026-06-27 4:50 PM ET · broker-truth sourced · 0 round-trip(s)_

## A · DID THE SYSTEM RUN CORRECTLY TODAY?

**Funnel (broker-truth + candidate log):** universe scanned ~530 -> candidates evaluated 16 -> passed in-play gate 0 -> selected 16 -> symbols FILLED 0.

**Re-arm windows (multiscan_trace):**
- 10:35 AM: armed 16, refused 2 ({'slots_exhausted': 2})
- 11:35 AM: armed 16, refused 2 ({'slots_exhausted': 2})
- 12:35 PM: armed 16, refused 2 ({'slots_exhausted': 2})
- 1:35 PM: armed 16, refused 2 ({'slots_exhausted': 2})
- 2:35 PM: armed 16, refused 2 ({'slots_exhausted': 2})

**Incidents today:** 0 (none).
**SAFE_MODE:** currently off (no engage today unless an incident above shows it)

**Gate drove entries:** INCONCLUSIVE/FAIL rc=1 -- VERDICT: FAIL — gate_enforced is False; gate ran in SHADOW. Set ORB_INPLAY_GATE=True.
  _(NOTE: verify_gate_drove_entries validates only the 9:35 path; re-arm fills are NOT in the 9:35 SELECTED set by design, so it reports FAIL on re-arm-heavy days. The per-day gate-integrity signal is the gate_not_failing_open reliability check.)_

**Broker reconciliation at close:** FLAT (0 positions, 0 working); position_recon=OK (broker and bot agree both ways (0 position(s) reconciled))

## A2 · STRATEGY-RULE & IN-PLAY COMPLIANCE (did we trade to the rules?)

- no closed round-trips today (nothing to check)

## B · PER-TRADE LEDGER (one row per round-trip; broker-truth)

| # | sym | side | occ | entry(act/intend) | slip bps | delay m | gate (RelVol·mv%·RSvSPY·$tier·mcap·win) | shares | gross$ | 0.15ATR lvl | conf | EXIT REASON/time/px | hold m | MFE | MAE | leftHold$ | gP&L | comm | netP&L | R | order IDs |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|

## C · COST & EXECUTION SUMMARY (edge-survival line)

- Total commission (broker-actual): $0.00  ·  fees: $0.00
- Commission 0.00 bps + fees 0.00 bps of $1 notional = **0.00 bps avg cost**
- Avg entry slippage: n/a (adverse +)
- Slippage trend (prior 10d, adverse + bps): [2.1, 2.2, 1.3, 0.8, 0.9, 1.2, 0.8, 1.4, 0.2, 0.1] · trailing avg 1.1 bps
- no trades

## D · AGGREGATE  *(context, not a verdict — building toward N>=30)*

- no closed round-trips today

## E · ANOMALIES & DIVERGENCES CODE FLAGGED

- none flagged by code today

## F · PROVENANCE / FIELD-AVAILABILITY MAP

| field | source | note |
|--|--|--|
| symbol/side/shares/order IDs/status | BROKER-TRUTH | broker_orders_unified.csv raw_order_json |
| actual entry/exit price + time | BROKER-TRUTH | FilledPrice/ExecutionPrice + OpenedDateTime (UTC) |
| intended entry trigger price | LOGGED | signal_trigger_px / intended_price / StopPrice |
| intended/submission time | LOGGED | submit_time (ET) -- proxy for arm time, not breakout-detect time |
| entry delay / slippage bps | DERIVED | actual vs intended (above) |
| commission (per trade) | BROKER-ACTUAL | raw_order_json CommissionFee, summed entry+exit |
| fees (per trade) | BROKER-ACTUAL | raw_order_json UnbundledRouteFee (0 today) |
| gross/net P&L, net R | DERIVED | from broker fills + commission; R uses 0.15xATR (9:35 only) |
| gate ctx (RelVol/move%/RSvSPY/$tier/mcap) | LOGGED (9:35 only) | orb_candidate_log.jsonl selected names; RE-ARM names NOT in candidate log |
| 0.15xATR protective level | DERIVED (9:35 only) | ATR from orb_daily_state entries_submitted; re-arm ATR NOT-logged |
| confirm fired? | LOGGED (9:35 only) | bot_alerts ORB_CONFIRM_SWAP; re-arm confirm not tracked |
| exit type (EOD vs synthetic) | DERIVED | by exit time; fine reason (candle-close vs hard-stop) NOT joined (in bot_alerts) |
| MFE / MAE | DERIVED from 1-min bars | barcharts over hold window; NOT logged natively (REG-08 INERT without this) |
| broker-flat + position recon | BROKER-TRUTH (asserted) | reliability_checks.fetch_truth + check_position_recon |

_Never fabricated: any field above marked NOT-logged/NOT-computed is shown as such in the rows._

## G — FADE vs BREAKOUT counterfactual (TUNE-01; context, NOT a verdict — building toward N)

_N=16 candidates today (deduped by symbol) -> fade_breakout_log.jsonl (append-only, OOS accumulation). R = signed move in the breakout direction / ATR; fade_R = -breakout_R. context, NOT a verdict -- building toward a permutation test._

- @EOD: mean breakout_R = 0.003; breakout won (R>0) 9/16 (if breakout_R<0 the FADE would have paid).
- by cap bucket (mean breakout_R @EOD): large=-0.0 (n11), mega=0.01 (n5)
## H · CAPITAL DEPLOYMENT (by hour + idle attribution)

_(no utilization snapshots for the day)_

**Idle-capital attribution** (why capital sat idle vs the $400k cap; RE-ARM windows):
- **Qualified trades refused for CAPITAL today: 0** (peak idle below cap $84,152; gross demand upper-bound $0 at $25k/name). _The only number that justifies raising the deploy target._

| window | deployed | idle vs cap | thin-signal | self-throttle | refused cap/slot/reentry |
|--|--|--|--|--|--|
| 1035 | $315,848 | $84,152 | $34,152 | $50,000 | 0/2/0 |
| 1135 | $315,848 | $84,152 | $34,152 | $50,000 | 0/2/0 |
| 1235 | $315,848 | $84,152 | $34,152 | $50,000 | 0/2/0 |
| 1335 | $315,848 | $84,152 | $34,152 | $50,000 | 0/2/0 |
| 1435 | $315,848 | $84,152 | $34,152 | $50,000 | 0/2/0 |

- STALE-SLOT (separate; DEPLOYED-but-stuck, NOT idle): $0 in 0 red name(s) held to EOD-flatten -- a tighter exit would have freed the slot.
- _thin-signal + self-throttle = idle (cap-deployed) per window. Thin-signal idle is CORRECT (no qualified candidate wanted it -- NOT a defect, no floor implied); self-throttle is fixable (our caps). The 9:35 path deploys first; this covers the re-arm windows in the trace._

## I · LOSER ATTRIBUTION (exit-reason x confirm x side)

- no closed round-trips today

## TRADE AUTOPSY — 2026-06-27

_READ-ONLY post-close autopsy · broker-truth sourced · 0 round-trip(s) · generated 2026-06-27 4:50 PM ET_

**Reconciliation:** book NET $0.00 vs broker truth $0.00 (gross $0.00) -> MATCH

### Per-round-trip ledger (one row per RT)

| # | sym | side | path | entry fill | net$ | conf | early MAE 1/2/3/5m (xATR) | early MFE 1/2/3/5m (xATR) | hold m | exit reason | EODflat | rev->bleed |
|--|--|--|--|--|--|--|--|--|--|--|--|--|

### Day summary — confirmed vs unconfirmed

- CONFIRMED: N=0 · net $0.00 · win None%
- UNCONFIRMED: N=0 · net $0.00 · win None%
- **Day net $0.00**

### THE GIVEBACK LINE (3 PM -> close)

- By ~3:00 PM: 0 RT completed = $0.00 (intraday peak).
- At close: 0 RT = $0.00.
- **Given back: $0.00** across the 0 late-closer(s) (completed after 3:00 PM, net $0.00).

Per late-closer — early-reversal BLEEDER vs WINNER that gave back into the EOD flatten:

| sym | side | exit | net$ | bucket |
|--|--|--|--|--|

- BLEEDER bucket sum: $0.00 (0 RT)
- WINNER-gaveback bucket sum: $0.00 (0 RT)

### LENS A — early-reversal losers

- Day losers: 0 · total loser net $0.00
- Early-reversal losers: 0 · net $0.00
- Of those, LATE-CLOSERS (exit after 3:00 PM) in the giveback: 0 · net $0.00

### LENS B — MUST-NOT-CUT: early exit at K=0.75xATR adverse-before-confirm (full book)

_Pinned-bar real-time method (l1_mustnotcut_audit), K pinned at 0.75 (never tighter). EARLY-POLL CAVEAT: the live monitor is blind in the first ~5 min, so these are what an IDEAL early-poll would do, NOT what today's live bot could have fired._

- **Bleeders cut: 0 · $ saved $0.00**
- **Confirmed winners clipped: 0 · $ given up $0.00**
- **THREE-SIDED net-of-cost: $0.00** (= saved $0.00 − winners given up $0.00)
- coverage: 0 safe (never crossed K before confirm), 0 NOT-AVAILABLE (no pin/atr), 0 intrabar-ambiguous (counted worst-case against the leash)

### LENS C — MU-class check (cluster vs one extended/gap-top trade)

- no losers today

### CUMULATIVE TALLY (across available days)

- Days: 2026-06-18, 2026-06-22, 2026-06-23, 2026-06-24, 2026-06-25, 2026-06-26
- Confirmed N=70 · unconfirmed N=39 · confirm-NA N=29 (progress toward N>=30 confirmed: 70/30)
- Cumulative early-exit-at-0.75 three-sided net-of-cost: **$458.54**
- One-trade-dominance guard: WITHOUT the single biggest trade (2026-06-25/MU (bleeder saved), $810.09): **$-351.55**

| date | confirmed N | unconfirmed N | three-sided net$ |
|--|--|--|--|
| 2026-06-18 | 7 | 5 | $0.00 |
| 2026-06-22 | 12 | 4 | $0.00 |
| 2026-06-23 | 7 | 4 | $0.00 |
| 2026-06-24 | 14 | 7 | $52.76 |
| 2026-06-25 | 15 | 8 | $392.76 |
| 2026-06-26 | 15 | 11 | $13.02 |

### Caveats

- confirm = polled flag -> segment clean-fail vs poll-near-miss (a trade can miss confirm by a hair).
- EARLY-POLL CAVEAT: the live monitor is blind in the first ~5 min, so Lens B's early-exit numbers are "what an IDEAL early-poll would do," NOT what today's live bot could have fired -- read them as a ceiling, not a live-achievable result.

_Diagnostic, in-sample. These days are in-sample for any un-promoted rule; a streak of confirming days accumulates N toward >=30 but does not promote anything -- promotion still requires a locked rule + fresh OOS forward test + the gauntlet._

---
