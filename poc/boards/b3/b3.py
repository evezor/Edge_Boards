
import machine
from machine import Pin

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

    def light_oo(self, light_no, oo):
        # turn a light on or off

        v = 0 if oo == "off" else 1
        self.light_pins[light_no].value(v)

    def light_1_on(self):
        self.light_oo(0, "on")

    def light_1_off(self):
        self.light_oo(0, "off")

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
        # did the button change from off to on?
        parameter_name = "button_{}".format(button_no+1)
        if self.parameter_table[parameter_name]['value'] == "on":
            # already on, can't be more on.
            ret = False
        else:
            # check for on:
            v = self.button_pins[button_no].value()
            if v == 0:
                self.parameter_table[parameter_name]['value'] = "on"
                # parameter_table["button_1"]['dirty'] = True
                ret = True
            else:
                # was off, still off.
                ret = False

        return ret

    def button_x_off(self, button_no):
        # did the button change from on to off?
        parameter_name = "button_{}".format(button_no+1)
        if self.parameter_table[parameter_name]['value'] == "off":
            # already off, can't be more off.
            ret = False
        else:
            # check for on:
            v = self.button_pins[button_no].value()
            if v == 1:
                self.parameter_table[parameter_name]['value'] = "off"
                # parameter_table["button_1"]['dirty'] = True
                ret = True
            else:
                # was off, still off.
                ret = False

        return ret

    def button_1_on(self):
        return self.button_x_on(0)

    def button_1_off(self):
        return self.button_x_off(0)

    def button_2_on(self):
        return self.button_x_on(1)

    def button_2_off(self):
        return self.button_x_off(1)


    def show_buttons(self):
        while True:
            print(
                self.button_pins[0].value(),
                self.button_pins[1].value()
                )

            self.light_pins[0].value(self.button_pins[0].value())
            self.light_pins[1].value(self.button_pins[1].value())




