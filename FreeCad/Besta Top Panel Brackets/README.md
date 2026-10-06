# BESTÅ Top Panel Brackets

Small hidden L brackets that fix an IKEA **BESTÅ oak veneer top panel (180 × 42 × 2 cm, solid particleboard)** between two tall BESTÅ cabinets, for example flush with their tops. One leg is bolted to the cabinet side and the other is screwed up into the underside of the panel. Nothing is visible from the front, and nothing sits between the panel end and the cabinet.

![Overview](overview.png)

## Parts

| File | Qty | What it is |
|---|---|---|
| `l_bracket_x4.stl` | 4 | 40 × 40 × 40 mm L bracket with a 45° gusset and rounded edges, 2 per side (front and back). |
| `top_panel_brackets.py` | – | Parametric FreeCAD script that generates everything. |
| `top_panel_brackets.FCStd` | – | FreeCAD model. |

![Sections and bracket positions](sections.png)

## Hardware

| Qty | Item | Where |
|---|---|---|
| 8 | M4 × 30 countersunk bolt (ISO 10642 / DIN 7991) | brackets → through the cabinet side |
| 8 | M4 washer, wide (DIN 9021) | inside the cabinet |
| 8 | M4 nyloc nut (DIN 985), or domed cap nut (DIN 1587) | inside the cabinet |
| 8 | 3.5 × 16 countersunk chipboard screw (e.g. Spax) | brackets → underside of the top panel |

- **Cabinet side:** BESTÅ frame sides have a honeycomb paper core, so bolt through them rather than using wood screws. M4 × 30 works for sides up to ~19 mm thick; use M4 × 35 if yours are thicker.
- **Top panel:** it is solid particleboard. A 3.5 × 16 screw goes 11 mm into the 20 mm panel, so it never comes through the top.

## Printing (Bambu Lab A1 mini)

| Setting | Value |
|---|---|
| Material | PETG or ASA |
| Layer height | 0.2 mm |
| Walls | 5 |
| Infill | 40 % gyroid |
| Supports | none |

![Print orientation](print_orientation.png)

Stand each bracket on its L profile (40 mm tall), so the layers follow the profile and the corner is as strong as possible. The 4 brackets fit on one plate.

## Installation

1. **Check the fit.** The panel is exactly 180 cm, so the gap between the tall cabinets must be at least 1800 mm. The brackets take no extra width. The panel is 42 cm deep against 40 cm cabinets, so decide whether the 2 cm overhang goes at the front (covers the cabinet edges) or at the back.
2. **Mark the height.** For a panel flush with the cabinet tops (192 cm), the top of each bracket sits **20 mm below the cabinet top**. A 20 mm offcut of wood makes a good spacer.
3. **Position the brackets.** Use 2 brackets per side, about **30 mm from the front and back edges** (see the plan view above).
4. **Drill the cabinet side.** Use each bracket as a template and drill **4.5 mm** through the cabinet side at its 2 holes. Clamp a scrap block inside so the melamine doesn't chip.
5. **Bolt the brackets.** Fit the countersunk bolts from the bracket side, and the washers and nuts inside the cabinet.
6. **Lay the panel.** Rest the panel on the 4 brackets and check that it is level and flush.
7. **Screw into the panel.** From below, drill **2.5 mm** pilot holes into the panel through the bracket holes. Wrap tape on the bit at **13 mm** as a depth stop, so you never come out through the veneer. Then drive the 3.5 × 16 screws.

## Notes

- **Sag.** 20 mm particleboard free over 1.8 m sags roughly 1 cm from its own weight, and more with load and over time. For books or heavy items, add a hidden support at mid-span (for example a low wall bracket screwed up into the underside, like the center bracket in [Besta Glass Shelf Support](../Besta%20Glass%20Shelf%20Support/)).
- **IKEA fittings.** The mounting fittings supplied with the panel are meant for placing it on top of BESTÅ cabinets and are not needed here.

## Changing the design

All dimensions, including the fillet radii (`R_INNER`, `R_OUTER`, `R_END`), are parameters at the top of `top_panel_brackets.py`. Edit them and run:

```bash
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd top_panel_brackets.py
```

This regenerates the `.FCStd` model and the STL file in this folder.
