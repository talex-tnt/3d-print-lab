# Coupler that holds two 10-pin JST XH crimp housings (XHP-10) face to face,
# joined by a strip of 2.54 mm male-male pin header (the black plastic bar stays on).
# A U-shaped cradle takes both housings and the header, the wires leave through a
# slot in each end wall (the wall lips stop the housings from being pulled out),
# and a lid snaps on top with two hooks.
# FreeCAD script: edit the parameters below and run it again
#   - from FreeCAD: Macro > Macros... > Execute
#   - from a terminal: "/Applications/FreeCAD 1.1.0.app/Contents/Resources/bin/freecadcmd" jst_xh_coupler.py
# All dimensions are in mm.
# Axes: X = along the pin row, Y = mating axis (wires leave at both Y ends), Z = up (tray floor at Z=0).

import os
import FreeCAD as App
import Part
import Mesh

# ------------- PARAMETERS -------------
# --- connectors (JST XH datasheet, XHP-10; check them with a caliper) ---
HOUSING_W = 27.3   # housing length along the pin row (XHP-10 "B"), end posts included
HOUSING_D = 5.7    # housing thickness (lock face to back face)
HOUSING_H = 7.75   # housing height along the mating axis (7.5 + 0.25)
BAR_T     = 2.5    # plastic bar of the pin header (2.54 mm header)
# the full stack (housing + bar + housing) as in the photos; measure it if you can
STACK_LEN = 2 * HOUSING_H + BAR_T
WIRE_Z    = HOUSING_D / 2   # wire row height above the housing back face (measure: centered?)
WIRE_ROW  = 22.5   # first-to-last wire distance (9 x 2.5)
WIRE_OD   = 1.9    # max wire insulation diameter (XH: 0.9-1.9)

# --- fits ---
CLR_W     = 0.25   # clearance per side along X
CLR_D     = 0.3    # total clearance on the housing thickness
CLR_L     = 0.3    # total clearance on the stack length (keep it small: no slack = no rattle)
LOCK_RELIEF = 0.6  # shallow pocket in floor and lid for the housing lock bump
RELIEF_MARGIN = 1.2  # border left around that pocket, which still locates the housing

# --- body ---
FLOOR     = 1.6    # tray floor
WALL      = 1.6    # side walls (at the X ends of the pin row)
END_WALL  = 2.0    # end walls the wires go through
LID       = 1.6    # lid plate
SLOT_H    = 3.0    # height of the wire slot in the end walls (>= WIRE_OD + margin)
SLOT_W    = WIRE_ROW + WIRE_OD + 1.0   # width of the wire slot

# --- snap hooks on the lid ---
HOOK_W    = 8.0    # hook width (along Y)
HOOK_T    = 1.2    # hook arm thickness
HOOK_NUB  = 0.6    # how far the nub reaches into the groove
HOOK_GAP  = 0.15   # gap between hook arm and tray wall
GROOVE_Z  = 1.2    # groove bottom above the tray floor bottom
GROOVE_H  = 1.4    # groove height
FIT       = 0.2    # clearance of the lid tongues in the wire slots

OUT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
# --------------------------------------

CAV_W = HOUSING_W + 2 * CLR_W
CAV_D = HOUSING_D + CLR_D
CAV_L = STACK_LEN + CLR_L
OUT_W = CAV_W + 2 * WALL
OUT_L = CAV_L + 2 * END_WALL
TRAY_H = FLOOR + CAV_D
WZ = FLOOR + CLR_D / 2 + WIRE_Z           # wire row height in the tray
SLOT_Z0 = WZ - SLOT_H / 2                  # bottom of the wire slot
SLOT_Z1 = WZ + SLOT_H / 2                  # top of the wire slot (the lid tongue comes down to here)


def box(x0, y0, z0, dx, dy, dz):
    return Part.makeBox(dx, dy, dz, App.Vector(x0, y0, z0))


def relief(z0):
    m = RELIEF_MARGIN
    return box(-CAV_W / 2 + m, -CAV_L / 2 + m, z0, CAV_W - 2 * m, CAV_L - 2 * m, LOCK_RELIEF)


def tray():
    body = box(-OUT_W / 2, -OUT_L / 2, 0, OUT_W, OUT_L, TRAY_H)
    body = body.cut(box(-CAV_W / 2, -CAV_L / 2, FLOOR, CAV_W, CAV_L, CAV_D + 1))
    body = body.cut(relief(FLOOR - LOCK_RELIEF))
    # wire slots, open at the top so the wires drop in
    for y in (-OUT_L / 2 - 1, CAV_L / 2 - 0.01):
        body = body.cut(box(-SLOT_W / 2, y, SLOT_Z0, SLOT_W, END_WALL + 1.01, TRAY_H))
    # grooves for the lid hooks on the outside of the side walls
    for sx in (-1, 1):
        x0 = OUT_W / 2 - HOOK_NUB if sx > 0 else -OUT_W / 2 - 0.01
        body = body.cut(box(x0, -HOOK_W / 2 - 0.5, GROOVE_Z, HOOK_NUB + 0.01, HOOK_W + 1, GROOVE_H))
    return body.removeSplitter()


def lid():
    # modelled in place, on top of the tray
    z0 = TRAY_H
    body = box(-OUT_W / 2, -OUT_L / 2, z0, OUT_W, OUT_L, LID)
    # tongues that close the top of the wire slots
    for y in (-OUT_L / 2, CAV_L / 2):
        body = body.fuse(box(-SLOT_W / 2 + FIT, y, SLOT_Z1, SLOT_W - 2 * FIT, END_WALL, z0 - SLOT_Z1 + 0.01))
    # snap hooks hanging down outside the side walls
    for sx in (-1, 1):
        xin = sx * (OUT_W / 2 + HOOK_GAP)               # inner face of the hook arm
        x0 = xin if sx > 0 else xin - HOOK_T
        body = body.fuse(box(x0, -HOOK_W / 2, GROOVE_Z, HOOK_T, HOOK_W, z0 - GROOVE_Z + 0.01))
        xb = OUT_W / 2 - 0.01 if sx > 0 else -OUT_W / 2 - HOOK_GAP - HOOK_T
        body = body.fuse(box(xb, -HOOK_W / 2, z0, HOOK_GAP + HOOK_T + 0.01, HOOK_W, LID))
        # nub: flat catch on top, 45 degree lead-in below
        reach = HOOK_GAP + HOOK_NUB - 0.05             # tip stops 0.05 short of the groove bottom
        xt = xin - sx * reach
        top = GROOVE_Z + GROOVE_H - 0.05
        tip = 0.3
        pts = [(xin, top), (xt, top), (xt, top - tip), (xin, top - tip - reach)]
        v = [App.Vector(x, -HOOK_W / 2, z) for x, z in pts]
        nub = Part.Face(Part.makePolygon(v + [v[0]])).extrude(App.Vector(0, HOOK_W, 0))
        body = body.fuse(nub)
    # lock-bump pocket on the inside of the lid
    body = body.cut(relief(z0 - 0.01))
    return body.removeSplitter()


t = tray()
l = lid()
clash = t.common(l).Volume
print(f"stack {STACK_LEN:.2f}  cavity {CAV_W:.2f} x {CAV_L:.2f} x {CAV_D:.2f}")
print(f"outside {OUT_W + 2 * (HOOK_GAP + HOOK_T):.1f} x {OUT_L:.1f} x {TRAY_H + LID:.1f} mm")
print(f"wire slot z {SLOT_Z0:.2f}-{SLOT_Z1:.2f}, lips {SLOT_Z0 - FLOOR - CLR_D / 2:.2f} / {FLOOR + CLR_D / 2 + HOUSING_D - SLOT_Z1:.2f} mm on the housing back")
print("tray valid:", t.isValid(), "lid valid:", l.isValid(), "overlap mm3:", round(clash, 4))

doc = App.newDocument("JstXhCoupler")
for name, shp in (("Tray", t), ("Lid", l)):
    o = doc.addObject("Part::Feature", name); o.Shape = shp
doc.recompute()
doc.saveAs(os.path.join(OUT_DIR, "jst_xh_coupler.FCStd"))

# print orientation: tray on its floor, lid upside down (flat face on the bed, hooks up)
lp = l.copy()
lp.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), 180)
lp.translate(App.Vector(0, 0, -lp.BoundBox.ZMin))
Mesh.Mesh(t.tessellate(0.02)).write(os.path.join(OUT_DIR, "tray.stl"))
Mesh.Mesh(lp.tessellate(0.02)).write(os.path.join(OUT_DIR, "lid.stl"))
print("tray.stl", t.BoundBox, "\nlid.stl", lp.BoundBox)
