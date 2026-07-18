import math
print("="*72); print("1) GRADIENT — computed from your ceiling measurements"); print("="*72)
drop = 1.98 - 1.41
print(f"  pipe below ceiling: 1.41 m (first boca tubo) -> 1.98 m (outlet end)")
print(f"  vertical drop = {drop:.2f} m  (assuming the ceiling/eave line is level along the run)")
for L in (60, 63, 67.5):
    print(f"    over {L:>5.1f} m  ->  gradient = {drop/L*100:.2f}%")
print("  => ~0.85-0.95%.  Essentially the design 1%, maybe a hair under. NOT sagged, NOT steep.")

print("\n"+"="*72); print("2) THE BOCA TUBO DROP (my invented hf) — now MEASURED"); print("="*72)
D = 0.2032
print(f"  pipe invert -> canaleta floor:  far end 1.13 m,  outlet end 1.65 m")
print(f"  the gap GROWS by {1.65-1.13:.2f} m toward the outlet — because the pipe drops {drop:.2f} m")
print(f"  and the canaleta stays level. These two numbers agree ({1.65-1.13:.2f} vs {drop:.2f} m).")
print(f"  => CONFIRMS a LEVEL canaleta, independently. Your earlier observation was right.")
hf_far = 1.13 - D
print(f"\n  model hf = crown->canaleta floor at the FAR (tight) end = 1.13 - {D:.2f} = {hf_far:.2f} m")
print(f"  I had been using 0.5 m. The real buffer is ~{hf_far:.2f} m — almost double.")

print("\n"+"="*72); print("3) HANGERS — 0.85-0.90 m spacing"); print("="*72)
def sag(Lh, E=1.0e9):
    OD,wall,k=0.2191,0.00818,1.0; ID=OD-2*wall
    I=math.pi*(OD**4-ID**4)/64
    w=(math.pi*(OD**2-ID**2)/4*1400+math.pi*ID**2/4*1000)*9.81
    return 5*w*Lh**4/(384*E*I)*1000
print(f"  code max spacing 1.22 m -> sag {sag(1.22):.2f} mm")
print(f"  YOUR spacing  0.87 m    -> sag {sag(0.87):.2f} mm   ({(0.87/1.22)**4:.2f}x the code sag)")
print(f"  => sag is NEGLIGIBLE. My 'hung off 3 m trusses' worry is DEAD. Good install.")
print(f"  (64 hangers / 8 per line = 8 collector lines: 2 eaves + 2 valleys x ~3 pipes, roughly)")

print("\n"+"="*72); print("4) THE ANGLED WYE ENTRY"); print("="*72)
print("  Boca tubos enter at ~45deg WITH the flow (a wye, not a tee) — visible in the photo.")
print("  Effect: lower entry loss, momentum aimed downstream. It HELPS. And it's the same")
print("  fitting family as the 'Y-T' overflow. Good practice; nothing adverse to model.")
