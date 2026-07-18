import math
print("="*80); print("Q4 + SAG: WHAT PRESSURISING A DRAIN PIPE ACTUALLY DOES"); print("="*80)

# 8" PVC, two plausible classes
CLASSES = {
    "Sch 40 (ASTM D1785/D2665 DWV)": dict(OD=0.2191, wall=0.00818),
    "SDR-35 sewer (ASTM D3034)":     dict(OD=0.2134, wall=0.00610),
    "SDR-41 thin-wall":              dict(OD=0.2191, wall=0.00534),
}
RHO_PVC, E_NEW, E_LONG = 1400.0, 2.76e9, 1.0e9   # Pa; long-term = 50-yr creep modulus

print("\n1) HOW MUCH PRESSURE ARE WE EVEN TALKING ABOUT?")
for h in (0.2, 0.5, 1.0, 1.5):
    print(f"   HGL {h:.1f} m above the crown -> {h*9.81:.1f} kPa = {h*9.81/100:.3f} bar"
          f" = {h*9.81*0.145:.1f} psi")
print("   PVC drain pipe is rated in the HUNDREDS of kPa. Structurally this is nothing.")
print("   The danger is NOT burst. It is weight, joints and geometry. ->")

print("\n2) WEIGHT: a full pipe vs a half-full one")
for nm, c in CLASSES.items():
    ID = c["OD"] - 2*c["wall"]
    a_w = math.pi*ID**2/4
    a_p = math.pi*(c["OD"]**2 - ID**2)/4
    w_pipe = a_p*RHO_PVC
    w_full = a_w*1000
    print(f"   {nm:<32} ID={ID*1000:5.1f} mm  pipe {w_pipe:4.1f} kg/m"
          f" + water {w_full:4.1f} kg/m = {w_pipe+w_full:5.1f} kg/m full"
          f"  ({(w_pipe+w_full)/(w_pipe+w_full/2):.2f}x the half-full load)")

print("\n3) SAG: delta = 5.w.L^4/(384.E.I)   -- note the FOURTH power of hanger spacing")
print("   IPC Table 308.5 requires PVC horizontal support every 4 ft = 1.22 m.\n")
print(f"   {'hanger':>7} {'sag NEW':>9} {'sag AGED':>9} {'local adverse':>14} {'net slope':>11}  verdict")
print(f"   {'spacing':>7} {'(mm)':>9} {'(mm)':>9} {'4d/L (%)':>14} {'@1% (%)':>11}")
c = CLASSES["Sch 40 (ASTM D1785/D2665 DWV)"]
ID = c["OD"] - 2*c["wall"]
I  = math.pi*(c["OD"]**4 - ID**4)/64
w  = (math.pi*(c["OD"]**2-ID**2)/4*RHO_PVC + math.pi*ID**2/4*1000)*9.81   # N/m, full
S_DESIGN = 0.01
for Lh in (1.22, 1.5, 2.0, 2.5, 3.0, 4.0):
    d_new  = 5*w*Lh**4/(384*E_NEW*I)
    d_long = 5*w*Lh**4/(384*E_LONG*I)
    adverse = 4*d_long/Lh
    net = S_DESIGN - adverse
    verdict = "PONDS - runs uphill" if net <= 0 else ("marginal" if net < 0.005 else "ok")
    print(f"   {Lh:>6.2f}m {d_new*1000:>9.2f} {d_long*1000:>9.2f} {adverse*100:>14.2f}"
          f" {net*100:>11.2f}  {verdict}")

crit = S_DESIGN/4
print(f"\n   Critical sag that flattens a 1% pipe to zero: delta = S.L/4")
for Lh in (1.22, 3.0):
    print(f"     at {Lh:.2f} m hangers -> only {crit*Lh*1000:.1f} mm of droop is enough")

print("\n4) SO WHAT? -- the failure chain")
print("   sag -> local reverse grade -> water ponds in every span -> pipe must SURCHARGE")
print("   to push flow over each crest -> surcharged pipe is heavier -> PVC creeps ->")
print("   MORE sag. It is a ratchet, and it explains 'it used to work'.")
print("   Air also collects at every crest and cannot escape (the Y-T at the outlet is")
print("   the only opening). Trapped air blocks bore. Neither effect is in the model.")
