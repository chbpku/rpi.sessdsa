#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main_littlegame.py
#
#  Copyright 2017  <pi@raspberrypi>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import RPi.GPIO as GPIO
import time
import random
from sakshat import SAKSHAT
import pygame
from pygame.locals import *
import sys
from sys import exit

music = pygame.mixer.music
SAKS = SAKSHAT()
ds = 6
shcp = 19
stcp = 13
di = 25
clk = 5

pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 250, 0)
yellow = (250, 250, 0)
purple = (200, 0, 200)  # the colors

rect1 = Rect(30, 40, 740, 740)
rect2 = Rect(860, 620, 160, 160)
rect3 = Rect(1040, 620, 160, 160)
rect4 = Rect(1220, 620, 160, 160)
rect5 = Rect(1040, 440, 160, 160)
rect6 = Rect(1200, 0, 200, 200)  # the rectangles

font1 = pygame.font.Font('./Downloads/font1.ttf', 400)  # the big font
font2 = pygame.font.Font('./Downloads/font1.ttf', 140)  # the small font

pic_correct = pygame.image.load('./Downloads/RIGHT.jpg')
pic_wrong = pygame.image.load('./Downloads/WRONG.jpg')


# about lights
def GPIO_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ds, GPIO.OUT)
    GPIO.setup(shcp, GPIO.OUT)
    GPIO.setup(stcp, GPIO.OUT)
    GPIO.setup(clk, GPIO.OUT)
    GPIO.setup(di, GPIO.OUT)
    GPIO.output(ds, GPIO.LOW)
    GPIO.output(shcp, GPIO.LOW)
    GPIO.output(stcp, GPIO.LOW)
    GPIO.output(clk, GPIO.LOW)
    GPIO.output(di, GPIO.LOW)


def writeBit(data):
    GPIO.output(ds, data)
    GPIO.output(shcp, GPIO.LOW)
    GPIO.output(shcp, GPIO.HIGH)


def writeByte(data):
    for i in range(0, 8):
        writeBit((data >> i) & 0x01)
    GPIO.output(stcp, GPIO.LOW)
    GPIO.output(stcp, GPIO.HIGH)


def light():
    GPIO_init()
    for j in range(2):
        for i in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]:
            writeByte(i)
            time.sleep(0.1)
    GPIO.cleanup()
    return 0


# number game
def play_begin():
    music.load('./Downloads/welcome.mp3')
    music.play()
    time.sleep(3.2)
    return


def play_choosemode():
    music.load('./Downloads/ChooseMode.mp3')
    music.play()
    return

def play_choosedifficulty():
    music.load('./Downloads/input_difficulty.mp3')
    music.play()
    return

def play_ready():
    music.load('./Downloads/ReadyGo.mp3')
    music.play()
    return

def play_whenwrong1():
    music.load('./Downloads/when_wrong1.mp3')
    music.play()
    time.sleep(2)
    return

def play_whenright1():
    music.load('./Downloads/when_right1.wav')
    music.play()
    light()
    return

def play_inputmin():
    music.load('./Downloads/input_min.mp3')
    music.play()
    return

def play_inputmid():
    music.load('./Downloads/input_mid.mp3')
    music.play()
    return

def play_inputmax():
    music.load('./Downloads/input_max.mp3')
    music.play()
    return

def play_congratulations():
    music.load('./Downloads/congratulations.mp3')
    music.play()
    time.sleep(1.6)
    return

def play_grade1():
    music.load('./Downloads/grade_dalao.mp3')
    music.play()
    time.sleep(3)
    return

def play_grade2():
    music.load('./Downloads/grade_son.mp3')
    music.play()
    time.sleep(3)
    return

def play_over():
    music.load('./Downloads/grade_fate.mp3')
    music.play()
    time.sleep(5)
    return

def play_grade4():
    music.load('./Downloads/grade_forgive.mp3')
    music.play()
    time.sleep(3)
    return

def play_grade5():
    music.load('./Downloads/grade_degenerate.mp3')
    music.play()
    time.sleep(4)
    return

def play_grade3():
    music.load('./Downloads/grade_smarter.mp3')
    music.play()
    time.sleep(2.1)
    return

def play_com(grade):
    if grade != 0:  # if right
        play_whenright1()
    else:  # when wrong
        play_whenwrong1()
    return

def getlistsize(difficulty):
    if difficulty < 5:
        return 3
    else:
        return 5

def showgrade_numbers(correct, tryanswer, lasttime, difficulty):  # get the grade of number game
    if int(tryanswer) == correct:  # if  correct
        ## play: congratulations
        if lasttime < (2 + difficulty / 3):
            grade = 100
        elif lasttime < (4 + difficulty / 3):
            grade = 100 - lasttime * 6
        elif lasttime < (6 + difficulty / 3):
            grade = 100 - lasttime * 6
        elif lasttime > (8 + difficulty / 3):
            grade = 10
        else:
            grade = 100 - lasttime * 10
    else:  # if wrong
        grade = 0
    if grade == 0:
        s = "00.00"
    else:
        s = "%2.2f" % grade
    GPIO_init()
    SAKS.digital_display.show(s)  # show the grade
    return grade

def show_numbers(numlist, listsize, sleeptime, difficulty):
    for i in range(listsize):  # show the numbers
        if difficulty < 4:
            num = random.randint(10, 99)
        elif difficulty < 7:
            num = random.randint(100, 999)
        else:
            num = random.randint(1000, 9999)  # the numbers are from 10 to 9999
        numlist.append(num)
        if num / 10 < 1:
            s = "###" + str(num)
        elif num / 100 < 1:  # the number is double-digit
            s = "##" + str(num)
        elif num / 1000 < 1:  # the num is 3-digit
            s = "#" + str(num)
        else:  # the num is 4-digit
            s = str(num)
        GPIO_init()
        SAKS.digital_display.show(s)
        time.sleep(sleeptime)
        SAKS.digital_display.show("####")
        time.sleep(0.08)
    SAKS.digital_display.show("####")  # end of the show time
    return numlist

def game_max(difficulty):  # remember and input the max number
    listsize = getlistsize(difficulty)
    numlist = []
    sleeptime = 1.5 - difficulty / 6
    numlist = show_numbers(numlist, listsize, sleeptime, difficulty)  # show the numbers
    maxnum = max(numlist)
    starttime = time.time()  # start the time keeping
    play_inputmax()  # play: please input the max number
    trynum = int(input())
    endtime = time.time()
    lasttime = endtime - starttime - 2
    grade = showgrade_numbers(maxnum, trynum, lasttime, difficulty)
    play_com(grade)
    return grade  # return the grade

def game_min(difficulty):  # remember and input the min number
    listsize = getlistsize(difficulty)
    numlist = []
    sleeptime = 1.5 - difficulty / 6
    numlist = show_numbers(numlist, listsize, sleeptime, difficulty)  # show the numbers
    minnum = min(numlist)
    starttime = time.time()  # start the time keeping
    play_inputmin()  # play: please input the min number
    trynum = int(input())
    endtime = time.time()
    lasttime = endtime - starttime
    grade = showgrade_numbers(minnum, trynum, lasttime, difficulty)
    play_com(grade)
    return grade  # return the grade

def game_mid(difficulty):  # remember and input the middle number
    listsize = getlistsize(difficulty)
    numlist = []
    sleeptime = 1.5 - difficulty / 6
    numlist = show_numbers(numlist, listsize, sleeptime, difficulty)  # show the numbers
    numlist.sort()  # sort the list and get the midnum
    midnum = numlist[(listsize - 1) // 2]
    starttime = time.time()  # start the time keeping
    play_inputmid()  # play: please input the max number
    trynum = int(input())
    endtime = time.time()
    lasttime = endtime - starttime
    grade = showgrade_numbers(midnum, trynum, lasttime, difficulty)
    play_com(grade)
    return grade  # return the grade

# color game
def show_colors(screen):
    pygame.draw.rect(screen, black, rect1, 1)
    pygame.draw.rect(screen, black, rect2, 1)
    pygame.draw.rect(screen, black, rect3, 1)
    pygame.draw.rect(screen, black, rect4, 1)
    pygame.draw.rect(screen, black, rect5, 1)  # draw the rectangles
    colordict = {'黑': black, '蓝': blue, '红': red, '绿': green, '黄': yellow, '紫': purple}
    colorlist = list(colordict.keys())
    word = random.choice(colorlist)  # choose a random color
    word1 = word
    while word1 == word:  # choose a different color as the word1
        word1 = random.choice(colorlist)
    words = [word] * 4
    correct = random.randint(0, 3)  # choose a random position as the correct one
    for i in range(4):
        if i != correct:  # change the word which is not in the right position
            while words[i] == word or words[i] in words[:i]:
                words[i] = random.choice(colorlist)
    screen.blit(font1.render(word1, True, colordict[word]), (190, 180))  # write the big word
    screen.blit(font2.render(words[0], True, black), (870, 620))
    screen.blit(font2.render(words[1], True, black), (1050, 620))
    screen.blit(font2.render(words[2], True, black), (1230, 620))
    screen.blit(font2.render(words[3], True, black), (1050, 440))  # write the small words
    return correct

def showgrade_color(right, wrong, screen):
    grade = 100
    if right + wrong == 0:
        grade = 0
    else:
        grade -= 25 - (right + wrong) * 2
        grade = grade * right / (right + wrong)
    if grade > 100:
        grade = 100
    screen.fill(white)
    screen.blit(font1.render('%.2f' % grade, True, black), (240, 220))  # show the grade
    pygame.display.update()
    if grade > 90:  # if the grade is great
        play_grade1()
    elif grade > 75:
        play_grade2()
    elif grade > 60:
        play_grade3()
    elif grade > 40:
        play_grade4()
    else:
        play_grade5()
    time.sleep(2)
    return grade

# the main game
def main():
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0)  # set the volume
    play_begin()
    play_choosemode()  # play: please select a kind of game mode, 1: numbers, 2: colors
    chosenmode = int(input())
    if chosenmode == 1:  # about numbers
        play_choosedifficulty()  # play: pleade select a kind of difficulty
        difficulty = int(input())
        die = 0
        level = 0
        gradesum = 0
        while level < 5:  # continue the game
            play_ready()  # play: are you ready
            input()
            mode = random.randint(0, 2)
            if mode == 0:
                grade = game_min(difficulty)
            elif mode == 1:
                grade = game_mid(difficulty)
            else:
                grade = game_max(difficulty)
            gradesum += grade
            if grade == 0:  # if wrong
                die += 1
            if die == 2:
                play_over()
                break
            level += 1
        if grade != 0:  # if pass
            play_congratulations()
        fingrade = gradesum / 5
        s = "%2.2f" % fingrade
        GPIO_init()
        SAKS.digital_display.show(s)
        if fingrade > 90:  # if the grade is great
            play_grade1()
        elif fingrade > 75:
            play_grade2()
        elif fingrade > 60:
            play_grade3()
        elif fingrade > 40:
            play_grade4()
        else:
            play_grade5()
        SAKS.digital_display.show('####')

    else:  # about color
        play_ready()  # play: are you ready
        input()
        screen = pygame.display.set_mode()
        pygame.display.set_caption('Chose The Right color !')  # write the title
        time_font = pygame.font.SysFont('arial', 50)
        time_surface = screen.subsurface(rect6)  # the small rectangle to show the time
        screen.fill(white)
        correct = show_colors(screen)
        answerright = 0
        answerwrong = 0
        t = 10
        clock = pygame.time.Clock()
        while t > 0:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                    return
                elif event.type == KEYDOWN:
                    right = False
                    if event.key == K_LEFT and correct == 0:
                        right = True
                    elif event.key == K_DOWN and correct == 1:
                        right = True
                    elif event.key == K_RIGHT and correct == 2:
                        right = True
                    elif event.key == K_UP and correct == 3:
                        right = True
                    if right:  # if right
                        pygame.mixer.music.load('./Downloads/when_right2.mp3')
                        pygame.mixer.music.play()
                        screen.fill(white)
                        screen.blit(pic_correct, (500, 240))  # show the picture
                        pygame.display.update()
                        time.sleep(0.4)
                        answerright += 1
                    else:  # if wrong
                        pygame.mixer.music.load('./Downloads/when_wrong2.mp3')
                        pygame.mixer.music.play()
                        screen.fill(white)
                        screen.blit(pic_wrong, (500, 240))  # show the picture
                        pygame.display.update()
                        time.sleep(0.4)
                        answerwrong += 1
                    screen.fill(white)
                    correct = show_colors(screen)
            time_passed = clock.tick()
            t -= time_passed / 1000
            time_surface.fill(white)
            time_surface.blit(time_font.render(str(int(t)), True, black), (10, 10))  # show the left time
            pygame.display.update()
        screen.fill(white)
        showgrade_color(answerright, answerwrong, screen)  # show the final grade
        time.sleep(2)
        exit()
    return 0


if __name__ == '__main__':
    main()