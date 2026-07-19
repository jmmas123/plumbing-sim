# Next-session init prompt — paste into the fresh window

The **relief-model refinement track is COMPLETE.** No coding slice is queued. This session should
start by reading state and deciding direction **with the user** — do not start building anything
before that.

Read first, in order:
1. `docs/STATE.md` — where the project stands (Open leads are now just inspection + SWMM).
2. `CLAUDE.md` — project rules and domain facts (don't re-derive).
3. Only if the chosen direction touches the relief/section model: the specs in
   `docs/superpowers/specs/` (coupling, relief-diameter) and `.superpowers/sdd/progress.md`.

**What just shipped (do not redo):** the steady-state one-collector model is fully built and the
relief refinements are all closed —
- Y-T momentum-split tab ③ (`7822919`);
- outlet–relief coupling tab ② (`4bc93b8`) — outlet is a real bottleneck (overloaded → backs up →
  lifts the HGL), with a relief on/off toggle;
- relief has its own diameter `dRelief`, default 8″, independent of the collector (`3cfbfa3`);
- **M3 bend loss — closed as verified-N/A (`9f43961`):** the user confirmed the relief run is
  **straight** from the Y-T to daylight (no bends), so `Krel` (exit + entrance + friction) is already
  complete — there was no bend term to add. Recorded in relief-diameter spec §6 + a tab-② note.
The artifact is republished and current. Harness: `node sim/verify.mjs` → 60/60, ALL CHECKS PASS.

**There is no pending relief/section work.** If the user wants to model a *re-routed* relief (a bend),
that is a new brainstorm — add `+ Kb·nBends` to `Krel` (Kb ≈ 0.6 per standard 90° elbow) + a
blocked-outlet monotonicity guard; but the as-built run is straight, so this is speculative until asked.

**The genuine next leads (STATE Open leads — pick WITH the user, brainstorm before building):**
1. **SWMM build for timing/storage** — the big one. Steady-state can't see storage/attenuation or
   design storms per return period; SWMM can. Refs are in `refs/` (verified SWMM API + El Salvador
   rainfall research). This is a NEW subsystem → **START WITH `superpowers:brainstorming`** (hard gate),
   then decompose (it is large — likely its own spec/plan, separate from `sim/index.html`).
2. **Physical pipe-interior inspection** for silt/blockage — the cheapest "worked for years then
   failed" explanation. Not a coding task; if the user reports findings, fold them into the model.

**Load-bearing conventions (apply to any build):**
- Doc-only changes commit directly to `main` (repo practice: `b2cd310`, `785540b`, `9f43961`). Solver/
  feature changes: **branch first** (e.g. `feat/…`), then merge/push.
- After ANY edit to `sim/index.html` run `node sim/verify.mjs` green — it extracts the solver, so keep
  `solveCollector`/`threshold`/`reliefSplit` before the `/* svg helpers */` marker, and
  `<meta charset="utf-8">` the FIRST line. UI (`renderS`, fieldsets, `readS`) lives after it; `readS`
  is the single reader feeding both tabs.
- Vertical leaders = IPC orifice rating, NEVER Manning; the RELIEF is horizontal ⇒ pipe losses apply.
- Provenance tags `class="tag t-known"` / `class="tag t-assume"` only.
- Honesty invariant: the relief can't help an UPSTREAM-caused far-end flood; it CAN help a
  BACKUP-caused one. Never weaken the C1 direction or the blocked-outlet monotonicity guards.
- Republish `sim/index.html` to the SAME artifact URL
  `https://claude.ai/code/artifact/bffe0f46-2342-40d6-a44c-dfef82d8f9f9` (favicon `🌧️`) via the
  Artifact tool's `url=` param at the end of any change that touches the HTML.

Repo: `git@github.com:jmmas123/plumbing-sim.git`, main at `9f43961`.
