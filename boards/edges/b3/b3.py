from driver import Driver

class B3(Driver):

    # inputs

    def button0(self):
        return self.button_ck( 'button0' )

    def button1(self):
        return self.button_ck( 'button1' )

    def pot0(self):
        return self.adc( 'pot0' )

    # outputs

    def led0(self, value):
        return self.led_set( 'led0', value )

    def led1(self, value):
        return self.led_set( 'led1', value )


