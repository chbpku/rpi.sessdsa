import pygame
from pygame.locals import *
from sys import exit
 
from random import *
from math import pi
 
pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
points = []

screen.fill((255,255,255))
rc = (11,240,191)
rp = (100, 100)
rv =(200,300)
rs = (639-randint(rp[0], 639), 479-randint(rp[1], 479))
pygame.draw.rect(screen, rc, Rect(rp, rv),10)
r=(400,100)
rr=(200,300)
pos=(350,200)
po=(350,300)
pygame.draw.rect(screen, rc, Rect(r, rr),10)
pygame.draw.circle(screen, rc, pos, 10, 10)
pygame.draw.circle(screen, rc, po, 10, 10)

screen=pygame.display.set_mode([640,480])    
my_font=pygame.font.SysFont(None,22)
screen.fill([255,255,255])
textstr='location:'
text_screen=my_font.render(textstr, True, (255, 0, 0))
screen.blit(text_screen, (100,100))
pygame.display.update()
