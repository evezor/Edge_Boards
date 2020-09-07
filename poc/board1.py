# board1.py
# random stuff to run on board 1

import random
import time

from ocan import OCan

import bits

def zorg(ocan):
    print("zorging...")

    macs = ['zorg',]

    ocan.send("NWK", 0, 0, 'iam zorg')
    ocan._setfilter(0, (0,0) )
    while True:
        beer = ocan.recieve()
        if beer.cid==0 and beer.bonus==0:
            ocan.send("NWK", 0, 0, 'iam zorg')
        if beer.cid==0 and beer.bonus==1:
            mac = beer.data
            if mac not in macs:
                macs.append(mac)
            can_id = macs.index(mac)
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


def main():
    ocan = OCan()
    # spew(ocan)
    zorg(ocan)

if __name__=='__main__':
    main()
