from driver import Driver

class B3(Driver):

    def button_0_on(self):
        return self.button_ck( 'button_0', 0 )

    def button_0_off(self):
        return self.button_ck( 'button_0', 1 )

    def button_1_on(self):
        return self.button_ck( 'button_1', 0 )

    def button_1_off(self):
        return self.button_ck( 'button_1', 1 )

    def pot_0(self):
        return self.adc( 'pot_0' )

    def led_1_on(self):
        return self.led_set( 'led_1', 1 )

    def led_1_off(self):
        return self.led_set( 'led_1', 0 )

    def led_1_toggle(self):
        return self.led_toggle( 'led_1' )

    def led_0_dim(self, value):
        return self.led_dim( 'led_0_dim', value )

