
import machine
from machine import Pin

def wake_up():
    p = Pin("D6", Pin.OUT)
    p.value(0)

