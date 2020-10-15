# dump_lables.py
"""
Prints the lables? of a kicad map? that begin with /

Might be a way to seed a manifest.
"""

# https://github.com/realthunder/kicad_parser

from kicad_parser import KicadPCB

pcb = KicadPCB.load("CONTROLLER/GENERIC_CAN.kicad_pcb")

for i in pcb['net']:
    if i[1][0] == "/":
        label = i[1][1:]
        print(i, label)
