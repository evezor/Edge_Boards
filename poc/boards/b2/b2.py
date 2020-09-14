import machine
import os
import pyb

from driver import Driver

class B2(Driver):

    def halt(self):
        machine.reset()

    def mkfs(self):
        flash = pyb.Flash()
        os.umount('/flash')
        os.VfsFat(flash)
        os.mount(flash, '/flash')

