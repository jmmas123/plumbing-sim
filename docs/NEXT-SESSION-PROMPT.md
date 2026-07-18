# Next-session init prompt — paste into the fresh window

We're adding a **RELIEF-DIAMETER input** to the Bodega Triple stormwater sim (tab ②) — the top
deferred follow-up (adversarial finding **M2**) from the just-shipped outlet–relief coupling.

Read first, in order:
1. `docs/STATE.md` — where the project stands (Open leads #3 is this follow-up).
2. `docs/superpowers/specs/2026-07-18-outlet-relief-coupling-design.md` — §3.2 (relief as a pipe),
   §3.5 (the `dRelief = d` assumption row, tagged), §3.6 **M2**, and §5 (the invariant already
   worded "larger `dRelief` … raises the flood threshold" — it currently exercises `Lrel`, not Ø).
3. `.superpowers/sdd/progress.md` — the FINISHED ledger for the coupling, incl. the M2/M3 rationale.
4. `CLAUDE.md` — project rules.

**What just shipped (do not redo):** the outlet–relief coupling on tab ② — the outlet is a real
fall+relief bottleneck that backs up and lifts the HGL, with a relief on/off toggle and an `Lrel`
slider (merged to `main` at `4bc93b8`, pushed; STATE at `7417b2b`; republished to the artifact URL
below). The adversarial physics review returned SHIP.

**The problem to solve:** tab ②'s relief area is `Arel = π/4·(p.d·IN)²` — it ties the relief's
diameter to the COLLECTOR. So a 10″ re-pipe silently models a 10″ relief run. If the real
daylighting run stays 8″, the tool overstates the relief's help by ~(10/8)²≈1.56×. The C1
DIRECTION (relief helps the 10″ case) is robust; only the MAGNITUDE is sensitive. Goal: let the
relief diameter be set independently, so the user can run "10″ collector, 8″ relief."

**START WITH BRAINSTORMING** (`superpowers:brainstorming` — it's a HARD GATE before any plan/code;
this is a modeling decision, not a mechanical edit). Design questions to resolve with the user:
- Default for `dRelief`: keep `= collector Ø` (backward-compatible, current behavior) or default to a
  fixed 8″ (the as-built straight run)? Which is the honest default?
- Provenance tag: the as-built relief IS the collector's measured 8″ straight run (`t-known`); but a
  re-pipe hypothetical relief Ø is `t-assume`. How should the tag reflect the active case?
- Does re-piping the collector physically re-pipe the straight-through relief run too, or not? (This
  is the user's call about the remediation — ask them.)
- Reconcile with tab ③: `reliefSplit(qIn, p)` already parameterizes a through-pipe diameter
  (`p.dPipe`) and `p.dFall` separately from the collector. Reuse that `dPipe` concept for tab ②'s
  relief Ø (one source of truth) or keep them separate? Check this before designing.
- Bundle **M3** (add a bend loss to `Krel`, ~10–15% capacity) into the same slice, or keep separate?

Then `superpowers:writing-plans` → `superpowers:subagent-driven-development` (fresh implementer per
task, per-task spec+quality review, opus final whole-branch review). Physics-adjacent — re-run an
adversarial physics check if the head-balance math changes.

**Load-bearing conventions:**
- **Branch before implementing** (e.g. `feat/relief-diameter-input`). After ANY edit to
  `sim/index.html` run `node sim/verify.mjs` green — it extracts the solver from the shipped HTML, so
  keep all `solveCollector`/`threshold`/`reliefSplit` code before the `/* ---------------- svg helpers */`
  marker, and keep `<meta charset="utf-8">` the FIRST line. UI (`renderS`, fieldsets) lives AFTER it.
- The relief is HORIZONTAL ⇒ pipe losses apply (`Krel = 1 + Ke + f·L/D`); the FALL is a vertical
  leader ⇒ IPC `leader()` rating, never Manning. Don't blur the two.
- Provenance tags are `class="tag t-known"` / `class="tag t-assume"` only (no `measured`/`assumed`
  modifier class). Put the relief-Ø control in tab ②'s "Outlet — fall & relief" fieldset (next to `Lrel`).
- Honesty: relief can't help an UPSTREAM-caused far-end flood; CAN help a BACKUP-caused one — this
  must survive. Add/extend an invariant: SMALLER relief Ø ⇒ LESS relief help (lower flood threshold);
  keep the C1 guard ("10″ re-pipe, relief HELPS under a clear outlet") green.
- Extract, don't duplicate: if tab ② and tab ③ both need a relief-Ø-area, make it one shared helper.

**Finish:** merge to `main`, push, and republish `sim/index.html` to the SAME artifact URL
`https://claude.ai/code/artifact/bffe0f46-2342-40d6-a44c-dfef82d8f9f9` (favicon `🌧️`) via the
Artifact tool's `url=` param — a fresh conversation otherwise mints a new URL. Repo:
`git@github.com:jmmas123/plumbing-sim.git`, main at `7417b2b`.
