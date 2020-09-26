import machine
import os
import pyb

import time

from driver import Driver

class B2(Driver):

    end_time = None

    # inputs:

    def read_states(self):
        if self.end_time is not None:
            if time.time() >= self.end_time:
                parameter = next(d for d in self.parameters if d["name"] == "timer")
                parameter['new value'] = "stop"
                self.end_time = None

    def timer_end(self):
        """ did the button change from running to stop? """

        parameter_name = "timer"

        parameter = next(d for d in self.parameters if d["name"] == parameter_name)
        ov = parameter['old value']
        nv = parameter['new value']

        ret = self.truth_fairy(ov=="running" and nv=="stop")

        return ret


    # outputs:

    def timer_start(self):

        parameter_name="cook time"
        parameter = next(d for d in self.parameters if d["name"] == parameter_name)
        self.end_time = time.time() + parameter['old value']

        parameter_name="timer"
        parameter = next(d for d in self.parameters if d["name"] == parameter_name)
        parameter['old value'] = "running"
        parameter['new value'] = "running"


if __name__ == '__main__':
    x = B2()
    x.read_states()


