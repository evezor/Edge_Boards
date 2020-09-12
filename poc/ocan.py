# ocan.py
# OshBus on Can

# parameter names of wrappers come from:
# https://docs.micropython.org/en/latest/library/pyb.CAN.html#pyb.CAN.info

import time
import random

from collections import OrderedDict, namedtuple

from pyb import CAN

from bundle import Bundle

BOARD_NO_ID = 0
ZORG_CANID = 1

channels = [
        "e",
        "falt",
        "FH",
        "",
        "",
        "FM",
        "",
        "",
        "FL",
        "",
        "",
        "NWK",
        "",
        "",
        "DEBUG",
        ]

NWK = [
"ZORG_IAM",
"BOARD_IAM",
"BOARD_DISCOVER",
"ZORG_OFFER",
"PAUSE",
"RESUME",
"SET_INPUT",
"SET_OUTPUT",
"SET_PARMA",
]

BeerCan = namedtuple('BeerCan', [
    "channel", "can_id", "header",
    "rtr", "fmi", "message",
    ])

class CanMessageId(Bundle):

    def __init__(self):
        self.bundle = OrderedDict()
        self.bundle["channel"] = 4
        self.bundle["can_id"] = 7
        self.bundle["header"] = 18
        self.bundle_size = 29

class Header(Bundle):

    def __init__(self):
        self.bundle = OrderedDict()
        self.bundle["rfe"] = 4
        self.bundle["random"] = 14
        self.bundle_size = 18

class OCan():

    def __init__(self, bus=1):
        self.can = CAN(bus, mode=CAN.NORMAL, extframe=True,
                prescaler=12, bs1=11, bs2=2)

    def _send(self, msg_id, message):
        # id is the id of the message to be sent.

        # only send if there is a free buffer
        # block/hang/sleep until there is (bad?)

        # TODO: try: .send() except: if no buffers sleep and loop.

        pending_tx = True
        while pending_tx:

            tec, rec, e_warns, e_passives, e_offs, pending_tx, pending_rx0, pending_rx1 = self.can.info()

            # number of pending TX messages
            time.sleep_ms(pending_tx)

        self.can.send(message, msg_id)

    def send(self, channel_name, can_id, header=0, message=b''):
        print("tx: ",channel_name, can_id, header, message)
        channel_num = channels.index(channel_name)

        ci = CanMessageId()

        if channel_name == "NWK":
            # this has got to go.  somewhere.
            hi = Header()
            header = hi.pack( rfe=NWK.index(header), random=random.getrandbits(14))

        msg_id = ci.pack(
                channel=channel_num, can_id=can_id, header=header)

        ret = self._send(msg_id, message)

        beer = BeerCan( channel_name, can_id, header,
                None, None, message )

        return beer


    def _setfilter(self, fifo, params):
        # always 1, MASK32 I hope.
        self.can.setfilter(1, CAN.MASK32, fifo, params)


    def _recieve(self, fifo, timeout):

        try:
            r = self.can.recv(fifo, timeout=timeout)
        except OSError: # [Errno 110] ETIMEDOUT
            r = None

        return r

    def recieve(self, fifo, timeout=0):

        ret = self._recieve(fifo, timeout)

        if ret is None:
            beercan = None
        else:
            can_id, rtr, fmi, message  = ret
            ci = CanMessageId()
            r2 = ci.unpack(can_id)
            channel_name = channels[ r2.channel ]

            if channel_name == "NWK":
                hi = Header()
                header = hi.unpack( r2.header)
                header = NWK[header.rfe]
            else:
                header = r2.header

            beercan = BeerCan( channel_name, r2.can_id, header,
                    rtr, fmi, message )

            print("rx: ", beercan)

        return beercan


