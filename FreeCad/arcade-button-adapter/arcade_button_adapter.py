# Ring adapter for a 24 mm arcade button in a 29 mm panel hole.
# The flange sits on the front of the panel, the tube goes through the hole and the button
# snaps into the tube: its clips rest on the ledge at the top of the 25 mm bore.
# The adapter holds in the panel with 4 flexible tabs cut in the tube. Each tab is anchored
# at the top of the tube and hangs down to just above the flange, with a hook just behind the panel.
# The tab ends stop TAB_GAP above the flange, so the front face stays a closed ring: they print
# sagging onto the flange and the light bond breaks the first time the tabs are squeezed.
# To remove it: take out the button, squeeze the 4 hooks inward from behind the panel and push.
# FreeCAD script: edit the parameters below and run it again
#   - from FreeCAD: Macro > Macros... > Execute
#   - from a terminal: "/Applications/FreeCAD 1.1.0.app/Contents/Resources/bin/freecadcmd" arcade_button_adapter.py
# All dimensions are in mm.
# Axes: Z = up, front face of the flange at Z=0, tube pointing +Z (= behind the panel).

import os
import math
import FreeCAD as App
import Part
import Mesh

# ------------- PARAMETERS -------------
# --- panel ---
PANEL_HOLE = 29.0   # hole in the panel
PANEL_T    = 1.85   # panel thickness (2.0 left a little play up and down)

# --- flange (front of the panel) ---
FLANGE_D   = 36.0
FLANGE_T   = 0.5
FLANGE_R   = 0.5    # rounded bottom outer edge

# --- tube ---
TUBE_D     = 28.9   # 0.05 mm clearance per side in the panel hole (28.6 was loose)
TUBE_H     = 9.5    # total height, flange included
BORE_D     = 25.0   # button body
LEDGE_H    = 2.5    # height of the 25 mm bore = ledge the button clips rest on
CLIP_D     = 27.0   # room for the button clips, above the ledge

# --- tabs ---
TABS       = 4
TAB_W      = 7.0    # tab width (along the circumference)
SLOT_W     = 0.8    # slots on the sides of each tab
TAB_IN_D   = 27.2   # inner diameter of the tabs
TAB_FOOT_IN_D = 28.1  # inner diameter of the tab ends below the hook, thinner so they don't hit the ledge when pushed in
TAB_TOP    = 8.5    # top of the slots: above this the tube is a full ring the tabs hang from
LEDGE_GAP_D = 26.2  # ledge outer diameter behind the tabs (room for the tab ends to flex in)
NOTCH_D    = 29.4   # room around each tab, above the flange
TAB_GAP    = 0.2    # gap between the tab ends and the flange (raise to 0.3 if they stay fused)
HOOK       = 0.7    # how far the hook reaches over the hole edge (0.3 and 0.5 held too little)
HOOK_PLAY  = 0.05   # extra space for the panel between the flange and the hook
HOOK_RAMP  = 2.0    # height of the hook's lead-in slope

OUT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
# --------------------------------------

V = App.Vector
Z = V(0, 0, 1)


def revolve(pts, angle=360, start=0):
    """Revolve a closed (r, z) polygon around Z, from angle start for angle degrees."""
    w = Part.makePolygon([V(r, 0, z) for r, z in pts] + [V(pts[0][0], 0, pts[0][1])])
    s = Part.Face(w).revolve(V(0, 0, 0), Z, angle)
    s.rotate(V(0, 0, 0), Z, start)
    return s


def sector(r_in, r_out, z0, z1, width, ang):
    """Ring sector centered on angle ang, width measured as an arc at r_out."""
    a = math.degrees(width / r_out)
    return revolve([(r_in, z0), (r_out, z0), (r_out, z1), (r_in, z1)], a, ang - a / 2)


def body():
    r_t, r_f, r_c, r_b = TUBE_D / 2, FLANGE_D / 2, CLIP_D / 2, BORE_D / 2
    # profile with the rounded flange edge
    e = [Part.LineSegment(V(r_b, 0, 0), V(r_f - FLANGE_R, 0, 0)).toShape(),
         Part.Arc(V(r_f - FLANGE_R, 0, 0),
                  V(r_f - FLANGE_R + FLANGE_R * math.sin(math.pi / 4), 0, FLANGE_R * (1 - math.cos(math.pi / 4))),
                  V(r_f, 0, FLANGE_R)).toShape()]
    pts = [(r_f, FLANGE_R), (r_f, FLANGE_T), (r_t, FLANGE_T), (r_t, TUBE_H), (r_c, TUBE_H),
           (r_c, LEDGE_H), (r_b, LEDGE_H), (r_b, 0)]
    for a, b in zip(pts, pts[1:]):
        if a != b:
            e.append(Part.LineSegment(V(a[0], 0, a[1]), V(b[0], 0, b[1])).toShape())
    s = Part.Face(Part.Wire(Part.__sortEdges__(e))).revolve(V(0, 0, 0), Z, 360)
    return s


def adapter():
    s = body()
    r_t = TUBE_D / 2
    z_hook = FLANGE_T + PANEL_T + HOOK_PLAY       # underside of the hook = back of the panel
    r_hook = PANEL_HOLE / 2 + HOOK
    for i in range(TABS):
        ang = 360 / TABS * i
        # free the tab: slots and room behind it, down to the flange (the front face stays closed)
        s = s.cut(sector(LEDGE_GAP_D / 2, NOTCH_D / 2, FLANGE_T, TAB_TOP, TAB_W + 2 * SLOT_W, ang))
        tab = sector(TAB_IN_D / 2, r_t, FLANGE_T + TAB_GAP, TAB_TOP + 0.01, TAB_W, ang)
        tab = tab.cut(sector(TAB_IN_D / 2 - 0.01, TAB_FOOT_IN_D / 2, -1, z_hook, TAB_W + 0.1, ang))
        a = math.degrees(TAB_W / r_t)
        hook = revolve([(r_t - 0.01, z_hook), (r_hook, z_hook), (r_t - 0.01, z_hook + HOOK_RAMP)],
                       a, ang - a / 2)
        s = s.fuse(tab).fuse(hook)
    return s.removeSplitter()


s = adapter()
bb = s.BoundBox
print(f"size {bb.XLength:.2f} x {bb.YLength:.2f} x {bb.ZLength:.2f} mm, volume {s.Volume:.1f} mm3")
print("valid:", s.isValid(), "solids:", len(s.Solids))

doc = App.newDocument("ArcadeButtonAdapter")
o = doc.addObject("Part::Feature", "Adapter"); o.Shape = s
doc.recompute()
doc.saveAs(os.path.join(OUT_DIR, "arcade_button_adapter.FCStd"))

# print orientation: flange on the bed, tube up, no supports (the tab ends print over the TAB_GAP)
Mesh.Mesh(s.tessellate(0.01)).write(os.path.join(OUT_DIR, "arcade_button_adapter.stl"))
print("arcade_button_adapter.stl", bb)
