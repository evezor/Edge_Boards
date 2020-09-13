# board2.py
# random stuff to run on the other board

import time

import machine

from ocan import *
from board import Board

class Edge(Board):

    inputs = []
    outputs = []
    parameter_table = {}

    heart_time = 0
    pause = True

    def boot(self):

        print("booting...")
        print("state 0")

        self.parameter_table.update(self.manifest['parameter_table'])

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
                and beer.message == mac:
                    can_id = beer.can_id
                    break

        print("booted! can_id:{}".format(can_id))
        self.can_id = can_id

    def heartbeat(self):
        if self.heart_time <= time.time():
            beer = self.ocan.send( "NWK", self.can_id, header="HEART_BEAT" )
            self.heart_time = time.time() + 1

    def drink_beer(self, beer=None):

        def nwk(beer):

            if beer.header=='SET_INPUT':
                channel, function_no = list(beer.message)
                x = {
                    'channel': channels[channel],
                    'function': self.manifest['inputs'][function_no]
                    }
                self.inputs.append(x)
                print(channel,function_no,x)

            elif beer.header=='SET_OUTPUT':
                # chan, src func, src board, dst func
                channel, src_function_no, src_board, dst_function_no = list(
                        beer.message)
                x = {
                    'channel': channels[channel],
                    'source': {
                        'function_no': src_function_no,
                        'can_id': src_board
                        },
                    'function_name': self.manifest['outputs'][dst_function_no]
                    }
                self.outputs.append(x)
                print(x)

            elif beer.header=='SET_PARMA':
                parma_no, value = list(beer.message)
                parma_name = list(self.parameter_table.keys())[parma_no]

            elif beer.header=='PAUSE':
                self.pause = True
            elif beer.header=='RESUME':
                self.pause = False


        if beer is None:
            # if we don't have any beer, try to get some.
            beer = self.ocan.recieve(0)

        if beer is not None:

            if beer.channel == "falt":
                self.driver.halt()

            if beer.can_id == self.can_id:

                if beer.channel == "NWK":
                    nwk(beer)

            if not self.pause and beer.channel in ["FH", "FM", "FL"]:
                # BeerCan(channel='FM', can_id=2, header=0, ... message=b'')
                # see if this message should trigger any outputs
                for output in self.outputs:
                    print(output)
                    if  output['channel'] == beer.channel \
                            and output['source']['function_no'] == beer.header \
                            and output['source']['can_id'] == beer.can_id:

                        function_name = output['function_name']
                        function = getattr(self.driver, function_name)
                        ret = function()


    def check_inputs(self):
        for inny in self.inputs:
            # print(inny)
            # {'channel': 'FM', 'function': 'button_1_on'}
            function_name = inny['function']
            function = getattr(self.driver, function_name)
            ret = function()
            print( function_name, self.parameter_table['button_1'] )
            if ret:
                # print( "{}: {}".format( function_name )
                channel = inny['channel']
                function_no = self.manifest['inputs'].index(function_name)
                message = bytes()
                beer = self.ocan.send(
                        channel, self.can_id, header=function_no, message=message)
                # incase there are local outputs:
                self.drink_beer( beer )

        return None


    def iris(self):

        while True:

            self.heartbeat()

            # check for messages
            self.drink_beer()

            # check for inputs
            if not self.pause:
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
