# driver.py
# abstract driver class, real boards make it real.

import machine
import os
import pyb

from pyb import Pin, Timer

class Driver:

    parameters = []

    button_pins = []
    led_pins = []

    # stops:

    def halt(self):
        print("halt.")
        while True:
            self.led_0_on()
            time.sleep(.1)
            self.led_0_off()
            time.sleep(.1)

    def soft_reset(self):
        machine.soft_reset()

    # dangers:

    def mkfs(self):
        flash = pyb.Flash()
        flash = pyb.Flash(start=0)
        os.umount('/flash')
        os.VfsFat(flash)
        os.mount(flash, '/flash')
        # print( os.listdir() )
        # for  CP: storage.erase_filesystem()

    # Handy things:

    def truth_fairy(self, v):
        # smash True/False into True/None
        ret = v if v else None
        return ret

    # Board things

    def wake_up_can(self):
        can_chip_pin = Pin("D6", Pin.OUT)
        can_chip_pin.value(0)

    def init(self):
        pass

    # Iris things
    def read_states(self):
        pass

    def save_states(self):
        for parameter in self.parameters:
            parameter['old value'] =  parameter['new value']
