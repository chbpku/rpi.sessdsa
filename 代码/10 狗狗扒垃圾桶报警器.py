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
    GPIO.output(STCP, GPIO.HIGH)
    beep(0.2)
    

def alarm():
    global done
    done=False
    for i in [0x01,0x04,0x10,0x40,0x02,0x08,0x20,0x80]:  # 一组8个编码由一组二进制转换而成,分别对应8个LED点亮状态
        led_buzzer(i)
        time.sleep(0.2)
    done=True
    
def turn_off(channel):      #终止报警系统
    global key,done
    key = True      #对报警系统整体进行终止，该轮报警后不再连续报警
    #关闭LED最后的灯（不进行该操作最后的灯会一直亮）
    while done is False:        #在LED一轮结束后再进行关灯操作
        if done==True:
            break
        
    if done==True:
   
        for i in range(0, 8):
            writeBit(0x00 & 0x01)       #把0x00对应的8位存入寄存器，不代表任何灯
        GPIO.output(STCP, GPIO.LOW)
        GPIO.output(STCP, GPIO.HIGH)
    time.sleep(1)
  
    
def main():
    init()
    global  alarm_beep_times, key, count
    GPIO.add_event_detect(LKEY,GPIO.FALLING, callback=turn_off)
    while True:                             #持续监测下部红外线
        key = False
        count = 0
        alarm_beep_times = 0
        while GPIO.input(LIR_RCV) is 1:     #检测到下部的红外线受到遮挡
            count+=1
            
            if GPIO.input(HIR_RCV) is 0:    #未检测到上部红外线受遮挡--说明不是人！！开始计数
                count += 1
                print(count)
                print(GPIO.input(HIR_RCV))
                while alarm_beep_times < 4 and key is False and count > 80:     #计数达到80则开始执行报警程序
                    alarm()
                    alarm_beep_times += 1
            else:   #检测到上部红外线受阻--说明是人在倒垃圾
                count=0
main()



