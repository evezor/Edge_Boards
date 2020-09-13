# b3.py
# driver for b3 board.

import time
import os
import pyb

from machine import Pin

BUTTON={
        0:"on",
        1:"off"
        }

class B3:

    can_chip_pins = []

    light_pins = []

    button_count = 2
    button_pins = []
    button_states = []

    def setup_pins(self):

        # CANbus chip
        self.can_chip_pins = [
            Pin("D6", Pin.OUT),
            ]

        self.light_pins = [
            Pin("D5", Pin.OUT),
            Pin("D13", Pin.OUT),
            ]

        self.button_pins = [
            Pin("D11", Pin.IN, Pin.PULL_UP),
            Pin("D12", Pin.IN, Pin.PULL_UP),
            ]


    def setup_states(self):
        self.button_states = [ 1, 1 ]

    def wake_up_can(self):
        self.can_chip_pins[0].value(0)

    def init(self):
        self.setup_pins()
        self.setup_states()
        self.wake_up_can()

    def halt(self):
        print("halt.")
        while True:
            self.light_0_on()
            time.sleep(.1)
            self.light_0_off()
            time.sleep(.1)

    def mkfs(self):
        flash = pyb.Flash()
        os.umount('/flash')
        os.VfsFat(flash)
        os.mount(flash, '/flash')


    def light_oo(self, light_no, oo):
        # turn a light on or off

        v = 0 if oo == "off" else 1
        self.light_pins[light_no].value(v)

    def light_0_on(self):
        self.light_oo(0, "on")

    def light_0_off(self):
        self.light_oo(0, "off")

    def light_1_on(self):
        self.light_oo(1, "on")

    def light_1_off(self):
        self.light_oo(1, "off")

    def ck_buttons(self):
        # maybe not used

        changes = []
        for i in range(self.button_count):
            v = self.button_pins[i].value()
            if v != self.button_states[i]:
                changes.append( (i,v) )
                self.button_states[i] = v

        return changes

    def button_x_on(self, button_no):
        """ did the button change from off to on? """

        parameter_name = "button_{}".format(button_no+1)

        pv = self.parameter_table[parameter_name]['value']
        bv = BUTTON[self.button_pins[button_no].value()]

        ret = pv=="off" and bv=="on"
        if ret: print("#1", bv, ret)

        self.parameter_table[parameter_name]['value'] = bv

        return ret

    def button_x_off(self, button_no):
        """ did the button change from on to off? """

        parameter_name = "button_{}".format(button_no)

        pv = self.parameter_table[parameter_name]['value']
        bv = BUTTON[self.button_pins[button_no].value()]

        ret = pv=="on" and bv=="off"
        if ret: print("#2", bv, ret)

        self.parameter_table[parameter_name]['value'] = bv

        return ret

    def button_0_on(self):
        return self.button_x_on(0)

    def button_0_off(self):
        return self.button_x_off(0)

    def button_1_on(self):
        return self.button_x_on(1)

    def button_1_off(self):
        return self.button_x_off(1)


    def show_buttons(self):
        while True:
            print(
                self.button_pins[0].value(),
                self.button_pins[1].value()
                )

            self.light_pins[0].value(self.button_pins[0].value())
            self.light_pins[1].value(self.button_pins[1].value())




