# board2.py
# random stuff to run on the other board

import time

from pyb import CAN

import bits


def init():
    can = CAN(1, mode=CAN.NORMAL, extframe=True)
    return can

def set_filter(can):
    can.setfilter(0, CAN.MASK32, 0, (0,0) )
    # can.setfilter(1, CAN.MASK32, 0, (0b11111111111111111111111111111,0) )
    # can.setfilter(2, CAN.MASK32, 0, (0,0b11111111111111111111111111111) )
    # can.setfilter(3, CAN.MASK32, 0, ( 0b11111111111111111111111111111,
    #    0b11111111111111111111111111111) )

def recieve(can):

    r = None
    while r is None:
        try:
            r = can.recv(0)
        except OSError: # [Errno 110] ETIMEDOUT
            continue

    return r

def drink(can):
    print("waiting...")

    last_id = None
    while True:

        can_id, rtr, fmi, data = recieve(can)
        print(can_id, end=' ')

        if last_id is not None:
            assert can_id == last_id + 1
            ticks = time.ticks_ms() - last_tick
            print("*"*ticks)

        last_id = can_id
        last_tick = time.ticks_ms()



def main():
    can = init()
    set_filter(can)
    drink(can)

if __name__=='__main__':
    main()
