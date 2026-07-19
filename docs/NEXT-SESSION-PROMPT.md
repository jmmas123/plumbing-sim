# Next-session init prompt — paste into the fresh window

We're adding **M3 — a bend-loss term to the relief pipe's head loss (`Krel`)** in the Bodega Triple
stormwater sim. This is the last tracked refinement of the relief model.

Read first, in order:
1. `docs/STATE.md` — where the project stands (Open leads #3 is this, M3).
2. `docs/superpowers/specs/2026-07-18-outlet-relief-coupling-design.md` — §3.2 (relief as a pipe,
   the `Krel = 1 + Ke + f·L/D` derivation) and §3.6 **M3** (the bend-loss gap the adversarial review
   flagged: ~10–15% capacity, currently omitted).
3. `docs/superpowers/specs/2026-07-18-relief-diameter-design.md` — the just-shipped sibling change
   (relief diameter), for the pattern (control in the outlet fieldset, tagged, wired via `readS`).
4. `.superpowers/sdd/progress.md` — the FINISHED ledgers for the coupling and relief-diameter.
5. `CLAUDE.md` — project rules.

**What just shipped (do not redo):** the relief now has its own diameter (`dRelief`, default 8″,
independent of the collector), merged to `main` `3cfbfa3` / STATE bump `b2cd310`, pushed, republished.
Before that, the outlet–relief coupling. The relief's pipe head loss is
`Krel = 1 (exit) + 0.5 (entrance) + fDarcy·Lrel/D (friction)` in `solveCollector`'s outlet block
(locate by content — `const Krel = 1 + 0.5 + fDarcy*Lrel/D`). M3 adds a **bend-loss term**.

**The crux (why brainstorm, not just edit):** the relief is the collector's *straight-through* run
past the Y-T (the Y-T replaced a 90° elbow — the FALL turns down, the relief goes straight). So
whether the relief run has ANY bends between the Y-T and where it daylights on the rear platform is a
**site fact only the user knows**. If it runs straight to daylight, M3 may be ~zero (a documentation
note, or a `nBends=0` default); if it turns to reach the platform, add the bend K.

**START WITH BRAINSTORMING** (`superpowers:brainstorming` — HARD GATE before any plan/code). Resolve
with the user:
- How many direction changes does the real relief run have between the Y-T and daylighting? (0? 1?)
- What kind of bends (long-radius K≈0.3 / standard 90° K≈0.5–0.75 / mitered K≈1.1)?
- Expose bend count as its own tagged input (like `Lrel`/`dRelief`), or fix a conservative default?
- Does tab ③'s `reliefSplit` need any change, or is M3 confined to the tab-② `Krel`? (Check: the
  momentum split uses `Kb`, not the pipe `Krel` — likely tab-② only, but confirm.)

**This DOES change the head-balance physics** (unlike the diameter change): the relief carries
~10–15% less, so relief-limited flood thresholds shift DOWN. Therefore **re-run an adversarial physics
check** on the implemented `Krel` (the coupling pattern), and **update the shifted guard numbers** —
but do NOT weaken the C1 direction ("10″ re-pipe: relief HELPS under a clear outlet") or the
blocked-outlet monotonicity. Then `superpowers:writing-plans` → `superpowers:subagent-driven-development`.

**Load-bearing conventions:**
- **Branch before implementing** (e.g. `feat/relief-bend-loss`). After ANY edit to `sim/index.html`
  run `node sim/verify.mjs` green — it extracts the solver, so keep `solveCollector`/`threshold`/
  `reliefSplit` before the `/* ---------------- svg helpers */` marker, and `<meta charset="utf-8">`
  the FIRST line. UI (`renderS`, fieldsets, `readS`) lives after it; `readS` is the single reader
  feeding both tabs.
- The relief is a horizontal PIPE ⇒ minor + friction losses in `Krel` (the bend is a minor loss);
  the FALL is a vertical leader ⇒ IPC `leader()`, never Manning. Don't blur them.
- Provenance tags `class="tag t-known"` / `class="tag t-assume"` only (a bend count/geometry the user
  isn't sure of is `t-assume`). Any new control goes in tab ②'s "Outlet — fall & relief" fieldset.
- Honesty: adding bend loss makes the relief HELP LESS (more conservative) — never more. Relief still
  can't help an UPSTREAM-caused far-end flood; CAN help a BACKUP-caused one.
- Extract, don't duplicate; test the property where it's first-order (relief-Ø/Lrel monotonicity is
  tested under a BLOCKED outlet — do the same for any bend-loss monotonicity guard).

**Finish:** merge to `main`, push, and republish `sim/index.html` to the SAME artifact URL
`https://claude.ai/code/artifact/bffe0f46-2342-40d6-a44c-dfef82d8f9f9` (favicon `🌧️`) via the
Artifact tool's `url=` param — a fresh conversation otherwise mints a new URL. Repo:
`git@github.com:jmmas123/plumbing-sim.git`, main at `b2cd310`.
