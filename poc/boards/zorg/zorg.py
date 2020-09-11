# zorg.py

import json
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

        self.mapo = json.load(open('mapo.json'))
        self.commission = json.load(open('commission.json'))

        print("zorg wakes up")
        self.iam_zorg()

    def zorg(self):

        def assign_can_id(mac):
            # Edge asks for can_id
            bigmac = ':'.join( "{:02x}".format(i) for i in mac )
            print("bigmac: {}".format(bigmac))

            if bigmac not in self.macs:
                self.macs[bigmac] = {}
            can_id = list(self.macs.keys()).index(bigmac)
            self.ocan.send("NWK", can_id, "ZORG_OFFER", mac)

            self.mapo[self.commission[bigmac]]['can_id'] = can_id

            return

        def all_awake():
            # Are all of the Edges awake?
            sleeping = [self.commission[k]
                    for k in self.commission if k not in self.macs]
            print(sleeping)

            return len(sleeping) == 0

        def maps_send_board(board_name):

            # TODO: the in/out/parma data is packed into .data here and
            # unpacked in edge.
            # the pack/unpack format needs to be consistant.
            # it would be nice if the pack/unpack code was in the same place.

            print("sending maps to {}".format(board_name))
            mad_map = self.mapo[board_name]
            can_id = mad_map['can_id'] # target of these messages
            for inny in mad_map['inputs']:
                print(inny)
                # {'function_no': 0, 'channel': 'FM', 'board_name': 'A'}
                message = bytes((
                    channels.index(inny['channel']),
                    inny['function_no']
                    ))
                self.ocan.send("NWK", can_id, "SET_INPUT", message)

            for out in mad_map['outputs']:
                print(out)
                # {'source': {'function_no': 0, 'channel': 'FM', 'board_name': 'A'}, 'function_no': 2}
                # {'source': {'function_no': {1}, 'channel': {0}, 'board_name': {2}}, 'function_no': {3}}
                # chan, src func, src board, dst func
                src_board_chan_id = self.mapo[out['source']['board_name']]['can_id']
                message = bytes((
                    channels.index(out['source']['channel']),
                    out['source']['function_no'],
                    src_board_chan_id,
                    out['function_no']
                    ))
                self.ocan.send("NWK", can_id, "SET_OUTPUT", message)

            for parma in mad_map['parameters']:
                print(parma)
                message = bytes((
                    parma['param_no'],
                    parma['value'],
                    ))
                self.ocan.send("NWK", can_id, "SET_PARMA", message)

            self.ocan.send("NWK", can_id, "RESUME")

        def maps_send_all():

            for board_name in self.mapo:
                maps_send_board(board_name)


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
                    assign_can_id(beer.data)
                    if all_awake():
                        maps_send_all()


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
