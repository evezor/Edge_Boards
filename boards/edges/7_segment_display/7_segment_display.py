from driver import Driver

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

    def setup_pins(self):

        parameters[0]['DIGITS'] = ["A0", "A1", "A2", "A3"]
        parameters[0]['SEGMENTS'] = ["E4", "E3", "D0", "D1", "E2", "E1", "A5", "A4"]
        parameters[0]['digit'] = 0

        parameters[1]['DIGITS'] = ["E13", "E14", "E15", "E17"]
        parameters[1]['SEGMENTS'] = ["E11", "E10", "SD_DETECT", "E8", "E7", "E6", "E5", "E12"]
        parameters[1]['digit'] = 0

        for parameter in parameters:
            for pin_label in parameter['DIGITS']:
                pins[pin_lable] = Pin(pin_label, Pin.OUT)
            for pin_label in parameter['SEGMENTS']:
                pins[pin_lable] = Pin(pin_label, Pin.OUT)

    # outputs

    def digits_0(self, value):
        parameters[0]['value'] = value


    def digits_1(self, value):
        parameters[1]['value'] = value

    # refreshs

    def one_p(self, parameter):
        # blank out current digit
        parameter['DIGITS'][parameter['digit']].value(0)

        # setup the next digit
        parameter['digit'] = (parameter['digit'] + 1 )% 4
        digit = format( parameter['value'], "4")[parameter['digit']]
        for segment,pin_label in map(
                font[digit],
                parameter['SEGMENTS']):
            pins[pin_label].value(segment)
        # turn on the new digit
        parameter['DIGITS'][parameter['digit']].value(0)

    def refresh(self):

        for parameter in parameters:
            one_p(parameter)


