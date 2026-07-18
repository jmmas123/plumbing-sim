# SWMM Python — Verified API Reference (warehouse roof drainage)

Self-contained build reference. Every claim tagged:
**[RUN]** = I executed it and observed the output · **[DOCS]** = manual/code/table citation, not executed here.

Test bed: macOS 26.5.1 **arm64**, Python 3.12.9. Scratchpad: `/private/tmp/claude-501/-Users-jm-Coding-Python-plumbing-sim/1afd1154-127a-4548-8f97-0eb0a2868c6b/scratchpad/`

---

## 1. Versions & install

| package | version tested | role |
|---|---|---|
| `swmm-api` | **0.4.74** | build/edit `.inp`, read `.rpt`/`.out`, batch run |
| `pyswmm` | **2.1.0** | run + step-by-step control, live node/link state |
| `swmm-toolkit` | **0.17.0** | native engine (pulled in by pyswmm) |
| `swmmio` | 0.8.2 | **not recommended — skip** (see below) |
| pandas / numpy | 3.0.3 / 2.5.1 | — |
| **SWMM engine** | **5.2.4** (int `52004`) | `solver.swmm_version_info()` |

```bash
uv pip install swmm-api pyswmm        # do NOT add swmmio
```

**Engine binary: ships natively for macOS arm64. [RUN]** `swmm-toolkit` bundles `libswmm5.dylib` as Mach-O **arm64**. No separate EPA install, no Rosetta, no `swmm5` on PATH.

### 🚨 BLOCKER — pyswmm is broken out-of-the-box on macOS arm64 [RUN]

Reproduced on a clean `--no-cache` venv: **`import pyswmm` is SIGKILLed instantly** (uncatchable; faulthandler can't trace it; disabling sandbox doesn't help). Crash report:

```
"signal": "SIGKILL (Code Signature Invalid)"
"termination": {"namespace": "CODESIGNING", "indicator": "Invalid Page"}
```

Cause: in the **swmm-toolkit 0.17.0** arm64 wheel, `libomp.dylib` and `libswmm-output.dylib` fail `codesign -v` ("code or signature have been modified") — delocate rewrote install names after signing. `libswmm5.dylib` links `@loader_path/libomp.dylib`, so loading it trips the invalid page.

Two verified fixes — **pick one, it is mandatory**:

```bash
# A) re-adhoc-sign  [RUN: import OK, engine 5.2.4]  -- must re-run on every fresh venv/CI job
codesign --force --sign - .venv/lib/python3.12/site-packages/swmm/toolkit/*.dylib

# B) pin last good release  [RUN: import OK, engine 5.2.4]  -- declarative, put in pyproject.toml
#    0.16.0 statically links (_solver.cpython-312-darwin.so, no loose dylibs)
uv pip install 'swmm-toolkit==0.16.0'
```
0.17.0 switched to abi3 wheels + external dylibs; that's the regression. **B is preferred** (survives CI), but needs a wheel matching your exact Python version.

### swmmio: skip it [RUN]
`swmmio>=0.8.3` pins `pyswmm<2.0` **and** `numpy<2.0` — installing `swmmio==0.8.5` **silently downgrades pyswmm 2.1.0 → 1.5.1** and numpy → 1.26.4. It's also redundant: swmm-api covers `.inp`+`.rpt`+`.out` with better column names (`Total_Flood_Volume_10^6 ltr` vs swmmio's unitless `TotalFloodVol`).

---

## 2. Allowed APIs

```python
from swmm_api import SwmmInput, SwmmReport, SwmmOutput, swmm5_run, read_inp_file
from swmm_api.input_file import sections as sec
from swmm_api.input_file.section_labels import OPTIONS, REPORT, JUNCTIONS, CONDUITS  # ...
from pyswmm import Simulation, Nodes, Links, Subcatchments, SystemStats
```

### 2.1 Constructors — exact signatures (`self` stripped) [RUN — introspected + executed]

```python
Junction(name, elevation, depth_max=0, depth_init=0, depth_surcharge=0, area_ponded=0)
Outfall(name, elevation, kind, *args, data=nan, has_flap_gate=False, route_to=nan)
Storage(name, elevation, depth_max, depth_init, kind, *args, data=None,
        depth_surcharge=0.0, frac_evaporation=0.0, suction_head=nan,
        hydraulic_conductivity=nan, moisture_deficit_init=nan)
Divider(name, elevation, link, kind, *args, data=None, depth_max=0, depth_init=0,
        depth_surcharge=0, area_ponded=0)
Conduit(name, from_node, to_node, length, roughness,
        offset_upstream=0, offset_downstream=0, flow_initial=0, flow_max=nan)
Weir(name, from_node, to_node, form, height_crest, discharge_coefficient,
     has_flap_gate=False, n_end_contractions=0, discharge_coefficient_end=0,
     can_surcharge=True, road_width=nan, road_surface=nan, coefficient_curve=nan)
Orifice(name, from_node, to_node, orientation, offset, discharge_coefficient,
        has_flap_gate=False, hours_to_open=0)
Outlet(name, from_node, to_node, offset, curve_type, *args,
       curve_description=None, has_flap_gate=False)
Pump(name, from_node, to_node, curve_name, status='ON', depth_on=0, depth_off=0)
CrossSection(link, shape, height=0, parameter_2=0, parameter_3=0, parameter_4=0,
             n_barrels=1, culvert=nan, transect=None, curve_name=None, street=None)
SubCatchment(name, rain_gage, outlet, area, imperviousness, width, slope,
             curb_length=0, snow_pack=nan)
SubArea(subcatchment, n_imperv, n_perv, storage_imperv, storage_perv, pct_zero,
        route_to='OUTLET', pct_routed=100)
InfiltrationHorton(subcatchment, rate_max, rate_min, decay, time_dry, volume_max, kind=None)
RainGage(name, form, interval, SCF, source, *args,
         timeseries=nan, filename=nan, station=nan, units=nan)
TimeseriesData(name, data)          # data = [("MM/DD/YYYY HH:MM", value), ...]
TimeseriesFile(name, filename, kind='FILE')
Loss(link, entrance=0, exit=0, average=0, has_flap_gate=False, seepage_rate=0)
Inflow(node, constituent='FLOW', time_series=None, kind='FLOW',
       mass_unit_factor=1.0, scale_factor=1.0, base_value=0.0, pattern=nan)
Curve(name, kind, points)
Coordinate(node, x, y)
Polygon(subcatchment, polygon)
Vertices(link, vertices)
Tag(kind, name, tag, *tags)
```

### 2.2 Enums [RUN]
```python
Outfall.TYPES         FREE FIXED NORMAL TIDAL TIMESERIES
Storage.TYPES         FUNCTIONAL TABULAR          Storage.SHAPES  CYLINDRICAL CONICAL PARABOLOID PYRAMIDAL
Divider.TYPES         CUTOFF OVERFLOW TABULAR WEIR
Weir.FORMS            TRANSVERSE SIDEFLOW V_NOTCH('V-NOTCH') TRAPEZOIDAL ROADWAY
Orifice.ORIENTATION   BOTTOM SIDE
CrossSection.SHAPES   CIRCULAR RECT_OPEN RECT_CLOSED TRAPEZOIDAL TRIANGULAR PARABOLIC
                      FILLED_CIRCULAR FORCE_MAIN EGG HORSESHOE IRREGULAR STREET ... (25 total)
```

### 2.3 Build / write [RUN]
`SwmmInput()` is **dict-like**:
```python
inp = SwmmInput()
inp[OPTIONS] = sec.OptionSection(); inp[OPTIONS]["FLOW_UNITS"] = "LPS"
inp.add_obj(obj); inp.add_multiple(*objs)
inp.write_file("m.inp")        # also: inp.to_string(), read_inp_file("m.inp")
```
`OptionSection` supports **both** `inp[OPTIONS]["KEY"]=v` and typed setters (`set_flow_routing`, `set_allow_ponding`, `set_min_surfarea`, `set_variable_step`, `set_lengthening_step`, `set_head_tolerance`, `set_simulation_duration`, …). Also `.is_metric()` / `.is_imperial()`.

### 2.4 Run [RUN]
```python
# batch (no step control) — verified identical results to pyswmm
swmm5_run("m.inp", fn_rpt="m.rpt", fn_out="m.out")

# step-by-step
with Simulation("m.inp") as sim:
    sim.engine_version   # '5.2.4'
    sim.flow_units       # 'LPS'
    sim.system_units     # 'SI'
    for step in sim: ...
    sim.flow_routing_error; sim.runoff_error   # % continuity
```

### 2.5 Read results [RUN]
```python
# live, inside the loop
node.depth  node.head  node.flooding  node.total_inflow  node.volume  node.ponding_area (get/SET)
link.flow   link.depth link.velocity  link.froude       link.capacity
sub.runoff  sub.rainfall

# cumulative — ONLY valid AFTER the loop completes
node.statistics['flooding_volume']    # m3 (SI)
node.statistics[...] -> keys: average_depth max_depth max_depth_date peak_total_inflow
    max_inflow_date peak_lateral_inflowrate peak_flooding_rate max_flooding_date
    max_ponded_volume max_report_depth courant_crit_duration flooding_duration
    surcharge_duration lateral_infow_vol  flooding_volume        # NOTE the typo, see §3
SystemStats(sim).routing_stats['flooding']   # system total
SwmmReport("m.rpt").node_flooding_summary    # DataFrame, units in column names
SwmmOutput("m.out").to_frame()               # MultiIndex (kind, name, variable)
#   node vars: depth head volume lateral_inflow total_inflow flooding
#   link vars: flow depth velocity volume capacity
```
`node.flooding` = instantaneous **rate**. Cumulative volume is **only** via `.statistics`.

**Units [RUN]:** FLOW_UNITS drives the whole system. `CFS/GPM/MGD` → US; `CMS/LPS/MLD` → SI. In SI: lengths/elevations **m**, xsection dims **m** (not mm!), subcatchment area **ha**, rainfall **mm/hr**, depression storage **mm**, `statistics['flooding_volume']` **m³**. RPT reports flood volume in **10⁶ L** (verified: 99.219 m³ ↔ RPT `0.099`).

---

## 3. Anti-patterns — all [RUN]-verified

1. **`Outfall`/`Storage`/`Divider`: passing `data` POSITIONALLY silently discards every trailing keyword.** Source does `if args: ... else: <apply kwargs>` — the kwargs branch is never reached.
   ```python
   sec.Outfall('O1', 5.0, 'FIXED', 3.0, has_flap_gate=True)   # -> has_flap_gate=False  SILENTLY WRONG
   sec.Outfall('O1', 5.0, 'FIXED', data=3.0, has_flap_gate=True)   # correct
   sec.Divider('D',10,'L','CUTOFF', 0.5, depth_max=2)   # -> depth_max=0.0  SILENTLY WRONG
   ```
   **Rule: always pass `data=` as a keyword.**
2. **`data=0.0` becomes `nan`** — source does `self.data = data or np.nan` (falsy trap).
3. **`node.total_flooding` / `.flooding_volume` / `.flood_volume` DO NOT EXIST** (AttributeError). Use `.flooding` (rate) + `.statistics['flooding_volume']` (m³).
4. **`solver.version()` does not exist** → `solver.swmm_version_info()`.
5. **`swmm_api.run_swmm` is a MODULE, not a function** (same for `.run_swmm_toolkit`) → use `swmm5_run(...)`.
6. **`SwmmInput.DIVIDERS` attribute does not exist** (every other section has one) → `inp['DIVIDERS']`. `add_obj(Divider(...))` works fine.
7. **swmm-api does NOT validate OPTIONS keys.** `ROUTING_MODEL`, `TOTALLY_MADE_UP`, `FLOW_ROUTNIG` all written silently. The correct key is **`FLOW_ROUTING`**.
   → **the `roof_badkey.inp` lesson:** the engine *does* catch it, but the Python exception is only generic `ERROR 200: one or more errors in input file`. The actionable message — `ERROR 205: invalid keyword ROUTING_MODEL at line 4 of [OPTION] section` — exists **only in the .rpt**. And `SwmmReport.get_errors()` **returns `{}`** on such a report (parser finds only 2 parts). **Grep the raw .rpt on failure.**
8. **pyswmm stats key is misspelled: `lateral_infow_vol`** (missing "l"). Spell it wrong or KeyError.
9. **Rain gage `interval` must match timeseries spacing** → else `ERROR 159: recording interval greater than time series interval`.
10. **`node.statistics` is meaningless until the step loop finishes.**
11. **`.inp` xsection `height` is metres in SI** — GUIs *display* mm/in; the file does not.

---

## 4. THE DOWNSPOUT RULE — never a steep conduit

### Why [RUN]
Ref Manual Vol. II (EPA/600/R-17/111) §2.1.5 p.33: conduit `length` is the **HYPOTENUSE** — `Δx = √(L² − Δy²)`, `S₀ = Δy/Δx`. Verified against SWMM's own reported slope to 4 dp:

| length | drop | predicted `Δy/√(L²−Δy²)` | SWMM reported |
|---|---|---|---|
| 10.0 | 5.0 | 0.5774 | **57.7350 %** ✓ |
| 5.05 | 5.0 | 7.0535 | **705.3456 %** ✓ |
| 5.0 | 5.0 | degenerate (Δx=0) | **100.0000 %** + `WARNING 08: elevation drop exceeds length` |

A near-vertical downspout therefore gets a **705% slope**, not 99%. Since Manning Q ∝ √S₀, capacity explodes. Measured 4″ downspout as a conduit: **69.10 L/s**, 100% supercritical, 49% normal-flow-limited (Ref Vol II §3.3.4 pp.51–52 Eq. 3-23 normal-flow limiter). My independent full-bore Manning check (D=0.1016, n=0.011, S=1.0) = **63.7 L/s** → confirms SWMM is just applying Manning.

### The real capacity [DOCS]
| source | 4″ leader | = L/s | SWMM 69.10 is |
|---|---|---|---|
| **IPC Table 1106.3** (Vertical Leader Sizing) | 192 gpm | **12.11** | **5.7×** over |
| **UPC 2006 Table 11-2** (via Jay R. Smith Mfg.) | 144 gpm | **9.08** | **7.6×** over |

**SWMM overestimates a 4″ vertical downspout by ~6–8×.** Root cause is a *physical-model mismatch, not a bug*: the UPC footnote states leader ratings assume flow **"7/24 full"** — a thin annular sheet with air entrainment — while Manning assumes full-bore open-channel flow. Parameter tuning cannot fix this.

### The idiom: ORIFICE — worked spec [RUN]
EPA's own Rooftop Disconnection LID (User's Manual v5.2 pp.294–295) models gutters+downspouts as `q = C·hⁿ` with *"n would be 0.5 (making the drain act like an orifice)"*. Ref Vol II p.107: *"A riser pipe or inlet box … can be modeled as a bottom orifice with a vertical offset."*

**Verified: SWMM's bottom orifice reproduces `Q = Cd·A·√(2gh)` exactly**, and with `Cd=0.65, D=0.1016` it lands on the code ratings with no fudging:

| head h | SWMM measured Q | vs code |
|---|---|---|
| 0.05 m | 5.22 L/s | |
| 0.10 m | 7.38 L/s | typical roof-drain design head |
| **0.15 m** | **9.04 L/s** | ≈ **UPC 9.08** ✓ |
| 0.20 m | 10.44 L/s | |
| **0.269 m** | **12.11 L/s** | = **IPC 12.11** (exact) ✓ |

**Use this. Cd=0.65, CIRCULAR, height=0.1016 needs no calibration** — it is self-limiting and conservative at realistic gutter heads.

```python
inp.add_obj(sec.Orifice("DS_1", from_node="J_GUT", to_node="J_BASE",
                        orientation=sec.Orifice.ORIENTATION.BOTTOM,
                        offset=0.0, discharge_coefficient=0.65))
inp.add_obj(sec.CrossSection("DS_1", sec.CrossSection.SHAPES.CIRCULAR, height=0.1016))
```
```ini
[ORIFICES]
;;Name   From     To       Type    Offset  Qcoeff  Gated  CloseTime
DS_1     J_GUT    J_BASE   BOTTOM  0       0.65    NO     0
[XSECTIONS]
DS_1     CIRCULAR  0.1016  0  0  0  1
```
Orifice link needs **no length/roughness** — it is a head-discharge control, not a routed pipe. Requires **DYNWAVE**.

---

## 5. OVERFLOW / RELIEF BRANCH — verdict

### ⛔ DIVIDER is disqualified [RUN + DOCS]
User's Manual v5.2 §3.2.5 **p.54**: *"Flow dividers are only active under Steady Flow and Kinematic Wave routing and are treated as simple junctions under Dynamic Wave routing."*

Confirmed empirically (50 LPS in, CUTOFF set to divert everything above 20 LPS):

| routing | C_MAIN | C_RELIEF | RPT warning |
|---|---|---|---|
| KINWAVE | **20.00** | **30.00** ✓ honoured | none |
| DYNWAVE | 31.84 | 31.84 ✗ **ignored** | **NONE** |

**Silent failure** — and the RPT *still labels the node `DIVIDER`*, which makes it doubly deceptive. Since we require DYNWAVE (§7), **never use DIVIDER.**

### ✅ Both working idioms [RUN]
Relief crest/offset set 0.50 m above the split-node invert; ramped inflow. Both stayed dry below threshold and activated correctly:

| idiom | first flows at | verdict |
|---|---|---|
| offset conduit (`offset_upstream=0.5`) | 0.504 m | ✓ correct |
| WEIR (`height_crest=0.5`) | 0.501 m | ✓ correct, discharges more freely at low head |

**Recommendation — pick by physical form:**
- **Relief pipe / secondary drain that daylights → OFFSET CONDUIT → `Outfall(kind=FREE)`.** ← *use this for a piped relief branch.* It is a real pipe with real length/roughness/diameter, so it routes and can surcharge like one.
- **Scupper / opening in a parapet → WEIR.** It physically *is* a weir; don't model an opening as a pipe.

**Winning snippet — piped relief that daylights:**
```python
inp[OPTIONS]["LINK_OFFSETS"] = "DEPTH"       # offsets = depth above node invert
inp.add_obj(sec.Conduit("C_RELIEF", from_node="J_SPLIT", to_node="O_RELIEF",
                        length=20.0, roughness=0.011,
                        offset_upstream=0.5))          # <-- activates only above 0.5 m
inp.add_obj(sec.CrossSection("C_RELIEF", sec.CrossSection.SHAPES.CIRCULAR, height=0.15))
inp.add_obj(sec.Outfall("O_RELIEF", elevation=9.5, kind=sec.Outfall.TYPES.FREE))
```
Emits exactly (verified — note swmm-api omits the trailing `MaxFlow` field when it is `nan`):
```ini
[CONDUITS]
;;Name    From     To        Length  Rough  InOffset  OutOffset  InitFlow
C_RELIEF  J_SPLIT  O_RELIEF  20      0.011  0.5       0          0
[XSECTIONS]
C_RELIEF  CIRCULAR  0.15  0  0  0  1
[OUTFALLS]
O_RELIEF  9.5  FREE  NO
```

### DYNWAVE caveats
- Conduit **offsets are IGNORED under KINWAVE** [DOCS: Ref Vol II Table 2-1] — the relief would run wet from 0 m. DYNWAVE is mandatory.
- A standalone **weir/orifice not on a storage node only works under DYNWAVE** [DOCS].
- **Minor losses are DYNWAVE-only** [DOCS: UM v5.2 p.382].
- `LINK_OFFSETS=DEPTH` vs `ELEVATION` changes the meaning of `offset_upstream`. Set it explicitly.

---

## 6. PONDING vs FLOODING — reporting rule

### The no-op gate [RUN + code]
Engine source `dynwave.c` / `flowrout.c`: `canPond = (AllowPonding && Node[i].pondedArea > 0.0);` — **both** required. Verified end-to-end:

| config | Node Flooding Summary vol | max ponded depth | continuity **Flooding Loss** |
|---|---|---|---|
| `ALLOW_PONDING=NO`, area=0 | 0.120 | 0.00 m | **0.121** |
| `ALLOW_PONDING=YES`, area=0 | 0.120 | 0.00 m | **0.121** ← **identical: no-op** |
| `ALLOW_PONDING=YES`, area=50 | 0.111 | 1.07 m | **0.038** |

**`ALLOW_PONDING YES` with `area_ponded=0` does nothing.** Set `Junction(..., area_ponded=X)` too, or don't bother.

### ⚠️ The trap [RUN]
**The Node Flooding Summary does NOT tell you what left the system.** With ponding active it still reports **0.111** (10⁶ L) of "flooding" while only **0.038 actually left** — **~66% of reported flooding was recovered, not lost.** Sizing an overflow off "Total Flood Volume" overstates real loss by ~3×.

RPT states the definition verbatim: *"Flooding refers to all water that overflows a node, whether it ponds or not."*

**Read `Flooding Loss` from Flow Routing Continuity, not Total Flood Volume.** swmm-api does not expose it as a clean field — regex the RPT [RUN]:
```python
import re
txt = open("m.rpt").read()
m = re.search(r"Flooding Loss \.+\s+\S+\s+(\S+)", txt)   # groups: (hectare-m, 10^6 ltr)
flooding_loss_10e6_L = float(m.group(1))                 # -> 0.038

# cross-checks
from swmm_api import SwmmReport
SwmmReport("m.rpt").flow_routing_continuity     # dict form of the same table
# and in pyswmm: SystemStats(sim).routing_stats['flooding']  (system total, m3)
```

---

## 7. Required OPTIONS block (copy-ready)

**DYNWAVE is mandatory** — it is the only routing method that captures surcharge, reverse flow, backwater, and looped/split layouts. [DOCS: UM — STEADY & KINWAVE "cannot account for backwater effects, entrance/exit losses, flow reversal, or pressurized flow"; engine `flowrout.c: validateTreeLayout()` *rejects* non-dendritic layouts under STEADY/KINWAVE.]

```python
o = sec.OptionSection(); inp[OPTIONS] = o
o["FLOW_UNITS"]          = "LPS"        # CHANGED from CFS -> SI system (m, ha, mm/hr, m3)
o["FLOW_ROUTING"]        = "DYNWAVE"    # CHANGED. required. NOT the key "ROUTING_MODEL"
o["LINK_OFFSETS"]        = "DEPTH"      # CHANGED. offsets = depth above invert (relief branch)
o["INFILTRATION"]        = "HORTON"
o["START_DATE"]="01/01/2024"; o["START_TIME"]="00:00:00"
o["END_DATE"]  ="01/01/2024"; o["END_TIME"]  ="02:00:00"
o["REPORT_STEP"]         = "00:01:00"
o["WET_STEP"]            = "00:00:30"
o["ROUTING_STEP"]        = 1            # CHANGED from 20s. small pipes -> Courant
o["VARIABLE_STEP"]       = 0.75         # default (valid range 0-2, NOT 0-1)
o["LENGTHENING_STEP"]    = 0            # default (off)
o["MIN_SURFAREA"]        = 1.167        # default 12.566 ft2 = 1.1677 m2
o["HEAD_TOLERANCE"]      = 0.0015       # default 0.005 ft = 0.0015 m
o["MAX_TRIALS"]          = 8            # default
o["INERTIAL_DAMPING"]    = "PARTIAL"    # default
o["NORMAL_FLOW_LIMITED"] = "BOTH"       # default
o["ALLOW_PONDING"]       = "NO"         # NO-OP unless node area_ponded > 0 (see §6)
o["SKIP_STEADY_STATE"]   = "NO"         # default
```

**Verified 5.2 defaults** [DOCS: engine source `project.c setDefaults()` / `dynwave.c`, VERSION 52004]: `ROUTING_STEP` 20 s · `MIN_ROUTE_STEP` 0.5 s · `VARIABLE_STEP` 0.75 (range **0–2**) · `LENGTHENING_STEP` 0 · `MIN_SURFAREA` **12.566 ft² = 1.1677 m²** (`dynwave.c: DEFAULT_SURFAREA = 12.566; // ~4 ft diam.`) · `HEAD_TOLERANCE` 0.005 ft · `MAX_TRIALS` 8 · `INERTIAL_DAMPING` PARTIAL · `NORMAL_FLOW_LIMITED` BOTH · `SURCHARGE_METHOD` EXTRAN (SLOT = 5.2 Preissmann, attaches at `SLOT_CROWN_CUTOFF=0.985257`) · `ALLOW_PONDING` NO · `THREADS` 1.

**Why changed:** `ROUTING_STEP 1` — default 20 s badly violates Courant on plumbing-scale conduits (metres, not hundreds of metres). `LINK_OFFSETS=DEPTH` — makes the relief offset readable. Consider `SURCHARGE_METHOD=SLOT` if EXTRAN shows continuity error; test both, don't assume [DOCS: practitioner guidance, not EPA-endorsed].

**Minor losses** `[LOSSES]` format `Conduit Kentry Kexit Kavg (Flap Seepage)`; `Seepage` is **new in 5.2**. **DYNWAVE-only** [DOCS: UM v5.2 p.382 *"Minor losses are only computed for the Dynamic Wave flow routing option"*]. SWMM publishes **no** K table — it cites Frost 2006 (JWMM R225-23): sharp entrance ≈0.5, exit ≈1.0, 90° bend 0.07–0.23. **Diameter transition (8″→10″): no dedicated feature** — a conduit has one fixed section. Split into two conduits at a junction and apply the coefficient on **one side only** (do not double-count) [DOCS: Frost 2006 §23.3 + openswmm.org; practitioner convention, manual is silent].

---

## 8. Minimal end-to-end snippet [RUN]

Roof subcatchment → gutter → 4″ downspout → junction → outfall. Builds, runs, reads flooding.

```python
from swmm_api import SwmmInput
from swmm_api.input_file import sections as sec
from swmm_api.input_file.section_labels import OPTIONS, REPORT
from pyswmm import Simulation, Nodes, Links, Subcatchments

INP = "minimal.inp"
inp = SwmmInput()
o = sec.OptionSection(); inp[OPTIONS] = o
o["FLOW_UNITS"]="LPS"; o["INFILTRATION"]="HORTON"; o["FLOW_ROUTING"]="DYNWAVE"
o["LINK_OFFSETS"]="DEPTH"
o["START_DATE"]="01/01/2024"; o["START_TIME"]="00:00:00"
o["END_DATE"]="01/01/2024";   o["END_TIME"]="02:00:00"
o["REPORT_STEP"]="00:01:00"; o["WET_STEP"]="00:00:30"; o["ROUTING_STEP"]=1
o["INERTIAL_DAMPING"]="PARTIAL"; o["NORMAL_FLOW_LIMITED"]="BOTH"
o["VARIABLE_STEP"]=0.75; o["LENGTHENING_STEP"]=0; o["MIN_SURFAREA"]=1.167
o["MAX_TRIALS"]=8; o["HEAD_TOLERANCE"]=0.0015; o["ALLOW_PONDING"]="NO"

inp[REPORT] = sec.ReportSection()
inp[REPORT]["NODES"]="ALL"; inp[REPORT]["LINKS"]="ALL"; inp[REPORT]["SUBCATCHMENTS"]="ALL"

# gage interval MUST match timeseries spacing else SWMM ERROR 159
inp.add_obj(sec.RainGage("RG1", form="INTENSITY", interval="0:05", SCF=1.0,
                         source="TIMESERIES", timeseries="TS_STORM"))
rain = [(f"01/01/2024 {m//60:02d}:{m%60:02d}", 100.0 if m < 60 else 0.0)
        for m in range(0, 125, 5)]                 # 100 mm/hr for 1 h
inp.add_obj(sec.TimeseriesData("TS_STORM", rain))

# ROOF: 2000 m2 = 0.2 ha, 100% impervious, flow length 20 m => width = 100 m
inp.add_obj(sec.SubCatchment("S_ROOF", rain_gage="RG1", outlet="J_GUT_IN",
                             area=0.2, imperviousness=100, width=100, slope=2.0))
inp.add_obj(sec.SubArea("S_ROOF", n_imperv=0.012, n_perv=0.1,
                        storage_imperv=0.5, storage_perv=2.0,   # mm
                        pct_zero=100, route_to="OUTLET"))
inp.add_obj(sec.InfiltrationHorton("S_ROOF", rate_max=76.2, rate_min=3.3,
                                   decay=4.14, time_dry=7, volume_max=0))

inp.add_obj(sec.Junction("J_GUT_IN", elevation=6.00, depth_max=0.15))
inp.add_obj(sec.Junction("J_DS_TOP", elevation=5.95, depth_max=0.15))
inp.add_obj(sec.Junction("J_BASE",   elevation=0.20, depth_max=1.00))
inp.add_obj(sec.Outfall("OUT1", elevation=0.00, kind=sec.Outfall.TYPES.FREE))

inp.add_obj(sec.Conduit("C_GUTTER",    from_node="J_GUT_IN", to_node="J_DS_TOP",
                        length=20.0, roughness=0.012))
inp.add_obj(sec.Conduit("C_DOWNSPOUT", from_node="J_DS_TOP", to_node="J_BASE",
                        length=5.75, roughness=0.011))   # <-- see §4: prefer an ORIFICE
inp.add_obj(sec.Conduit("C_LATERAL",   from_node="J_BASE", to_node="OUT1",
                        length=10.0, roughness=0.011))
inp.add_obj(sec.CrossSection("C_GUTTER", sec.CrossSection.SHAPES.RECT_OPEN,
                             height=0.15, parameter_2=0.20))
inp.add_obj(sec.CrossSection("C_DOWNSPOUT", sec.CrossSection.SHAPES.CIRCULAR, height=0.1016))
inp.add_obj(sec.CrossSection("C_LATERAL",   sec.CrossSection.SHAPES.CIRCULAR, height=0.1016))
inp.add_obj(sec.Loss("C_DOWNSPOUT", entrance=0.5, exit=1.0, average=0.0))
for n, x, y in [("J_GUT_IN",0,100), ("J_DS_TOP",20,100), ("J_BASE",20,0), ("OUT1",30,0)]:
    inp.add_obj(sec.Coordinate(n, x, y))
inp.write_file(INP)

with Simulation(INP) as sim:
    print(f"engine {sim.engine_version} | units {sim.flow_units} / {sim.system_units}")
    nodes = {n.nodeid: n for n in Nodes(sim)}
    roof, ds = Subcatchments(sim)["S_ROOF"], Links(sim)["C_DOWNSPOUT"]
    peak_runoff = peak_ds = 0.0
    for _ in sim:
        peak_runoff = max(peak_runoff, roof.runoff); peak_ds = max(peak_ds, ds.flow)
    print(f"peak roof runoff     = {peak_runoff:6.2f} LPS")
    print(f"peak downspout flow  = {peak_ds:6.2f} LPS")
    for name, n in nodes.items():
        print(f"   {name:9s} flood_volume = {n.statistics['flooding_volume']:8.2f} m3")
    print(f"continuity: routing {sim.flow_routing_error:.3f} % | runoff {sim.runoff_error:.3f} %")
```

**Real output:**
```
engine 5.2.4 | units LPS / SI
peak roof runoff     =  55.56 LPS
peak downspout flow  =  27.07 LPS
   J_GUT_IN  flood_volume =    99.22 m3
   J_DS_TOP  flood_volume =     0.00 m3
   J_BASE    flood_volume =    21.40 m3
   OUT1      flood_volume =     0.00 m3
continuity: routing 0.000 % | runoff 0.000 %
```
Sanity-checked: wet-weather inflow 200 m³ = hand-calc (100 mm/hr × 1 h × 2000 m²); 99.22 + 21.40 = 120.6 = `SystemStats.routing_stats['flooding']`; 0% continuity error. Note this demo uses a *conduit* downspout (27 LPS) — **swap it for the §4 orifice for real work.**

---

## 9. Open questions / judgment calls

| topic | status |
|---|---|
| **Roof Manning's n (`n_imperv`)** | **No roof row exists in any EPA table.** UM v5.2 App. A.6 p.211: smooth asphalt **0.011**, smooth concrete **0.012** (McCuen et al. 1996). Ref Vol I Table 3-5 p.75 gives three disparate sources and the manual itself concedes *"no consensus … common to fix n and calibrate with width."* Practitioners use **0.011–0.015** for metal/membrane roofs. **Judgment call — 0.012 used above.** |
| **Roof D-Store (`storage_imperv`)** | **No roof split-out.** UM App. A.5 p.210: impervious surfaces **0.05–0.10 in** (ASCE 1992) = 1.3–2.5 mm. Practitioners (Dickinson/Brooker, openswmm.org) recommend nonzero **~0.5–2 mm** over 0. 0 is defensible for design-storm peaks, not water balance. **0.5 mm used above.** |
| **`%Zero-Imperv`** | GUI default 25% is generic, **not** roof-specific. Pick **either** `pct_zero=100` **or** a D-Store depth — not both. |
| **Subcatchment `width`** | UM p.226 fn.1 — explicitly a **calibration parameter** (area / overland flow length). Not a measured quantity. |
| **Gutter modelling** | **No manual guidance.** For a simple roof→downspout run, standard practice is to **lump the gutter into the subcatchment overland path**. Explicit RECT_OPEN conduits are for street gutters or when gutter storage/overtopping matters — which for a warehouse parapet gutter it may. **Unresolved; decide per geometry.** |
| **Sourcing note** | There is **no distinct "SWMM 5.2 Reference Manual"** — Vol. II in circulation is **EPA/600/R-17/111 (May 2017)**, written for 5.1. Hydraulics content unchanged for 5.2; only the *User's Manual* (EPA/600/R-22/030) and engine source carry 5.2 features. |
| **Still unverified** | Whether `[LOSSES] Seepage` is DYNWAVE-gated. Whether ponded-area and surcharge-depth can coexist at a junction (secondary-source claim only). No EPA-endorsed non-zero `LENGTHENING_STEP`. STEADY's exclusion from minor-loss computation is structurally inferred, not quoted. The "1–20 s routing step" range is CHI practitioner guidance, not an EPA mandate. IPC/UPC leader tables are **[DOCS]** — I verified the gpm→L/s arithmetic but did not read the printed code books. |
| **Not investigated** | The two AutoCAD files in the project dir (`ARQUITECTURA BODEGA TRIPLE.dwg`, `HIDRAULICOS AP AN ALL BODEGA TRIPLE 2020 15 FEBRERO 2021.dwg`) — presumably the roof/hydraulic geometry source. No DWG reader installed. |
