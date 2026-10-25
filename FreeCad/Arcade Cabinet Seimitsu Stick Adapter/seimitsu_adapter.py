# Adapters to mount a Seimitsu LS-32-01 joystick in the control panel of an arcade cabinet
# without drilling the steel sheet. The panel is a 14.5 mm wood board with two through
# cut-outs (one per player) and a 1.8 mm steel sheet on top (it comes off). Each adapter
# fills the area around the stick hole in its cut-out:
#   - with the sheet off, the adapter drops into the cut-out from above and is screwed to
#     the wood with angled wood screws, driven from the top face down and out into the walls
#   - the stick body (62.5 mm square) goes in from below through a square hole; around
#     it, over the PCB / microswitches, the adapter is thinner and ends just above them;
#     outside that area it is as thick as the wood, flush with its bottom face
#   - the LS-32 mounting plate goes in from above into a pocket on the top face and is
#     screwed to the stick body; the plate is flush with the wood (0.1 mm proud) and the
#     steel sheet, once back on, holds it down
# The cut-out outlines were measured from the cardboard tracings (photos in this folder),
# calibrated on the plate, the ruler and the set square.
# FreeCAD script: edit the parameters below and run it again
#   - from FreeCAD: Macro > Macros... > Execute
#   - from a terminal: "/Applications/FreeCAD 1.1.0.app/Contents/Resources/bin/freecadcmd" seimitsu_adapter.py
# All dimensions are in mm.
# Axes (top view, as the player sees the panel): X = right, Y = towards the screen, Z = up.
# Z = 0 is the top of the wood (underside of the steel sheet). Each player's data is
# relative to the centre of their stick hole.

import os
import math
import FreeCAD as App
import Part
import Mesh

V = App.Vector

# ------------- PARAMETERS -------------
# --- panel ---
WOOD_T    = 14.5   # wood board (caliper)
SHEET_T   = 1.8    # steel sheet
SHEET_HOLE = 30.0  # stick hole in the sheet (estimated from the photos, only for the model)

# --- Seimitsu LS-32-01 (measured on the part / photos) ---
PLATE_W   = 98.0   # mounting plate (98 x 65 measured, datasheet says 97)
PLATE_H   = 65.0
PLATE_T   = 1.85
HOUSING   = 62.5   # square body under the plate
HOUSING_H = 10.9   # body height under the plate before the PCB / switches start

# --- fits ---
# The outlines below are the centre of the marker line. The marker was run along the wall
# from inside the cut-out, so the wall is past the outer edge of the line; the first fit
# test (P1) came out 2-3 mm short per side with the line centre.
LINE_HALF = {"P1": 1.13, "P2": 1.46}   # half the marker line width measured on each tracing
TRACE_EXTRA = 1.0  # wall beyond the outer edge of the line
WALL_CLR  = 0.5    # gap between the adapter and the wall
PLATE_FIT = 0.3    # pocket clearance per side
HOUSING_FIT = 0.5  # square hole clearance per side
PLATE_PROUD = 0.1  # plate top above the wood: the sheet presses on the plate
TOP_GAP   = 0.1    # adapter top face below the wood top
PCB_CLR   = 0.6    # gap between the adapter bottom and the PCB / microswitches
PCB_HALF  = 47.0   # half size of the square kept thin under the stick (PCB ~72 x 73, switch tabs +-45)

# --- adapter outline ---
HALF_W    = 53.5   # half width along X (plate is 49 + wall)
CORNER_R  = 2.0    # rounding of the outer corners

# --- wood screws into the walls (3.5 x 20 countersunk) ---
SCREW_L   = 25.0   # length, head included
SCREW_ANGLE = 25.0 # below horizontal, pointing out into the wall
SCREW_IN  = 8.0    # head centre: distance inside the adapter edge
HEAD_Z    = -2.0   # head top (flat of the countersunk head)
SCREW_D   = 3.8    # clearance hole in the adapter (the thread only bites in the wood)
SCREW_HEAD = 7.4   # countersink diameter
CHANNEL_D = 7.6    # access channel above the head, for the head and the screwdriver bit

# --- tabs under the wood (backup support, 3.5 x 16 countersunk wood screws) ---
TAB_T     = 4.0
TAB_W     = 14.0
TAB_END   = 6.0    # material past each hole
TAB_IN    = 5.0    # adapter screw: distance inside the adapter edge
TAB_OUT   = 8.0    # wood screw: distance past the wall
TAB_SCREW_D = 3.8  # clearance in the tab
TAB_SINK  = 7.4    # countersink diameter
PILOT_D   = 2.8    # pilot hole in the adapter
PILOT_DEPTH = 12.5

# --- fit test ---
FIT_T     = 1.6    # thin copy of each footprint, to test the fit in the cut-out

OUT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
# --------------------------------------

# Cut-out outlines (top view, centre of the stick hole = 0,0), from the tracings.
RECESS = {
    "P1": [
        (150.6, -90.6), (152.0, -89.7), (157.1, -82.8), (159.0, -74.4), (166.3, -68.7), (172.5, -61.0),
        (173.2, -59.6), (173.6, -48.5), (176.2, -44.6), (182.6, -40.0), (193.0, -29.3), (198.2, -20.2),
        (198.4, -18.2), (197.9, -16.2), (198.6, -14.9), (201.4, -13.1), (211.8, -9.3), (245.3, 2.1),
        (252.0, 6.4), (255.7, 9.6), (259.1, 13.8), (262.7, 19.9), (264.1, 26.0), (264.4, 32.1),
        (263.9, 36.7), (261.7, 43.4), (258.3, 49.9), (254.2, 54.7), (249.6, 58.2), (244.4, 60.8),
        (236.5, 63.0), (232.2, 63.2), (222.1, 62.4), (216.5, 61.0), (214.7, 59.7), (212.6, 59.5),
        (210.0, 57.8), (207.2, 56.6), (204.6, 56.3), (201.9, 54.7), (197.7, 53.1), (181.4, 48.0),
        (172.9, 44.4), (170.2, 44.2), (168.4, 43.2), (165.8, 42.6), (150.6, 36.2), (138.6, 33.2),
        (134.5, 32.5), (128.9, 33.0), (90.6, 41.8), (80.2, 44.8), (73.2, 46.0), (50.4, 51.7),
        (-7.6, 49.9), (-9.8, 49.6), (-12.2, 48.6), (-15.2, 49.6), (-45.8, 49.0), (-48.5, 49.3),
        (-52.2, 48.7), (-53.7, 47.3), (-54.7, 40.9), (-54.4, 36.7), (-54.9, 33.5), (-55.9, 31.1),
        (-55.8, 28.4), (-56.8, 23.7), (-57.9, 3.6), (-57.8, -36.6), (-57.3, -39.8), (-56.0, -41.5),
        (-50.5, -43.6), (-46.7, -44.0), (-43.6, -43.4), (-41.6, -45.1), (-40.2, -45.7), (-38.0, -45.8),
        (-35.4, -46.7), (-28.5, -47.8), (5.3, -55.8), (19.5, -59.9), (22.3, -60.0), (35.1, -63.6),
        (40.6, -64.4), (46.0, -66.0), (60.9, -69.0), (66.4, -70.8), (71.9, -71.5), (74.9, -72.7),
        (109.1, -81.4), (114.7, -81.9), (118.7, -83.4), (148.9, -90.8)],
    "P2": [
        (-62.2, -64.0), (-13.2, -65.1), (26.8, -65.0), (40.6, -64.5), (47.2, -65.0), (57.5, -64.4),
        (63.1, -65.1), (65.1, -64.4), (68.7, -63.9), (70.9, -62.3), (71.8, -60.4), (72.1, -56.9),
        (73.6, -51.8), (77.6, -45.6), (80.5, -44.1), (124.8, -33.8), (148.0, -27.2), (177.6, -20.5),
        (199.8, -14.3), (202.2, -12.0), (203.1, -8.5), (204.3, 29.6), (203.5, 33.2), (201.0, 36.0),
        (200.1, 39.6), (198.2, 42.8), (198.1, 45.4), (201.4, 51.1), (202.0, 54.9), (204.4, 58.0),
        (205.3, 60.0), (206.1, 76.6), (205.6, 80.3), (203.8, 82.3), (200.7, 83.4), (174.8, 82.8),
        (171.6, 83.1), (170.0, 83.5), (163.0, 88.6), (156.0, 91.5), (151.7, 91.9), (149.1, 91.1),
        (147.2, 89.9), (140.2, 88.8), (137.5, 86.7), (134.8, 82.6), (130.2, 80.8), (110.4, 80.6),
        (98.6, 80.0), (63.0, 71.6), (44.8, 66.6), (9.4, 58.5), (-0.4, 60.1), (-22.2, 68.7),
        (-81.2, 87.8), (-88.9, 89.1), (-91.9, 88.8), (-95.9, 87.2), (-100.8, 84.3), (-105.5, 79.3),
        (-109.2, 71.6), (-110.2, 66.0), (-109.6, 53.4), (-109.9, 43.3), (-109.6, 34.2), (-110.2, 21.6),
        (-110.5, -55.8), (-109.4, -61.6), (-107.6, -63.5), (-105.1, -64.4)],
}
# Where the screws go: a ray from a point inside the adapter, the screw goes into the wall
# where the ray meets it, perpendicular to it.
SCREWS = {
    "P1": [((-40, 0), (0, 1)), ((0, 0), (0, 1)), ((38, 0), (0, 1)),
           ((-24, 0), (0, -1)), ((5, 0), (0, -1)), ((27, 0), (0, -1))],
    "P2": [((-40, 0), (0, -1)), ((0, 0), (0, -1)), ((40, 0), (0, -1)),
           ((-40, 0), (0, 1)), ((0, 0), (0, 1)), ((40, 0), (0, 1))],
}

# Tabs: same idea, a ray to the wall. They must sit where the adapter is full thickness
# (outside the PCB square), so P1 has none on the screen side.
TABS = {
    "P1": [((0, 20), (-1, 0)), ((0, -20), (-1, 0)), ((16, 0), (0, -1))],
    "P2": [((-20, 0), (0, -1)), ((20, 0), (0, -1)), ((-20, 0), (0, 1)), ((20, 0), (0, 1))],
}

# Buttons near the sticks, estimated from the photos (+-5 mm): centre, and the microswitch
# box (x0, x1, y0, y1) as mounted now. Used to keep the adapter clear of them.
BUTTON_R = 17.0
KEEP_MARGIN = 2.0
BUTTONS = {
    "P1": [((82.5, -5.7), (58.7, 79.0, -20.0, 0.6)),
           ((65.0, -48.6), (35.0, 63.5, -63.0, -45.0)),
           ((123.8, -12.0), None), ((170.0, -15.0), None),
           ((107.0, -55.0), None), ((152.0, -60.0), None)],
    "P2": [((81.3, 37.7), None), ((82.0, -7.8), None),
           ((121.6, 9.0), None), ((122.0, 54.5), None),
           ((162.6, 27.8), None), ((162.0, 75.0), None),
           ((-83.6, 61.0), (-100.0, -81.0, 29.0, 71.0))],
}

# Rough position of the two sticks on the panel (only for the context model)
STICK_POS = {"P1": (-290.0, 60.0), "P2": (150.0, 25.0)}
PANEL_W, PANEL_D = 900.0, 430.0

PLATE_TOP = PLATE_PROUD
POCKET_Z = PLATE_TOP - PLATE_T               # pocket floor = plate underside
TOP_Z = -TOP_GAP                             # adapter top face
BOT_Z = POCKET_Z - HOUSING_H + PCB_CLR       # adapter bottom under the stick, just above the PCB
FOOT_Z = -WOOD_T                             # adapter bottom elsewhere, flush with the wood
HOLE = HOUSING + 2 * HOUSING_FIT


# ---------- 2D helpers (faces in the XY plane) ----------
def poly_face(pts, z=0.0):
    v = [V(x, y, z) for x, y in pts]
    return Part.Face(Part.makePolygon(v + [v[0]]))


def rect_face(x0, x1, y0, y1):
    return poly_face([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def rrect_face(w, h, r, cx=0.0, cy=0.0):
    f = rect_face(cx - w / 2 + r, cx + w / 2 - r, cy - h / 2 + r, cy + h / 2 - r)
    return f.makeOffset2D(r)


def disc(cx, cy, r):
    return Part.Face(Part.Wire(Part.makeCircle(r, V(cx, cy, 0))))


def biggest_face(shape):
    return max(shape.Faces, key=lambda f: f.Area)


def prism(face, z0, h):
    f = face.copy()
    f.translate(V(0, 0, z0))
    return f.extrude(V(0, 0, h))


def cyl(r, h, x, y, z):
    return Part.makeCylinder(r, h, V(x, y, z))


def wall_face(player):
    """the cut-out at the wall: traced line centre pushed out to the wall"""
    f = poly_face(RECESS[player])
    return biggest_face(f.makeOffset2D(LINE_HALF[player] + TRACE_EXTRA))


def wall_points(player):
    """wall outline as a CCW list of (x, y), ~0.5 mm apart"""
    pts = [(v.x, v.y) for v in wall_face(player).OuterWire.discretize(Distance=0.5)]
    if pts[0] == pts[-1]:
        pts = pts[:-1]
    area = sum(pts[i - 1][0] * pts[i][1] - pts[i][0] * pts[i - 1][1] for i in range(len(pts)))
    return pts if area > 0 else pts[::-1]


# ---------- screw placement ----------
def ray_hit(pts, origin, direction):
    """first crossing of the ray with the outline: point and outline index"""
    ox, oy = origin
    dx, dy = direction
    best = None
    n = len(pts)
    for i in range(n):
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        den = dx * ey - dy * ex
        if abs(den) < 1e-12:
            continue
        t = ((ax - ox) * ey - (ay - oy) * ex) / den
        u = ((ax - ox) * dy - (ay - oy) * dx) / den
        if t > 0 and 0 <= u <= 1 and (best is None or t < best[0]):
            best = (t, i, u)
    t, i, u = best
    return (ox + t * dx, oy + t * dy), i


def wall_normal(pts, i, span=6.0):
    """inward normal of the wall around segment i, averaged over +-span mm (outline is CCW)"""
    n = len(pts)
    def walk(step):
        j, d = i, 0.0
        while d < span:
            k = (j + step) % n
            d += math.dist(pts[j], pts[k])
            j = k
        return pts[j]
    a, b = walk(-1), walk(1)
    tx, ty = b[0] - a[0], b[1] - a[1]
    L = math.hypot(tx, ty)
    return (-ty / L, tx / L)          # left of the direction of travel = inside for CCW


def screw_axes(player):
    """(head top point, unit axis pointing out and down, wall point) for each screw"""
    pts = wall_points(player)
    out = []
    ca, sa = math.cos(math.radians(SCREW_ANGLE)), math.sin(math.radians(SCREW_ANGLE))
    for origin, direction in SCREWS[player]:
        p, i = ray_hit(pts, origin, direction)
        nx, ny = wall_normal(pts, i)
        d = WALL_CLR + SCREW_IN
        head = V(p[0] + nx * d, p[1] + ny * d, HEAD_Z)
        axis = V(-nx * ca, -ny * ca, -sa)
        out.append((head, axis, p))
    return out


def screw_cutter(head, axis):
    """clearance hole, countersink and screwdriver channel for one screw"""
    sink = (SCREW_HEAD - SCREW_D) / 2
    hole = Part.makeCylinder(SCREW_D / 2, 30, head, axis)
    cone = Part.makeCone(SCREW_HEAD / 2, SCREW_D / 2, sink, head, axis)
    channel = Part.makeCylinder(CHANNEL_D / 2, 40, head, -axis)
    return hole.fuse([cone, channel])


def screw_shape(head, axis):
    """the screw itself, for the model"""
    sink = (SCREW_HEAD - SCREW_D) / 2 - 0.2
    cone = Part.makeCone(SCREW_HEAD / 2 - 0.2, 1.75, sink, head, axis)
    shank = Part.makeCylinder(1.75, SCREW_L - sink, head + axis * sink, axis)
    return cone.fuse(shank)


def tab_frames(player):
    """(adapter screw, wood screw) for each tab"""
    pts = wall_points(player)
    out = []
    for origin, direction in TABS[player]:
        p, i = ray_hit(pts, origin, direction)
        nx, ny = wall_normal(pts, i)
        d = WALL_CLR + TAB_IN
        out.append(((p[0] + nx * d, p[1] + ny * d), (p[0] - nx * TAB_OUT, p[1] - ny * TAB_OUT)))
    return out


def tab_shape(p_in, p_out):
    """flat tab under the wood and the adapter, countersunk from below"""
    cx, cy = (p_in[0] + p_out[0]) / 2, (p_in[1] + p_out[1]) / 2
    half = math.dist(p_in, p_out) / 2
    z0 = FOOT_Z - TAB_T
    body = prism(rrect_face(2 * half + 2 * TAB_END, TAB_W, TAB_W / 2 - 0.01), z0, TAB_T)
    sink = (TAB_SINK - TAB_SCREW_D) / 2
    for x in (-half, half):
        body = body.cut(cyl(TAB_SCREW_D / 2, TAB_T + 2, x, 0, z0 - 1))
        body = body.cut(Part.makeCone(TAB_SINK / 2 + 0.01, TAB_SCREW_D / 2, sink + 0.01, V(x, 0, z0 - 0.01)))
    body.rotate(V(0, 0, 0), V(0, 0, 1), math.degrees(math.atan2(p_in[1] - p_out[1], p_in[0] - p_out[0])))
    body.translate(V(cx, cy, 0))
    return body.removeSplitter()


# ---------- adapter ----------
def footprint(player):
    f = biggest_face(wall_face(player).makeOffset2D(-WALL_CLR))
    f = biggest_face(f.common(rect_face(-HALF_W if player == "P2" else -80, HALF_W, -100, 100)))
    for (bx, by), sw in BUTTONS[player]:
        f = biggest_face(f.cut(disc(bx, by, BUTTON_R + KEEP_MARGIN)))
        if sw:
            x0, x1, y0, y1 = sw
            f = biggest_face(f.cut(rect_face(x0 - KEEP_MARGIN, x1 + KEEP_MARGIN, y0 - KEEP_MARGIN, y1 + KEEP_MARGIN)))
    # round the outer corners
    f = biggest_face(biggest_face(f.makeOffset2D(-CORNER_R)).makeOffset2D(CORNER_R))
    return f


def pocket():
    pw, ph = PLATE_W + 2 * PLATE_FIT, PLATE_H + 2 * PLATE_FIT
    return prism(rrect_face(pw, ph, 1.0), POCKET_Z, TOP_Z - POCKET_Z + 1)


def adapter(player):
    fp = footprint(player)
    body = prism(fp, FOOT_Z, TOP_Z - FOOT_Z)
    # thinner over the PCB / microswitches
    body = body.cut(prism(rrect_face(2 * PCB_HALF, 2 * PCB_HALF, 3.0), FOOT_Z - 1, BOT_Z - FOOT_Z + 1))
    # body of the stick
    body = body.cut(prism(rrect_face(HOLE, HOLE, 1.5), FOOT_Z - 1, TOP_Z - FOOT_Z + 2))
    # plate pocket
    body = body.cut(pocket())
    # wood screws into the walls
    for head, axis, p in screw_axes(player):
        body = body.cut(screw_cutter(head, axis))
    # pilot holes for the tab screws
    for a_in, a_out in tab_frames(player):
        body = body.cut(cyl(PILOT_D / 2, PILOT_DEPTH + 1, a_in[0], a_in[1], FOOT_Z - 1))
    return body.removeSplitter(), fp


def fit_test(fp):
    """thin copy of the footprint, to test the fit in the cut-out before the real print"""
    f = biggest_face(fp.cut(rrect_face(HOLE, HOLE, 1.5)))
    return prism(f, 0, FIT_T)


# ---------- context: panel, sheet, stick, buttons ----------
def moved(shape, player):
    s = shape.copy()
    x, y = STICK_POS[player]
    s.translate(V(x, y, 0))
    return s


def wood():
    b = prism(rect_face(-PANEL_W / 2, PANEL_W / 2, -PANEL_D / 2, PANEL_D / 2), -WOOD_T, WOOD_T)
    for p in RECESS:
        b = b.cut(moved(prism(wall_face(p), -WOOD_T - 1, WOOD_T + 2), p))
    return b


def sheet():
    b = prism(rect_face(-PANEL_W / 2, PANEL_W / 2, -PANEL_D / 2, PANEL_D / 2), PLATE_TOP, SHEET_T)
    for p in RECESS:
        b = b.cut(moved(cyl(SHEET_HOLE / 2, SHEET_T + 2, 0, 0, -1), p))
        for (bx, by), sw in BUTTONS[p]:
            b = b.cut(moved(cyl(15.0, SHEET_T + 2, bx, by, -1), p))
    return b


def buttons(player):
    parts = []
    for (bx, by), sw in BUTTONS[player]:
        parts.append(cyl(BUTTON_R, 30, bx, by, -30))
        if sw:
            x0, x1, y0, y1 = sw
            parts.append(prism(rect_face(x0, x1, y0, y1), -38, 30))
    return Part.makeCompound(parts)


def stick():
    top = PLATE_TOP
    plate = prism(rect_face(-PLATE_W / 2, PLATE_W / 2, -PLATE_H / 2, PLATE_H / 2), top - PLATE_T, PLATE_T)
    plate = plate.cut(cyl(12.0, 5, 0, 0, top - 3))
    zb = top - PLATE_T
    housing = prism(rect_face(-HOUSING / 2, HOUSING / 2, -HOUSING / 2, HOUSING / 2), zb - HOUSING_H, HOUSING_H)
    lower = prism(rect_face(-40, 40, -40, 40), zb - 31.8, 31.8 - HOUSING_H)
    shaft = cyl(4.75, 27.5, 0, 0, top)
    ball = Part.makeSphere(17.5, V(0, 0, top + 27.5 + 16.75))
    return Part.makeCompound([plate, housing, lower, shaft, ball])


# ---------- build ----------
doc = App.newDocument("SeimitsuAdapter")
w = wood()
o = doc.addObject("Part::Feature", "Wood"); o.Shape = w
o = doc.addObject("Part::Feature", "SteelSheet"); o.Shape = sheet()

for p in ("P1", "P2"):
    a, fp = adapter(p)
    axes = screw_axes(p)
    screws = Part.makeCompound([screw_shape(h, ax) for h, ax, _ in axes])
    st = stick()
    bt = buttons(p)
    # checks
    hit_wood = moved(a, p).common(w).Volume
    hit_stick = a.common(st).Volume
    hit_buttons = a.common(bt).Volume
    bb = a.optimalBoundingBox()
    print(f"{p}: adapter {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm, valid {a.isValid()}, "
          f"volume {a.Volume / 1000:.1f} cm3")
    print(f"    overlap with wood {hit_wood:.2f} mm3, stick {hit_stick:.2f} mm3, buttons {hit_buttons:.2f} mm3")
    # material under the plate (what holds it up)
    pw, ph = PLATE_W + 2 * PLATE_FIT, PLATE_H + 2 * PLATE_FIT
    seat = prism(rrect_face(pw, ph, 1.0), FOOT_Z - 1, POCKET_Z - FOOT_Z + 1)
    seat = seat.cut(prism(rrect_face(HOLE, HOLE, 1.5), FOOT_Z - 2, WOOD_T + 4))
    ta = math.tan(math.radians(SCREW_ANGLE))
    above = TOP_Z - (HEAD_Z - SCREW_IN * ta + SCREW_D / 2 / math.cos(math.radians(SCREW_ANGLE)))
    print(f"    screws: {above:.1f} mm of adapter above the hole at the adapter edge")
    for i, (h, ax, wp) in enumerate(axes):
        tip = h + ax * SCREW_L
        sc = moved(screw_shape(h, ax), p)
        in_wood = sc.common(w).Volume / (math.pi * 1.75 ** 2)
        print(f"    screw {i}: wall at ({wp[0]:.1f}, {wp[1]:.1f}), tip Z {tip.z:.1f}, "
              f"~{in_wood:.1f} mm in the wood, channel cuts under the plate: "
              f"{screw_cutter(h, ax).common(seat).Volume:.1f} mm3")
    tabs = [tab_shape(a_in, a_out) for a_in, a_out in tab_frames(p)]
    pcb_zone = prism(rrect_face(2 * PCB_HALF, 2 * PCB_HALF, 3.0), FOOT_Z - 40, 40)
    cutters = Part.makeCompound([screw_cutter(h, ax) for h, ax, _ in axes])
    for i, (a_in, a_out) in enumerate(tab_frames(p)):
        pilot = cyl(PILOT_D / 2 + 1.0, PILOT_DEPTH, a_in[0], a_in[1], FOOT_Z)   # pilot + 1 mm wall
        print(f"    tab {i}: adapter screw ({a_in[0]:.1f}, {a_in[1]:.1f}), wood screw ({a_out[0]:.1f}, {a_out[1]:.1f}), "
              f"under the PCB square {tabs[i].common(pcb_zone).Volume:.1f} mm3, "
              f"pilot vs side screws {pilot.common(cutters).Volume:.1f} mm3, "
              f"pilot in solid {pilot.common(a).Volume / pilot.Volume * 100:.0f} %, "
              f"tab vs wood {moved(tabs[i], p).common(w).Volume:.1f} mm3")
    for name, shp in ((f"Adapter{p}", a), (f"Screws{p}", screws), (f"Tabs{p}", Part.makeCompound(tabs)),
                      (f"Stick{p}", st), (f"Buttons{p}", bt)):
        o = doc.addObject("Part::Feature", name)
        o.Shape = moved(shp, p)
    # print orientation: bottom face on the bed (the thin area under the stick needs supports)
    ap = a.copy()
    ap.translate(V(0, 0, -FOOT_Z))
    Mesh.Mesh(ap.tessellate(0.05)).write(os.path.join(OUT_DIR, f"adapter_{p.lower()}.stl"))
    Mesh.Mesh(fit_test(fp).tessellate(0.05)).write(os.path.join(OUT_DIR, f"fit_test_{p.lower()}.stl"))
    if p == "P2":
        t = tabs[0].copy()
        t.translate(V(0, 0, -(FOOT_Z - TAB_T)))
        c = t.BoundBox.Center
        t.translate(V(-c.x, -c.y, 0))
        Mesh.Mesh(t.tessellate(0.02)).write(os.path.join(OUT_DIR, "tab.stl"))

doc.recompute()
doc.saveAs(os.path.join(OUT_DIR, "seimitsu_adapter.FCStd"))
print(f"adapter top {TOP_Z:.2f}, bottom {BOT_Z:.2f} under the stick ({TOP_Z - BOT_Z:.2f} thick, "
      f"{BOT_Z - POCKET_Z:.2f} under the plate) and {FOOT_Z:.2f} outside ({TOP_Z - FOOT_Z:.2f} thick), "
      f"ball bottom {PLATE_TOP + 27.5 - SHEET_T:.1f} mm above the sheet")
