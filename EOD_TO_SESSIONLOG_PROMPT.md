# EOD → SESSION LOG (always, every trading day) — standing prompt
*Rhett directive 2026-06-30: the EOD debrief must reliably reach the SESSION_LOG **and** be readable by Planning (a fresh Planning chat couldn't read it — cause: the SESSION_LOG is ~585KB and Planning's web-fetch truncates large files, so the EOD block, appended at the bottom, never arrives).*

## THE FIX (do this every EOD, after the 4:50 PM debrief)
The 4:50 `AlphaQuant_EodReconciliation` task already APPENDS the EOD debrief block to `C:\AlphaQuant\SESSION_LOG.md`. Your job is to make it READABLE to Planning:

1. **Verify** today's block is in the local log:
   `grep "EOD SUMMARY — <today>" C:\AlphaQuant\SESSION_LOG.md` (also accept `--`). If missing, run `eod_debrief.py` manually.
2. **Push the SESSION_LOG** to coordination (so the full log is mirrored):
   copy `C:\AlphaQuant\SESSION_LOG.md` → `C:\repos\alpha-quant-coordination\SESSION_LOG.md`, commit, push.
3. **Push the STANDALONE EOD** (this is what Planning actually reads — small, not truncated):
   copy `C:\AlphaQuant\outputs\reports\eod_debrief_<today>.md` → BOTH `C:\repos\alpha-quant-coordination\eod_debrief_<today>.md` AND `C:\repos\alpha-quant-coordination\EOD_LATEST.md`, commit, push.
4. **Give Planning the fetch URL** (always-current small file):
   `https://raw.githubusercontent.com/Rhettduleba/alpha-quant-coordination/main/EOD_LATEST.md`
   (If Planning still says "can't read it," it hit a CDN cache — have it fetch the commit-pinned URL per the ramp template, or paste the EOD directly.)
5. **Log it**: one line in SESSION_LOG — `EOD pushed to coordination <date>: SESSION_LOG + EOD_LATEST.md @ <sha>`.

## WHY PLANNING COULDN'T READ IT (root cause + the real fix)
The EOD *is* in the SESSION_LOG and *is* pushed — verified both 585KB. The blocker is SIZE: a 585KB markdown file gets truncated by Planning's fetch tool, and the EOD block is at the END. The standalone `EOD_LATEST.md` (~10-15KB) is the reliable channel. **Standing recommendation: TRIM/ARCHIVE the SESSION_LOG** — move loops older than ~2 weeks to `SESSION_LOG_ARCHIVE_<month>.md`, keep the live SESSION_LOG under ~150KB so the whole thing is fetchable again. Until then, point Planning at `EOD_LATEST.md` for the day's debrief.

## AUTOMATE IT (so it never depends on a session being open)
The cleanest durable fix is to make the standalone-EOD push part of the EOD task chain (a 5th action after the debrief that copies `eod_debrief_<today>.md` → coordination `EOD_LATEST.md` + `git push`). Until that's wired, this prompt is the manual backstop — run it every trading evening.
