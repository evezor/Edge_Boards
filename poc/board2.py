# board2.py
# random stuff to run on the other board

import time

from ocan import OCan

def boot(ocan):

    print("booting...")
    print("state 0")

    # >>> binascii.unhexlify('ff0000ff')
    # b'\xff\x00\x00\xff'
    # mac = b'\xff\x00\x00\xff'
    mac = machine.unique_id()[-5:]

    print("state 1")
    # hello zorg, I am here
    ocan.send("NWK", 0, 0, b'')

    # wait for Zorg to wake up
    ocan._setfilter(0, (0,0) )
    beer = ocan.recieve()
    # zorg: who are you?
    print("state 2")

    # I am foof:
    ocan.send("NWK", 0, 1, mac )

    # wait for Zorg to assign a can_id
    ocan._setfilter(0, (0,0) )
    can_id = None
    while can_id is None:
        beer = ocan.recieve()
        print("state 3")
        hacky_1 = 1
        if beer.bonus == hacky_1 and beer.data == mac:
            can_id = beer.cid
            break

    print("booted!")



def drink(ocan):

    ocan._setfilter(0, (0,0) )

    print("waiting...")

    last_num = None
    while True:

        beer = ocan.recieve()
        print(beer.channel, beer.cid, beer.bonus, beer.data, end=' ')

        if last_num is not None:
            assert beer.bonus == last_num + 1, "sequance broken by {}".format(beer.bonus - last_num)
            ticks = time.ticks_ms() - last_tick
            print("*"*ticks)

        last_num = beer.bonus
        last_tick = time.ticks_ms()


def main():
    ocan = OCan()
    # drink(ocan)
    boot(ocan)


if __name__=='__main__':
    main()
