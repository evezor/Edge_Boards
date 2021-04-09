from driver import Driver
from pyb import Pin

class Potentiometer(Driver):

    graph = [ "D0", "D1", "E2", "E1", "A5", "A4", "A3", "A2", ]

    graph_parameters = [ 'graph_a', 'graph_b']
    graph_current = 0
    x = 0

    def setup_pins(self):

        for parameter in self.parameters.values():

            if parameter['type'] == "graph":
                 self.pins[parameter['pin']] = \
                 Pin(parameter['pin'], Pin.OUT, Pin.PULL_DOWN)

        for pin_label in self.graph:
             self.pins[pin_label] = \
             Pin(pin_label, Pin.OUT)

        super().setup_pins()


    # buttons:

    def button_a(self):
        return self.button_ck( 'button_a' )

    def button_b(self):
        return self.button_ck( 'button_b' )

    # adcs:

    def pot_a(self):
        return self.adc( 'pot_a' )

    def pot_b(self):
        return self.adc( 'pot_b' )

    # led graphs:

    def graph_a(self,value):
        self.parameters['graph_a']['value'] = int(value)

    def graph_b(self,value):
        self.parameters['graph_b']['value'] = int(value)


    # refreshs

    def refresh(self):

        if not self.x:

            # turn off current graph

            parameter = self.parameters[self.graph_parameters[self.graph_current]]
            self.pins[parameter['pin']].value(1)

            # setup next graph
            self.graph_current = ( self.graph_current +1 ) % 2
            parameter = self.parameters[self.graph_parameters[self.graph_current]]

            for pin_label in self.graph[:parameter['value']]:
                 self.pins[pin_label].value(1)

            for pin_label in self.graph[parameter['value']:]:
                 self.pins[pin_label].value(0)

            # light it up
            self.pins[parameter['pin']].value(0)

        self.x = ( self.x+1) % 80

