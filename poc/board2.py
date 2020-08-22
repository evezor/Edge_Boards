# board2.py
# random stuff to run on the other board

import time

from ocan import OCan

def drink(ocan):
    print("waiting...")

    last_num = None
    while True:

        beer = ocan.recieve()
        print(beer.channel, beer.cid, beer.bonus, end=' ')

        if last_num is not None:
            assert beer.bonus == last_num + 1
            ticks = time.ticks_ms() - last_tick
            print("*"*ticks)

        last_num = beer.bonus
        last_tick = time.ticks_ms()


def main():
    ocan = OCan()
    ocan._setfilter(0, (0,0) )
    drink(ocan)


if __name__=='__main__':
    main()
