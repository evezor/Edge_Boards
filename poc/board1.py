# board1.py
# random stuff to run on board 1

import random
import time

from collections import OrderedDict

from ocan import OCan

import bits

def zorg(ocan):
    print("zorging...")

    macs = OrderedDict()
    macs['zorg'] = {'cid': 0}

    print("zorg wakes up")
    ocan.send("NWK", 0, 0, 'iam zorg')

    ocan._setfilter(fifo=0, params=(0,0) )
    while True:
        beer = ocan.recieve(fifo=0, timeout=5000)

        if beer is None:
            continue

        elif beer.cid==0 and beer.bonus==0:
            # if Edge wakes up, tell it Zorg is here
            ocan.send("NWK", 0, 0, 'iam zorg')

        elif beer.cid==0 and beer.bonus==1:
            # Edge asks for cid
            mac = beer.data
            if mac not in macs:
                macs[mac] = {}
            can_id = list(macs.keys()).index(mac)
            hacky_1 = 1
            ocan.send("NWK", can_id, hacky_1, mac)

def spew(ocan):
    # all the numbers as fast as we can
    # send() will trottle it to keep the local buffer from overflowing.

    while True:
        for i in range(536870911):
            # channel = i % 2 ** bits.bundle["channel"]
            channel = 'DEBUG'
            cid = i % 2 ** bits.bundle["cid"]
            bonus = i
            ocan.send(channel, cid, bonus, 'message!')


def main(manifest):
    ocan = OCan()
    # spew(ocan)
    zorg(ocan)

if __name__=='__main__':
    main()
