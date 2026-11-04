# Gripper design: single moving jaw

![Gripper scheme](schemes/gripper-scheme.svg)

One SG90 stands on the palm CH with its shaft pointing up. A flat spine rides on the horn, and the moving jaw plate hangs from the spine. The fixed jaw plate is glued to the servo's far side. The jaw swings sideways, away from the palm, and closes on an object against the fixed jaw.

All distances are measured from the servo shaft. Forward is the direction the jaws point.

| Item | Value |
|---|---|
| Servo | SG90, shaft up, mounting ears trimmed off, 22.5 × 12.2 × 22.7 mm |
| Servo position | Rear end 6 mm in front of pin H, shaft 22.5 mm in front of H |
| Moving jaw plate | 24 × 20 × 3 mm, from 14 mm to 38 mm in front of the shaft |
| Spine | 46 × 10 × 3 mm, from 5 mm behind the shaft to 41 mm in front |
| Fixed jaw plate | 42 × 18 × 3 mm, from 4 mm behind the shaft to 38 mm in front |
| Pads | 3 mm foam on both inner faces |
| Jaw swing | About 53° (closed at −2°, open at −55°, toward the palm side) |
| Opening between the pads | About 19 mm mid-jaw, 28 mm at the tips |
| Largest object | About 18 mm wide and 10 g |
| Gripper weight | About 13–14 g |

## Parts

| Part | Made from | Notes |
|---|---|---|
| Gripper servo | SG90 | Cut both mounting ears off |
| Horn | Single-arm horn | Trim the arm to 12 mm from the centre |
| Spine | 3 sticks laminated, 46 mm | 3 mm hole 5 mm from the rear end for the horn screw |
| Moving jaw plate | 3 layers of two sticks side by side | 24 mm long, plus a 24 mm splint across the seam on the outer face |
| Fixed jaw plate | 3 layers, each a full stick plus one trimmed to 8 mm | 42 mm long, plus a splint on the outer face |
| Foam pads | Craft foam | 3 × 12 × 22 mm, two of them |
| Palm CH | Existing | 70 mm; cut a 75 mm palm back by 5 mm |

## Build steps

1. Make the jaw plates and the spine, and let the glue dry.
2. Centre the servo at 90° with the test sketch in [../firmware/gripper_servo_test](../firmware/gripper_servo_test/gripper_servo_test.ino).
3. Glue the servo's side face to the palm's back face, 6 mm in front of pin H, centred vertically on the palm, and add a small zip tie. Keep glue off the H pin's glue ball.
4. Glue the fixed jaw plate flat onto the servo's far side face. Its bottom edge is level with the moving plate's bottom, and its top edge is level with the servo's top.
5. Fit the horn so the jaw points about 28° toward the palm side at servo angle 90° (half open), and fix it with the centre screw.
6. Glue the spine flat on the horn arm, with the hole over the centre screw, then glue the moving jaw plate under the spine, 14 mm to 38 mm in front of the shaft.
7. Glue a foam pad on each inner jaw face.
8. Use the test sketch to find the closed and open angles, and never go past them.

Checkpoints: the jaw swings from closed to open without touching the palm, the servo or the H pin, and the pads meet evenly when closed.
