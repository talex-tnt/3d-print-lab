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

# --- anti-tip clip (slides on the arm of a metal wall bracket, holds the back edge of the glass) ---
# Made for T-shaped flat-bar shelf brackets (TESSTINA "concealed" type): wall plate 100 x 30 x 5.8 mm,
# arm a flat bar laid flat, leaving the plate bottom edge. MEASURE YOURS and adjust.
BAR_W     = 38.0   # arm width
BAR_T     = 5.8    # arm thickness
PLATE_T   = 5.8    # wall plate thickness
PLATE_UP  = 24.0   # how far the wall plate rises above the top of the arm
BEND_R    = 4.0    # clearance for the bend between plate and arm
FIT       = 0.4    # clearance around the arm
CLIP_W    = 100.0  # clip width (covers the wall plate)
CLIP_WALL = 4.0    # front wall thickness: the back edge of the glass ends up at PLATE_T + 0.3 + CLIP_WALL from the wall
CLIP_LIP  = 12.0   # how far the lip covers the glass
CLIP_LIP_T = 4.0   # lip thickness
CLIP_REACH = 25.0  # how far the clip runs along the arm
CLIP_FLOOR = 4.0   # thickness under the arm
SET_D     = 3.4    # set screw hole (M4 screw self-taps into the plastic)
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


def anti_tip_clip():
    # profile in the YZ plane (Y = out from the wall, Z = up, top of the metal arm at Z=0), extruded along X
    y0 = PLATE_T + 0.3                       # back face rests against the wall plate
    yw = y0 + CLIP_WALL                      # back edge of the glass
    zb = -BAR_T - FIT - CLIP_FLOOR           # underside
    pts = [(y0, zb), (y0 + CLIP_REACH, zb), (y0 + CLIP_REACH, 0), (yw, 0), (yw, SLOT),
           (yw + CLIP_LIP, SLOT), (yw + CLIP_LIP, SLOT + CLIP_LIP_T), (yw, SLOT + CLIP_LIP_T),
           (yw, PLATE_UP + 1), (y0, PLATE_UP + 1)]
    v = [App.Vector(-CLIP_W / 2, y, z) for y, z in pts]
    body = Part.Face(Part.makePolygon(v + [v[0]])).extrude(App.Vector(CLIP_W, 0, 0))
    # the glass slot is open: glass rests on the arm (and on the clip top at Z=0) with felt
    # channel for the metal arm
    hw = BAR_W / 2 + FIT
    body = body.cut(Part.makeBox(2 * hw, CLIP_REACH + 2, BAR_T + FIT + 0.01,
                                 App.Vector(-hw, y0 - 1, -BAR_T - FIT)))
    # clearance for the plate/arm bend
    v = [App.Vector(-hw, y, z) for y, z in ((y0 - 1, -0.01), (y0 + BEND_R, -0.01), (y0 - 1, BEND_R + 1))]
    body = body.cut(Part.Face(Part.makePolygon(v + [v[0]])).extrude(App.Vector(2 * hw, 0, 0)))
    # set screw from below: presses the arm up against the clip and stops it sliding
    body = body.cut(Part.makeCylinder(SET_D / 2, CLIP_FLOOR + 2,
                                      App.Vector(0, y0 + CLIP_REACH - 9, zb - 1)))
    return body.removeSplitter()


doc = App.newDocument("GlassShelfSupports")
side = side_bracket()
clip = anti_tip_clip()
o1 = doc.addObject("Part::Feature", "SideBracket"); o1.Shape = side
o2 = doc.addObject("Part::Feature", "AntiTipClip"); o2.Shape = clip
o2.Placement.Base = App.Vector(120, 0, 0)
doc.recompute()
doc.saveAs(os.path.join(OUT_DIR, "glass_shelf_supports.FCStd"))

for shape, name in ((side, "side_bracket_x2.stl"), (clip, "anti_tip_clip_x2.stl")):
    m = Mesh.Mesh(shape.tessellate(0.05))
    m.write(os.path.join(OUT_DIR, name))
    print(name, "volume cm3:", round(shape.Volume / 1000, 1), "valid:", shape.isValid(),
          "bbox:", shape.BoundBox)
