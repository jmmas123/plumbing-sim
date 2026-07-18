import math
IN=0.0254; C=0.95
def seg(y,D):
    if y<=0: return (0,0,0)
    if y>=D: return (math.pi*D*D/4, math.pi*D, 2*math.pi)
    th=2*math.acos(1-2*y/D); return (D*D/8*(th-math.sin(th)), D*th/2, th)
def sect(y,D,hs):
    hs=max(0,min(hs,D*0.9))
    if y<=hs: return (1e-9,1e-9)
    ay,py,_=seg(min(y,D),D); as_,ps,ts=seg(hs,D)
    a=ay-as_; chord=D*math.sin(ts/2) if hs>0 else 0
    p=(py-ps)+chord; return (max(a,1e-9),max(a/max(p,1e-9),1e-9))
def cap(D,S,n,hs=0):
    a,r=sect(D,D,hs); return (1/n)*a*r**(2/3)*math.sqrt(max(S,1e-6))*1000

print("LEADER RATINGS (IPC 1106.3): 4\"=12.1  6\"=35.5  8\"=76.2 L/s")
print("=> switching boca tubos 4\"->6\" nearly TRIPLES per-drain capacity\n")

print("CANALETA (open-channel) conveyance, Manning n=0.013, level->0.1% water-surface slope")
for nm,w,dep in [("single 40x14",0.40,0.14),("double 50x17",0.50,0.17)]:
    a=w*dep; r=a/(w+2*dep)
    q=(1/0.013)*a*r**(2/3)*math.sqrt(0.001)*1000
    print(f"  {nm:<14} area {a*1e4:.0f} cm2  Rh {r*100:.1f} cm  ->  ~{q:.0f} L/s if nearly level")
print("  (a near-level canaleta conveys very little; it is a COLLECTION trough, the")
print("   boca tubos do the vertical removal. Its DEPTH is the freeboard that matters.)\n")

print("FLOOD THRESHOLD vs canaleta DEPTH  (8\" collector @1%, per-collector area)")
# quick steady check: flood when HGL (crown + friction rise) exceeds canaleta edge
def flood_i(area, D_in, S, n, gdep, hf, nb, Ls_share=0):
    D=D_in*IN
    lo,hi=5,600
    for _ in range(50):
        i=(lo+hi)/2
        Qtot=C*(i/1000/3600)*area
        # far-end HGL above crown ~ Sf0*L/3 (tapering), plus surcharge if over cap
        Qc=cap(D,S,n)/1000
        if Qtot<=Qc:
            rise=S*(Qtot/Qc)**2*70/3   # friction rise, still free surface-ish
            hgl_above_crown=max(0,rise-D)  # crude
            over = rise > (hf+gdep+D)  # very rough
        else:
            # surcharged: climb ~ how far over capacity
            over = (Qtot/Qc-1)*0.5 > (hf+gdep)  # crude proxy
        if over: hi=i
        else: lo=i
    return hi
for gdep in (0.14,0.17,0.25):
    print(f"  canaleta depth {gdep*100:.0f} cm: (deeper = more freeboard = floods later)")
