# Hidden L brackets to fix an IKEA BESTA 180x42x2 cm oak veneer top panel
# between two tall BESTA cabinets (one leg screwed to the cabinet side,
# the other screwed up into the underside of the panel).
# FreeCAD script: edit the parameters below and run it again
#   - from FreeCAD: Macro > Macros... > Execute
#   - from a terminal: /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd top_panel_brackets.py
# All dimensions are in mm. Print 4 (2 per side, front and back).

import os
import FreeCAD as App
import Part
import Mesh

# ------------- PARAMETERS -------------
WIDTH     = 40.0   # bracket width (along the shelf depth)
LEDGE     = 40.0   # how far the top leg reaches under the panel
LEDGE_T   = 5.0    # top leg thickness
PLATE     = 5.0    # cabinet leg thickness
DROP      = 40.0   # how far the cabinet leg goes down
GUSSET    = 15.0   # 45 degree gusset size (keeps both screw rows reachable)
SCREW_D   = 4.5    # screw hole (M4 through bolts or 3.5 mm chipboard screws)
CSK_D     = 8.0    # countersink diameter
SCREW_GAP = 20.0   # distance between the two screws in each leg
R_INNER   = 5.0    # fillet on the inner gusset corners
R_OUTER   = 2.0    # fillet on the outer profile corners
R_END     = 1.2    # fillet on the edges of the two end faces

OUT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
# --------------------------------------


def bracket():
    # profile in the XZ plane (X = away from the cabinet, Z = up, top of panel leg at Z=0), extruded along Y
    gz = -(LEDGE_T + GUSSET)
    pts = [(0, -DROP), (PLATE, -DROP), (PLATE, gz), (PLATE + GUSSET, -LEDGE_T),
           (LEDGE, -LEDGE_T), (LEDGE, 0), (0, 0)]
    v = [App.Vector(x, 0, z) for x, z in pts]
    body = Part.Face(Part.makePolygon(v + [v[0]])).extrude(App.Vector(0, WIDTH, 0))

    # round the profile corners: wide radius on the inner gusset corners, small on the outer ones
    def corner_edge(shape, x, z):
        return [e for e in shape.Edges if abs(e.BoundBox.XMin - x) < 1e-6 and abs(e.BoundBox.XMax - x) < 1e-6
                and abs(e.BoundBox.ZMin - z) < 1e-6 and abs(e.BoundBox.ZMax - z) < 1e-6]
    inner = [(PLATE, gz), (PLATE + GUSSET, -LEDGE_T)]
    for x, z in pts:
        body = body.makeFillet(R_INNER if (x, z) in inner else R_OUTER, corner_edge(body, x, z))
    # soften the edges of the two end faces
    ends = [e for e in body.Edges if abs(e.BoundBox.YMax - e.BoundBox.YMin) < 1e-6]
    body = body.makeFillet(R_END, ends)

    csk_h = (CSK_D - SCREW_D) / 2
    for y in (WIDTH / 2 - SCREW_GAP / 2, WIDTH / 2 + SCREW_GAP / 2):
        # cabinet leg: horizontal screws below the gusset, head on the open side
        zs = (gz - DROP) / 2
        body = body.cut(Part.makeCylinder(SCREW_D / 2, PLATE + 2, App.Vector(-1, y, zs), App.Vector(1, 0, 0)))
        body = body.cut(Part.makeCone(SCREW_D / 2, CSK_D / 2, csk_h + 0.01,
                                      App.Vector(PLATE - csk_h, y, zs), App.Vector(1, 0, 0)))
        # panel leg: vertical screws beyond the gusset, head underneath
        xs = (PLATE + GUSSET + LEDGE) / 2
        body = body.cut(Part.makeCylinder(SCREW_D / 2, LEDGE_T + 2, App.Vector(xs, y, -LEDGE_T - 1)))
        body = body.cut(Part.makeCone(CSK_D / 2, SCREW_D / 2, csk_h + 0.01, App.Vector(xs, y, -LEDGE_T - 0.01)))
    return body.removeSplitter()


doc = App.newDocument("TopPanelBrackets")
b = bracket()
o = doc.addObject("Part::Feature", "LBracket"); o.Shape = b
doc.recompute()
doc.saveAs(os.path.join(OUT_DIR, "top_panel_brackets.FCStd"))
Mesh.Mesh(b.tessellate(0.05)).write(os.path.join(OUT_DIR, "l_bracket_x4.stl"))
print("l_bracket_x4.stl volume cm3:", round(b.Volume / 1000, 1), "valid:", b.isValid(), "bbox:", b.BoundBox)
