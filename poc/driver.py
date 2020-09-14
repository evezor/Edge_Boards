# driver.py
# abstract driver class, real boards make it real.


class Driver:

    parameter_table = {}

    def init(self):
        pass

    def halt():
        pass

    def read_states(self):
        pass

    def save_states(self):
        for parameter_name in self.parameter_table:
            self.parameter_table[parameter_name]['old value'] = \
                self.parameter_table[parameter_name]['new value']
