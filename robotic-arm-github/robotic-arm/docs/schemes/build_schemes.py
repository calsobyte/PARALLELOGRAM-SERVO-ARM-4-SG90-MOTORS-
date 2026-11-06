#!/usr/bin/env python3
"""Writes the scheme drawings (SVG) of the parallelogram gripper arm.
   side-view.svg, layer-stack-top-view.svg and gripper-scheme.svg  (millimetres in the model, px in the drawing)."""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
COL = ["#1D9E75", "#BA7517", "#7F77DD", "#D85A30"]
DARK = ["#0F6E56", "#854F0B", "#534AB7", "#993C1D"]
STYLE = ("<style>text{font-family:Helvetica,Arial,sans-serif}.ts{font-size:12px;fill:#5F5E5A}"
         ".th{font-size:14px;font-weight:600;fill:#1F1E1D}.tp{font-size:12px;font-weight:600;fill:#1F1E1D}</style>")

def wrap(inner, w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<title>{title}</title>{STYLE}<rect width="{w}" height="{h}" fill="#FFFFFF"/>{inner}</svg>')
def u(d): return (math.cos(math.radians(d)), math.sin(math.radians(d)))
def add(p, q): return (p[0]+q[0], p[1]+q[1])
def mul(p, s): return (p[0]*s, p[1]*s)

def pose(t1, t2, L1=100, L2=75, c=25, k=40):
    A = (0, 0); B = mul(u(t1), L1); C = add(B, mul(u(t2), L2)); ph = t2 + 180
    D = mul(u(ph), c); E = add(B, mul(u(ph), c)); K = (k, 0); F = (B[0]+k, B[1]); H = (C[0]+k, C[1])
    return dict(A=A, B=B, C=C, D=D, E=E, K=K, F=F, H=H, T=(k, -35))

# ------------------------------------------------------------------ side view
def side_view(t1=60, t2=-10):
    S = 2; AX, AY = 120, 390; P = pose(t1, t2)
    X = lambda p: AX + S*p[0]; Y = lambda p: AY - S*p[1]
    o = []
    o.append(f'<text class="th" x="20" y="28">Side view at shoulder {t1}°, forearm {t2}°. Layers: L0 front … L3 back</text>')
    o.append(f'<line x1="40" y1="{AY+100}" x2="650" y2="{AY+100}" stroke="#8F8D85" stroke-dasharray="6 4"/>')
    o.append(f'<text class="ts" x="650" y="{AY+118}" text-anchor="end">pick surface (50 mm below the axle)</text>')
    o.append(f'<rect x="60" y="{AY+70}" width="190" height="10" rx="2" fill="#E9E7DF" stroke="#8F8D85" stroke-width="0.5"/>')
    o.append(f'<text class="ts" x="155" y="{AY+92}" text-anchor="middle">turntable</text>')
    o.append(f'<rect x="{AX-12}" y="{AY-12}" width="24" height="56" rx="3" fill="#E9E7DF" stroke="#8F8D85"/>')
    o.append(f'<text class="ts" x="{AX}" y="{AY+60}" text-anchor="middle">arm servos</text>')
    poly = lambda pts: " ".join(f"{X(p):.1f},{Y(p):.1f}" for p in pts)
    o.append('<g fill="#888780" fill-opacity="0.12" stroke="#8F8D85" stroke-width="0.5" stroke-dasharray="4 3">'
             f'<polygon points="{poly([P["A"],P["D"],P["E"],P["B"]])}"/><polygon points="{poly([P["A"],P["K"],P["F"],P["B"]])}"/>'
             f'<polygon points="{poly([P["B"],P["F"],P["H"],P["C"]])}"/></g>')
    links = [("AB", 0, "A", "B"), ("KF", 0, "K", "F"), ("AK", 1, "K", "T"), ("FH", 1, "F", "H"),
             ("DE", 2, "D", "E"), ("BF", 2, "B", "F"), ("CH", 2, "C", "H"), ("E–B–C", 3, "E", "C"), ("AD", 3, "A", "D")]
    for layer in (3, 2, 1, 0):
        for n, l, a, b in links:
            if l == layer:
                o.append(f'<line x1="{X(P[a]):.1f}" y1="{Y(P[a]):.1f}" x2="{X(P[b]):.1f}" y2="{Y(P[b]):.1f}" stroke="{COL[l]}" stroke-width="7" stroke-linecap="round"/>')
    hx, hy = X(P["H"]), Y(P["H"])                       # gripper (side view: servo box, spine, one jaw)
    o.append(f'<rect x="{hx+12}" y="{hy-22.7}" width="45" height="45.4" rx="3" fill="#2D5DA8" stroke="#1F3F73"/>')
    o.append(f'<rect x="{hx+37}" y="{hy-22.7}" width="84" height="36" rx="2" fill="#888780" fill-opacity="0.6" stroke="#5F5E5A" stroke-dasharray="3 2"/>')
    o.append(f'<rect x="{hx+73}" y="{hy-26.7}" width="48" height="40" rx="2" fill="#378ADD" stroke="#185FA5"/>')
    o.append(f'<rect x="{hx+35}" y="{hy-32.7}" width="92" height="6" rx="1" fill="#B5D4F4" stroke="#378ADD"/>')
    o.append(f'<text class="ts" x="{hx+12}" y="{hy+44}">gripper (jaws open sideways)</text>')
    for n, l, a, b in links:
        mx, my = (X(P[a])+X(P[b]))/2, (Y(P[a])+Y(P[b]))/2 + {'BF': -16, 'E–B–C': 14}.get(n, 0); w = 10 + 6.5*len(n)
        o.append(f'<rect x="{mx-w/2:.1f}" y="{my-8:.1f}" width="{w}" height="16" rx="4" fill="#FFFFFF" stroke="{COL[l]}" stroke-width="1.2"/>')
        o.append(f'<text class="tp" x="{mx:.1f}" y="{my+4:.1f}" text-anchor="middle">{n}</text>')
    for n in "ABCDEKFH":
        o.append(f'<circle cx="{X(P[n]):.1f}" cy="{Y(P[n]):.1f}" r="8" fill="#E9E7DF" stroke="#1F1E1D" stroke-width="1.2"/>')
        o.append(f'<text class="tp" x="{X(P[n]):.1f}" y="{Y(P[n])+4:.1f}" text-anchor="middle">{n}</text>')
    names = [("AB", "upper arm", 0), ("KF", "leveling rod", 0), ("AK", "fixed post", 1), ("FH", "leveling rod", 1),
             ("DE", "elbow rod", 2), ("BF", "link", 2), ("CH", "palm", 2), ("E–B–C", "forearm", 3), ("AD", "crank", 3)]
    for i, (n, d, l) in enumerate(names):
        cx, cy = (20, 50 + 20*i) if i < 5 else (250, 50 + 20*(i-5))
        o.append(f'<rect x="{cx}" y="{cy}" width="12" height="12" rx="2" fill="{COL[l]}"/>')
        o.append(f'<text class="ts" x="{cx+20}" y="{cy+10}"><tspan class="tp">{n}</tspan>  {d} (L{l})</text>')
    o.append('<text class="ts" x="250" y="150">Lengths (mm): AB 100 · E–B 25 · B–C 75 · AD 25</text>')
    o.append('<text class="ts" x="250" y="166">DE 100 · KF 100 · FH 75 · AK, BF, CH 40</text>')
    return wrap("".join(o), 680, 530, "Side view of the parallelogram gripper arm")

# ------------------------------------------------------------------ top view of the layer stack
def top_view(t1=60, t2=-10):
    s, Zs = 2.6, 5.2; xS, y0 = 90, 190; P = pose(t1, t2)
    X = lambda m: xS + s*m; Yw = lambda w: y0 + Zs*w
    c1, c2 = math.cos(math.radians(t1)), math.cos(math.radians(t2)); cphi = math.cos(math.radians(t2+180))
    o = [f'<text class="th" x="20" y="22">Top view of the layer stack (shoulder {t1}°, forearm {t2}°). The arm points right.</text>']
    o.append(f'<rect x="25" y="34" width="208" height="395" rx="6" fill="#F5F4EF" stroke="#8F8D85" stroke-width="0.8" stroke-dasharray="5 4"/>')
    o.append('<text class="ts" x="30" y="446">turntable (seen from above)</text><text class="ts" x="32" y="54">FRONT</text><text class="ts" x="32" y="418">BACK</text>')
    o.append(f'<line x1="{X(0)}" y1="69" x2="{X(0)}" y2="389" stroke="#8F8D85" stroke-dasharray="5 4"/><text class="ts" x="114" y="84">A: axle, no pin</text>')
    for yy, hh in ((69, 108), (270.6, 118)):                         # arm servos outside the stack
        o.append(f'<rect x="{X(-6.1)}" y="{yy}" width="{s*12.2}" height="{hh}" rx="3" fill="#E9E7DF" stroke="#8F8D85"/>')
    o.append(f'<rect x="76" y="177" width="28" height="13" fill="#B4B2A9" stroke="#888780" stroke-width="0.8"/>')
    o.append(f'<rect x="76" y="260.2" width="28" height="10.4" fill="#B4B2A9" stroke="#888780" stroke-width="0.8"/>')
    o.append('<text class="ts" x="114" y="116">shoulder servo (front)</text><text class="ts" x="114" y="134">drives AB on L0</text>')
    o.append('<text class="ts" x="114" y="330">elbow servo (back)</text><text class="ts" x="114" y="348">drives AD on L3</text>')
    strips = [("AB", 0, -5*c1, P["B"][0]+5*c1), ("KF", 0, P["K"][0]-5*c1, P["F"][0]+5*c1), ("AK", 1, P["K"][0]-5, P["K"][0]+5),
              ("FH", 1, P["F"][0]-5*c2, P["H"][0]+5*c2), ("DE", 2, P["D"][0]-5*c1, P["E"][0]+5*c1),
              ("BF", 2, P["B"][0]-5, P["F"][0]+5), ("CH", 2, P["C"][0]-5, P["C"][0]+65),
              ("E–B–C", 3, P["E"][0]-5*c2, P["C"][0]+5*c2), ("AD", 3, P["D"][0]+5*cphi, 0-5*cphi)]
    LABEL_X = {"AB": 14, "KF": 72, "AK": None, "FH": 108, "DE": 12, "BF": 68, "CH": 145, "E–B–C": 75, "AD": -12}
    for n, l, x1, x2 in strips:
        y = Yw(3.5*l)
        o.append(f'<rect x="{X(x1):.1f}" y="{y:.1f}" width="{s*(x2-x1):.1f}" height="{Zs*3:.1f}" rx="3" fill="{COL[l]}" stroke="{DARK[l]}"/>')
        if n == "AK": o.append(f'<text class="tp" x="173" y="{Yw(7)+Zs*1.5+4:.1f}" text-anchor="middle" style="fill:{COL[1]}">AK</text>')
        else: o.append(f'<text class="tp" x="{X(LABEL_X[n]):.1f}" y="{y+Zs*1.5+4:.1f}" text-anchor="middle" style="fill:#ffffff">{n}</text>')
    spans = dict(B=(0, 3), C=(2, 3), D=(2, 3), E=(2, 3), K=(0, 1), F=(0, 2), H=(1, 2))
    for n, (lo, hi) in spans.items():
        x = X(P[n][0]); ya = Yw(3.5*lo); yb = Yw(3.5*hi + 3)
        o.append(f'<rect x="{x-4:.1f}" y="{ya:.1f}" width="8" height="{yb-ya:.1f}" fill="#A67C52" stroke="#7A5A36" stroke-width="0.8"/>')
        for yy in (ya-6, yb+6): o.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="6" fill="#C9C7BE" stroke="#888780" stroke-width="0.8"/>')
        o.append(f'<text class="tp" x="{x:.1f}" y="{ya-16:.1f}" text-anchor="middle">{n}</text>')
    o.append(f'<circle cx="{X(0)}" cy="{Yw(6.75):.1f}" r="7" fill="none" stroke="#1F1E1D" stroke-width="1.2"/>'
             f'<line x1="{X(0)-6}" y1="{Yw(6.75):.1f}" x2="{X(0)+6}" y2="{Yw(6.75):.1f}" stroke="#1F1E1D"/>'
             f'<line x1="{X(0)}" y1="{Yw(6.75)-6:.1f}" x2="{X(0)}" y2="{Yw(6.75)+6:.1f}" stroke="#1F1E1D"/>')
    hx = P["H"][0]; sh = hx + 22.5                                   # gripper servo on the palm's back face (w = 10 .. 22.2)
    o.append(f'<rect x="{X(hx+6):.1f}" y="{Yw(10):.1f}" width="{s*22.5:.1f}" height="{Zs*12.2:.1f}" rx="3" fill="#2D5DA8" stroke="#1F3F73"/>')
    o.append(f'<rect x="{X(sh-4):.1f}" y="{Yw(22.2):.1f}" width="{s*42:.1f}" height="{Zs*3:.1f}" fill="#888780" stroke="#5F5E5A"/>')
    th = math.radians(-35); ux, uw = math.cos(th), math.sin(th); nx, nw = -uw, ux
    pts = []
    for r, side in ((14, -1), (38, -1), (38, 1), (14, 1)):
        px, pw = sh + r*ux + side*1.5*nx, 16.1 + r*uw + side*1.5*nw; pts.append(f"{X(px):.1f},{Yw(pw):.1f}")
    o.append(f'<polygon points="{" ".join(pts)}" fill="#378ADD" stroke="#185FA5"/>')
    o.append(f'<circle cx="{X(sh):.1f}" cy="{Yw(16.1):.1f}" r="5" fill="#1F1E1D"/>')
    o.append(f'<text class="ts" x="{X(hx+6):.1f}" y="{Yw(26)+14:.1f}">gripper servo and jaws</text>')
    for i, (n, d, l) in enumerate([("L0 front", "AB upper arm, KF rod", 0), ("L1", "AK post, FH rod", 1), ("L2", "DE rod, BF link, CH palm", 2), ("L3 back", "E–B–C forearm, AD crank", 3)]):
        o.append(f'<rect x="440" y="{50+22*i}" width="12" height="12" rx="2" fill="{COL[l]}"/><text class="ts" x="460" y="{60+22*i}"><tspan class="tp">{n}</tspan>  {d}</text>')
    o.append('<text class="ts" x="260" y="388">Tan bars: bamboo pins. Grey dots: glue stops.</text>')
    o.append('<text class="ts" x="260" y="406">⊕ marks the vertical rotation axis of the base.</text>')
    o.append('<text class="ts" x="260" y="424">Thickness is drawn 2× so the layers are readable.</text>')
    return wrap("".join(o), 680, 460, "Top view of the layer stack")

if __name__ == "__main__":
    for name, svg in (("side-view.svg", side_view()), ("layer-stack-top-view.svg", top_view())):
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(svg); print("wrote", name)
