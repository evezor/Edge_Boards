# driver.py
# abstract driver class, real boards make it real.

import machine
import os
import pyb

from pyb import Pin, Timer

class Driver:

    parameters = {}

    pins = {}

    def setup_pins(self):

        for parameter in self.parameters.values():

            if parameter['type'] == "boolean":
                self.pins[parameter['name']] = \
                    Pin(parameter['pin'], Pin.IN, Pin.PULL_UP)

            elif parameter['type'] == "adc":
                self.pins[parameter['name']] = \
                    pyb.ADC(parameter['pin'])

            elif parameter['type'] == "int":
                pin = Pin(parameter['pin'], Pin.OUT)
                self.pins[parameter['name']] = pin

            elif parameter['type'] == "pwm":
                pin = Pin(parameter['pin'], Pin.OUT)
                tim = Timer(3, freq=1000)
                self.pins[parameter['name']] = \
                        tim.channel(2, Timer.PWM, pin=pin )

            elif parameter['type'] == "neo":
                pin = Pin(parameter['pin'], Pin.OUT)
                self.pins[parameter['name']] = pin


    def init(self):
        self.setup_pins()
        self.wake_up_can()


    # Inputs
    # Iris has 3 steps: read, act, save:

    # Read hardware, set parameter

    def read_states(self):
        # read values from hardware, save to parameter table

        for key in self.parameters:
            parameter = self.parameters[key]

            """
            "name": "JOY_SW",
            "type": "button",
            "pin": "E0",
            """

            if parameter['type'] == "boolean":
                parameter['new'] = \
                    self.pins[parameter['name']].value()
                # print( parameter['new'] )

            elif parameter['type'] == "adc":
                parameter['new'] = \
                    self.pins[parameter['name']].read()

        return None

    # part 2: Act
    # Maybe Iris will check if an input has changed
    # Iris will call some other function that will likely call these

    def button_ck(self, name ):
        # did the button change
        # (or is the old value None, like on startup)

        parameter = self.parameters[name]

        if parameter['old'] is None:
            return parameter['new']

        if parameter['old'] != parameter['new']:
            return parameter['new']
        else:
            return None

    def adc(self, name ):
        # did the analog value change beyond the noise threashold
        # (or is the old value None, like on startup)

        parameter = self.parameters[name]

        if parameter['old'] is None:
            return parameter['new']

        if abs(parameter['old'] - parameter['new']) >= parameter['noise']:
            return parameter['new']
        else:
            # hack: reset new back to old so slow change doesn't creap noise
            # this makes me think we need a dirty bit
            # so we can control when old gets updated.
            parameter['new'] = parameter['old']
            return None

    # wrap up read,act,save:
    def save_states(self):

        for key in self.parameters:
            parameter = self.parameters[key]

            if parameter['type'] in [ "boolean", "adc", "code"]:
                parameter = self.parameters[key]
                parameter['old'] = parameter['new']

    # outputs

    # Hardware gets set by setting a parameter value and dirty

    def set_states(self, name, value):
        # push new values to hardware

        for key in self.parameters:
            parameter =self.parameters[key]

            if parameter['dirty']:

                if parameter['type'] == "int":
                    self.pins[parameter[pin]].value(v)

                elif parameter['type'] == "pwm":
                    self.pins[parameter[pin]].pulse_width_percent(val)

                elif parameter['type'] == "neo":
                    pass

                parameter['dirty'] = False


    def led_set(self, name, value):
        # print( "#3",  name, self.pins[name], value )
        self.pins[name].value(value)


    def led_toggle(self, name):
        # flip value between 0 and 1
        value = 0 if self.parameters[name] else 1
        self.led_set( name, value)

    def led_dim(self, name, value):
        self.pins[name].pulse_width_percent(value)

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
        print("waking up can...")
        can_chip_pin = Pin("D6", Pin.OUT)
        can_chip_pin.value(0)


