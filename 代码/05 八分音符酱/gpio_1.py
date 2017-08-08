import RPi.GPIO as GPIO
from sakshat import SAKSHAT 
GPIO.setmode(GPIO.BCM)
DS = 6
SHCP = 19
STCP = 13

SAKS = SAKSHAT() 
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

def number(n):
    SAKS.digital_display.show("%04d" % n)
    
def light(n):
    init()
    #00000001,00000011,00000111,00001111,00011111,00111111,01111111,11111111
    lst = [0x00, 0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3F, 0x7F, 0xFF]
    writeByte(lst[n])

