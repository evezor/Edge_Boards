# b3b.py
# driver for b3b board. (b3 and piazo)

import time
import os
import pyb
import struct

# from machine import Pin
from pyb import Pin, Timer

from driver import Driver


BUTTON={
        0:"on",
        1:"off"
        }

class B3b(Driver):

    can_chip_pins = []
    led_pins = []
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
            pyb.ADC('A0'),
            pyb.ADC('A1'),
            ]

        # outputs:
        self.led_pins = [
            Pin("D5", Pin.OUT),
            Pin("D13", Pin.OUT),
            ]

        tim = Timer(3, freq=1000)
        self.ch = tim.channel(2, Timer.PWM, pin=self.led_pins[0])
        self.ch.pulse_width_percent(0)


    def wake_up_can(self):
        self.can_chip_pins[0].value(0)

    def init(self):
        self.setup_pins()
        self.wake_up_can()

    # inputs:

    def read_states(self):

        # button 0
        v = BUTTON[self.button_pins[0].value()]
        parameter = next(d for d in self.parameters if d["name"] == "button_0")
        parameter['new value'] = v

        # button 1
        v = BUTTON[self.button_pins[1].value()]
        parameter = next(d for d in self.parameters if d["name"] == "button_1")
        parameter['new value'] = v


        # pot:
        # 1 to 4096.. ish
        parameter = next(d for d in self.parameters if d["name"] == "pot_0")
        ov = parameter['old value']
        nv = self.adc_pins[0].read()
        if abs(ov - nv) > 10:
            parameter['new value'] = nv


        # piezo
        # 1 to 4096.. ish
        parameter = next(d for d in self.parameters if d["name"] == "piezo")
        ov = parameter['old value']
        nv = self.adc_pins[1].read()
        if abs(ov - nv) > 200:
            parameter['new value'] = nv


        return None


    def button_x_on(self, button_no):
        """ did the button change from off to on? """

        parameter_name = "button_{}".format(button_no)

        parameter = next(d for d in self.parameters if d["name"] == parameter_name)
        ov = parameter['old value']
        nv = parameter['new value']

        ret = self.truth_fairy(ov=="off" and nv=="on")

        return ret

    def button_x_off(self, button_no):
        """ did the button change from on to off? """

        parameter_name = "button_{}".format(button_no)

        parameter = next(d for d in self.parameters if d["name"] == parameter_name)
        ov = parameter['old value']
        nv = parameter['new value']

        ret = self.truth_fairy(ov=="on" and nv=="off")

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

        parameter = next(d for d in self.parameters if d["name"] == parameter_name)
        ov = parameter['old value']
        nv = parameter['new value']

        if ov != nv:
            ret = nv
        else:
            ret = None

        return ret


    # outputs:

    def led_oo(self, led_no, oo):
        # turn a led on or off

        v = 0 if oo == "off" else 1
        self.led_pins[led_no].value(v)

    def led_0_on(self):
        self.led_oo(0, "on")

    def led_0_off(self):
        self.led_oo(0, "off")

    def led_1_on(self):
        self.led_oo(1, "on")

    def led_1_off(self):
        self.led_oo(1, "off")

    def led_0_dim(self, val):
        self.ch.pulse_width_percent(val)


    def spew_piezo(self):

        self.init()

        q = []

        while True:

            pot = self.adc_pins[0].read()
            piezo = self.adc_pins[1].read()

            l = len(q)

            if l:
                s = sum(q)
                mn = min(q)
                mx = max(q)

                a = s/l
                d = piezo - a

                if self.button_pins[0].value():
                    print((d, a-mn, a-mx, ))
                else:
                    print((piezo, ))

            q.append(piezo)
            if l == 100:
                q.pop(0)

            time.sleep(pot/4096)


print( """
from b3b import B3b
b=B3b()
b.init()
b.spew_piezo()
""" )

