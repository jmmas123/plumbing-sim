# STATE — Bodega Triple stormwater sim
_Updated 2026-07-18._

## Current position
- Steady-state sim of ONE aerial collector: 3 tabs (Runoff ①, Section ②, Relief ③).
  `sim/index.html` (self-contained, file://) + `sim/verify.mjs`. Artifact:
  https://claude.ai/code/artifact/bffe0f46-2342-40d6-a44c-dfef82d8f9f9
- SHIPPED: Y-T momentum-split tab ③ (`7822919`) + outlet–relief coupling tab ② (merged main
  `4bc93b8`, pushed, republished). Tab ② makes the outlet a real bottleneck: overloaded → backs
  up → lifts the HGL, with a relief on/off toggle. Fixed two latent bugs: `fallCap` uses the FALL
  Ø (not collector Ø); `qDeliverMax` gradient no longer double-counts slope.
- SHIPPED: relief now has its own diameter (`dRelief`, default 8″ as-built), independent of
  the collector — a 10″ re-pipe keeps the honest 8″ relief; dial up via tab-②'s "Relief diameter".

## System, as measured on site
- Roof 8,343 m² (123.6 × 67.5 m, 3 gables), plan area (pitch does NOT change Q).
- Each 8″ collector serves ONE roof slope ≈ 1,390 m²; 6 collectors. Valley: double canaleta
  (50×17) → 2 pipes, 9 boca tubos each. Collector 8″ PVC, ~0.9% grade, 63 m.
- Boca tubos 9/collector, 6″, 45° wye. Canaleta single 40×14 / double 50×17 (level).
- Buffer crown→canaleta floor: 0.93 m far end, ~1.65 m outlet. Hangers 0.87 m → sag negligible.
- Outlet open/free, no tailwater. Y-T relief daylights on rear platform.

## Key results
- Pipe cap ~38–40 L/s (8″@0.9%). Surcharges >~104 mm/h; FLOODS >~307 mm/h (as-measured) ≈ 2.6×
  the 2-yr storm ⇒ competently built. Observed far-end failure reproduced (level canaleta + friction).
- Worst 24 h = 82.5 mm ≈ 2-yr day; no sub-daily gauge within 17 km.

## Open leads
1. INSPECT pipe interiors for silt/blockage — cheapest "worked for years then failed" explanation.
2. SWMM build for timing/storage (design storms per return period). Refs in `refs/`.
3. Optional tab-② refinement: bend loss in Krel (M3).

## Conventions
- Self-contained `sim/index.html`; `<meta charset="utf-8">` FIRST line; `node sim/verify.mjs` green
  after ANY edit (it extracts the solver — keep solver code before the `/* svg helpers */` marker).
- Vertical leaders = IPC orifice rating, NEVER Manning; the RELIEF is horizontal ⇒ pipe losses apply.
- Provenance tags `class="tag t-known"` / `class="tag t-assume"` (no `measured`/`assumed` modifier).
- Honesty: relief can't help an UPSTREAM-caused far-end flood; CAN help a BACKUP-caused one.
- Git: origin `github.com/jmmas123/plumbing-sim`, main at `3cfbfa3` (pushed). Branch before implementing;
  merge/push + republish (Artifact `url=` the URL above, favicon 🌧️) at the end.
