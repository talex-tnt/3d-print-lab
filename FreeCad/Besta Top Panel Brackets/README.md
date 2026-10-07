# BESTÅ Top Panel Brackets

Fixes an IKEA **BESTÅ oak veneer top panel (180 × 42 × 2 cm, solid particleboard)** between two tall BESTÅ cabinets, for example flush with their tops:

- **It is carried by 3 metal wall brackets.** They are flat-bar T brackets with 25 cm arms, 30 cm from each end and one in the middle (every 60 cm), screwed up into the panel, so the panel stands on the wall alone, even fully loaded with boxed consoles (see [Load](#load-boxed-consoles)).
- **4 small printed L brackets lock its ends** to the cabinet sides: one leg is bolted to the cabinet, the other is screwed up into the panel. Nothing is visible from the front, and nothing sits between the panel end and the cabinet. To move a cabinet later, unbolt its two L brackets and the panel stays up.

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
| 3 | Flat-bar T shelf bracket, 25 cm arm (e.g. TESSTINA "concealed" 80 kg) | wall |
| 9 | **Resin** wall fixings for those brackets, see [Fixing into a thick stone wall](../Besta%20Glass%20Shelf%20Support/README.md#fixing-into-a-thick-stone-wall) | metal bracket → wall |
| 6–9 | 3.5 × 16 countersunk chipboard screw | metal bracket arm → underside of the panel |
| 8 | M4 × 35 countersunk bolt (ISO 10642 / DIN 7991) | L brackets → through the cabinet side |
| 8 | M4 washer, wide (DIN 9021) | inside the cabinet |
| 8 | M4 nyloc nut (DIN 985), or a plain nut with medium (blue) threadlocker | inside the cabinet |
| 8 | 3.5 × 16 countersunk chipboard screw (e.g. Spax) | L brackets → underside of the panel |

- **Cabinet side:** BESTÅ frame sides have a honeycomb paper core, so bolt through them rather than using wood screws. The BESTÅ sides measure 18–19 mm, so use **M4 × 35**. Through a 5–6 mm printed plate, the side, a washer and a 5 mm tall nyloc nut, an M4 × 30 would be ~2 mm too short, while M4 × 35 leaves a few mm of thread past the nut.
- **Top panel:** it is solid particleboard. A 3.5 × 16 screw goes ~11 mm into the 20 mm panel through a printed bracket (5 mm), or ~11 mm through a metal arm (5 mm), so it never comes through the top. Don't use the long shelf screws supplied with the metal brackets: they would go through the panel.

## Printing (Bambu Lab A1 mini)

| Setting | Value |
|---|---|
| Material | PETG or ASA |
| Layer height | 0.2 mm |
| Walls | 5 |
| Infill | 40 % gyroid |
| Supports | none |

![Print orientation](print_orientation.png)

Stand each L bracket on its L profile (40 mm tall), so the layers follow the profile and the corner is as strong as possible. All 4 fit on one plate.

## Before you start

- **Width:** the panel is exactly 180 cm, so the gap between the tall cabinets must be at least 1800 mm. The L brackets take no extra width.
- **Depth:** the panel is 42 cm deep against 40 cm cabinets. Its back edge sits ~5 mm off the wall, in front of the metal wall plates, so it sticks out about 2.5 cm in front of cabinets that touch the wall.
- **Wall plates:** they rise 25 mm above the arm, so they stick up ~5 mm behind the back edge of the 20 mm panel. At 192 cm high this can't be seen.

## Installation

1. **Mark the height.** For a panel flush with the cabinet tops (192 cm), the top of the metal arms and of the L brackets sits **20 mm below the cabinet top**. A 20 mm offcut of wood makes a good spacer.
2. **Metal brackets.** Mount the 3 metal brackets on the wall **30 cm from each end of the gap and one in the middle** (at 30, 90 and 150 cm, 60 cm apart), level with each other. Use a spirit level on each one and a long straight edge across all three. Use resin anchors (see the stone wall notes).
3. **L brackets.** Use 2 per side, about **30 mm from the front and back edges** (see the plan view above), at the same height as the arms. Lay the straight edge on the arms to transfer it.
4. **Drill the cabinet sides.** Use each L bracket as a template and drill **4.5 mm** through the cabinet side at its 2 holes. Clamp a scrap block inside so the melamine doesn't chip.
5. **Bolt the L brackets.** Fit the countersunk bolts from the bracket side, and the washers and nuts inside the cabinet.
6. **Lay the panel.** Rest the panel on the 3 arms and the 4 L brackets. Push it back against the wall plates and check that it is level and flush.
7. **Screw from below.** Drill **2.5 mm** pilot holes into the panel through the holes of the arms and the L brackets. Wrap tape on the bit at **13 mm** as a depth stop, so you never come out through the veneer. Then drive the 3.5 × 16 screws.

## Load: boxed consoles

The panel is meant to display retro and modern consoles in their original boxes, standing upright, in 2 rows (front and back) and 2 high: about **16 boxes**. Rough boxed weights (console, PSU, controllers, inserts, box):

| Retro | kg | Modern | kg |
|---|---|---|---|
| NES / SNES / N64 | ~2.3–2.5 | PS2 | ~3.5 |
| GameCube / Wii | ~2.5 | PS4 | ~4.5 |
| Master System / Mega Drive | ~2 | PS3 fat / PS5 | ~7 |
| Saturn / Dreamcast / PS1 | ~2.5–3 | Xbox / 360 / One / Series X | ~6–6.5 |
| Switch | ~1.8 | Wii U | ~3.5 |

That is **~60–65 kg** for a typical mix and **~90 kg** if it is mostly modern consoles, plus the 12.8 kg panel.

With 3 brackets (30 / 90 / 150 cm) and the L brackets, each metal bracket carries ~22–29 kg and the panel stays straight (stress ~0.3–0.4 MPa against ~11–14 MPa for particleboard). With only 2 brackets the panel would be fine too, but it would carry ~38–51 kg each and sag 5–9 mm over the months.

**The weak point is the wall, not the panel.** The wall plate is only 25 mm tall, so it has little leverage: with the boxes centered ~20 cm from the wall, ~25 kg on a bracket pulls on its 3 screws with roughly **70–90 kg each**. So:

- **Use resin anchors** for these 3 brackets, not plastic plugs, in the old stone wall.
- **Put the heaviest boxes at the back and over the brackets.** Place PS3, PS5 and the Xboxes in the row against the wall, near the brackets, and the light retro boxes in front and between the brackets. The closer the weight is to the wall, the less the screws pull.
- **Stop the boxes from falling.** Two boxes stacked upright reach ~60–80 cm above 192 cm, above the TV, and Emilia is an earthquake zone. Add a low lip along the front edge, or a dab of removable putty (e.g. Patafix) under the boxes, and check the clearance to the ceiling.

## How stiff is it?

Rough estimates of the sag of the 1.8 m panel:

| Support | 20 mm oak top panel |
|---|---|
| Only at the ends (L brackets alone) | ~11 mm, more over time |
| 2 brackets 40 cm from the ends, 64 kg of consoles | ~5–7 mm after months |
| **3 brackets at 30 / 90 / 150 cm + L brackets, 64–90 kg of consoles** | **< 1 mm** |
| 3 brackets alone (cabinets moved), 64 kg of consoles | ~3 mm after months |

## Changing the design

All dimensions, including the fillet radii (`R_INNER`, `R_OUTER`, `R_END`), are parameters at the top of `top_panel_brackets.py`. Edit them and run:

```bash
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd top_panel_brackets.py
```

This regenerates the `.FCStd` model and the STL file in this folder.

The script also prints the bolt length needed for the cabinet sides from `CABINET_SIDE` (measured: 18–19 mm, set to 19) and the washer and nut sizes. Rerun it if your sides differ.
