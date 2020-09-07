# board1.py
# random stuff to run on board 1

import random
import time

from collections import OrderedDict

from ocan import * # OCan

import bits

def zorg(ocan):

    def iam_zorg():
        ocan.send("NWK", ZORG_CANID, NWK_ZORG_IAM, 'iam zorg')

    print("zorging...")

    macs = OrderedDict()
    macs[None] = {'cid': BOARD_NO_ID}  # unconfigured Edge
    macs['zorg'] = {'cid': ZORG_CANID} # maybe this and that go in ocan or bits

    print("zorg wakes up")
    iam_zorg()

    ocan._setfilter(fifo=0, params=(0,0) )

    while True:
        beer = ocan.recieve(fifo=0, timeout=5000)

        if beer is None:
            continue

        elif beer.cid==macs[None]['cid'] \
                and beer.header==NWK_BOARD_IAM:
            # if Edge wakes up, tell it Zorg is awake
            iam_zorg()

        elif beer.cid==macs[None]['cid'] \
                and beer.header==NWK_BOARD_DISCOVER:
            # Edge asks for cid
            mac = beer.data
            if mac not in macs:
                macs[mac] = {}
            can_id = list(macs.keys()).index(mac)
            ocan.send("NWK", can_id, NWK_ZORG_OFFER, mac)

def spew(ocan):
    # all the numbers as fast as we can
    # send() will trottle it to keep the local buffer from overflowing.

    while True:
        for i in range(536870911):
            # channel = i % 2 ** bits.bundle["channel"]
            channel = 'DEBUG'
            cid = i % 2 ** bits.bundle["cid"]
            header = i
            ocan.send(channel, cid, header, 'message!')


def main(manifest):
    ocan = OCan()
    # spew(ocan)
    zorg(ocan)

if __name__=='__main__':
    main()
