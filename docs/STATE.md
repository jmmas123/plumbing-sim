# STATE — Bodega Triple stormwater sim

_Updated 2026-07-17._

## Current position
- Steady-state hydraulic sim of ONE aerial collector is built, fully measured, and
  test-backed. Files: `sim/index.html` (self-contained, opens via file://), `sim/verify.mjs`.
- Published artifact: https://claude.ai/code/artifact/bffe0f46-2342-40d6-a44c-dfef82d8f9f9
- Next task: analyze the Y-T emergency relief flow split — see
  `docs/YT-OVERFLOW-ANALYSIS-BRIEF.md`. To be done in a fresh context.

## System, as measured on site
- Roof 8,343 m² (123.6 × 67.5 m, 3 gables), plan area (pitch does NOT change Q).
- Each 8″ aerial collector serves ONE roof slope ≈ 1,390 m²; 6 collectors total.
  Valleys: one double canaleta (50×17 cm) → 2 pipes, 9 boca tubos each.
- Collector: 8″ PVC, gradient ~0.85–0.90% (measured drop 0.57 m / 63 m), run 63 m.
- Boca tubos: 9 per collector, 6″, 45° wye entry. Canaleta single 40×14, double 50×17 (level).
- Buffer (crown→canaleta floor): 0.93 m far end, ~1.65 m outlet (measured; model derives
  1.70, cross-check Δ 5 cm).
- Hangers 0.87 m spacing → sag negligible (0.04 mm). Good install.
- Outlet: open, free, above floor, no tailwater. Y-T relief daylights on rear platform.

## Key results
- Pipe capacity ~38–40 L/s (8″ @0.9%). Surcharges >~104 mm/h; FLOODS >~307 mm/h (as-measured).
- Flood point ≈ 2.6× the 2-year storm ⇒ system is competently built, NOT chronically undersized.
- Observed failure (far boca tubos, rows 6–8) reproduced qualitatively (level canaleta + friction).
- Rain was NOT clearly exceptional: worst 24 h = 82.5 mm ≈ 2-yr day; wetter by VOLUME (+17%).
  No sub-daily gauge within 17 km ⇒ 5-min burst intensity unknowable from data.

## Open leads (in priority order)
1. INSPECT pipe interiors for silt/blockage — cheapest explanation for "worked for years,
   then failed"; 30 mm silt drops flood threshold to ~225 mm/h.
2. Y-T relief flow-split analysis (fresh context — brief written).
3. SWMM build for timing/storage (design storms per return period). Refs in `refs/`.

## Conventions
- `sim/index.html` is self-contained on purpose (ES modules don't load over file://).
  Has `<meta charset="utf-8">` at top — required for local file://; harmless when published.
- `node sim/verify.mjs` extracts the solver from the shipped HTML and checks it (21 checks).
  Run it after ANY edit to the sim. Keep it green.
- Downspouts/leaders are rated by IPC code (orifice), NEVER Manning (6–8× error).
- Numbers tagged in-UI as `from CAD` / `measured` / `assumed` — preserve that honesty.

## Blockers
- No git remote configured — commit is local only; push pending a remote (ask user / `gh repo create`).
- No local IDF curves within 17 km; sub-daily rainfall restricted (DGOA-MARN request is the path).
