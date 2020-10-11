# board2.py
# random stuff to run on the other board

import json
import machine
import time
import struct

from ocan import *
from board import Board

class Edge(Board):

    map_version = None
    can_id = None

    inputs = []
    outputs = []

    heart = None

    pause = True

    def boot(self):

        print("booting...")

        # >>> binascii.unhexlify('ff0000ff')
        # b'\xff\x00\x00\xff'
        # mac = b'\xff\x00\x00\xff'
        mac = bytes(list(machine.unique_id())[::2])

        try:

            print( "trying to restore state...")

            state = json.load(open('state.json'))

            self.map_version = state['map_version']
            self.can_id = state['can_id']

            self.inputs = state['inputs']
            self.outputs = state['outputs']

            self.driver.parameters = state['parameters']

            self.pause = False

            print("state loaded. ver: {}  can_id: {}".format(
                self.map_version, self.can_id) )

        except Exception as e:
            print("restore state failed:", e)

        # hello zorg, I am here
        self.ocan.send("NWK", BOARD_NO_ID, "BOARD_IAM", b'iam bord')

        if self.can_id is None:

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

            # Zorg awake, tell zorg mac:
            self.ocan.send("NWK", BOARD_NO_ID, "BOARD_DISCOVER", mac )

            # wait for Zorg to assign a can_id
            while self.can_id is None:
                beer = self.ocan.recieve(0, timeout=1000)
                if beer is None:
                    continue

                if beer.channel=='NWK' \
                    and beer.header == "ZORG_OFFER" \
                    and beer.message == mac:
                        self.can_id = beer.can_id
                        break

        else:
            self.ocan.send("NWK", self.can_id, "VERSION",
                    bytes([self.map_version]))

        print("booted! can_id:{}".format(self.can_id))

    def heartbeat(self):
        if self.heart is not None:
            if self.heart['time'] <= time.time():
                beer = self.ocan.send( "NWK", self.can_id, header="HEARTBEAT" )
                self.heart['time'] = time.time() + self.heart['rate']

    def drink_beer(self, beer=None):

        def nwk(beer):

            if beer.header=='PAUSE':
                self.pause = True

            elif beer.header=='CLEAR_MAPS':
                self.inputs=[]
                self.outputs=[]

            elif beer.header=='VERSION':
                self.map_version = list(beer.message)[0]

            elif beer.header=='SET_INPUT':
                l = list(beer.message)
                channel, function_no = l[:2]
                function_name = self.manifest['inputs'][function_no]['name']
                input_ = {
                    'channel': channels[channel],
                    'function_name': function_name,
                    }
                if "range" in self.manifest['inputs'][function_no]:
                    l2 = struct.unpack( "BBHH", beer.message)
                    assert channel == l2[0]
                    assert function_no == l2[1]
                    input_["range"] = { 'low': l2[2], 'high': l2[3] }

                self.inputs.append(input_)

            elif beer.header=='SET_OUTPUT':

                # chan, src func, src board, dst func
                # and maybe range
                l = list(beer.message)
                channel, src_function_no, src_board, dst_function_no = l[:4]

                function_name = self.manifest['outputs'][dst_function_no]['name']

                output = {
                    'channel': channels[channel],
                    'source': {
                        'function_no': src_function_no,
                        'can_id': src_board
                        },
                    'function_name': function_name,
                    }

                if "range" in self.manifest['outputs'][dst_function_no]:
                    l2 = struct.unpack( "BBBBHH", beer.message)
                    output["range"] = { 'low': l2[4], 'high': l2[5] }

                self.outputs.append(output)

            elif beer.header=='HEART_RATE':
                self.heart = {
                        'rate': list(beer.message)[0],
                        'time': time.time(),
                        }

            elif beer.header=='SAVE_ME':
                if self.map_version is None:
                    raise
                sotwca = {
                        'map_version': self.map_version,
                        'can_id': self.can_id,
                        'inputs': self.inputs,
                        'outputs': self.outputs,
                        'parameters': self.driver.parameters,
                        }
                json.dump(sotwca, open('state.json', 'w'))

            elif beer.header=='SET_PARMA':
                parma_no, value = list(beer.message)
                parma_name = self.driver.parameters[parma_no]['name']
                self.driver.parameters[parma_name] = value

            elif beer.header=='RESUME':
                self.pause = False


        if beer is None:
            # if we don't have any beer, try to get some.
            beer = self.ocan.recieve(0)

        if beer is not None:

            if beer.channel == "FAULT":
                if beer.header == "HALT":
                    self.driver.halt()
                if beer.header == "SOFT_RESET":
                    self.driver.soft_reset()

            if beer.can_id == self.can_id:

                if beer.channel == "NWK":
                    nwk(beer)

            if not self.pause and beer.channel in ["FH", "FM", "FL"]:
                # BeerCan(channel='FM', can_id=2, header=0, ... message=b'')
                # see if this message should trigger any outputs
                # TODO: optimize this loop into a dict lookup
                # note: the same input can trigger many outputs.
                for output in self.outputs:
                    if  output['channel'] == beer.channel \
                            and output['source']['function_no'] == beer.header \
                            and output['source']['can_id'] == beer.can_id:

                        function_name = output['function_name']
                        function = getattr(self.driver, function_name)
                        if 'range' in output:

                            val, low_input, high_input = struct.unpack(
                                    "HHH", beer.message)
                            low_output = output['range']['low']
                            high_output = output['range']['high']

                            print( val, low_input, high_input,
                                    low_output, high_output)

                            # clamp values outside the range?
                            # val = max(low_input, min(val, high_input))

                            y = (high_output - low_output) / (high_input - low_input) *  (val - low_input) + low_output

                            print(y)

                            ret = function(y)
                        else:
                            ret = function()



    def check_inputs(self):
        for input_ in self.inputs:
            function_name = input_['function_name']
            function = getattr(self.driver, function_name)
            ret = function()
            if ret is not None:
                channel = input_['channel']
                function_no = [
                        d['name'] for d in self.manifest['inputs']].index(
                            function_name)

                if 'range' in input_:
                    low = input_['range']['low']
                    high = input_['range']['high']
                    message =  struct.pack("HHH", ret, low, high)
                    print("check_inputs #2", input_, ret)
                else:
                    message =  b''

                beer = self.ocan.send(
                        channel, self.can_id, header=function_no, message=message)

                # process local outputs:
                self.drink_beer( beer )

        return None


    def iris(self):

        while True:

            self.heartbeat()

            # check for messages
            self.drink_beer()

            # check for inputs
            if not self.pause:
                self.driver.read_states()
                self.check_inputs()
                self.driver.save_states()


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
