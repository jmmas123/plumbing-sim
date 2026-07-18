# Design spec — coupling the outlet (fall + relief) into the section flood model

_Date: 2026-07-18 · Status: revised after adversarial physics review (score 6.5→ targets ≥8.5),
pending user review._

## 1. Purpose

The section tab (②) marches the water surface upstream from the outlet but seeds that march with a
**free-discharge** boundary (`sim/index.html:616`): it assumes the outlet passes **unlimited** flow.
The fall's leader cap and the Y-T relief are computed but never fed into the boundary. This spec
makes the outlet a **real throughput constraint** so that when the arriving flow exceeds what the
outlet (fall + relief) can pass, the outlet backs up, lifting the HGL along the whole line — and the
relief can be toggled to see it hold that backup down.

## 2. The honest result this must produce

The relief changes the section picture **only when the fall is the binding outlet constraint**.
That happens in two distinct ways — and the adversarial review showed the second is the important
one, not an edge case:

- **(a) A blocked / restricted outlet.** The fall's cap drops (→ 0 when blocked); the relief becomes
  the only path.
- **(b) The collector out-delivers the fall — the 10″ re-pipe.** Re-pipe the collector to 10″ but
  leave the existing 8″ fall, and the collector delivers ~128 L/s into a fall that passes ~76 → the
  fall backs up **with a perfectly clear outlet**, and the relief genuinely helps. Measured:
  `qDeliverMax(10″) ≈ 128 > leader(8″) = 76`. A steeper regrade or a shorter run does the same.

**As-built only**, the relief is redundant: `qDeliverMax(8″) ≈ 61–71 L/s < leader(8″) = 76`, so the
outlet never backs up and with-relief ≡ without-relief. This redundancy is an **arithmetic property
of the as-built geometry (a ~5–15 L/s margin), NOT a structural guarantee** — the tool must say so,
and must NOT suppress case (b). Case (b) is a real, decision-relevant coupling between the user's two
remediation measures (10″ re-pipe + relief), and surfacing it is a feature, not an over-claim.

### The far-end caveat, corrected

The relief **cannot** help far-end flooding **caused upstream** — the as-built observed flood, where
the outlet is free and the far boca tubos top because of the level canaleta + friction. That water
never reaches the Y-T. But the relief **can** lower the far end when the far-end flood is **caused by
outlet backup** (blocked/drowned outlet, or case (b)): relieving the outlet drops the whole HGL,
including at `x = L` (measured 1.19 m far-end drop, blocked case). Copy must draw exactly this
distinction — "cannot help an upstream-caused far-end flood; can help a backup-caused one" — because
the model's own output contradicts any blanket "cannot reach the far end" claim.

## 3. Physics — the outlet head balance

`Q_arr = min(Qtot, qDeliverMax)` is the flow reaching the outlet. Datum: outlet invert at `x=0`,
elevation 0; crown at `D`; outlet canaleta lip at `gut(0)`. Two parallel paths discharge it; we
resolve the outlet-end head `H_out` the arriving flow demands.

### 3.1 Fall (vertical leader) — corrected cap

The fall is a vented vertical leader capped by its plumbing-code rating (annular film, ~head-
independent; project convention, never Manning). **The cap must use the FALL diameter and honor the
blocked flag** (this corrects a bug — see §6):

```
fallCap = blocked ? 0 : leader(dFall)/1000       # dFall = ytFall || d ; NOT leader(d)
q_fall  = min(Q_arr, fallCap)                     # fall takes flow first (drops away downhill)
```

### 3.2 Relief — a horizontal PIPE head-discharge (not a thin orifice)

The relief is the collector's open straight-through run daylighting on the rear platform — a short
horizontal pipe, so pipe losses apply (entrance + friction + exit + velocity head), referenced to
the opening centroid. It carries the overflow the fall cannot:

```
q_over = max(0, Q_arr − fallCap)                                  # overflow
A_rel  = π/4·(dRelief·IN)²                                        # relief = collector straight run: dRelief = d
f      = 8·g·n² / (D/4)^(1/3)                                     # Darcy f from the pipe's own Manning n
K_rel  = 1 + K_e + f·L_rel/D          (K_e = 0.5 entrance, +1 exit/velocity head)
H_rel  = reliefOn ? K_rel·(q_over/A_rel)²/(2g) : ∞               # pipe head-loss to pass q_over
```

For a short daylighting run (`L_rel ≈ 3 m` default, exposed & tagged): `K_rel ≈ 1.9`, effective
discharge coeff ≈ 0.73 — more capacity than a thin-plate `Cd = 0.6`, and the honest value. `Cd = 0.6`
is retained only as a **labeled conservative floor** for `L_rel < ~10 m`; beyond ~10 m the pipe form
must be used or it would over-state the relief.

### 3.3 Outlet-end head → HGL boundary (three regimes)

```
if q_over == 0:            H_out = normalDepth(Q_arr, Seff)   # free outlet — unchanged behavior
elif reliefOn:             H_out = D + H_rel                  # crown + relief pipe head (see §3.4)
else:                      H_out = gut(0)                     # no relief path → drowned to the outlet lip

H_out  = min(H_out, gut(0))                                  # cannot exceed the lip; it spills there
hgl(0) = zInv(0) + max(normalDepth(Q_arr, Seff), H_out)      # never below the free-outlet floor
```

The existing upstream march (`:617–623`) carries this elevated seed unchanged. Note the march then
re-imposes its own `normalDepth(Qtot)` at `x=0` (`:619`), so the effective seed is
`max(§3 boundary, march normalDepth(Qtot))` — for the free branch this masks the difference (both
cap at D); the boundary only bites when `H_out > D`.

### 3.4 Relief engagement is modeled at the crown — a deliberate LOWER BOUND

The relief opening is at pipe level, so it physically starts wetting below the crown (tab ③ shows it
carrying 9–13 L/s by momentum at 65–70 L/s). Modeling the relief as engaging only once the fall is
maxed and the junction reaches the crown therefore **under-states** the relief's help — a deliberate
conservative lower bound. Tab ② is the *capacity* question (does the outlet back up), and it
deliberately ignores the tab-③ momentum diversion; the two are not numerically identical and the
copy must not claim they are (§3.6).

### 3.5 Assumptions and basis (every one exposed or tagged)

| Quantity | Value / form | Basis | Tag |
|---|---|---|---|
| Fall cap | `leader(dFall)`, blocked-aware, head-independent | IPC leader rating | from literature |
| Fall takes flow first | `min(Q_arr, fallCap)` | gravity-preferred downhill path; relief = overflow | assumed |
| Relief discharge | pipe head-loss `√(2gH/K_rel)`, `K_rel=1+K_e+fL/D` | pipe hydraulics (entrance/friction/exit) | from literature |
| Relief run length | `L_rel = 3 m` default, exposed | site (short daylighting run) | assumed / measure |
| Relief engages at crown | `H_out = D + H_rel` | conservative lower bound (truly earlier) | assumed |
| Relief diameter | `dRelief = d` | collector's straight run | measured |
| Arriving flow | `min(Qtot, qDeliverMax)` with corrected qDeliverMax (§6) | conveyance ceiling | derived |

### 3.6 Known limitations (stated, not hidden)

- **Not a fixed point (I4):** `Q_arr` uses the free-outlet delivery ceiling while §3 backs the outlet
  up; the true delivery is slightly lower. Direction is conservative (overstates backup, under-sells
  relief). Not iterated — acceptable, tagged.
- **Momentum divergence (I2):** tab ② ignores the tab-③ momentum diversion, so its backup threshold is
  a **lower bound** on relief benefit. State this; do not claim tab-②/③ numerical consistency.
- **Vent function unmodeled (I5):** at a surcharged junction the fall's top is not vented; the relief
  also acts as an **air vent** that lets a would-be-airlocked fall keep flowing — a real relief benefit
  §3 does not capture. Using the vented leader rating is conservative if the fall would otherwise
  siphon. Flag as a limitation.
- **Drowned ≠ blocked (M3):** a drowned (submerged) outlet still passes some flow as a pressurized
  pipe; modeling it as `fallCap = 0` is conservative. Out of scope, tagged.

## 4. UI (section tab ②)

- **Controls:** "emergency relief — modeled / ignored" (`reliefOn`, default modeled) and, if not
  already reachable from the section tab, the existing "outlet — clear / blocked" (`ytBlocked`). Expose
  `L_rel` (relief run length) tagged `assumed`.
- **Readout** (section stat strip): `Q_arr`, `fallCap`, and the **flood threshold with vs. without the
  relief**. Identical under the as-built clear outlet; divergent under a blocked outlet OR a fall-limited
  geometry (10″ re-pipe / steeper / shorter). A one-line note names the 10″-re-pipe case explicitly.
- **Profile:** no new drawing — the elevated `hgl(0)` lifts the existing water line at `x=0` and
  propagates; overloaded-without-relief visibly drowns the outlet end.
- Provenance tags per §3.5.

## 5. Invariants (`sim/verify.mjs`)

- **As-built clear outlet ⇒ relief redundant** (scoped to as-built): threshold(relief) ≈ threshold(no
  relief), Δ ≈ 0.
- **10″ collector + 8″ fall, CLEAR outlet ⇒ relief helps:** threshold(relief) > threshold(no relief).
  (Guards C1 — the case the guardrail must not suppress.)
- **`fallCap` uses the fall diameter:** `solveCollector({...,d:10,ytFall:8}).fallCap ≈ leader(8)`, not
  `leader(10)`. (Guards C2.)
- **Blocked, no relief ⇒ severe:** threshold far below the clear-outlet threshold.
- **Blocked, relief modeled ⇒ between:** threshold(blocked,no-relief) < threshold(blocked,relief) <
  threshold(clear).
- **Bigger relief ⇒ more capacity:** under a fall-limited outlet, larger `dRelief` (or shorter `L_rel`)
  raises the flood threshold.
- **Backpressure ∝ overflow² (relief-ON branch only):** double the overflow ⇒ ~4× `H_rel`.
- **Free-outlet floor preserved:** `hgl(0) ≥ zInv(0)+normalDepth(Q_arr)` always.
- **No regression:** existing checks stay green; `reliefFrac`/tab-③ untouched (except the shared
  `fallCap` correction, which must keep the as-built `ytActive` result unchanged — for `d=dFall=8`,
  `leader(dFall)=leader(d)`).

## 6. Pre-existing corrections bundled (the coupling's correctness depends on them)

- **C2 — fall cap by fall diameter.** `sim/index.html:640` `fallCap = leader(p.d)` → must be
  `leader(p.dFall||p.d)` and honor `blocked`; `ytActive` (`:658`) consumes it. For the as-built
  (`d=dFall=8`) the value is unchanged; it only corrects the 10″-collector/8″-fall case. Verify the
  existing `ytActive` invariants stay green.
- **I4 — qDeliverMax gradient.** `:641` gradient `S + (hf+gdep+S·L)/L` expands to `2S+(hf+gdep)/L`,
  double-counting the slope. First-principles (far-end lip → outlet crown, over L):
  `Δ = gut(L) − D = hf + S·L + gdep`, so gradient `= S + (hf+gdep)/L`. This lowers as-built
  `qDeliverMax` ~14% (≈71 → ≈61 L/s), *widening* the as-built redundancy margin (still `< 76`), and
  is the load-bearing ceiling for `Q_arr`. Fix and pin; keep `qDeliverMax < fallCap` invariant green.

## 7. Out of scope

Re-deriving the tab-③ momentum split; a simultaneous leader+orifice junction solve; the relief's vent
mechanism; iterating `Q_arr` to a fixed point; time-varying storms; SWMM.
