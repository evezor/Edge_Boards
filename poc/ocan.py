# ocan.py
# OshBus on Can

# parameter names of wrappers come from:
# https://docs.micropython.org/en/latest/library/pyb.CAN.html#pyb.CAN.info

import time
from collections import namedtuple

from pyb import CAN

import bits

channels = [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "NWK",
        "",
        "",
        "DEBUG",
        ]


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

    def send(self, channel_name, p2, p3, message):
        print("tx: ",channel_name, p2, p3, message)
        channel_num = channels.index(channel_name)
        msg_id = bits.pack(channel=channel_num, cid=p2, bonus=p3)
        ret = self._send(msg_id, message)
        return ret


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
        BeerCan = namedtuple('BeerCan', [
            "channel", "cid", "bonus",
            "rtr", "fmi", "data",
            ])

        ret = self._recieve(fifo, timeout)
        if ret is None:
            beercan = None
        else:
            can_id, rtr, fmi, data = ret
            r2 = bits.unpack(can_id)
            channel_name = channels[ r2['channel'] ]
            beercan = BeerCan( channel_name, r2['cid'], r2['bonus'],
                    rtr, fmi, data, )

        print("rx: ",beercan)
        return beercan


