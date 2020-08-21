# ocan.py
# OshBus on Can

# parameter names of wrappers come from:
# https://docs.micropython.org/en/latest/library/pyb.CAN.html#pyb.CAN.info

from pyb import CAN

import bits

Class OCan():

    def __init__(self, bus=1):
        self.can = CAN(bus, mode=CAN.NORMAL, extframe=True)

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

    def send(self, can_id, message):

    def _set_filter(self, bank, mode, fifo, params, *, rtr):
        self.can.setfilter(bank, mode, fifo, params, rtr=rtr)


    def recieve(self):
        # TODO: maybe we don't want the "wait forever" feature here.

        r = None
        while r is None:
            try:
                r = self.can.recv(0)
            except OSError: # [Errno 110] ETIMEDOUT
                continue

        return r

        self.can.setfilter(0, CAN.MASK32, 0, (0,0) )
