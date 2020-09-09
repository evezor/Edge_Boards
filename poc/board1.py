# board1.py
# random stuff to run on board 1

import random
import time

from collections import OrderedDict

from ocan import * # OCan

def zorg(ocan):

    def iam_zorg():
        ocan.send("NWK", ZORG_CANID, "ZORG_IAM", 'iam zorg')

    print("zorging...")

    macs = OrderedDict()
    macs[None] = {'can_id': BOARD_NO_ID}  # unconfigured Edge
    macs['zorg'] = {'can_id': ZORG_CANID} # maybe this and that go in ocan or bits

    print("zorg wakes up")
    iam_zorg()

    ocan._setfilter(fifo=0, params=(0,0) )

    while True:
        beer = ocan.recieve(fifo=0, timeout=5000)

        if beer is None:
            continue

        elif beer.can_id==macs[None]['can_id'] \
                and beer.header=="BOARD_IAM":
            # if Edge wakes up, tell it Zorg is awake
            iam_zorg()

        elif beer.can_id==macs[None]['can_id'] \
                and beer.header=="BOARD_DISCOVER":
            # Edge asks for can_id
            mac = beer.data
            if mac not in macs:
                macs[mac] = {}
            can_id = list(macs.keys()).index(mac)
            ocan.send("NWK", can_id, "ZORG_OFFER", mac)

def spew(ocan):
    # all the numbers as fast as we can
    # send() will trottle it to keep the local buffer from overflowing.

    while True:
        for i in range(536870911):
            # channel = i % 2 ** bits.bundle["channel"]
            channel = 'DEBUG'
            can_id = i % 2 ** bits.bundle["can_id"]
            header = i
            ocan.send(channel, can_id, header, 'message!')


def main(manifest):
    ocan = OCan()
    # spew(ocan)
    zorg(ocan)

if __name__=='__main__':
    main()
