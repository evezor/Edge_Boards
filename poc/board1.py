# board1.py
# random stuff to run on board 1

import random
import time

from ocan import OCan

import bits

def zorg(ocan):
    ocan.send(channel, cid, i, 'message!')
    while True:
        pass

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
    spew(ocan)

if __name__=='__main__':
    main()
