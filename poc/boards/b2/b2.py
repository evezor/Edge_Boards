import machine
import os
import pyb

import time

from driver import Driver

class B2(Driver):

    end_time = None

    def halt(self):
        machine.reset()

    def mkfs(self):
        flash = pyb.Flash()
        os.umount('/flash')
        os.VfsFat(flash)
        os.mount(flash, '/flash')

    # inputs:

    def read_states(self):
        if self.end_time is not None:
            if time.time() >= self.end_time:
                self.parameter_table["timer"]['new value'] = "stop"
                self.end_time = None

    def timer_end(self):
        """ did the button change from running to stop? """

        parameter_name = "timer"

        ov = self.parameter_table[parameter_name]['old value']
        nv = self.parameter_table[parameter_name]['new value']

        ret = self.truth_fairy(ov=="running" and nv=="stop")

        return ret


    # outputs:

    def timer_start(self, message):
        print(self.parameter_table)
        self.end_time = time.time() + self.parameter_table["cook time"]['old value']
        self.parameter_table["timer"]['old value'] = "running"
        self.parameter_table["timer"]['new value'] = "running"


if __name__ == '__main__':
    x = B2()
    x.read_states()


