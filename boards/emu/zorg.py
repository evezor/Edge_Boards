# zorg.py

import json
import random
import struct
import time

from collections import OrderedDict

from ocan import *
from board import Board

# System_States
OFF=1
BOOTING=2
STARTING=3
RUNNING=4
PAUSED=5
FAULT=6


class Zorg(Board):

    system_state = OFF

    def iam_zorg(self):
        self.ocan.send("NWK", ZORG_CANID, "ZORG_IAM", 'iam zorg')

    def boot(self):

        print("zorging...")

        self.system_state = BOOTING

        self.mapo = json.load(open('mapo.json'))
        self.commission = json.load(open('commission.json'))

        self.macs = OrderedDict()
        self.macs['zorg'] = {'can_id': ZORG_CANID} # maybe this and that go in ocan or bits

        print("zorg wakes up")
        self.iam_zorg()

        self.system_state = STARTING

    def zorg(self):

        def assign_can_id(mac):
            # Edge asks for can_id

            bigmac = ':'.join( "{:02x}".format(i) for i in mac )
            print("bigmac: {}".format(bigmac))

            if bigmac not in self.commission:
                # new board
                print("{} not in commission".format(bigmac))
                ret = None

            else:
                board_name = self.commission[bigmac]
                print(board_name)

                if board_name not in self.mapo['boards']:
                    # Unused board on the wire
                    print("'{}' not in mapo: {}".format(
                        board_name, self.mapo['boards'].keys()))
                    ret = None

                else:

                    if bigmac not in self.macs:
                        self.macs[bigmac] = {}
                    can_id = list(self.macs.keys()).index(bigmac)

                    self.mapo['boards'][board_name]['can_id'] = can_id
                    self.ocan.send("NWK", can_id, "ZORG_OFFER", mac)

                    ret = board_name

            return ret

        def send_fault(fault_type):
            self.ocan.send("FAULT", ZORG_CANID, header=fault_type)

        def pulse_log(can_id):
            # logs the heartbeat from the board
            mac = list(self.macs.keys())[can_id]
            board_name = self.commission[mac]
            self.mapo['boards'][board_name]['heart']['pulse'] = time.time()

        def ck_version(can_id, version):
            # A board told us its map version,
            # check to see if it is current
            # update the board if it isn't
            if version == self.mapo['version']:
                self.ocan.send("NWK", can_id, "RESUME")
            else:
                mac = list(self.macs.keys())[can_id]
                board_name = self.commission[mac]
                maps_send_board(board_name)

        def ck_hearts():
            for board_name in self.mapo['boards']:
                board = self.mapo['boards'][board_name]
                if 'heart' in board:
                    if board['heart']['pulse'] < time.time()-2:
                        print(board_name, board['heart'])
                        print("no pulse: {}".format(board))
                        send_fault("HALT")
                        self.system_state = FAULT

        def all_awake():
            # Are all of the Edges awake?
            # self.mapo[board_name]['can_id'] = can_id
            sleeping = [ board_name
                    for board_name in self.mapo['boards']
                    if "can_id" not in self.mapo['boards'][board_name]
                    ]
            print("sleeping: {}".format(sleeping))

            return len(sleeping) == 0

        def maps_send_board(board_name):

            # TODO: the in/out/parma message is packed into .message here and
            # unpacked in edge.
            # the pack/unpack format needs to be consistant.
            # it would be nice if the pack/unpack code was in the same place.

            print("sending maps to {}".format(board_name))

            mad_map = self.mapo['boards'][board_name]
            can_id = mad_map['can_id'] # target of these messages

            self.ocan.send("NWK", can_id, "PAUSE")
            self.ocan.send("NWK", can_id, "CLEAR_MAPS")

            self.ocan.send("NWK", can_id, "VERSION",
                    bytes([self.mapo['version']]))

            if 'heart' in mad_map:
                # this looks a lot like a parameter
                self.ocan.send("NWK", can_id, "HEART_RATE",
                        bytes([mad_map['heart']['rate']]))
                pulse_log(can_id)

            for input_ in mad_map['inputs']:
                f,l = "BB", [
                    channels.index(input_['channel']),
                    input_['function_no']
                    ]
                # if "range" in input_:
                #    f += "HH"
                #    l.extend( (input_['range']['low'], input_['range']['high']) )

                message = struct.pack(f,*l)
                self.ocan.send("NWK", can_id, "SET_INPUT", message)
                time.sleep_ms(10)

            for output in mad_map['outputs']:
                print(output)
                src_board_chan_id = self.mapo['boards'][output['source']['board']]['can_id']
                f,l = "BBBB", [
                    channels.index(output['source']['channel']),
                    output['source']['function_no'],
                    src_board_chan_id,
                    output['function_no']
                    ]
                # if "range" in output:
                #    f += "HH"
                #    l.extend((output['range']['low'], output['range']['high']))
                message = struct.pack(f,*l)
                self.ocan.send("NWK", can_id, "SET_OUTPUT", message)

            for parma in mad_map['parameters']:
                print(parma)
                message = bytes((
                    parma['param_no'],
                    parma['value'],
                    ))
                self.ocan.send("NWK", can_id, "SET_PARMA", message)

            self.ocan.send("NWK", can_id, "RESUME")
            time.sleep_ms(10)
            self.ocan.send("NWK", can_id, "SAVE_ME")

        def maps_send_all():

            for board_name in self.mapo['boards']:
                maps_send_board(board_name)

        def nwk(beer):

            if beer.can_id == BOARD_NO_ID:
                # unconfigured Edge

                if beer.header=="BOARD_IAM":
                    # if Edge wakes up, tell it Zorg is awake too.
                    self.iam_zorg()

                elif beer.header=="BOARD_DISCOVER":
                    # Hello board, have some things
                    board_name = assign_can_id(beer.message)
                    # TODO: I don't like this here:
                    if board_name is not None:
                        if self.system_state == RUNNING:
                            maps_send_board(board_name)
                        else:
                            if all_awake():
                                maps_send_all()
                                self.system_state = RUNNING


            elif beer.header=="HEARTBEAT":
                pulse_log(beer.can_id)

            elif beer.header=="VERSION":
                version = beer.message[0]
                ck_version(beer.can_id, version)


        # load up 'dynamic' can_id lists
        # takes the place of assigning id's as he boards boot
        for mac in self.commission:
            mac_bytes = bytes([ int(h,16) for h in mac.split(":")])
            board_name = assign_can_id(mac_bytes)
        # maps_send_all()
        # self.system_state = RUNNING

        # um...
        # reboot all the Edges
        # send_fault("HARD_RESET")
        send_fault("SOFT_RESET")

        # main zorg loop:
        while True:

            if self.system_state == RUNNING:
                ck_hearts()

            beer = self.ocan.recieve(fifo=0, timeout=1)

            if beer is None:
                continue

            if beer.channel == "NWK":
                nwk(beer)

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
