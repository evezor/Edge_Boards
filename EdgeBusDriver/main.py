from machine import Pin
import utime
from pyb import CAN
from machine import Pin

#Evezor edge Bus driver basic implementation of Oshbus
led1 = Pin("D6", Pin.OUT)
led1.low()

#Prepare controller for initialization 


#I'm hoping we can package bus driver functions neatly enough we can run it on slave devices
#For instance the hospital bed, during programming there's some other device that is driver and then tells the button board that it will take duties after initialization, then device[hospital bed] runs headless as there's no outside interactions needed after.
isBusDriver = True


#Set up CAN bus
can = CAN(1, CAN.NORMAL)

#Set filters 

#FIFO 0
can.setfilter(0, CAN.MASK16, 0, (0, 1920, 0, 2047)) #Receive all EMCY messages and [none] 
can.setfilter(1, CAN.MASK16, 0, (128, 1920, 256, 1920)) #EXP TX and RX

#FIFO 1

can.setfilter(2, CAN.MASK16, 1, (384, 1920, 512, 1920))  #CMD TX and RX
can.setfilter(3, CAN.MASK16, 1, (640, 1920, 768, 1920))  #EVENT TX and RX
can.setfilter(4, CAN.MASK16, 1, (896, 1920, 1024, 1920))  #GPC1 and GPC2
can.setfilter(5, CAN.MASK16, 1, (1152, 1920, 1280, 1920))  #GPC3 and GPC4
can.setfilter(6, CAN.MASK16, 1, (1408, 1920, 1536, 1920))  #GPC5 and GPC6
can.setfilter(7, CAN.MASK16, 1, (1664, 1920, 1792, 1920))  #GPC7 and HBT
can.setfilter(8, CAN.MASK16, 1, (1920, 1920, 2047, 2047))  #Debug and [none]

#list filter list for Node devices
# can.setfilter(1, CANLIST16, 1, (384+thisID, 255, 383, 511)) #This CMD channel and Public Access List
# can.setfilter(2, CANLIST16, 1, (639, 767, 895, 1023))       #Public Access List cont'd
# can.setfilter(3, CANLIST16, 1, (1151, 1279, 1407, 1535))    #Public Access List cont'd
# can.setfilter(2, CANLIST16, 1, (1663, 1791, 1919, 2046))    #Public Access List cont'd



channelName = ["EMCY", "EXP TX", "EXP RX", "CMD TX", "CMD RX", "EVENT TX", "EVENT RX", "GPC1", "GPC2", "GPC3", "GPC4", "GPC5", "GPC6", "GPC7", "HBT", "DEBUG"]

#Setup specific instance

ledVal = 0 #Value for built in LED
led = Pin("D13", Pin.OUT)


#Send a CAN Message
def CAN(chan, devID, mess): 
    print("sending message: chan: " + str(chan) + " devID: " + str(devID) + " mess: " + str(mess))
    arbID = chan*128 + devID
    can.send(mess, arbID)

    
def fifo0():
    if(can.any(0)):
        mess = can.recv(0)
        parseMessage(mess)
    else:
        pass


def fifo1():
    if(can.any(1)):
        mess = can.recv(1)
        parseMessage(mess)
    else:
        pass


def parseMessage(mess):
    devID = mess[0]%128
    chan = mess[0]//128
    print(channelName[chan] + " deviceID: " + str(devID) + " payload: " + str(mess[3]))
    if(chan == 3 and devID == 1 and mess[3] == b'0'):
        print("soft_reboot")
        machine.soft_reset()
    

    #Execute any running services        
def runServices():
    if(isBusDriver):#do bus driver high priority tasks
        pass
    
    #do this devices tasks
    
    if(isBusDriver): #do low priority bus driver tasks
        heartbeats()
    pass


#Check heartbeats for timeout overruns    
def heartbeats():
    pass

def main():
    fifo0()
    fifo1()
    runServices()

print("Device Startup FEATHER3")
while(True):
    main()
