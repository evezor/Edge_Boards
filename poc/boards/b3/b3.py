# b3.py
# driver for b3 board.

import time
import os
import pyb

# from machine import Pin
from pyb import Pin, Timer

from driver import Driver



BUTTON={
        0:"on",
        1:"off"
        }

class B3(Driver):

    can_chip_pins = []
    light_pins = []
    button_pins = []

    def setup_pins(self):

        # CANbus chip
        self.can_chip_pins = [
            Pin("D6", Pin.OUT),
            ]

        # inputs
        self.button_pins = [
            Pin("D11", Pin.IN, Pin.PULL_UP),
            Pin("D12", Pin.IN, Pin.PULL_UP),
            ]

        self.adc_pins = [
            pyb.ADC('A0')
            ]

        # outputs:
        self.light_pins = [
            Pin("D5", Pin.OUT),
            Pin("D13", Pin.OUT),
            ]

        # led5 = Pin('D5')
        # tim = Timer(3, freq=1000)
        # ch = tim.channel(2, Timer.PWM, pin=led5)

        # c13 = tim.channel(2, Timer.PWM, pin=d13)
        # ValueError: Pin(C1) doesn't have an af for Timer(3)

        tim = Timer(3, freq=1000)
        self.ch = tim.channel(2, Timer.PWM, pin=self.light_pins[0])
        self.ch.pulse_width_percent(5)


    def wake_up_can(self):
        self.can_chip_pins[0].value(0)

    def init(self):
        self.setup_pins()
        self.wake_up_can()

    # stops:

    def halt(self):
        print("halt.")
        while True:
            self.light_0_on()
            time.sleep(.1)
            self.light_0_off()
            time.sleep(.1)

    # dangers:

    def mkfs(self):
        flash = pyb.Flash()
        os.umount('/flash')
        os.VfsFat(flash)
        os.mount(flash, '/flash')


    # inputs:

    def read_states(self):
        v = BUTTON[self.button_pins[0].value()]
        self.parameter_table["button_0"]['new value'] = v

        v = BUTTON[self.button_pins[1].value()]
        self.parameter_table["button_1"]['new value'] = v

        # 1 to 4096.. ish
        v = self.adc_pins[0].read()
        self.parameter_table["pot_0"]['new value'] = v


    def button_x_on(self, button_no):
        """ did the button change from off to on? """

        parameter_name = "button_{}".format(button_no)

        ov = self.parameter_table[parameter_name]['old value']
        nv = self.parameter_table[parameter_name]['new value']

        ret = (ov=="off" and nv=="on")

        return ret

    def button_x_off(self, button_no):
        """ did the button change from on to off? """

        parameter_name = "button_{}".format(button_no)

        ov = self.parameter_table[parameter_name]['old value']
        nv = self.parameter_table[parameter_name]['new value']

        ret = (ov=="on" and nv=="off")

        return ret

    def button_0_on(self):
        return self.button_x_on(0)

    def button_0_off(self):
        return self.button_x_off(0)

    def button_1_on(self):
        return self.button_x_on(1)

    def button_1_off(self):
        return self.button_x_off(1)

    def pot_0(self):
        """ did the pot change more than.... 10? """

        parameter_name = "pot_0"

        ov = self.parameter_table[parameter_name]['old value']
        nv = self.parameter_table[parameter_name]['new value']

        ret = abs(ov - nv) > 10

        # print(ov,nv,ret)

        return ret


    # outputs:

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

    def led_0_dim(self):

        parameter_name = "pot_0"
        ov = self.parameter_table[parameter_name]['old value']

        v = 100 * ov/4096

        self.ch.pulse_width_percent(v)


