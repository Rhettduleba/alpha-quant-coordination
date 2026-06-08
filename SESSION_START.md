# Alpha Quant — new-session ramp-up

Paste the block below at the start of a new Claude Code session (working
directory = the "Trade station Main" project root), filling in the task.

**FIRST STEP — name the session so it is findable in the sidebar later:**
run the slash command `/rename "<sub-project name>"` (e.g.
`/rename "Alpha Costs"`). A session name is set only by `/rename` or by
`claude -n "<name>"` at launch; an unnamed session just shows an
auto-generated summary, which is hard to navigate back to.

---

Ramp up on the Alpha Quant project before doing anything:

1. Read the State of Record — `C:\repos\alpha-quant-coordination\ALPHA_QUANT_STATE.md`.
   It has the current state, open items, and operating rules. Follow its §4
   "re-verify" list to check live bot/advisor state from the actual files; the
   §4 snapshot is dated, not current.
2. The three `CLAUDE.md` files (project root + `tradestation-bot/` +
   `ai-trading-strategy-agent/`) auto-load. Read the `feedback_*.md` files named
   in your `MEMORY.md` index — the index auto-loads, the files themselves don't.

Keep in mind: the bot trades live in SIM — propose-first for anything that
changes live behavior, and never touch files it reads/writes mid-cycle. Verify
before asserting. One question per turn. The observation period is in progress —
no tuning or architectural work until it completes. Git: the code repo's git
directory is `C:\repos\trade-station-main-git\` (run git from there); the
coordination repo is `C:\repos\alpha-quant-coordination\`.

TODAY'S TASK: <describe the task — or "tell me where things stand">

---

Shortcut: instead of pasting the whole block you can just say —
"Read C:\repos\alpha-quant-coordination\SESSION_START.md and follow it.
Today's task: ___"
