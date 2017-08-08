# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import pyaudio
import struct
from DXK import *
#import gpio_1
import random
import time

map_list = ((0, 1, 1, 1, 1), (1, 0, 1, 0, 1), (1, 0, 0, 1, 1), (1, 0, 0, 0, 1),(0, 0, 0, 0, 1))
#随机地图块元组
screen_size = (800, 600)
#屏幕大小

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    #初始化界面
    
    font = pygame.font.SysFont("arial", 24)
    #显示文字的字体格式

    pa = pyaudio.PyAudio()
    SAMPLING_RATE = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
    NUM_SAMPLES = 4096
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=NUM_SAMPLES)
    #初始化声音输入
    score = 0
    score_max = 0

    with open("score.txt", "r") as f:
        lst = f.read().split()
        if len(lst) == 2:
            score_max = int(lst[1])
    start = False

    dxk = DXK("dxk1.png")
    block = Block("black.png")
    #角色和方块对象
    
    #游戏总循环
    while True:
        map_queue_1 = list()
        #当前地图方块队列
        map_queue_2 = list()
        #等待地图方块队列
        for i in range(9):
            map_queue_1.append([1, 1])
        for i in map_list[3]:
            map_queue_2.append([i, 1])
        #地图初始化

        h0 = screen_size[1]-dxk.height-block.height
        #地面高度
        h = h0
        block_s = 0.

        reset = False
        fall = False
    
        while not start:
            screen.fill((255, 255, 255))
            for i in range(9):
                if map_queue_1[i]!=0:
                    screen.blit(block.image, (i * 100. + block_s, block.y))
            screen.blit(dxk.image, (screen_size[0]/2-dxk.width/2, h))
            screen.blit(font.render("Please speak loudly to start!", True, (0,0,0)),(260,100))
            string_audio_data = stream.read(NUM_SAMPLES)
            k = max(struct.unpack('%dh'%(NUM_SAMPLES,), string_audio_data))
            #gpio_1.light(k*8//32767)
            if k*8//32767 == 8:
                start = True
            pygame.display.update()
        stream.close()    
        clock = pygame.time.Clock()
        stop = False


        while True:
            #当前游戏循环
            for event in pygame.event.get():
                #事件处理
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == 285 and event.mod == 256:
                        exit()
                    if event.key == K_r:
                        reset = True
            #按R键重新开始游戏
            if reset:
                break
           
            screen.fill((255, 255, 255))
            screen.blit(dxk.image, (screen_size[0]/2-dxk.width/2, h))
            for i in range(9):
                if map_queue_1[i][0]!=0:
                    screen.blit(block.image, (i * 100. + block_s, screen_size[1]-block.height))
            #绘制背景、角色和地图方块

            screen.blit(font.render("Score: %d"%score, True, (0,0,0)),(0, 0))
            screen.blit(font.render("Maxscore: %d"%score_max, True, (0,0,0)),(0, 20))
            #绘制分数信息

            stream = pa.open(format=pyaudio.paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=NUM_SAMPLES)
            string_audio_data = stream.read(NUM_SAMPLES)
            k = max(struct.unpack('%dh' % (NUM_SAMPLES,), string_audio_data))
            stream.close()
            light_num = k*8//32767
            #声音输入
            #gpio_1.light(light_num)
            #GPIO显示音量大小
            
                        
            if k <= 1500:
                dxk.stop()
            elif not stop:
                dxk.move()
                if not fall and k > 8000:
                    dxk.jump(2.5)
                    if k > 20000:
                        dxk.fly()
                        
            time_passed = clock.tick()
            time_passed_seconds = time_passed / 1000.0
            t = time_passed_seconds * 100
            if not dxk.can_jump and not fall:
                h -= dxk.speed_y * t
                dxk.speed_y -= dxk.g * t
                if h >= h0:
                    dxk.land()
                    dxk.can_jump = True
                    h = h0
            block_s += dxk.speed_x * t
            #实现角色移动
            
            if fall:
                if map_queue_1[5][0]==1 and block_s <= -78:
                    dxk.stop()
                    stop = True
                dxk.speed_y = -2.5
                if h < 600-53:
                    h -= dxk.speed_y * t
                else:
                    dxk.stop()
                    break
            #实现角色掉落
            if map_queue_1[3][0] == 0 and map_queue_1[3][1]:
                score += 1
                if score>score_max:
                    score_max = score
                map_queue_1[3][1] = 0
            f = open("score.txt", 'w')
            f.write("%d %d"%(score, score_max))
            f.close()
            #实现记录分数，用文件输出

            if h >= h0:
                if map_queue_1[4][0]==0: 
                    if block_s < -22 and block_s > -78:
                        fall = True
                    elif map_queue_1[5][0]==0 and block_s <=-78:
                        fall = True
                    elif map_queue_1[3][0]==0 and block_s > -22:
                        fall = True
            #掉落判断
            

            if block_s <= -100.:
                map_queue_1.pop(0)
                map_queue_1.append(map_queue_2.pop(0))
                block_s += 100.
            while len(map_queue_2) < 2:
                rand = random.randrange(10) % 5
                for i in map_list[rand]:
                    map_queue_2.append([i, 1])
            #地图更新
            pygame.display.update()

        while not reset:
            screen.blit(font.render("Please speak loudly to restart!", True, (0,0,0)),(250,100))
            stream = pa.open(format=pyaudio.paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=NUM_SAMPLES)
            
            string_audio_data = stream.read(NUM_SAMPLES)
            k = max(struct.unpack('%dh'%(NUM_SAMPLES,), string_audio_data))
            stream.close()
            #gpio_1.light(k*8//32767)
            if k*8//32767 == 8:
                break
            pygame.display.update()
        #掉落界面
        score = 0

if __name__ == '__main__':
    main()
