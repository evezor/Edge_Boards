from machine import Pin
import utime
from pyb import CAN


#Evezor edge Bus driver basic implementation of Oshbus


#Prepare controller for initialization 

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



#Setup specific instance

ledVal = 0 #Value for built in LED
led = Pin("D13", Pin.OUT)



#Send a CAN Message
def CAN(channel): 
    print("sending message")
    can.send('Message', channel)

def getMessage():
    if(can.any(0)):
        print("FIFO 0")
        mess = can.recv(0)
        if(mess[0]<128):
            print("EMCY: " + str(mess))
        
        elif(mess[0]<256):
            print("EXP TX: " + str(mess))    
        
        elif(mess[0]<384):
            print("EXP RX: " + str(mess))    
        
        elif(mess[0]<512):
            print("CMD TX: " + str(mess))    
        
        elif(mess[0]<640):
            print("CMD RX: " + str(mess))    
        
        elif(mess[0]<768):
            print("EVENT TX: " + str(mess))    
        
        elif(mess[0]<896):
            print("EVENT RX: " + str(mess))    
        
        elif(mess[0]<1024):
            print("GPC1: " + str(mess))    
       
        elif(mess[0]<1152):
            print("GPC2: " + str(mess))    
        
        elif(mess[0]<1280):
            print("GPC3: " + str(mess))    
        
        elif(mess[0]<1408):
            print("GPC4: " + str(mess))    
        
        elif(mess[0]<1536):
            print("GPC5: " + str(mess))    
        
        elif(mess[0]<1664):
            print("GPC6: " + str(mess))    
        
        elif(mess[0]<1792):
            print("GPC7: " + str(mess))    
        
        elif(mess[0]<1920):
            print("HBT: " + str(mess))    
        
        else:
            print("DEBUG: " + str(mess))
    
    elif(can.any(1)):
        print("FIFO 1")
        mess = can.recv(1)
        if(mess[0]<128):
            print("EMCY: " + str(mess))
        
        elif(mess[0]<256):
            print("EXP TX: " + str(mess))    
        
        elif(mess[0]<384):
            print("EXP RX: " + str(mess))    
        
        elif(mess[0]<512):
            print("CMD TX: " + str(mess))    
        
        elif(mess[0]<640):
            print("CMD RX: " + str(mess))    
        
        elif(mess[0]<768):
            print("EVENT TX: " + str(mess))    
        
        elif(mess[0]<896):
            print("EVENT RX: " + str(mess))    
        
        elif(mess[0]<1024):
            print("GPC1: " + str(mess))    
       
        elif(mess[0]<1152):
            print("GPC2: " + str(mess))    
        
        elif(mess[0]<1280):
            print("GPC3: " + str(mess))    
        
        elif(mess[0]<1408):
            print("GPC4: " + str(mess))    
        
        elif(mess[0]<1536):
            print("GPC5: " + str(mess))    
        
        elif(mess[0]<1664):
            print("GPC6: " + str(mess))    
        
        elif(mess[0]<1792):
            print("GPC7: " + str(mess))    
        
        elif(mess[0]<1920):
            print("HBT: " + str(mess))    
        
        else:
            print("DEBUG: " + str(mess))
    
    else:
        print("no Messages")
