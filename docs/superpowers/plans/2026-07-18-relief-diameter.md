# Relief-Diameter Input Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the emergency relief its own diameter (`dRelief`), decoupled from the collector, so a 10″ collector re-pipe no longer silently models a 10″ relief run — the real relief stays 8″.

**Architecture:** One `dRelief` value is read in `solveCollector` and fed to both places that hardcode the collector Ø for the relief pipe (tab ②'s `Arel`, tab ③'s `reliefSplit(dPipe:…)`). It defaults to the as-built 8″ (NOT `p.d`), is exposed in the return for testing, and gets a `<select>` control in tab ②'s outlet fieldset wired through the single `readS`. No head-balance math changes — only which diameter feeds the existing formulas — so no adversarial physics re-check is required.

**Tech Stack:** Vanilla ES-in-`<script>` in one self-contained `sim/index.html` (opens over `file://`); Node harness `sim/verify.mjs` extracts the solver from the shipped HTML.

## Global Constraints

- `sim/index.html` self-contained: no external `<script src>`/`<link>`/imports. `<meta charset="utf-8">` stays the FIRST line. All of `solveCollector`/`threshold`/`reliefSplit` stays before the `/* ---------------- svg helpers */` marker so the harness extracts it; UI (`renderS`, fieldsets, `readS`) lives after it.
- After every edit, `node sim/verify.mjs` green.
- `dRelief` default is the as-built relief run **8″**, independent of the collector: `const dRelief = p.dRelief != null ? p.dRelief : 8;`. It is a measured domain fact (CLAUDE.md: 8″ collectors), NOT `p.d`.
- The relief is a horizontal PIPE (its area is `π/4·(dRelief·IN)²`); the FALL is a vertical leader (`leader()`), never Manning. This task only changes the relief's diameter source — no formula changes.
- Provenance tags: `class="tag t-known"` / `class="tag t-assume"` only. The relief-Ø control is tagged `t-known` (as-built 8″ run). Put it in tab ②'s existing "Outlet — fall & relief" fieldset.
- Honesty (load-bearing): the relief run is the existing 8″ straight-through pipe; re-piping the collector does not change it unless it is also replaced. A smaller relief helps LESS in a backup case, never more. Do not weaken the C1 direction ("10″ re-pipe: relief HELPS under a clear outlet").

## Phase 0 — Discovery (COMPLETE)

Verified against the tree at authoring time:
- Relief-Ø sites (grep): `Arel = Math.PI/4 * Math.pow(p.d*IN, 2)` at `sim/index.html:658`; `dPipe: p.d` at `:696`. `reliefSplit`'s own `A = π/4·(p.dPipe*IN)²` (`:740`) reads its `dPipe` PARAM, so changing the `:696` argument suffices — do NOT edit `:740`. `D = p.d*IN` (`:617`) is the COLLECTOR barrel (conveyance) — must NOT change.
- Single state reader: `readS` (`:841–848`) feeds both tabs — `renderRelief` (tab ③) calls `readS()` at `:1151`, and its sweep spreads `s` at `:1161`. So `dRelief` in `readS` reaches both tabs.
- Control types to match: collector `d` is a range slider (`:305–307`, min 4 max 14 step 1); `ytFall` is a `<select>` of pipe sizes (`:485–486`). The relief Ø is a pipe choice → use a `<select>`.
- `verify.mjs`: `base = {i:120, area:1390, d:8, …}` (`:37`, no `dRelief`); `rep10 = {...base, d:10, ytFall:8}` (`:170`); `fld = p => M.threshold(p, x => x.spilling.length > 0)` (`:39`). Every relief test except the `rep10` pair uses `d=8`, where `dRelief` defaults to 8 regardless — so this change is additive to the suite.

---

### Task 1: Solver — `dRelief` param, both consumers, return, guards

**Files:**
- Modify: `sim/index.html` — `solveCollector`: add the `dRelief` const, point `Arel` (line 658) and the `reliefSplit` `dPipe` arg (line 696) at it, add `dRelief` to the return object (line 711 region).
- Test: `sim/verify.mjs` — a new "relief diameter" invariant block.

**Interfaces:**
- Consumes: new optional `p.dRelief` (inches; defaulted so existing callers are unaffected).
- Produces: `solveCollector(...).dRelief` (number, 8 by default); `Arel` and the tab-③ `reliefSplit` now use `dRelief`. All other return keys unchanged.

- [ ] **Step 1: Write the failing tests** — append this block to `sim/verify.mjs` immediately AFTER the "outlet backup coupling" invariant section (locate by content: after the `inv("free-outlet floor preserved …")` line), before the next `console.log` section:

```javascript
console.log("\nINVARIANT — relief diameter (independent of the collector)");
inv("as-built relief Ø defaults to 8\"", M.solveCollector(base).dRelief === 8,
  `dRelief=${M.solveCollector(base).dRelief}`);
inv("a 10\" collector re-pipe does NOT upsize the relief (stays 8\" by default)",
  M.solveCollector({ ...base, d: 10, ytFall: 8 }).dRelief === 8,
  `dRelief=${M.solveCollector({ ...base, d: 10, ytFall: 8 }).dRelief}`);
const fldRelO10 = fld({ ...rep10, dRelief: 10 });
const fldRelO8  = fld({ ...rep10, dRelief: 8 });
inv("upsizing the relief (Ø 8→10) raises the flood point under a fall-limited outlet",
  fldRelO10 !== null && fldRelO8 !== null && fldRelO10 > fldRelO8 + 3,
  `Ø10 ${fldRelO10===null?"—":fldRelO10.toFixed(0)} > Ø8 ${fldRelO8===null?"—":fldRelO8.toFixed(0)} mm/h`);
const fldRel8On  = fld({ ...rep10, dRelief: 8, reliefOn: true });
const fldRel8Off = fld({ ...rep10, dRelief: 8, reliefOn: false });
inv("the honest 8\" relief still HELPS the 10\" re-pipe under a clear outlet",
  fldRel8On !== null && fldRel8Off !== null && fldRel8On > fldRel8Off + 3,
  `with ${fldRel8On===null?"—":fldRel8On.toFixed(0)} > without ${fldRel8Off===null?"—":fldRel8Off.toFixed(0)} mm/h`);
```

- [ ] **Step 2: Run to verify it fails**

Run: `node sim/verify.mjs`
Expected: FAIL. The two default guards fail (`.dRelief` is `undefined`, so `undefined === 8` is false). The monotonicity guard fails because `dRelief` is ignored today (both sides use `p.d=10` → equal → `490 > 490+3` false). The "still helps" guard already passes (it's a regression guard: today rep10 models a 10″ relief ~490 > 208).

- [ ] **Step 3: Add the `dRelief` const and point both consumers at it** — in `sim/index.html`, insert the const immediately BEFORE the `Arel` line (currently 658) and change `Arel` to use it:

```javascript
  const dRelief = p.dRelief != null ? p.dRelief : 8;                    // as-built relief run (8"), NOT the collector
  const Arel = Math.PI/4 * Math.pow(dRelief*IN, 2);                     // relief pipe area (its own diameter)
```

Then change the `reliefSplit` call's `dPipe` argument (currently line 696) from `dPipe: p.d,` to:

```javascript
    dPipe: dRelief, dFall: p.ytFall || p.d,
```

- [ ] **Step 4: Expose `dRelief` in the return** — in the return object, on the line that currently reads `qArr: Qarr, qOver, reliefOn, Hout, outletBackup,` (currently 711), append `dRelief`:

```javascript
    qArr: Qarr, qOver, reliefOn, Hout, outletBackup, dRelief,
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `node sim/verify.mjs`
Expected: PASS — the four new checks AND every pre-existing check. Confirm in your report that all four `fld…` values used by the new guards are non-null (observable within the 600 mm/h ceiling) and print their numbers (expect roughly: Ø10 ≈ 490, Ø8 lower but > 208, both < 600). If any is null, STOP and report it — it means an 8″ relief pushes the crossing past the ceiling, which would need discussion, not a test tweak.

- [ ] **Step 6: Commit**

```bash
git add sim/index.html sim/verify.mjs
git commit -m "feat: relief gets its own diameter (dRelief), default 8\" independent of the collector"
```

---

### Task 2: UI — relief-diameter control, wiring, and honest copy

**Files:**
- Modify: `sim/index.html` — new control in the "Outlet — fall & relief" fieldset (after the `Lrel` control, before the fieldset's `</fieldset>`, currently line 425); `sIds` (currently 812); `readS` (currently 848); a one-clause honesty addition to the section `.note` (the block opening at line 428).

**Interfaces:**
- Consumes: `solveCollector`'s `p.dRelief` (Task 1); `readS`.
- Produces: DOM id `dRelief` (a `<select>`), read into `p.dRelief`.

- [ ] **Step 1: Add the control** — in `sim/index.html`, insert this `.ctl` block immediately AFTER the `Lrel` control's closing `</div>` (currently line 424) and BEFORE the `</fieldset>` (currently line 425):

```html
        <div class="ctl">
          <label for="dRelief"><span>Relief diameter <span class="tag t-known">as-built</span></span></label>
          <select id="dRelief">
            <option value="6">6″</option>
            <option value="8" selected>8″ (as-built run)</option>
            <option value="10">10″</option>
            <option value="12">12″</option>
          </select>
          <p class="hint">The straight-through relief run is your existing 8″ pipe. Re-piping the collector
            (its diameter is on this tab) does NOT change it — leave it at 8″ unless the re-pipe would
            replace this run too. Upsizing it here shows how much more the relief could carry.</p>
        </div>
```

- [ ] **Step 2: Wire read-state** — add the id to `sIds` (currently line 812), appending `"dRelief"` to the array:

```javascript
              "hanger","cls","aged","silt","ytAngle","ytHead","ytFall","ytBlocked","reliefOn","Lrel","dRelief"];
```

and extend the `readS` return (currently line 848) — change `reliefOn: $("reliefOn").value === "1", Lrel: +$("Lrel").value});` to:

```javascript
  reliefOn: $("reliefOn").value === "1", Lrel: +$("Lrel").value, dRelief: +$("dRelief").value});
```

- [ ] **Step 3: Add the honesty clause to the section note** — in the section `.note` block (opens at line 428), find the existing paragraph that mentions the 10″ re-pipe making the relief effective, and append one sentence to it (or add a short sentence within that block):

```html
      <p>The <strong>relief diameter</strong> is set separately (Outlet fieldset): a collector re-pipe
        does not upsize the existing 8″ relief run unless you replace it too, so a 10″ collector with the
        as-built 8″ relief helps less than a fully-10″ relief would — dial the relief Ø up to compare.</p>
```

- [ ] **Step 4: Verify + wiring cross-check**

Run: `node sim/verify.mjs`
Expected: PASS (solver window unchanged by UI edits).

Static self-check (report it): the id `dRelief` is created once in the fieldset, listed in `sIds`, and read in `readS`; `readS` is the single reader feeding both tabs (`renderRelief` calls `readS()`), so tab ③'s `reliefSplit` gets the same `dRelief`. Confirm no other tag class than `t-known`/`t-assume` was introduced and `<meta charset>` is still line 1.

- [ ] **Step 5: Commit**

```bash
git add sim/index.html
git commit -m "feat: section-tab relief-diameter control + honest copy (relief run independent of collector re-pipe)"
```

---

### Task 3: STATE update (controller republish follows)

**Files:**
- Modify: `docs/STATE.md`.

- [ ] **Step 1: Update STATE.md** — under "Current position", record that the relief now has its own diameter (`dRelief`, default as-built 8″), independent of the collector re-pipe; the 10″-re-pipe relief benefit is now modeled with the honest 8″ run (dial it up to compare). In "Open leads #3", mark the relief-Ø input DONE and leave M3 (bend loss) as the remaining refinement. Keep STATE.md ≤40 lines (tighten, don't pile on).

- [ ] **Step 2: Run the full harness**

Run: `node sim/verify.mjs`
Expected: PASS — `ALL CHECKS PASS`.

- [ ] **Step 3: Commit**

```bash
git add docs/STATE.md
git commit -m "docs: relief-diameter input shipped; STATE + open-leads update"
```

- [ ] **Step 4: Republish** — controller step (not the implementer). Redeploy `sim/index.html` to the SAME artifact URL `https://claude.ai/code/artifact/bffe0f46-2342-40d6-a44c-dfef82d8f9f9`, favicon `🌧️`.

---

## Self-Review

**Spec coverage:** §2 honest result (as-built unchanged; re-pipe keeps 8″ relief; upsize to compare) → Task 1 guards + Task 2 copy. §3 model (one `dRelief`, both consumers, default 8″, no math change) → Task 1 Steps 3–4. §3.1 diameter table → Task 1 (independent const). §4 UI (control, tag, copy, wiring through one reader) → Task 2. §5 invariants (as-built unchanged; default 8″ not collector; smaller Ø ⇒ lower threshold; C1 direction; explicit override) → Task 1 Step 1 (`dRelief===8`, monotonicity Ø8 vs Ø10, "still helps"). §6 out of scope (M3, extent, ceiling) → nothing built beyond.

**Placeholder scan:** none — the const, the two consumer edits, the return key, the select options, and the four test assertions are all concrete. No magnitude is hardcoded (guards are relational), so nothing is brittle to the exact 8″-relief crossing value.

**Type consistency:** `dRelief` is a number everywhere — `p.dRelief != null ? p.dRelief : 8` (solver), `+$("dRelief").value` (readS), `.dRelief === 8` (tests). The return key `dRelief` (Task 1 Step 4) is what Task 1's tests read. The `reliefSplit` call now passes `dPipe: dRelief`; `reliefSplit`'s body still reads its `p.dPipe` param (unchanged) — no signature drift.

**One spec-vs-code note (surfaced, not silently changed):** the collector `d` control is tagged `t-assume` ("verify"), while this plan tags the relief-Ø control `t-known` ("as-built") per spec §4 — defensible because 8″ is an established domain fact (CLAUDE.md), but it differs from the collector's own tag. Flag to the human at plan hand-off; a one-word tag change either way is trivial.
