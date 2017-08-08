from sakshat import SAKSHAT

from sakspins import SAKSPins as PINS

SAKS = SAKSHAT()

global h

global m

h = 0

m = 0

def tact_event_handler():

    global h

    global m

    if SAKS.dip_switch.is_on[0] == True and SAKS.dip_switch.is_on[1]==True:

        h+=1

    if SAKS.dip_switch.is_on[0] == False and SAKS.dip_switch.is_on[1]==True:

        m+=1

    if SAKS.dip_switch.is_on[0] == True and SAKS.dip_switch.is_on[1] == False:

        h-=1

    if SAKS.dip_switch.is_on[0] == False and SAKS.dip_switch.is_on[1]==False:

        m-=1

    return None



if __name__ == "__main__":

    SAKS.digital_display.show(("%02d%02d" % (0, 0)))

    SAKS.tact_event_handler = tact_event_handler()

    SAKS.digital_display.show(("%02d%02d" % (h, m)))
