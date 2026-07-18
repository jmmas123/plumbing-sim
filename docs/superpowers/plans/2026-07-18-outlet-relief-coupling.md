# Outlet–Relief Coupling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the section tab's outlet a real throughput constraint (fall + relief), so an overloaded outlet backs up and lifts the HGL along the line — and the relief can be toggled to see it hold the backup down. Bundle two pre-existing solver corrections the coupling depends on.

**Architecture:** All physics lives in `solveCollector` in `sim/index.html`: correct the fall cap and delivery ceiling, then resolve an outlet-end head `H_out` from a fall+relief head balance and use it to seed the existing upstream HGL march. The section tab (②) gains a relief on/off toggle, a relief-length control, and a with/without-relief flood-threshold readout. `sim/verify.mjs` gains invariants. Tab ③ and the momentum split are untouched except the shared fall-cap correction (a no-op for the as-built `d=dFall=8`).

**Tech Stack:** Vanilla ES-in-`<script>` in one self-contained `sim/index.html` (opens over `file://`); Node harness `sim/verify.mjs` extracts the solver from the shipped HTML.

## Global Constraints

- `sim/index.html` self-contained: no external `<script src>`/`<link>`/imports. `<meta charset="utf-8">` stays the FIRST line.
- After every edit, `node sim/verify.mjs` green. Solver code (all of `solveCollector`) stays before the `/* ---------------- svg helpers */` marker so the harness extracts it.
- Vertical leaders (the fall) rated by `leader()` (IPC), never Manning. The relief is HORIZONTAL, so pipe losses DO apply to it (entrance + friction + exit) — it is neither a leader nor a thin plate.
- Provenance tags: `class="tag t-known"` (measured/CAD), `class="tag t-assume"` (assumed/external). No other tag class has color CSS.
- Honesty (load-bearing): the relief cannot help far-end flooding caused UPSTREAM (as-built, free outlet); it CAN lower the far end when the far-end flood is caused by OUTLET BACKUP (blocked, or the 10″ re-pipe). Copy must draw exactly this line and must not suppress the 10″-re-pipe benefit.
- Physics constants from the spec (`docs/superpowers/specs/2026-07-18-outlet-relief-coupling-design.md`): `fallCap = leader(dFall)/1000` blocked-aware; delivery gradient `S + (hf+gdep)/L`; relief `A_rel = π/4·(d·IN)²`, `f = 8·GRAV·n²/(D/4)^(1/3)`, `K_rel = 1 + 0.5 + f·L_rel/D`, `H_rel = K_rel·(q_over/A_rel)²/(2·GRAV)`; `L_rel` default 3 m; `GRAV = 9.81` (the module constant already defined for `reliefSplit`, in scope inside `solveCollector` at call time).

## Phase 0 — Model discovery (COMPLETE)

The model and its coefficients were sourced in the spec and hardened by an adversarial physics review (findings C1, C2, I1–I5, M1–M3). Allowed model — do not deviate:
- Fall: `min(Q_arr, leader(dFall))`, 0 if blocked (gravity-preferred, head-independent leader).
- Relief: carries `q_over = max(0, Q_arr − fallCap)` as a pipe head-loss `K_rel·(q_over/A_rel)²/(2g)` above the crown (conservative lower bound — truly engages earlier; the momentum diversion tab ③ shows is deliberately ignored here).
- `Q_arr = min(Qtot, qDeliverMax)` with the corrected gradient.
- Three regimes → `H_out` (free / crown+H_rel / drowned-to-lip), clamped to the outlet lip; seed = `max(free-march depth, H_out)`.
- Anti-patterns: do NOT use `leader(d)` for the fall cap (must be `dFall`); do NOT model the relief as a thin orifice `Cd=0.6` (pipe head-loss); do NOT claim tab-②/③ numerical consistency.

---

### Task 1: Pre-existing corrections — fall cap by fall diameter, delivery-gradient fix

**Files:**
- Modify: `sim/index.html` — `solveCollector`: `fallCap` (line 640), `qDeliverMax` (line 641).
- Test: `sim/verify.mjs` — two absolute checks + confirm the existing block stays green.

**Interfaces:**
- Consumes: existing `leader`, `pipeCapacity`, `p.ytFall`, `p.ytBlocked`, `D`, `S`, `L`, `p.hf`, `p.gdep`, `p.n`, `hs`.
- Produces: `solveCollector(...).fallCap` now = `leader(p.ytFall||p.d)/1000`, 0 if `p.ytBlocked`; `.qDeliverMax` uses gradient `S + (hf+gdep)/L`. Return-object keys unchanged.

- [ ] **Step 1: Write the failing tests** — append to `sim/verify.mjs` immediately before the final summary `console.log`:

```javascript
console.log("\nABSOLUTE — pre-existing outlet corrections");
ok('fallCap uses the FALL diameter (10" collector, 8" fall)',
  M.solveCollector({ ...base, d: 10, ytFall: 8 }).fallCap * 1000, 76.18, 0.1);
ok('a blocked outlet zeroes the fall cap',
  M.solveCollector({ ...base, ytBlocked: true }).fallCap, 0, 1e-9);
ok('qDeliverMax gradient no longer double-counts slope (base)',
  M.solveCollector(base).qDeliverMax * 1000, 58.2, 1.0);
```

- [ ] **Step 2: Run to verify it fails**

Run: `node sim/verify.mjs`
Expected: FAIL — `fallCap` currently returns `leader(10)=141.4` (not 76.18) and ignores `ytBlocked`; `qDeliverMax` returns ~70.8 (not 58.2).

- [ ] **Step 3: Apply the corrections** — in `sim/index.html`, replace the two lines (currently 640–641):

```javascript
  const fallCap = leader(p.d)/1000;
  const qDeliverMax = pipeCapacity(D, S + (p.hf + p.gdep + S*L)/L, p.n, hs);
```

with:

```javascript
  const dFall = p.ytFall || p.d;                        // the fall may differ from the collector
  const fallCap = (p.ytBlocked ? 0 : leader(dFall))/1000;
  /* Delivery ceiling: driving head = far-end canaleta lip -> outlet crown, over L.
   * grad = S + (hf+gdep)/L. The old form S + (hf+gdep+S*L)/L expanded to 2S+(hf+gdep)/L,
   * double-counting the invert slope. */
  const qDeliverMax = pipeCapacity(D, S + (p.hf + p.gdep)/L, p.n, hs);
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `node sim/verify.mjs`
Expected: PASS — the three new checks, AND every pre-existing check (for the as-built `d=dFall=8`, `leader(dFall)=leader(d)`, so `ytActive`/`qDeliverMax<fallCap` are unchanged in direction; `61<76` still holds). If the tab-③ check "a violent storm wakes the as-built relief" (`reliefFrac>0` at `i:600`) now sits too close to its momentum threshold and flips, raise that test's intensity to `i:900` (still the as-built, still the momentum regime) — note this in your report.

- [ ] **Step 5: Commit**

```bash
git add sim/index.html sim/verify.mjs
git commit -m "fix: fall cap by fall diameter (blocked-aware) + delivery-gradient de-double-count"
```

---

### Task 2: Outlet head balance + HGL boundary coupling

**Files:**
- Modify: `sim/index.html` — `solveCollector`: move the Task-1 `fallCap`/`qDeliverMax` up before the march, add the outlet head balance, change the march seed (line 616), extend the return object; drop the now-duplicate definitions further down.
- Test: `sim/verify.mjs` — coupling invariants.

**Interfaces:**
- Consumes (new optional params on `p`, all defaulted so existing callers are unaffected): `p.reliefOn` (bool, default true → modeled), `p.Lrel` (m, default 3). Existing `p.ytFall`, `p.ytBlocked` already read by `readS`.
- Produces: `solveCollector` return gains `qArr`, `qOver`, `reliefOn`, `Hout`, `outletBackup` (bool `Hout > D`). The HGL profile (`prof`) reflects the elevated outlet seed. `reliefFrac`/tab-③ fields unchanged.

- [ ] **Step 1: Write the failing tests** — append to `sim/verify.mjs` after the Task-1 block:

```javascript
console.log("\nINVARIANT — outlet backup coupling");
const fld = q => M.threshold(q, x => x.spilling.length > 0);
const clr8  = { ...base };                                  // as-built 8" collector, 8" fall, clear
const rep10 = { ...base, d: 10, ytFall: 8 };                // 10" re-pipe over the existing 8" fall
inv("as-built clear outlet: relief is redundant (thresholds match)",
  Math.abs(fld({ ...clr8, reliefOn: true }) - fld({ ...clr8, reliefOn: false })) < 3,
  `with ${fld({...clr8,reliefOn:true}).toFixed(0)} vs without ${fld({...clr8,reliefOn:false}).toFixed(0)} mm/h`);
inv("10\" re-pipe over an 8\" fall: relief HELPS under a CLEAR outlet",
  fld({ ...rep10, reliefOn: true }) > fld({ ...rep10, reliefOn: false }) + 3,
  `with ${fld({...rep10,reliefOn:true}).toFixed(0)} > without ${fld({...rep10,reliefOn:false}).toFixed(0)} mm/h`);
inv("blocked outlet, no relief ⇒ floods far below the clear-outlet threshold",
  fld({ ...clr8, ytBlocked: true, reliefOn: false }) < fld({ ...clr8, reliefOn: false }) - 20);
inv("blocked ordering: no-relief < relief < clear",
  fld({ ...clr8, ytBlocked: true, reliefOn: false })
    < fld({ ...clr8, ytBlocked: true, reliefOn: true })
    && fld({ ...clr8, ytBlocked: true, reliefOn: true }) < fld({ ...clr8, reliefOn: false }));
inv("a shorter relief run carries more (higher threshold under a blocked outlet)",
  fld({ ...clr8, ytBlocked: true, reliefOn: true, Lrel: 1 })
    > fld({ ...clr8, ytBlocked: true, reliefOn: true, Lrel: 20 }));
inv("as-built clear outlet does not back up; a blocked overloaded outlet does",
  !M.solveCollector({ ...clr8, i: 300 }).outletBackup
    && M.solveCollector({ ...clr8, ytBlocked: true, reliefOn: false, i: 300 }).outletBackup);
inv("free-outlet floor preserved (as-built seed unchanged at a routine storm)",
  Math.abs(M.solveCollector({ ...clr8, i: 120 }).prof[0].hgl
    - M.solveCollector({ ...clr8, i: 120, reliefOn: false }).prof[0].hgl) < 1e-9);
```

- [ ] **Step 2: Run to verify it fails**

Run: `node sim/verify.mjs`
Expected: FAIL — `outletBackup` is `undefined`; `reliefOn`/`Lrel` have no effect yet, so the with/without and blocked invariants do not hold.

- [ ] **Step 3: Move the corrected caps up and add the head balance** — in `sim/index.html`, DELETE the two Task-1 lines from their current spot (just above the `reliefSplit` call, ~lines 640–644 region: the `const dFall …`, `const fallCap …`, and `const qDeliverMax …` you wrote in Task 1), and INSERT this block immediately AFTER the `const Qat = x => …;` line (currently 613) and BEFORE `const dx = 0.05, prof = [];` (currently 615):

```javascript
  /* ---- OUTLET THROUGHPUT (fall + relief) sets the downstream HGL boundary ----
   * The fall is a leader capped by the FALL diameter (0 if blocked). The relief
   * carries only the overflow the fall cannot, as a short horizontal PIPE
   * (entrance + friction + exit head-loss), engaging at ~crown — a conservative
   * lower bound (it truly wets earlier; the tab-③ momentum diversion is ignored
   * here). When nothing carries the overflow the outlet drowns to the canaleta lip. */
  const dFall = p.ytFall || p.d;
  const fallCap = (p.ytBlocked ? 0 : leader(dFall))/1000;
  const qDeliverMax = pipeCapacity(D, S + (p.hf + p.gdep)/L, p.n, hs);   // far-end lip -> outlet crown
  const Qarr  = Math.min(Qtot, qDeliverMax);
  const qOver = Math.max(0, Qarr - fallCap);
  const reliefOn = p.reliefOn !== false;                                 // default: modeled
  const Arel = Math.PI/4 * Math.pow(p.d*IN, 2);                          // relief = collector's straight run
  const Lrel = p.Lrel != null ? p.Lrel : 3;                             // relief run length (m)
  const fDarcy = 8*GRAV*p.n*p.n / Math.pow(D/4, 1/3);                    // Darcy f from Manning n
  const Krel = 1 + 0.5 + fDarcy*Lrel/D;                                  // exit + entrance + friction
  const lipHead = gut(0) - zInv(0);                                      // outlet canaleta lip above invert
  let Hout;
  if (qOver <= 0)     Hout = Math.min(normalDepth(Qarr, D, Seff, p.n, hs), D);   // free outlet
  else if (reliefOn)  Hout = D + Krel*Math.pow(qOver/Arel, 2)/(2*GRAV);          // crown + relief pipe head
  else                Hout = lipHead;                                            // drowned to the lip
  Hout = Math.min(Hout, lipHead);
  const outletBackup = Hout > D + 1e-9;
```

- [ ] **Step 4: Seed the march with the outlet head** — replace the march-seed line (currently 616):

```javascript
  let hgl = zInv(0) + Math.min(normalDepth(Qat(0), D, Seff, p.n, hs), D);
```

with:

```javascript
  let hgl = zInv(0) + Math.max(Math.min(normalDepth(Qat(0), D, Seff, p.n, hs), D), Hout);
```

- [ ] **Step 5: Feed the reliefSplit call and extend the return** — the `reliefSplit` call (now just below, formerly ~643) reads `Math.min(Qtot, qDeliverMax)`; change that argument to the already-computed `Qarr`. Then in the return object add these keys alongside `fallCap, qDeliverMax, ytActive`:

```javascript
    qArr: Qarr, qOver, reliefOn, Hout, outletBackup,
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `node sim/verify.mjs`
Expected: PASS — all coupling invariants plus every pre-existing and Task-1 check. If `inv("10\" re-pipe … relief HELPS")` does not hold, do NOT weaken it — report it: it is the load-bearing C1 guarantee and a failure means the coupling is wrong.

- [ ] **Step 7: Commit**

```bash
git add sim/index.html sim/verify.mjs
git commit -m "feat: outlet fall+relief head balance seeds the HGL march"
```

---

### Task 3: Section-tab controls + with/without-relief readout

**Files:**
- Modify: `sim/index.html` — new "Outlet — fall & relief" fieldset in `panel-s` (after the Canaleta fieldset, ~line 406); `sIds` + `readS` (~lines 654/684) for `reliefOn`, `Lrel`; the section stat strip in `renderS` (~line 1020).

**Interfaces:**
- Consumes: `solveCollector`'s new fields; `readS`; `setStrip`; `threshold`.
- Produces: DOM ids `reliefOn`, `Lrel`, `Lrel_v`; new stat rows.

- [ ] **Step 1: Add the controls** — insert this fieldset in `panel-s` immediately AFTER the Canaleta fieldset's closing `</fieldset>` (currently line 406) and BEFORE the `</div>` that closes `.panels` (line 407):

```html
      <fieldset>
        <legend>Outlet — fall &amp; relief</legend>
        <div class="ctl">
          <label for="reliefOn"><span>Emergency relief <span class="tag t-known">as-built</span></span>
            <select id="reliefOn"><option value="1" selected>modeled — count it in outlet capacity</option>
              <option value="0">ignored — see the line without it</option></select></label>
          <p class="hint">Toggle it to compare. Under a clear as-built outlet the fall alone suffices, so
            this changes nothing. Under a blocked outlet — or a 10″ re-pipe over the 8″ fall — it is what
            holds the backup down. Outlet clear/blocked is on the Relief tab (③).</p>
        </div>
        <div class="ctl">
          <label for="Lrel"><span>Relief run length <span class="tag t-assume">assumed</span></span>
            <span class="val" id="Lrel_v">3.0 m</span></label>
          <input type="range" id="Lrel" min="1" max="20" step="0.5" value="3">
          <p class="hint">The horizontal run from the Y-T to where it daylights. A shorter run has less
            pipe friction, so the relief carries more for the same head.</p>
        </div>
      </fieldset>
```

- [ ] **Step 2: Wire read-state** — add the two ids to `sIds` (currently line 654–655):

```javascript
              "hanger","cls","aged","silt","ytAngle","ytHead","ytFall","ytBlocked","reliefOn","Lrel"];
```

and extend the `readS` return (line 684) with:

```javascript
  reliefOn: $("reliefOn").value === "1", Lrel: +$("Lrel").value,
```

- [ ] **Step 3: Add the readout** — in `renderS`, update the `Lrel_v` label and add the with/without rows. The existing `tFld` (line 1017) already sweeps at the current `reliefOn`, so compute only the OPPOSITE case — **one** extra `threshold` sweep, not two (renderS runs on every tab-② drag; keep it cheap). After the existing `const tSur = …, tFld = …;` line (currently 1017), add:

```javascript
  $("Lrel_v").textContent = p.Lrel.toFixed(1) + " m";
  const fldOther = threshold({ ...p, reliefOn: !p.reliefOn }, x => x.spilling.length > 0);
  const fldWith = p.reliefOn ? tFld : fldOther;
  const fldWithout = p.reliefOn ? fldOther : tFld;
  const reliefHelps = fldWith !== null && fldWithout !== null && fldWith - fldWithout > 2;
```

Then add these two rows to the `setStrip($("strip"), [ … ])` array (append inside the array, after the "Spilling now" row):

```javascript
    ,["Outlet capacity", (r.fallCap*1000).toFixed(0)+(r.reliefOn?"+relief":""),
      `fall passes ${(r.fallCap*1000).toFixed(0)} L/s · arriving ${(r.qArr*1000).toFixed(0)} L/s`,
      r.outletBackup?"bad":"ok"],
    ["Floods w/ vs w/o relief", (fldWith===null?"—":fldWith.toFixed(0))+" / "+(fldWithout===null?"—":fldWithout.toFixed(0)),
      reliefHelps ? "mm/h — relief raises the flood point here" : "mm/h — same (fall not the bottleneck)",
      reliefHelps ? "ok" : ""]
```

- [ ] **Step 4: Verify + eyeball**

Run: `node sim/verify.mjs`
Expected: PASS (solver window unchanged by UI edits).

Manual: open `sim/index.html`, tab ②. Confirm the Outlet fieldset renders; the `Lrel` slider updates its readout; toggling "emergency relief" changes nothing for the as-built clear outlet; then on tab ③ set the outlet to blocked and confirm the with/without threshold row and the HGL profile's outlet end both respond, and the profile's water line lifts at the outlet (left) end.

- [ ] **Step 5: Commit**

```bash
git add sim/index.html
git commit -m "feat: section-tab outlet controls + with/without-relief flood readout"
```

---

### Task 4: Honest copy, method note, verify, republish

**Files:**
- Modify: `sim/index.html` — extend the section `.note` (line 409) with the outlet-coupling method/limits and the corrected far-end caveat.
- Modify: `docs/STATE.md` — record the capability + the two corrections.

- [ ] **Step 1: Add the method/caveat note** — inside the section tab's existing `.note` block (starting line 409), append these paragraphs before its closing `</div>`:

```html
      <p><strong>The outlet is now a real bottleneck.</strong> The fall passes its leader rating
        (<code>leader(dFall)</code>, 0 if blocked); the relief carries the overflow as a short pipe
        <span class="tag t-assume">assumed L</span>. When the arriving flow exceeds both, the outlet
        backs up and lifts this whole water line. For the as-built the fall out-capacities the
        collector, so the relief is redundant — but a <strong>10″ re-pipe over the 8″ fall</strong>
        makes the fall the limiter, and then the relief earns its keep with a clear outlet.</p>
      <p><strong>What the relief can and cannot do.</strong> It cannot help far-end flooding caused
        <em>upstream</em> (the flood you actually saw, outlet free — that water never reaches the Y-T).
        It <em>can</em> lower the far end when the flood is caused by <em>outlet backup</em> (a blocked
        outlet, or the 10″ re-pipe) — relieving the outlet drops the HGL everywhere, including the far
        end. This tab ignores the small momentum bypass tab ③ shows, so its relief benefit is a
        conservative lower bound.</p>
```

- [ ] **Step 2: Run the full harness**

Run: `node sim/verify.mjs`
Expected: PASS — `ALL CHECKS PASS`.

- [ ] **Step 3: Update STATE.md** — under "Current position", add a line: the section tab now couples the outlet (fall + relief) into the flood model; note the two corrections (fall cap by fall diameter; delivery-gradient de-double-count) and that the 10″ re-pipe makes the relief effective under a clear outlet. Keep it terse and factual.

- [ ] **Step 4: Commit**

```bash
git add sim/index.html docs/STATE.md
git commit -m "docs: outlet-coupling method/caveat note + state update"
```

- [ ] **Step 5: Republish** — controller step (not the implementer). Redeploy `sim/index.html` to the SAME artifact URL `https://claude.ai/code/artifact/bffe0f46-2342-40d6-a44c-dfef82d8f9f9`, favicon `🌧️`.

---

## Self-Review

**Spec coverage:** §2 honest result (as-built redundant; 10″ helps; far-end caveat) → Task 2 invariants + Task 4 copy. §3.1 fall cap → Task 1. §3.2 relief pipe head-loss → Task 2 block. §3.3 three regimes + seed → Task 2 Steps 3–4. §3.6 limitations → Task 4 copy (momentum lower bound) + spec (vent, non-fixed-point tagged). §4 UI → Task 3. §5 invariants → Task 2 tests. §6 corrections → Task 1. §7 out of scope → nothing built beyond.

**Placeholder scan:** none — every formula and test value is concrete (`58.2`, `76.18`, `K_rel` form, gradient). `L_rel` default pinned at 3 m.

**Type consistency:** `solveCollector` gains `qArr, qOver, reliefOn, Hout, outletBackup` (Task 2) consumed in Task 3's strip (`r.fallCap, r.qArr, r.reliefOn, r.outletBackup`). `readS` keys `reliefOn` (bool) / `Lrel` (number) match `p.reliefOn !== false` / `p.Lrel != null` in the solver. `threshold({...p, reliefOn:false}, …)` matches the solver's `p.reliefOn` read. `fallCap`/`qDeliverMax` are defined once (moved up in Task 2 Step 3; Task 1's temporary location is deleted in the same step) — no double declaration.
