import machine
import os
import pyb

class B2():

    def init(self):
        pass

    def halt(self):
        machine.reset()

    def mkfs(self):
        flash = pyb.Flash()
        os.umount('/flash')
        os.VfsFat(flash)
        os.mount(flash, '/flash')

