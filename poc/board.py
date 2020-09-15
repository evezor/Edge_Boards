# board.py
# abstract class for zorg and edge

import time

from ocan import *

class Board():

    can_id = None
    pause = True

    ocan = None

    def __init__(self, manifest):

        self.manifest = manifest

        self.ocan = OCan()
        self.init_board()
        self.init_filters()

        self.boot()

    def init_filters(self):
        self.ocan._setfilter(0, (0,0) )

    def init_board(self):
        # setup Edge hardware (driven by manifest and driver)
        if "driver" in self.manifest:
            module = __import__(self.manifest['driver'])
            print(module)
            driver = getattr( module, self.manifest['driver'] )()

            driver.parameter_table = self.manifest['parameters']
            for parameter_name in driver.parameter_table:
                driver.parameter_table[parameter_name]['new value'] = \
                    driver.parameter_table[parameter_name]['old value']

            print(driver)
            if "init" in self.manifest:
                init = getattr(driver,self.manifest['init'])
                print(init)
                init()

            self.driver = driver



    def boot(self):
        # Zorg just goes, Edge waits on Zorg
        pass

