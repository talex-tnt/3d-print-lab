// Piastrina 40 x 40 x 4 mm con foro passante centrale da 6 mm
lato = 40;
altezza = 4;
diametro_foro = 6;   // metti 6.2 se il foro deve accogliere un perno da 6 mm

difference() {
    cube([lato, lato, altezza]);
    translate([lato/2, lato/2, -1])
        cylinder(d = diametro_foro, h = altezza + 2, $fn = 192);
}
