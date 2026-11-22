# Angled Strip

A 170 × 5 mm strip with a 10 mm tab at one end, folded back 145° (180 − 35) out of the strip's plane like a hook: 35° are left between tab and strip. The bend axis runs across the 5 mm width, and the outside of the bend is rounded.

## Parts

| File | Qty | What it is |
|---|---|---|
| `angled_strip_1_0mm.stl` | 1 | 1.0 mm thick version |
| `angled_strip_1_5mm.stl` | 1 | Alternative: 1.5 mm thick, stiffer |
| `angled_strip.py` | – | Parametric FreeCAD script that generates everything |
| `angled_strip.FCStd` | – | FreeCAD model (both versions) |

Lengths are measured on the centre line: 170 mm up to the bend, 10 mm after it. Overall size: about 171 × 7 × 5 mm. The gap between tab and strip opens to about 4–5 mm at the tip of the tab.

## Printing

| Setting | Value |
|---|---|
| Printer | Bambu Lab A1 mini (fits the 180 × 180 bed along X) |
| Material | PLA |
| Layer height | 0.2 mm |
| Orientation | on its side: hook profile on the bed, 5 mm width upright (as exported) |
| Supports | none |
| Adhesion | brim recommended (thin 5 mm high wall) |

```bash
"/Applications/FreeCAD 1.1.0.app/Contents/Resources/bin/freecadcmd" angled_strip.py
```
