# Next-session init prompt — paste into the fresh window

We're implementing the **OUTLET–RELIEF COUPLING** for the Bodega Triple stormwater sim.

Read first, in order:
1. `docs/STATE.md` — where the project stands.
2. `docs/superpowers/plans/2026-07-18-outlet-relief-coupling.md` — **THE PLAN you execute** (4 TDD tasks).
3. `docs/superpowers/specs/2026-07-18-outlet-relief-coupling-design.md` — the physics behind it (esp. §3 model, §6 the two corrections, §3.6 limitations).
4. `CLAUDE.md` — project rules.

**What just shipped:** the Y-T relief momentum-split tab ③ (merged to main `7822919`, pushed, republished). This feature couples that relief + the fall into the **Section tab ②** as a real outlet bottleneck: when arriving flow exceeds fall + relief capacity, the outlet backs up and lifts the whole HGL; toggle the relief to watch it hold the backup down.

**Execute the plan subagent-driven** (`superpowers:subagent-driven-development`): fresh implementer per task, per-task spec+quality review gate, opus final whole-branch review. This is **physics-critical** — after Task 2 (the outlet head balance) re-run an **adversarial physics check on the IMPLEMENTED boundary** before merge. Do **NOT** weaken the C1 guard test (`"10\" re-pipe … relief HELPS under a clear outlet"`); a failure there means the coupling is wrong, not the test.

**Load-bearing conventions:**
- **Branch before implementing** (e.g. `feat/outlet-relief-coupling`). After ANY edit to `sim/index.html` run `node sim/verify.mjs` and keep it green — it extracts the solver from the shipped HTML, so keep all `solveCollector` code before the `/* ---------------- svg helpers */` marker, and keep `<meta charset="utf-8">` the first line.
- Vertical leaders = IPC orifice rating, **never Manning** — but the **relief is horizontal**, so pipe losses (entrance + friction + exit) DO apply to it.
- Provenance tags are `class="tag t-known"` (measured/CAD) / `class="tag t-assume"` (assumed) — there is no `measured`/`assumed` modifier class.
- **Honesty (must survive in the UI copy):** the relief cannot help far-end flooding caused **upstream** (the as-built observed flood), but **can** when the far-end flood is caused by **outlet backup** (blocked outlet, or the 10″ re-pipe). The 10″-re-pipe benefit must **not** be suppressed — it connects the user's two remediations.
- **Task 1 bundles two pre-existing bug fixes** (fall cap by fall diameter; delivery-gradient de-double-count) that shift some published numbers — the user approved this. Watch that the tab-③ "violent storm wakes the relief" test doesn't flip on the lower `qDeliverMax`; raise its intensity if needed (noted in the plan).

**Finish:** merge to main, push, and republish `sim/index.html` to the SAME artifact URL
`https://claude.ai/code/artifact/bffe0f46-2342-40d6-a44c-dfef82d8f9f9` (favicon `🌧️`) via the Artifact tool's `url=` param — a fresh conversation otherwise mints a new URL. Repo: `git@github.com:jmmas123/plumbing-sim.git`, main at `1224d96`.
