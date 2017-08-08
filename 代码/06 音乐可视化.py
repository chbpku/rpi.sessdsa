import random
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)
GPIO.setup(40,GPIO.OUT)                            
GPIO.setup(37,GPIO.OUT)

adict = {1:22,2:36,3:37,4:11,5:12,6:40,7:1,8:1}

def beeep(seconds,PIN_NO):
	GPIO.output(PIN_NO,GPIO.HIGH)

def beep(seconds,PIN_NO):
	GPIO.output(PIN_NO,GPIO.HIGH)
	time.sleep(seconds)
	GPIO.output(PIN_NO,GPIO.LOW)
	time.sleep(seconds)

def beepall(seconds):
	for i in range(1,7):
		GPIO.output(adict[i],GPIO.HIGH)
	time.sleep(seconds)
	for i in range(1,7):
		GPIO.output(adict[i],GPIO.LOW)
	time.sleep(0.1)

def beepround(seconds):
	beeep(seconds,22)
	time.sleep(seconds)
	beeep(seconds,36)
	beeep(seconds,37)
	time.sleep(seconds)
	beeep(seconds,11)
	time.sleep(seconds)
	beeep(seconds,12)
	beeep(seconds,40)
	time.sleep(seconds)
def beepblingbling(seconds,num):
	beep(seconds,num)
	beep(seconds,num)
	beep(seconds,num)
def test():
	GPIO.output(PIN_NO,GPIO.LOW)
def hothothot(seconds):
	for i in range(1,7):
		GPIO.output(adict[i],GPIO.HIGH)
	time.sleep(seconds)
	for i in range(1,7):
		GPIO.output(adict[i],GPIO.LOW)
starttime=time.time()
while True:
	endtime=time.time()
	if endtime-starttime<6:
#	beepround(1)
#	beepall(0.1)
		beep(2,adict[random.randrange(1,7)])
		beepblingbling(0.2,22)
		hothothot(1)
	elif endtime-starttime>=6 and endtime-starttime<30:
		beep(1,adict[random.randrange(1,7)])
		beepblingbling(0.1,36)
		beepblingbling(0.2,40)
	elif endtime-starttime>=30 and endtime-starttime<40:
		beep(0.2,adict[random.randrange(1,7)])
		hothothot(2)
	else:
		beep(0.1,adict[random.randrange(1,7)])
		beepall(0.1)
		beep(0.1,adict[random.randrange(1,7)])
		beep(0.1,adict[random.randrange(1,7)])
		beep(0.1,adict[random.randrange(1,7)])
		beep(0.1,adict[random.randrange(1,7)])
		beep(0.1,adict[random.randrange(1,7)])
		for i in range(30):
			beep(0.1,adict[random.randrange(1,7)])
		beepblingbling(0.5,40)
		beep(0.1,adict[random.randrange(1,7)])
		hothothot(1.5)
		beepblingbling(0.2,36)
		for i in range(20):
			beep(0.1,adict[random.randrange(1,7)])
#	beep(0.125,11)
#	beep(0.125,22)
#	beep(0.125,12)
#	beep(0.125,40)
#	beep(0.125,37)
#
'''
while True:
	beep(1)
'''
'''
beep(0.2)
time.sleep(1.2)
beep(0.2)
time.sleep(1.2)
beep(0.2)
'''
'''
close()
time.sleep(2)
test()
'''
