"""HGL along the aerial collector. Settles: where is the bottleneck, and where does it spill?"""
import math

D_IN, N, S_PIPE, L = 8, 0.011, 0.01, 70.4
ROOF_PER = 1390.0; C = 0.95
D = D_IN*0.0254; A = math.pi*D**2/4; R = D/4

def sf(Q):
    """Friction slope for full-bore flow Q (m3/s).  Sf = n^2 Q^2 / (A^2 R^(4/3))"""
    return (N**2 * Q**2) / (A**2 * R**(4.0/3.0))

print("="*78)
print("CLAIM 1: 'friction is highest in the fall, so widen there'")
print("="*78)
print("  A pipe bottlenecks where REQUIRED friction slope > AVAILABLE slope.\n")
print(f"  {'section':<22} {'available':>10} {'required@55L/s':>15} {'verdict':>22}")
for label, avail in [("horizontal collector", 0.01), ("vertical fall", 1.00)]:
    req = sf(0.055)
    if req > avail:
        v = f"DEFICIT {(req-avail)*100:.2f}%  BOTTLENECK"
    else:
        v = f"surplus {(avail-req)*100:.0f}%  fine"
    print(f"  {label:<22} {avail*100:>9.0f}% {req*100:>14.2f}% {v:>22}")

qv = A*(1.0/N)*R**(2/3.)*math.sqrt(1.00)*1000
qh = A*(1.0/N)*R**(2/3.)*math.sqrt(0.01)*1000
print(f"\n  Same 8\" pipe:  vertical = {qv:.0f} L/s   horizontal@1% = {qh:.0f} L/s   ({qv/qh:.0f}x more)")
print("  Real leader (annular, IPC 8\"=1208gpm) = 76 L/s -- still ~2x the collector.")
print("  => The fall is NOT the constraint. Widening it enlarges the surplus.")

print("\n"+"="*78)
print("CLAIM 2: 'it should overflow at the far end' -- depends on GUTTER geometry")
print("="*78)

def profile(i_mmh, gutter_slope):
    """March upstream from the outlet. x=0 outlet, x=L far end.
       gutter_slope=0.0 -> level gutter;  0.01 -> gutter parallel to pipe."""
    Qtot = C*(i_mmh/1000/3600)*ROOF_PER
    dx, x, hgl = 0.1, 0.0, 0.0 + D          # start just-full at the free outlet
    out = []
    while x < L:
        Q = Qtot*(1 - x/L)                   # flow decreases upstream
        z = S_PIPE*x                         # invert rises upstream
        hgl = max(hgl, z + D)                # can't be below crown if full
        g = D + gutter_slope*x + 0.35        # gutter/boca-tubo lip elevation
        out.append((x, hgl, g, hgl - g))
        hgl += sf(Q)*dx
        x += dx
    return out

for i_mmh in (120, 150):
    print(f"\n  --- intensity {i_mmh} mm/h ({C*(i_mmh/1000/3600)*ROOF_PER*1000:.0f} L/s per collector) ---")
    for gs, name in [(0.0, "LEVEL gutter (drains every bay)"),
                     (0.01, "gutter PARALLEL to pipe @1%")]:
        p = profile(i_mmh, gs)
        spills = [r for r in p if r[3] >= 0]
        print(f"    {name:<34}", end="")
        if not spills:
            worst = max(p, key=lambda r: r[3])
            print(f" no spill (closest at x={worst[0]:.0f} m, {-worst[3]*100:.0f} cm freeboard)")
        else:
            first = min(spills, key=lambda r: r[0]); far = max(spills, key=lambda r: r[0])
            print(f" SPILLS x={first[0]:.0f}-{far[0]:.0f} m  (0=outlet, {L:.0f}=far end)")

print("\n"+"="*78)
print("  Level gutter + sloping pipe => the pipe DIVES AWAY from the gutter")
print(f"  downstream: over {L:.0f} m @1% that is {S_PIPE*L*100:.0f} cm of extra freeboard")
print("  at the outlet end. Meanwhile friction lifts the HGL going upstream.")
print("  BOTH effects push the first spill to the FAR END. -> user is right.")
print("="*78)
