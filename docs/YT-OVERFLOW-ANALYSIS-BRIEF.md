# Analysis brief — the Y-T emergency relief flow split

**Task for the fresh session.** Determine what fraction of the incoming flow `Q_in`
leaves *straight out the open back end* of the Y-T (the relief) versus being turned
*90° down into the fall* toward the outlet — as a function of flow rate, junction
geometry, and downstream conditions. This is a **dividing-flow junction** problem, and
the interesting part is that it is governed by **momentum**, not head alone.

---

## What the Y-T is (geometry — CONFIRM before modelling)

The original system was: horizontal 8″ collector → **90° elbow** → vertical fall → outlet.
The modification replaced that top elbow with a **Y-T** whose:

- **straight-through run** continues horizontally and is **left open**, daylighting on a
  concrete platform at the back wall — this is the *relief*;
- **branch leg** turns down into the vertical fall to the ditch outlet — this is the
  *normal path*.

The site photo (see conversation) shows the boca-tubo connections are **45° wyes**, not
90° tees. **The single biggest lever on the answer is whether the down-turn is a true 90°
tee take-off or a 45° wye + elbow.** A wye makes the straight path the low-resistance path
(more goes straight); a 90° tee resists the straight→branch turn (less). *Confirm the
actual fitting on site before trusting any number.*

Open questions to pin down (all affect the split materially):
1. Fitting type and branch angle (90° tee vs 45° wye).
2. Diameter of each leg — collector is 8″; is the relief run 8″ and the fall 8″→10″?
3. Elevation of the open back end relative to the collector invert (sets the relief's
   discharge head).
4. Is the open end truly free-discharging, or does it hit the platform / pond?

---

## Why momentum matters (the crux the user identified)

Two independent driving mechanisms, and the user correctly separated them into two scenarios:

**Scenario 1 — backup / over-capacity (head-driven).**
If the outlet is blocked, or `Q_in` exceeds what the fall+outlet can pass, head builds at
the junction and the relief discharges by the head difference. `Q_straight = Q_in − Q_fall,max`.
This is the "sink overflow" mode and is the *dominant* relief mechanism. Straightforward
once `Q_fall,max` and the back-end discharge elevation are known.

**Scenario 2 — full capacity, momentum pass-through (momentum-driven).**
Even when the fall is NOT backed up, the incoming horizontal flow carries momentum aimed
straight at the open end. The 90° down-turn requires a force (pressure gradient + wall
reaction) to redirect that momentum. With part of the outer wall now *open*, a fraction of
the flow continues straight and exits — nothing forces it down. This fraction is small at
low velocity and grows with velocity.

### The governing balance (1-D control volume at the junction)

- **Mass:** `Q_in = Q_straight + Q_fall`
- **Energy (each branch, with a dividing-flow loss K):**
  `H_junction = z_back + (1+K_s)·V_s²/2g`  (straight, free discharge at z_back)
  `H_junction = z_out + h_L,fall + K_b·V_b²/2g`  (down, large elevation drop z_out ≪ z_back)
- **Streamwise momentum (horizontal):** incoming `ρ Q_in V_in` is split; the down leg
  carries away little horizontal momentum, so the horizontal balance is what "wants" to
  keep flow going straight.

**Scale estimate to anchor intuition:** at the design velocity V ≈ 1.25 m/s, velocity head
V²/2g ≈ **0.08 m**. The fall provides *metres* of elevation drop. So in normal, at-capacity
flow, gravity/head overwhelmingly favours the down path and the momentum pass-through is
**small (order a few %)**. The relief does its real work in Scenario 1. Quantify both;
do not assume Scenario 2 is negligible until the number is in hand (it grows with V², so a
high-velocity surcharged burst is where it matters most).

---

## Methods to use (in preference order)

1. **1-D control-volume split with empirical dividing-flow loss coefficients.** Fast,
   defensible, produces the curve `Q_straight/Q_in` vs conditions. Source the K-factors from:
   - Idelchik, *Handbook of Hydraulic Resistance* — tee/wye dividing-flow K as f(area
     ratio, branch angle, Q_branch/Q_main).
   - Gardel (1957); Ito & Imai; Ramamurthy et al.; Oka & Ito — experimental dividing-flow data.
   - Hager, *Wastewater Hydraulics* — junction/bifurcation treatment for the free-surface case.
   *Note the regime:* pressurised pipe flow vs. free-surface junction use different K sets.
   The relief only engages when the pipe is surcharged (pressurised), so pressurised
   dividing-flow coefficients are the right family, but the free-surface transition matters.
2. **Coupled energy–momentum solve at the junction** (more first-principles; good cross-check
   on method 1).
3. **CFD (2-D/3-D)** only as a validation of the definitive split for one geometry — heavy,
   likely out of scope; mention as an option, don't default to it.

Validate methods 1 and 2 against each other; they should agree within the K-factor uncertainty.

---

## Deliverable

- `Q_straight/Q_in` as a function of storm intensity (→ Q_in via the existing rational-method
  chain), spanning both regimes, for the as-built geometry.
- The intensity at which the relief starts carrying meaningful flow.
- Sensitivity to the three big unknowns: fitting angle (wye vs tee), back-end elevation, and
  fall/outlet capacity (incl. the blocked-outlet case).
- Fold it into the existing sim as a **relief-junction element** with a physically-based
  split rule, plus a visual/tab showing when the relief engages and how much it carries.
  This also *fixes a known limitation* of both the steady tool and SWMM, which split by head
  only and therefore **under-count** the straight pass-through.

---

## CRITICAL context to carry forward (do not let the analysis over-claim)

- **The Y-T sits at the outlet end, DOWNSTREAM of the collector.** The observed flooding is
  at the FAR boca tubos (rows 6–8), UPSTREAM. Water must traverse the entire 63 m collector
  to even reach the Y-T. Therefore the relief **cannot relieve the far-end flooding** — it
  only helps if the binding constraint is at/after the junction (Scenario 1: blocked or
  drowned outlet), or if it acts as a **vent** for air trapped in a surcharged line (the
  air-binding hazard raised earlier, which neither the steady model nor SWMM captures).
- Establishing the *split* is still worth doing: it feeds the SWMM model (which would
  otherwise miss the momentum term) and answers the user's direct question honestly.
- The current steady model already encodes a conservative version: `qDeliverMax` (most the
  collector can push to the fall, ~67–71 L/s) < 8″ fall leader capacity (76 L/s) ⇒ the
  as-built Y-T "stays dry" under head-only logic. The momentum analysis is precisely the
  correction to that conservative result.

## Anchoring numbers (from the measured, validated model)

- Per collector: 1,390 m² roof, Q_in ≈ 44 L/s @120 mm/h, ≈ 64 L/s @ i(Tc≈2.2 min).
- Collector: 8″, 0.9% grade, 63 m, design velocity ~1.25 m/s (velocity head ~0.08 m).
- Fall: 8″ (leader-rated ~76 L/s); user plans/pondered 10″ on the bottom 2–3 m.
- Outlet: open, free, above floor, no tailwater (confirmed) — so Scenario 1 requires an
  *actual* blockage, not ambient backup.
- Buffer before the canaleta tops: ~0.93 m at the far end (measured).
