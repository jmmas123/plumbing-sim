# Design spec — an independent relief-diameter input

_Date: 2026-07-18 · Status: brainstormed with user, pending spec review._

## 1. Purpose

The outlet–relief coupling (shipped, `4bc93b8`) ties the emergency relief's diameter to the
**collector**: tab ②'s outlet head uses `Arel = π/4·(p.d·IN)²` (`sim/index.html:658`), and tab ③'s
`reliefSplit` is called with `dPipe: p.d` (`:695–696`). So a hypothetical 10″ collector re-pipe
silently models a 10″ relief run. Per the user, the real relief run — the open straight-through pipe
past the Y-T that daylights on the rear platform — **stays 8″** even if the collector is re-piped.
Tying it to the collector overstates the relief's modeled help by ~(10/8)² ≈ 1.56× in exactly the
decision case (the 10″ re-pipe). This spec gives the relief its **own diameter**, decoupled from the
collector, so the re-pipe scenario is modeled honestly.

## 2. The honest result this must produce

- **As-built is unchanged.** Collector 8″, relief 8″ → `Arel` identical to today; every as-built
  number holds.
- **A collector re-pipe no longer upsizes the relief.** Set the collector to 10″ and the relief stays
  8″ (its default), so the "floods with relief" figure drops from today's overstated ~490 mm/h toward
  the true 8″-relief value — **still above** the ~208 mm/h without-relief, so the relief still helps,
  just honestly less.
- **The user can still model "upsize the relief too"** by dialing the relief diameter up — then it
  tracks the collector and reproduces the old ~490 result. Both scenarios are legitimate and visible.

The load-bearing honesty line from the coupling spec is unchanged and must survive: the relief cannot
help an UPSTREAM-caused far-end flood (as-built, free outlet); it CAN help a BACKUP-caused one. A
smaller relief simply helps *less* in the backup case — never *more*.

## 3. Model — one diameter, two consumers

Introduce a single parameter `dRelief` (inches), read once in `solveCollector` and used in both
places that currently hardcode `p.d` for the relief pipe:

```
dRelief = p.dRelief != null ? p.dRelief : 8      # default = the measured as-built relief run (8")
Arel    = π/4·(dRelief·IN)²                        # tab ② outlet head  (was p.d — sim/index.html:658)
reliefSplit(Qarr, { dPipe: dRelief, dFall: p.ytFall||p.d, ... })   # tab ③  (was dPipe: p.d — :696)
```

- **No head-balance math changes.** The only change is *which diameter* feeds `Arel` and `dPipe`; the
  formulas (`Krel = 1 + 0.5 + fDarcy·Lrel/D`, `Hrel = Krel·(qOver/Arel)²/(2g)`, the three-regime
  `Hout`, the momentum split) are untouched. Therefore **no adversarial physics re-check is required**
  — only the numeric magnitude shifts, and its direction (smaller Ø ⇒ less relief) is monotone and
  obvious. (Contrast the coupling itself, which changed the boundary and did need the review.)
- **Default is honest, not collector-tracking.** `dRelief` defaults to the as-built relief run (8″),
  NOT to `p.d` — that is the whole point of the fix. `8` is a measured domain fact (as-built collector
  = relief straight run = 8″; see `CLAUDE.md`), not a magic number.
- **Single source of truth.** `dRelief` is computed once and consumed by both tabs, so tab ② and tab
  ③ can never disagree about the relief size. This reuses the existing `dPipe` seam rather than adding
  a parallel concept.

### 3.1 Diameter relationships

`dRelief` is independent of both `d` (collector) and `ytFall` (the vertical fall leader). The three
are distinct physical pipes:

| Param | Physical pipe | Default | Role |
|---|---|---|---|
| `d` | the collector barrel | 8″ | conveyance + the "re-pipe" what-if |
| `ytFall` | the vertical fall/leader at the outlet | `= d` | leader-rated fall cap |
| `dRelief` | the horizontal straight-through relief run past the Y-T | **8″ (fixed as-built)** | relief pipe head-loss area |

## 4. UI (section tab ②)

- A **"Relief diameter"** control in the existing *"Outlet — fall & relief"* fieldset, next to
  `Lrel`. Default 8″, tagged `class="tag t-known"` (the relief run is a measured 8″ pipe). Range
  covering plausible sizes (e.g. 4″–12″), step matching the collector control.
- **Copy** (honest, non-engineer): the relief run is your existing 8″ straight-through pipe; re-piping
  the collector does not change it unless you also replace it. Dial this up only if the re-pipe would
  upsize the relief run too.
- The existing "floods w/ vs w/o relief" readout and the tab-③ momentum curve both react to it
  automatically (they consume the shared solver). No new drawing.
- **Wiring:** ensure the state reader(s) that build `p` for BOTH tabs include `dRelief` (or share it),
  so switching tabs keeps the relief size consistent. Locate the read functions at authoring time;
  do not assume tab ③ reuses tab ②'s reader.

## 5. Invariants (`sim/verify.mjs`)

- **As-built unchanged:** `solveCollector(base)` (d=8, no dRelief) is bit-identical to before — `Arel`
  uses 8″ either way. All existing as-built checks stay green.
- **Default relief is 8″ regardless of collector:** `solveCollector({...base, d:10, ytFall:8}).` relief
  area corresponds to 8″, not 10″ (the honest default). Guard the ~1.56× correction directly.
- **Smaller relief ⇒ less help (new):** under a fall-limited outlet (10″ collector, 8″ fall), the
  with-relief flood threshold is monotone in `dRelief` — a larger `dRelief` raises it, a smaller one
  lowers it. (Complements the spec-§5 `Lrel` monotonicity already worded for "larger dRelief".)
- **C1 guard still green (updated):** the 10″-re-pipe case with the honest **8″** relief still floods
  at a HIGHER threshold with relief than without (relief still helps) — update the existing rep10
  guard (`verify.mjs`, the `fldRep10*` block) to the 8″-default magnitude, and keep/rename the
  "explicitly upsized relief" case (`dRelief:10`) as a separate check that reproduces the ~490 figure.
  Do NOT weaken the direction (`with > without`).
- **Explicit override works:** `solveCollector({...rep10, dRelief:10})` reproduces the pre-fix ~490
  crossing (the "upsize the relief too" scenario).

## 6. Out of scope (tracked follow-ups)

- **M3 — bend loss in `Krel`** (~10–15%): a separate, smaller refinement; user chose to keep it out.
- Drown-to-lip flood *extent* overstatement (L1), the cosmetic `Math.min` recomputes (#1/#2), raising
  the search ceiling further. None are touched here.
- No change to the head-balance physics, the fall/leader model, or the momentum split.
