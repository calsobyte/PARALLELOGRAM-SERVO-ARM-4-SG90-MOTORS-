#!/usr/bin/env python3
"""Writes gripper-scheme.svg: top view and front view of the single-moving-jaw gripper.
Layout: fixed jaw plate glued face to face onto the palm, servo clamped onto that plate with a zip tie,
spine on the horn, moving jaw plate hanging from the spine, opening away from the palm."""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = ("<style>text{font-family:Helvetica,Arial,sans-serif}.ts{font-size:12px;fill:#5F5E5A}"
         ".th{font-size:14px;font-weight:600;fill:#1F1E1D}.tp{font-size:12px;font-weight:600;fill:#1F1E1D}</style>")
o = []
def poly(pts, **kw):
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    o.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" {a}/>')
def rect(x, y, w, h, **kw):
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" {a}/>')
def text(x, y, t, cls="ts", anchor="start", extra=""):
    o.append(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {extra}>{t}</text>')
def badge(x, y, n):
    o.append(f'<circle cx="{x}" cy="{y}" r="10" fill="#F5F4EF" stroke="#1F1E1D"/>')
    text(x, y + 4, str(n), "tp", "middle")

# ------------------------------------------------------------------ top view (scale 6 px/mm, shaft at S)
s = 6.0; SX, SY = 200.0, 185.0
X = lambda m: SX + s * m               # m = millimetres in front of the shaft
G = lambda g: SY + s * g               # g = millimetres behind the shaft's lateral position (+ = away from the palm)
def u(d): return math.cos(math.radians(d)), math.sin(math.radians(d))
def bar(c, r0, r1, half, d):           # rotated bar: centre line from r0 to r1 mm along angle d, +-half mm wide
    ux, uy = u(d); nx, ny = -uy, ux; p0 = (SX + s*r0*ux, SY + s*r0*uy); p1 = (SX + s*r1*ux, SY + s*r1*uy)
    h = s * half; return [(p0[0]+h*nx, p0[1]+h*ny), (p0[0]-h*nx, p0[1]-h*ny), (p1[0]-h*nx, p1[1]-h*ny), (p1[0]+h*nx, p1[1]+h*ny)]
def side_bar(r0, r1, half, d, offset, thick):   # bar of thickness `thick`, offset from the centre line toward -g
    ux, uy = u(d); nx, ny = -uy, ux
    pts = []
    for r, o_ in ((r0, offset), (r1, offset), (r1, offset + thick), (r0, offset + thick)):
        pts.append((SX + s*(r*ux - o_*nx), SY + s*(r*uy - o_*ny)))
    return pts

text(10, 22, "Top view (looking down). The arm is to the left, the jaws point right.", "th")
text(10, 60, "palm side ↑"); text(10, 330, "far side ↓")
# dimensions
for y, x1, x2, label in ((95, X(0), X(38), "38 mm, shaft to jaw tip"), (74, X(-18.5), X(38), "fixed jaw plate 56.5 mm")):
    o.append(f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" stroke="#5F5E5A"/><line x1="{x1:.1f}" y1="{y-5}" x2="{x1:.1f}" y2="{y+5}" stroke="#5F5E5A"/><line x1="{x2:.1f}" y1="{y-5}" x2="{x2:.1f}" y2="{y+5}" stroke="#5F5E5A"/>')
    text((x1 + x2) / 2, y - 6, label, "ts", "middle")
# palm
rect(X(-32), G(-12.1), s*39.5, s*3, fill="#7F77DD", stroke="#534AB7")
o.append(f'<polyline points="{X(-32):.1f},{G(-12.1):.1f} {X(-32)-5:.1f},{G(-11.1):.1f} {X(-32)+5:.1f},{G(-10.1):.1f} {X(-32)-5:.1f},{G(-9.1)+1:.1f}" fill="none" stroke="#5F5E5A"/>')
text(6, G(-12.1) - 8, "to arm")
# H pin glue ball on the palm's back face
o.append(f'<circle cx="{X(-22.5):.1f}" cy="{G(-6.8):.1f}" r="{2.3*s:.1f}" fill="#C9C7BE" stroke="#888780"/>')
text(X(-22.5), G(-6.8) + 4, "H", "tp", "middle")
# fixed jaw plate (glued to the palm), servo, fixed pad
rect(X(-18.5), G(-9.1), s*56.5, s*3, fill="#888780", stroke="#5F5E5A")
rect(X(-16.5), G(-6.1), s*22.5, s*12.2, rx=3, fill="#E9E7DF", stroke="#8F8D85")
rect(X(14), G(-6.1), s*22, s*3, fill="#E0B84C", stroke="#A67C1F")
# zip tie
rect(X(-11.5) - 7.5, G(-12.1) - 6, 15, s*18.2 + 12, fill="#333333", fill_opacity="0.8", stroke="#1F1E1D")
# closed position (dashed)
poly(bar(0, -5, 41, 5, 2), fill="none", stroke="#378ADD", stroke_width="1.2", stroke_dasharray="5 4")
poly(bar(0, 14, 38, 1.5, 2), fill="none", stroke="#378ADD", stroke_width="1.2", stroke_dasharray="5 4")
# example object (18 mm wide), between the pads when open
rect(X(20), G(-3.1), s*18, s*18, fill="none", stroke="#5F5E5A", stroke_dasharray="4 3")
text(X(29), G(5.5), "example object", "ts", "middle"); text(X(29), G(5.5) + 14, "18 mm wide", "ts", "middle")
# horn hub, open moving jaw, pad, spine
o.append(f'<circle cx="{SX}" cy="{SY}" r="{3.5*s:.1f}" fill="#B4B2A9" stroke="#888780"/>')
poly(bar(0, 14, 38, 1.5, 55), fill="#378ADD", stroke="#185FA5")
poly(side_bar(16, 36, 1.5, 55, 1.5, 3), fill="#E0B84C", stroke="#A67C1F")
poly(bar(0, -5, 41, 5, 55), fill="#B5D4F4", fill_opacity="0.55", stroke="#378ADD", stroke_width="1.2")
o.append(f'<circle cx="{SX}" cy="{SY}" r="5" fill="#1F1E1D"/>')
a0, a1 = (SX + 190*u(2)[0], SY + 190*u(2)[1]), (SX + 190*u(55)[0], SY + 190*u(55)[1])
o.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M2 1L8 5L2 9" fill="none" stroke="#378ADD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
o.append(f'<path d="M{a0[0]:.1f} {a0[1]:.1f} A190 190 0 0 1 {a1[0]:.1f} {a1[1]:.1f}" fill="none" stroke="#378ADD" stroke-width="1.5" marker-end="url(#ar)"/>')
text(430, 290, "swing about 53°"); text(300, 428, "open (+55°)"); text(452, 214, "closed (+2°)")
for x, y, n in ((125, 185, 1), (225, 168, 2), (351, 380, 3), (290, 314, 4), (350, 139, 5), (350, 157, 6), (120, 121, 7), (131, 245, 8)):
    badge(x, y, n)

# ------------------------------------------------------------------ front view (looking back toward the arm; palm side on the right)
text(10, 482, "Front view (looking back toward the arm from the jaw tips; the palm side is on the right)", "th")
fx = lambda g: 340 - 6 * g; fy = lambda yy: 640 - 6 * yy
def frect(g0, g1, y0, y1, **kw):
    rect(fx(g1), fy(y1), 6*(g1-g0), 6*(y1-y0), **kw)
frect(-12.1, -9.1, -5, 5, fill="#7F77DD", stroke="#534AB7")                  # palm
frect(-6.1, 6.1, -11.35, 11.35, rx=3, fill="#E9E7DF", stroke="#8F8D85")         # servo
frect(-9.1, -6.1, -6.65, 11.35, fill="#888780", stroke="#5F5E5A")             # fixed jaw plate
frect(-6.1, -3.1, -2, 10, fill="#E0B84C", stroke="#A67C1F")                   # fixed pad
rect(fx(6.6), fy(11.85), 6*19.2, 6*23.7, fill="none", stroke="#333333", stroke_dasharray="5 3", stroke_width="1.5")   # zip tie behind
frect(-3.5, 3.5, 11.35, 13.35, fill="#B4B2A9", stroke="#888780")              # horn
frect(-3.6, 6.4, 13.35, 16.35, fill="#B5D4F4", stroke="#378ADD")              # spine
frect(-0.1, 2.9, -6.65, 13.35, fill="#378ADD", stroke="#185FA5")              # moving jaw plate
frect(-3.1, -0.1, -2, 10, fill="#E0B84C", stroke="#A67C1F")                   # moving pad
for yy, label, ly in ((-5, "palm bottom", 672), (-6.65, "jaw bottom (1.7 mm lower)", 692)):
    o.append(f'<line x1="150" y1="{fy(yy):.1f}" x2="470" y2="{fy(yy):.1f}" stroke="#5F5E5A" stroke-dasharray="4 3"/>')
    text(476, ly, label)
text(250, 560, "far side", "ts", "end"); text(424, 520, "palm side")
for x, y, n in ((403.6, 640, 7), (385.6, 600, 5), (358.6, 600, 6), (331.6, 625, 4), (338, 700, 1), (331.6, 551, 3), (372, 566, 2), (424, 566, 8)):
    badge(x, y, n)

LEGEND = [("1", "Gripper servo: SG90, shaft up, ears trimmed, 22.5 × 12.2 × 22.7 mm. It is clamped onto the fixed jaw plate."),
          ("2", "Horn: single arm trimmed to 12 mm, on the shaft."),
          ("3", "Spine: 46 × 10 × 3 mm, glued flat on the horn."),
          ("4", "Moving jaw plate: 24 × 20 × 3 mm, hangs under the spine, 14–38 mm ahead of the shaft."),
          ("5", "Fixed jaw plate: 56.5 × 18 × 3 mm, glued face to face onto the palm, starting 4 mm in front of pin H."),
          ("6", "Foam pads: 3 mm thick, on both inner jaw faces."),
          ("7", "Palm CH: 75 mm stick, three layers. The plate is glued over its front 26 mm."),
          ("8", "Zip tie: around the palm, the plate and the servo, behind the spine.")]
for i, (n, t) in enumerate(LEGEND):
    y = 748 + 20 * i
    badge(20, y - 4, n); text(38, y, t)
text(10, 920, "Dashed blue: jaw closed. Solid blue: jaw open (away from the palm).")
text(10, 938, "Opening between the pads: about 19 mm mid-jaw and 28 mm at the tips.")
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="680" height="955" viewBox="0 0 680 955" role="img"><title>Single moving jaw gripper scheme</title>'
       f'{STYLE}<rect width="680" height="955" fill="#FFFFFF"/>{"".join(o)}</svg>')
open(os.path.join(HERE, "gripper-scheme.svg"), "w", encoding="utf-8").write(svg)
print("wrote gripper-scheme.svg")
