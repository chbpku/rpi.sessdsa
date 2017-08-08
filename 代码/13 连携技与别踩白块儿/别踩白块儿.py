import pygame
from pygame import *
import time
from sakshat import SAKSHAT
from sakspins import SAKSPins as PINS
import random
import RPi.GPIO as GPIO

#screen = pygame.display.set_mode((640, 480), 0, 32)

GPIO.setmode(GPIO.BCM)  #采用BCM编码模式
SAKS = SAKSHAT()        #调用SAKSHAT模块
DS = 6                  # 控制LED灯的三个端口的BCM编码
SHCP = 19
STCP = 13


speed = 0.36            # set speed

def init():             # 初始化端口状态
    
    GPIO.setup(DS, GPIO.OUT)
    GPIO.setup(SHCP, GPIO.OUT)
    GPIO.setup(STCP, GPIO.OUT)
    
    GPIO.output(DS, GPIO.LOW)
    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(STCP, GPIO.LOW)

# 实现1到8对应流水灯的状态，i对应从左到右前i个LED灯亮
LEDlist = [0x00,0x01,0x03,0x07,0x0f,0x1f,0x3f,0x7f,0xff]
def writeBit(data):
    GPIO.output(DS, data)
    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(SHCP, GPIO.HIGH)

#写入8位LED的状态
def writeByte(data):
    for i in range (0, 8):
        writeBit((data >> i) & 0x01)
    #状态刷新信号
    GPIO.output(STCP, GPIO.LOW)
    GPIO.output(STCP, GPIO.HIGH)

# 燕园情简谱字符串，print用来显示在数字屏上
yyq_print = '''0003002350003002350035600561000656121232000300235000300235003560056100065612123100011600400165003003220320130001160040016500300322012032000553001005530030034405605400066300200613002003220120310000000116000165000116000465000553052061203500011600016500011600046500055305206120030001000'''
# string用来播放对应的音频文件
yyq_string = '''0006005610006005680068900894000212454565000600561000600568006890089400021245456400044900700498006006550650460004490070049800600655045065000116004001860060067708908700022600500946005006550450640000000449000498000449000798000116085024506800044900049800044900079800011608502450060004000'''



flag = []   # 列表，记录简谱字符串中的每个数字有没有被访问过，1表示没被访问过，0表示访问过
score = 0   # 得分，初始为0

music_print = yyq_print     # 封装
music_string = yyq_string
music_list = list(music_string)

for i in range(len(music_print)):
    flag += [1]


def tact_event_handler(pin, status):        # 用来捕捉按键事件的函数
    
    global __light_status,cst,t0,flag,score,LEDlist
    # 如果按右键
    if pin == PINS.TACT_RIGHT :
        # 判断是否按对
        if int(music_print[cst-1])%2 == 0 and flag[cst-1] == 1 and music_print[cst-1] != '0':
            score += 1 # 按对，得分加一
            flag[cst-1] = 0
            writeByte(LEDlist[score%9])

            pygame.mixer.music.load(sound[int(music_list[cst-1])])# 播放对应音高的音乐文件
            pygame.mixer.music.play()
            
    elif pin == PINS.TACT_LEFT :    #如果按下右键，和按下左键时情况对称
        if int(music_print[cst-1])%2 == 1 and flag[cst-1] == 1:
            score += 1
            flag[cst-1] = 0
            writeByte(LEDlist[score%9])
            pygame.mixer.music.load(sound[int(music_list[cst-1])])
            pygame.mixer.music.play()

            
            

# 制作翻译简谱字符串的字典
sound = {}

for i in range(1,4):
    
    sound[i] = '3%s.ogg' % ('GAB'[i-1])

for i in range(4,10):
    sound[i] = '4%s.ogg' % ('CDEFGA'[i-4])

sound[0] = 0






for cst in range(len(music_string)):        # 依次读取简谱字符串中的内容

    
    if sound[int(music_list[cst])] == 0:        # 如果读到0，那么对应位置不显示

        SAKS.digital_display.show(music_print[cst-1:cst+3].replace('0','#')) #切片显示，并将‘0’替换成‘#’
        time.sleep(speed)
        
        
    elif cst <= len(music_string) - 4:
        

        SAKS.digital_display.show(music_print[cst-1:cst+3].replace('0','#'))        
        
        SAKS.tact_event_handler = tact_event_handler

            
        time.sleep(speed)
        

    else:
        
        SAKS.digital_display.show('1###')        
        
        SAKS.tact_event_handler = tact_event_handler

        time.sleep(speed)


score = score  / (len(music_string) - music_string.count('0')) # 计算并展示最后得分
score = int(score * 100)
score = str(score)
while len(score)<4:
    score = '#'+score
    
SAKS.digital_display.show(score)
time.sleep(3)

writeByte(0x00) # 结束游戏
