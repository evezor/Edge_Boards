# board1.py
# random stuff to run on board 1

import random
import time

from pyb import CAN

import bits

def init():
    can = CAN(1, mode=CAN.NORMAL, extframe=True)
    return can

def send(can, can_id, message):
    # only send if there is a free buffer
    # block/hang/sleep until there is (bad?)

    pending_tx = True
    while pending_tx:

        tec, rec, e_warns, e_passives, e_offs, pending_tx, pending_rx0, pending_rx1 = can.info()

        # number of pending TX messages
        time.sleep_ms(pending_tx)

    can.send(message, can_id)

def spew(can):
    # all the numbers as fast as we can
    # send() will trottle it to keep the local buffer from overflowing.

    while True:
        for i in range(536870911):
            send(can, i, 'message!')


def main():
    can = init()
    spew(can)

if __name__=='__main__':
    main()
