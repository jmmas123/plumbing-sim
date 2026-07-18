# Y-T Relief Momentum-Split Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the head-only `ytActive` boolean with a physically-based, momentum-aware dividing-flow split at the Y-T, and expose it as a new "Relief" tab showing what fraction of flow exits straight out the open back vs. turns down the fall.

**Architecture:** One pure `reliefSplit(qIn, geom)` function added to the shipped solver in `sim/index.html`, called from inside `solveCollector`. A new "Relief" tab renders a `straight-fraction vs. storm-intensity` curve (via the existing generic `chart()`) plus a live junction-split diagram. `sim/verify.mjs` gains invariants that pin the physics. The existing head-only `ytActive` field is retained unchanged as the conservative reference the spec requires.

**Tech Stack:** Vanilla ES-in-`<script>` inside a single self-contained `sim/index.html` (opens over `file://`); Node ES-module harness `sim/verify.mjs` that extracts the solver from the shipped HTML and imports it.

## Global Constraints

- `sim/index.html` is self-contained on purpose — ES modules do not load over `file://`. Do not add external `<script src>`/`<link>`/imports.
- `<meta charset="utf-8">` MUST remain the **first line** of `sim/index.html`.
- After **every** edit to `sim/index.html`, run `node sim/verify.mjs` and keep all checks green. It extracts the solver from `js.slice(js.indexOf("const IN = 0.0254"), js.indexOf("/* ---------------- svg helpers"))`, so **all solver code (including `reliefSplit`) MUST sit before the `/* ---------------- svg helpers */` marker** (currently line 603) to be in the extraction window. UI code (`renderRelief`, diagrams) sits AFTER that marker and is not extracted.
- **Reuse existing helpers, do not re-implement:** stat cards use `setStrip(node, rows)` + `stat(k,v,n,cls)` (lines 611–618) into a `.strip` container; line charts use `chart(svg, opt)` (line 621); DOM helpers `$`, `el`, `txt`, `clear`.
- Downspouts / vertical leaders are rated by IPC code (`leader()` orifice rating), NEVER Manning.
- Preserve the in-UI provenance tags `from CAD` / `measured` / `assumed`. New K-factors are tagged `from literature`; the branch head `h` is tagged `assumed`; the fitting geometry is `measured`.
- The Y-T is DOWNSTREAM of the collector and **cannot** relieve far-end (rows 6–8) flooding — UI copy must say so; do not over-claim.
- Fitting: **90° tee** as-built (user-confirmed 2026-07-16); 45° wye is the sensitivity floor.
- Coefficients (from Phase 0 research, cite in code comments): `K_b(θ) = 1 − cos θ` (1.0 @ 90°, 0.29 @ 45°; Idelchik Ch. 7 / Crane TP-410 bracket 0.7–1.7 @ 90°); straight-run `K_s ≈ 0`; branch effective head `h` default 0.3 m, swept 0.1–1.0 m; gravity `g = 9.81`.

## Phase 0 — Documentation discovery (COMPLETE)

Dividing-flow coefficients were sourced and cross-checked by two independent research passes; results are pinned in the spec (`docs/superpowers/specs/2026-07-17-yt-relief-momentum-split-design.md`, §4). Allowed model — **do not deviate without re-sourcing**:

- **Split law (primary):** `phi = ((1+Kb) − sqrt(1 + Kb + Kb/N)) / Kb`, clipped at 0, with `N = V_in²/(2·g·h)`. Derived by control-volume energy split with a momentum-derived turning loss; cross-checked by an independent ballistic-transit argument (both give the same `V²` law and the same `phi→0` as `V→0`). Source: momentum-CV research pass; corroborated by Ramamurthy & Satish (1988) J. Hydraulic Eng. 114(4):428 and Hager, *Wastewater Hydraulics*.
- **Turning loss:** `Kb(θ) = 1 − cos θ` (Borda / destroyed-streamwise-component form). Empirical bracket: Idelchik `K_c,b = A′[1+0.3q²]` ≈ 0.73–0.94 @ 90°, Crane TP-410 ≈ 1.0–1.7 @ 90°; both ≈ 0.3–0.8 @ 45°. Sources: Idelchik *Handbook of Hydraulic Resistance* Ch. 7 (via Deltares WANDA T/Y-junction docs); Crane TP-410 (via Caleb Bell `fluids` library).
- **Anti-pattern to avoid:** Miller *Internal Flow Systems* dividing-flow data is **90°-only (angle-blind)** — must NOT be used to derive the 45°-vs-90° sensitivity.
- **Regime caveat:** these are full-bore **pressurised** correlations. Below surcharge onset the junction is open-channel and `phi = 0` — hence the `qIn ≥ qFull` gate.

---

### Task 1: `reliefSplit()` core physics function

**Files:**
- Modify: `sim/index.html` — insert `reliefSplit` after `solveCollector` ends (currently line 594) and before the `/* ---------------- svg helpers */` marker (line 603).
- Modify: `sim/verify.mjs:22` — add `reliefSplit` to the export list.
- Test: `sim/verify.mjs` — new ABSOLUTE/INVARIANT block.

**Interfaces:**
- Consumes: existing `IN` (0.0254) and `leader(d)` (L/s) from the solver core.
- Produces: `reliefSplit(qIn_m3s, geom) → { qIn, qStraight, qFall, reliefFrac, mechanism, vIn, N, phi, Kb, cap }` where `geom = { dPipe, dFall, angleDeg, h, blocked, qFull }` (dPipe/dFall in inches, h in m, qFull in m³/s, blocked bool). `qStraight + qFall === qIn`; `0 ≤ reliefFrac ≤ 1`; `mechanism ∈ {"dry","momentum","head","both"}`.

- [ ] **Step 1: Write the failing tests** — append this block to `sim/verify.mjs` immediately before the final `console.log("\n" + ...)` summary line (currently line 120):

```javascript
console.log("\nABSOLUTE — momentum-aware Y-T relief split (closed form vs hand calc)");
const gj = { dPipe: 8, dFall: 8, angleDeg: 90, h: 0.3, blocked: false, qFull: 0.040 };
ok("90 deg relief frac @70 L/s", M.reliefSplit(0.070, gj).reliefFrac, 0.194, 0.02);
ok("45 deg relief frac @70 L/s", M.reliefSplit(0.070, { ...gj, angleDeg: 45 }).reliefFrac, 0.011, 0.01);

console.log("\nINVARIANT — the relief split obeys the physics");
inv("90 deg tee sends MORE straight than a 45 wye",
  M.reliefSplit(0.070, gj).reliefFrac > M.reliefSplit(0.070, { ...gj, angleDeg: 45 }).reliefFrac,
  `90:${M.reliefSplit(0.070,gj).reliefFrac.toFixed(3)} vs 45:${M.reliefSplit(0.070,{...gj,angleDeg:45}).reliefFrac.toFixed(3)}`);
inv("a blocked outlet forces the WHOLE flow straight",
  Math.abs(M.reliefSplit(0.070, { ...gj, blocked: true }).reliefFrac - 1) < 1e-9);
inv("below surcharge onset the relief is DRY (open-channel, gravity wins)",
  M.reliefSplit(0.030, gj).reliefFrac === 0 && M.reliefSplit(0.030, gj).mechanism === "dry");
inv("a deep branch head starves the momentum relief (N below threshold)",
  M.reliefSplit(0.070, { ...gj, h: 5.0 }).reliefFrac < 0.01,
  "raising h drops N below 1/(1+Kb) so phi -> 0");
inv("mass is conserved at the junction",
  Math.abs(M.reliefSplit(0.070, gj).qStraight + M.reliefSplit(0.070, gj).qFall - 0.070) < 1e-12);
inv("relief fraction is bounded [0,1]",
  (r => r.reliefFrac >= 0 && r.reliefFrac <= 1)(M.reliefSplit(0.070, gj)));
inv("momentum grows with velocity head (V^2)",
  M.reliefSplit(0.090, gj).reliefFrac > M.reliefSplit(0.070, gj).reliefFrac,
  "more flow -> higher V -> larger straight fraction");
```

- [ ] **Step 2: Add the export, then run to verify it fails** — edit `sim/verify.mjs:22`:

```javascript
  "\nexport {solveCollector, threshold, leader, idf, timeOfConcentration, rationalQ, sagOf, section, reliefSplit};\n");
```

Run: `node sim/verify.mjs`
Expected: FAIL — the run aborts with `does not provide an export named 'reliefSplit'` (function not yet defined).

- [ ] **Step 3: Implement `reliefSplit`** — in `sim/index.html`, insert after the closing `}` of `solveCollector` (line 594) and before the `/* ---------------- svg helpers */` comment:

```javascript
/* ---- Y-T RELIEF SPLIT ----------------------------------------------------
 * Dividing junction at the outlet: the straight-through RUN is the OPEN relief,
 * the BRANCH turns down the fall. Head-only logic (see `ytActive`) says the relief
 * stays dry; this adds the momentum pass-through that a head balance omits.
 *
 * Regime gate: below surcharge onset (qIn < qFull) the junction runs as an open
 * channel and gravity drains everything down the branch -> phi = 0. Once
 * pressurised, a control-volume energy split with a momentum-derived turning loss
 * gives the straight fraction (cross-checked by a ballistic-transit argument):
 *     phi = ((1+Kb) - sqrt(1 + Kb + Kb/N)) / Kb ,   N = V^2 / (2 g h)
 * Kb(theta) = 1 - cos(theta): 1.0 at a 90 deg tee, 0.29 at a 45 deg wye. Idelchik
 * Ch.7 / Crane TP-410 bracket Kb(90) in ~0.7-1.7 -> the sensitivity band. The fall
 * swallows at most its leader rating; the capped remainder ALSO spills straight,
 * unifying the momentum and head-overflow mechanisms in one min(). */
const GRAV = 9.81;
function reliefSplit(qIn, p){
  const A = Math.PI/4 * Math.pow(p.dPipe*IN, 2);        // full-bore collector area
  const vIn = qIn > 0 ? qIn/A : 0;                      // combined velocity (the K reference)
  const Kb = 1 - Math.cos(p.angleDeg*Math.PI/180);      // turning loss into the branch
  const N = (vIn > 0 && p.h > 0) ? (vIn*vIn)/(2*GRAV*p.h) : 0;
  let phi = 0;
  if (qIn >= p.qFull && N > 0 && Kb > 1e-9)
    phi = Math.max(0, ((1+Kb) - Math.sqrt(1 + Kb + Kb/N)) / Kb);
  const cap = p.blocked ? 0 : leader(p.dFall)/1000;     // annular-film leader cap (m3/s)
  const qFall = Math.min((1-phi)*qIn, cap);
  const qStraight = qIn - qFall;
  const reliefFrac = qIn > 0 ? qStraight/qIn : 0;
  const capBinds = (1-phi)*qIn > cap + 1e-12;           // fall pinned at its rating -> overflow
  let mechanism = "dry";
  if (qStraight > 1e-9) mechanism = (phi > 1e-6 && capBinds) ? "both"
                                  : capBinds ? "head" : "momentum";
  return {qIn, qStraight, qFall, reliefFrac, mechanism, vIn, N, phi, Kb, cap};
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `node sim/verify.mjs`
Expected: PASS — all prior checks plus the 10 new lines. The two `ok()` lines land at 0.194 / 0.011; `ALL CHECKS PASS` at the end.

- [ ] **Step 5: Commit**

```bash
git add sim/index.html sim/verify.mjs
git commit -m "feat: momentum-aware reliefSplit core + invariants"
```

---

### Task 2: Wire `reliefSplit` into `solveCollector`

**Files:**
- Modify: `sim/index.html` — inside `solveCollector`, after `qDeliverMax` is computed (line 581) and in the return object (lines 588–593).
- Test: `sim/verify.mjs` — three solver-level invariants.

**Interfaces:**
- Consumes: `reliefSplit` (Task 1); existing `Qtot`, `qDeliverMax`, `Qcap` locals in `solveCollector`; new optional params on `p`: `ytAngle` (deg, default 90), `ytHead` (m, default 0.3), `ytBlocked` (bool, default false), `ytFall` (in, default `p.d`).
- Produces: extends `solveCollector`'s return with `reliefFrac`, `qStraight`, `qFall`, `reliefMech`, `reliefVin`. Leaves `ytActive` (head-only boolean) UNCHANGED.

- [ ] **Step 1: Write the failing tests** — append to `sim/verify.mjs` right after the Task 1 block:

```javascript
console.log("\nINVARIANT — solveCollector surfaces the momentum relief");
inv("a violent storm wakes the as-built relief",
  M.solveCollector({ ...base, i: 600 }).reliefFrac > 0,
  `frac ${(M.solveCollector({ ...base, i: 600 }).reliefFrac*100).toFixed(0)}%`);
inv("a routine storm leaves the as-built relief dry",
  M.solveCollector({ ...base, i: 120 }).reliefFrac === 0);
inv("head-only ytActive is untouched (still the conservative reference)",
  M.solveCollector({ ...base, i: 600 }).ytActive === false);
```

- [ ] **Step 2: Run to verify it fails**

Run: `node sim/verify.mjs`
Expected: FAIL — `reliefFrac` is `undefined` on `solveCollector`'s return, so `undefined > 0` is false → the first new `inv` fails.

- [ ] **Step 3: Implement the wiring** — in `sim/index.html`, immediately after the `qDeliverMax` line (581), add:

```javascript
  const relief = reliefSplit(Math.min(Qtot, qDeliverMax), {
    dPipe: p.d, dFall: p.ytFall || p.d,
    angleDeg: (p.ytAngle != null ? p.ytAngle : 90),
    h: (p.ytHead != null ? p.ytHead : 0.3),
    blocked: !!p.ytBlocked, qFull: Qcap });
```

Then extend the return object (lines 588–593) by adding these fields alongside `fallCap, qDeliverMax, ytActive`:

```javascript
    reliefFrac: relief.reliefFrac, qStraight: relief.qStraight, qFall: relief.qFall,
    reliefMech: relief.mechanism, reliefVin: relief.vIn,
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `node sim/verify.mjs`
Expected: PASS — all checks green, including the three new ones and every pre-existing invariant (the head-only `ytActive` block at lines 111–118 is unchanged).

- [ ] **Step 5: Commit**

```bash
git add sim/index.html sim/verify.mjs
git commit -m "feat: expose relief split from solveCollector, keep ytActive reference"
```

---

### Task 3: Relief tab — controls, panel, and stat readout (reuse `setStrip`)

**Files:**
- Modify: `sim/index.html` — tab button (after line 136), new tabpanel before `<script>` (line 427), `sIds` (line 654), `readS` (lines 684–688), `renderRelief` (after `renderS`, ~line 954), `update()` (line 955), `tabs` array (line 971).

**Interfaces:**
- Consumes: `readS()`, `solveCollector`, existing `setStrip(node, rows)` / `stat(k,v,n,cls)` (lines 611–618), `$`.
- Produces: `renderRelief()` (called from `update()`); DOM ids `ytAngle`, `ytHead`, `ytHeadOut`, `ytFall`, `ytBlocked`, `panel-r`, `tab-r`, `relief-stats`, `relief-curve`, `relief-diagram`.

- [ ] **Step 1: Add the tab button** — after line 136 (`tab-s` button):

```html
    <button role="tab" id="tab-r" aria-controls="panel-r" aria-selected="false">③ Relief — the Y-T split</button>
```

- [ ] **Step 2: Add the tab panel** — immediately before the `<script>` line (currently 427), after the `</div>` that closes `panel-s`. Both SVG mounts are included now (following the runoff tab's `.grid2`/`.sheet`/`.cap` pattern) so Task 4 only fills render logic:

```html
  <!-- ================= RELIEF ================= -->
  <div role="tabpanel" id="panel-r" aria-labelledby="tab-r" hidden>
    <p class="sub">Of the flow that reaches the outlet, how much shoots straight out the open back
      (the relief) versus turning 90° down the fall. The head-only model on tab ② says the relief
      stays dry — this is the momentum correction it cannot see.</p>

    <div class="strip" id="relief-stats"></div>

    <div class="grid2">
      <div class="sheet">
        <svg id="relief-curve" viewBox="0 0 520 300" role="img"
             aria-label="Straight-out fraction versus storm intensity"></svg>
        <div class="cap"><span>Straight-out fraction vs storm intensity</span></div>
      </div>
      <div class="sheet">
        <svg id="relief-diagram" viewBox="0 0 520 200" role="img"
             aria-label="Junction split schematic at current settings"></svg>
        <div class="cap"><span>The split at your current settings</span></div>
      </div>
    </div>

    <div class="panels">
      <fieldset>
        <legend>Y-T junction <span class="tag measured">measured</span></legend>
        <label for="ytAngle"><span>Down-turn fitting</span>
          <select id="ytAngle"><option value="90">90° tee (as-built)</option>
            <option value="45">45° wye</option></select></label>
        <label for="ytFall"><span>Fall diameter</span>
          <select id="ytFall"><option value="8">8″ (as-built)</option>
            <option value="10">10″ (planned)</option></select></label>
        <label for="ytBlocked"><span>Outlet</span>
          <select id="ytBlocked"><option value="0">clear</option>
            <option value="1">blocked (emergency)</option></select></label>
        <label for="ytHead"><span>Branch head h <span class="tag assumed">assumed</span></span>
          <input type="range" id="ytHead" min="0.1" max="1.0" step="0.05" value="0.3">
          <output id="ytHeadOut">0.30 m</output></label>
        <p class="hint">h is the branch's effective gravity head — the dominant uncertainty in the
          split (±0.1 on the fraction). It sets the storm intensity at which the relief wakes.</p>
      </fieldset>
      <div class="note" style="margin:0">
        <p><strong>The relief sits DOWNSTREAM of the whole collector.</strong> It can only help a
          blocked or drowned outlet, or vent trapped air. It <em>cannot</em> relieve the far-end
          boca-tubo flooding you observed — that water never reaches the Y-T.</p>
      </div>
    </div>
  </div>
```

- [ ] **Step 3: Wire read-state** — add the four ids to `sIds` (lines 654–655):

```javascript
const sIds = ["i","area","d","s","L","n","gs","gwid","gdep","gtype","hf","nb","db","useTc",
              "hanger","cls","aged","silt","ytAngle","ytHead","ytFall","ytBlocked"];
```

Extend the `readS` return (line 684) by adding:

```javascript
  ytAngle:+$("ytAngle").value, ytHead:+$("ytHead").value, ytFall:+$("ytFall").value,
  ytBlocked:$("ytBlocked").value === "1",
```

- [ ] **Step 4: Add `renderRelief` with the stat strip** — after `renderS` ends (before `const update`, ~line 954):

```javascript
/* ---------------- relief tab ---------------- */
const RELIEF_MECH = {dry:"all down the fall", momentum:"momentum pass-through",
  head:"head overflow (fall capped)", both:"overflow + momentum"};
function renderRelief(){
  $("ytHeadOut").textContent = (+$("ytHead").value).toFixed(2) + " m";
  const s = readS(), r = solveCollector(s);
  const qJ = Math.min(r.Qtot, r.qDeliverMax)*1000;
  setStrip($("relief-stats"), [
    ["straight out the back", (r.reliefFrac*100).toFixed(0)+"%",
      `${(r.qStraight*1000).toFixed(1)} of ${qJ.toFixed(1)} L/s`, r.reliefFrac>1e-6?"bad":""],
    ["down the fall", ((1-r.reliefFrac)*100).toFixed(0)+"%", `${(r.qFall*1000).toFixed(1)} L/s`],
    ["regime", RELIEF_MECH[r.reliefMech]||r.reliefMech, `at i = ${s.i} mm/h`]
  ]);
}
```

- [ ] **Step 5: Register in `update()` and the `tabs` array** — change line 955:

```javascript
const update = () => { renderS(renderQ()); renderRelief(); };
```

and line 971:

```javascript
const tabs = [["tab-q","panel-q"],["tab-s","panel-s"],["tab-r","panel-r"]];
```

- [ ] **Step 6: Verify solver still green, then eyeball the tab**

Run: `node sim/verify.mjs`
Expected: PASS.

Manual: open `sim/index.html`, click tab ③, confirm three stat cards render, the `h` slider updates its `m` readout live, and switching the fitting select from 90° to 45° lowers the "straight out the back" percentage. (The two SVGs are empty until Task 4.)

- [ ] **Step 7: Commit**

```bash
git add sim/index.html
git commit -m "feat: Relief tab shell, controls, and split readout"
```

---

### Task 4: Relief tab — intensity-sweep curve (reuse `chart`) + junction diagram

**Files:** Modify `sim/index.html` — add a bespoke `reliefDiagram` builder, and extend `renderRelief` with a `chart()` call plus the diagram render.

**Interfaces:**
- Consumes: `chart(svg, opt)` (line 621), `solveCollector`, `el`, `txt`, `clear`; CSS vars `--water`, `--bad`, `--muted`, `--ink-2`.
- Produces: `reliefDiagram(svg, r)`; the two SVG renders inside `renderRelief`.

- [ ] **Step 1: Write the bespoke junction-diagram builder** — add inside the IIFE, above `renderRelief` (there is no existing helper for a schematic, so this SVG is hand-rolled; the line chart is not):

```javascript
/* Live schematic: incoming run (left), open straight relief (right), branch down
 * the fall. Bar thicknesses ~ flow share; the relief bar turns red when it carries flow. */
function reliefDiagram(svg, r){
  clear(svg); const g = el("g",{}); svg.appendChild(g);
  const midY = 92, jx = 300, active = r.reliefFrac > 1e-6;
  const wOf = f => 5 + 40*Math.max(0.02, f);
  g.appendChild(el("rect",{x:36,y:midY-wOf(1)/2,width:jx-36,height:wOf(1),
    fill:"var(--water)",opacity:0.28}));                                  // incoming run
  g.appendChild(el("rect",{x:jx,y:midY-wOf(r.reliefFrac)/2,width:150,height:wOf(r.reliefFrac),
    fill:active?"var(--bad)":"var(--muted)",opacity:active?0.5:0.2}));    // straight relief
  g.appendChild(el("rect",{x:jx-wOf(1-r.reliefFrac)/2,y:midY,width:wOf(1-r.reliefFrac),height:86,
    fill:"var(--water)",opacity:0.5}));                                   // branch down
  g.appendChild(txt(150,midY-26,"collector in",{"font-size":10,fill:"var(--muted)"}));
  g.appendChild(txt(486,midY-wOf(r.reliefFrac)/2-6,`relief ${(r.qStraight*1000).toFixed(1)} L/s`,
    {"text-anchor":"end","font-size":10,fill:active?"var(--bad)":"var(--muted)"}));
  g.appendChild(txt(jx+14,midY+80,`fall ${(r.qFall*1000).toFixed(1)} L/s`,
    {"font-size":10,fill:"var(--water)"}));
}
```

- [ ] **Step 2: Draw the curve and diagram from `renderRelief`** — append to the end of `renderRelief` (after the `setStrip(...)` call). The 45° floor and the current-fitting line form the sensitivity band; the mark is the live operating point:

```javascript
  const sweep = angle => { const pts=[]; for (let i=5;i<=600;i+=5)
    pts.push([i, solveCollector({ ...s, i, ytAngle: angle }).reliefFrac]); return pts; };
  chart($("relief-curve"), {
    xmin:0, xmax:600, ymin:0, ymax:1,
    xticks:[0,150,300,450,600], yticks:[0,0.25,0.5,0.75,1.0],
    xlab:"storm intensity (mm/h)", ylab:"straight-out fraction", yfmt:v=>(v*100).toFixed(0)+"%",
    series:[
      {pts:sweep(45), attrs:{stroke:"var(--muted)","stroke-width":1.3,"stroke-dasharray":"4 3"}},
      {pts:sweep(+s.ytAngle), attrs:{stroke:"var(--water)","stroke-width":2.5}}
    ],
    marks:[{x:+s.i, y:r.reliefFrac, label:"you are here", color:"var(--ink-2)"}]
  });
  reliefDiagram($("relief-diagram"), r);
```

- [ ] **Step 3: Verify + eyeball**

Run: `node sim/verify.mjs`
Expected: PASS (solver window unchanged).

Manual: open `sim/index.html`, tab ③. Confirm: the water-blue 90° curve rises above the dashed grey 45° floor; sliding `h` right shifts the curve's takeoff to higher intensity; setting Outlet → blocked pins the curve near 100%; the diagram's relief bar turns red and widens as intensity climbs; the "you are here" mark tracks the `i` slider.

- [ ] **Step 4: Commit**

```bash
git add sim/index.html
git commit -m "feat: relief intensity curve (chart) + live junction diagram"
```

---

### Task 5: Honesty copy, method note, and republish

**Files:**
- Modify: `sim/index.html` — add a "Method / Limits" note to `panel-r`.
- Modify: `docs/STATE.md` — record the new capability.

**Interfaces:** none (documentation + provenance only).

- [ ] **Step 1: Add the method note** — inside `panel-r`, append after the `.panels` block (before the panel's closing `</div>`):

```html
    <div class="note">
      <p><strong>Method.</strong> A dividing-flow split at the junction. Below surcharge the
        junction runs part-full and gravity takes everything down the fall (relief dry). Once
        pressurised, momentum overshoots the 90° down-turn: <code>φ = ((1+Kb) − √(1+Kb+Kb/N))/Kb</code>,
        <code>N = V²/2gh</code>, <code>Kb = 1 − cos θ</code>
        <span class="tag t-assume">from literature</span> (Idelchik Ch. 7 / Crane TP-410; cross-checked
        by a momentum control volume). The fall is leader-capped; the remainder spills straight.</p>
      <p><strong>Limits.</strong> Steady flow. The branch head <code>h</code> is assumed, not
        measured — it moves the fraction by ±0.1 and sets the wake-up intensity. The 90° branch loss
        itself is uncertain ~2× (Idelchik ~1.0 vs Crane ~1.7); this tool uses the Borda form 1.0.</p>
    </div>
```

(Provenance tags in this file are `class="tag t-known"` for measured/CAD facts and `class="tag t-assume"` for assumptions/external values — there is no `measured`/`assumed` modifier. Literature-sourced coefficients use `t-assume`.)

- [ ] **Step 2: Run the full harness one last time**

Run: `node sim/verify.mjs`
Expected: PASS — `ALL CHECKS PASS`.

- [ ] **Step 3: Update STATE.md** — under "Current position", note that the Relief tab (momentum-aware Y-T split) is built and test-backed; move the Y-T item out of "Open leads" into done.

- [ ] **Step 4: Commit**

```bash
git add sim/index.html docs/STATE.md
git commit -m "docs: relief method/limits note + state update"
```

- [ ] **Step 5: Republish the artifact** — redeploy the SAME published tool (do NOT mint a new URL). Use the `Artifact` tool:
  - `file_path`: `sim/index.html`
  - `url`: `https://claude.ai/code/artifact/bffe0f46-2342-40d6-a44c-dfef82d8f9f9`
  - `favicon`: keep the existing emoji unchanged.
  - Confirm the published page shows tab ③.

- [ ] **Step 6: Push**

```bash
git push origin main
```

---

## Self-Review

**Spec coverage:** §1 purpose → Tasks 1–4. §4 Mechanism 1 (overflow) → Task 1 `cap`/`min()`; Mechanism 2 (momentum) → Task 1 `phi`; unified combining → Task 1. §5 sensitivity axes (angle, h, fall/blocked) → Task 3 controls + Task 4 band curve. §6 deliverables (`reliefSplit`, curve, engagement intensity, tab, diagram) → Tasks 1/3/4. §7 integration (supersede via new tab, keep `ytActive` reference, new invariants, provenance tags, charset, verify-green, reuse helpers) → Tasks 2/3/4/5. §2 downstream caveat → Task 3 note. §8 out-of-scope (SWMM/CFD/time) → not built. **Gap:** "intensity at which relief starts carrying meaningful flow" is shown *visually* (curve takeoff + live "regime" stat) rather than as a separate numeric stat — acceptable per spec; a numeric threshold readout is a possible future refinement, not a blocker.

**Placeholder scan:** none. No TBD/TODO/"implement later". Every code step shows complete code.

**Type consistency:** `reliefSplit` returns `{reliefFrac, qStraight, qFall, mechanism, vIn, ...}` (Task 1); `solveCollector` re-exposes them as `reliefFrac, qStraight, qFall, reliefMech, reliefVin` (Task 2 — the `mechanism`→`reliefMech` rename is deliberate and is consumed as `r.reliefMech` in Task 3 Step 4). `geom` keys (`dPipe, dFall, angleDeg, h, blocked, qFull`) match between the Task 1 definition and the Task 2 call site. `readS` keys (`ytAngle, ytHead, ytFall, ytBlocked`) match the `p.yt*` reads in Task 2. Tab/panel ids (`tab-r`/`panel-r`) and SVG ids (`relief-curve`/`relief-diagram`) are consistent across Tasks 3–4. Helper reuse verified against source: `setStrip`/`stat` (lines 611–618), `chart` (line 621), `.strip`/`.sheet`/`.cap`/`.grid2` markup (runoff tab, lines 141–158).
