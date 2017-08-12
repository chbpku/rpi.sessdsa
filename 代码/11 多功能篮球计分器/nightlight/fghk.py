
from sakshat import SAKSHAT
from sakspins import SAKSPins as PINS
import time
 

SAKS = SAKSHAT()
__light_status = False
a=0
b=0
def tact_event_handler(pin,status):
    global a
    global b
    

    if pin == PINS.TACT_RIGHT and status == True:
            
        a=a+1    
    if pin == PINS.TACT_LEFT and status == True:
        b=b+1
    SAKS.digital_display.show("%02d%d" %(b,a))
    
    
if __name__ == "__main__":
    
    global a
    global b
    a=0
    b=0
    SAKS.digital_display.show("%02d%d#" %(b,a))
    SAKS.tact_event_handler = tact_event_handler  
        
    input("Enter any keys to exit...")
