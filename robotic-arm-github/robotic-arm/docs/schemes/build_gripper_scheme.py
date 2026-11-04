#!/usr/bin/env python3
"""Writes gripper-scheme.svg: top view and front section of the single-moving-jaw gripper."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = ("<style>text{font-family:Helvetica,Arial,sans-serif}.ts{font-size:12px;fill:#5F5E5A}"
         ".th{font-size:14px;font-weight:600;fill:#1F1E1D}</style>")
BODY = r'''
<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M2 1L8 5L2 9" fill="none" stroke="#378ADD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
<text class="th" x="10" y="22">Top view (looking down). The arm is to the left, the jaws point right.</text>
<text class="ts" x="10" y="62">palm side</text>
<text class="ts" x="10" y="372">far side</text>
<rect x="22.5" y="221.3" width="210" height="21" fill="#7F77DD" stroke="#534AB7" stroke-width="1"/>
<polyline points="22.5,221.3 17,227 28,233 17,239 22.5,242.3" fill="none" stroke="var(--text-secondary)" stroke-width="1"/>
<text class="ts" x="6" y="212">to arm</text>
<circle cx="57.5" cy="258.4" r="16" fill="#C9C7BE" stroke="#888780" stroke-width="1"/>
<text class="ts" x="57.5" y="259" text-anchor="middle" dominant-baseline="central" style="fill:var(--text-primary)">H</text>
<rect x="99.5" y="242.3" width="157.5" height="85.4" rx="3" fill="var(--surface-2)" stroke="var(--border-strong)" stroke-width="1"/>
<rect x="187" y="327.7" width="294" height="21" fill="#888780" stroke="#5F5E5A" stroke-width="1"/>
<rect x="313" y="306.7" width="154" height="21" fill="#E0B84C" stroke="#A67C1F" stroke-width="1"/>
<polygon points="178.8,251.2 500.6,240 503,310 181.2,321.2" fill="none" stroke="#378ADD" stroke-width="1.2" stroke-dasharray="5 4"/>
<polygon points="312.5,271.1 480.4,265.2 481.2,286.2 313.3,292.1" fill="none" stroke="#378ADD" stroke-width="1.2" stroke-dasharray="5 4"/>
<rect x="355" y="180.7" width="126" height="126" fill="none" stroke="var(--text-secondary)" stroke-width="1" stroke-dasharray="4 3"/>
<text class="ts" x="418" y="250" text-anchor="middle">example object</text>
<text class="ts" x="418" y="266" text-anchor="middle">18 mm wide</text>
<circle cx="215" cy="285" r="24" fill="#B4B2A9" stroke="#888780" stroke-width="1"/>
<polygon points="262.6,198.7 359,61.1 376.2,73.1 279.8,210.7" fill="#378ADD" stroke="#185FA5" stroke-width="1"/>
<polygon points="287.8,199.2 368.2,84.6 385.4,96.6 305.0,211.2" fill="#E0B84C" stroke="#A67C1F" stroke-width="1"/>
<polygon points="166.2,293.6 350.9,29.8 408.3,70.0 223.6,333.8" fill="#B5D4F4" fill-opacity="0.55" stroke="#378ADD" stroke-width="1.2"/>
<circle cx="215" cy="285" r="5" fill="var(--text-primary)"/>
<path d="M424.9 277.7 A210 210 0 0 0 335.5 113.0" fill="none" stroke="#378ADD" stroke-width="1.5" marker-end="url(#ar)"/>
<text class="ts" x="440" y="160">swing about 53°</text>
<text class="ts" x="416" y="52">open (−55°)</text>
<text class="ts" x="508" y="262">closed (−2°)</text>
<text class="ts" x="560" y="298">forward →</text>
<line x1="215" y1="366" x2="481" y2="366" stroke="var(--text-secondary)" stroke-width="1"/>
<line x1="215" y1="360" x2="215" y2="372" stroke="var(--text-secondary)" stroke-width="1"/><line x1="481" y1="360" x2="481" y2="372" stroke="var(--text-secondary)" stroke-width="1"/>
<text class="ts" x="348" y="360" text-anchor="middle">38 mm, shaft to jaw tip</text>
<line x1="187" y1="388" x2="481" y2="388" stroke="var(--text-secondary)" stroke-width="1"/>
<line x1="187" y1="382" x2="187" y2="394" stroke="var(--text-secondary)" stroke-width="1"/><line x1="481" y1="382" x2="481" y2="394" stroke="var(--text-secondary)" stroke-width="1"/>
<text class="ts" x="334" y="406" text-anchor="middle">fixed jaw plate 42 mm</text>
<g stroke="var(--text-primary)" stroke-width="1" fill="var(--surface-1)">
<circle cx="130" cy="285" r="10"/><circle cx="236" cy="262" r="10"/><circle cx="380" cy="50" r="10"/><circle cx="319" cy="136" r="10"/>
<circle cx="440" cy="338" r="10"/><circle cx="440" cy="317" r="10"/><circle cx="110" cy="232" r="10"/>
</g>
<g class="ts" text-anchor="middle" dominant-baseline="central" style="fill:var(--text-primary);font-weight:600">
<text x="130" y="285">1</text><text x="236" y="262">2</text><text x="380" y="50">3</text><text x="319" y="136">4</text>
<text x="440" y="338">5</text><text x="440" y="317">6</text><text x="110" y="232">7</text>
</g>
<text class="th" x="10" y="440">Front section (looking forward from the arm, palm side on the left)</text>
<rect x="276.3" y="525" width="21" height="70" fill="#7F77DD" stroke="#534AB7" stroke-width="1"/>
<rect x="297.3" y="480.6" width="85.4" height="158.9" rx="3" fill="var(--surface-2)" stroke="var(--border-strong)" stroke-width="1"/>
<rect x="382.7" y="480.6" width="21" height="126" fill="#888780" stroke="#5F5E5A" stroke-width="1"/>
<rect x="361.7" y="490" width="21" height="84" fill="#E0B84C" stroke="#A67C1F" stroke-width="1"/>
<rect x="315.5" y="466.6" width="49" height="14" fill="#B4B2A9" stroke="#888780" stroke-width="1"/>
<rect x="295.2" y="445.6" width="70" height="21" fill="#B5D4F4" stroke="#378ADD" stroke-width="1"/>
<rect x="319.7" y="466.6" width="21" height="140" fill="#378ADD" stroke="#185FA5" stroke-width="1"/>
<rect x="340.7" y="490" width="21" height="84" fill="#E0B84C" stroke="#A67C1F" stroke-width="1"/>
<line x1="230" y1="595" x2="470" y2="595" stroke="var(--text-secondary)" stroke-width="1" stroke-dasharray="4 3"/>
<line x1="230" y1="606.6" x2="470" y2="606.6" stroke="var(--text-secondary)" stroke-width="1" stroke-dasharray="4 3"/>
<text class="ts" x="476" y="594">palm bottom</text>
<text class="ts" x="476" y="618">jaw bottom (1.7 mm lower)</text>
<text class="ts" x="268" y="550" text-anchor="end">palm side</text>
<text class="ts" x="414" y="470">far side</text>
<g stroke="var(--text-primary)" stroke-width="1" fill="var(--surface-1)">
<circle cx="287" cy="560" r="10"/><circle cx="360" cy="622" r="10"/><circle cx="330" cy="456" r="10"/><circle cx="330" cy="520" r="10"/>
<circle cx="393" cy="540" r="10"/><circle cx="351" cy="532" r="10"/><circle cx="356" cy="473" r="10"/>
</g>
<g class="ts" text-anchor="middle" dominant-baseline="central" style="fill:var(--text-primary);font-weight:600">
<text x="287" y="560">7</text><text x="360" y="622">1</text><text x="330" y="456">3</text><text x="330" y="520">4</text>
<text x="393" y="540">5</text><text x="351" y="532">6</text><text x="356" y="473">2</text>
</g>
'''
LEGEND = [("1", "Gripper servo: SG90, shaft up, ears trimmed, 22.5 × 12.2 × 22.7 mm"),
          ("2", "Horn: single arm trimmed to 12 mm, on the shaft"),
          ("3", "Spine: 46 × 10 × 3 mm, glued on the horn"),
          ("4", "Moving jaw plate: 24 × 20 × 3 mm, 14–38 mm ahead of the shaft"),
          ("5", "Fixed jaw plate: 42 × 18 × 3 mm, glued on the servo’s far side"),
          ("6", "Foam pads: 3 mm thick on both inner faces"),
          ("7", "Palm CH: 70 mm; the servo is glued to its back face")]
MAP = {"var(--surface-1)": "#F5F4EF", "var(--surface-2)": "#E9E7DF", "var(--border-strong)": "#8F8D85",
       "var(--text-primary)": "#1F1E1D", "var(--text-secondary)": "#5F5E5A"}
for k, v in MAP.items(): BODY = BODY.replace(k, v)
leg = ""
for i, (n, t) in enumerate(LEGEND):
    y = 668 + 20*i
    leg += (f'<circle cx="20" cy="{y-4}" r="9" fill="#F5F4EF" stroke="#1F1E1D"/><text class="ts" x="20" y="{y-3.5}" text-anchor="middle" dominant-baseline="central" style="fill:#1F1E1D;font-weight:600">{n}</text>'
            f'<text class="ts" x="38" y="{y}">{t}</text>')
leg += '<text class="ts" x="10" y="824">Dashed blue: jaw closed. Solid blue: jaw open. Opening between the pads: about 19 mm mid-jaw and 28 mm at the tips.</text>'
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="680" height="840" viewBox="0 0 680 840" role="img"><title>Single moving jaw gripper scheme</title>'
       f'{STYLE}<rect width="680" height="840" fill="#FFFFFF"/>{BODY}{leg}</svg>')
open(os.path.join(HERE, "gripper-scheme.svg"), "w", encoding="utf-8").write(svg)
print("wrote gripper-scheme.svg")
