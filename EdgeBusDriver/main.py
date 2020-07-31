from machine import Pin
import utime
from pyb import CAN

can = CAN(1, CAN.NORMAL)
can.setfilter(0, CAN.LIST16, 0, (123, 124, 125, 126))  # set a filter to receive messages with id=123, 124, 125 and 126


val = 0 #Value for built in LED
led = Pin("D13", Pin.OUT)


#Send a CAN Message
def CAN(): 
    print("sending message")
    can.send('Message', 123)

def getMess():
    if(can.any(0)):
        print("message recieved")
        mess = can.recv(0)
        print(mess[3])
        global val
        if(val ==0):
            val = 1
            led.value(val)
        else:
            val = 0
            led.value(val)
        
        
    else:
        print("no message")
        utime.sleep_ms(100)

while True:    
    getMess()
    utime.sleep_ms(500)

    
    
    
    
    
    
    
