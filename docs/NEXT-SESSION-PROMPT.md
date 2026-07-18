# Next-session init prompt — paste into the fresh window

We are analyzing the **Y-T emergency relief pipe** on the Bodega Triple stormwater system.
Before anything else, read, in order:
1. `docs/STATE.md` — where the project stands and the measured system.
2. `docs/YT-OVERFLOW-ANALYSIS-BRIEF.md` — the full task, physics framework, methods, and the
   critical caveats. THIS is your spec.
3. `sim/index.html` — the existing steady-state model (self-contained). Its solver already
   encodes a conservative, head-only version of the Y-T ("stays dry"); your job is the
   momentum correction to that.
4. Skim `refs/SWMM_API_REFERENCE.md` only if you get to the SWMM-feeding step.

## What just shipped (this session)
- A fully-measured, validated single-collector steady sim (`sim/index.html` + `sim/verify.mjs`,
  21 checks green). Every parameter is from CAD or field measurement; geometry cross-checks
  to 5 cm. Published at https://claude.ai/code/artifact/bffe0f46-2342-40d6-a44c-dfef82d8f9f9.
- Diagnosis: the system floods at ~2.6× the 2-year storm ⇒ competently built, not chronically
  undersized. Most likely real-world culprit for "failed this year": silt/blockage (inspect).

## Your task
Compute what fraction of `Q_in` exits STRAIGHT out the open back end of the Y-T vs. turning 90°
down the fall, across both regimes: (1) blocked/over-capacity outlet [head-driven], and (2)
full-capacity momentum pass-through [momentum-driven, ∝ V²]. Deliver a `Q_straight/Q_in` curve
vs. intensity, sensitivity to fitting geometry (90° tee vs 45° wye — the biggest lever), and
fold a physically-based relief-junction split into the sim as a new element/tab.

## Recommended first move
Invoke `superpowers:brainstorming` (or `claude-mem:make-plan`) to scope the analysis BEFORE
coding — per the user's workflow rules, creative/build work starts with a plan skill. Then
build incrementally and keep `node sim/verify.mjs` green.

## Load-bearing conventions (do NOT rediscover)
- `sim/index.html` is self-contained deliberately (ES modules fail over file://); keep the
  `<meta charset="utf-8">` first line.
- After ANY edit to the sim, run `node sim/verify.mjs` — it tests the SHIPPED solver, not a copy.
- Republish the SAME artifact: pass `url:` = the URL above (a new conversation otherwise mints
  a new URL). Same `file_path` from THIS conversation would redeploy; from a fresh one use `url`.
- Downspouts/vertical leaders = orifice/IPC rating, never Manning (6–8× error). Read `Flooding
  Loss`, not `Total Flood Volume`, if/when SWMM is involved.
- Preserve the in-UI honesty tags (`from CAD` / `measured` / `assumed`).
- The Y-T is DOWNSTREAM of the collector, so it cannot relieve the far-end (rows 6–8) flooding;
  it helps only for a blocked outlet or as an air vent. Do not let the analysis over-claim this.

## Git
- Repo initialized this session; committed locally. NO REMOTE yet — ask the user for one (or
  `gh repo create`) before attempting to push. Branch: main.
