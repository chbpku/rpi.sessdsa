from sakshat import SAKSHAT
import RPi.GPIO as GPIO
import time
import datetime
from sakspins import SAKSPins as PINS
import random

SAKS = SAKSHAT()

PIN_NO_BEEP = 12
PIN_NO_LED = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_NO_BEEP, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(PIN_NO_LED, GPIO.OUT, initial=GPIO.HIGH)
def beep(seconds):
    GPIO.output(PIN_NO_BEEP, GPIO.LOW)
    GPIO.output(PIN_NO_LED, GPIO.LOW)
    time.sleep(seconds)
    GPIO.output(PIN_NO_BEEP, GPIO.HIGH)
    GPIO.output(PIN_NO_LED, GPIO.HIGH)
def beepAction(secs, sleepsecs, times):
    for i in range(times):
        beep(secs)
        time.sleep(sleepsecs)

        
__dp = True
__alarm_beep_status = False
__alarm_beep_times = 0
__alarm_time = "17:01:10"
__firstalarm_time = '17:00:00'

a = 0
u = 7
count = 0
def tact_event_handler(pin, status):
    '''
    called while the status of tacts changed
    :param pin: pin number which stauts of tact is changed
    :param status: current status
    :return: void
    '''
    global __alarm_beep_status
    global __alarm_beep_times
    global count
    global u
    global a
    count = count + 1
    print(count)
    if pin == PINS.TACT_LEFT and status == True:
        a = 0*10**(u) + a
        u = u -1
    elif pin == PINS.TACT_LEFT and status == False:
        a = 0*10**(u) + a
        u = u -1
    elif pin == PINS.TACT_RIGHT and status == True:
        a = 1*10**(u) + a
        u = u -1
    elif pin == PINS.TACT_RIGHT and status == False:
        a = 1*10**(u) + a
        u = u -1
        
    if abc == int(a) and count == 8:
        __alarm_beep_status = False
        __alarm_beep_times = 0
        SAKS.buzzer.off()
        SAKS.ledrow.off_for_index(0)
        SAKS.ledrow.off_for_index(1)
        SAKS.ledrow.off_for_index(2)
        SAKS.ledrow.off_for_index(3)
        SAKS.ledrow.off_for_index(4)
        SAKS.ledrow.off_for_index(5)
        SAKS.ledrow.off_for_index(6)
        SAKS.ledrow.off_for_index(7)

DS = 6
SHCP = 19
STCP = 13

def init():
    GPIO.setup(DS, GPIO.OUT)
    GPIO.setup(SHCP, GPIO.OUT)
    GPIO.setup(STCP, GPIO.OUT)

    GPIO.output(DS, GPIO.LOW)
    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(STCP, GPIO.LOW)

def writeBit(data):
    GPIO.output(DS, data)
    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(SHCP, GPIO.HIGH)

def writeByte(data):
    for i in range (0, 8):
        writeBit((data >> i) & 0x01)
    GPIO.output(STCP, GPIO.LOW)
    GPIO.output(STCP, GPIO.HIGH)

if __name__ == "__main__":
    flag = 0
    abc = 0
    global abc
    flag = random.randint(1,4)
    if flag == 1:
        SAKS.digital_display.show("0000")
        abc = 0
    elif flag == 2:
        SAKS.digital_display.show("1100")
        abc = 11110000
    elif flag == 3:
        SAKS.digital_display.show("0011")
        abc = 1111
    elif flag == 4:
        SAKS.digital_display.show("1111")
        abc = 11111111
    print(abc)   
    SAKS.tact_event_handler = tact_event_handler
    
    SAKS.buzzer.off()
    SAKS.ledrow.off_for_index(0)
    SAKS.ledrow.off_for_index(1)
    SAKS.ledrow.off_for_index(2)
    SAKS.ledrow.off_for_index(3)
    SAKS.ledrow.off_for_index(4)
    SAKS.ledrow.off_for_index(5)
    SAKS.ledrow.off_for_index(6)
    SAKS.ledrow.off_for_index(7)
    judge = 1
    while True:
        print(abc)
        print(a)
        t = time.localtime()
        h = t.tm_hour
        m = t.tm_min
        s = t.tm_sec
        w = time.strftime('%w',t)
        print "%02d:%02d:%02d" % (h, m, s)
        if __alarm_beep_status == False:
            print False
        else:
            print True

        if ("%02d:%02d:%02d" % (h, m, s)) <= __alarm_time and ("%02d:%02d:%02d" % (h, m, s)) >= __firstalarm_time:
            for i in range(15):
                for j in range(8):
                    SAKS.ledrow.on_for_index(j)
                    if j == 0:
                        SAKS.ledrow.off_for_index(7)
                    else:
                        SAKS.ledrow.off_for_index(j-1)
                    time.sleep(3.0/(float(i)+1.0))
                if i > 8:
                    beepAction(0.05,0,i-7)
                print(i)
                print "%02d:%02d:%02d" % (h, m, s)
                t = time.localtime()
            
        
        if ("%02d:%02d:%02d" % (h, m, s)) >= __alarm_time and judge == 1:
            __alarm_beep_status = True
            __alarm_beep_times = 0
            judge = 0

        if __dp:
            if __alarm_beep_status:
                
                if flag == 1:
                    SAKS.digital_display.show("0000")
                elif flag == 2:
                    SAKS.digital_display.show("1100")
                elif flag == 3:
                    SAKS.digital_display.show("0011")
                elif flag == 4:
                    SAKS.digital_display.show("1111")
                print('go and half')

                SAKS.buzzer.on()
                SAKS.ledrow.on_for_index(0)
                SAKS.ledrow.on_for_index(1)
                SAKS.ledrow.on_for_index(2)
                SAKS.ledrow.on_for_index(3)
                SAKS.ledrow.on_for_index(4)
                SAKS.ledrow.on_for_index(5)
                SAKS.ledrow.on_for_index(6)
                SAKS.ledrow.on_for_index(7)
                __alarm_beep_times = __alarm_beep_times + 1
                if __alarm_beep_times > 30:
                    __alarm_beep_status = False
                    __alarm_beep_times = 0
            else:
                SAKS.digital_display.show(("%02d%02d." % (h, m)))
        else:
            if __alarm_beep_status:
                if flag == 1:
                    SAKS.digital_display.show("0000")
                elif flag == 2:
                    SAKS.digital_display.show("1100")
                elif flag == 3:
                    SAKS.digital_display.show("0011")
                elif flag == 4:
                    SAKS.digital_display.show("1111")
                SAKS.buzzer.off()
                SAKS.ledrow.off_for_index(0)
                SAKS.ledrow.off_for_index(1)
                SAKS.ledrow.off_for_index(2)
                SAKS.ledrow.off_for_index(3)
                SAKS.ledrow.off_for_index(4)
                SAKS.ledrow.off_for_index(5)
                SAKS.ledrow.off_for_index(6)
                SAKS.ledrow.off_for_index(7)
            else:
                SAKS.digital_display.show(("%02d%02d" % (h, m)))
        __dp = not __dp

        time.sleep(0.5)
    input("Enter any keys to exit...")
