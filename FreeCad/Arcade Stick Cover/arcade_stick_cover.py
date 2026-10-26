# Dust cover (washer) for an arcade stick: a thin disc with a chamfered rim, a raised
# conical boss in the middle and a hole for the shaft. Same shape as the original
# cover (~38 mm), only wider (60 mm), so it hides the marks around the panel hole.
# FreeCAD script: edit the parameters below and run it again
#   - from FreeCAD: Macro > Macros... > Execute
#   - from a terminal: "/Applications/FreeCAD 1.1.0.app/Contents/Resources/bin/freecadcmd" arcade_stick_cover.py
# All dimensions are in mm.
# Axes: Z = shaft axis, flat underside on Z=0 (also the print orientation, no supports).

import os
import FreeCAD as App
import Part
import Mesh

# ------------- PARAMETERS -------------
OUTER_D   = 60.0   # new outer diameter, wide enough to hide the marks on the panel
HOLE_D    = 11.0   # shaft hole (measured on the original)
HOLE_CLR  = 0.2    # extra on the hole diameter, printed holes come out a bit small
DISC_T    = 1.0    # disc thickness
BOSS_H    = 2.0    # boss height above the disc (total height = DISC_T + BOSS_H)
BOSS_D0   = 14.0   # boss diameter at its base (estimated from the photos)
BOSS_D1   = 12.5   # boss diameter at its top (estimated from the photos)
RIM_T     = 0.4    # disc thickness at the very edge
RIM_W     = 2.0    # radial width of the chamfer on the top edge of the disc

OUT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
# --------------------------------------

ri = (HOLE_D + HOLE_CLR) / 2
ro = OUTER_D / 2
# half profile in the XZ plane, revolved around Z
pts = [
    (ri, 0),
    (ro, 0),
    (ro, RIM_T),
    (ro - RIM_W, DISC_T),
    (BOSS_D0 / 2, DISC_T),
    (BOSS_D1 / 2, DISC_T + BOSS_H),
    (ri, DISC_T + BOSS_H),
]
v = [App.Vector(x, 0, z) for x, z in pts]
face = Part.Face(Part.makePolygon(v + [v[0]]))
cover = face.revolve(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 360).removeSplitter()

print(f"cover {OUTER_D:.1f} mm, hole {2 * ri:.2f} mm, height {DISC_T + BOSS_H:.1f} mm")
print("valid:", cover.isValid(), "volume mm3:", round(cover.Volume, 1))

doc = App.newDocument("ArcadeStickCover")
o = doc.addObject("Part::Feature", "Cover"); o.Shape = cover
doc.recompute()
doc.saveAs(os.path.join(OUT_DIR, "arcade_stick_cover.FCStd"))
Mesh.Mesh(cover.tessellate(0.02)).write(os.path.join(OUT_DIR, "arcade_stick_cover.stl"))
print("arcade_stick_cover.stl", cover.BoundBox)
