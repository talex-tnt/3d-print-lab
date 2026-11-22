# Strip 170 x 5 mm with a 10 mm tab at one end, bent 145 degrees (180 - 35) out of the strip's
# plane: the tab folds back towards the strip, leaving 35 degrees between them, like a hook
# (the bend axis runs across the 5 mm width). The outside of the bend is rounded.
# Two versions: 1.0 mm and 1.5 mm thick.
# FreeCAD script: edit the parameters below and run it again
#   - from FreeCAD: Macro > Macros... > Execute
#   - from a terminal: "/Applications/FreeCAD 1.1.0.app/Contents/Resources/bin/freecadcmd" angled_strip.py
# All dimensions are in mm.
# Print orientation (on its side, no supports): the hook profile lies in XY
# (strip along X, tab bent towards +Y, thickness along Y), the 5 mm width goes up along Z.

import os
import math
import FreeCAD as App
import Part
import Mesh

# ------------- PARAMETERS -------------
LENGTH     = 170.0         # straight part, measured on the centre line up to the bend
WIDTH      = 5.0           # bend axis runs across this side
TAB_LEN    = 10.0          # angled tab, measured on the centre line from the bend
BEND_DEG   = 180.0 - 35.0  # how much the tab turns away from the strip direction (35 deg left between them)
THICKNESS  = (1.0, 1.5)    # one STL per value

OUT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
# --------------------------------------

a = math.radians(BEND_DEG)
P = App.Vector(LENGTH, 0, 0)                                    # bend point on the centre line
d2 = App.Vector(math.cos(a), math.sin(a), 0)                    # tab direction
n1 = App.Vector(0, 1, 0)                                        # normal of the strip
n2 = App.Vector(-math.sin(a), math.cos(a), 0)                   # normal of the tab
E = P + d2 * TAB_LEN                                            # end of the tab on the centre line

doc = App.newDocument("AngledStrip")
for t in THICKNESS:
    h = t / 2
    m = (n1 + n2) * (h / (1 + n1.dot(n2)))                      # mitre offset, inside of the bend
    mid = App.Vector(n1 + n2); mid.normalize()
    edges = [
        Part.makeLine(App.Vector(0, -h, 0), P - n1 * h),
        Part.Arc(P - n1 * h, P - mid * h, P - n2 * h).toShape(),  # rounded outside of the bend
        Part.makeLine(P - n2 * h, E - n2 * h),
        Part.makeLine(E - n2 * h, E + n2 * h),
        Part.makeLine(E + n2 * h, P + m),
        Part.makeLine(P + m, App.Vector(0, h, 0)),
        Part.makeLine(App.Vector(0, h, 0), App.Vector(0, -h, 0)),
    ]
    face = Part.Face(Part.Wire(edges))
    face.translate(App.Vector(0, -face.BoundBox.YMin, 0))       # keep everything at Y >= 0
    shp = face.extrude(App.Vector(0, 0, WIDTH))
    tag = f"{t:.1f}".replace(".", "_")
    bb = shp.BoundBox
    print(f"{t:.1f} mm: {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm, "
          f"valid {shp.isValid()}, volume {shp.Volume:.1f} mm3")
    o = doc.addObject("Part::Feature", f"Strip_{tag}mm"); o.Shape = shp
    Mesh.Mesh(shp.tessellate(0.02)).write(os.path.join(OUT_DIR, f"angled_strip_{tag}mm.stl"))
doc.recompute()
doc.saveAs(os.path.join(OUT_DIR, "angled_strip.FCStd"))
