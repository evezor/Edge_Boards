# board2.py
# random stuff to run on the other board

import time

import machine

from ocan import * # OCan
from board import Board

class Edge(Board):

    inputs = []
    outputs = []

    def boot(self):

        print("booting...")
        print("state 0")

        self.parameter_table = self.manifest['parameter_table']

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

    def drink_beer(self):

        beer = self.ocan.recieve(0)
        if beer is not None:
            if beer.can_id == self.can_id:

                if beer.header=='SEND_INPUT':

                    channel, function_no = list(beer.data)
                    print(channel,function_no)
                    print(self.manifest['inputs'])
                    print(self.manifest)
                    self.inputs.append({
                        'channel': channel,
                        'function': self.manifest['inputs'][function_no]
                        })

                elif beer.header=='RESUME':
                    pass

    def check_inputs(self):
        for inny in self.inputs:
            function_name = inny['function']['function']
            function = getattr(self.driver, function_name)
            ret = function(self.parameter_table)
            if ret:
                # print( "{}: {}".format( function_name )
                print( function_name )


    def iris(self):

        while True:

            self.drink_beer()
            self.check_inputs()











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
    edge = Edge(manifest)
    edge.iris()


if __name__=='__main__':
    main()
