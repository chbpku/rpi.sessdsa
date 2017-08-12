from sakshat import SAKSHAT
from sakspins import SAKSPins as PINS
import RPi.GPIO as GPIO
import time
import pygame
from pygame.locals import *
from sys import exit
 
from random import *
from math import pi
SAKS = SAKSHAT()
def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24,GPIO.IN)
    
def detct():
        
    if GPIO.input(24) == True:
        print ("wow")
        ring()
        
        
        

global clock
global p
p=0
def ring():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.OUT)
    GPIO.output(12, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(12, GPIO.LOW)
    time.sleep(1)
    GPIO.output(12,GPIO.HIGH)
    SAKS.ledrow.off()
def tact_event_handler(pin,status):
    global a
    global m
    if pin == PINS.TACT_RIGHT and status == True:
        a=a+1    
    if pin == PINS.TACT_LEFT and status == True:
        m=m+1
    SAKS.digital_display.show('%02d%02d'%(m,a))

def dip_switch_status_changed_handler(status):
    global clock
    global p
    if status[1]:
        t2=1
        SAKS.ledrow.on()
        while t2<=24:
            time.sleep(1)
            t2=t2+1
            if t2==24:
                SAKS.ledrow.off_for_index(7)
            if t2==6:
                SAKS.ledrow.off_for_index(1)
            if t2==9:
                SAKS.ledrow.off_for_index(2)
            if t2==12:
                SAKS.ledrow.off_for_index(3)
            if t2==15:
                SAKS.ledrow.off_for_index(4)
            if t2==18:
                SAKS.ledrow.off_for_index(5)
            if t2==21:
                SAKS.ledrow.off_for_index(6)
            if t2==3:
                SAKS.ledrow.off_for_index(0) 
        ring()
        
        clock=clock+2
    if status[0]:
        p=1
    
if __name__ == "__main__":
    SAKS.ledrow.off()
    t=time.time()
    global a
    global m
    global clock
    a=0
    m=0
    clock=0
    SAKS.digital_display.show('%02d%02d'%(m,a))
    while clock<=2400:
        time.sleep(1)
        clock=clock+1
        init()
        detct()
        print(clock)
        if clock%600==0:
            SAKS.ledrow.on()
            ring()
            if clock!=1200:
                time.sleep(120)
            if clock==1200:
                time.sleep(600)
            SAKS.ledrow.on()
            ring()
        SAKS.dip_switch_status_changed_handler = dip_switch_status_changed_handler
        SAKS.tact_event_handler=tact_event_handler
        if p==1:
            time.sleep(120)
            ring()
            p=0
        pygame.init()
        screen = pygame.display.set_mode((640, 480), 0, 32)
        background_image_filename = 'tim3.jpg'
        background = pygame.image.load(background_image_filename).convert()
        screen.blit(background, (0,0))
        pygame.display.update()
        if clock==2400:
            de='GAME OVER'
            my_font2=pygame.font.SysFont(None,120)
            text_screen2=my_font2.render(de, True, (255, 0, 0))
            screen.blit(text_screen2, (50,200))
            pygame.display.update()
            time.sleep(10)
        points = []
        my_font=pygame.font.SysFont(None,50)
        my_font1=pygame.font.SysFont(None,350)
        screen.blit(background, (0,0))
        
        textstr='time:'+str(clock)
        s=str(m)+' '+':'+' '+str(a)
        text_screen=my_font.render(textstr, True, (255, 0, 0))
        text_screen1=my_font1.render(s, True, (255, 0, 0))
        screen.blit(text_screen, (0,0))
        screen.blit(text_screen1, (100,120))
        pygame.display.update()
    print("GAME OVER")
    SAKS.ledrow.on()
    ring()
    SAKS.ledrow.on()
    if m<a:
        SAKS.digital_display.show("0011")
        SAKS.ledrow.off_for_index(0)
        SAKS.ledrow.off_for_index(1)
        SAKS.ledrow.off_for_index(2)
        SAKS.ledrow.off_for_index(3)
        time.sleep(4)
    else:
        SAKS.digital_display.show("1100")
        SAKS.ledrow.off_for_index(4)
        SAKS.ledrow.off_for_index(5)
        SAKS.ledrow.off_for_index(6)
        SAKS.ledrow.off_for_index(7)
        time.sleep(4)
    GPIO.cleanup()
