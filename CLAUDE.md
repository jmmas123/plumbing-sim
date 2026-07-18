# Bodega Triple — stormwater simulation

Numerically evaluate the roof-drainage capacity of a three-gable warehouse in San Andrés,
Ciudad Arce, El Salvador (MEROPIS S.A.), which overflowed during recent wet seasons, and
quantify remediation measures (10″ re-pipe, a Y-T emergency relief).

## Orientation
- Read `docs/STATE.md` first every session.
- `sim/index.html` — the working steady-state model (2 tabs: runoff, and collector section).
  Self-contained, opens via `file://`. `sim/verify.mjs` is its test harness.
- `refs/` — verified SWMM API reference and El Salvador rainfall research.
- `analysis/` — the standalone first-principles Python calcs behind the model.
- Source CAD: two `.dwg` files (AC1027). Read via `libredwg` JSON path, NOT `dwg2dxf`
  (which silently truncates the hydraulic file before the ENTITIES section).

## Domain facts established (don't re-derive)
- Units in the DWG are metres despite `$INSUNITS=1`. Roof 8,343 m² (dimensioned CAD text).
- Each 8″ collector ≈ 1,390 m² of roof; ~0.9% grade; 63 m; 9× 6″ boca tubos (45° wye entry);
  level canaleta (single 40×14, double 50×17 cm); ~0.93 m buffer to the canaleta lip.
- Rain falls vertically ⇒ **roof PITCH does not change Q** (catch = horizontal projection).
  Pitch changes only timing (time of concentration), a ~few-% effect on peak Q.
- No IDF curves within 17 km; sub-daily rainfall restricted. Observed worst day ≈ 2-yr event.

## Modelling rules (violating these produces confidently-wrong results)
- **Vertical leaders/downspouts = orifice at the IPC code rating, NEVER Manning** (Manning
  overstates a vertical leader 6–8× — it assumes full-bore, real leaders run as an annular film).
- **Surcharge ≠ flood.** A full pipe pressurises and water climbs the boca tubos; flooding is
  only when it tops the canaleta. Track both thresholds separately.
- In SWMM, read **`Flooding Loss`** (Flow Routing Continuity), not `Total Flood Volume`.
  Use `DYNWAVE` routing for surcharge/reverse flow. `ALLOW_PONDING` with area 0 is a no-op.
- The Y-T relief is DOWNSTREAM of the collector; it cannot relieve far-end (rows 6–8) flooding.

## Working conventions
- After ANY edit to `sim/index.html`, run `node sim/verify.mjs` and keep all checks green.
  It extracts the solver from the shipped HTML, so it tests what actually runs.
- Keep `<meta charset="utf-8">` as the first line of `sim/index.html` (needed for file://).
- The sim stays self-contained (ES modules don't load over file://).
- Preserve the in-UI provenance tags: `from CAD` / `measured` / `assumed`.
- Follow the user's global workflow: plan skill before builds; verify before claiming done.

## Python
- `uv run --quiet --with ezdxf python script.py`. Never name a script `inspect.py` (shadows stdlib).
