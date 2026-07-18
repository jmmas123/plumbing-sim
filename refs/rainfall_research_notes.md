# Rainfall research — warehouse @ 13.815527, -89.408015 (Zapotitán valley, La Libertad, El Salvador)

## Station distances (SOURCED: MARN Lizmap WFS, layer `Estaciones`, 130 stations)
Endpoint: https://ruraladelante.snet.gob.sv/index.php/lizmap/service/?repository=estaciones&project=estaciones&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&TYPENAME=Estaciones&OUTPUTFORMAT=GeoJSON

| km | station | tipo | lat | lon | IDF published? |
|---|---|---|---|---|---|
| 3.55 | Ciudad Arce | P | 13.829981 | -89.437325 | NO |
| 5.28 | AgrC Zapotitan | M | 13.7682 | -89.4119 | NO |
| 5.28 | ENA-SanAndres | M | 13.768187 | -89.41183 | NO |
| 7.59 | Talnique | H | 13.751 | -89.431 | NO |
| 12.65 | Coatepeque | P | 13.867639 | -89.51214 | NO |
| 17.68 | Boqueron (L-18) | M | 13.7339 | -89.2675 | **YES (table)** |
| 19.62 | PROCAFE | M | 13.6843 | -89.2866 | **YES (equation)** |
| 23.99 | Santa Ana | M | 13.9825 | -89.5488 | NO |
| 33.90 | Ilopango (S-10) | M | 13.6983 | -89.1183 | named official, table not obtained |

Santa Tecla (L-08) not in telemetric layer (conventional station). IDF table obtained anyway.

NOTE conflict: a web-search snippet gave "San Andrés 13.808, -89.407" (=0.84 km). Official WFS
puts ENA-SanAndres at 13.768187,-89.41183 (=5.28 km). Trust WFS.

## SOURCED IDF — Procafé (exact, verbatim)
OPAMSS "Guía Técnica para el diseño de SUDS en el AMSS", Módulo 4, Ecuación 22.1 (image extracted):

    I = 10.72738 * T^0.21884 / (D^0.63024 + 1.00332)
    I = mm/min ; T = years ; D = minutes

VALIDATED: doc's own worked example says Tr=5, D=60 → 64.45 mm. Equation gives 64.44 mm. ✓

## SOURCED IDF tables — Santa Tecla & Boquerón (units mm/min)
SNET/Servicio Hidrológico Nacional, doc00237 (archived). Tables were embedded images; read via
pypdf image extraction + positional (cm-matrix) reading-order analysis. Units confirmed mm/min by
summing the Boquerón Tr=25/120-min hyetograph image (~78 mm) vs table 0.64*120 = 76.8 mm. ✓

Santa Tecla (L-08), 1954-1984, D = 5,10,15,20,30,45,60,90,120,180,240,360 min
  T=2:   2.61 2.13 1.85 1.65 1.35 1.05 0.81 0.60 0.47 0.32 0.25 0.17
  T=5:   3.03 2.45 2.16 1.95 1.63 1.28 1.03 0.75 0.58 0.40 0.33 0.23
  T=10:  3.26 2.62 2.32 2.10 1.77 1.41 1.17 0.85 0.64 0.44 0.37 0.27
  T=15:  3.37 2.71 2.41 2.18 1.84 1.47 1.24 0.90 0.68 0.47 0.39 0.29
  T=20:  3.44 2.76 2.46 2.24 1.89 1.51 1.29 0.94 0.71 0.48 0.40 0.30
  T=25:  3.49 2.80 2.50 2.27 1.92 1.53 1.33 0.96 0.72 0.50 0.41 0.31
  T=50:  3.65 2.92 2.61 2.38 2.02 1.62 1.45 1.05 0.78 0.54 0.44 0.33
  T=100: 3.78 3.02 2.71 2.48 2.11 1.69 1.57 1.13 0.84 0.58 0.47 0.35

Boquerón (L-18), 1967-1993 + 2004-2007, D = 5,10,15,20,30,45,60,90,120,150,180,240,360 min
  T=2:   3.11 2.28 1.88 1.70 1.37 1.04 0.85 0.61 0.48 0.39 0.34 0.25 0.19
  T=5:   3.69 2.63 2.13 1.97 1.57 1.17 0.96 0.70 0.56 0.47 0.41 0.31 0.25
  T=10:  3.99 2.81 2.25 2.11 1.68 1.24 1.02 0.74 0.60 0.51 0.44 0.35 0.28
  T=15:  4.14 2.90 2.32 2.18 1.73 1.27 1.05 0.76 0.62 0.53 0.46 0.37 0.29
  T=20:  4.24 2.96 2.36 2.23 1.77 1.29 1.07 0.77 0.63 0.54 0.48 0.39 0.30
  T=25:  4.31 3.01 2.39 2.26 1.79 1.31 1.08 0.78 0.64 0.55 0.48 0.40 0.31
  T=50:  4.52 3.13 2.48 2.36 1.87 1.35 1.12 0.81 0.67 0.58 0.51 0.44 0.33
  T=100: 4.71 3.25 2.56 2.45 1.93 1.39 1.16 0.84 0.69 0.61 0.53 0.48 0.34

Data-quality note: 2-dp rounding creates small non-monotonic cumulative depths
(Boquerón Tr=2: 180min→61.2 mm vs 240min→60.0 mm). Enforce monotonic cumulative depth when interpolating.

## DERIVED (my fits, NOT sourced) — per-return-period, I[mm/min] = a/(D^n + c)
Santa Tecla: T2 a=76.178 n=1.0291 c=24.369 (MAPE 1.3%) ... T100 a=129.221 n=0.99711 c=31.136 (MAPE 4.0%)
Boquerón:    T2 a=47.697 n=0.93614 c=11.492 (MAPE 2.5%) ... T100 a=25.612 n=0.73112 c=2.2401 (MAPE 3.6%)
Single separable k*T^m/(D^n+c) fits POORLY (max err ~19-21%) — T-dependence varies with duration
(Santa Tecla growth ratio T100/T2: 1.45 @5min → 2.06 @360min). Use table interpolation, not a global fit.

## Regulation (SOURCED)
Current: OPAMSS LDOTAMSS y Reglamento, Dic 2025 — https://opamss.org.sv/wp-content/uploads/2025/12/LDOTAMSS-Y-REGLAMENTO-DIC_-2025.pdf
- "Mientras se generan y publican las curvas IDF para el AMSS, en coordinación con el MARN" → official AMSS IDF NOT yet published
- Official IDF stations: S-10 Aeropuerto Ilopango, S-04 ITIC, L-08 Santa Tecla, L-18 Boquerón
- 5 km single-station rule; 5-10 km inverse-distance weighting, never < 85% of max; >10 km → assigned station by municipality; >3 stations → Thiessen
- Caudal hidrológico: **Tr ≥ 50 yr** (100 if OPAMSS requests)
- Colectores de aguas lluvias: **Tr ≥ 25 yr**, rational method, **Tc = 5 min** for tragantes
- Rational method for areas ≤ **2.5 km²** (the 2020 draft said 15,000 Ha — superseded)
- TCi = **0.65 * TCc** (2020 draft said 0.70 — superseded)
- **Hyetograph: "hidrograma de lluvia tipo 'Chicago' o de bloques alternativos de 5 minutos"** ← answers item 5
- Runoff coeff: Techos 0.80/0.90/0.95 ; Industrial >70% imperm 0.70/0.80/0.90
- CN: Áreas industriales (72% imperm) A81 B88 C91 D93 ; Pavimento y tejados = 100
- Design with AMC III; CNIII = 23*CNII/(10+0.13*CNII)
- SMIH peak reduction 50-90% vs pre-development

JURISDICTION: site is in Ciudad Arce (La Libertad) = NOT one of the 14 AMSS municipalities → OPAMSS
does not legally apply. Best-documented Salvadoran practice nonetheless.

ANDA "Normas Técnicas" (https://www.anda.gob.sv/wp-content/uploads/2023/08/Normas-Tecnicas-ANDA.pdf):
potable water + aguas negras ONLY. Grep for pluvial/retorno/intensidad → no storm design content.
National D-70-91 Reglamento LUC: requires aguas lluvias drainage but NO return period/intensity spec.

## Hyetograph shape (SOURCED, SNET doc00237 §2 and §4)
- SNET generated design storms using "método de bloque alterno" BUT rearranged to the OBSERVED
  temporal pattern rather than the alternating arrangement.
- "generalmente las máximas cantidades de lluvia, sin importar la duración total, se presentan
  entre los 10 a 20 minutos desde que comienza la lluvia, o en su defecto entre los 20 a 30 minutos"
  → Salvadoran convective storms are FRONT-LOADED (peak ~15-25% into the storm), NOT SCS Type II (50%).
- Boquerón Tr=25/120min hyetograph (Fig 5, read from image): 11.5, 16.5, 18.3, 11.3, 3.2, 3.3, 3.3,
  2.7, 2.4, 2.3, 2.2, 1.3 mm per 10-min block → peak in 3rd block (20-30 min).

## Flood thresholds AMSS (SOURCED, doc00237 §1) — intensities that cause flooding
PROCAFE: 10 mm/10min, 20 mm/20min | BOQUERON: 23 mm/10min, 33 mm/20min | ILOPANGO: 20 mm/10min, 30 mm/20min

## Sources
- SNET doc00237 (archived): http://web.archive.org/web/20190711175023/http://portafolio.snet.gob.sv:80/digitalizacion/pdf/spa/doc00237/doc00237-contenido.pdf
  (live portafolio.snet.gob.sv is NXDOMAIN; WebFetch cannot reach web.archive.org — use curl)
- OPAMSS SUDS Módulo 4: https://opamss.org.sv/wp-content/uploads/2021/07/Modulo-4-Diseno-SUB-para-el-AMSS.pdf
- OPAMSS SUDS Módulo 2: https://opamss.org.sv/wp-content/uploads/2021/07/Modulo-2.-El-proceso-de-diseno-de-SUDS-en-el-AMSS.pdf
- OPAMSS Art V.14 (2020 draft): https://opamss.org.sv/wp-content/uploads/2020/07/Propuesta-modificacion-del-Reglamento-V.14-OPAMSS.pdf
- UES thesis (Zona Oriental, 2014): https://repositorio.ues.edu.sv/items/b92c8991-09c6-4dd9-a29e-c3599a1d7b7f

## Guatemala INSIVUMEH national IDF (regional fallback / cross-check) — SOURCED
https://insivumeh.gob.gt/wp-content/uploads/2026/03/Curvas-de-Intensidad-Duracion-y-Frecuencia-IDF-para-la-Republica-de-Guatemala.pdf
Sherman model, published per IFI/FRIEND convention:  I(mm/h) = K*Tr^m/(D+B)^n ; D min, Tr yr. 30 stations.
Most relevant (elevation analog to site):
  Asuncion Mita, Jutiapa, Ostua-Guija basin, elev 478 m, 14.33444/-89.7058, 66.0 km from site:
      I = 3931 * Tr^0.220 / (D + 26.36)^1.090
  Esquipulas (1000 m, 14.55889/-89.3419): I = 1074*Tr^0.135/(D+16.12)^0.697
  Montufar (10 m, 13.80889/-90.1550):     I = 1438*Tr^0.148/(D+27.26)^0.717
  Los Esclavos (737 m):                   I = 1933*Tr^0.144/(D+20.56)^0.887

## KEY FINDING — short-duration equations over-predict
Guija (SV, 485 m) and Asuncion Mita (GT, 478 m) are 27.2 km apart, same basin, same elevation,
independent agencies. Their IDF agree within ~10-18% at 15-60 min but diverge badly at 5 min
(ratio 0.52-0.64) and 360 min.
Cause: the Salvadoran UCA-2004 equations are PURE power laws i = a*T^m/d^n with NO +B term, so they
diverge as d->0. Guatemala's Sherman form has (D+26.36) which correctly flattens at short duration.

Intensity at d=5 min, Tr=25 across all sources:
  Izalco eq (pure power law)      439 mm/h   <- highest, least trustworthy at 5 min
  Ilopango S-10 eq (pure power)   353
  Procafe eq (c=1.003, ~pure)     346
  Guija eq (pure power law)       335
  Boqueron MEASURED TABLE         259
  Santa Tecla MEASURED TABLE      209
  Asuncion Mita GT (B=26.36)      187
=> MEASURED tables + GT Sherman converge on ~190-260 mm/h; the fitted pure power laws give 335-439.
=> Do NOT trust the UCA-2004/Procafe equations below ~10-15 min. This matters a lot for a warehouse
   roof (very short Tc) where the 5-min block drives the SWMM peak.

## Observed vs design (item 4 integration)
San Andres (L-04, conventional climatological stn, ~1-5 km from site; MARN normals 1981-2010 = 1648 mm/yr)
  2024 May-Oct 1693.8 mm, max 24h  82.5 mm (17 Jun 2024)
  2025 May-Oct 1688.4 mm, max 24h  64.6 mm (16 Aug 2025)
  2026 May1-Jul15 643.1 mm, max 24h 66.4 mm (22 May 2026)
Design 24-h depth (extrapolated): Tr=2 ~104 mm.
=> The largest 24-h depth observed at the site in 3 seasons (82.5 mm) is BELOW the ~2-yr 24-h depth.
   The overflows are therefore NOT driven by extraordinary daily totals -> look at short-duration
   intensity and/or system capacity. SNET AMSS flood thresholds are ~10-23 mm in 10 min.
Daily data portal (no auth): https://srt.ambiente.gob.sv/old/index.php?rutina=ver_diarios&fecha=YYYY-MM-DD
Sub-daily (10-min) telemetric data exists but is LOGIN-GATED (consulta_telem).

## Item 6 — gridded fallback: CLOSED (verified from primary sources)
Requirement: OPAMSS Reglamento Dic-2025 mandates 5-MINUTE blocks (Chicago / bloques alternativos).

| product | native temporal res | spatial | period | 5-min capable? | source |
|---|---|---|---|---|---|
| GPM IMERG | **30 min** (Early 4h / Late ~12-14h / Final ~2.5mo latency) | ~0.1 deg | 2000- | **NO** (6x too coarse) | https://gpm.nasa.gov/data/imerg |
| CHIRPS | **daily** (+pentad) | 0.05 deg | 1981-, 50S-50N | **NO** (288x too coarse) | https://www.chc.ucsb.edu/data/chirps |
| ERA5 single levels | **hourly** | 0.25 deg (~28 km here) | 1940- | **NO** (12x too coarse) | https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels |

=> NO freely-available gridded product can resolve the 5-min intensity that drives this model.
   Reanalysis/satellite additionally smooth convective peaks (they under-estimate exactly the
   short-duration extremes that matter). Gridded data is therefore NOT a viable substitute for the
   local IDF here; it is only useful for seasonal/24-h context.
   The usable regional fallback is the Guatemala INSIVUMEH Sherman IDF (Asuncion Mita, 478 m) above.

NOAA Atlas 14 equivalent for El Salvador: NONE FOUND. Guatemala HAS a national IDF publication
(INSIVUMEH 2026, 30 stations, Sherman form per IFI/FRIEND); El Salvador does not.
