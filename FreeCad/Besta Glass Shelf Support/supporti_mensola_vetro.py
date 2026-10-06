# Supporti per mensola in vetro IKEA BESTA 180x40 cm
# Script FreeCAD: modifica i parametri qui sotto e rilancialo
#   - da FreeCAD: Macro > Macros... > Esegui
#   - da terminale: /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd supporti_mensola_vetro.py
# Tutte le misure sono in mm.

import os
import FreeCAD as App
import Part
import Mesh

# ---------------- PARAMETRI (MISURA PRIMA DI STAMPARE!) ----------------
GLASS_T   = 6.0    # spessore del vetro (misuralo col calibro)
PAD       = 1.0    # spessore feltrino/gommino adesivo (sopra e sotto il vetro)
CLEAR     = 0.6    # gioco per infilare il vetro
SLOT      = GLASS_T + 2 * PAD + CLEAR   # altezza della fessura

# --- supporto laterale (si avvita al fianco del mobile alto) ---
L_LEN     = 170.0  # lunghezza lungo la profondita' (si stampa in piedi: A1 mini max 180)
BACK      = 3.0    # spessore della U tra vetro e mobile. Serve: luce tra i mobili >= 1800 + 2*BACK + 2
                   # metti 0 se il vetro entra "a filo": diventa una L (solo appoggio, senza labbro sopra)
LEDGE     = 30.0   # quanto il ripiano entra sotto il vetro
LEDGE_T   = 6.0    # spessore del ripiano inferiore
TOP_LIP   = 12.0   # quanto il labbro superiore copre il vetro
TOP_T     = 4.0    # spessore labbro superiore
PLATE     = 6.0    # spessore piastra contro il mobile (sotto il ripiano)
DROP      = 46.0   # quanto scende la piastra sotto il piano d'appoggio
SCREW_D   = 4.0    # foro vite (viti truciolare 3.5 mm)
CSK_D     = 8.0    # diametro svasatura testa vite

# --- supporto centrale (a muro, sostiene il centro del vetro) ---
C_WIDTH   = 40.0   # larghezza
C_ARM     = 165.0  # sbalzo dal muro (si stampa sdraiato: A1 mini piatto 180x180)
C_H       = 120.0  # altezza sotto il piano d'appoggio
C_PLATE   = 8.0    # spessore piastra a muro
C_LT      = 8.0    # spessore braccio
C_STRUT   = 10.0   # spessore puntone diagonale
GLASS_BACK = 10.0  # distanza muro -> bordo posteriore del vetro (min. 4)
C_LIP     = 12.0   # labbro superiore sopra il bordo posteriore del vetro
WALL_SCREW = 5.2   # larghezza asola per vite a muro (tassello 6 + vite 4.5/5)
SLOT_LEN  = 6.0    # escursione asola per regolare l'altezza (+-3 mm)

OUT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
# ------------------------------------------------------------------------


def prism(pts_xz, length):
    """Profilo nel piano XZ, estruso lungo +Y."""
    v = [App.Vector(x, 0, z) for x, z in pts_xz]
    face = Part.Face(Part.makePolygon(v + [v[0]]))
    return face.extrude(App.Vector(0, length, 0))


def supporto_laterale():
    gz = -(LEDGE_T + (LEDGE - PLATE))       # base del raccordo a 45 gradi
    pts = [(0, -DROP), (PLATE, -DROP), (PLATE, gz), (LEDGE, -LEDGE_T), (LEDGE, 0)]
    if BACK > 0:
        pts += [(BACK, 0), (BACK, SLOT), (TOP_LIP, SLOT), (TOP_LIP, SLOT + TOP_T), (0, SLOT + TOP_T)]
    else:
        pts += [(0, 0)]
    body = prism(pts, L_LEN)

    # 3 viti orizzontali nel fianco del mobile, sotto il raccordo (accessibili col cacciavite)
    zs = (gz - DROP) / 2
    for y in (25, L_LEN / 2, L_LEN - 25):
        hole = Part.makeCylinder(SCREW_D / 2, PLATE + 2, App.Vector(-1, y, zs), App.Vector(1, 0, 0))
        csk = Part.makeCone(SCREW_D / 2, CSK_D / 2, (CSK_D - SCREW_D) / 2 + 0.01,
                            App.Vector(PLATE - (CSK_D - SCREW_D) / 2, y, zs), App.Vector(1, 0, 0))
        body = body.cut(hole).cut(csk)

    # smusso d'invito sul lato anteriore della fessura per infilare il vetro
    ch = 2.0
    def wedge_x(tri_yz, x0, x1):
        v = [App.Vector(x0, y, z) for y, z in tri_yz]
        return Part.Face(Part.makePolygon(v + [v[0]])).extrude(App.Vector(x1 - x0, 0, 0))
    for y0, s in ((0, 1), (L_LEN, -1)):   # entrambi i lati: il pezzo e' reversibile
        body = body.cut(wedge_x([(y0 - s, 0), (y0 + s * ch, 0), (y0 - s, -ch - 1)], BACK - 0.01, LEDGE + 1))
        if BACK > 0:
            body = body.cut(wedge_x([(y0 - s, SLOT), (y0 + s * ch, SLOT), (y0 - s, SLOT + ch + 1)],
                                    BACK - 0.01, TOP_LIP + 1))
    return body.removeSplitter()


def supporto_centrale():
    # profilo nel piano YZ (Y = uscita dal muro), estruso lungo X
    def pr(pts):
        v = [App.Vector(0, y, z) for y, z in pts]
        return Part.Face(Part.makePolygon(v + [v[0]])).extrude(App.Vector(C_WIDTH, 0, 0))

    z_top = SLOT + 4 + 22          # la piastra sale sopra il vetro per la vite superiore
    z_bot = -C_H - 22              # e scende sotto il piede del puntone per quella inferiore
    plate = pr([(0, z_bot), (C_PLATE, z_bot), (C_PLATE, z_top), (0, z_top)])
    arm = pr([(0, -C_LT), (C_ARM, -C_LT), (C_ARM, 0), (0, 0)])
    back = pr([(0, 0), (GLASS_BACK, 0), (GLASS_BACK, SLOT), (0, SLOT)])
    lip = pr([(0, SLOT), (GLASS_BACK + C_LIP, SLOT), (GLASS_BACK + C_LIP, SLOT + 4), (0, SLOT + 4)])
    # puntone diagonale dalla base della piastra all'80% del braccio
    ya, za = C_PLATE, -C_H
    yb, zb = C_ARM * 0.8, -C_LT
    import math
    dy, dz = yb - ya, zb - za
    n = math.hypot(dy, dz)
    oy, oz = -dz / n * C_STRUT, dy / n * C_STRUT   # offset perpendicolare
    strut = pr([(ya, za), (yb, zb), (yb + oy, zb + oz), (ya + oy, za + oz)])
    strut = strut.common(pr([(0, -C_H), (C_ARM, -C_H), (C_ARM, 0), (0, 0)]))
    # raccordi
    f1 = pr([(C_PLATE, -C_LT), (C_PLATE + 15, -C_LT), (C_PLATE, -C_LT - 15)])
    f2 = pr([(C_PLATE, -C_H + 20), (C_PLATE, -C_H), (C_PLATE + 14, -C_H)])
    body = plate.fuse([arm, back, lip, strut, f1, f2])

    # tappo del bordo braccio arrotondato: smusso sulla punta inferiore
    # asole verticali a muro, libere davanti (cacciavite dritto)
    cx = C_WIDTH / 2
    for zc in (z_top - 11, z_bot + 11):
        r = WALL_SCREW / 2
        s = Part.makeCylinder(r, C_PLATE + 2, App.Vector(cx, -1, zc - SLOT_LEN / 2), App.Vector(0, 1, 0))
        s2 = Part.makeCylinder(r, C_PLATE + 2, App.Vector(cx, -1, zc + SLOT_LEN / 2), App.Vector(0, 1, 0))
        sb = Part.makeBox(2 * r, C_PLATE + 2, SLOT_LEN, App.Vector(cx - r, -1, zc - SLOT_LEN / 2))
        body = body.cut(s).cut(s2).cut(sb)
    return body.removeSplitter()


doc = App.newDocument("SupportiMensolaVetro")
lat = supporto_laterale()
cen = supporto_centrale()
o1 = doc.addObject("Part::Feature", "SupportoLaterale"); o1.Shape = lat
o2 = doc.addObject("Part::Feature", "SupportoCentrale"); o2.Shape = cen
o2.Placement.Base = App.Vector(80, 0, 0)
doc.recompute()
doc.saveAs(os.path.join(OUT_DIR, "supporti_mensola_vetro.FCStd"))

for shape, name in ((lat, "supporto_laterale_x2.stl"), (cen, "supporto_centrale_x1.stl")):
    m = Mesh.Mesh(shape.tessellate(0.05))
    m.write(os.path.join(OUT_DIR, name))
    print(name, "volume cm3:", round(shape.Volume / 1000, 1), "valid:", shape.isValid(),
          "bbox:", shape.BoundBox)
