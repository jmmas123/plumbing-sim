"""First-principles capacity check. No SWMM, no libraries - just Manning + Rational."""
import math

def manning_full(D_in, S, n):
    """Full-bore capacity of a circular pipe. Q = (1/n) A R^(2/3) S^(1/2)."""
    D = D_in * 0.0254
    A = math.pi * D**2 / 4
    R = D / 4                      # hydraulic radius of a full circular pipe
    V = (1.0/n) * R**(2.0/3.0) * math.sqrt(S)
    return A*V*1000, V             # L/s, m/s

print("=" * 74)
print("PIPE CAPACITY - Manning, full bore  (PVC: n=0.009 smooth ... 0.011 aged/derated)")
print("=" * 74)
print(f"{'Dia':>5} {'Slope':>6} | {'Q @n=.009':>10} {'Q @n=.011':>10} | {'V @n=.011':>9}")
for D_in in (4, 6, 8, 10):
    for S in (0.005, 0.01, 0.02):
        q9,_ = manning_full(D_in, S, 0.009)
        q11,v11 = manning_full(D_in, S, 0.011)
        print(f'{D_in:>4}" {S*100:>5.1f}% | {q9:>7.1f} L/s {q11:>7.1f} L/s | {v11:>6.2f} m/s')

print()
print("=" * 74)
print("THE KEY COMPARISON: does 8\" -> 10\" matter?   (both @ 1%)")
print("=" * 74)
for n in (0.009, 0.011):
    q8,_  = manning_full(8, 0.01, n)
    q10,_ = manning_full(10, 0.01, n)
    print(f"  n={n}:  8\" = {q8:5.1f} L/s   ->   10\" = {q10:5.1f} L/s   "
          f"= +{(q10/q8-1)*100:.0f}% capacity")

print()
print("=" * 74)
print("ROOF AREA a single pipe can serve  (Rational Q=CiA, C=0.95 for metal roof)")
print("=" * 74)
C = 0.95
print(f"{'intensity':>10} | " + " | ".join(f'{d}\" @1%'.rjust(9) for d in (6,8,10)))
for i_mmh in (50, 75, 100, 125, 150, 175, 200):
    row = []
    for D_in in (6, 8, 10):
        q,_ = manning_full(D_in, 0.01, 0.011)      # L/s
        area = (q/1000) / (C * i_mmh/1000/3600)    # m2
        row.append(f'{area:>7.0f} m2')
    print(f'{i_mmh:>7} mm/h | ' + " | ".join(row))

print()
print("=" * 74)
print("INVERSE: flow generated per 1000 m2 of roof")
print("=" * 74)
for i_mmh in (50, 100, 150, 200):
    q = C * (i_mmh/1000/3600) * 1000 * 1000        # L/s per 1000 m2
    print(f'  {i_mmh:>3} mm/h  ->  {q:>6.1f} L/s per 1000 m2')
