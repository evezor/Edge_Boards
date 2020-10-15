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
            driver = self.manifest['driver']
            print("init_board driver:", driver)
            module = __import__(driver)
            print("init_board module:", module)

            driver = getattr( module, driver )
            self.driver = driver()

            # manifest parameters create 2 things:
            # 1. list of names in edge.parameters
            # 2. dict in driver.parameters

            for parameter in self.manifest['parameters']:
                self.parameters.append(parameter['name'])
                driver.parameters[parameter['name']] = parameter


            if "init" in self.manifest:
                init = self.manifest['init']
                print("init_board init:", init)
                init = getattr(self.driver,init)
                init()



    def boot(self):
        # Zorg just goes, Edge waits on Zorg
        pass

