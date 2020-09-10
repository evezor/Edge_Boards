# zorg.py

import random
import time

from collections import OrderedDict

from ocan import * # OCan
from board import Board

class Zorg(Board):

    def iam_zorg(self):
        self.ocan.send("NWK", ZORG_CANID, "ZORG_IAM", 'iam zorg')

    def boot(self):

        print("zorging...")

        self.macs = OrderedDict()
        self.macs['zorg'] = {'can_id': ZORG_CANID} # maybe this and that go in ocan or bits

        print("zorg wakes up")
        self.iam_zorg()

    def zorg(self):

        def assign_can_id(mac):
            # Edge asks for can_id
            if mac not in self.macs:
                self.macs[mac] = {}
            can_id = list(self.macs.keys()).index(mac)
            self.ocan.send("NWK", can_id, "ZORG_OFFER", mac)

            return can_id

        def send_map(can_id):
            print("sending maps to {}".format(can_id))

        while True:

            beer = self.ocan.recieve(fifo=0, timeout=-1)
            # blocking here:
            if beer is None:
                continue

            # all the zorg things:

            if beer.can_id == BOARD_NO_ID:
                # unconfigured Edge

                if beer.header=="BOARD_IAM":
                    # if Edge wakes up, tell it Zorg is awake too.
                    self.iam_zorg()

                elif beer.header=="BOARD_DISCOVER":

                    # Hello board, have some things
                    can_id = assign_can_id(beer.data)
                    send_map(can_id)


def spew(ocan):
    # all the numbers as fast as we can
    # send() will trottle it to keep the local buffer from overflowing.

    while True:
        for i in range(536870911):
            # channel = i % 2 ** bits.bundle["channel"]
            channel = 'DEBUG'
            can_id = i % 2 ** bits.bundle["can_id"]
            header = i
            ocan.send(channel, can_id, header, 'message!')


def main(manifest):
    zorg = Zorg(manifest)
    zorg.zorg()

if __name__=='__main__':
    main()
