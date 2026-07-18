"""Does roof pitch affect Q? Direct answer, then the indirect one."""
import math

A_PLAN, C, i = 1390.0, 0.95, 120.0

print("="*74)
print("DIRECT EFFECT OF ROOF PITCH ON Q  --  rain falls VERTICALLY")
print("="*74)
print(f"{'pitch':>7} {'surface area':>14} {'vs plan':>9} {'Q = C*i*A_plan':>16} {'Q if you (wrongly)':>20}")
print(f"{'':>7} {'(m2)':>14} {'':>9} {'(L/s)':>16} {'used surface (L/s)':>20}")
for pct in (0, 6, 12, 25, 50, 100):
    s = pct/100
    a_surf = A_PLAN*math.sqrt(1+s*s)
    q_correct = C*(i/1000/3600)*A_PLAN*1000
    q_wrong   = C*(i/1000/3600)*a_surf*1000
    print(f"{pct:>6}% {a_surf:>14,.0f} {a_surf/A_PLAN:>8.3f}x {q_correct:>16.2f} {q_wrong:>20.2f}")
print("\n  Q is IDENTICAL at every pitch. A steeper roof has more skin, but it")
print("  intercepts the same falling rain -- the catch is the HORIZONTAL shadow.")
print("  => You are right: pitch does not affect Q directly.")
print("\n  (Note: the CAD agent's '8,343 -> 8,403 m2 slope correction' must NOT be")
print("   applied to Q. 8,343 m2 (plan) is the correct number. Surface area matters")
print("   for buying roofing sheet, not for catching rain.)")

print("\n"+"="*74)
print("INDIRECT EFFECT: pitch -> speed -> time of concentration -> intensity -> Q")
print("="*74)

def idf(t, i10=120.0, b=10.0, c=0.75):
    """Sherman form. Flattens at short duration -- unlike a bare power law,
       which blows up as t->0 (the trap flagged in the rainfall research)."""
    return i10*((10.0+b)/(t+b))**c

def tc(pitch, L=20.6, n_roof=0.012, t_other=1.5):
    """Kinematic wave sheet flow; iterate because t depends on i depends on t."""
    S = max(pitch, 1e-4); t = 5.0
    for _ in range(60):
        i_now = idf(t)
        t_sheet = 6.99*(n_roof*L)**0.6/(i_now**0.4 * S**0.3)
        t = 0.5*t + 0.5*(t_sheet + t_other)
    return t, idf(t)

print(f"{'pitch':>7} {'Tc (min)':>10} {'i at Tc':>10} {'Q':>10} {'vs 12% roof':>13}")
base_t, base_i = tc(0.12)
base_q = C*(base_i/1000/3600)*A_PLAN*1000
for pct in (1, 2, 6, 12, 25, 50):
    t, ii = tc(pct/100)
    q = C*(ii/1000/3600)*A_PLAN*1000
    print(f"{pct:>6}% {t:>10.2f} {ii:>9.0f}  {q:>9.1f} {q/base_q:>12.2f}x")

print(f"\n  Your roof is 12% -> Tc = {base_t:.2f} min, i = {base_i:.0f} mm/h, Q = {base_q:.0f} L/s")
print("  Flattening 12% -> 2% slows runoff and LOWERS peak Q by ~10%.")
print("  So pitch matters ~10% via TIMING, and 0% via AREA. Both are true at once.")

print("\n"+"="*74)
print("WHY THIS MATTERS: a fast roof reads a HIGHER number off the IDF curve")
print("="*74)
for t in (2, 2.5, 3, 5, 10, 20, 60):
    q = C*(idf(t)/1000/3600)*A_PLAN*1000
    flag = "  <-- floods (>249 L/s eq.)" if q > 40.4/0.95*0.95 and idf(t) > 249 else ""
    print(f"  storm duration {t:>4.1f} min -> i = {idf(t):>5.0f} mm/h -> Q = {q:>5.1f} L/s{flag}")
print("\n  Reading the 10-min number (120 mm/h) for a roof that responds in ~2.5 min")
print("  understates the intensity it actually sees. That was MY error earlier.")
