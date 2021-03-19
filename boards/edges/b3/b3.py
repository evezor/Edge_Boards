from driver import Driver

class B3(Driver):

    def button0(self):
        return self.button_ck( 'button0' )

    def button1(self):
        return self.button_ck( 'button1' )

    def pot_0(self):
        return self.adc( 'pot_0' )

    def led0(self, value):
        return self.led_set( 'led0', value )

    def led1(self, value):
        return self.led_set( 'led1', value )

    def led_1_off(self):
        return self.led_set( 'led_1', 0 )

    def led_1_toggle(self):
        return self.led_toggle( 'led_1' )

    def led_0_dim(self, value):
        return self.led_dim( 'led_0_dim', value )

