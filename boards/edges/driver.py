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

        self.pins["D13"] = Pin("D13", Pin.OUT) # HBT_LED
        self.pins["D5"] = Pin("D5", Pin.IN, Pin.PULL_UP) # FUNC_BUTTON

        for parameter in self.parameters.values():

            if parameter['type'] == "in":
                self.pins[parameter['pin']] = \
                    Pin(parameter['pin'], Pin.IN, Pin.PULL_UP)

            elif parameter['type'] == "adc":
                self.pins[parameter['pin']] = \
                    pyb.ADC(parameter['pin'])

            elif parameter['type'] == "out":
                pin = Pin(parameter['pin'], Pin.OUT)
                self.pins[parameter['pin']] = pin

            elif parameter['type'] == "pwm":
                pin = Pin(parameter['pin'], Pin.OUT)
                tim = Timer(3, freq=1000)
                self.pins[parameter['pin']] = \
                        tim.channel(2, Timer.PWM, pin=pin )

            elif parameter['type'] == "neo":
                pin = Pin(parameter['pin'], Pin.OUT)
                self.pins[parameter['pin']] = pin


    def init(self):
        self.setup_pins()
        self.read_states()
        self.set_states()
        self.wake_up_can()
        self.heart_set(1)


    # Inputs
    # Iris has 3 steps: read, act, save:

    # Read hardware, set parameter

    def read_states(self):
        # read values from hardware, save to parameter table

        for parameter in self.parameters.values():

            if parameter['type'] == "in":
                parameter['new'] = \
                    self.pins[parameter['pin']].value()
                # print( parameter['new'] )

            elif parameter['type'] == "adc":
                parameter['new'] = \
                    self.pins[parameter['pin']].read()

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

        for parameter in self.parameters.values():

            if parameter['type'] in [ "in", "adc", "code" ]:
                parameter['old'] = parameter['new']

    # outputs

    # Hardware gets set by setting a parameter value and dirty

    def set_states(self):
        # push new values to hardware

        for parameter in self.parameters.values():

            if parameter.get('dirty'):

                if parameter['type'] == "out":
                    self.pins[parameter['name']].value(parameter['value'])

                elif parameter['type'] == "pwm":
                    self.pins[parameter['name']].pulse_width_percent(val)

                elif parameter['type'] == "neo":
                    pass

                parameter['dirty'] = False


    def led_set(self, pin_label, value):
        # print( "#3",  name, self.pins[name], value )
        self.pins[pin_label].value(value)


    def led_toggle(self, pin_label):
        # flip value between 0 and 1
        wtf()
        value = 0 if self.parameters[name] else 1
        self.led_set( pin_label, value)

    def led_dim(self, pin_label, value):
        self.pins[pin_label].pulse_width_percent(value)

    # refresh
    # long running jobs that need more than just setting a pin.
    def refresh(self):
        return None

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

    def heart_set(self, value):
        return self.led_set("D13", value)

    def ck_func(self):
       return self.pins['D5'].value()
