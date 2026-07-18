"""At what rainfall intensity does the as-built system fail? First principles."""
import math

# --- Geometry, from dimensioned CAD text (NOT measured/guessed) ---
W, L = 123.6, 67.5                 # m, grid A->K x rows 1->10
ROOF = W * L                       # m2 footprint
N_COLLECTORS = 6                   # 2 eave singles + 2 valley pairs
A_PER = ROOF / N_COLLECTORS        # m2 served per 8" collector
C = 0.95                           # runoff coeff, metal roof

def manning_full(D_in, S, n):
    D = D_in*0.0254
    A = math.pi*D**2/4
    return A*(1.0/n)*(D/4)**(2/3.)*math.sqrt(S)*1000     # L/s

def crit_intensity(q_lps, area_m2):
    """Rainfall intensity (mm/h) that exactly fills this pipe."""
    return (q_lps/1000)/(C*area_m2)*1000*3600

print("="*72)
print(f"ROOF {ROOF:,.0f} m2  ({W} x {L} m)   |   {N_COLLECTORS} collectors  ->  {A_PER:,.0f} m2 each")
print("="*72)

print("\nAS-BUILT: 8\" @ 1%, uniform, ~70 m run")
for n in (0.011, 0.009):
    q = manning_full(8, 0.01, n)
    i = crit_intensity(q, A_PER)
    print(f"  n={n}:  capacity {q:5.1f} L/s   ->  OVERFLOWS above  {i:5.0f} mm/h")

print("\nWHAT THE WHOLE ROOF GENERATES")
for i_mmh in (60, 100, 120, 150, 200):
    q_tot = C*(i_mmh/1000/3600)*ROOF*1000
    print(f"  {i_mmh:>3} mm/h -> {q_tot:6.1f} L/s total  ({q_tot/N_COLLECTORS:5.1f} L/s per collector)")

print("\n" + "="*72)
print("BENCHMARK: measured Salvadoran 2-yr short-duration intensity")
print("  Ilopango 20 mm/10min = 120 mm/h  == its 2-YEAR intensity  (SNET)")
print("  SNET AMSS flooding thresholds 10-23 mm/10min = 60-138 mm/h")
print("="*72)

print("\nCANDIDATE FIXES (per collector, vs 8\"@1% n=0.011 baseline)")
base = manning_full(8, 0.01, 0.011)
for label, D, S in [("8\" @ 1%  (as-built)", 8, 0.01),
                    ("8\" @ 2%  (re-hang steeper)", 8, 0.02),
                    ("10\" @ 1% (full re-pipe)", 10, 0.01),
                    ("10\" @ 2% (both)", 10, 0.02),
                    ("12\" @ 1%", 12, 0.01)]:
    q = manning_full(D, S, 0.011)
    i = crit_intensity(q, A_PER)
    print(f"  {label:<28} {q:5.1f} L/s  ({q/base:4.2f}x)  fails above {i:5.0f} mm/h")

print("\nTIME OF CONCENTRATION (sets which IDF duration matters)")
t_pipe = 70.4/1.25
print(f"  collector travel: 70.4 m @ 1.25 m/s = {t_pipe:.0f} s = {t_pipe/60:.1f} min")
print(f"  + roof sheet flow (~20 m @ 12% metal, minutes) -> Tc ~ 3-5 min")
print("  => the 5-MINUTE IDF block governs. Sub-hourly data is mandatory.")
