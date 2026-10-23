# Replacement for the small grey 4-arm "stabilizer" of a DualShock 2 pad:
# a hub (dome on one side, collar with a 2.1 mm hole on the other) with four thin
# arms in a cross. Each arm steps up near its end into a short rounded tab with a pin on top.
# The original in imgs/ is broken: its +Y arm is missing, so that one mirrors the -Y arm.
# FreeCAD script: edit the parameters below and run it again
#   - from FreeCAD: Macro > Macros... > Execute
#   - from a terminal: "/Applications/FreeCAD 1.1.0.app/Contents/Resources/bin/freecadcmd" pad_stabilizer.py
# All dimensions are in mm, measured with a caliper on the original (see imgs/).
# Axes: Z = up, flat (collar) side of the arms at Z=0, dome and pins pointing +Z.
# Arms: two in line along X (left/right), two in line along Y (front/back).

import os
import math
import FreeCAD as App
import Part
import Mesh

# ------------- PARAMETERS -------------
# --- hub ---
DOME_D    = 6.9    # dome base diameter
DOME_TIP  = 1.4    # flat top of the dome (diameter)
FLANGE_D  = 7.3    # flat ring the arms come out of
COLLAR_D  = 4.8    # collar around the hole, on the flat side
COLLAR_H  = 0.5    # how far the collar stands out of the flat side (estimated from the photos)
HUB_H     = 4.7    # collar bottom to dome top
HOLE_D    = 2.1    # hole in the collar
HOLE_DEPTH = 3.0   # hole depth from the collar face (not measured: blind hole assumed)

# --- arms ---
ARM_T     = 0.9    # arm thickness
ARM_W0    = 2.4    # arm width at the hub
ARM_W1    = 1.6    # arm width at the end (also the tab width)
SPAN      = 25.9   # left tip to right tip
STEM_TIP  = 12.95  # hub center to the tip of the Y arms (not measured: same as the X arms)
ARM_ANGLES = (0, 90, 180, 270)   # a cross: X arms left/right, Y arms front/back

# --- stepped end with pin ---
RISER_T   = 0.9    # thickness of the vertical step
STEP_H    = 2.3    # flat side (Z=0) to the top of the tab
TAB_L     = 1.6    # outer face of the step to the pin center
PIN_D     = 1.0    # pin diameter
PIN_H     = 1.0    # pin height above the tab (end height = STEP_H + PIN_H = 3.3)

OUT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
# --------------------------------------

V = App.Vector


def cyl(d, h, x=0, y=0, z=0):
    return Part.makeCylinder(d / 2, h, V(x, y, z))


def arm(tip):
    """One arm along +X, ending at radius tip (outer edge of the rounded tab)."""
    r_pin = tip - ARM_W1 / 2
    r_out = r_pin - TAB_L              # outer face of the riser
    r_in = r_out - RISER_T             # inner face of the riser = end of the flat arm
    pts = [V(0, -ARM_W0 / 2, 0), V(r_in + 0.01, -ARM_W1 / 2, 0),
           V(r_in + 0.01, ARM_W1 / 2, 0), V(0, ARM_W0 / 2, 0)]
    a = Part.Face(Part.makePolygon(pts + [pts[0]])).extrude(V(0, 0, ARM_T))
    a = a.fuse(Part.makeBox(RISER_T, ARM_W1, STEP_H, V(r_in, -ARM_W1 / 2, 0)))
    z_tab = STEP_H - ARM_T
    a = a.fuse(Part.makeBox(r_pin - r_in, ARM_W1, ARM_T, V(r_in, -ARM_W1 / 2, z_tab)))
    a = a.fuse(cyl(ARM_W1, ARM_T, r_pin, 0, z_tab))     # rounded tab end
    a = a.fuse(cyl(PIN_D, PIN_H, r_pin, 0, STEP_H))
    return a


def stabilizer():
    dome_h = HUB_H - COLLAR_H - ARM_T
    body = cyl(FLANGE_D, ARM_T)
    body = body.fuse(Part.makeCone(DOME_D / 2, DOME_TIP / 2, dome_h, V(0, 0, ARM_T - 0.01)))
    body = body.fuse(cyl(COLLAR_D, COLLAR_H + 0.01, z=-COLLAR_H))
    for ang in ARM_ANGLES:
        tip = STEM_TIP if ang in (90, 270) else SPAN / 2
        a = arm(tip)
        a.rotate(V(0, 0, 0), V(0, 0, 1), ang)
        body = body.fuse(a)
    body = body.cut(cyl(HOLE_D, HOLE_DEPTH, z=-COLLAR_H - 0.01))
    return body.removeSplitter()


s = stabilizer()
bb = s.BoundBox
print(f"size {bb.XLength:.2f} x {bb.YLength:.2f} x {bb.ZLength:.2f} mm, volume {s.Volume:.1f} mm3")
print("valid:", s.isValid())

doc = App.newDocument("PadStabilizer")
o = doc.addObject("Part::Feature", "Stabilizer"); o.Shape = s
doc.recompute()
doc.saveAs(os.path.join(OUT_DIR, "pad_stabilizer.FCStd"))

# print orientation: collar on the bed, dome and pins up (the arms need a little support)
p = s.copy()
p.translate(V(0, 0, -p.BoundBox.ZMin))
Mesh.Mesh(p.tessellate(0.01)).write(os.path.join(OUT_DIR, "pad_stabilizer.stl"))
print("pad_stabilizer.stl", p.BoundBox)
