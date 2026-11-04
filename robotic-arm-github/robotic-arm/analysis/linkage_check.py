#!/usr/bin/env python3
"""
Checks the parallelogram gripper arm over its whole range of motion (pure Python, no dependencies).

  1. clearance between sticks that share a layer (sticks are 10 mm wide)
  2. clearance between each pin and the sticks it passes beside
  3. reach and lowest point
  4. worst-case gravity moment about the shoulder axle (empty and with a payload)
  5. how much a 0.5 mm length error tilts the forearm / palm

Run:  python3 analysis/linkage_check.py
"""
import math, itertools

# ---- geometry (mm) -----------------------------------------------------------
L1, L2, CR, KK = 100.0, 75.0, 25.0, 40.0        # upper arm, forearm, crank, leveling offset
HALF, CLEAR, PIN_R = 5.0, 1.5, 3.5              # stick half-width, required edge gap, pin + washer radius
SHOULDER = range(20, 101, 2)                    # upper arm angle above horizontal (deg)
FOREARM = range(-90, 21, 2)                     # forearm angle above horizontal (deg)
BEND = (20, 150)                                # allowed angle between upper arm and forearm
LAYER = {"AB": 0, "KF": 0, "AK": 1, "FH": 1, "DE": 2, "BF": 2, "CH": 2, "EBC": 3, "AD": 3}
PIVOT_LINKS = {"B": ["AB", "EBC", "BF"], "C": ["EBC", "CH"], "D": ["AD", "DE"], "E": ["EBC", "DE"],
               "K": ["AK", "KF"], "F": ["KF", "BF", "FH"], "H": ["FH", "CH"]}   # A has no pin (servo horns)
PIN_SPAN = {"B": (0, 3), "C": (2, 3), "D": (2, 3), "E": (2, 3), "K": (0, 1), "F": (0, 2), "H": (1, 2)}

def u(d): return (math.cos(math.radians(d)), math.sin(math.radians(d)))
def add(a, b): return (a[0] + b[0], a[1] + b[1])
def mul(a, s): return (a[0] * s, a[1] * s)

def geometry(t1, t2):
    A = (0.0, 0.0); B = mul(u(t1), L1); C = add(B, mul(u(t2), L2)); ph = t2 + 180
    D = mul(u(ph), CR); E = add(B, mul(u(ph), CR)); K = (KK, 0.0); F = (B[0] + KK, B[1]); H = (C[0] + KK, C[1])
    P = dict(A=A, B=B, C=C, D=D, E=E, K=K, F=F, H=H)
    S = dict(AB=(A, B), KF=(K, F), AK=(K, (K[0], -35.0)), FH=(F, H), DE=(D, E), BF=(B, F), CH=(C, H), EBC=(E, C), AD=(A, D))
    return P, S

def pt_seg(p, a, b):
    ab = (b[0]-a[0], b[1]-a[1]); ap = (p[0]-a[0], p[1]-a[1]); d = ab[0]**2 + ab[1]**2
    t = 0 if d == 0 else max(0, min(1, (ap[0]*ab[0] + ap[1]*ab[1]) / d))
    return math.hypot(p[0] - (a[0] + ab[0]*t), p[1] - (a[1] + ab[1]*t))

def seg_dist(p1, p2, q1, q2):
    def ccw(a, b, c): return (c[1]-a[1])*(b[0]-a[0]) - (b[1]-a[1])*(c[0]-a[0])
    d1, d2, d3, d4 = ccw(p1, p2, q1), ccw(p1, p2, q2), ccw(q1, q2, p1), ccw(q1, q2, p2)
    if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)): return 0.0
    return min(pt_seg(p1, q1, q2), pt_seg(p2, q1, q2), pt_seg(q1, p1, p2), pt_seg(q2, p1, p2))

def poses():
    for t1 in SHOULDER:
        for t2 in FOREARM:
            if BEND[0] <= t1 - t2 <= BEND[1]: yield t1, t2

def main():
    pair_min, pin_min = {}, {}; low_c = 1e9; tip_x = [1e9, -1e9]; n = 0
    for t1, t2 in poses():
        n += 1; P, S = geometry(t1, t2)
        for i, j in itertools.combinations(S, 2):
            if LAYER[i] == LAYER[j]: pair_min[(i, j)] = min(pair_min.get((i, j), 1e9), seg_dist(*S[i], *S[j]))
        for pv, (lo, hi) in PIN_SPAN.items():
            for m, l in LAYER.items():
                if m in PIVOT_LINKS[pv] or not lo <= l <= hi: continue
                pin_min[(pv, m)] = min(pin_min.get((pv, m), 1e9), pt_seg(P[pv], *S[m]))
        low_c = min(low_c, P["C"][1]); tip_x = [min(tip_x[0], P["H"][0]), max(tip_x[1], P["H"][0])]
    need = 2 * HALF + CLEAR
    print(f"poses checked: {n}  (shoulder 20-100, forearm -90..20, bend {BEND[0]}-{BEND[1]} deg)")
    print("\n1. Same-layer sticks, closest centre-line gap (sticks are 10 mm wide, need >= %.1f mm):" % need)
    for (i, j), d in sorted(pair_min.items(), key=lambda kv: kv[1])[:5]:
        print(f"   {i:>3} - {j:<3} {d:6.1f} mm  ({d - 2*HALF:4.1f} mm between edges)  {'OK' if d >= need else 'TOO CLOSE'}")
    print("\n2. Pins passing beside other sticks, closest distance (need >= %.1f mm):" % (HALF + PIN_R + CLEAR))
    for (pv, m), d in sorted(pin_min.items(), key=lambda kv: kv[1])[:5]:
        print(f"   pin {pv} - {m:<3} {d:6.1f} mm  {'OK' if d >= HALF + PIN_R + CLEAR else 'TOO CLOSE'}")
    print(f"\n3. Reach: palm end {tip_x[0]:.0f} to {tip_x[1]:.0f} mm from the axle; lowest point of the palm {low_c:.0f} mm below the axle")

    # 4. worst-case gravity moment about the axle (grams * cm); masses are estimates in grams
    def mid(a, b): return ((a[0]+b[0])/2, (a[1]+b[1])/2)
    worst = 0.0; worst_pose = None; payload_arm = 0.0
    for t1, t2 in poses():
        P, S = geometry(t1, t2); H = P["H"]
        parts = [(2.0, mid(*S["AB"])), (2.0, mid(*S["EBC"])), (2.0, mid(*S["DE"])), (2.0, mid(*S["KF"])), (1.5, mid(*S["FH"])),
                 (0.9, mid(*S["BF"])), (1.3, mid(*S["CH"])), (0.6, mid(*S["AD"])), (9.0, (H[0] + 16, H[1])), (4.0, (H[0] + 38, H[1])),
                 (1.5, mid(*S["EBC"]))] + [(0.35, P[k]) for k in "BCDEFHK"]
        m = sum(g * p[0] / 10 for g, p in parts)
        if m > worst: worst, worst_pose, payload_arm = m, (t1, t2), (H[0] + 40) / 10
    print(f"\n4. Gravity moment about the axle at the worst pose (shoulder/forearm {worst_pose}):")
    for load in (0, 10, 15, 20):
        print(f"   payload {load:2d} g: {(worst + load * payload_arm) / 1000:.2f} kg*cm   (half of the SG90's 1.8 kg*cm stall rating = 0.90)")

    # 5. tilt caused by a 0.5 mm length error in one rod
    def circ(centre, r, target, length, start):
        f = lambda a: math.hypot(centre[0] + r*math.cos(math.radians(a)) - target[0], centre[1] + r*math.sin(math.radians(a)) - target[1]) - length
        lo, hi = start - 20, start + 20
        if f(lo) * f(hi) > 0: return None
        for _ in range(50):
            mid_ = (lo + hi) / 2
            if f(lo) * f(mid_) <= 0: hi = mid_
            else: lo = mid_
        return (lo + hi) / 2
    errs = {"DE (tilts the forearm)": [], "KF (tilts the palm)": [], "FH (tilts the palm)": []}
    for t1, t2 in poses():
        if t1 % 4 or t2 % 4: continue
        P, S = geometry(t1, t2)
        a = circ(P["B"], CR, P["D"], L1 + 0.5, t2 + 180); errs["DE (tilts the forearm)"] += [abs(a - (t2 + 180))] if a is not None else []
        a = circ(P["B"], KK, P["K"], L1 + 0.5, 0); errs["KF (tilts the palm)"] += [abs(a)] if a is not None else []
        a = circ(P["C"], KK, P["F"], L2 + 0.5, 0); errs["FH (tilts the palm)"] += [abs(a)] if a is not None else []
    print("\n5. Tilt caused by a 0.5 mm length error:")
    for k, v in errs.items(): print(f"   {k:24s} {min(v):.1f} to {max(v):.1f} deg  (median {sorted(v)[len(v)//2]:.1f})")

if __name__ == "__main__":
    main()
