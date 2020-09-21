# driver.py
# abstract driver class, real boards make it real.

import machine

class Driver:

    parameters = {}

    def truth_fairy(self, v):
        # smash True/False into True/None
        ret = v if v else None
        return ret

    def soft_reset(self):
        machine.soft_reset()

    def init(self):
        pass

    def halt():
        pass

    def read_states(self):
        pass

    def save_states(self):
        for parameter in self.parameters:
            parameter['old value'] =  parameter['new value']
