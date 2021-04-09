from driver import Driver
from pyb import Pin

class Seven(Driver):

    font = {
'0': [1,1,1,1,1,1,0,0],
'1': [0,1,1,0,0,0,0,0],
'2': [1,1,0,1,1,0,1,0],
'3': [1,1,1,1,0,0,1,0],
'4': [0,1,1,0,0,1,1,0],
'5': [1,0,1,1,0,1,1,0],
'6': [1,0,1,1,1,1,1,0],
'7': [1,1,1,0,0,0,0,0],
'8': [1,1,1,1,1,1,1,0],
'9': [1,1,1,1,0,1,1,0],
' ': [0,0,0,0,0,0,0,0],
}
    x=0

    def setup_pins(self):

        self.parameters['digits_0']['DIGITS'] = ["A0", "A1", "A2", "A3"]
        self.parameters['digits_0']['SEGMENTS'] = ["E4", "E3", "D0", "D1", "E2", "E1", "A5", "A4"]
        self.parameters['digits_0']['digit'] = 0

        self.parameters['digits_1']['DIGITS'] = ["E13", "E14", "E15", "E17"]
        self.parameters['digits_1']['SEGMENTS'] = ["E11", "E10", "SD_DETECT", "E8", "E7", "E6", "E5", "E12"]
        self.parameters['digits_1']['digit'] = 0

        for parameter in self.parameters.values():
            for pin_label in parameter['DIGITS']:
                self.pins[pin_label] = Pin(pin_label, Pin.OUT)
            for pin_label in parameter['SEGMENTS']:
                self.pins[pin_label] = Pin(pin_label, Pin.OUT)

    # outputs

    def digits_0(self, value):
        self.parameters['digits_0']['value'] = int(value)


    def digits_1(self, value):
        self.parameters['digits_1']['value'] = int(value)

    # refreshs

    def one_p(self, parameter):
        # turn off current digit
        self.pins[parameter['DIGITS'][parameter['digit']]].value(1)

        # setup the next digit
        parameter['digit'] = (parameter['digit'] + 1 )% 4
        # digit = format( parameter['value'], "4")[parameter['digit']]
        digit = "{:4}".format(parameter['value'])[parameter['digit']]
        glif = self.font[digit]
        segments = parameter['SEGMENTS']
        for pin_label,value in zip(segments, glif):
            self.pins[pin_label].value(value)
        # turn on the new digit
        self.pins[parameter['DIGITS'][parameter['digit']]].value(0)

    def refresh(self):

        if not self.x:
            for parameter in self.parameters.values():
                self.one_p(parameter)

        self.x = ( self.x+1) % 40

