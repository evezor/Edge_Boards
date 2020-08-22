# board1.py
# random stuff to run on board 1

import random
import time

from ocan import OCan

import bits

def spew(ocan):
    # all the numbers as fast as we can
    # send() will trottle it to keep the local buffer from overflowing.

    while True:
        for i in range(536870911):
            ocan._send(i, 'message!')


def main():
    ocan = OCan()
    spew(ocan)

if __name__=='__main__':
    main()
