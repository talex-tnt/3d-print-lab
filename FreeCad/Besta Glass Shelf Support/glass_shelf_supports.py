# Supports for an IKEA BESTA 180x40 cm glass top used as a shelf
# FreeCAD script: edit the parameters below and run it again
#   - from FreeCAD: Macro > Macros... > Execute
#   - from a terminal: /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd glass_shelf_supports.py
# All dimensions are in mm.

import os
import FreeCAD as App
import Part
import Mesh

# ------------- PARAMETERS (MEASURE BEFORE PRINTING!) -------------
GLASS_T   = 4.0    # glass thickness (IKEA spec: 0.4 cm, check with a caliper)
PAD       = 1.0    # adhesive felt/rubber pad thickness (above and below the glass)
CLEAR     = 0.6    # clearance to slide the glass in
SLOT      = GLASS_T + 2 * PAD + CLEAR   # slot height

# --- side bracket (screwed to the side of the tall cabinet) ---
L_LEN     = 170.0  # length along the shelf depth (printed upright: A1 mini max 180)
BACK      = 3.0    # U back wall between glass and cabinet. Needs: gap between cabinets >= 1800 + 2*BACK + 2
                   # set 0 for a flush fit: becomes an L (glass rests on it, no top lip)
LEDGE     = 30.0   # how far the ledge reaches under the glass
LEDGE_T   = 6.0    # lower ledge thickness
TOP_LIP   = 12.0   # how far the top lip covers the glass
TOP_T     = 4.0    # top lip thickness
PLATE     = 6.0    # plate thickness against the cabinet (below the ledge)
DROP      = 46.0   # how far the plate extends below the resting surface
SCREW_D   = 4.5    # screw hole (M4 through bolts or 3.5 mm chipboard screws)
CSK_D     = 8.0    # countersink diameter

# --- center bracket (wall mounted, supports the middle of the glass) ---
C_WIDTH   = 40.0   # width
C_ARM     = 165.0  # reach from the wall (printed lying down: A1 mini bed 180x180)
C_H       = 120.0  # height below the resting surface
C_PLATE   = 8.0    # wall plate thickness
C_LT      = 8.0    # arm thickness
C_STRUT   = 10.0   # diagonal strut thickness
GLASS_BACK = 10.0  # distance from wall to the back edge of the glass (min. 4)
C_LIP     = 12.0   # top lip over the back edge of the glass
WALL_SCREW = 5.2   # wall screw slot width (6 mm plug + 4.5/5 mm screw)
SLOT_LEN  = 6.0    # slot travel for height adjustment (+-3 mm)

OUT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
# ------------------------------------------------------------------------


def prism(pts_xz, length):
    """Profile in the XZ plane, extruded along +Y."""
    v = [App.Vector(x, 0, z) for x, z in pts_xz]
    face = Part.Face(Part.makePolygon(v + [v[0]]))
    return face.extrude(App.Vector(0, length, 0))


def side_bracket():
    gz = -(LEDGE_T + (LEDGE - PLATE))       # foot of the 45 degree gusset
    pts = [(0, -DROP), (PLATE, -DROP), (PLATE, gz), (LEDGE, -LEDGE_T), (LEDGE, 0)]
    if BACK > 0:
        pts += [(BACK, 0), (BACK, SLOT), (TOP_LIP, SLOT), (TOP_LIP, SLOT + TOP_T), (0, SLOT + TOP_T)]
    else:
        pts += [(0, 0)]
    body = prism(pts, L_LEN)

    # 3 horizontal screws into the cabinet side, below the gusset (screwdriver access)
    zs = (gz - DROP) / 2
    for y in (25, L_LEN / 2, L_LEN - 25):
        hole = Part.makeCylinder(SCREW_D / 2, PLATE + 2, App.Vector(-1, y, zs), App.Vector(1, 0, 0))
        csk = Part.makeCone(SCREW_D / 2, CSK_D / 2, (CSK_D - SCREW_D) / 2 + 0.01,
                            App.Vector(PLATE - (CSK_D - SCREW_D) / 2, y, zs), App.Vector(1, 0, 0))
        body = body.cut(hole).cut(csk)

    # lead-in chamfer on the slot entry to slide the glass in
    ch = 2.0
    def wedge_x(tri_yz, x0, x1):
        v = [App.Vector(x0, y, z) for y, z in tri_yz]
        return Part.Face(Part.makePolygon(v + [v[0]])).extrude(App.Vector(x1 - x0, 0, 0))
    for y0, s in ((0, 1), (L_LEN, -1)):   # both ends: the part is reversible
        body = body.cut(wedge_x([(y0 - s, 0), (y0 + s * ch, 0), (y0 - s, -ch - 1)], BACK - 0.01, LEDGE + 1))
        if BACK > 0:
            body = body.cut(wedge_x([(y0 - s, SLOT), (y0 + s * ch, SLOT), (y0 - s, SLOT + ch + 1)],
                                    BACK - 0.01, TOP_LIP + 1))
    return body.removeSplitter()


def center_bracket():
    # profile in the YZ plane (Y = out from the wall), extruded along X
    def pr(pts):
        v = [App.Vector(0, y, z) for y, z in pts]
        return Part.Face(Part.makePolygon(v + [v[0]])).extrude(App.Vector(C_WIDTH, 0, 0))

    z_top = SLOT + 4 + 22          # plate rises above the glass for the upper screw
    z_bot = -C_H - 22              # and drops below the strut foot for the lower one
    plate = pr([(0, z_bot), (C_PLATE, z_bot), (C_PLATE, z_top), (0, z_top)])
    arm = pr([(0, -C_LT), (C_ARM, -C_LT), (C_ARM, 0), (0, 0)])
    back = pr([(0, 0), (GLASS_BACK, 0), (GLASS_BACK, SLOT), (0, SLOT)])
    lip = pr([(0, SLOT), (GLASS_BACK + C_LIP, SLOT), (GLASS_BACK + C_LIP, SLOT + 4), (0, SLOT + 4)])
    # diagonal strut from the plate foot to 80% of the arm
    ya, za = C_PLATE, -C_H
    yb, zb = C_ARM * 0.8, -C_LT
    import math
    dy, dz = yb - ya, zb - za
    n = math.hypot(dy, dz)
    oy, oz = -dz / n * C_STRUT, dy / n * C_STRUT   # perpendicular offset
    strut = pr([(ya, za), (yb, zb), (yb + oy, zb + oz), (ya + oy, za + oz)])
    strut = strut.common(pr([(0, -C_H), (C_ARM, -C_H), (C_ARM, 0), (0, 0)]))
    # fillets
    f1 = pr([(C_PLATE, -C_LT), (C_PLATE + 15, -C_LT), (C_PLATE, -C_LT - 15)])
    f2 = pr([(C_PLATE, -C_H + 20), (C_PLATE, -C_H), (C_PLATE + 14, -C_H)])
    body = plate.fuse([arm, back, lip, strut, f1, f2])

    # vertical wall slots, clear in front (straight screwdriver access)
    cx = C_WIDTH / 2
    for zc in (z_top - 11, z_bot + 11):
        r = WALL_SCREW / 2
        s = Part.makeCylinder(r, C_PLATE + 2, App.Vector(cx, -1, zc - SLOT_LEN / 2), App.Vector(0, 1, 0))
        s2 = Part.makeCylinder(r, C_PLATE + 2, App.Vector(cx, -1, zc + SLOT_LEN / 2), App.Vector(0, 1, 0))
        sb = Part.makeBox(2 * r, C_PLATE + 2, SLOT_LEN, App.Vector(cx - r, -1, zc - SLOT_LEN / 2))
        body = body.cut(s).cut(s2).cut(sb)
    return body.removeSplitter()


doc = App.newDocument("GlassShelfSupports")
side = side_bracket()
cen = center_bracket()
o1 = doc.addObject("Part::Feature", "SideBracket"); o1.Shape = side
o2 = doc.addObject("Part::Feature", "CenterBracket"); o2.Shape = cen
o2.Placement.Base = App.Vector(80, 0, 0)
doc.recompute()
doc.saveAs(os.path.join(OUT_DIR, "glass_shelf_supports.FCStd"))

for shape, name in ((side, "side_bracket_x2.stl"), (cen, "center_bracket_x1.stl")):
    m = Mesh.Mesh(shape.tessellate(0.05))
    m.write(os.path.join(OUT_DIR, name))
    print(name, "volume cm3:", round(shape.Volume / 1000, 1), "valid:", shape.isValid(),
          "bbox:", shape.BoundBox)
