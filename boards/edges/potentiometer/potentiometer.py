from driver import Driver

class Potentiometer(Driver):

    # buttons:

    def a_button(self):
        return self.button_ck( 'a_button' )

    def b_button(self):
        return self.button_ck( 'b_button' )

    def function(self):
        return self.button_ck( 'function' )

    # adcs:

    def pot_a(self):
        return self.adc( 'pot_a' )

    def pot_b(self):
        return self.adc( 'pot_b' )

    # leds:

    def row_0(self,value):
        return self.led_set( 'row_0', value )

    def row_1(self,value):
        return self.led_set( 'row_1', value )

    def row_2(self,value):
        return self.led_set( 'row_2', value )

    def row_3(self,value):
        return self.led_set( 'row_3', value )

    def row_4(self,value):
        return self.led_set( 'row_4', value )

    def row_5(self,value):
        return self.led_set( 'row_5', value )

    def row_6(self,value):
        return self.led_set( 'row_6', value )

    def row_7(self,value):
        return self.led_set( 'row_7', value )

    def hbt_led(self,value):
        return self.led_set( 'hbt_led', value )

    # pwms:

    # neos:

    def NEO_STATUS(self, value):
        return self.neo_play( 'NEO_STATUS', value )

