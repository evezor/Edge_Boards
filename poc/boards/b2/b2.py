import machine
import os
import pyb

import time

from driver import Driver

class B2(Driver):

    end_time = None

    # inputs:

    def read_states(self):

        parameter_name = "timer"
        parameter = self.parameters[parameter_name]

        if self.end_time is None:
            parameter['new'] = "stop"

        elif time.time() >= self.end_time:
            parameter['new'] = "stop"
            self.end_time = None

    def timer_end(self):
        """ did the button change from running to stop? """

        parameter_name = "timer"
        parameter = self.parameters[parameter_name]

        ov = parameter['old']
        nv = parameter['new']

        ret = self.truth_fairy(ov=="running" and nv=="stop")

        return ret


    # outputs:

    def timer_start(self):

        parameter_name="cook time"
        parameter = self.parameters[parameter_name]
        self.end_time = time.time() + parameter['old']

        parameter_name="timer"
        parameter = self.parameters[parameter_name]

        parameter['new'] = "running"


if __name__ == '__main__':
    x = B2()
    x.read_states()


