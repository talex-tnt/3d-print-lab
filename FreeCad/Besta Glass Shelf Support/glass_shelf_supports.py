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

# --- anti-tip clip (a frame around the wall plate of a metal bracket, flush with the wall, with a lip
#     over the back edge of the glass) ---
# Made for T-shaped flat-bar shelf brackets (TESSTINA "concealed" type): wall plate 100 x 30 x 5.8 mm,
# arm a flat bar laid flat, leaving the plate bottom edge. MEASURE YOURS and adjust.
BAR_W     = 38.0   # arm width
BAR_T     = 5.8    # arm thickness
PLATE_W   = 100.0  # wall plate width
PLATE_T   = 5.8    # wall plate thickness (the clip frame is just as thick, so both sit flush on the wall)
PLATE_UP  = 24.0   # how far the wall plate rises above the top of the arm
BEND_R    = 4.0    # clearance for the bend between plate and arm: the back edge of the glass sits at PLATE_T + BEND_R
FIT       = 0.4    # clearance around the arm and the plate
CLIP_SIDE = 10.0   # frame width left and right of the plate
CLIP_TOP  = 3.0    # frame width above the plate
CLIP_LIP  = 12.0   # how far the lip covers the glass
CLIP_LIP_T = 5.0   # lip thickness
CLIP_FLOOR = 5.0   # frame bar under the wall plate (holds the set screws)
SET_D     = 3.4    # set screw holes (M4 screws self-tap into the plastic, press on the plate bottom edge)
SET_X     = 32.0   # set screws left and right of center

# --- reference model of the metal bracket (not printed, only to check the fit in FreeCAD) ---
BAR_LEN   = 250.0  # arm length
PLATE_CH  = 8.0    # chamfer on the ends of the wall plate
BEND_IN   = 2.0    # inner radius of the plate/arm bend (must be smaller than BEND_R)
# --- rounding ---
R_INNER   = 5.0    # fillet on inner (concave) structural corners
R_OUTER   = 1.5    # fillet on outer corners
R_SLOT    = 0.8    # fillet in the corners where the glass sits (keep small)
R_END     = 1.0    # fillet on the edges of the end faces

OUT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
# ------------------------------------------------------------------------


def prism(pts_xz, length):
    """Profile in the XZ plane, extruded along +Y."""
    v = [App.Vector(x, 0, z) for x, z in pts_xz]
    face = Part.Face(Part.makePolygon(v + [v[0]]))
    return face.extrude(App.Vector(0, length, 0))


def round_corners(body, corners, axis):
    """Fillet the edges running along `axis` ('x' or 'y') at the given profile corners [(u, z, r), ...]."""
    def at(e, u, z):
        bb = e.BoundBox
        lo, hi = (bb.XMin, bb.XMax) if axis == "y" else (bb.YMin, bb.YMax)
        return abs(lo - u) < 1e-6 and abs(hi - u) < 1e-6 and abs(bb.ZMin - z) < 1e-6 and abs(bb.ZMax - z) < 1e-6
    for u, z, r in corners:
        body = body.makeFillet(r, [e for e in body.Edges if at(e, u, z)])
    return body


def round_ends(body, axis, r):
    """Fillet every edge lying in the two end faces normal to `axis`."""
    def flat(e):
        bb = e.BoundBox
        return abs(bb.YMax - bb.YMin) < 1e-6 if axis == "y" else abs(bb.XMax - bb.XMin) < 1e-6
    return body.makeFillet(r, [e for e in body.Edges if flat(e)])


def side_bracket():
    gz = -(LEDGE_T + (LEDGE - PLATE))       # foot of the 45 degree gusset
    pts = [(0, -DROP), (PLATE, -DROP), (PLATE, gz), (LEDGE, -LEDGE_T), (LEDGE, 0)]
    if BACK > 0:
        pts += [(BACK, 0), (BACK, SLOT), (TOP_LIP, SLOT), (TOP_LIP, SLOT + TOP_T), (0, SLOT + TOP_T)]
    else:
        pts += [(0, 0)]
    body = prism(pts, L_LEN)
    corners = [(0, -DROP, R_OUTER), (PLATE, -DROP, R_OUTER), (PLATE, gz, R_INNER),
               (LEDGE, -LEDGE_T, R_OUTER), (LEDGE, 0, R_OUTER)]
    if BACK > 0:
        corners += [(BACK, 0, R_SLOT), (BACK, SLOT, R_SLOT), (TOP_LIP, SLOT, R_OUTER),
                    (TOP_LIP, SLOT + TOP_T, R_OUTER), (0, SLOT + TOP_T, R_OUTER)]
    else:
        corners += [(0, 0, R_OUTER)]
    body = round_ends(round_corners(body, corners, "y"), "y", R_END)

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
    # Y = out from the wall (wall at Y=0), Z = up (top of the metal arm at Z=0), X = along the wall.
    # A frame around the wall plate, flush with the wall, plus a lip over the back edge of the glass.
    # The metal bracket carries the glass; the clip only stops the back edge from lifting.
    xw = PLATE_W / 2 + FIT + CLIP_SIDE       # half width
    yg = PLATE_T + BEND_R                    # back edge of the glass
    zb = -BAR_T - FIT - CLIP_FLOOR           # underside
    zt = PLATE_UP + FIT + CLIP_TOP           # top of the frame
    pts = [(0, zb), (PLATE_T, zb), (PLATE_T, 0), (yg, 0), (yg, SLOT),
           (yg + CLIP_LIP, SLOT), (yg + CLIP_LIP, SLOT + CLIP_LIP_T), (PLATE_T, SLOT + CLIP_LIP_T),
           (PLATE_T, zt), (0, zt)]
    v = [App.Vector(-xw, y, z) for y, z in pts]
    body = Part.Face(Part.makePolygon(v + [v[0]])).extrude(App.Vector(2 * xw, 0, 0))
    corners = [(0, zb, R_OUTER), (PLATE_T, zb, R_OUTER),   # (PLATE_T, 0) stays sharp: a fillet there would touch the arm
               (yg, 0, R_SLOT), (yg, SLOT, R_SLOT), (yg + CLIP_LIP, SLOT, R_OUTER),
               (yg + CLIP_LIP, SLOT + CLIP_LIP_T, R_OUTER), (PLATE_T, SLOT + CLIP_LIP_T, 3.0),
               (PLATE_T, zt, R_OUTER), (0, zt, R_OUTER)]
    body = round_ends(round_corners(body, corners, "x"), "x", R_END)
    # opening for the wall plate (and the root of the arm): the frame sits around it, flush with the wall
    hp = PLATE_W / 2 + FIT
    body = body.cut(Part.makeBox(2 * hp, PLATE_T + 1 + FIT, PLATE_UP + BAR_T + 2 * FIT,
                                 App.Vector(-hp, -1, -BAR_T - FIT)))
    # clearance for the plate/arm bend
    hw = BAR_W / 2 + FIT
    v = [App.Vector(-hw, y, z) for y, z in ((PLATE_T - 0.5, -0.01), (PLATE_T + BEND_R + 0.01, -0.01),
                                            (PLATE_T - 0.5, BEND_R + 0.5))]
    body = body.cut(Part.Face(Part.makePolygon(v + [v[0]])).extrude(App.Vector(2 * hw, 0, 0)))
    # 2 set screws from below, pressing on the bottom edge of the wall plate
    for x in (-SET_X, SET_X):
        body = body.cut(Part.makeCylinder(SET_D / 2, CLIP_FLOOR + 2, App.Vector(x, PLATE_T / 2, zb - 1)))
    return body.removeSplitter()


def metal_bracket_ref():
    """T-shaped flat-bar shelf bracket: wall plate standing on the wall, arm leaving its bottom edge."""
    hp, hw = PLATE_W / 2, BAR_W / 2
    zp0, zp1 = -BAR_T, PLATE_UP
    v = [App.Vector(x, 0, z) for x, z in ((-hp + PLATE_CH, zp0), (hp - PLATE_CH, zp0), (hp, zp0 + PLATE_CH),
                                          (hp, zp1 - PLATE_CH), (hp - PLATE_CH, zp1), (-hp + PLATE_CH, zp1),
                                          (-hp, zp1 - PLATE_CH), (-hp, zp0 + PLATE_CH))]
    plate = Part.Face(Part.makePolygon(v + [v[0]])).extrude(App.Vector(0, PLATE_T, 0))
    arm = Part.makeBox(BAR_W, BAR_LEN, BAR_T, App.Vector(-hw, 0, -BAR_T))
    body = plate.fuse(arm).removeSplitter()
    bend = [e for e in body.Edges if abs(e.BoundBox.YMin - PLATE_T) < 1e-6 and abs(e.BoundBox.YMax - PLATE_T) < 1e-6
            and abs(e.BoundBox.ZMin) < 1e-6 and abs(e.BoundBox.ZMax) < 1e-6 and e.BoundBox.XLength <= BAR_W + 1e-6]
    body = body.makeFillet(BEND_IN, bend)
    zc = (zp0 + zp1) / 2
    for x in (-hp + 12, 0, hp - 12):   # countersunk wall screw holes
        body = body.cut(Part.makeCylinder(2.75, PLATE_T + 2, App.Vector(x, -1, zc), App.Vector(0, 1, 0)))
        body = body.cut(Part.makeCone(2.75, 5.5, 2.76, App.Vector(x, PLATE_T - 2.75, zc), App.Vector(0, 1, 0)))
    for y in (60, 150, BAR_LEN - 20):  # screw holes along the arm
        body = body.cut(Part.makeCylinder(2.25, BAR_T + 2, App.Vector(0, y, -BAR_T - 1)))
    return body


def check_fit(clip, ref, glass):
    """Print the overlap between the clip and the metal bracket / glass, also while sliding the clip on."""
    for d in (0, 1, 3, 6, 15, 40):
        c = clip.copy(); c.translate(App.Vector(0, d, 0))
        print(f"clip {d:>2} mm from home: overlap with bracket {c.common(ref).Volume:.3f} mm3")
    print(f"clip home: overlap with glass {clip.common(glass).Volume:.3f} mm3,"
          f" gap to bracket {clip.distToShape(ref)[0]:.2f} mm")


doc = App.newDocument("GlassShelfSupports")
side = side_bracket()
clip = anti_tip_clip()
o1 = doc.addObject("Part::Feature", "SideBracket"); o1.Shape = side
o1.Placement.Base = App.Vector(-200, 0, 0)
o2 = doc.addObject("Part::Feature", "AntiTipClip"); o2.Shape = clip
# reference parts, mounted around the clip (wall at Y=0, top of the metal arm at Z=0)
ref = metal_bracket_ref()
glass = Part.makeBox(300, 400, GLASS_T, App.Vector(-150, PLATE_T + BEND_R, PAD))
o3 = doc.addObject("Part::Feature", "Ref_MetalBracket"); o3.Shape = ref
o4 = doc.addObject("Part::Feature", "Ref_Glass"); o4.Shape = glass
if App.GuiUp:
    o3.ViewObject.ShapeColor = (0.2, 0.2, 0.2)
    o4.ViewObject.ShapeColor = (0.6, 0.8, 0.9); o4.ViewObject.Transparency = 60
check_fit(clip, ref, glass)
doc.recompute()
doc.saveAs(os.path.join(OUT_DIR, "glass_shelf_supports.FCStd"))

for shape, name in ((side, "side_bracket_x2.stl"), (clip, "anti_tip_clip_x2.stl")):
    m = Mesh.Mesh(shape.tessellate(0.05))
    m.write(os.path.join(OUT_DIR, name))
    print(name, "volume cm3:", round(shape.Volume / 1000, 1), "valid:", shape.isValid(),
          "bbox:", shape.BoundBox)
