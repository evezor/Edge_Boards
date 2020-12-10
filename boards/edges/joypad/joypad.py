from driver import Driver

class Joypad(Driver):

    # buttons:

    def joy_sw(self):
        return self.button_ck( 'joy_sw' )

    def d_up(self):
        return self.button_ck( 'd_up' )

    def d_right(self):
        return self.button_ck( 'd_right' )

    def d_down(self):
        return self.button_ck( 'd_down' )

    def d_push(self):
        return self.button_ck( 'd_push' )

    def d_left(self):
        return self.button_ck( 'd_left' )

    def start(self):
        return self.button_ck( 'start' )

    def select(self):
        return self.button_ck( 'select' )

    def function(self):
        return self.button_ck( 'function' )

    def red_but(self):
        return self.button_ck( 'red_but' )

    def grn_but(self):
        return self.button_ck( 'grn_but' )

    def blu_but(self):
        return self.button_ck( 'blu_but' )

    def yel_but(self):
        return self.button_ck( 'yel_but' )

    # adcs:

    def joy_x(self):
        return self.adc( 'joy_x' )

    def joy_y(self):
        return self.adc( 'joy_y' )

    # leds:

    def red_but_led(self,value):
        return self.led_set( 'red_but_led', value )

    def grn_but_led(self,value):
        return self.led_set( 'grn_but_led', value )

    def blu_but_led(self,value):
        return self.led_set( 'blu_but_led', value )

    def yel_but_led(self,value):
        return self.led_set( 'yel_but_led', value )

    def hbt_led(self,value):
        return self.led_set( 'hbt_led', value )

    # pwms:

    def buzzer(self, value):
        return self.led_dim( 'buzzer', value )

    # neos:

    def neo_status(self, value):
        return self.neo_play( 'neo_status', value )

    def neo_strip(self, value):
        return self.neo_play( 'neo_strip', value )

