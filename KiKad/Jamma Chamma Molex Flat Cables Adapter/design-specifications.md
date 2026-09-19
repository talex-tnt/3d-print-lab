# JAMMA/CHAMMA Extension Cable: Molex + Flat Cable Adapter

Design specifications (KiCad project). Status: draft, pre-layout.

## 1. Goal

An extension "cable" for JAMMA and CHAMMA that is made of:

- two adapter boards, one at each end;
- one Molex (Mini-Fit Jr) cable carrying power and GND;
- one flat (IDC ribbon) cable carrying all signals.

One adapter is the **female** end and plugs onto the game board's edge fingers. The other is the **male** end (PCB edge fingers) and plugs into the cabinet/supergun harness (for example a Pandora Box, which may output CHAMMA).

```
 Game board  <--[female adapter]==Molex (power/GND)==[male adapter]--> Cabinet / supergun / Pandora Box
                               ==Flat (signals)=====
```

The connection is straight-through: pin N at one end is pin N at the other end.

## 2. Molex power cable

Connector family: **Molex Mini-Fit Jr, 4.2 mm pitch, 2x4 (8 circuits)**, same housing at both ends, 1:1 harness (no crossovers).

### 2.1 Pinout

Pin 1 is directly opposite pin 5. Verify the numbering against the Molex drawing before finalizing the KiCad footprint.

| Row | Pin 1 | Pin 2 | Pin 3 | Pin 4 |
|---|---|---|---|---|
| Top | +12V (6a+6b) | GND A | GND B | -5V (5a+5b) |

| Row | Pin 5 | Pin 6 | Pin 7 | Pin 8 |
|---|---|---|---|---|
| Bottom | +5V A (3a+3b) | 27a: P1 Button 6 (CHAMMA) / GND (JAMMA) | 27b: P2 Button 6 (CHAMMA) / GND (JAMMA) | +5V B (4a+4b) |

Placement rationale:

- 27a and 27b (pins 6 and 7) have GND above them and +5V or the other 27 wire beside them. A 5V neighbor is harmless on a button input.
- +12V and -5V are kept away from the button-6 wires, so a stray strand or a half-seated housing cannot put 12V or -5V on a button input.

### 2.2 Net grouping on the adapter boards

| Net | JAMMA fingers | Molex pins |
|---|---|---|
| +5V | 3a, 3b, 4a, 4b (bridged into one pour) | 5, 8 |
| +12V | 6a, 6b | 1 |
| -5V | 5a, 5b | 4 |
| GND | 1a, 1b, 2a, 2b, 28a, 28b (one pour) | 2, 3 |
| Pin 27a | 27a | 6 |
| Pin 27b | 27b | 7 |

Both +5V pins are fed from the same pour and both GND pins from the same pour, so the original A/B grouping of the fingers no longer matters. It also shares the current between the two wires.

### 2.3 Pin 27 (27a/27b) pass-through

- 27a/27b stay on the Molex for JAMMA backward compatibility.
- The Molex only links the two adapters (it is not fed by a PSU harness), so these wires are a pure pass-through. Whatever is on 27 at one end appears at the other end: GND from a JAMMA source, or Button 6 from a CHAMMA source such as a Pandora Box.
- Known limitation: a CHAMMA game board on a JAMMA-only cabinet receives GND on 27, which the board sees as Button 6 held down. This is identical to plugging the two together without the adapter.
- Optional extra (not in the base design): a per-end 3-pad solder jumper on 27a/27b that connects the finger either to the local GND pour or to the cable. Independent per-end settings would isolate mismatched combinations. Default position: GND.
- Verify the CHAMMA pin 27 = Button 6 assignment against your reference pinout.

### 2.4 Known trade-offs of the pinout

- In CHAMMA mode wires 6 and 7 stop being GND, leaving two GND wires (pins 2 and 3) for the whole return current. This is fine for a typical Pandora-Box-driven board. For a high-current board in CHAMMA mode, consider a **2x5 (10-circuit)** Mini-Fit Jr connector for two extra GND wires.
- A button-6 logic line runs in a bundle with 5V and 12V power wires. Keep the Molex harness short and tidy to limit coupled noise.

### 2.5 Wire and connector parts

| Item | Part | Notes |
|---|---|---|
| Cable-end housing | Molex 39-01-2080 (5557-08R) | Dual row, 8 circuits, 4.2 mm pitch; one at each end |
| Crimp terminals | Molex 5556 series female | 8 per end; pre-crimped leads 0797580001 / 0797580009 are an alternative |
| PCB header, gold | Molex 39-30-1082 | Right-angle, 8 circuits, snap-in peg; one per adapter board |
| PCB header, tin | Molex 39-30-1080 | Same header with tin plating |
| Wire | 16 AWG or heavier | Same length for the +5V and GND wires |

Current rating: distributor listings show 13 A per contact for the housing (one lists 9 A). The real rating depends on wire gauge and loaded circuits, so confirm in the Molex datasheet.

Do not use a PC-PSU-looking connector without clear polarity marking: a Mini-Fit Jr 2x4 resembles PC EPS/PCIe 8-pin connectors. Mark polarity and pin 1 on the silkscreen, and label the cable so it cannot be mistaken for a PC power lead.

## 3. Flat (signal) cable

### 3.1 Decision

- **One 50-way IDC ribbon (2x25)**: 1.27 mm wire pitch, 2.54 mm IDC connector pitch, female IDC socket at both ends, 1:1 (pin N to pin N), target length 30 cm.
- Why 50-way: the ribbon carries 38 signals (see 3.2). A 40-way leaves only 2 spare conductors for GND, and a 56-way (2x28) is not a common standard size. The 50-way leaves 12 spare conductors.
- Fallback if a 50-way cannot be sourced: two 26-way (2x13) ribbons (52 conductors, 14 spare). This is the only case in which the design uses two flat cables.

### 3.2 Pin budget

| Item | Count |
|---|---|
| Fingers: 28 positions x 2 faces | 56 |
| Pin 7 (a and b) is the key slot, no finger | -2 |
| Contacts | 54 |
| Power/GND on the Molex: 1, 2, 3, 4, 5, 6, 28 (a and b) | -14 |
| 27a and 27b on the Molex (see 2.3) | -2 |
| **Signals on the ribbon** (includes the video GND finger) | **38** |
| Ribbon conductors | 50 |
| **Spare conductors** | **12** |

Route every remaining finger, including the ones unused in plain JAMMA, so the adapter also works with JAMMA+/CHAMMA boards. Confirm the count against your netlist.

### 3.3 Use of the 12 spare conductors

| Use | Conductors |
|---|---|
| GND interleaved between the video lines (R, G, B, sync) | 5 |
| Second conductor in parallel for each speaker line | 2 |
| GND guard on each side of the speaker pair | 2 |
| GND spread among the digital inputs | 3 |

- All extra GND conductors connect to the GND pour at both ends.
- Carry the video GND finger on the ribbon.
- A 28 AWG ribbon conductor is good for roughly 1 A (confirm with the cable data). The speaker lines can carry about 0.6 A at 3 W into 8 ohm, hence the doubled conductors.
- Keep the ribbon short: video quality degrades with length. Target 30 cm, keep it under about 50 cm.
- A pin-by-pin table (JAMMA finger to ribbon pin) is still to be written once the JAMMA/CHAMMA reference pinout is chosen.

### 3.4 Board connectors

- One shrouded, keyed **box header 2x25 (2.54 mm)** per adapter board, vertical or right-angle. It is about 61 mm long, which fits inside the 111 mm width of the edge connector. Check the footprint in KiCad's `Connector_IDC` library.
- Mark pin 1 on both boards. With the ribbon laid straight between the two boards, pin 1 must sit on the same physical side of the ribbon at both ends. If the boards face opposite ways, mirror one footprint.

### 3.5 Purchasing (cheap, standard parts)

- **Chosen cable:** AliExpress item 33029492417 (`https://it.aliexpress.com/item/33029492417.html`), a grey flat ribbon with female IDC connectors, 2.54 mm pitch, 30 cm, listed for 105 C and 300 V, with 6 to 50 pin variants. **Select the 50-pin variant.**
- Check before ordering: a female socket at both ends, the red pin-1 stripe on the same side at both ends, and the conductor gauge (not stated in the listing).
- On arrival: continuity test of all 50 conductors, and no shorts between neighbouring conductors.
- **Alternative:** bare 50-conductor ribbon plus two 50-pin female IDC sockets, crimped in a vise. The listing links its IDC sockets at `https://www.aliexpress.com/item/1005001400147026.html`.

## 4. Adapter boards

### 4.1 Male end (to cabinet/supergun)

- 1.6 mm PCB, hard-gold plated edge fingers, chamfered edge.
- Key slot at the pin 7 position.
- 28 positions per face at the JAMMA 3.96 mm pitch. Pin 7 is the key slot, so 27 fingers per face (54 contacts).

### 4.2 Female end (to game board)

- Card-edge connector for JAMMA (28 positions x 2 faces), 3.96 mm pitch, with a key plug at the pin 7 position.
- Mounting holes or a support so the connector's weight does not stress the game board fingers.

### 4.3 Layout rules

- Wide pours on both layers for +5V and GND, with stitching vias, or use 2 oz copper. Check widths with an IPC-2221 calculator for your worst-case current.
- Vias are required to bridge the a and b fingers of the same pin (they are on opposite faces).
- Keep a low-resistance path from the fingers to the Molex header pins.
- Identical Molex header pinout on both boards so the cable is symmetric.

## 5. Face (a/b) convention

- Conventions for which face is "a" and which is "b" vary between sources. Verify against the game board and the harness that you are using.
- Do a full continuity test through the assembled cable before applying power. A female connector at one end and edge fingers at the other is where a/b mix-ups happen.

## 6. Acceptance checks

1. Continuity test of every finger through Molex and ribbon, both ends, both faces, and of all 50 ribbon conductors.
2. GND, +5V, +12V and -5V isolated from each other (no shorts) with a multimeter.
3. Polarity and pin 1 markings visible on both boards and on the harness.
4. Bench power test with a current-limited supply before connecting a real board.
5. Test with a JAMMA game board and a CHAMMA source (button 6 pass-through).

## 7. Open items

- Final cable length (ribbon and Molex). The ribbon is planned at 30 cm.
- Whether to include the per-end 27a/27b jumpers.
- Whether to use a 2x5 Molex for extra GND.
- Confirm CHAMMA pin 27 assignment and the a/b face convention against your reference documents.
- Write the pin-by-pin table (JAMMA finger to ribbon pin) once the reference pinout is chosen.
- Verify the 50-pin variant of the AliExpress ribbon (female at both ends, 1:1, conductor gauge) before ordering.
