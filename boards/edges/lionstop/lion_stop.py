from driver import Driver

from pyb import Pin

import utime

class Lion_Stop(Driver):

    # buttons:

    def limit_switch_0(self):
        return self.button_ck( 'limit_switch_0' )

    def limit_switch_1(self):
        return self.button_ck( 'limit_switch_1' )

    # param?

    def position_get(self):
        parameter = self.parameters['position']
        if parameter['dirty']:
            ret = parameter['value']
            parameter['dirty'] = False
        else:
            ret = None

        return ret

    # commands

    def home(self, value):
        if value:
            # move till limit switch flips
            self.parameters['home']['value'] = True

    def left(self, value):
        if value:
            self.parameters['left']['value'] = 0
        else:
            self.parameters['left']['value'] = 1


    # refreshs

    def enable(self):
        if  self.parameters['last_used']['value'] is None:
            self.heart_set(1)

            self.pins[self.parameters['enable']['pin']].value(0)
            # self.parameters['enable']['value'] = 0
            # self.parameters['enable']['dirty'] = True

            ret = False
        else:
            ret = True

        return ret


    def set_direction(self, direction):
        if self.parameters['direction']['value'] != direction:
            # self.parameters['direction']['value'] = direction
            # self.parameters['direction']['dierty'] = True
            self.pins[self.parameters['direction']['pin']].value(direction)


    def disable(self):
        self.parameters['last_used']['value'] = None
        self.pins[self.parameters['enable']['pin']].value(1)
        # self.parameters['enable']['value'] = 1
        # self.parameters['enable']['dirty'] = True
        self.heart_set(0)


    def step(self, direction, soft_stop=True):
        # returns True if moved

        # check for stops

        if direction == 0:

            step = -1

            if self.parameters['limit_switch_0']['new'] == 1:
                # 1 = hit the switch, so stop, no more moving
                ret = False
                print("limit_switch_0 is True (1)")
            else:
                ret = True

                if soft_stop:

                    if self.parameters['position']['value'] <= \
                            self.parameters['min_position']['value'] :
                        # hit the limit, so stop, no more moving
                        ret = False
                        print("position: {} <= min_position: {}".format(
                            self.parameters['position']['value'],
                            self.parameters['min_position']['value']))
        else:

            step = 1

            if self.parameters['limit_switch_1']['new'] == 1:
                ret = False
                print("limit_switch_1 is True (1)")
            else:
                ret = True

                if soft_stop:

                    if self.parameters['position']['value'] >= \
                            self.parameters['max_position']['value'] :
                        # hit the limit, so stop, no more moving
                        ret = False
                        print("position: {} >= max_position: {}".format(
                            self.parameters['position']['value'],
                            self.parameters['max_position']['value']))

        if ret:

            deadline = utime.ticks_add(
                    self.parameters['last_used']['value'],
                    self.parameters['move_delay']['value'])

            if utime.ticks_diff(deadline, utime.ticks_ms()) <= 0:

                self.enable()

                self.set_direction(direction)

                self.pins[self.parameters['step']['pin']].value(1)
                self.pins[self.parameters['step']['pin']].value(0)
                self.parameters['last_used']['value'] = utime.ticks_ms()
                self.parameters['position']['value'] += step
                self.parameters['position']['dirty']=True

                print( self.parameters['position']['value'] )

        return ret


    def move_home(self):
        ret = self.step(0, soft_stop=False)
        if ret is not None and not ret:
            print("homed")
            self.parameters['home']['value']=False
            self.parameters['position']['value']=0
            self.parameters['position']['dirty']=True

        return ret

    def move_left(self):
        ret = self.step(1)


    def ck_timeout(self):

        if  self.parameters['last_used']['value'] is None:
            # already off, nothing to do.
            ret = None

        else:

            deadline = utime.ticks_add(
                    self.parameters['last_used']['value'],
                    self.parameters['time_out']['value'])

            # print( "ck_timeout: {}".format(utime.ticks_diff(deadline, utime.ticks_ms())))

            if utime.ticks_diff(deadline, utime.ticks_ms()) > 0:
                ret = False
            else:
                self.disable()
                ret = True

        return ret



    def refresh(self):

        if self.parameters['home']['value']:
            self.move_home()

        if self.parameters['left']['value']:
            self.move_left()

        self.ck_timeout()


# import lion_stop; lion_stop.disable(); import machine; machine.soft_reset()
def disable():
    # from pyb import Pin
    Pin("A4", Pin.OUT).value(1)
    Pin("D13", Pin.OUT).value(0)
    print(" A4.set(1) disabled.")
    print("import machine; machine.soft_reset() ")

