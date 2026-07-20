# STATE — Bodega Triple stormwater sim
_Updated 2026-07-20._

## Current position
- Steady-state sim of ONE aerial collector: 3 tabs (Runoff ①, Section ②, Relief ③).
  `sim/index.html` (self-contained, file://) + `sim/verify.mjs`. Artifact:
  https://claude.ai/code/artifact/bffe0f46-2342-40d6-a44c-dfef82d8f9f9
- SHIPPED: Y-T momentum-split tab ③ (`7822919`); outlet–relief coupling tab ② (`4bc93b8`) — outlet is
  a real bottleneck (overloaded → backs up → lifts HGL) + relief on/off; relief has its own diameter
  `dRelief` (default 8″, independent of the collector, `3cfbfa3`).
- VERIFIED N/A: M3 bend loss in `Krel` — relief run straight to daylight; `Krel` complete (spec §6).
- SHIPPED (`3449d17`, labels only, solver verified bit-identical): tabs ② and ③ now state that they
  answer different questions — ③ = momentum ROUTING split at the tee (~14% at 65 L/s, h=0.30),
  ② = SURPLUS the fall can't swallow (0 under a clear outlet). ② excludes ③'s diversion because `h`
  is assumed (moves the fraction ~40%→0); proved over 1,920 configs that `qOver ≤ qStraight` always,
  so ② can only understate the relief. User: "do the labels, dont change the physics".

## System, as measured on site  (full list in CLAUDE.md — not repeated here)
- Buffer crown→canaleta floor: 0.93 m far end, ~1.65 m outlet. Hangers 0.87 m → sag negligible.
- Outlet confirmed open/free by the user (2026-07-20), no tailwater. Y-T relief daylights on rear
  platform; its drop below the tee (= branch head `h`) is still unmeasured.

## Key results
- Pipe cap ~38–40 L/s (8″@0.9%). Surcharges >~104 mm/h; FLOODS >~307 mm/h (as-measured) ≈ 2.6×
  the 2-yr storm ⇒ competently built. Observed far-end failure reproduced (level canaleta + friction).
- Worst 24 h = 82.5 mm ≈ 2-yr day; no sub-daily gauge within 17 km.

## Open leads
1. MEASURE branch head `h` — the drop from the Y-T down to where the relief daylights. Only assumed
   input left in the relief model; collapses the ~40%→0 spread in tab ③'s split.
2. INSPECT pipe interiors for silt/blockage — cheapest "worked for years then failed" explanation.
3. SWMM build for timing/storage (design storms per return period). Refs in `refs/`.

## Conventions
- Self-contained `sim/index.html`; `<meta charset="utf-8">` FIRST line; `node sim/verify.mjs` green
  after ANY edit (it extracts the solver — keep solver code before the `/* svg helpers */` marker).
- Vertical leaders = IPC orifice rating, NEVER Manning; the RELIEF is horizontal ⇒ pipe losses apply.
- Provenance tags `class="tag t-known"` / `class="tag t-assume"` (no `measured`/`assumed` modifier).
- Honesty: relief can't help an UPSTREAM-caused far-end flood; CAN help a BACKUP-caused one.
- Git: origin `github.com/jmmas123/plumbing-sim`, main at `3449d17` (pushed). Branch before implementing;
  merge/push + republish (Artifact `url=` the URL above, favicon 🌧️) at the end.
