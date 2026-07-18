import math
print("="*78); print("Q1. WHERE 1,390 m2 COMES FROM"); print("="*78)
W_MOD, N_MOD, LEN = 41.2, 3, 67.5
print(f"  From dimensioned CAD text (DIM layer), not measured pixels:")
print(f"    '123.600'  -> A->K total width;  two x '41.200' -> module width")
print(f"    grid A,D,H,K spaced {W_MOD} m;  {N_MOD} x {W_MOD} = {N_MOD*W_MOD} m  [matches '123.600']")
print(f"    rows 1..10 at 7.5 m -> 9 x 7.5 = {LEN} m")
roof = N_MOD*W_MOD*LEN
print(f"    ROOF (plan) = {N_MOD*W_MOD} x {LEN} = {roof:,.0f} m2")
print(f"  Independent cross-check: CAD text 'area piso'+'area mezzanine' for 2 modules")
print(f"    2,797.47 + 2,811.06 = 5,608.53 m2  -> x3/2 = {5608.53*3/2:,.0f} m2  "
      f"(delta {abs(5608.53*3/2-roof)/roof*100:.1f}%)")
print(f"\n  THREE PEAKS -> 3 gables -> each module drains 2 ways (ridge in the middle):")
for nm, share in [("A  eave  (module 1 west half)", 0.5), ("D  pair  (mod 1 east + mod 2 west)", 1.0),
                  ("H  pair  (mod 2 east + mod 3 west)", 1.0), ("K  eave  (module 3 east half)", 0.5)]:
    print(f"    {nm:<36} {share*W_MOD*LEN:>8,.0f} m2")
print(f"  CAD found 6 collector lines: 2 singles at the edges + 2 tight PAIRS (4.5-4.9 m apart).")
print(f"  The pairs are the two-sided catch, already split across two pipes.")
print(f"    {roof:,.0f} / 6 = {roof/6:,.0f} m2 per collector = one roof slope = "
      f"{W_MOD/2} x {LEN} = {W_MOD/2*LEN:,.0f} m2  [consistent]")

print("\n"+"="*78); print("Q2. WHY D^(8/3) AND S^(1/2)"); print("="*78)
print("  Manning:  Q = (1/n) . A . R^(2/3) . S^(1/2)")
print("  For a full circular pipe:  A = pi.D^2/4  (prop. D^2)   R = D/4  (prop. D^1)")
print("  =>  Q  prop.  D^2 . D^(2/3)  =  D^(8/3)      and   Q prop. S^(1/2)")
for a,b in [(8,10),(8,12),(8,9)]:
    print(f"    {a}\" -> {b}\":  ({b}/{a})^(8/3) = {(b/a)**(8/3):.3f}  -> +{((b/a)**(8/3)-1)*100:.0f}% flow")
for m in (2,3,4):
    print(f"    slope x{m}:   {m}^(1/2) = {m**0.5:.3f}  -> +{(m**0.5-1)*100:.0f}% flow")

print("\n"+"="*78); print("Q3. THE 1.85% FIGURE -- I MISLABELLED IT"); print("="*78)
D=8*0.0254; A=math.pi*D*D/4; R=D/4; n=0.011
Qcap=(1/n)*A*R**(2/3)*math.sqrt(0.01)
print("  Rearranged Manning:   Sf = ( Q.n / (A . R^(2/3)) )^2")
print(f"  8\" full: A={A:.5f} m2  R={R:.4f} m  R^(2/3)={R**(2/3):.5f}  n={n}")
print(f"  Shortcut:  Sf = S_design x (Q/Qcap)^2      Qcap@1% = {Qcap*1000:.2f} L/s")
for Q in (0.0404, 0.044, 0.055, 0.064):
    Sf=(Q*n/(A*R**(2/3)))**2
    print(f"    Q={Q*1000:5.1f} L/s -> Sf = {Sf*100:5.2f} cm per 100   "
          f"[check via shortcut: {0.01*(Q/Qcap)**2*100:5.2f}]")
print("\n  I wrote '44 L/s needs 1.85 cm per 100'. WRONG: 44 L/s needs 1.18.")
print("  1.85 is the 55 L/s case (150 mm/h). The claim was right, the label was not.")

print("\n"+"="*78); print("Q5. THE 43 cm HGL RISE"); print("="*78)
print("  Flow tapers upstream: Q(x) = Qtot.(1 - x/L)   [boca tubos hand in along the way]")
print("  Sf(x) = Sf0.(1-x/L)^2   ->   integral over 0..L  =  Sf0 . L/3")
for Q,label in [(0.055,"55 L/s @150 mm/h"),(0.044,"44 L/s @120 mm/h"),(0.064,"64 L/s @ i(Tc)")]:
    Sf0=0.01*(Q/Qcap)**2
    print(f"    {label:<20} Sf0={Sf0*100:5.2f}%  ->  rise = {Sf0:.5f} x 70/3 = {Sf0*70/3*100:5.1f} cm")
print("\n  The L/3 (not L) is because flow tapers. 43 cm was the 55 L/s case.")
