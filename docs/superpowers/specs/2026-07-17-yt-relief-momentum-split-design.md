# Design spec — Y-T emergency relief, momentum-aware flow split

_Date: 2026-07-17 · Status: approach approved, pending spec review._

## 1. Purpose

The Bodega Triple collector ends at a **Y-T**: the straight-through run is left open (the
**relief**, daylighting on the rear concrete platform) and the branch turns **90° down** the
vertical fall to the ditch outlet (the **normal path**). The existing steady model
(`sim/index.html`) splits flow at this junction by **head only**, and therefore predicts the
relief stays permanently dry — because the gravity-fed fall out-swallows everything the
collector can deliver (`qDeliverMax ≈ 67–71 L/s` < `leader(8) = 76 L/s`).

That head-only view structurally cannot see the effect the user asked about: with the fall on a
90° branch and the relief on the low-loss straight-through, incoming **horizontal momentum**
favors the relief. This spec defines a physically-based split that answers, as a function of
storm intensity and junction geometry, **what fraction of `Q_in` exits straight out the relief
vs. turns down the fall** — across both regimes the user identified — and folds it into the sim.

## 2. Confirmed inputs and standing constraints

- **Fitting: 90° tee** — branch = fall (turns down), run = relief (straight through). Confirmed
  by the user 2026-07-16. Naming is "Y-T", so the model must also sweep a 45° wye as the
  sensitivity floor.
- Collector: 8″ PVC, ~0.9% grade, 63 m, 9 boca tubos. Flow reaching the junction
  `Q_in = min(Qtot, qDeliverMax)` (the collector pipe cannot convey more than `qDeliverMax`
  to the junction; the excess backs up and spills at the far boca tubos — the observed flood).
- Fall: 8″ vertical leader, `leader(8) = 76.18 L/s`; 10″ is the user's pondered upgrade
  (`leader(10) = 141.4 L/s`), so `d_fall` is a parameter.
- Relief open end `z_back`: a horizontal continuation, so ≈ pipe level at the junction
  (low elevation barrier). Sweepable — a deliberately raised opening would suppress relief flow.
- Outlet: free discharge, above floor, no tailwater. A **blocked/drowned outlet** is the
  Scenario-1 extreme (`Q_fall,max → 0`).

### CRITICAL caveat (must not be over-claimed by the analysis)

The Y-T sits at the outlet end, **downstream** of the entire collector. The observed flooding is
at the **far** boca tubos (rows 6–8), **upstream**. Water must traverse all 63 m to even reach
the junction. Therefore the relief **cannot** relieve the far-end flooding. It helps only when the
binding constraint is at or after the junction (a blocked/drowned outlet), or by acting as a
**vent** for air trapped in a surcharged line. The deliverable text must state this plainly.

## 3. Physics — corrected geometry ranking

The relief is the straight-through (0° turn, low loss) in **both** fitting options. What differs is
the **branch** (fall) turn:

| Fitting | Branch turn | Momentum overshoot to relief | Relief share |
|---|---|---|---|
| 90° tee (as-built) | 90° — violently resists incoming momentum | large | **more** |
| 45° wye (floor) | 45° — flow follows into branch easily | small | **less** |

This corrects a backwards consequence-label used while eliciting the fitting: 90° tee → **more**
relief, 45° wye → **less**. The 90° as-built case is where the head-only model discards the most.

## 4. Model — two mechanisms

Reported at the junction: `{ q_in, q_straight, q_fall, relief_frac = q_straight/q_in, mechanism }`
with `q_straight + q_fall = q_in` (mass conservation) and `0 ≤ relief_frac ≤ 1`.

### Mechanism 1 — head-limited overflow (Scenario 1, dominant)

Once the junction surcharges to the relief-opening level, any flow the fall cannot swallow spills
straight:

```
q_fall_max_eff = min( leader(d_fall), head_limited_take(H_j = z_back) )
q_straight_head = max(0, q_in − q_fall_max_eff)
```

For the as-built (clear 8″ fall), the annular-film leader cap (76 L/s) binds before any head cap,
and `q_in ≤ qDeliverMax ≈ 70 L/s`, so `q_straight_head = 0` — this **reproduces the current
model's dry relief**, preserving continuity with the shipped tool. For a blocked outlet,
`q_fall_max_eff → 0` and `q_straight_head → q_in` (full relief). This mechanism is the
"sink overflow" and is the relief's real job.

### Mechanism 2 — momentum pass-through (Scenario 2, the new physics)

A steady **energy** split at this junction gives ≈ 0 straight flow (the fall, with metres of
elevation drop, is head-favored and greedily fills to its leader cap). The straight overshoot is
therefore a genuinely **inertial** effect that the steady energy balance omits. It is modeled with
a **horizontal-momentum control volume** at the junction and a turning coefficient keyed to branch
angle:

```
q_straight_mom = phi_mom(V_in, angle) · q_in
```

with `phi_mom → 0` as `V_in → 0`, growing with `V_in²`, and `phi_mom(90°) > phi_mom(45°)`.
`V_in = q_in / A_pipe` at full bore. This term matters most in a high-velocity surcharged burst.

### Combining (no double-counting)

The mechanisms compose in sequence, not by addition. Head-limited overflow spills first; momentum
then skims a fraction of only the flow that head-logic still sends **down**:

```
q_down_candidate = q_in − q_straight_head        # what head-logic routes to the fall
q_straight       = q_straight_head + phi_mom · q_down_candidate
q_fall           = q_in − q_straight
```

This reduces correctly at both limits: unchoked fall (`q_straight_head = 0`) → `q_straight =
phi_mom · q_in` (pure momentum); fully blocked (`q_straight_head = q_in`) → `q_straight = q_in`
(pure overflow). `mechanism ∈ {dry, head, momentum, both}` is reported so the UI can show *why*
the relief is (or isn't) engaged.

### Coefficient sourcing — Phase 0, DO NOT INVENT

`K_branch`, `K_straight`, and the momentum turning coefficient are **not** to be guessed. They must
be sourced in the implementation plan's Phase 0 from:
- Idelchik, *Handbook of Hydraulic Resistance* — dividing tee/wye K as f(area ratio, branch angle,
  `Q_branch/Q_main`).
- Miller, *Internal Flow Systems* — tee/junction loss data.
- A control-volume momentum derivation as an independent cross-check (methods must agree within
  the K-factor uncertainty band).

The spec commits to the **structure**; the plan pins the **numbers** with citations.

## 5. Sensitivity axes (the deliverable's spine)

1. **Fitting angle** 45° ↔ 90° — the single biggest lever; reported as a band, not a line.
2. **Back-end elevation** `z_back` — sets the Scenario-1 head threshold.
3. **Fall capacity** — 8″ vs 10″, and the **blocked-outlet** extreme (Scenario-1 upper bound).

## 6. Deliverables

- A pure `reliefSplit(q_in, geom)` core function returning the split object above.
- A **`Q_straight/Q_in` vs storm-intensity** curve (intensity → `q_in` via the existing rational
  chain), spanning both regimes, for the as-built geometry, with the 45°↔90° band.
- The **intensity at which the relief starts carrying meaningful flow** (threshold, e.g. > 5% of
  `q_in`).
- A new **"Relief" tab**: the curve plus a live junction-split diagram at the current slider
  settings, showing which mechanism is active.

## 7. Integration and testing

- **Supersede** the boolean `ytActive` with the continuous split. Keep the head-only value as a
  labeled reference (`ytActiveHead`) so the existing `verify.mjs` invariants ("collector cannot
  out-push the fall", "Y-T stays dry at as-built under head-only") remain meaningful and green.
- **New invariants** for `verify.mjs`: `relief_frac(90°) > relief_frac(45°)` at equal flow;
  blocked outlet ⇒ `relief_frac → 1`; `phi_mom → 0` as `V_in → 0`; `0 ≤ relief_frac ≤ 1`;
  `q_straight + q_fall = q_in`.
- Preserve in-UI provenance tags: K-factors `assumed` / `from literature`; geometry `measured`.
- Keep `<meta charset="utf-8">` as the first line. Run `node sim/verify.mjs` green after **every**
  edit (it extracts and tests the shipped solver).
- Downspouts/leaders stay orifice/IPC-rated, never Manning.

## 8. Out of scope (YAGNI)

- Feeding the split into a SWMM model — a later slice; note the momentum term is exactly what SWMM
  would otherwise miss.
- CFD — mention as a single-geometry validation option only; do not build.
- Time-varying storms — the tool is steady-state; keep it steady.
