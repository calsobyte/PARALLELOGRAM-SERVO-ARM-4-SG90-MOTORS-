#!/usr/bin/env python3
"""
3D model of the parallelogram-linkage gripper arm.

Writes STL files (cad/stl/) and PNG renders (docs/images/) from one parametric
description. Units are millimetres.

Axes: X = forward (arm direction), Y = up, Z = towards the viewer in the front
view (front layer L0 has the largest Z, back layer L3 the smallest).

Usage:  python3 cad/generate_cad.py          (needs numpy and pillow)
"""
import math, os, struct
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STL_DIR = os.path.join(ROOT, "cad", "stl")
IMG_DIR = os.path.join(ROOT, "docs", "images")
os.makedirs(STL_DIR, exist_ok=True); os.makedirs(IMG_DIR, exist_ok=True)

# ---------------------------------------------------------------- parameters
L_UPPER, L_FORE, CRANK, K_OFF = 100.0, 75.0, 25.0, 40.0   # link lengths (mm)
THK, PITCH, STICK_W = 3.0, 3.5, 10.0                       # laminate, layer pitch, stick width
HOLE_R = 1.6                                               # 3.2 mm holes for 3 mm pins
THETA1, THETA2 = 62.0, -18.0                               # pose: upper arm / forearm angle
JAW_DEG = 35.0                                             # gripper jaw angle (closed +2, open +55, away from the palm)
LAYER_COL = ["#1D9E75", "#BA7517", "#7F77DD", "#D85A30"]   # L0 .. L3

def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ---------------------------------------------------------------- primitives
def rotz(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
def roty(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

_FACES = [((1,-1,-1),(1,1,-1),(1,1,1),(1,-1,1)), ((-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1)),
          ((-1,1,-1),(-1,1,1),(1,1,1),(1,1,-1)), ((-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1)),
          ((-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)), ((-1,-1,-1),(-1,1,-1),(1,1,-1),(1,-1,-1))]

def obox(center, half, R=None):
    """Oriented box. half = half-extents in the local frame, R = local->world rotation."""
    R = np.eye(3) if R is None else R
    half = np.array(half, float); c = np.array(center, float); tris = []
    for q in _FACES:
        p = [R @ (np.array(v) * half) + c for v in q]
        tris += [[p[0], p[1], p[2]], [p[0], p[2], p[3]]]
    return np.array(tris)

def ring_pts(cx, cy, r, n):
    return [(cx + r * math.cos(2*math.pi*k/n), cy + r * math.sin(2*math.pi*k/n)) for k in range(n)]

def cyl_z(cx, cy, r, z0, z1, n=20):
    t = []; P = ring_pts(cx, cy, r, n)
    for k in range(n):
        a, b = P[k], P[(k+1) % n]
        t += [[(*a, z0), (*b, z0), (*b, z1)], [(*a, z0), (*b, z1), (*a, z1)],
              [(cx, cy, z1), (*a, z1), (*b, z1)], [(cx, cy, z0), (*b, z0), (*a, z0)]]
    return np.array(t, float)

def ring_z(cx, cy, r_in, r_out, z0, z1, n=24):
    t = []; O = ring_pts(cx, cy, r_out, n); I = ring_pts(cx, cy, r_in, n)
    for k in range(n):
        k2 = (k+1) % n
        t += [[(*O[k], z0), (*O[k2], z0), (*O[k2], z1)], [(*O[k], z0), (*O[k2], z1), (*O[k], z1)],
              [(*I[k2], z0), (*I[k], z0), (*I[k], z1)], [(*I[k2], z0), (*I[k], z1), (*I[k2], z1)],
              [(*I[k], z1), (*O[k], z1), (*O[k2], z1)], [(*I[k], z1), (*O[k2], z1), (*I[k2], z1)],
              [(*I[k], z0), (*O[k2], z0), (*O[k], z0)], [(*I[k], z0), (*I[k2], z0), (*O[k2], z0)]]
    return np.array(t, float)

def sphere(c, r, nlat=8, nlon=14):
    t = []
    def P(i, j):
        th = math.pi * i / nlat; ph = 2 * math.pi * j / nlon
        return (c[0] + r*math.sin(th)*math.cos(ph), c[1] + r*math.cos(th), c[2] + r*math.sin(th)*math.sin(ph))
    for i in range(nlat):
        for j in range(nlon):
            a, b, cc, d = P(i, j), P(i+1, j), P(i+1, j+1), P(i, j+1)
            t.append([a, d, cc]); t.append([a, cc, b])
    return np.array(t, float)

def plate(origin, d, length, holes, z0, z1, hole_r=HOLE_R, width=STICK_W, n=32):
    """Flat stick (laminated link) in the XY plane with round holes on its centre line.
    origin = 2D start of the stick, d = unit direction, holes = distances from the start."""
    half = width / 2; holes = sorted(holes); V = []; T = []
    def addv(p): V.append(p); return len(V) - 1
    tiles = []
    for s in holes:
        ring, bnd = [], []
        for k in range(n):
            th = 2*math.pi*k/n; c, sn = math.cos(th), math.sin(th); m = max(abs(c), abs(sn))
            ring.append(addv((s + hole_r*c, hole_r*sn))); bnd.append(addv((s + half*c/m, half*sn/m)))
        tiles.append((ring, bnd))
    for ring, bnd in tiles:
        for k in range(n):
            k2 = (k+1) % n
            T.append((ring[k], bnd[k], bnd[k2])); T.append((ring[k], bnd[k2], ring[k2]))
    q = n // 8                                       # square corners sit at k = q, 3q, 5q, 7q
    right = lambda b: [b[k % n] for k in range(7*q, 9*q+1)]            # bottom -> top
    left  = lambda b: [b[k] for k in range(5*q, 3*q-1, -1)]            # bottom -> top
    def zipper(L, R):
        i = j = 0
        while i < len(L)-1 or j < len(R)-1:
            if i == len(L)-1: adv = 'R'
            elif j == len(R)-1: adv = 'L'
            else: adv = 'L' if V[L[i+1]][1] <= V[R[j+1]][1] else 'R'
            if adv == 'R': T.append((L[i], R[j], R[j+1])); j += 1
            else: T.append((L[i], R[j], L[i+1])); i += 1
    for (r1, b1), (r2, b2) in zip(tiles[:-1], tiles[1:]):
        if V[b2[0]][0] - V[b1[0]][0] > 2*half + 1e-6: zipper(right(b1), left(b2))
    ends = None
    if length - (holes[-1] + half) > 1e-6:           # plain stick beyond the last hole
        e0 = addv((length, -half)); e1 = addv((length, half)); zipper(right(tiles[-1][1]), [e0, e1]); ends = [e0, e1]
    loop = []
    for ring, bnd in tiles: loop += [bnd[k] for k in range(5*q, 7*q+1)]                    # bottom edge
    loop += ends if ends else [tiles[-1][1][k % n] for k in range(7*q+1, 9*q+1)]          # far end
    for ring, bnd in reversed(tiles): loop += [bnd[k] for k in range(q, 3*q+1)]            # top edge
    loop += [tiles[0][1][k] for k in range(3*q+1, 5*q)]                                    # near end
    clean = [loop[0]]
    for v in loop[1:]:
        if v != clean[-1]: clean.append(v)
    if clean[-1] == clean[0]: clean.pop()
    loops = [clean] + [list(reversed(r)) for r, _ in tiles]                                # holes run clockwise
    dd = np.array(d, float); perp = np.array([-dd[1], dd[0]]); o = np.array(origin, float)
    W3 = lambda v, z: (*(o + V[v][0]*dd + V[v][1]*perp), z)
    out = []
    for a, b, c in T:
        out.append([W3(a, z1), W3(b, z1), W3(c, z1)]); out.append([W3(a, z0), W3(c, z0), W3(b, z0)])
    for lp in loops:
        for i in range(len(lp)):
            a, b = lp[i], lp[(i+1) % len(lp)]
            out += [[W3(a, z0), W3(b, z0), W3(b, z1)], [W3(a, z0), W3(b, z1), W3(a, z1)]]
    return np.array(out, float)

def xf(tris, R=None, t=(0, 0, 0)):
    R = np.eye(3) if R is None else R
    return (tris.reshape(-1, 3) @ R.T + np.array(t)).reshape(-1, 3, 3)

# ---------------------------------------------------------------- the arm
def u2(deg): return np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))])
def zr(layer): w0 = PITCH * layer; return (-(w0 + THK), -w0)        # (z_min, z_max) of a layer

def build():
    parts = []
    def add(name, group, color, tris): parts.append(dict(name=name, group=group, color=color, tris=np.asarray(tris, float)))
    t1, t2 = THETA1, THETA2; phi = t2 + 180
    A = np.array([0., 0.]); B = L_UPPER*u2(t1); C = B + L_FORE*u2(t2)
    D = CRANK*u2(phi); E = B + CRANK*u2(phi); K = np.array([K_OFF, 0.])
    F = B + np.array([K_OFF, 0.]); H = C + np.array([K_OFF, 0.])
    P = dict(A=A, B=B, C=C, D=D, E=E, K=K, F=F, H=H)

    def stick(name, layer, p_from, p_to, holes_at, a_margin=5.0, length=None):
        d = (p_to - p_from) / np.linalg.norm(p_to - p_from)
        origin = p_from - a_margin * d
        hs = [a_margin + float(np.dot(h - p_from, d)) for h in holes_at]
        ln = length if length else max(hs) + 5.0
        z0, z1 = zr(layer)
        add(name, f"L{layer}", LAYER_COL[layer], plate(origin, d, ln, hs, z0, z1))

    stick("AB_upper_arm", 0, A, B, [A, B])
    stick("KF_leveling_rod", 0, K, F, [K, F])
    stick("FH_leveling_rod", 1, F, H, [F, H])
    stick("DE_elbow_rod", 2, D, E, [D, E])
    stick("BF_link", 2, B, F, [B, F])
    stick("CH_palm", 2, C, H, [C, H], length=75.0)
    stick("EBC_forearm", 3, E, C, [E, B, C])
    stick("AD_crank", 3, A, D, [A, D])
    z0, z1 = zr(1)                                                   # fixed post AK (L1)
    add("AK_fixed_post", "L1", LAYER_COL[1], plate(np.array([K[0], 5.0]), (0, -1), 40.0, [5.0], z0, z1))

    # pins, glue balls, washers
    spans = dict(B=(0, 3), C=(2, 3), D=(2, 3), E=(2, 3), K=(0, 1), F=(0, 2), H=(1, 2))
    pin_t, ball_t, wash_t = [], [], []
    for n_, (lo, hi) in spans.items():
        x, y = P[n_]; zb, zf = zr(hi)[0], zr(lo)[1]
        pin_t.append(cyl_z(x, y, 1.5, zb - 1.6, zf + 1.6, 16))
        for zc in (zb - 2.4, zf + 2.4): ball_t.append(sphere((x, y, zc), 2.3))
        wash_t.append(ring_z(x, y, 1.6, 3.5, zb - 0.5, zb)); wash_t.append(ring_z(x, y, 1.6, 3.5, zf, zf + 0.5))
        for k in range(lo, hi):
            wash_t.append(ring_z(x, y, 1.6, 3.5, zr(k+1)[1], zr(k)[0]))
    wash_t.append(ring_z(B[0], B[1], 1.6, 3.5, zr(1)[0], zr(1)[1]))      # spacer at B in layer L1
    add("pins", "hardware", "#A67C52", np.concatenate(pin_t))
    add("glue_stops", "hardware", "#D8D6CC", np.concatenate(ball_t))
    add("washers_spacer", "hardware", "#9A9890", np.concatenate(wash_t))

    # servos and horns (shoulder in front of L0, elbow behind L3)
    SERVO = "#2D5DA8"; WHITE = "#E8E8E8"
    add("shoulder_servo", "base", SERVO, obox((0, -5.25, 2 + 11.35), (6.1, 11.25, 11.35)))
    add("elbow_servo", "base", SERVO, obox((0, -5.25, -(15.5 + 11.35)), (6.1, 11.25, 11.35)))
    add("shoulder_horn", "base", WHITE, obox((*(4.5*u2(t1)), 1.0), (7.5, 3.0, 1.0), rotz(math.radians(t1))))
    add("elbow_horn", "base", WHITE, obox((*(4.5*u2(phi)), -14.5), (7.5, 3.0, 1.0), rotz(math.radians(phi))))
    # turntable, risers, base servo, base board
    WOOD = "#C8A26B"
    add("turntable", "base", WOOD, obox((15, -37, -7), (40, 2, 37)))
    add("risers", "base", WOOD, np.concatenate([obox((0, -25.75, 13.35), (6.1, 9.25, 11.35)),
                                                   obox((0, -25.75, -26.85), (6.1, 9.25, 11.35))]))
    add("base_servo", "base", SERVO, obox((0, -50.35, -6.75), (11.25, 11.35, 6.1)))
    add("base_board", "base", WOOD, obox((10, -64, -5), (60, 2, 45)))

    # ---- gripper: fixed jaw plate glued face to face onto the palm, servo clamped onto that plate
    hx, hy = H; sx = hx + 22.5; zc = -19.1
    add("fixed_jaw", "gripper", "#888780", obox((hx + 32.25, hy + 2.35, -11.5), (28.25, 9.0, 1.5)))   # X hx+4 .. hx+60.5
    add("gripper_servo", "gripper", SERVO, obox((hx + 17.25, hy, zc), (11.25, 11.35, 6.1)))
    th = math.radians(JAW_DEG); Ry = roty(th); dirv = np.array([math.cos(th), 0, -math.sin(th)])
    def along(r, dy=0.0, dz=0.0):                                     # point at distance r along the jaw
        return np.array([sx, hy + dy, zc]) + r * dirv + dz * np.array([math.sin(th), 0, math.cos(th)])
    add("jaw_horn", "gripper", WHITE, obox(along(4.5, 12.35), (7.5, 1.0, 3.0), Ry))
    add("jaw_spine", "gripper", "#B5D4F4", obox(along(18, 14.85), (23, 1.5, 5.0), Ry))
    add("moving_jaw", "gripper", "#378ADD", obox(along(26, 3.35), (12, 10.0, 1.5), Ry))
    add("moving_pad", "gripper", "#E0B84C", obox(along(26, 4.0, 3.0), (10, 6.0, 1.5), Ry))
    add("fixed_pad", "gripper", "#E0B84C", obox((sx + 25, hy + 4.0, -14.5), (11, 6.0, 1.5)))
    tx = hx + 11.0                                                    # zip tie around palm, plate and servo
    add("zip_tie", "gripper", "#333333", np.concatenate([
        obox((tx, hy + 11.85, -16.1), (1.25, 0.5, 9.6)), obox((tx, hy - 11.85, -16.1), (1.25, 0.5, 9.6)),
        obox((tx, hy, -25.7), (1.25, 12.35, 0.5)), obox((tx, hy, -6.5), (1.25, 12.35, 0.5))]))
    return parts, P

# ---------------------------------------------------------------- STL writer
def write_stl(path, tris, name="part"):
    tris = np.asarray(tris, np.float32).reshape(-1, 3, 3)
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]).astype(np.float64)
    ln = np.linalg.norm(n, axis=1); ok = ln > 1e-12
    tris, n, ln = tris[ok], n[ok], ln[ok]; n = (n / ln[:, None]).astype(np.float32)
    rec = np.zeros(len(tris), dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
    rec["n"], rec["v"] = n, tris
    with open(path, "wb") as f:
        f.write(name.encode()[:80].ljust(80, b" ")); f.write(struct.pack("<I", len(tris))); f.write(rec.tobytes())
    return len(tris)

# ---------------------------------------------------------------- renderer
def render(items, cam, target, up=(0, 1, 0), size=(1600, 1000), fov=24.0, ortho=None, ss=2, outline=True):
    """items: list of (tris, '#rrggbb'). Flat-shaded z-buffer render with part outlines."""
    W, Hh = size[0]*ss, size[1]*ss
    cam = np.array(cam, float); target = np.array(target, float)
    f = target - cam; f /= np.linalg.norm(f); r = np.cross(f, up); r /= np.linalg.norm(r); u = np.cross(r, f)
    light = -f + 0.5*u - 0.3*r; light /= np.linalg.norm(light)
    img = np.full((Hh, W, 3), 255, np.float32); zbuf = np.full((Hh, W), np.inf, np.float32); idb = np.full((Hh, W), -1, np.int32)
    focal = (Hh/2) / math.tan(math.radians(fov)/2)
    for pid, (tris, col) in enumerate(items):
        base = np.array(hexrgb(col), np.float32)
        d = tris.reshape(-1, 3) - cam; x, y, z = d @ r, d @ u, d @ f
        if ortho: sx, sy = x*ortho*ss + W/2, -y*ortho*ss + Hh/2
        else: sx, sy = x/z*focal + W/2, -y/z*focal + Hh/2
        S = np.stack([sx, sy, z], 1).reshape(-1, 3, 3)
        nrm = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]); l = np.linalg.norm(nrm, axis=1); l[l == 0] = 1; nrm /= l[:, None]
        to_cam = cam - tris.mean(1); nrm = np.where((nrm*to_cam).sum(1)[:, None] < 0, -nrm, nrm)
        shade = 0.42 + 0.58*np.clip(nrm @ light, 0, 1)
        for tri, sh in zip(S, shade):
            if (tri[:, 2] <= 0.1).any(): continue
            x0, y0 = tri[0, :2]; x1, y1 = tri[1, :2]; x2, y2 = tri[2, :2]
            den = (y1-y2)*(x0-x2) + (x2-x1)*(y0-y2)
            if abs(den) < 1e-9: continue
            xa, xb = int(max(0, math.floor(min(x0, x1, x2)))), int(min(W-1, math.ceil(max(x0, x1, x2))))
            ya, yb = int(max(0, math.floor(min(y0, y1, y2)))), int(min(Hh-1, math.ceil(max(y0, y1, y2))))
            if xa > xb or ya > yb: continue
            gx, gy = np.meshgrid(np.arange(xa, xb+1) + 0.5, np.arange(ya, yb+1) + 0.5)
            w0 = ((y1-y2)*(gx-x2) + (x2-x1)*(gy-y2)) / den; w1 = ((y2-y0)*(gx-x2) + (x0-x2)*(gy-y2)) / den; w2 = 1 - w0 - w1
            m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            if not m.any(): continue
            zz = w0*tri[0, 2] + w1*tri[1, 2] + w2*tri[2, 2]
            zs = zbuf[ya:yb+1, xa:xb+1]; m &= zz < zs
            if not m.any(): continue
            zs[m] = zz[m]; img[ya:yb+1, xa:xb+1][m] = base*sh; idb[ya:yb+1, xa:xb+1][m] = pid
    if outline:
        e = np.zeros(idb.shape, bool)
        e[:, 1:] |= idb[:, 1:] != idb[:, :-1]; e[1:, :] |= idb[1:, :] != idb[:-1, :]
        e &= idb >= 0
        e2 = e.copy(); e2[:, 1:] |= e[:, :-1]; e2[1:, :] |= e[:-1, :]
        img[e2] = img[e2]*0.35
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize(size, Image.LANCZOS)

def main():
    parts, P = build()
    groups = {}
    for p in parts: groups.setdefault(p["group"], []).append(p)
    nt = write_stl(os.path.join(STL_DIR, "arm_assembly.stl"), np.concatenate([p["tris"] for p in parts]), "arm_assembly")
    print("arm_assembly.stl", nt, "triangles")
    for g, fname in [("L0", "layer0_front"), ("L1", "layer1"), ("L2", "layer2"), ("L3", "layer3_back"),
                     ("hardware", "pins_washers_glue_stops"), ("gripper", "gripper"), ("base", "base_and_servos")]:
        print(fname, write_stl(os.path.join(STL_DIR, fname + ".stl"), np.concatenate([p["tris"] for p in groups[g]]), fname))
    allitems = [(p["tris"], p["color"]) for p in parts]
    centre = np.array([78.0, 18.0, -8.0])
    def az(a, e, dist):
        a, e = math.radians(a), math.radians(e)
        return centre + dist*np.array([math.sin(a)*math.cos(e), math.sin(e), math.cos(a)*math.cos(e)])
    render(allitems, az(38, 22, 540), centre, fov=26).save(os.path.join(IMG_DIR, "render_iso.png"))
    render(allitems, az(0, 0, 900), centre, ortho=3.4).save(os.path.join(IMG_DIR, "render_side.png"))
    render(allitems, centre + np.array([0, 900, 0]), centre, up=(0, 0, -1), size=(1600, 900), ortho=3.4).save(os.path.join(IMG_DIR, "render_top.png"))
    gp = np.array([P['H'][0] + 30, P['H'][1], -16.0])
    gitems = [(q['tris'], q['color']) for q in parts if q['group'] == 'gripper' or q['name'] == 'CH_palm']
    render(gitems, gp + 170*np.array([0.62, 0.50, -0.62]), gp, size=(1400, 1000), fov=24).save(os.path.join(IMG_DIR, "render_gripper.png"))
    ex = []
    for p in parts:
        if p["group"] in ("L0", "L1", "L2", "L3"): dz = -30.0*int(p["group"][1])
        elif p["name"] in ("shoulder_servo", "shoulder_horn"): dz = 30.0
        elif p["name"] in ("elbow_servo", "elbow_horn"): dz = -30.0*3 - 30.0
        else: continue
        ex.append((xf(p["tris"], t=(0, 0, dz)), p["color"]))
    ec = np.array([75.0, 25.0, -42.0])
    render(ex, ec + 560*np.array([0.93, 0.30, 0.36]), ec, size=(1600, 1000), fov=24).save(os.path.join(IMG_DIR, "render_exploded.png"))
    print("renders written")

if __name__ == "__main__":
    main()
