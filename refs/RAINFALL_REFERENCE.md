# RAINFALL REFERENCE — SAN ANDRES OFIBODEGAS / BODEGA TRIPLE (MEROPIS S.A. de C.V.)

**Site:** Km 34 Carretera San Salvador–Santa Ana, Cantón San Andrés, Ciudad Arce, La Libertad, El Salvador
**Coordinates:** 13.815527, -89.408015 · **Elevation: 461.5–463.5 msnm** (from drawings)

> **Provenance convention used throughout.**
> **[SOURCED]** = read verbatim from a cited document.
> **[DERIVED]** = computed by me *from* sourced values (method stated).
> **[ESTIMATE]** = judgement. **There are no [ESTIMATE] coefficients in this file.**
> No IDF coefficient in this document was invented. Every one is traceable to a citation below.

---

## 0. HEADLINE ANSWER (read this first)

1. **There is NO published IDF curve for the San Andrés gauge.** The station is real, active, and
   essentially on the site — but it is a **daily-read** climatological station, not a pluviograph.
   This is the single most important finding and it is a **negative**. Details in §1.
2. **No global/gridded product can supply the 5-min intensity this site needs.** GSDR-IDF (the
   lead chased) bottoms out at **1 hour** and has **zero Central America gauges** — nearest is
   **1,533 km**, against the authors' own **200 km** transfer limit. Details in §5.
3. **Real, verified Salvadoran IDF equations DO exist** — for stations 19–47 km away. Use them,
   with the short-duration correction in §3.1. Details in §2.
4. **The observed 2024–26 rain near the site was NOT extreme** — max 24-h depth in three seasons
   was **82.5 mm**, ≈ the **2-year** event. If the system overflowed on that, the deficiency is
   capacity or short-duration intensity, not exceptional rainfall. Details in §6. **This is the
   most actionable finding for the model.**

---

## 1. THE SAN ANDRÉS STATION — what actually exists

**[SOURCED]** `L4 SAN ANDRES` is a **live MARN conventional climatological station**, reporting
daily rainfall (21.1 mm on 2026-06-15). Confirmed directly from MARN's own daily report:
`https://srt.ambiente.gob.sv/old/index.php?rutina=ver_diarios&fecha=2026-06-15`
It sits in the **L-series** (La Libertad) alongside Santa Tecla **L-08** and Boquerón **L-18**.
Same portal independently returns `A15 GUIJA` and `S10 A. ILOPANGO`, matching the station indices
printed in the 2004 UCA thesis — which **validates the station-code system** used below.

**[SOURCED — negative] San Andrés is not a pluviograph station.** The Servicio Hidrológico Nacional
supplied sub-daily intensities for exactly **six** stations (Güija, Izalco, Galera, El Papalón,
Santa Cruz Porrillo, Aeropuerto Ilopango — SNET doc00245). **San Andrés is not among them.**
OPAMSS's official IDF station list is a different four (S-10, S-04, L-08, L-18) — **San Andrés is
not among those either.** Two independent lists, neither includes it.

**⇒ CONCLUSION: IDF for San Andrés is NOT OBTAINABLE from any public source.** It is not that I
failed to find it; the evidence indicates the sub-daily record needed to build it was never
published, and the station type suggests it may never have been recorded at sub-daily resolution.

**Corroborating this:** the GSDR global gauge inventory (Lewis et al. 2019, `10.1175/JCLI-D-18-0143.1`,
Tables A1/A2) lists **El Salvador sub-daily data as "Yes (restricted)" → "Included in dataset: No"**.
Salvadoran sub-daily records exist but have never been released. **This makes a direct request to
DGOA-MARN the only real path to site-specific 5-min data.**

### Nearest stations — exact distances **[DERIVED**, haversine from MARN's own WFS coordinates:
`ruraladelante.snet.gob.sv/index.php/lizmap/service/?repository=estaciones&project=estaciones&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=Estaciones&OUTPUTFORMAT=GeoJSON`, 130 stations**]**

| Station | Type | km from site | Elev (m) | IDF available? |
|---|---|---:|---:|---|
| Ciudad Arce | Pluviométrica | **3.55** | — | **No** |
| ENA-SanAndrés / AgrC Zapotitán | Meteorológica | **5.28** | — | **No** |
| Talnique | Hidrológica | 7.59 | — | No |
| Coatepeque | Pluviométrica | 12.65 | — | No |
| **Boquerón (L-18)** | Meteorológica | 17.68 | ~1800¹ | **YES — measured table** |
| **PROCAFE** | Meteorológica | 19.62 | — | **YES — equation** |
| **Izalco (T-3)** | — | **32.60** | **390** | **YES — equation** |
| **Aeropuerto Ilopango (S-10)** | Meteorológica | 33.90 | **615** | **YES — equation, 44-yr** |
| Santa Ana | Meteorológica | 23.99 | — | No |
| **Güija (A-15)** | — | 46.50 | **485** | **YES — equation** |
| Santa Tecla (L-08) | Conventional | ~21¹ | ~920¹ | **YES — measured table** |

¹ **[ESTIMATE]** — elevations/distance for Boquerón, Santa Tecla, PROCAFE are *not* sourced. All
other elevations are **[SOURCED]** verbatim from SNET doc00245 station metadata.

> ⚠ **Coordinate conflict, unresolved:** three sources place "San Andrés" at 0.84 km, ~2 km, and
> 5.28 km from the site. The MARN WFS (5.28 km, ENA-SanAndrés) is the most authoritative. Immaterial
> at IDF scale, but do not quote a precise San Andrés distance.

---

## 2. IDF EQUATIONS — actual coefficients, all verified

### 2.1 The four Salvadoran station equations **[SOURCED]**

**Source:** Carías Juárez, B.E.; Chacón Novoa, E.T.; Martínez Márquez, M.Á. (2004),
*"Validación de Metodologías para el Cálculo de Caudales Máximos en El Salvador"*, Trabajo de
Graduación, Ingeniero Civil, **Universidad Centroamericana "José Simeón Cañas" (UCA)**, Oct 2004.
Archived: `http://web.archive.org/web/20150501044943/http://portafolio.snet.gob.sv:80/digitalizacion/pdf/spa/doc00245/doc00245-seccion%20d.pdf`
(live host `portafolio.snet.gob.sv` is dead/NXDOMAIN — **use the archive.org copy via `curl`;
WebFetch cannot reach archive.org**)

> **PROVENANCE CAVEAT — read before citing.** The **intensities were supplied by the SHN**
> (official), but the **equations are the thesis authors' own fits**. This is a *university thesis*,
> not a MARN publication. Legitimate route to the primary numbers, but not itself an official norm.

Form: **`i = a · T^m / d^n`** — `i` = **mm/h**, `T` = **years**, `d` = **minutes**

| Station | Índice | Lat | Lon | Elev (m) | Record | Equation |
|---|---|---|---|---:|---|---|
| **Izalco** | **T-3** | 13°45.7' | 89°42.3' | **390** | 18 yr (1965-1982) | **`i = 554.63·T^0.274 / d^0.693`** |
| **A. Ilopango** | **S-10** | 13°41.9' | 89°7.1' | **615** | **44 yr (1953-2003)** | **`i = 478.63·T^0.24 / d^0.67`** |
| **Güija** | **A-15** | 14°13.7' | 89°28.7' | **485** | 22 yr (1961-1982) | **`i = 379.31·T^0.275 / d^0.627`** |
| Galera | Z-4 | 14°2.8' | 88°5.2' | 1900 | 11 yr (1973-1983) | `i = 400.87·T^0.24 / d^0.634` |
| El Papalón | M-6 | 13°26.6' | 88°7.4' | 80 | 22 yr (1961-1981) | `i = 537.03·T^0.346 / d^0.7` |
| Sta Cruz Porrillo | V-6 | 13°26.4' | 88°48.2' | 30 | 30 yr (1954-1983) | `i = 549.54·T^0.29 / d^0.66` |

**VERIFICATION [DERIVED]:** the Güija equation reproduces the thesis's own printed Tabla 3.8 to a
**max error of 0.007 mm/h across all 78 cells** → equation form and exponents correctly transcribed. ✓
**Cross-check:** the S-10 coordinates (13.6983, -89.1183) match the MARN WFS Ilopango coordinates
**exactly**. ✓

### 2.2 Procafé equation **[SOURCED]**

**Source:** OPAMSS, *"Guía Técnica para el diseño de SUDS en el AMSS"*, **Módulo 4**, Ecuación 22.1
`https://opamss.org.sv/wp-content/uploads/2021/07/Modulo-4-Diseno-SUB-para-el-AMSS.pdf`
(equation is an embedded image; extracted via pypdf image extraction)

```
I = 10.72738 · T^0.21884 / (D^0.63024 + 1.00332)
I = mm/MIN  (note: mm/min, not mm/h) · T = years · D = minutes
```
**VERIFICATION [DERIVED]:** the guide's own worked example states Tr=5, D=60 → **64.45 mm**.
The equation yields **64.44 mm**. ✓ Fully validated. No period of record is stated in the source.

### 2.3 Measured IDF tables — Santa Tecla & Boquerón **[SOURCED]**

**Source:** Erazo Chica, Adriana María (Ing. MSc.), *"Análisis de lluvias en el Área Metropolitana de
San Salvador para generación de Sistema de Alerta Temprana y para modelación hidrológica e
hidráulica (Informe Preliminar)"*, **SNET / Servicio Hidrológico Nacional, Octubre 2008**.
Archived: `http://web.archive.org/web/20190711175023/http://portafolio.snet.gob.sv:80/digitalizacion/pdf/spa/doc00237/doc00237-contenido.pdf`

**These are MEASURED tables (not fitted equations) — the most trustworthy short-duration data found.**
Tables were embedded images; recovered via image extraction + PDF content-stream position analysis
to establish reading order. **Units: mm/min** — confirmed [DERIVED] by summing the document's own
printed Boquerón Tr=25/120-min hyetograph (≈78 mm) against table value 0.64 × 120 = 76.8 mm. ✓

**Santa Tecla (L-08), 1954–1984 — mm/min**, d = 5,10,15,20,30,45,60,90,120,180,240,360
```
T=2:   2.61 2.13 1.85 1.65 1.35 1.05 0.81 0.60 0.47 0.32 0.25 0.17
T=5:   3.03 2.45 2.16 1.95 1.63 1.28 1.03 0.75 0.58 0.40 0.33 0.23
T=10:  3.26 2.62 2.32 2.10 1.77 1.41 1.17 0.85 0.64 0.44 0.37 0.27
T=15:  3.37 2.71 2.41 2.18 1.84 1.47 1.24 0.90 0.68 0.47 0.39 0.29
T=20:  3.44 2.76 2.46 2.24 1.89 1.51 1.29 0.94 0.71 0.48 0.40 0.30
T=25:  3.49 2.80 2.50 2.27 1.92 1.53 1.33 0.96 0.72 0.50 0.41 0.31
T=50:  3.65 2.92 2.61 2.38 2.02 1.62 1.45 1.05 0.78 0.54 0.44 0.33
T=100: 3.78 3.02 2.71 2.48 2.11 1.69 1.57 1.13 0.84 0.58 0.47 0.35
```
**Boquerón (L-18), 1967–1993 + 2004–2007 — mm/min**, d = 5,10,15,20,30,45,60,90,120,150,180,240,360
```
T=2:   3.11 2.28 1.88 1.70 1.37 1.04 0.85 0.61 0.48 0.39 0.34 0.25 0.19
T=5:   3.69 2.63 2.13 1.97 1.57 1.17 0.96 0.70 0.56 0.47 0.41 0.31 0.25
T=10:  3.99 2.81 2.25 2.11 1.68 1.24 1.02 0.74 0.60 0.51 0.44 0.35 0.28
T=15:  4.14 2.90 2.32 2.18 1.73 1.27 1.05 0.76 0.62 0.53 0.46 0.37 0.29
T=20:  4.24 2.96 2.36 2.23 1.77 1.29 1.07 0.77 0.63 0.54 0.48 0.39 0.30
T=25:  4.31 3.01 2.39 2.26 1.79 1.31 1.08 0.78 0.64 0.55 0.48 0.40 0.31
T=50:  4.52 3.13 2.48 2.36 1.87 1.35 1.12 0.81 0.67 0.58 0.51 0.44 0.33
T=100: 4.71 3.25 2.56 2.45 1.93 1.39 1.16 0.84 0.69 0.61 0.53 0.48 0.34
```
**Multiply by 60 for mm/h. Multiply by d for depth in mm.**
⚠ 2-dp rounding makes cumulative depth slightly non-monotonic (Boquerón T=2: 180 min → 61.2 mm vs
240 min → 60.0 mm). **Enforce monotonic cumulative depth when interpolating.**

### 2.4 Regional cross-check — Guatemala **[SOURCED]**

INSIVUMEH, *"Curvas de Intensidad, Duración y Frecuencia (IDF) para la República de Guatemala"*
`https://insivumeh.gob.gt/wp-content/uploads/2026/03/Curvas-de-Intensidad-Duracion-y-Frecuencia-IDF-para-la-Republica-de-Guatemala.pdf`
Sherman model per IFI/FRIEND convention: **`I(mm/h) = K·Tr^m / (D + B)^n`**, D in min, Tr in yr. 30 stations.

**Asunción Mita** — Jutiapa, Ostúa-Güija basin, **elev 478 m**, 14.33444/-89.7058, **66.0 km** from site:
```
I = 3931 · Tr^0.220 / (D + 26.36)^1.090
```
Nearly identical elevation to the site (461–463 m). Other useful: Esquipulas (1000 m)
`I = 1074·Tr^0.135/(D+16.12)^0.697`; Los Esclavos (737 m) `I = 1933·Tr^0.144/(D+20.56)^0.887`.

---

## 3. COPY-READY INTENSITY TABLES (mm/h) **[DERIVED from the §2 sourced equations]**

### Izalco (T-3) — 390 m, 32.6 km SW — *best elevation analog with a real equation*
| d (min) | T=2 | T=5 | T=10 | T=25 | T=50 | T=100 |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 219.8 | 282.6 | 341.7 | 439.2 | 531.0 | 642.1 |
| 10 | 136.0 | 174.8 | 211.4 | 271.7 | 328.5 | 397.2 |
| 15 | 102.7 | 132.0 | 159.6 | 205.1 | 248.0 | 299.9 |
| 20 | 84.1 | 108.1 | 130.7 | 168.0 | 203.2 | 245.7 |
| 30 | 63.5 | 81.6 | 98.7 | 126.9 | 153.4 | 185.5 |
| 45 | 48.0 | 61.6 | 74.5 | 95.8 | 115.8 | 140.1 |
| 60 | 39.3 | 50.5 | 61.1 | 78.5 | 94.9 | 114.7 |
| 90 | 29.7 | 38.1 | 46.1 | 59.3 | 71.7 | 86.6 |
| 120 | 24.3 | 31.2 | 37.8 | 48.5 | 58.7 | 71.0 |
| 180 | 18.3 | 23.6 | 28.5 | 36.7 | 44.3 | 53.6 |
| 360 | 11.3 | 14.6 | 17.6 | 22.7 | 27.4 | 33.2 |
| 720 † | 7.0 | 9.0 | 10.9 | 14.0 | 17.0 | 20.5 |
| 1440 † | 4.3 | 5.6 | 6.7 | 8.7 | 10.5 | 12.7 |

### Aeropuerto Ilopango (S-10) — 615 m, 33.9 km E — *longest record (44 yr), official OPAMSS station*
| d (min) | T=2 | T=5 | T=10 | T=25 | T=50 | T=100 |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 192.3 | 239.6 | 282.9 | 352.5 | 416.3 | 491.7 |
| 10 | 120.9 | 150.6 | 177.8 | 221.6 | 261.7 | 309.0 |
| 15 | 92.1 | 114.8 | 135.5 | 168.9 | 199.4 | 235.5 |
| 20 | 76.0 | 94.6 | 111.8 | 139.3 | 164.5 | 194.2 |
| 30 | 57.9 | 72.1 | 85.2 | 106.1 | 125.3 | 148.0 |
| 45 | 44.1 | 55.0 | 64.9 | 80.9 | 95.5 | 112.8 |
| 60 | 36.4 | 45.3 | 53.5 | 66.7 | 78.8 | 93.0 |
| 90 | 27.7 | 34.5 | 40.8 | 50.8 | 60.0 | 70.9 |
| 120 | 22.9 | 28.5 | 33.6 | 41.9 | 49.5 | 58.5 |
| 180 | 17.4 | 21.7 | 25.6 | 32.0 | 37.7 | 44.6 |
| 360 | 11.0 | 13.6 | 16.1 | 20.1 | 23.7 | 28.0 |
| 720 † | 6.9 | 8.6 | 10.2 | 12.7 | 15.0 | 17.7 |
| 1440 † | 4.3 | 5.4 | 6.4 | 7.9 | 9.4 | 11.1 |

**† 720 and 1440 min are EXTRAPOLATIONS beyond the 5–360 min fitting range. Flagged, not trusted.**
For 24-h magnitudes prefer GPEX (§6) or the observed record.

### 3.1 ⚠ CRITICAL CORRECTION — the equations over-predict at 5–10 min

**[DERIVED]** Güija (SV, 485 m) and Asunción Mita (GT, 478 m) sit **27.2 km apart**, same basin,
same elevation, fitted independently by **two different national agencies**. They agree within
**10–18% at 15–60 min** — but diverge badly at 5 min (ratio 0.52–0.64).

**Cause:** the Salvadoran UCA-2004 equations are **pure power laws with no `+B` term**, so `i → ∞`
as `d → 0`. Guatemala's Sherman form has `(D + 26.36)`, which correctly flattens at short duration.
Procafé's `c = 1.00332` is so small it behaves like a pure power law too.

**Intensity at d = 5 min, Tr = 25 — all sources:**

| Source | mm/h | Type |
|---|---:|---|
| Izalco eq | **439** | pure power law — **least trustworthy here** |
| Ilopango S-10 eq | 353 | pure power law |
| Procafé eq | 346 | ~pure power law |
| Güija eq | 335 | pure power law |
| **Boquerón** | **259** | **MEASURED TABLE** |
| **Santa Tecla** | **209** | **MEASURED TABLE** |
| **Asunción Mita (GT)** | **187** | Sherman **with** +B |

**The measured tables and the properly-formed Sherman curve converge on ~190–260 mm/h. The fitted
pure power laws give 335–439 — up to ~2× higher.**

> **⇒ RECOMMENDATION: do NOT use the UCA-2004 / Procafé equations below ~10–15 min.**
> **Cap the 5–10 min blocks to the 190–260 mm/h band (Tr=25).** For a warehouse roof
> (Tc ≈ 5–10 min) the 5-min block *dominates* the SWMM peak — so this choice, not the station
> choice, is the largest single lever on the result. Run both bounds as a sensitivity.

---

## 4. REQUIRED RETURN PERIOD — Salvadoran practice **[SOURCED]**

### 4.1 What does NOT apply (verified negatives — saves re-checking)
- **ANDA** *"Normas Técnicas para Abastecimiento de Agua Potable y Alcantarillados de Aguas Negras"*
  (`https://www.anda.gob.sv/wp-content/uploads/2023/08/Normas-Tecnicas-ANDA.pdf`) — **contains NO
  stormwater design content.** Potable water + sanitary sewers only. Grepped for
  pluvial/retorno/intensidad: no design criteria. **Do not cite ANDA for storm drainage.**
- **National Reglamento a la Ley de Urbanismo y Construcción (D-70-91)** — requires aguas lluvias
  drainage but specifies **no return period, no intensity, no design storm.** Every "retorno" hit is
  *retorno de la vía* (cul-de-sac turnaround), not return period.
- **⇒ There is no national Salvadoran technical norm setting a design return period for storm drainage.**

### 4.2 What does apply (the only quantified Salvadoran norm)
**Source (CURRENT, binding):** OPAMSS, *LDOTAMSS y Reglamento*, **Dic 2025**, Art. V.14
`https://opamss.org.sv/wp-content/uploads/2025/12/LDOTAMSS-Y-REGLAMENTO-DIC_-2025.pdf`

| Item | Requirement |
|---|---|
| **Caudal hidrológico** | **Tr ≥ 50 yr** minimum; OPAMSS may require **100 yr** |
| **Colectores de aguas lluvias** | **Tr ≥ 25 yr**, Rational method, **Tc = 5 min** for tragantes |
| Rational method limit | areas **≤ 2.5 km²**; else hydrological modelling |
| Tc for intensity | **TCi = 0.65 · TCc** (≥3 formulas required) |
| **C — Techos (roofs)** | **0.80 / 0.90 / 0.95** (min/recommended/max) |
| C — Industrial >70% impermeable | 0.70 / **0.80** / 0.90 |
| CN — Áreas industriales (72% imp.) | A=81, B=88, C=91, D=93; Pavimento y tejados = **100** |
| Design AMC | **AMC III**; `CN_III = 23·CN_II / (10 + 0.13·CN_II)` |
| SMIH peak reduction | 50–90% vs pre-development |

> ⚠ **JURISDICTION — this is important. [SOURCED]** AMSS is defined as **14 municipalities**:
> Antiguo Cuscatlán, Apopa, Ayutuxtepeque, Cuscatancingo, Delgado, Ilopango, Mejicanos, Nejapa,
> Santa Tecla, San Marcos, San Martín, San Salvador, Soyapango, Tonacatepeque.
> **"Ciudad Arce" appears ZERO times in the entire LDOTAMSS.** **OPAMSS does not legally apply to
> this site.** It is cited as best-documented Salvadoran practice, not as a binding requirement.
> The permitting authority here is **VMVDU**, whose norm sets no return period (§4.1).

> **[SOURCED]** The Dec-2025 reglamento states: *"**Mientras se generan y publican las curvas IDF
> para el AMSS**, en coordinación con el MARN…"* — i.e. **official AMSS IDF curves are still NOT
> published as of Dec 2025.** MARN supplies the data on request. (A peer thread asserted V.14
> "proves MARN already publishes 5-min IDF" — **that overstates it**; the reglamento says the
> opposite. It names the four stations whose data MARN *holds*: S-10, S-04, L-08, L-18.)

**Recommendation for this project [ESTIMATE — engineering judgement, not a citation]:** absent a
binding norm, adopt **Tr = 25 yr for the roof/site collector network** and **Tr = 50 yr for the
outfall / detention check**, mirroring OPAMSS. Defensible because it is the only quantified
Salvadoran criterion and is conservative relative to the (silent) national norm.

---

## 5. DESIGN-STORM HYETOGRAPH — method + justification

### 5.1 This is settled by regulation, not judgement **[SOURCED]**
OPAMSS Reglamento Dic-2025, Art. V.14, verbatim:
> *"se deberá utilizar un **hidrograma de lluvia tipo "Chicago" o de bloques alternativos de 5
> minutos de duración de cada bloque**. La misma unidad de tiempo aplica al análisis en general."*

**⇒ Chicago or alternating-block, 5-minute blocks. NOT SCS Type II.**

### 5.2 Why SCS Type II is wrong for this rain **[SOURCED]**
SNET doc00237 §2, from analysis of **133 real storms**:
> *"generalmente las máximas cantidades de lluvia, sin importar la duración total de la lluvia, se
> presentan **entre los 10 a 20 minutos desde que comienza la lluvia**, o en su defecto entre los
> 20 a 30 minutos."*

Salvadoran convective storms are **front-loaded**. SCS Type II peaks at the **midpoint (r = 0.5)**
and would misplace the peak. **[DERIVED]** from the document's own printed Boquerón Tr=25/120-min
design hyetograph (peak in the 20–30 min block of 120 min) → **r ≈ 0.21**.

Notably, SNET itself used *"método de bloque alterno"* **but rearranged the blocks to the observed
temporal pattern** rather than the symmetric alternating order — i.e. Salvadoran official practice
already rejects a centred peak.

**⇒ RECOMMENDATION: Chicago hyetograph, 5-min blocks, r ≈ 0.21–0.35.** Sensitivity-test r = 0.5
(standard alternating block) as the conservative-timing bound.

### 5.3 Copy-ready design storms **[DERIVED from Izalco eq; see §3.1 caveat on the peak block]**
5-min blocks, r = 0.21. Totals: **Tr=25/60 min = 78.5 mm**; **Tr=25/120 min = 97.1 mm**;
**Tr=50/60 min = 94.9 mm**; **Tr=50/120 min = 117.4 mm**.

SWMM `[TIMESERIES]`, INTENSITY format, INTERVAL 0:05, **mm/h**:
```
;; DS_T25_60min   total 78.5 mm   ** peak block 439 mm/h — see §3.1, cap to ~190-260 **
DS_T25_60min  0:00  36.89
DS_T25_60min  0:05  47.66
DS_T25_60min  0:10  72.02
DS_T25_60min  0:15  439.19   <-- OVER-PREDICTED; substitute 190-260 band
DS_T25_60min  0:20  104.15
DS_T25_60min  0:25  56.82
DS_T25_60min  0:30  41.44
DS_T25_60min  0:35  33.40
DS_T25_60min  0:40  30.62
DS_T25_60min  0:45  28.34
DS_T25_60min  0:50  26.44
DS_T25_60min  0:55  24.82

;; DS_T50_60min   total 94.9 mm
DS_T50_60min  0:00  44.61
DS_T50_60min  0:05  57.63
DS_T50_60min  0:10  87.09
DS_T50_60min  0:15  531.05   <-- OVER-PREDICTED; substitute
DS_T50_60min  0:20  125.93
DS_T50_60min  0:25  68.70
DS_T50_60min  0:30  50.11
DS_T50_60min  0:35  40.39
DS_T50_60min  0:40  37.02
DS_T50_60min  0:45  34.27
DS_T50_60min  0:50  31.97
DS_T50_60min  0:55  30.02
```

---

## 6. OBSERVED 2024–2026 — the calibration target **[SOURCED]**

**Station San Andrés (L-4)** — effectively on site. MARN normal 1981–2010 = **1648 mm/yr**.

| Season | May–Oct total | **Max 24-h depth** | Date |
|---|---:|---:|---|
| **2024** | 1693.8 mm (national +17%) | **82.5 mm** | 17 Jun 2024 |
| **2025** | 1688.4 mm (national +11%) | **64.6 mm** | 16 Aug 2025 |
| **2026** (to 15 Jul) | 643.1 mm | **66.4 mm** | 22 May 2026 |

Also **[SOURCED]**: AgrC Zapotitán recorded **48 mm on 11 Jul 2026** (07:00–20:55) — highest in the
country that day. 2026 systems incl. TS Cristina.

### 6.1 ⚠ THE KEY INSIGHT — the rain was not exceptional
**[DERIVED]** **GPEX** (Gründemann et al. 2023, `10.1016/j.jhydrol.2023.129558`; data DOI
`10.4121/12764429.v4`), an extreme-value product on a 0.1° grid, evaluated at the nearest cell
**13.85 N, −89.45 W (~7 km from site)**:
- **24-h GEV: 84.41 mm (2 yr)** / 131.77 mm (10 yr) / 250.28 mm (100 yr)
- 3-h GEV: 51.33 (2 yr) / 70.40 (10 yr) / 94.23 mm (100 yr)

**The largest 24-h depth observed at the site in three seasons (82.5 mm) ≈ the 2-YEAR 24-h depth
(84.4 mm) from an independent gridded product 7 km away.**

**⇒ The reported overflows are NOT being driven by extraordinary rainfall.** 2024 (+17%) and 2025
(+11%) were wetter *seasons* — that is accumulated volume, not event intensity. **Look at
short-duration intensity and/or system capacity.**

**Corroboration [SOURCED]** — SNET doc00237 §1 measured the intensities that actually cause flooding
in AMSS: **PROCAFE 10 mm/10 min; ILOPANGO 20 mm/10 min; BOQUERÓN 23 mm/10 min.**
**[DERIVED]** the S-10 equation gives 20.1 mm/10 min at **Tr = 2** — i.e. **AMSS drainage floods at
roughly the 2-year event.** Perfectly consistent with SNET's own narrative that *"las inundaciones …
no siempre son provocadas por cantidades altas de lluvia."* **A system overflowing at ~Tr=2 is
normal for El Salvador — and is a capacity problem, not a rainfall anomaly.**

### 6.2 Getting real sub-daily data (the calibration target proper)
- **Daily, no auth:** `https://srt.ambiente.gob.sv/old/index.php?rutina=ver_diarios&fecha=YYYY-MM-DD`
  (confirmed working; returns all conventional stations incl. `L4 SAN ANDRES`)
- **10-min telemetric data EXISTS but is LOGIN-GATED** (`consulta_telem`). Nearest telemetric
  gauges: **Ciudad Arce (3.55 km)**, **AgrC Zapotitán / ENA-SanAndrés (5.28 km)**.
- **⇒ HIGHEST-VALUE ACTION: request the 10-min series for Ciudad Arce / Zapotitán covering the
  actual failure dates from DGOA-MARN.** That is a *real observed hyetograph at the site* — worth
  more than any synthetic design storm, and it is the only way to know what actually overflowed it.

---

## 7. GLOBAL / GRIDDED FALLBACKS — all fail the 5-min requirement **[SOURCED]**

The binding constraint is **5-minute** blocks (§5.1) and a roof Tc of ~5–10 min.

| Product | Finest duration | Coverage at site | 5-min capable? |
|---|---|---|---|
| **GSDR-IDF** (Green/Guerreiro/Fowler, Sci Data, 14 Feb 2026, `10.1038/s41597-026-06858-4`) | **1 h** (1/3/6/24 h; Tr 10/30/100 only) | **ZERO Central America gauges; nearest 1,533 km** vs authors' own **200 km** limit (7.7×) | **NO — decisively** |
| GPEX (`10.1016/j.jhydrol.2023.129558`) | **3 h** | ✅ real values ~7 km away | **NO** — but useful for 3-h/24-h sanity check (§6.1) |
| GPM IMERG (`gpm.nasa.gov/data/imerg`) | **30 min** | ~0.1° | **NO** (6× too coarse) |
| ERA5 (`cds.climate.copernicus.eu`) | **hourly**, 0.25° (~28 km) | yes | **NO** (12× too coarse) |
| CHIRPS (`chc.ucsb.edu/data/chirps`) | **daily** (+pentad), 0.05° | yes | **NO** (288× too coarse) |
| **NOAA Atlas 14** | — | **NO** — 50 states + DC + PR + USVI + Pacific Is. only | **N/A** |
| **NOAA Atlas 15** | — | **NO, and none planned** — scope is "the entire United States" | **N/A** |

**On the GSDR-IDF lead specifically (priority #4): CHASED AND CLOSED — it does not work.** GSDR is an
**hourly** gauge dataset, so GSDR-IDF can never reach 5 min; and it has no Central America stations.
**But the underlying GSDR inventory yields the single most useful fact in this report:
El Salvador sub-daily data is listed "Yes (restricted) → Included: No" — the records EXIST and are
simply unreleased.** Costa Rica (9 gauges) and Panama (14) *are* in GSDR; Guatemala/Honduras/Nicaragua
are absent entirely.

**Also verified absent:** "OpenIDF" does not exist; no WMO/GWP IDF product; NG-IDF is CONUS-only;
Ombadi et al. PERSIANN-CDR IDF is CONUS-only. **Central America L-moments regionalization: not found**
(flagged as *not found*, not *proven absent* — least search depth).
⚠ **PXR-4 caution:** its published Eq. 7 prints a **sign error** (`−` where the author's own code uses
`+`); with κ = −0.114 the printed form drives intensity **negative at T=100**. Avoid, or use `+`.

**⇒ Satellite/reanalysis additionally SMOOTH convective peaks — they under-represent precisely the
short-duration extremes that matter here. Gridded data is not a substitute; it is context only.**

---

## 8. CONFIDENCE + GAPS

### HIGH confidence
- All equations/tables transcribed and **independently verified**: Güija → 0.007 mm/h over 78 cells;
  Procafé → 64.44 vs 64.45 mm; S-10 coords match MARN WFS exactly; A15/S10 indices match MARN's live
  portal; mm/min units confirmed by hyetograph sum.
- Distances **[DERIVED]** from MARN's own WFS coordinates.
- Regulation quoted verbatim from the **current** (Dec 2025) text; jurisdiction confirmed by
  zero-hit search for "Ciudad Arce".
- GSDR-IDF / NOAA / IMERG / CHIRPS / ERA5 specs read from primary sources.
- Observed 2024–26 San Andrés depths and the GPEX 7-km cross-check.

### MEDIUM confidence
- **Which station best represents the site.** Izalco (390 m, 32.6 km) is the best elevation analog;
  S-10 has the longest record (44 yr) and is an official station; Asunción Mita (478 m) matches
  elevation best of all but is 66 km away and in another country. **No station is close AND
  elevation-matched AND IDF-bearing.** Spread across sources at Tr=25 is **1.26–1.41× at 20–60 min**,
  worsening to **2.1× at 5 min**.

### GAPS — stated plainly
1. **IDF for San Andrés: NOT OBTAINABLE.** Not published; station is daily-read; absent from both
   the SHN pluviograph list and the OPAMSS official list. **This is a firm negative, not a
   search failure.** ← *the single most consequential gap*
2. **No IDF for ANY station within 17 km.** Ciudad Arce (3.55 km) and Zapotitán (5.28 km) have no
   published IDF. Every IDF-bearing station is ≥17 km away.
3. **No observed sub-daily intensity for 2024–26.** MARN publishes only 24-h totals; 10-min
   telemetric data exists but is **login-gated**. **This is the gap that actually blocks calibration.**
4. **Elevation mismatch.** Site 461–463 m. IDF stations: Izalco 390 m, Güija 485 m, S-10 615 m,
   Santa Tecla ~920 m, Boquerón ~1800 m. The two *measured* tables (best short-duration data) are
   the two *worst* elevation analogs — an unavoidable trade-off.
5. **Data vintage.** UCA-2004 equations rest on 1953–2003 records; Santa Tecla table ends **1984**.
   None reflect any post-2007 trend. A peer thread cited a **"+30–40% per MARN 2019"** uplift —
   **I could not verify this and did NOT apply it. Do not use that figure until sourced.**
6. **ITIC (S-04) table not obtained** — one of the four official OPAMSS stations.
7. **Conflicting San Andrés coordinates** (0.84 / ~2 / 5.28 km) — unresolved; immaterial at IDF scale.
8. **Procafé equation has no stated period of record.**

### Recommended next action (highest value first)
1. **Request from DGOA-MARN:** (a) 10-min series for **Ciudad Arce** and **Zapotitán/ENA-San Andrés**
   over the actual 2024–26 failure dates → *real observed hyetograph, the true calibration target*;
   (b) *Intensidad de Precipitación Máxima Anual* for **San Andrés L-4** / Ciudad Arce. This is
   exactly what OPAMSS's own procedure mandates and would replace every transfer assumption here.
2. Until then: **Izalco T-3 for d ≥ 15 min**, **5–10 min capped to the 190–260 mm/h (Tr=25) band**,
   Chicago 5-min blocks at r ≈ 0.21, Tr=25 collectors / Tr=50 outfall.
3. **Model the Tr=2 event too.** Given §6.1, the system plausibly fails at ~Tr=2 — reproducing that
   is a stronger validation of the model than any 50-yr synthetic storm.

---
*Supersedes `research_rainfall.md` (retained as working notes). Nothing written to the project directory.*
