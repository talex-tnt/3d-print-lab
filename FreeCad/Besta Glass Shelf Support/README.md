# BESTÅ Glass Shelf Support

3D printed supports that turn an IKEA **BESTÅ glass top panel (180 × 40 cm, 4 mm tempered glass)** into a floating shelf between two tall BESTÅ cabinets, above the BESTÅ TV bench. The glass is never drilled: its ends slide into two sideways-U brackets bolted to the cabinet sides, and a wall bracket supports the middle.

![Overview](overview.png)

## Parts

| File | Qty | What it is |
|---|---|---|
| `side_bracket_x2.stl` | 2 | Sideways U, 170 mm long. The glass end slides into the slot and the plate below is bolted to the cabinet side. It is symmetric, so for the other side just rotate it 180°. |
| `center_bracket_x1.stl` | 1 | Wall bracket with a 165 mm arm and a lip over the back edge of the glass. Without it the 4 mm glass sags about 3–4 cm over 1.8 m from its own weight. |
| `glass_shelf_supports.py` | – | Parametric FreeCAD script that generates everything. |
| `glass_shelf_supports.FCStd` | – | FreeCAD model. |

![Sections with fasteners](sections.png)

## Hardware

| Qty | Item | Where |
|---|---|---|
| 6 | M4 × 30 countersunk bolt (ISO 10642 / DIN 7991) | side brackets → through the cabinet side |
| 6 | M4 washer, wide (DIN 9021) | inside the cabinet |
| 6 | M4 nyloc nut (DIN 985), or domed cap nut (DIN 1587) for a tidier look | inside the cabinet |
| 2 | 5 × 50 pan head wood screw | center bracket → wall |
| 2 | 6 mm wall plug for your wall type (masonry plug for brick/concrete, metal cavity anchor for drywall) | center bracket → wall |
| 2 | 5.3 mm washer (DIN 125) | center bracket slots |
| ~1 m | 1 mm adhesive felt tape, 10 mm wide | lines every face that touches the glass |

**Why through bolts?** BESTÅ frame sides are particleboard skins with a honeycomb paper core, so wood screws in the middle of a side panel hold poorly. Bolting through the side with a wide washer inside spreads the load and holds firmly. M4 × 30 works for sides up to ~18 mm thick, so measure yours and use M4 × 35 if it is thicker.

## Before you start

1. **Glass thickness.** The IKEA spec is 0.4 cm. Measure it with a caliper and set `GLASS_T` if it differs.
2. **Gap between the tall cabinets.** It must be at least **1808 mm**: 1800 of glass, plus 3 mm of U back wall on each side, plus 2 mm of play. Tempered glass cannot be cut. If the gap is smaller, move a cabinet out a few mm, or set `BACK = 0`. With `BACK = 0` the side bracket becomes an L: the glass rests on it with no top lip, and nothing sits between the glass and the cabinet.
3. **Wall distance.** Measure how far the back edge of the glass will be from the wall and set `GLASS_BACK` (default 10 mm, min. 4).

## Printing (Bambu Lab A1 mini)

| Setting | Value |
|---|---|
| Material | PETG or ASA (not PLA: it creeps under constant load) |
| Layer height | 0.2 mm |
| Walls | 5 |
| Top/bottom layers | 5 |
| Infill | 40 % gyroid |
| Supports | none |
| Brim | yes for the side brackets (tall and narrow) |

![Print orientation](print_orientation.png)

- **Side bracket:** stand it upright on its U profile (170 mm tall). The layers then follow the profile, so the ledge carrying the glass does not load the layer lines in tension.
- **Center bracket:** lay it on its side (profile on the bed, 40 mm tall).

## Installation

1. **Mark the shelf height** on both cabinet sides. The top of the side-bracket ledge sits 1 mm (felt) below the underside of the glass. Use a laser or a long spirit level so both sides are at exactly the same height.
2. **Position the side brackets.** Hold each side bracket against the cabinet side with the U opening toward the gap, centered on the depth (about 115 mm from the front edge). Keep it level.
3. **Drill.** Use the bracket as a template and drill **4.5 mm** through the cabinet side at the 3 holes. Clamp a scrap block on the inside so the melamine doesn't chip.
4. **Bolt the side brackets.** Fit the countersunk bolts from the bracket side, and the washers and nuts inside the cabinet. Tighten firmly, but don't crush the panel.
5. **Mount the center bracket.** Hold it on the wall at mid-span, with its ledge at the same height as the side ledges; a straight edge across all three helps. Mark the slots, drill and plug the wall, then fit the screws with washers. Fine-tune the height (±3 mm) in the slots before the final tightening.
6. **Add the felt.** Stick felt tape on the ledge and under the top lip of each U, and on the center bracket ledge and lip.
7. **Fit the glass.** Hold it level at the height of the slots and slide it in from the front, pushing it back until it reaches the center bracket. It should not rattle. If it does, use thicker felt, and if it is too tight, thinner felt (or change `PAD` and reprint).

**Load:** keep it moderate (decorations, a few books spread out) and avoid heavy point loads near the front at mid-span.

## Changing the design

All dimensions are parameters at the top of `glass_shelf_supports.py`. Edit them and run:

```bash
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd glass_shelf_supports.py
```

This regenerates the `.FCStd` model and both STL files in this folder.
