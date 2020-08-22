# ocan.py
# OshBus on Can

# parameter names of wrappers come from:
# https://docs.micropython.org/en/latest/library/pyb.CAN.html#pyb.CAN.info

import time
from collections import namedtuple

from pyb import CAN

import bits

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

    def send(self, channel, p2, p3, message):
        msg_id = bits.pack(channel=channel, cid=p2, bonus=p3)
        ret = self._send(msg_id, message)
        return ret


    def _setfilter(self, fifo, params):
        # always 1, MASK32 I hope.
        self.can.setfilter(1, CAN.MASK32, fifo, params)


    def _recieve(self):
        # TODO: maybe we don't want the "wait forever" feature here.

        r = None
        while r is None:
            try:
                r = self.can.recv(0)
            except OSError: # [Errno 110] ETIMEDOUT
                continue

        return r

    def recieve(self):
        BeerCan = namedtuple('BeerCan', [
            "channel", "cid", "bonus",
            "rtr", "fmi", "data",
            ])

        can_id, rtr, fmi, data = self._recieve()
        r2 = bits.unpack(can_id)
        beercan = BeerCan(
                r2['channel'], r2['cid'], r2['bonus'],
                rtr, fmi, data, )

        return beercan


