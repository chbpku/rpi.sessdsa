
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
# BOARD编号方式，基于插座引脚编号
GPIO.setmode(GPIO.BCM)
# 输出模式
GPIO.setup(12, GPIO.OUT)
t=0  
while t<=3:
    GPIO.output(12, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(12, GPIO.LOW)
    time.sleep(1)
    t=t+1
GPIO.cleanup()
