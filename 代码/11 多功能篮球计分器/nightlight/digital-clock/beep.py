import RPi.GPIO as GPIO
#from sakshat import SAKSHAT
import time
import os,sys
import signal

#SAKS = SAKSHAT()
GPIO.setmode(GPIO.BCM)      # BOARD编号方式，基于插座引脚编号
GPIO.setwarnings(False)                    
DS = 6
SHCP = 19
STCP = 13                   #LED灯
LKEY = 16
RKEY = 20                   #左右开关
BEEP = 12
LIR_RCV = 18                 #地上红外线
HIR_RCV = 17                #较高位置红外线


def init():
    #输出方式
    GPIO.setup(DS,GPIO.OUT)
    GPIO.setup(SHCP,GPIO.OUT)
    GPIO.setup(STCP,GPIO.OUT)       #led灯
    GPIO.setup(BEEP, GPIO.OUT, initial = GPIO.HIGH)       #蜂鸣器
    #输入方式
    GPIO.setup(LIR_RCV,GPIO.IN)
    GPIO.setup(HIR_RCV,GPIO.IN)    #红外线
    GPIO.setup(LKEY,GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(RKEY,GPIO.IN)       #开关,输入方式

def writeBit(data):
    GPIO.output(DS, data)
    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(SHCP, GPIO.HIGH)

def beep(seconds):                   #蜂鸣器状态
    GPIO.output(BEEP, GPIO.LOW)
    time.sleep(seconds)
    GPIO.output(BEEP, GPIO.HIGH)

def led_buzzer(data):
    for i in range(0, 8):
        writeBit((data >> i) & 0x01) #写入8位LED的状态
    GPIO.output(STCP, GPIO.LOW)
    beep(0.2)
    GPIO.output(STCP, GPIO.HIGH)

def alarm():
    for i in [0x01,0x04,0x10,0x40,0x02,0x08,0x20,0x80]:  # 一组8个编码由一组二进制转换而成,分别对应8个LED点亮状态
        led_buzzer(i)
        time.sleep(0.2)
    
def turn_off(channel):
    global key
    GPIO.output(BEEP, GPIO.HIGH)
    GPIO.output(DS,8& 0x01)
    GPIO.output(SHCP, GPIO.HIGH)
    #GPIO.output(STCP, GPIO.LOW)
    #for i in range(0, 8):
     #   writeBit((0x00 >> i) & 0x80)
    time.sleep(1)
    key = True
    
def main():
    init()
    global  alarm_beep_times, key, count
    GPIO.add_event_detect(LKEY,GPIO.FALLING, callback=turn_off)
    while True:
        key = False
        count = 0
        alarm_beep_times = 0
        while GPIO.input(LIR_RCV) is 1:
            if GPIO.input(HIR_RCV) is 0:
                count += 1
                print(count)
                print(GPIO.input(HIR_RCV))
                while alarm_beep_times < 4 and key is False and count > 80: 
                    alarm()
                    alarm_beep_times += 1
main()



