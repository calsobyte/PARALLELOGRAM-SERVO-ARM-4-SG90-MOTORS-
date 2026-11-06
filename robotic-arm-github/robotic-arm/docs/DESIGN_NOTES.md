# Design notes

## Coordinates and names

Side view, in milimetres

## The three parallelograms

1. **A-D-E-B (elbow drive).** Crank AD, elbow rod DE, the forearm's rear extension EB and the upper arm AB. AD and EB are equal and parallel, and so are DE and AB. The forearm therefore copies the crank's angle, so the elbow servo can stay on the base.
2. **A-K-F-B and 3. B-F-H-C (leveling).** AK is fixed to the base, so the direction A→K never changes. The rod KF carries it to BF, and FH carries it to the palm CH. K is 40 mm in front of the axle, so the palm is always horizontal.

Each arm servo sets an absolute angle: the shoulder servo sets the upper arm's angle above horizontal, and the elbow servo sets the forearm's angle above horizontal.

## Limits

The mechanism collapses when the upper arm and forearm line up and binds when it is folded, so the angle between them stays between 20° and 150°. With the shoulder between 20° and 100° and the forearm between −90° and +20°, all 2,031 poses in that window were checked. *AGAIN, CALIBRATE IT YOURSELF TO MAKE SURE*

## Layer map

| Layer | Links |
|---|---|
| L0 (front) | AB upper arm, KF leveling rod |
| L1 | AK fixed post, FH leveling rod |
| L2 | DE elbow rod, BF link, CH palm |
| L3 (back) | E–B–C forearm, AD crank |

| Pivot | On the pin, front to back |
|---|---|
| A | AB (L0) on the front servo horn, AD (L3) on the back servo horn. No pin |
| B | AB (L0), spacer (L1), BF (L2), forearm (L3) |
| C | Palm (L2), forearm (L3) |
| D | DE (L2), AD (L3) |
| E | DE (L2), forearm (L3) |
| K | KF (L0), post (L1) |
| F | KF (L0), FH (L1), BF (L2) |
| H | FH (L1), palm (L2) |


## Sticks and joints

- Sticks: 10 × 110 × 1 mm. Every link is three sticks glued flat (about 3 mm thick), so the longest pivot-to-pivot distance is 100 mm with holes 5 mm from the ends.
- Hole diameter is the pin diameter plus 0.2 mm (3.2 mm for a 3 mm skewer).
- Pins are bamboo skewers cut to the stack thickness plus about 5 mm. A hot-glue ball on each end keeps the stack together, and a washer on every stop keeps glue out of the pivot. A strip of baking parchment under the second ball leaves 0.2–0.3 mm of side play.
- Rigid joints are glued: the laminations, the upper arm and crank on their servo horns, the post on the turntable.

## Results of the checks

See [../analysis/results.txt](../analysis/results.txt). In short: the tightest same-layer gap is 12.5 mm centre to centre (2.5 mm between edges), the lowest point of the palm is 41 mm below the axle, and the worst-case moment is 0.46 kg·cm empty and 0.71 kg·cm with a 10 g object, below half of the SG90's 1.8 kg·cm stall rating.

Assumptions in the moment estimate: 0.66 g per stick, 9 g for the gripper servo, 4 g for jaws and hardware, 0.35 g per pivot. The moment is shared between the two arm servos and the fixed post.

## Tolerances

A 0.5 mm error in a rod length tilts the forearm or palm by about 1° typically, and by up to roughly 3° (DE, KF) or 6° (FH) near the ends of the range. Hole spacing should therefore be within about ±0.3 mm, so identical parts are drilled together.
