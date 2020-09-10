# board2.py
# random stuff to run on the other board

import time

import machine

from ocan import * # OCan

class Edge():

    can_id = None
    ocan = None

    def __init__(self):
        self.ocan = OCan()
        self.ocan._setfilter(0, (0,0) )

    def init_board(self, manifest):
        if "driver" in manifest:
            module = __import__(manifest['driver'])
            print(module)
            driver = getattr( module, manifest['driver'] )()
            print(driver)
            if "init" in manifest:
                init = getattr(driver,manifest['init'])
                print(init)
                init()

            self.driver = driver

    def boot(self):

        print("booting...")
        print("state 0")

        # >>> binascii.unhexlify('ff0000ff')
        # b'\xff\x00\x00\xff'
        # mac = b'\xff\x00\x00\xff'
        mac = bytes(list(machine.unique_id())[::2])

        print("state 1")
        # hello zorg, I am here
        self.ocan.send("NWK", BOARD_NO_ID, "BOARD_IAM", b'iam bord')

        # wait for Zorg to be awwake
        beer = None
        while beer is None:
            beer = self.ocan.recieve(0, timeout=5000)
            if beer is not None \
                    and beer.can_id == ZORG_CANID \
                    and beer.header == "ZORG_IAM":
                break
            else:
                beer=None

        print("state 2")
        # Zorg awake, tell zorg mac:
        self.ocan.send("NWK", BOARD_NO_ID, "BOARD_DISCOVER", mac )

        print("state 3")
        # wait for Zorg to assign a can_id
        can_id = None
        while can_id is None:
            beer = self.ocan.recieve(0, timeout=1000)
            if beer is None:
                continue

            if beer.channel=='NWK' \
                and beer.header == "ZORG_OFFER" \
                and beer.data == mac:
                    can_id = beer.can_id
                    break

        print("booted! can_id:{}".format(can_id))
        self.can_id = can_id

    def iris(self):
        pass


def drink(ocan):
    # not maintained doubt this works any more.

    ocan._setfilter(0, (0,0) )

    print("waiting...")

    last_num = None
    while True:

        beer = ocan.recieve()
        print(beer.channel, beer.can_id, beer.header, beer.data, end=' ')

        if last_num is not None:
            assert beer.header == last_num + 1, "sequance broken by {}".format(beer.header - last_num)
            ticks = time.ticks_ms() - last_tick
            print("*"*ticks)

        last_num = beer.header
        last_tick = time.ticks_ms()


def main(manifest):
    edge = Edge()
    edge.init_board(manifest)
    edge.boot()
    edge.iris()


if __name__=='__main__':
    main()
